// Match two complete nine-column projections and finish their union.
#include "heavy_completion.hpp"
#include <map>
#include <sstream>
#include <string>

using Blocks = std::array<Mask, 16>;

struct Star {
    Blocks blocks;
    std::array<Mask, 9> rows{};
    std::vector<unsigned char> legal, pair_ok;

    explicit Star(const Blocks& b) : blocks(b) {
        for (int i = 0; i < 9; ++i)
            for (int j = 0; j < 16; ++j) rows[i] |= ((b[j] >> i) & 1) << j;
    }

    void prepare_left() {
        legal.assign(65536, 1);
        pair_ok.assign(65536, 1);
        for (int x = 0; x < 16; ++x)
            for (int y = 0; y < x; ++y)
                for (int z = 0; z < y; ++z) {
                    Mask m = (1u << x) | (1u << y) | (1u << z);
                    int count = 0;
                    for (auto r : rows) count += (r & m) == m;
                    if (count) pair_ok[m] = 0;
                    if (count >= 2) legal[m] = 0;
                }
        // A mask inherits every forbidden triple from its subsets.
        for (int j = 0; j < 16; ++j)
            for (int base = 0; base < 65536; base += 2 << j)
                for (int x = base; x < base + (1 << j); ++x) {
                    legal[x + (1 << j)] &= legal[x];
                    pair_ok[x + (1 << j)] &= pair_ok[x];
                }
    }
};

struct View {
    int star, peer;
    std::array<int, 15> order{}; // columns ordered by trace on the common rows
    Rows extra;                 // rows incident only with this mark
};
struct Bucket { std::vector<View> left, right; };
using Index = std::map<std::string, Bucket>;

void index_star(Index& index, const Star& star, int id, int overlap, bool use_left) {
    for (int j = 0; j < 16; ++j) {
        Mask shared = star.blocks[j];
        if (std::popcount(shared) != overlap) continue;
        std::vector<int> points;
        for (int i = 0; i < 9; ++i)
            if ((shared >> i) & 1) points.push_back(i);

        std::string best;
        std::vector<View> views;
        do {
            int deficit = 0;
            for (int i = 0; i < overlap; ++i)
                if (std::popcount(star.rows[points[i]]) == 6) deficit |= 1 << i;
            std::array<std::pair<int, int>, 15> columns;
            int n = 0;
            for (int k = 0; k < 16; ++k) {
                if (k == j) continue;
                int trace = 0;
                for (int i = 0; i < overlap; ++i)
                    trace |= ((star.blocks[k] >> points[i]) & 1) << i;
                columns[n++] = {trace, k};
            }
            std::sort(columns.begin(), columns.end());
            std::string key(1, char(deficit));
            View view{id, j, {}, {}};
            for (int k = 0; k < 15; ++k) {
                key += char(columns[k].first);
                view.order[k] = columns[k].second;
            }
            if (!best.empty() && key > best) continue;
            if (best.empty() || key < best) {
                best = key;
                views.clear();
            }
            for (int i = 0; i < 9; ++i)
                if (!((shared >> i) & 1)) view.extra.push_back(star.rows[i]);
            if (std::none_of(views.begin(), views.end(), [&](const View& v) {
                    return v.order == view.order;
                })) views.push_back(view);
        } while (std::next_permutation(points.begin(), points.end()));
        auto& group = index[best];
        if (use_left) group.left.push_back(views.front());
        group.right.insert(group.right.end(), views.begin(), views.end());
    }
}

struct Parts { Mask source, target; };
using Partition = std::vector<Parts>;

struct Counts { uint64_t alignments = 0, unions = 0, completions = 0; };

struct Join {
    const Star& star;
    const View& left;
    const View& right;
    const std::array<RowLayer, 3>& layers;
    Counts& counts;
    bool emit_union;
    Rows extra;

    void rows(const Partition& parts, size_t depth) {
        if (depth == right.extra.size()) {
            ++counts.unions;
            Rows full;
            for (Mask r : star.rows) full.push_back(r | (1u << 16));
            full.insert(full.end(), extra.begin(), extra.end());
            if (emit_union) {
                std::cout << "union " << left.star << ' ' << left.peer << ' '
                          << right.star << ' ' << right.peer;
                for (auto r : full) std::cout << ' ' << r;
                std::cout << '\n';
            } else {
                counts.completions += HeavyCompletion(layers, full, left.peer).run();
            }
            return;
        }
        Partition next;
        next.reserve(15);
        image(parts, 0, right.extra[depth], 1u << left.peer, next, depth);
    }

    void image(const Partition& parts, size_t i, Mask row, Mask candidate,
               Partition& next, size_t depth) {
        if (!star.legal[candidate]) return;
        if (i == parts.size()) {
            for (auto m : extra)
                if (!star.pair_ok[m & candidate]) return;
            extra.push_back(candidate);
            rows(next, depth + 1);
            extra.pop_back();
            return;
        }
        auto [source, target] = parts[i];
        Mask take = source & row;
        if (!take || take == source) {
            next.push_back(parts[i]);
            image(parts, i + 1, row, candidate | (take ? target : 0), next, depth);
            next.pop_back();
            return;
        }
        // Within one trace class any subset of the required size is an image.
        // Splitting the class preserves all column bijections for later rows.
        for (Mask x = target; x; x = (x - 1) & target) {
            if (std::popcount(x) != std::popcount(take)) continue;
            next.push_back({take, x});
            next.push_back({source ^ take, target ^ x});
            image(parts, i + 1, row, candidate | x, next, depth);
            next.pop_back();
            next.pop_back();
        }
    }
};

int main(int argc, char** argv) {
    if (argc != 4 && argc != 5) return 2;
    int overlap = std::stoi(argv[1]), first = std::stoi(argv[2]), last = std::stoi(argv[3]);
    bool emit_union = argc == 5 && std::string(argv[4]) == "--unions";
    if ((argc == 5 && !emit_union) || overlap < 2 || overlap > 5 || first < 0 || last < first)
        return 2;
    std::vector<Star> stars;
    Index index;
    for (std::string line; std::getline(std::cin, line);) {
        std::istringstream in(line);
        Blocks blocks;
        int sum = 0;
        for (auto& x : blocks) {
            if (!(in >> x) || x >= 512) return 2;
            sum += std::popcount(x);
        }
        std::string trailing;
        if (in >> trailing || sum != 62) return 2;
        int id = stars.size();
        auto& star = stars.emplace_back(blocks);
        bool use_left = first <= id && id < last;
        if (use_left) star.prepare_left();
        index_star(index, star, id, overlap, use_left);
    }
    if (last > int(stars.size())) return 2;
    std::array<RowLayer, 3> layers{RowLayer(6), RowLayer(7), RowLayer(8)};
    Counts counts;
    for (const auto& [key, bucket] : index)
        for (const auto& a : bucket.left)
            for (const auto& b : bucket.right) {
                if (a.star > b.star) continue;
                Partition parts;
                for (int i = 0; i < 15;) {
                    int j = i;
                    Mask source = 0, target = 0;
                    do {
                        source |= 1u << b.order[j];
                        target |= 1u << a.order[j];
                        ++j;
                    } while (j < 15 && key[i + 1] == key[j + 1]);
                    parts.push_back({source, target});
                    i = j;
                }
                std::sort(parts.begin(), parts.end(), [](Parts p, Parts q) {
                    return std::popcount(p.source) < std::popcount(q.source);
                });
                ++counts.alignments;
                Join search{stars[a.star], a, b, layers, counts, emit_union, {}};
                search.rows(parts, 0);
            }
    std::cout << "counts " << counts.alignments << ' ' << counts.unions << ' '
              << counts.completions << '\n';
}
