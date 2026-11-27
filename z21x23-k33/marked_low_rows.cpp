// Complete the rows of degrees 10 through 12 outside a marked eight-one column.
#include <algorithm>
#include <array>
#include <bit>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using Mask = unsigned;
using Rows = std::vector<Mask>;
using Counts = std::array<int, 3>;  // Numbers of missing tens, elevens and twelves.

class RowSearch {
    Rows fixed;
    std::array<unsigned, 22> pairs{};
    std::array<Rows, 3> supports;

    // A candidate row may cover each of the 28 pairs of fixed rows twice.
    void generate(int start, Mask row, int size, unsigned once, unsigned twice) {
        if (size >= 10) supports[size - 10].push_back(row);
        if (size == 12) return;
        for (int j = start; j < 22 && size + 22 - j >= 10; ++j) {
            unsigned added = pairs[j];
            if (added & twice) continue;
            generate(j + 1, row | (1u << j), size + 1, once | added, twice | (once & added));
        }
    }

    bool choose(const Rows& pool, const std::vector<int>& degrees, size_t pos) {
        if (pos == degrees.size()) return true;
        size_t need = degrees.size() - pos;
        for (size_t i = 0; i + need <= pool.size(); ++i) {
            Mask row = pool[i];
            int degree = std::popcount(row);
            if (degree > degrees[pos]) continue;
            if (degree < degrees[pos]) break;
            if (need == 1) return true;
            Rows next;
            for (size_t j = i + 1; j < pool.size(); ++j) {
                Mask common = row & pool[j];
                if (std::none_of(fixed.begin(), fixed.end(), [common](Mask other) {
                    return std::popcount(common & other) >= 3;
                })) next.push_back(pool[j]);
            }
            if (next.size() < need - 1) continue;
            fixed.push_back(row);
            bool found = choose(next, degrees, pos + 1);
            fixed.pop_back();
            if (found) return true;
        }
        return false;
    }

public:
    explicit RowSearch(std::array<Mask, 22> blocks) : fixed(8) {
        // Column order is immaterial. The dense blocks prune the most branches.
        std::sort(blocks.begin(), blocks.end(), [](Mask a, Mask b) {
            return std::popcount(a) > std::popcount(b);
        });
        for (int j = 0; j < 22; ++j) {
            int index = 0;
            for (int a = 0; a < 8; ++a) {
                if (blocks[j] & (1u << a)) fixed[a] |= 1u << j;
                for (int b = 0; b < a; ++b, ++index)
                    if ((blocks[j] >> a & 1) && (blocks[j] >> b & 1))
                        pairs[j] |= 1u << index;
            }
        }
        generate(0, 0, 0, 0, 0);
    }

    bool can_place(const Counts& counts) {
        Rows pool;
        std::vector<int> degrees;
        for (int i = 2; i >= 0; --i) {
            if (counts[i] > int(supports[i].size())) return false;
            if (counts[i] == 0) continue;
            degrees.insert(degrees.end(), counts[i], i + 10);
            pool.insert(pool.end(), supports[i].begin(), supports[i].end());
        }
        return choose(pool, degrees, 0);
    }
};

int main() {
    std::string line;
    size_t cases = 0;
    while (std::getline(std::cin, line)) {
        std::istringstream input(line);
        std::array<Mask, 22> blocks;
        for (Mask& block : blocks)
            if (!(input >> block) || block >= 256) throw std::runtime_error("invalid block");
        RowSearch search(blocks);
        Counts counts;
        bool has_profile = false;
        while (input >> counts[0]) {
            if (!(input >> counts[1] >> counts[2]) ||
                *std::min_element(counts.begin(), counts.end()) < 0)
                throw std::runtime_error("invalid row counts");
            has_profile = true;
            if (search.can_place(counts)) {
                std::cout << "survives " << line << '\n';
                return 0;
            }
        }
        if (!has_profile || !input.eof()) throw std::runtime_error("invalid input");
        ++cases;
    }
    std::cout << "excluded " << cases << '\n';
}
