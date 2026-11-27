// Complete the fixed five-row projections of starts 4, 25, 46 and 62 at total weight 209.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string_view>
#include <utility>
#include <vector>

using Mask = std::uint32_t;
using Rows = std::vector<Mask>;
using Side = std::array<Rows, 3>;
using Pools = std::array<Rows, 4>;
constexpr int core_width = 19;
constexpr Mask core = (1U << core_width) - 1;
constexpr int target = 209;
int weight(Mask row) { return std::popcount(row); }

bool compatible(Mask a, Mask b, const Rows& fixed) {
    const Mask shared = a & b;
    if (weight(shared) > 6) return false;
    for (Mask f : fixed) if (weight(f & shared) > 2) return false;
    return true;
}

// Each pool is sorted by decreasing weight. Rows within the same pool
// are interchangeable and are always chosen in increasing index order.
bool finish(const Pools& pool, std::array<int, 4> need, Rows& fixed,
            int total, std::uint64_t& nodes) {
    ++nodes;
    int chosen = -1, upper = total, slots = 0;
    for (int k = 0; k < int(need.size()); ++k) {
        if (!need[k]) continue;
        if (int(pool[k].size()) < need[k]) return false;
        for (int i = 0; i < need[k]; ++i) upper += weight(pool[k][i]);
        slots += need[k];
        if (chosen < 0 || pool[k].size()*need[chosen] < pool[chosen].size()*need[k]) chosen = k;
    }
    if (upper < target) return false;
    if (!slots) return true;
    Mask required = 0;
    if (slots <= 8) {
        for (int j = 0; j < core_width; ++j) {
            int degree = 0;
            for (Mask f : fixed) degree += (f >> j) & 1U;
            if (degree + slots < 8) return false;
            if (degree + slots == 8) required |= 1U << j;
        }
    }
    --need[chosen];
    for (size_t i = 0; i + need[chosen] < pool[chosen].size(); ++i) {
        const Mask a = pool[chosen][i];
        if ((a & required) != required) continue;
        if (slots == 1) {
            if (total + weight(a) < target) break;
            fixed.push_back(a);
            return true;
        }
        Pools next;
        bool enough = true;
        for (int k = 0; k < int(need.size()) && enough; ++k) {
            if (!need[k]) continue;
            for (size_t j = k == chosen ? i+1 : 0; j < pool[k].size(); ++j) {
                const Mask b = pool[k][j];
                if ((b & required) == required && compatible(a,b,fixed)) next[k].push_back(b);
            }
            enough = int(next[k].size()) >= need[k];
        }
        if (!enough) continue;
        fixed.push_back(a);
        if (finish(next, need, fixed, total + weight(a), nodes)) return true;
        fixed.pop_back();
    }
    return false;
}

using Limits = std::vector<std::pair<Mask, int>>;
Limits limits(const Rows& fixed, Mask marks, size_t first = 0) {
    Limits caps;
    for (size_t i = first; i < fixed.size(); ++i) {
        for (size_t j = 0; j < i; ++j) {
            const Mask common = fixed[i] & fixed[j];
            caps.emplace_back(common & core, 2-weight(common & marks));
        }
    }
    std::sort(caps.begin(), caps.end(), [](auto a, auto b) {
        return a.second - weight(a.first) < b.second - weight(b.first);
    });
    return caps;
}
bool fits(Mask r, const Limits& caps) {
    for (auto [set, limit] : caps) if (weight(set & r) > limit) return false;
    return true;
}
Rows domain(const Rows& fixed, Mask type) {
    Rows out;
    const Mask marks = type << core_width;
    const Limits caps = limits(fixed, marks);
    for (Mask r = 0; r <= core; ++r) {
        if (weight(r) >= 8 && fits(r,caps)) out.push_back(r | marks);
    }
    return out;
}

// Sort columns lexicographically on the fixed rows. Equal neighbouring
// columns may still be exchanged. Within each interchangeable row class
// a completion with descending row and column order exists by taking the
// lexicographically greatest row-major matrix among all permitted images.
constexpr std::array<int, 6> side_types{10, 10, 9, 4, 4, 4};
constexpr std::array<int, 6> pool_ids{0, 0, 1, 2, 2, 2};
constexpr std::array<Mask, 4> tail_types{1, 2, 0, 3};
constexpr std::array<int, 4> start_ids{4, 25, 46, 62};

struct Counts {
    std::uint64_t first_side = 0;
    std::uint64_t both_sides = 0;
    std::array<std::uint64_t, 4> nodes{};
};

bool place_sides(int depth, Mask equal, const Side& side, const Pools& base,
                 Rows& fixed, Counts& counts, int endings) {
    Pools filtered;
    const Pools* tail = &base;
    if (depth == 3 || depth == 6) {
        // A tail candidate already fits every pair of rows present at the
        // previous filter. Check the pairs involving a newly inserted row.
        for (size_t t = 0; t < base.size(); ++t) {
            if (base[t].empty()) continue;
            const Limits caps = limits(fixed, tail_types[t] << core_width, depth == 3 ? 5 : 8);
            for (Mask r : base[t]) if (fits(r, caps)) filtered[t].push_back(r);
        }
        if (depth == 6) {
            ++counts.both_sides;
            int sum = 0;
            for (Mask r : fixed) sum += weight(r);
            for (int t = 0; t < endings; ++t) {
                if (finish(filtered, {5-t, 4-t, 1+t, t}, fixed, sum, counts.nodes[t])) {
                    std::cerr << "Start " << start_ids[t] << ' ';
                    return true;
                }
            }
            return false;
        }
        ++counts.first_side;
        tail = &filtered;
    }
    for (Mask a : side[pool_ids[depth]]) {
        // equal contains the left edge of each still-equal adjacent column pair.
        if ((~a & (a >> 1) & equal) != 0) continue;
        if (depth > 0 && side_types[depth-1] == side_types[depth]) {
            const Mask diff = (fixed.back() ^ a) & core;
            if (!diff || !(fixed.back() & (diff & -diff))) continue;
        }
        Side next;
        for (int t = 0; t < 3; ++t) {
            if (std::find(pool_ids.begin()+depth+1, pool_ids.end(), t) == pool_ids.end()) continue;
            for (Mask b : side[t]) if (compatible(a, b, fixed)) next[t].push_back(b);
        }
        fixed.push_back(a);
        if (place_sides(depth+1, equal & ~(a ^ (a >> 1)), next, *tail, fixed, counts, endings)) return true;
        fixed.pop_back();
    }
    return false;
}

int main(int argc, char** argv) {
    const bool shared = argc == 2 && std::string_view(argv[1]) == "--shared-tails";
    if (argc != 1 && !shared) throw std::runtime_error("expected no options or --shared-tails");
    const int endings = shared ? 4 : 1;
    int h;
    while (std::cin >> h) {
        Rows fixed(5);
        constexpr std::array<unsigned, 5> types{15, 15, 12, 12, 12};
        Mask equal = (1U << (core_width-1)) - 1;
        for (size_t i = 0; i < fixed.size(); ++i) {
            if (!(std::cin >> fixed[i]) || (fixed[i] >> core_width) != types[i])
                throw std::runtime_error("unexpected fixed row");
            equal &= ~(fixed[i] ^ (fixed[i] >> 1));
        }
        const Side side{domain(fixed, 10), domain(fixed, 9), domain(fixed, 4)};
        Pools base{domain(fixed, 1), domain(fixed, 2), domain(fixed, 0), {}};
        if (shared) base[3] = domain(fixed, 3);
        for (Rows& rows : base) {
            std::sort(rows.begin(), rows.end(), [](Mask x, Mask y) { return weight(x) > weight(y); });
        }
        Counts counts;
        if (place_sides(0, equal, side, base, fixed, counts, endings)) {
            std::cerr << "Found matrix for " << h;
            for (Mask r : fixed) std::cerr << ' ' << r;
            std::cerr << '\n';
            return 10;
        }
        std::cout << h << ' ' << counts.first_side << ' ' << counts.both_sides;
        for (int t = 0; t < endings; ++t) std::cout << ' ' << counts.nodes[t];
        std::cout << std::endl;
    }
    return std::cin.eof() ? 0 : 1;
}
