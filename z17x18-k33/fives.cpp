#include "../z16x18-k33/block_families.hpp"
#include <iostream>
#include <string>
#include <sstream>

int main(int argc, char** argv) {
    if (argc != 3) return 2;
    int points = std::stoi(argv[1]);
    if (points < 10 || points > 11) return 2;
    if (std::string(argv[2]) == "unique") {
        std::set<Blocks> seen;
        std::string line;
        while (std::getline(std::cin,line)) {
            std::istringstream input(line);
            Blocks blocks;
            for (unsigned b; input >> b;) blocks.push_back(b);
            auto key = canonical_blocks(points,blocks);
            if (seen.insert(key).second) {
                for (auto b : key) std::cout << b << ' ';
                std::cout << '\n';
            }
        }
        return 0;
    }
    int first = std::stoi(argv[2]);
    if (points < 10 || points > 11 || first < 1) return 2;
    Blocks pool;
    for (unsigned b = 0; b < (1u << points); ++b)
        if (std::popcount(b) == 5) pool.push_back(b);
    std::set<Blocks> level{Blocks{}};
    for (int count = 1; !level.empty(); ++count) {
        std::set<Blocks> next;
        for (const auto& family : level)
            for (auto b : pool) {
                if (!fits(b, family)) continue;
                auto extended = family;
                extended.push_back(b);
                next.insert(canonical_blocks(points, extended));
            }
        level.swap(next);
        if (count >= first)
            for (const auto& family : level) {
                for (auto b : family) std::cout << b << ' ';
                std::cout << '\n';
            }
    }
}
