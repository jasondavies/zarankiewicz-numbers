#pragma once
#include <array>
#include <bit>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using Mask = unsigned;
using Lines = std::vector<Mask>;

struct Extensions {
    std::array<std::array<Mask, 18>, 18> forbidden{};
    Lines allowed, fixed;
    void supports(Mask pool, Mask chosen, int left) {
        if (!left) {
            allowed.push_back(chosen);
            return;
        }
        while (std::popcount(pool) >= left) {
            Mask bit = pool & -pool;
            pool ^= bit;
            int j = std::countr_zero(bit);
            Mask next = pool;
            for (Mask s = chosen; s; s &= s - 1)
                next &= ~forbidden[j][std::countr_zero(s)];
            supports(next, chosen | bit, left - 1);
        }
    }
    bool choose(const Lines &pool, int left) {
        if (!left)
            return true;
        for (size_t i = 0; i + left <= pool.size(); ++i) {
            Mask a = pool[i];
            Lines next;
            for (size_t j = i + 1; j < pool.size(); ++j) {
                Mask both = a & pool[j];
                bool ok = true;
                if (std::popcount(both) >= 3)
                    for (Mask b : fixed)
                        if (std::popcount(both & b) >= 3) {
                            ok = false;
                            break;
                        }
                if (ok)
                    next.push_back(pool[j]);
            }
            fixed.push_back(a);
            if (choose(next, left - 1))
                return true;
            fixed.pop_back();
        }
        return false;
    }
    bool run(int k) {
        std::array<Mask, 18> rows{};
        for (size_t j = 0; j < fixed.size(); ++j)
            for (Mask s = fixed[j]; s; s &= s - 1)
                rows[std::countr_zero(s)] |= 1u << j;
        for (int j = 0; j < 18; ++j)
            for (int i = 0; i < j; ++i)
                for (int h = 0; h < i; ++h)
                    if (std::popcount(rows[j] & rows[i] & rows[h]) >= 2)
                        forbidden[i][h] |= 1u << j;
        supports((1u << 18) - 1, 0, 7);
        return choose(allowed, k);
    }
};
