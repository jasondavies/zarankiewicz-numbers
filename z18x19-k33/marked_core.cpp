#include "seven_columns.hpp"
#include <algorithm>

template<int rows>
struct MarkedCoreSearch {
    // The marked row is stored in the high bit of every incident column.
    static constexpr int outside = rows - 1;
    int min_squares = 0, max_squares = 10000;
    int width = 19, minimum_degree = 0;
    bool emit_cores = false;
    // Optional requirement for a row of core degree eight meeting this much column excess.
    int eight_excess = -1, marked_excess = 0;
    int k, m, t, total, peak, remaining_excess, missing, excess, score_without_squares;
    std::array<int, outside> capacity{}, degrees{};
    Lines fixed;
    std::array<std::array<Mask, outside>, outside> forbidden_triples{};
    std::array<Lines, rows> options;
    std::vector<int> weights;
    std::array<int, 21> future_weight{};
    int unused_capacity = 0, multiplier = 1;
    std::array<unsigned char, 1u << outside> pair_cache{};
    bool compatible_pair(Mask both) {
        if (std::popcount(both) * (minimum_degree - 2) > 2 * (m - 2)) return false;
        if (std::popcount(both) <= 2)
            return true;
        auto &result = pair_cache[both];
        if (!result) {
            result = 1;
            for (int i = 0; i < t; ++i)
                if (std::popcount(both & fixed[i]) > 2) {
                    result = 2;
                    break;
                }
        }
        if (result == 2)
            return false;
        for (size_t i = t; i < fixed.size(); ++i)
            if (std::popcount(both & fixed[i]) > 2)
                return false;
        return true;
    }
    unsigned long long cores = 0, profiles_checked = 0;

    // Allowed column supports on the rows outside the mark. Each two old
    // columns have already reserved their common row triples.
    void generate_supports(Mask rest, Mask chosen, int n, int high) {
        if (n >= 8)
            options[n].push_back(chosen);
        if (n >= high)
            return;
        while (std::popcount(rest) + n >= 8 && rest) {
            Mask bit = rest & -rest;
            rest ^= bit;
            Mask next = rest;
            int j = std::countr_zero(bit);
            for (Mask s = chosen; s; s &= s - 1)
                next &= ~forbidden_triples[j][std::countr_zero(s)];
            generate_supports(next, chosen | bit, n + 1, high);
        }
    }
    bool extend_core() {
        if (std::any_of(degrees.begin(), degrees.end(), [&](int d) { return d < minimum_degree; }))
            return false;
        if (eight_excess >= 0 && !(t == 8 && marked_excess >= eight_excess)) {
            bool found = false;
            for (int r = 0; r < outside; ++r)
                if (degrees[r] == 8 && peak - capacity[r] - 8 * multiplier >= eight_excess)
                    found = true;
            if (!found) return false;
        }
        ++cores;
        if (emit_cores) {
            std::cout << "core";
            for (auto x : fixed) std::cout << ' ' << x;
            std::cout << '\n';
        }
        LineExtensions<rows> ext;
        ext.fixed = fixed;
        if (!ext.run(k))
            return false;
        std::cout << "solution";
        for (Mask x : ext.fixed)
            std::cout << " " << x;
        std::cout << std::endl;
        return true;
    }
    // Each pool contains supports compatible with all previously fixed columns.
    // Equal weights share one pool and are selected in increasing support-index order.
    bool choose_columns(int at, const std::array<Lines, rows> &pools) {
        if (at == (int)weights.size())
            return extend_core();
        const Lines &pool = pools[weights[at]];
        int d = weights[at], coeff = d - 8 + multiplier;
        Mask allow = 0, must = 0;
        const int slots = int(weights.size()) - at;
        const bool uniform = d == weights.back();
        // A row can spend only a multiple of step when all remaining weights agree.
        auto waste = [&](int cap, int future, int step) {
            return std::max(cap - future, cap % step);
        };
        const int step = uniform ? coeff : 1;
        const int next_step = slots == 1 || weights[at + 1] != weights.back()
            ? 1 : weights.back() - 8 + multiplier;
        int inevitable = 0;
        for (int j = 0; j < outside; ++j) {
            if (capacity[j] >= coeff) allow |= 1u << j;
            inevitable += waste(capacity[j], future_weight[at], step);
            if (minimum_degree) {
                int need = std::max(0, minimum_degree - degrees[j]);
                if (need > slots || capacity[j] < future_weight[weights.size() - need])
                    return false;
                if (need == slots) must |= 1u << j;
            }
        }
        if (inevitable > unused_capacity || std::popcount(allow) < d) return false;
        for (int j = 0; j < outside; ++j) {
            const int others = inevitable - waste(capacity[j], future_weight[at], step);
            if (others + waste(capacity[j], future_weight[at + 1], next_step) > unused_capacity)
                must |= 1u << j;
            if (capacity[j] >= coeff &&
                others + waste(capacity[j] - coeff, future_weight[at + 1], next_step) > unused_capacity)
                allow &= ~(1u << j);
        }
        if ((must & ~allow) || std::popcount(must) > d)
            return false;
        // On each row, bound the largest excess it could reach at degree eight,
        // separately for taking and skipping the next column.
        if (eight_excess >= 0 && !(t == 8 && marked_excess >= eight_excess)) {
            Mask can_skip = 0, can_take = 0;
            for (int j = 0; j < outside; ++j) {
                int need = 8 - degrees[j];
                if (need < 0 || need > slots) continue;
                int excess_now = peak - capacity[j] - multiplier * degrees[j];
                int required = eight_excess - excess_now;
                if (need < slots && future_weight[at + 1] - future_weight[at + 1 + need]
                                       - multiplier * need >= required) can_skip |= 1u << j;
                if (need && future_weight[at] - future_weight[at + need]
                                       - multiplier * need >= required) can_take |= 1u << j;
            }
            can_skip &= ~must;
            can_take &= allow;
            Mask possible = can_skip | can_take;
            if (!possible) return false;
            if (std::has_single_bit(possible)) {
                if (!can_skip) must |= possible;
                if (!can_take) allow &= ~possible;
            }
        }
        for (size_t i = 0; i < pool.size(); ++i) {
            Mask a = pool[i];
            if ((a & ~allow) || (a & must) != must)
                continue;
            std::array<Lines, rows> next;
            bool ok = true;
            for (int h = at + 1; h < (int)weights.size(); ++h) {
                if (h > at + 1 && weights[h] == weights[h - 1])
                    continue;
                const auto &old = pools[weights[h]];
                auto &out = next[weights[h]];
                Mask permitted = 0;
                const int coefficient = weights[h] - 8 + multiplier;
                for (int bit = 0; bit < outside; ++bit)
                    if (capacity[bit] - int((a >> bit) & 1u) * coeff >= coefficient)
                        permitted |= 1u << bit;
                const size_t first = (weights[h] == d) ? i + 1 : 0;
                for (size_t j = first; j < old.size(); ++j) {
                    if (old[j] & ~permitted)
                        continue;
                    Mask both = a & old[j];
                    if (compatible_pair(both))
                        out.push_back(old[j]);
                }
                int needed = std::count(weights.begin() + h, weights.end(), weights[h]);
                if ((int)out.size() < needed) {
                    ok = false;
                    break;
                }
            }
            if (!ok)
                continue;
            for (Mask s = a; s; s &= s - 1) {
                int j = std::countr_zero(s);
                capacity[j] -= coeff;
                ++degrees[j];
            }
            fixed.push_back(a);
            if (choose_columns(at + 1, next))
                return true;
            fixed.pop_back();
            for (Mask s = a; s; s &= s - 1) {
                int j = std::countr_zero(s);
                capacity[j] += coeff;
                --degrees[j];
            }
        }
        return false;
    }
    // Partition the remaining excess into nonincreasing column degrees minus eight.
    bool try_degree_profile(int left, int extra, int high, int sq) {
        if (score_without_squares + sq + extra > rows * peak || sq + extra > max_squares)
            return false;
        if (!left) {
            if (extra || sq < min_squares)
                return false;
            ++profiles_checked;
            unused_capacity = rows * peak - (score_without_squares + sq);
            std::array<Lines, rows> pools;
            for (int j = int(weights.size()) - 1; j >= 0; --j) {
                int d = weights[j];
                future_weight[j] = future_weight[j + 1] + d - 8 + multiplier;
                if (options[d].empty())
                    return false;
                if (j + 1 == int(weights.size()) || d != weights[j + 1])
                    pools[d] = options[d];
            }
            return choose_columns(0, pools);
        }
        for (int e = std::min({high, extra, outside - 8}); e * left >= extra; --e) {
            weights.push_back(8 + e);
            if (try_degree_profile(left - 1, extra - e, e, sq + e * e))
                return true;
            weights.pop_back();
        }
        return false;
    }
    bool run(int count, int points, const Lines &blocks, int goal, int alpha) {
        multiplier = alpha;
        k = count;
        m = width - k;
        t = points;
        if (t < minimum_degree) return false;
        total = goal - 7 * k;
        missing = m - t;
        excess = total - 8 * m;
        score_without_squares = multiplier * total + 8 * excess;
        fixed.assign(t, 1u << outside);
        std::array<int, rows> coefficients{};
        for (int j = 0; j < outside; ++j)
            for (Mask s = blocks[j]; s; s &= s - 1)
                fixed[std::countr_zero(s)] |= 1u << j;
        int accumulated = 0, sq = 0;
        for (int i = 0; i < t; ++i) {
            int e = std::popcount(fixed[i]) - 8;
            if (e < 0)
                return false;
            accumulated += e;
            sq += e * e;
            coefficients[i] = multiplier + e;
        }
        marked_excess = accumulated;
        peak = multiplier * t + accumulated;
        remaining_excess = excess - accumulated;
        if (sq + remaining_excess > max_squares || rows * peak < score_without_squares + excess ||
            remaining_excess < 0 || missing < 0 ||
            score_without_squares + sq + remaining_excess > rows * peak)
            return false;
        for (int j = 0; j < outside; ++j) {
            capacity[j] = peak;
            degrees[j] = std::popcount(blocks[j]);
            for (Mask s = blocks[j]; s; s &= s - 1)
                capacity[j] -= coefficients[std::countr_zero(s)];
            if (capacity[j] < 0)
                return false;
        }
        for (int j = 0; j < outside; ++j)
            for (int i = 0; i < j; ++i) {
                Mask both = blocks[j] & blocks[i];
                for (int h = 0; h < i; ++h)
                    if (std::popcount(both & blocks[h]) >= 2)
                        forbidden_triples[i][h] |= 1u << j;
            }
        if (missing)
            generate_supports((1u << outside) - 1, 0, 0, std::min(outside, 8 + remaining_excess));
        return try_degree_profile(missing, remaining_excess, outside - 8, sq);
    }
};
template<int rows>
int search(int argc, char **argv, int k, int t, int target, int alpha, int width) {
    std::string line;
    unsigned long long n = 0, c = 0, p = 0;
    while (std::getline(std::cin, line)) {
        Lines b;
        std::istringstream in(line);
        for (Mask a; in >> a;) {
            if (a >= (1u << t))
                return 2;
            b.push_back(a);
        }
        if (b.size() != rows - 1)
            return 2;
        MarkedCoreSearch<rows> check;
        check.width = width;
        if (argc >= 10) check.minimum_degree = std::stoi(argv[9]);
        if (argc >= 11) check.eight_excess = std::stoi(argv[10]);
        check.emit_cores = argc == 12;
        if (check.minimum_degree < 0 || check.minimum_degree > width ||
            check.eight_excess < -1) return 2;
        if (argc >= 7) {
            check.min_squares = std::stoi(argv[5]);
            check.max_squares = std::stoi(argv[6]);
        }
        if (check.run(k, t, b, target, alpha))
            return 0;
        ++n;
        c += check.cores;
        p += check.profiles_checked;
    }
    std::cout << "excluded " << n << " cores " << c << " profiles " << p << '\n';
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 3 || argc > 12 || argc == 6)
        return 2;
    if (argc == 12 && std::string(argv[11]) != "--emit-cores") return 2;
    int k = std::stoi(argv[1]), t = std::stoi(argv[2]);
    const int width = argc >= 8 ? std::stoi(argv[7]) : 19;
    if ((width < 19 || width > 21) || k < 0 || k > width - 10 || t < 2 || t > 12)
        return 2;
    const int target = argc >= 4 ? std::stoi(argv[3]) : 157;
    const int alpha = argc >= 5 ? std::stoi(argv[4]) : 1;
    if (alpha < 1 || alpha > 2)
        return 2;
    // Optional trailing arguments are row count, minimum core row degree, and
    // required excess on some eight-row. The original 18-row invocation is the default.
    if (argc >= 9) {
        const int rows = std::stoi(argv[8]);
        if (rows == 19)
            return search<19>(argc, argv, k, t, target, alpha, width);
        if (rows != 18) return 2;
    }
    return search<18>(argc, argv, k, t, target, alpha, width);
}
