#include "seven_columns.hpp"
#include <algorithm>

struct MarkedCoreSearch {
    int min_squares = 0, max_squares = 10000;
    int k, m, t, total, peak, remaining_excess, missing, excess, score_without_squares;
    std::array<int, 17> capacity{};
    Lines fixed;
    std::array<std::array<Mask, 17>, 17> forbidden_triples{};
    std::array<Lines, 18> options;
    std::vector<int> weights;
    std::array<int, 18> future_weight{};
    int unused_capacity = 0, multiplier = 1;
    std::array<unsigned char, 1u << 17> pair_cache{};
    bool compatible_pair(Mask both) {
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
        ++cores;
        Extensions ext;
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
    bool choose_columns(int at, const std::array<Lines, 18> &pools) {
        if (at == (int)weights.size())
            return extend_core();
        const Lines &pool = pools[weights[at]];
        int d = weights[at], coeff = d - 8 + multiplier;
        Mask allow = 0, must = 0;
        int inevitable = 0;
        for (int j = 0; j < 17; ++j) {
            if (capacity[j] >= coeff)
                allow |= 1u << j;
            inevitable += std::max(0, capacity[j] - future_weight[at]);
        }
        // Even a row present in every remaining column can absorb only future_weight[at].
        if (inevitable > unused_capacity || std::popcount(allow) < d)
            return false;
        for (int j = 0; j < 17; ++j)
            if (inevitable + std::max(0, capacity[j] - future_weight[at + 1]) -
                    std::max(0, capacity[j] - future_weight[at]) >
                unused_capacity)
                must |= 1u << j;
        if ((must & ~allow) || std::popcount(must) > d)
            return false;
        for (size_t i = 0; i < pool.size(); ++i) {
            Mask a = pool[i];
            if ((a & ~allow) || (a & must) != must)
                continue;
            std::array<Lines, 18> next;
            bool ok = true;
            for (int h = at + 1; h < (int)weights.size(); ++h) {
                if (h > at + 1 && weights[h] == weights[h - 1])
                    continue;
                const auto &old = pools[weights[h]];
                auto &out = next[weights[h]];
                Mask permitted = 0;
                const int coefficient = weights[h] - 8 + multiplier;
                for (int bit = 0; bit < 17; ++bit)
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
            for (Mask s = a; s; s &= s - 1)
                capacity[std::countr_zero(s)] -= coeff;
            fixed.push_back(a);
            if (choose_columns(at + 1, next))
                return true;
            fixed.pop_back();
            for (Mask s = a; s; s &= s - 1)
                capacity[std::countr_zero(s)] += coeff;
        }
        return false;
    }
    // Partition the remaining excess into nonincreasing column degrees minus eight.
    bool try_degree_profile(int left, int extra, int high, int sq) {
        if (score_without_squares + sq + extra > 18 * peak || sq + extra > max_squares)
            return false;
        if (!left) {
            if (extra || sq < min_squares)
                return false;
            ++profiles_checked;
            unused_capacity = 18 * peak - (score_without_squares + sq);
            std::array<Lines, 18> pools;
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
        for (int e = std::min({high, extra, 9}); e * left >= extra; --e) {
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
        m = 19 - k;
        t = points;
        total = goal - 7 * k;
        missing = m - t;
        excess = total - 8 * m;
        score_without_squares = multiplier * total + 8 * excess;
        fixed.assign(t, 1u << 17);
        std::array<int, 18> coefficients{};
        for (int j = 0; j < 17; ++j)
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
        peak = multiplier * t + accumulated;
        remaining_excess = excess - accumulated;
        if (sq + remaining_excess > max_squares || 18 * peak < score_without_squares + excess ||
            remaining_excess < 0 || missing < 0 ||
            score_without_squares + sq + remaining_excess > 18 * peak)
            return false;
        for (int j = 0; j < 17; ++j) {
            capacity[j] = peak;
            for (Mask s = blocks[j]; s; s &= s - 1)
                capacity[j] -= coefficients[std::countr_zero(s)];
            if (capacity[j] < 0)
                return false;
        }
        for (int j = 0; j < 17; ++j)
            for (int i = 0; i < j; ++i) {
                Mask both = blocks[j] & blocks[i];
                for (int h = 0; h < i; ++h)
                    if (std::popcount(both & blocks[h]) >= 2)
                        forbidden_triples[i][h] |= 1u << j;
            }
        if (missing)
            generate_supports((1u << 17) - 1, 0, 0, std::min(17, 8 + remaining_excess));
        return try_degree_profile(missing, remaining_excess, 9, sq);
    }
};
int main(int argc, char **argv) {
    if (argc < 3 || argc > 7 || argc == 6)
        return 2;
    int k = std::stoi(argv[1]), t = std::stoi(argv[2]);
    if (k < 0 || k > 9 || t < 2 || t > 10)
        return 2;
    const int target = argc >= 4 ? std::stoi(argv[3]) : 157;
    const int alpha = argc >= 5 ? std::stoi(argv[4]) : 1;
    if (alpha < 1 || alpha > 2)
        return 2;
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
        if (b.size() != 17)
            return 2;
        MarkedCoreSearch check;
        if (argc == 7) {
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
}
