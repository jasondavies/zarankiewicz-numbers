// Place one eleven-row and a prescribed number of ten-rows outside a ten-column.
#include "../z18x19-k33/seven_columns.hpp"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const int count = std::stoi(argv[1]);
    if (count < 0 || count > 11) return 2;
    std::string line;
    size_t tested = 0;
    while (std::getline(std::cin, line)) {
        ++tested;
        std::istringstream input(line);
        LineExtensions<22> search;
        search.fixed.resize(10);
        for (int j = 0; j < 22; ++j) {
            Mask block;
            if (!(input >> block) || block >= (1u << 10)) return 2;
            for (int i = 0; i < 10; ++i)
                if (block >> i & 1u) search.fixed[i] |= 1u << j;
        }
        search.run(0,11);
        if (search.allowed.empty()) continue;
        Lines elevens;
        elevens.swap(search.allowed);
        search.supports((1u << 22)-1,0,10);
        for (Mask row : elevens) {
            Lines pool;
            for (Mask ten : search.allowed) {
                Mask common = row & ten;
                bool good = true;
                for (Mask old : search.fixed)
                    if (std::popcount(old & common) > 2) { good = false; break; }
                if (good) pool.push_back(ten);
            }
            search.fixed.push_back(row);
            if (search.choose(pool,count)) {
                std::cout << "completion";
                for (size_t i = 0; i < search.fixed.size(); ++i)
                    std::cout << ' ' << (search.fixed[i] | ((i < 10) ? (1u << 22) : 0u));
                std::cout << '\n';
                return 0;
            }
            search.fixed.pop_back();
        }
    }
    std::cout << "excluded " << tested << '\n';
}
