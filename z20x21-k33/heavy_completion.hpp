// Finish a 20 x 17 heavy matrix after fixing the union of two nine-columns.
#pragma once

#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <vector>

using Mask = unsigned;
using Rows = std::vector<Mask>;
using Degrees = std::array<int, 15>;

// The remaining rows avoid the two marks. Each has 6, 7 or 8 of the other 15 entries.
class RowLayer {
    Rows supports;
    std::vector<std::vector<uint64_t>> forbidden;

public:
    explicit RowLayer(int weight) : forbidden(1 << 15) {
        for (Mask m = 0; m < 1u << 15; ++m)
            if (std::popcount(m) == weight) supports.push_back(m);
        for (Mask p = 0; p < 1u << 15; ++p) {
            if (std::popcount(p) < 3 || std::popcount(p) > 5) continue;
            auto& bits = forbidden[p];
            bits.resize((supports.size() + 63) / 64);
            for (size_t i = 0; i < supports.size(); ++i)
                if (std::popcount(supports[i] & p) >= 3)
                    bits[i / 64] |= uint64_t(1) << (i % 64);
        }
    }

    Rows allowed(const Rows& pairs) const {
        std::vector<uint64_t> bits((supports.size() + 63) / 64, ~uint64_t(0));
        if (supports.size() % 64) bits.back() = (uint64_t(1) << (supports.size() % 64)) - 1;
        for (auto p : pairs) {
            if (!forbidden[p].empty()) {
                for (size_t i = 0; i < bits.size(); ++i) bits[i] &= ~forbidden[p][i];
            } else {
                for (size_t i = 0; i < supports.size(); ++i)
                    if (std::popcount(supports[i] & p) >= 3)
                        bits[i / 64] &= ~(uint64_t(1) << (i % 64));
            }
        }
        Rows result;
        for (size_t i = 0; i < bits.size(); ++i)
            for (auto v = bits[i]; v; v &= v - 1)
                result.push_back(supports[64 * i + std::countr_zero(v)]);
        return result;
    }
};

class HeavyCompletion {
    const std::array<RowLayer, 3>& layers;
    const Rows& original;
    const int peer;
    Rows fixed;
    uint64_t found = 0;

    void emit() {
        ++found;
        std::cout << "heavy";
        for (auto m : original) std::cout << ' ' << m;
        const Mask low = (1u << peer) - 1;
        for (size_t i = original.size(); i < fixed.size(); ++i)
            std::cout << ' ' << ((fixed[i] & low) | ((fixed[i] & ~low) << 1));
        std::cout << '\n';
    }

    void choose(std::array<int, 3> left, const std::array<Rows, 3>& pools,
                const Degrees& counts, const Degrees& deficits) {
        int remaining = left[0] + left[1] + left[2];
        int tens = 0, possible_tens = 0;
        Mask must = 0, avoid = 0;
        for (int i = 0; i < 15; ++i) {
            const int have = counts[i];
            if (have > 10 || have + remaining < 9) return;
            if (have == 10) {
                ++tens;
                avoid |= 1u << i;
            }
            if (have + remaining == 9) must |= 1u << i;

            // Upper bound on D for a ten-column, filling it with the largest
            // deficits still available. The two marked columns already have degree nine.
            const int take = 10 - have;
            const int sixes = std::min(left[0], take);
            const int gain = 2 * sixes + std::min(take - sixes, left[1]);
            if (take <= remaining && deficits[i] + gain >= 4) ++possible_tens;
            if (!remaining && deficits[i] < (have == 10 ? 4 : 1)) return;
        }
        if (tens > 2 || possible_tens < 2) return;
        if (!remaining) {
            if (tens == 2) emit();
            return;
        }

        int layer = 2;
        while (!left[layer]) --layer;
        if (int(pools[layer].size()) < left[layer]) return;
        --left[layer];
        for (size_t j = 0; j + left[layer] < pools[layer].size(); ++j) {
            Mask m = pools[layer][j];
            if ((m & must) != must || (m & avoid)) continue;
            std::array<Rows, 3> next;
            bool enough = true;
            for (int t = layer; t >= 0; --t) {
                if (!left[t]) continue;
                for (size_t i = t == layer ? j + 1 : 0; i < pools[t].size(); ++i) {
                    Mask other = pools[t][i], common = m & other;
                    if (std::popcount(common) > 2 &&
                        std::any_of(fixed.begin(), fixed.end(), [common](Mask r) {
                            return std::popcount(r & common) > 2;
                        })) continue;
                    next[t].push_back(other);
                }
                if (int(next[t].size()) < left[t]) {
                    enough = false;
                    break;
                }
            }
            if (!enough) continue;
            auto c = counts, d = deficits;
            for (Mask v = m; v; v &= v - 1) {
                int i = std::countr_zero(v);
                ++c[i];
                d[i] += 2 - layer;
            }
            fixed.push_back(m);
            choose(left, next, c, d);
            fixed.pop_back();
        }
    }

public:
    HeavyCompletion(const std::array<RowLayer, 3>& layers, const Rows& rows, int peer)
        : layers(layers), original(rows), peer(peer) {}

    uint64_t run() {
        const int n = 20 - original.size();
        const Mask low = (1u << peer) - 1;
        int known_sevens = 0;
        Degrees counts{}, deficits{};
        for (auto r : original) {
            int degree = std::popcount(r);
            known_sevens += degree == 7;
            // Remove the left mark (bit 16) and the right mark (bit peer).
            Mask m = (r & low) | ((r >> 1) & ~low & 32767);
            fixed.push_back(m);
            for (Mask v = m; v; v &= v - 1) {
                int i = std::countr_zero(v);
                ++counts[i];
                deficits[i] += 8 - degree;
            }
        }
        Rows pairs;
        for (size_t i = 0; i < fixed.size(); ++i)
            for (size_t j = 0; j < i; ++j) {
                auto p = fixed[i] & fixed[j];
                if (std::popcount(p) > 2) pairs.push_back(p);
            }
        std::sort(pairs.begin(), pairs.end());
        pairs.erase(std::unique(pairs.begin(), pairs.end()), pairs.end());
        std::array<Rows, 3> pools;
        for (int t = 0; t < 3; ++t) pools[t] = layers[t].allowed(pairs);
        for (int six = 0; six <= 1; ++six) {
            int seven = 5 - 2 * six - known_sevens;
            int eight = n - six - seven;
            if (seven >= 0 && eight >= 0) choose({six, seven, eight}, pools, counts, deficits);
        }
        return found;
    }
};
