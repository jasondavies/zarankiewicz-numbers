// Print the canonical form of each block multiset read from standard input.
#include "../z16x18-k33/block_families.hpp"
#include <iostream>
#include <sstream>
#include <string>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    const int points = std::stoi(argv[1]);
    if (points < 1 || points > 12) return 2;
    for (std::string line; std::getline(std::cin, line);) {
        std::istringstream input(line);
        Blocks blocks;
        for (unsigned b; input >> b;) blocks.push_back(b);
        for (auto b : canonical_blocks(points, blocks)) std::cout << b << ' ';
        std::cout << '\n';
    }
}
