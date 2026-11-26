// Enumerate fixed-length block multisets on a marked row, up to relabelling.
#include "../z16x18-k33/block_families.hpp"
#include <array>
#include <iostream>

constexpr int max_points = 10;

int main(int argc, char **argv) {
    if (argc != 3 && argc != 5)
        return 2;
    int points = std::stoi(argv[1]), minimum = std::stoi(argv[2]);
    const int lines = argc == 5 ? std::stoi(argv[3]) : 17;
    const int min_load = argc == 5 ? std::stoi(argv[4]) : 7;
    if (points < 2 || points > max_points || lines < 1 || lines > 19 ||
        min_load < 0 || min_load > lines || minimum < 0 || minimum > 5 * lines)
        return 2;
    std::array<Blocks, 6> pool;
    for (unsigned b = 0; b < (1u << points); ++b)
        if (std::popcount(b) <= 5)
            pool[std::popcount(b)].push_back(b);
    std::set<Blocks> level{Blocks{}};
    for (int count = 1; count <= lines; ++count) {
        std::set<Blocks> next;
        for (const auto &base : level) {
            int total = 0, high = 5, used = 0;
            std::array<int, max_points> loads{};
            for (auto b : base) {
                int w = std::popcount(b);
                high = std::min(high, w);
                total += w;
                used += w * (w - 1) * (w - 2) / 6;
                for (int j = 0; j < points; ++j)
                    loads[j] += (b >> j) & 1u;
            }
            for (int d = high; total + d * (lines - count + 1) >= minimum && d >= 0; --d) {
                int left = lines - count;
                int want = std::max(0, minimum - total - d);
                // Convexity gives the least triples consumed by the remaining blocks.
                int cost = used + d * (d - 1) * (d - 2) / 6;
                if (left) {
                    int a = want / left, r = want % left;
                    cost += left * a * (a - 1) * (a - 2) / 6 + r * a * (a - 1) / 2;
                }
                if (cost > points * (points - 1) * (points - 2) / 6)
                    continue;
                for (auto b : pool[d]) {
                    if (!fits(b, base))
                        continue;
                    bool feasible = true;
                    for (int j = 0; j < points; ++j) {
                        int load = loads[j] + ((b >> j) & 1u);
                        if (load + left < min_load)
                            feasible = false;
                    }
                    if (!feasible)
                        continue;
                    auto child = base;
                    child.push_back(b);
                    next.insert(canonical_blocks(points, child));
                }
            }
        }
        level.swap(next);
    }
    for (const auto &blocks : level) {
        for (auto b : blocks)
            std::cout << b << ' ';
        std::cout << '\n';
    }
}
