// Reconstruct all missing lines from either side of a marked line.
#include <algorithm>
#include <bit>
#include <cstdint>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using Mask = unsigned;
using Lines = std::vector<Mask>;

class Layer {
    Lines supports;
    std::vector<std::vector<uint64_t>> excluded;
public:
    Layer(int n, int d) : excluded(1u << n) {
        for (Mask b = 0; b < (1u << n); ++b)
            if (std::popcount(b) == d) supports.push_back(b);
    }

    Lines allowed(const Lines& intersections, Mask marker) {
        size_t words = (supports.size() + 63) / 64;
        std::vector<uint64_t> forbidden(words);
        for (Mask both : intersections) {
            if (std::popcount(both) < 3) continue;
            auto& cached = excluded[both];
            if (cached.empty()) {
                cached.resize(words);
                for (size_t i = 0; i < supports.size(); ++i)
                    if (std::popcount(both & supports[i]) >= 3)
                        cached[i/64] |= uint64_t(1) << (i%64);
            }
            for (size_t i = 0; i < words; ++i) forbidden[i] |= cached[i];
        }
        Lines result;
        for (size_t i = 0; i < words; ++i) {
            uint64_t remaining = ~forbidden[i];
            if (i+1 == words && supports.size()%64)
                remaining &= (uint64_t(1) << (supports.size()%64)) - 1;
            for (; remaining; remaining &= remaining-1)
                result.push_back(supports[64*i + std::countr_zero(remaining)] | marker);
        }
        return result;
    }
};

// The pool is sorted in descending weight. Its members already satisfy every
// triple test against two fixed lines, including lines fixed in recursion.
bool choose(Lines& fixed, const Lines& pool, int left, int target, int floor) {
    if (left == 0) return target == 0;
    for (size_t i = 0; i+left <= pool.size(); ++i) {
        Mask a = pool[i];
        int d = std::popcount(a);
        if (d > target-(left-1)*floor) continue;
        int upper = d;
        for (int k = 1; k < left; ++k) upper += std::popcount(pool[i+k]);
        if (upper < target) break;
        if (left == 1) {
            fixed.push_back(a);
            return true; // The previous two tests give d == target.
        }
        Lines next;
        for (size_t j = i+1; j < pool.size(); ++j) {
            Mask both = a & pool[j];
            if (std::none_of(fixed.begin(), fixed.end(), [both](Mask b) {
                    return std::popcount(b & both) > 2;
                })) next.push_back(pool[j]);
        }
        if (int(next.size()) < left-1) continue;
        fixed.push_back(a);
        if (choose(fixed, next, left-1, target-d, floor)) return true;
        fixed.pop_back();
    }
    return false;
}

// Necessary test on the total excess above a weight threshold. Cheap rows
// cannot help achieve this excess and never enter this part of the search.
bool can_gain(Lines& fixed, const Lines& pool, int slots, int gap, int baseline) {
    if (gap <= 0) return true;
    if (!slots) return false;
    for (size_t i = 0; i < pool.size(); ++i) {
        int upper=0;
        for (size_t j=i; j<pool.size() && j<i+slots; ++j)
            upper += std::popcount(pool[j])-baseline;
        if (upper<gap) break;
        Mask a=pool[i];
        int gain=std::popcount(a)-baseline;
        if (gain>=gap) return true;
        Lines next;
        for (size_t j=i+1; j<pool.size(); ++j) {
            Mask both=a&pool[j];
            if (std::none_of(fixed.begin(),fixed.end(),[both](Mask b) {
                    return std::popcount(b&both)>2;
                })) next.push_back(pool[j]);
        }
        fixed.push_back(a);
        bool ok=can_gain(fixed,next,slots-1,gap-gain,baseline);
        fixed.pop_back();
        if (ok) return true;
    }
    return false;
}
int main(int argc, char** argv) {
    if (argc != 8 && argc != 9) return 2;
    const bool gain_pruning = argc == 9;
    if (gain_pruning && std::string(argv[8]) != "--gain") return 2;
    const std::string side = argv[1];
    const bool outside = side == "outside";
    if (!outside && side != "inside") return 2;
    const int points = std::stoi(argv[2]), n = std::stoi(argv[3]), extra = std::stoi(argv[4]);
    const int low = std::stoi(argv[5]), high = std::stoi(argv[6]), weight = std::stoi(argv[7]);
    if (points < 1 || points > 18 || n < 1 || n > 18 || extra < 1 ||
        low < int(outside) || high > n+int(outside) || high < low) return 2;
    const Mask marker = 1u << n;
    std::vector<Layer> layers;
    for (int d = low; d <= high; ++d) layers.emplace_back(n, d-int(outside));

    std::string line;
    size_t cases = 0;
    while (std::getline(std::cin, line)) {
        std::istringstream input(line);
        Lines fixed(points, outside ? 0u : marker), blocks;
        for (Mask b; input >> b;) blocks.push_back(b);
        if (int(blocks.size()) != n) throw std::logic_error("wrong projection length");
        for (int i = 0; i < n; ++i) {
            if (blocks[i] >= (1u << points)) throw std::logic_error("wrong mask width");
            for (int j = 0; j < points; ++j)
                fixed[j] |= ((blocks[i] >> j) & 1u) << i;
        }
        Lines pairs;
        int target = weight;
        for (int i = 0; i < points; ++i) {
            target -= std::popcount(fixed[i]);
            for (int j = 0; j < i; ++j) {
                Mask both = fixed[i] & fixed[j];
                for (int k = 0; k < j; ++k)
                    if (std::popcount(both & fixed[k]) > 2)
                        throw std::logic_error("invalid projection");
                pairs.push_back(both & (marker-1));
            }
        }
        ++cases;
        int peak = std::min(high, target-(extra-1)*low);
        Lines pool;
        for (; peak >= low && extra*peak >= target; --peak) {
            pool = layers[peak-low].allowed(pairs, outside ? marker : 0u);
            if (!pool.empty()) break;
        }
        if (pool.empty()) continue;
        int heavy = target-extra*(peak-1);
        if (heavy > 0) {
            auto test = fixed;
            if (!choose(test, pool, heavy, heavy*peak, peak)) continue;
        }
        bool feasible=true;
        for (int d = peak-1; d >= std::max(low,target-(extra-1)*peak); --d) {
            if (gain_pruning && d>=7 && target-extra*d >= 3 && !can_gain(fixed,pool,extra,target-extra*d,d)) {
                feasible=false;
                break;
            }
            auto more = layers[d-low].allowed(pairs, outside ? marker : 0u);
            pool.insert(pool.end(), more.begin(), more.end());
        }
        if (feasible && choose(fixed, pool, extra, target, low)) {
            std::cout << "completion";
            for (auto b : fixed) std::cout << ' ' << b;
            std::cout << '\n';
            return 0;
        }
    }
    std::cout << "excluded " << cases << '\n';
}
