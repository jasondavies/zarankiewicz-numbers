// Enumerate the nine-point neighbourhoods of a marked line.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>
#include <nauty/nauty.h>

using Mask = unsigned;
using Blocks = std::vector<Mask>;
constexpr Mask pivot = 1u << 8;

bool compatible(Mask x, const Blocks& blocks) {
    return std::all_of(blocks.begin(), blocks.end(), [x](Mask y) {
        return std::popcount(x & y) <= 2;
    });
}

// Equal keys are literally the same multiset after a permutation of the nine points.
Blocks key(const Blocks& blocks) {
    int n = 9 + blocks.size();
    graph g[25]{}, canonical[25]{};
    int lab[25], partition[25], orbits[25];
    for (int i = 0; i < n; ++i) {
        lab[i] = i;
        partition[i] = (i != 8 && i != n-1);
    }
    for (size_t i = 0; i < blocks.size(); ++i)
        for (int j = 0; j < 9; ++j)
            if (blocks[i] & (1u << j)) { ADDONEEDGE(g, 9+i, j, 1); }
    DEFAULTOPTIONS_GRAPH(options);
    options.defaultptn = FALSE;
    options.getcanon = TRUE;
    statsblk stats;
    densenauty(g, lab, partition, orbits, &options, &stats, 1, n, canonical);
    Blocks ordered(blocks.size());
    for (int j = 0; j < 9; ++j) {
        if (lab[j] < 0 || lab[j] >= 9) throw std::logic_error("point partition changed");
        for (size_t i = 0; i < blocks.size(); ++i)
            ordered[i] |= ((blocks[i] >> lab[j]) & 1u) << j;
    }
    std::sort(ordered.begin(), ordered.end());
    return ordered;
}

class Catalogue {
    int lines, minimum_weight, deficit_limit, minimum_load, maximum_load;
    std::array<Blocks,6> by_size;
    Blocks triples;
    std::vector<std::array<unsigned char,56>> images;
    std::unordered_set<uint64_t> pivot_orbits;
    std::set<Blocks> large_seen, complete_seen;

    // A useful pivot is in the maximum number of four-blocks. The four-blocks
    // through it are exactly triples on eight points with pair intersections <= 1.
    bool new_pivot_orbit(uint64_t chosen) {
        if (pivot_orbits.contains(chosen)) return false;
        for (const auto& perm : images) {
            uint64_t image = 0;
            for (auto s = chosen; s; s &= s-1)
                image |= uint64_t(1) << perm[std::countr_zero(s)];
            pivot_orbits.insert(image);
        }
        return true;
    }

    bool possible_loads(const Blocks& blocks, int left) const {
        int deficit = 0;
        for (int j = 0; j < 9; ++j) {
            int d = 0;
            for (auto b : blocks) d += (b >> j) & 1u;
            if (d > maximum_load || d+left < minimum_load) return false;
            deficit += std::max(0, 7-d-left);
        }
        return deficit <= deficit_limit;
    }

    void small(Blocks& blocks, const Blocks& choices, size_t start, int weight) {
        int left = lines - blocks.size();
        if (weight + 3*left < minimum_weight || !possible_loads(blocks, left)) return;
        if (left == 0) {
            complete_seen.insert(key(blocks));
            return;
        }
        for (size_t i = start; i < choices.size(); ++i) {
            Mask b = choices[i];
            int d = std::popcount(b);
            if (weight + left*d < minimum_weight) break;
            // Distinct small masks intersect in at most two points. Repetition
            // of a triple is forbidden, but a pair or smaller mask may recur.
            blocks.push_back(b);
            small(blocks, choices, i+(d==3), weight+d);
            blocks.pop_back();
        }
    }

    void off_pivot(Blocks& blocks, const Blocks& pool, int p, int fours, int weight) {
        int left = lines - blocks.size();
        if (weight + 3*left + std::min(left, int(pool.size())) < minimum_weight) return;
        if (!possible_loads(blocks, left)) return;
        if (weight + 3*left >= minimum_weight) {
            auto base = key(blocks);
            if (large_seen.insert(base).second) {
                Blocks tail;
                for (int d = 3; d >= 0; --d)
                    for (auto b : by_size[d]) if (compatible(b,base)) tail.push_back(b);
                small(base, tail, 0, weight);
            }
        }
        if (!left || 4*(fours+1) > 9*p) return;
        for (size_t i = 0; i < pool.size(); ++i) {
            Blocks rest;
            for (size_t j = i+1; j < pool.size(); ++j)
                if (std::popcount(pool[i]&pool[j]) <= 2) rest.push_back(pool[j]);
            blocks.push_back(pool[i]);
            off_pivot(blocks, rest, p, fours+1, weight+4);
            blocks.pop_back();
        }
    }

    void fives(Blocks& blocks, size_t start, int p, int m) {
        int required_fours = minimum_weight - 3*lines - 2*m;
        if (9*p >= 4*required_fours) {
            Blocks rest;
            for (auto b : by_size[4])
                if (!(b & pivot) && compatible(b,blocks)) rest.push_back(b);
            off_pivot(blocks, rest, p, p, 4*p+5*m);
        }
        if (m == 3) return;
        for (size_t i = start; i < by_size[5].size(); ++i) {
            auto b = by_size[5][i];
            if (!compatible(b, blocks)) continue;
            blocks.push_back(b);
            fives(blocks, i+1, p, m+1);
            blocks.pop_back();
        }
    }

    void pivot_triples(uint64_t chosen, size_t start, Blocks& blocks) {
        int p = blocks.size();
        if (9*p >= 4*(minimum_weight-3*lines-6) && new_pivot_orbit(chosen))
            fives(blocks, 0, p, 0);
        if (p == 8) return;
        for (size_t i = start; i < triples.size(); ++i) {
            auto b = pivot | triples[i];
            if (!compatible(b, blocks)) continue;
            blocks.push_back(b);
            pivot_triples(chosen | (uint64_t(1)<<i), i+1, blocks);
            blocks.pop_back();
        }
    }

public:
    explicit Catalogue(bool column) :
        lines(column?16:15), minimum_weight(column?62:60), deficit_limit(column?1:3),
        minimum_load(column?6:5), maximum_load(column?16:7) {
        for (Mask b = 0; b < 512; ++b) {
            int d = std::popcount(b);
            if (d <= 5) by_size[d].push_back(b);
            if (!(b & pivot) && d == 3) triples.push_back(b);
        }
        std::array<int,256> index{};
        for (size_t i = 0; i < triples.size(); ++i) index[triples[i]] = i;
        std::array<int,8> perm{0,1,2,3,4,5,6,7};
        do {
            std::array<unsigned char,56> action{};
            for (size_t i = 0; i < triples.size(); ++i) {
                Mask image = 0;
                for (Mask s = triples[i]; s; s &= s-1)
                    image |= 1u << perm[std::countr_zero(s)];
                action[i] = index[image];
            }
            images.push_back(action);
        } while (std::next_permutation(perm.begin(), perm.end()));
    }

    void run() {
        Blocks blocks;
        pivot_triples(0, 0, blocks);
        for (const auto& projection : complete_seen) {
            for (auto b : projection) std::cout << b << ' ';
            std::cout << '\n';
        }
    }
};

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    const std::string mode=argv[1];
    if (mode!="column" && mode!="row") return 2;
    Catalogue(mode=="column").run();
}
