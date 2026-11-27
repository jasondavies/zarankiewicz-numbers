// Canonical multisets of blocks on at most twelve points.
#pragma once
#include <algorithm>
#include <bit>
#include <set>
#include <stdexcept>
#include <vector>
#include <nauty/nauty.h>

using Blocks = std::vector<unsigned>;

inline Blocks canonical_blocks(int points, const Blocks& blocks) {
    int n = points + blocks.size();
    if (n > WORDSIZE) throw std::logic_error("graph exceeds one nauty word");
    graph g[WORDSIZE]{}, canonical[WORDSIZE]{};
    int lab[WORDSIZE], partition[WORDSIZE], orbits[WORDSIZE];
    for (int i = 0; i < n; ++i) {
        lab[i] = i;
        partition[i] = (i != points - 1 && i != n - 1);
    }
    for (size_t i = 0; i < blocks.size(); ++i)
        for (int j = 0; j < points; ++j)
            if (blocks[i] & (1u << j)) { ADDONEEDGE(g, points + i, j, 1); }
    DEFAULTOPTIONS_GRAPH(options);
    options.defaultptn = FALSE;
    options.getcanon = TRUE;
    statsblk stats;
    densenauty(g, lab, partition, orbits, &options, &stats, 1, n, canonical);
    Blocks result(blocks.size());
    for (int j = 0; j < points; ++j) {
        if (lab[j] >= points) throw std::logic_error("point partition changed");
        for (size_t i = 0; i < blocks.size(); ++i)
            result[i] |= ((blocks[i] >> lab[j]) & 1u) << j;
    }
    std::sort(result.begin(), result.end());
    return result;
}

inline bool fits(unsigned mask, const Blocks& blocks) {
    return std::all_of(blocks.begin(), blocks.end(), [mask](unsigned b) {
        return std::popcount(mask & b) <= 2;
    });
}
