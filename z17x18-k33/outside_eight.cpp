// Append one outside row of minimum degree to a projection on fewer rows.
#include "../z16x18-k33/block_families.hpp"
#include <array>
#include <iostream>
#include <sstream>
#include <string>

class Extension {
    const int points;
    const Blocks& blocks;
    std::array<std::array<unsigned,17>,17> forbidden{};
    std::array<unsigned,17> predecessor{};
    std::set<Blocks>& complete;

    void visit(unsigned pool, unsigned chosen, int need) {
        if (!need) {
            Blocks result = blocks;
            for (unsigned x = chosen; x; x &= x-1) result[std::countr_zero(x)] |= 1u << points;
            complete.insert(canonical_blocks(points+1,result));
            return;
        }
        while (std::popcount(pool) >= need) {
            unsigned bit = pool & -pool;
            pool ^= bit;
            int j = std::countr_zero(bit);
            if (predecessor[j] && !(predecessor[j] & chosen)) continue;
            unsigned remaining = pool;
            for (unsigned x = chosen; x; x &= x-1)
                remaining &= ~forbidden[j][std::countr_zero(x)];
            visit(remaining,chosen|bit,need-1);
        }
    }

public:
    Extension(int k,const Blocks& base,std::set<Blocks>& seen) : points(k),blocks(base),complete(seen) {
        for (int i = 0; i < 17; ++i) {
            if (blocks[i] >= (1u << points)) throw std::logic_error("outside mask exceeds point count");
            for (int j = 0; j < i; ++j) {
                if (blocks[i] == blocks[j]) predecessor[i] = 1u<<j;
                for (int k = j+1; k < i; ++k) {
                    int count = std::popcount(blocks[i] & blocks[j] & blocks[k]);
                    if (count > 2) throw std::logic_error("invalid seven-row projection");
                    if (count == 2) {
                        forbidden[i][j] |= 1u<<k;
                        forbidden[k][j] |= 1u<<i;
                        forbidden[i][k] |= 1u<<j;
                    }
                }
            }
        }
    }

    void run(int d) { visit((1u<<17)-1,0,d); }
};

int main(int argc,char** argv) {
    if (argc!=2 && argc!=5) return 2;
    const int d=std::stoi(argv[1]), points=argc==2 ? 7 : std::stoi(argv[2]);
    const int low=argc==2 ? 72 : std::stoi(argv[3]), high=argc==2 ? 73 : std::stoi(argv[4]);
    if (d<0 || d>17 || points<3 || points>8 || low>high) return 2;
    std::string line;
    std::set<Blocks> seen;
    while (std::getline(std::cin,line)) {
        std::istringstream input(line);
        Blocks blocks;
        for (unsigned b; input>>b;) blocks.push_back(b);
        if (blocks.size()!=17) throw std::logic_error("expected seventeen columns");
        int weight=d;
        for (auto b:blocks) weight+=std::popcount(b);
        if (weight<low || weight>high) continue;
        Extension(points,blocks,seen).run(d);
    }
    for (const auto& blocks:seen) {
        for (auto b:blocks) std::cout<<b<<' ';
        std::cout<<'\n';
    }
}
