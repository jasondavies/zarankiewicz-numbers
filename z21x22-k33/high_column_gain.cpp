// Necessary test for a ten-point projection of an extremal 21 by 22 matrix.
// Each selected column contributes its degree minus nine to the required excess.
#include "../z18x19-k33/seven_columns.hpp"
#include <algorithm>

class ExcessSearch {
    Lines fixed, selected, candidates;
    std::array<std::array<Mask, 20>, 20> forbidden{};
    std::vector<unsigned char> pair_status;

    void possible_columns(Mask available, Mask used, int size) {
        if (size >= 10) candidates.push_back(used);
        while (available && size + std::popcount(available) >= 10) {
            const Mask bit = available & -available;
            available ^= bit;
            Mask next = available;
            const int point = std::countr_zero(bit);
            for (Mask rest = used; rest; rest &= rest - 1)
                next &= ~forbidden[point][std::countr_zero(rest)];
            possible_columns(next, used | bit, size + 1);
        }
    }

    bool pair_allowed(Mask common) {
        if (std::popcount(common) <= 2) return true;
        if (std::popcount(common) > 6) return false;
        auto& status = pair_status[common];
        if (!status) {
            bool allowed = std::none_of(fixed.begin(), fixed.end(), [common](Mask c) {
                return std::popcount(c & common) > 2;
            });
            status = allowed ? 1 : 2;
        }
        return status == 1 && std::none_of(selected.begin(), selected.end(), [common](Mask c) {
            return std::popcount(c & common) > 2;
        });
    }

    bool choose(const Lines& options, int needed) {
        // The list is ordered by decreasing gain. Each new member is already
        // compatible with all pairs of columns placed above this node.
        for (size_t i = 0; i < options.size(); ++i) {
            Mask c = options[i];
            int gain = std::popcount(c) - 9;
            if (gain >= needed) return true;
            if (int(options.size() - i) * gain < needed) break;
            Lines next;
            int remaining_gain = 0;
            for (size_t j = i + 1; j < options.size(); ++j) {
                if (pair_allowed(c & options[j])) {
                    next.push_back(options[j]);
                    remaining_gain += std::popcount(options[j]) - 9;
                }
            }
            if (remaining_gain < needed - gain) continue;
            selected.push_back(c);
            bool found = choose(next, needed - gain);
            selected.pop_back();
            if (found) return true;
        }
        return false;
    }

public:
    bool possible(const Lines& blocks, int needed) {
        if (needed <= 0) return true;
        fixed.assign(10, 0);
        candidates.clear();
        selected.clear();
        for (auto& row : forbidden) row.fill(0);
        for (int i = 0; i < 20; ++i) {
            for (Mask rest = blocks[i]; rest; rest &= rest-1)
                fixed[std::countr_zero(rest)] |= 1u << i;
            for (int j = 0; j < i; ++j)
                for (int k = 0; k < j; ++k)
                    if (std::popcount(blocks[i] & blocks[j] & blocks[k]) >= 2)
                        forbidden[j][k] |= 1u << i;
        }
        possible_columns((1u << 20) - 1, 0, 0);
        std::erase_if(candidates, [&](Mask c) {
            return std::any_of(fixed.begin(), fixed.end(), [c](Mask f) {
                return std::popcount(c & f) > 6;
            });
        });
        std::sort(candidates.begin(), candidates.end(), [](Mask a, Mask b) {
            return std::popcount(a) > std::popcount(b);
        });
        pair_status.assign(1u << 20, 0);
        return choose(candidates, needed);
    }
};

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    int min_short = std::stoi(argv[1]);
    int seen = 0, kept = 0;
    ExcessSearch search;
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream input(line);
        Lines blocks;
        int load = 0;
        for (Mask b; input >> b;) {
            if (b >= 1024) return 2;
            blocks.push_back(b);
            load += std::popcount(b);
        }
        if (blocks.size() != 20 || load < 80) return 2;
        ++seen;
        if (search.possible(blocks, 3 + min_short - (load - 80))) {
            ++kept;
            std::cout << line << '\n';
        }
    }
    std::cerr << seen << " projections, " << kept << " survive\n";
}
