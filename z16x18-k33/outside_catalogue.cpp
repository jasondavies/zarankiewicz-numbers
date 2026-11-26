// Enumerate the submatrix on the rows avoiding one marked column.
// A block is the restriction of one other column to the rows avoiding the mark.
#include "block_families.hpp"
#include <array>
#include <iostream>
#include <string>

constexpr int width = 17;

int main(int argc, char** argv) {
    if (argc != 3 && argc != 4) return 2;
    const int rows = std::stoi(argv[1]), threshold = std::stoi(argv[2]);
    const int floor = argc == 4 ? std::stoi(argv[3]) : 6;
    if (rows < 5 || rows > 8 || floor < 0 || floor > width) return 2;
    const std::array<int,12> six{26,29,32,36,39,42,45,48,50,53,56,58};
    const std::array<int,12> seven{29,33,37,40,44,47,50,53,56,60,63,66};
    const std::array<int,12> eight{32,37,42,45,50,53,57,60,64,67,70,74};
    std::array<int,width+1> ceiling{};
    for (int j = 1; j <= width; ++j)
        ceiling[j] = j < 6 || rows == 5 ? rows*j : (rows == 6 ? six : rows == 7 ? seven : eight)[j-6];

    std::array<Blocks,9> by_size;
    for (unsigned b = 0; b < (1u << rows); ++b)
        by_size[std::popcount(b)].push_back(b);
    std::set<Blocks> level{Blocks{}};
    for (int count = 1; count <= width; ++count) {
        std::set<Blocks> next;
        for (const auto& base : level) {
            int weight = 0, max_size = rows;
            for (auto b : base) {
                weight += std::popcount(b);
                max_size = std::min(max_size, std::popcount(b));
            }
            std::array<int,8> loads{};
            Blocks pairs;
            for (size_t i = 0; i < base.size(); ++i) {
                for (int j = 0; j < rows; ++j) loads[j] += (base[i] >> j) & 1u;
                for (size_t j = 0; j < i; ++j) {
                    unsigned both = base[i] & base[j];
                    if (std::popcount(both) >= 3) pairs.push_back(both);
                }
            }
            for (int d = max_size; d >= 0; --d) {
                const int total = weight + d;
                if (total + (width-count)*d < threshold) break;
                if (total > ceiling[count]) continue;
                bool enough = true;
                for (int j = count; j <= width; ++j) {
                    int upper = std::min(ceiling[j], total + (j-count)*d);
                    if (upper + (width-j)*std::min(d,upper/j) < threshold) {
                        enough = false;
                        break;
                    }
                }
                if (!enough) continue;
                for (auto b : by_size[d]) {
                    if (!fits(b, pairs)) continue;
                    bool floors = true;
                    for (int j = 0; j < rows; ++j)
                        if (loads[j] + int((b >> j)&1u) + width-count < floor) floors = false;
                    if (!floors) continue;
                    Blocks child = base;
                    child.push_back(b);
                    next.insert(canonical_blocks(rows, child));
                }
            }
        }
        level.swap(next);
    }
    for (const auto& blocks : level) {
        for (auto b : blocks) std::cout << b << ' ';
        std::cout << '\n';
    }
}
