// Enumerate block multisets on ten points with a prescribed total-size floor and load range.
#include "../z16x18-k33/block_families.hpp"
#include <array>
#include <iostream>
#include <sstream>
#include <string>

using Loads = std::array<int,10>;
std::array<Blocks,6> by_size;
std::set<Blocks> answers;
int maximum_load = 9;
int block_count = 17, minimum_total = 70, minimum_load = 7;

void tails(Blocks& base, const Blocks& pool, size_t start, int weight, Loads loads) {
    int left = block_count - base.size();
    if (weight + 3 * left < minimum_total) return;
    for (int d : loads) if (d > maximum_load || d + left < minimum_load) return;
    if (!left) {
        answers.insert(canonical_blocks(10,base));
        return;
    }
    for (size_t i = start; i < pool.size(); ++i) {
        unsigned b = pool[i];
        int d = std::popcount(b);
        if (weight + d*left < minimum_total) break;
        auto next = loads;
        for (int j=0; j<10; ++j) next[j] += b >> j & 1u;
        base.push_back(b);
        tails(base,pool,i+int(d==3),weight+d,next);
        base.pop_back();
    }
}

void fours(Blocks& base, const Blocks& pool, int need, int weight, const Loads& loads) {
    if (int(pool.size()) < need) return;
    int remaining = block_count - base.size();
    for (int d : loads) if (d > maximum_load || d + remaining < minimum_load) return;
    if (!need) {
        Blocks small;
        if (remaining)
            for (int d=3; d>=0 && weight+d+3*(remaining-1)>=minimum_total; --d)
                for (unsigned b : by_size[d]) if (fits(b,base)) small.push_back(b);
        tails(base,small,0,weight,loads);
        return;
    }
    for (size_t i=0; i+need<=pool.size(); ++i) {
        unsigned b = pool[i];
        Blocks next;
        for (size_t j=i+1; j<pool.size(); ++j)
            if (std::popcount(b & pool[j]) <= 2) next.push_back(pool[j]);
        auto degrees = loads;
        for (int j=0; j<10; ++j) degrees[j] += b >> j & 1u;
        base.push_back(b);
        fours(base,next,need-1,weight+4,degrees);
        base.pop_back();
    }
}

void explore(const Blocks& fives) {
    int m = fives.size(), qmin = std::max(0,minimum_total-3*block_count-2*m), qmax=block_count-m;
    std::set<Blocks> level;
    for (int point=0; point<10; ++point) {
        Blocks marked=fives;
        marked.push_back(1u<<point);
        level.insert(canonical_blocks(10,marked));
    }
    for (int p=0; p<=maximum_load && !level.empty(); ++p) {
        std::set<Blocks> next;
        for (const auto& state : level) {
            Blocks base=state;
            auto it=std::find_if(base.begin(),base.end(),[](unsigned x){return std::popcount(x)==1;});
            unsigned pivot=*it;
            base.erase(it);
            Blocks off;
            Loads loads{};
            for (unsigned b : base) for (int j=0; j<10; ++j) loads[j] += b >> j & 1u;
            if (*std::max_element(loads.begin(),loads.end())>maximum_load) continue;
            for (unsigned b : by_size[4]) {
                if (!fits(b,base)) continue;
                if (!(b & pivot)) off.push_back(b);
                else if (p<maximum_load && p<qmax) {
                    Blocks child=state;
                    child.push_back(b);
                    next.insert(canonical_blocks(10,child));
                }
            }
            // Choose a point of maximum four-block frequency. The q fours
            // contribute 4*q incidences, at most p at each of the ten points.
            for (int q=std::max(p,qmin); q<=qmax && 4*q<=10*p; ++q)
                fours(base,off,q-p,5*m+4*p,loads);
        }
        level.swap(next);
    }
}

int main(int argc, char** argv) {
    if (argc != 1 && argc != 2 && argc != 5) return 2;
    if (argc >= 2) maximum_load = std::stoi(argv[1]);
    if (argc == 5) {
        block_count = std::stoi(argv[2]);
        minimum_total = std::stoi(argv[3]);
        minimum_load = std::stoi(argv[4]);
    }
    // The input consists of nonempty five-block families. The total must force one.
    if (block_count < 1 || block_count > 20 || minimum_total <= 4*block_count ||
        minimum_total > 5*block_count || minimum_load < 0 ||
        maximum_load < minimum_load || maximum_load > block_count) return 2;
    for (unsigned b=0; b<1024; ++b) if (std::popcount(b)<=5) by_size[std::popcount(b)].push_back(b);
    std::string line;
    while (std::getline(std::cin,line)) {
        std::istringstream input(line);
        Blocks fives;
        for (unsigned b; input>>b;) fives.push_back(b);
        if (int(fives.size()) < minimum_total-4*block_count) return 2;
        explore(fives);
    }
    for (const auto& base : answers) {
        for (auto b : base) std::cout << b << ' ';
        std::cout << '\n';
    }
}
