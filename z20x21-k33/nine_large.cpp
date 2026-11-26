// Enumerate nine-point block multisets by first fixing all blocks of size four or five.
// Nineteen blocks, pairwise intersections at most two, block sizes at most five,
// loads between low and high, and total at least minimum.
#include "../z16x18-k33/block_families.hpp"
#include <array>
#include <iostream>
#include <string>

constexpr int points = 9, lines = 19;
int minimum, low, high;
std::array<Blocks, 6> by_size;
std::set<Blocks> answers;
using Loads = std::array<int, points>;

Loads load_of(const Blocks& blocks) {
    Loads loads{};
    for (auto b : blocks)
        for (int p = 0; p < points; ++p) loads[p] += (b >> p) & 1u;
    return loads;
}

// Add the remaining blocks of size at most three in nonincreasing (size, index) order.
void small(Blocks& blocks, const Blocks& pool, size_t start, int total, Loads loads) {
    int left = lines - blocks.size();
    if (total + 3 * left < minimum) return;
    for (int p = 0; p < points; ++p)
        if (loads[p] > high || loads[p] + left < low) return;
    if (!left) {
        answers.insert(canonical_blocks(points, blocks));
        return;
    }
    for (size_t i = start; i < pool.size(); ++i) {
        unsigned b = pool[i];
        int d = std::popcount(b);
        if (total + d * left < minimum) break;
        if (d == 3 && !fits(b, blocks)) continue;
        auto next = loads;
        for (int p = 0; p < points; ++p) next[p] += (b >> p) & 1u;
        blocks.push_back(b);
        // A triple may not repeat; pairs, singletons and empty blocks may.
        small(blocks, pool, i + (d == 3), total + d, next);
        blocks.pop_back();
    }
}

int main(int argc, char** argv) {
    if (argc != 4) return 2;
    minimum = std::stoi(argv[1]);
    low = std::stoi(argv[2]);
    high = std::stoi(argv[3]);
    if (minimum < 0 || low < 0 || high < low || high > lines) return 2;
    for (unsigned b = 0; b < (1u << points); ++b)
        if (std::popcount(b) <= 5) by_size[std::popcount(b)].push_back(b);
    Blocks large;
    for (int d : {5, 4})
        for (auto b : by_size[d]) large.push_back(b);
    Blocks tail;
    for (int d = 3; d >= 0; --d)
        for (auto b : by_size[d]) tail.push_back(b);

    // Every final multiset has a well defined set of large blocks. Grow these
    // sets one block at a time, keeping one canonical copy of each.
    std::set<Blocks> level{Blocks{}};
    for (int count = 0; count <= lines && !level.empty(); ++count) {
        std::set<Blocks> next;
        for (const auto& family : level) {
            int m = 0, f = 0;
            for (auto b : family) (std::popcount(b) == 5 ? m : f)++;
            Loads loads = load_of(family);
            if (*std::max_element(loads.begin(), loads.end()) > high) continue;
            // At most three entries per remaining block.
            if (5 * m + 4 * f + 3 * (lines - count) >= minimum) {
                Blocks blocks = family;
                Blocks pool;
                for (auto b : tail)
                    if (std::popcount(b) < 3 || fits(b, family)) pool.push_back(b);
                small(blocks, pool, 0, 5 * m + 4 * f, loads);
            }
            if (count == lines) continue;
            for (auto b : large) {
                if (!fits(b, family)) continue;
                auto child = family;
                child.push_back(b);
                next.insert(canonical_blocks(points, child));
            }
        }
        level.swap(next);
    }
    for (const auto& blocks : answers) {
        for (auto b : blocks) std::cout << b << ' ';
        std::cout << '\n';
    }
}
