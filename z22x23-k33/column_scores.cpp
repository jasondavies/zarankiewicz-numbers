// Test necessary partial placements on the 22 columns outside a marked column.
#include "../z18x19-k33/seven_columns.hpp"
#include <algorithm>

constexpr Mask all_columns = (1u << 22) - 1;

bool clique(Mask pool, const std::array<Mask,22>& edges, int need) {
    if (!need) return true;
    while (std::popcount(pool) >= need) {
        int first = std::countr_zero(pool);
        pool &= pool - 1;
        if (clique(pool & edges[first], edges, need - 1)) return true;
    }
    return false;
}

// A further row through the marked column needs eight outside entries.
// Two of those columns may share at most one previously marked row.
bool can_add_incident_row(const Lines& blocks) {
    std::array<Mask,22> edges{};
    for (int i = 0; i < 22; ++i)
        for (int j = i + 1; j < 22; ++j)
            if (std::popcount(blocks[i] & blocks[j]) <= 1) edges[i] |= 1u << j;
    return clique(all_columns, edges, 8);
}

struct OutsideRows {
    LineExtensions<22> search;
    const int points;
    Lines tens;
    bool generated_tens = false;

    OutsideRows(const Lines& blocks, int points) : points(points) {
        search.fixed.resize(points);
        for (int j = 0; j < 22; ++j)
            for (int i = 0; i < points; ++i)
                if (blocks[j] >> i & 1u) search.fixed[i] |= 1u << j;
    }
    bool compatible_pair(Mask a, Mask b) const {
        Mask both = a & b;
        return std::none_of(search.fixed.begin(), search.fixed.end(),
                            [both](Mask r){ return std::popcount(both & r) > 2; });
    }
    bool fit_tens(int count) {
        if (!generated_tens) {
            search.allowed.clear();
            search.supports(all_columns, 0, 10);
            tens.swap(search.allowed);
            generated_tens = true;
        }
        Lines pool;
        for (Mask row : tens) {
            bool allowed = true;
            // Pairs wholly inside the mark were checked during support generation.
            for (size_t i = points; allowed && i < search.fixed.size(); ++i)
                for (size_t j = 0; j < i; ++j)
                    if (std::popcount(row & search.fixed[i] & search.fixed[j]) > 2) {
                        allowed = false;
                        break;
                    }
            if (allowed) pool.push_back(row);
        }
        return search.choose(pool, count);
    }
    bool select(const Lines& longer, int slots, int gain) {
        if (gain <= 0) return true;
        if (slots <= 0) return false;
        if (gain <= slots && fit_tens(gain)) return true;
        for (size_t i = 0; i < longer.size(); ++i) {
            // Fill slots optimistically with the longest remaining rows, then tens.
            int upper = slots;
            for (size_t j = i; j < longer.size() && j - i < size_t(slots); ++j)
                upper += std::popcount(longer[j]) - 10;
            if (upper < gain) break;
            Lines next;
            for (size_t j = i + 1; j < longer.size(); ++j)
                if (compatible_pair(longer[i], longer[j])) next.push_back(longer[j]);
            search.fixed.push_back(longer[i]);
            if (select(next, slots - 1, gain - (std::popcount(longer[i]) - 9))) return true;
            search.fixed.pop_back();
        }
        return false;
    }
    bool possible(int target, int min_nines) {
        int marked_weight = points, marked_nines = 0;
        for (Mask row : search.fixed) {
            marked_weight += std::popcount(row);
            marked_nines += std::popcount(row) == 8;
        }
        const int outside = 22 - points;
        const int slots = outside - std::max(0, min_nines - marked_nines);
        const int gain = target - marked_weight - 9 * outside;
        search.run(0,11); // Builds the forbidden triples from every pair of marked rows.
        Lines elevens, longer;
        elevens.swap(search.allowed);
        if (!elevens.empty() && gain > 1) {
            for (int degree = 15; degree >= 12; --degree) {
                search.allowed.clear();
                search.supports(all_columns, 0, degree);
                longer.insert(longer.end(), search.allowed.begin(), search.allowed.end());
            }
            longer.insert(longer.end(), elevens.begin(), elevens.end());
        }
        // For gain one, a feasible longer row always contains a feasible ten-subset.
        return slots >= 0 && select(longer, slots, gain);
    }
};

int main(int argc, char** argv) {
    if (argc != 5) return 2;
    std::string mode = argv[1];
    int points = std::stoi(argv[2]), target = std::stoi(argv[3]), nines = std::stoi(argv[4]);
    if ((mode != "through" && mode != "outside") || points < 9 || points > 10) return 2;
    std::string line;
    size_t tested = 0, passed = 0;
    while (std::getline(std::cin,line)) {
        std::istringstream input(line);
        Lines blocks(22);
        for (Mask& block : blocks) if (!(input >> block) || block >= (1u << points)) return 2;
        std::string extra;
        if (input >> extra) return 2;
        bool ok = mode == "through" ? can_add_incident_row(blocks)
                                    : OutsideRows(blocks, points).possible(target, nines);
        if (ok) { ++passed; std::cout << line << '\n'; }
        ++tested;
    }
    std::cerr << tested << " tested, " << passed << " passed\n";
}
