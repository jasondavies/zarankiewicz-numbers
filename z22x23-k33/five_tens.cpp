// Test ten-rows avoiding the marked eight-column of a 20 by 22 core.
#include "../z18x19-k33/seven_columns.hpp"
#include <algorithm>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const int needed = std::stoi(argv[1]);
    if (needed < 1 || needed > 5) return 2;
    size_t checked = 0, choices = 0;
    for (std::string line; std::getline(std::cin, line);) {
        std::istringstream input(line);
        LineExtensions<21> search;
        search.fixed.assign(8, 0);
        for (int j = 0; j < 21; ++j) {
            Mask block;
            if (!(input >> block) || block >= 256) return 2;
            for (int i = 0; i < 8; ++i)
                search.fixed[i] |= ((block >> i) & 1u) << j;
        }
        Mask extra;
        if (input >> extra) return 2;
        search.run(0, 10);
        for (int a = 0; a < 21; ++a)
            for (int b = 0; b < a; ++b)
                for (int c = 0; c < b; ++c)
                    for (int d = 0; d < c; ++d) {
                        Mask low = (1u << a) | (1u << b) | (1u << c) | (1u << d);
                        int total = 0;
                        for (auto row : search.fixed) {
                            int used = std::popcount(row & low);
                            if (used < 2 || used > 3) { total = 18; break; }
                            total += used;
                        }
                        if (total > 17) continue;
                        ++choices;
                        Lines pool;
                        for (auto row : search.allowed)
                            if (std::popcount(row & low) >= 3) pool.push_back(row);
                        if (search.choose(pool, needed)) {
                            std::cout << "completion " << low;
                            for (size_t i = 0; i < search.fixed.size(); ++i)
                                std::cout << ' ' << ((search.fixed[i] << 1) | unsigned(i < 8));
                            std::cout << '\n';
                            return 0;
                        }
                    }
        ++checked;
    }
    std::cout << "excluded " << checked << " choices " << choices << '\n';
}
