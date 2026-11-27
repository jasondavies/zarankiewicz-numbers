// A ninth marked column through seven or eight of twenty blocks on eight points.
#include "../z16x18-k33/block_families.hpp"
#include <array>
#include <cstdint>
#include <iostream>
#include <string>

using Families = std::set<Blocks>;

// Each point has its own byte. No projection has more than twenty blocks.
uint64_t point_loads(unsigned mask) {
    uint64_t loads = 0;
    for (unsigned s = mask; s; s &= s - 1)
        loads |= uint64_t(1) << (8 * std::countr_zero(s));
    return loads;
}

Families add_large_block(const Families& families, const Blocks& options) {
    Families extensions;
    for (const auto& family : families)
        for (auto block : options) {
            if (!fits(block, family)) continue;
            auto extended = family;
            extended.push_back(block);
            extensions.insert(canonical_blocks(8, extended));
        }
    return extensions;
}

class Projections {
    int ninth_load, total;
    Blocks rows;
    Families answers;
    std::array<Blocks, 4> options;
    std::array<int, 4> count{}, through{};

    // Slots 0..3 place triples down to empty blocks through the ninth point.
    // Slots 4..7 place the remaining blocks in the same size order.
    void fill(int slot, size_t first, int left, uint64_t loads) {
        if (slot == 8) {
            for (int j = 0; j < 8; ++j)
                if (((loads >> (8*j)) & 255) < 8) return;
            answers.insert(canonical_blocks(9, rows));
            return;
        }
        int size = 3 - slot % 4;
        if (!left) {
            int next = slot + 1;
            int d = 3 - next % 4;
            int needed = next < 4 ? through[d] : count[d] - through[d];
            fill(next, 0, needed, loads);
            return;
        }
        bool marked = slot < 4;
        bool distinct = size + int(marked) >= 3;
        for (size_t i = first; i < options[size].size(); ++i) {
            if (distinct && options[size].size() - i < size_t(left)) break;
            unsigned mask = options[size][i];
            unsigned block = mask | (marked ? 256u : 0u);
            if (!fits(block, rows)) continue;
            rows.push_back(block);
            fill(slot, i + int(distinct), left - 1, loads + point_loads(mask));
            rows.pop_back();
        }
    }

    void split(int size, int needed, uint64_t loads) {
        if (size < 0) {
            if (needed == 0) fill(0, 0, through[3], loads);
            return;
        }
        for (int k = 0; k <= std::min(count[size], needed); ++k) {
            through[size] = k;
            split(size - 1, needed - k, loads);
        }
    }

    void complete(const Blocks& base) {
        int small_rows = 20 - int(base.size());
        int small_ones = total;
        uint64_t loads = 0;
        for (auto mask : base) {
            small_ones -= std::popcount(mask);
            loads += point_loads(mask);
        }
        int gap = 3 * small_rows - small_ones;
        if (gap < 0 || small_ones < 0) return;
        for (auto& masks : options) masks.clear();
        for (unsigned mask = 0; mask < 256; ++mask)
            if (std::popcount(mask) <= 3 && fits(mask, base))
                options[std::popcount(mask)].push_back(mask);

        for (unsigned subset = 0; subset < (1u << base.size()); ++subset) {
            int needed = ninth_load - std::popcount(subset);
            if (needed < 0 || needed > small_rows) continue;
            rows.clear();
            for (size_t i = 0; i < base.size(); ++i) {
                unsigned block = base[i] | (((subset >> i) & 1) << 8);
                if (std::popcount(block) > 5 || !fits(block, rows)) break;
                rows.push_back(block);
            }
            if (rows.size() != base.size()) continue;
            // Relative to triples, empties cost three, singletons two, pairs one.
            for (count[0] = 0; 3*count[0] <= gap; ++count[0])
                for (count[1] = 0; 3*count[0] + 2*count[1] <= gap; ++count[1]) {
                    count[2] = gap - 3*count[0] - 2*count[1];
                    count[3] = small_rows - count[0] - count[1] - count[2];
                    if (count[3] >= 0) split(3, needed, loads);
                }
        }
    }

public:
    Projections(int ninth, int weight) : ninth_load(ninth), total(weight) {}

    void run() {
        Blocks fours, fives;
        for (unsigned mask = 0; mask < 256; ++mask) {
            if (std::popcount(mask) == 4) fours.push_back(mask);
            if (std::popcount(mask) == 5) fives.push_back(mask);
        }
        Families bases{Blocks{}};
        while (!bases.empty()) {
            for (Families level = bases; !level.empty(); level = add_large_block(level, fours))
                for (const auto& base : level) complete(base);
            bases = add_large_block(bases, fives);
        }
        for (const auto& family : answers) {
            for (auto block : family) std::cout << block << ' ';
            std::cout << '\n';
        }
    }
};

int main(int argc, char** argv) {
    if (argc != 3) return 2;
    int ninth = std::stoi(argv[1]), weight = std::stoi(argv[2]);
    if ((ninth != 7 && ninth != 8) || (weight != 68 && weight != 69)) return 2;
    Projections(ninth, weight).run();
}
