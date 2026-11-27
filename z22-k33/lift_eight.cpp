// Restore a minimum-load ninth point to a projection of an entire nine-row.
#include "../z16x18-k33/block_families.hpp"
#include <array>
#include <iostream>
#include <sstream>
#include <string>

struct Limits {
    int rows, maximum_load, long_columns, total, omitted_maximum;
};

class Lifts {
    Limits limits;
    Blocks base;
    std::array<unsigned, 22> compatible{};
    std::set<Blocks> result;

    void choose(unsigned pool, int remaining, unsigned selected) {
        if (!remaining) {
            Blocks lifted = base;
            for (unsigned p = selected; p; p &= p-1)
                lifted[std::countr_zero(p)] |= 1u << 8;
            result.insert(canonical_blocks(9, lifted));
            return;
        }
        while (std::popcount(pool) >= remaining) {
            unsigned bit = pool & -pool;
            pool ^= bit;
            choose(pool & compatible[std::countr_zero(bit)], remaining-1, selected | bit);
        }
    }

public:
    explicit Lifts(Limits settings) : limits(settings) {}

    void add(const Blocks& blocks) {
        if (int(blocks.size()) != limits.rows) throw std::logic_error("wrong block count");
        base = blocks;
        std::array<int,8> loads{};
        int total = 0;
        unsigned pool = 0;
        for (int i = 0; i < limits.rows; ++i) {
            if (base[i] >= 256) throw std::logic_error("expected eight points");
            total += std::popcount(base[i]);
            for (int j = 0; j < 8; ++j) loads[j] += (base[i] >> j) & 1u;
            if (std::popcount(base[i]) < 5) pool |= 1u << i;
            compatible[i] = 0;
            for (int j = i+1; j < limits.rows; ++j)
                if (std::popcount(base[i] & base[j]) <= 1) compatible[i] |= 1u << j;
        }
        if (*std::max_element(loads.begin(),loads.end()) > limits.maximum_load ||
            std::count_if(loads.begin(),loads.end(),[](int d){return d > 9;}) > limits.long_columns)
            return;
        const int smallest = *std::min_element(loads.begin(),loads.end());
        for (int d = 8; d <= std::min(smallest, limits.omitted_maximum); ++d)
            if (total+d >= limits.total) choose(pool, d, 0);
    }

    void print() const {
        for (const auto& rows : result) {
            for (auto block : rows) std::cout << block << ' ';
            std::cout << '\n';
        }
    }
};

int main(int argc, char** argv) {
    if (argc > 2) return 2;
    std::string target = argc == 2 ? argv[1] : "210";
    Limits limits{};
    if (target == "210") limits = {21,12,1,80,9};
    else if (target == "217") limits = {21,18,8,80,9};
    else if (target == "226") limits = {22,22,8,83,8};
    else return 2;
    Lifts search(limits);
    std::string line;
    while (std::getline(std::cin,line)) {
        std::istringstream input(line);
        Blocks rows;
        for (unsigned x; input >> x;) rows.push_back(x);
        search.add(rows);
    }
    search.print();
}
