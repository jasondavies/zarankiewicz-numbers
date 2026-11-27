// Search for the seven missing degree-ten columns of a marked 209-one square.
#include "../z18x19-k33/seven_columns.hpp"
#include <algorithm>
#include <cstdint>

class SevenTens {
    using Bits = std::vector<uint64_t>;
    Lines fixed, options, selected, witness;
    std::vector<unsigned char> cached_intersections;
    Bits edges;
    size_t words;

    bool compatible_with_fixed(Mask common) {
        const int size = std::popcount(common);
        if (size <= 2) return true;
        if (size > 5) return false;
        auto& status = cached_intersections[common];
        if (!status) {
            bool allowed = std::none_of(fixed.begin(), fixed.end(), [common](Mask col) {
                return std::popcount(common & col) > 2;
            });
            status = allowed ? 1 : 2;
        }
        return status == 1;
    }

    // The pool already satisfies all triple tests with two selected columns.
    // When adding v, test (v, candidate, older column) before descending.
    bool choose(Bits pool, int left) {
        int count = 0;
        for (auto word : pool) count += std::popcount(word);
        Bits next(words);
        for (size_t i = 0; i < words && count >= left; ++i) {
            while (pool[i] && count >= left) {
                size_t v = 64*i + std::countr_zero(pool[i]);
                pool[i] &= pool[i]-1;
                --count;
                if (left == 1) {
                    witness = selected;
                    witness.push_back(options[v]);
                    return true;
                }
                int available = 0;
                for (size_t j = i; j < words; ++j) {
                    next[j] = edges[v*words+j] & pool[j];
                    available += std::popcount(next[j]);
                }
                if (available < left-1) continue;
                for (size_t j = i; j < words && !selected.empty(); ++j) {
                    for (auto rest = next[j]; rest; rest &= rest-1) {
                        int bit = std::countr_zero(rest);
                        Mask common = options[v] & options[64*j+bit];
                        if (std::popcount(common) > 2 &&
                            std::any_of(selected.begin(), selected.end(), [common](Mask col) {
                                return std::popcount(common & col) > 2;
                            })) {
                            next[j] &= ~(uint64_t(1) << bit);
                            --available;
                        }
                    }
                }
                if (available < left-1) continue;
                selected.push_back(options[v]);
                bool found = choose(next, left-1);
                selected.pop_back();
                if (found) return true;
            }
            next[i] = 0;
        }
        return false;
    }

public:
    bool run(const Lines& blocks) {
        fixed.assign(10, 0);
        for (size_t i = 0; i < blocks.size(); ++i)
            for (Mask x = blocks[i]; x; x &= x-1)
                fixed[std::countr_zero(x)] |= 1u << i;
        LineExtensions<21> single;
        single.fixed = fixed;
        single.run(0, 10);
        options.clear();
        for (Mask col : single.allowed) {
            if (std::none_of(fixed.begin(), fixed.end(), [col](Mask f) {
                return std::popcount(col & f) > 5;
            })) options.push_back(col);
        }
        if (options.size() < 7) return false;
        cached_intersections.assign(1u << 21, 0);
        words = (options.size()+63)/64;
        edges.assign(words*options.size(), 0);
        for (size_t a = 0; a < options.size(); ++a)
            for (size_t b = a+1; b < options.size(); ++b)
                if (compatible_with_fixed(options[a]&options[b]))
                    edges[a*words+b/64] |= uint64_t(1) << (b%64);
        Bits pool(words, ~uint64_t(0));
        if (options.size()%64) pool.back() = (uint64_t(1) << (options.size()%64))-1;
        return choose(pool, 7);
    }

    void print_witness() const {
        std::cout << "placement";
        for (auto col : fixed) std::cout << ' ' << (col | (1u << 21));
        for (auto col : witness) std::cout << ' ' << col;
        std::cout << '\n';
    }
};

int main(int argc, char** argv) {
    bool control = argc == 2 && std::string(argv[1]) == "--control";
    if (argc != 1 && !control) return 2;
    SevenTens search;
    size_t seen = 0, kept = 0;
    for (std::string line; std::getline(std::cin,line);) {
        std::istringstream in(line);
        Lines blocks;
        int total = 0;
        for (Mask x; in >> x;) {
            if (x >= (1u << 10)) return 2;
            blocks.push_back(x);
            total += std::popcount(x);
        }
        if (blocks.size() != 21 || total != 84) return 2;
        ++seen;
        if (search.run(blocks)) {
            if (control) { search.print_witness(); return 0; }
            ++kept;
            std::cout << line << '\n';
        }
    }
    std::cerr << seen << " marks, " << kept << " survive\n";
}
