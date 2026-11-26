// Direct independent completion test, with no nauty dependency.
// c++ -O3 -std=c++20 audit_core_catalogue.cpp -o /tmp/audit-nine
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using Mask = unsigned;
using Masks = std::vector<Mask>;

struct WeightLayer {
    Masks masks;
    std::vector<std::vector<uint64_t>> bad;
    int words;
    WeightLayer(int n,int weight) : bad(1u<<n) {
        for (Mask m=0; m<(1u<<n); ++m)
            if (std::popcount(m)==weight) masks.push_back(m);
        words=(masks.size()+63)/64;
    }
    Masks allowed(const Masks& pairs) {
        std::vector<uint64_t> excluded(words);
        for (Mask p:pairs) {
            if (std::popcount(p)<3) continue;
            auto& flags=bad[p];
            if (flags.empty()) {
                flags.resize(words);
                for (size_t j=0;j<masks.size();++j)
                    if (std::popcount(p&masks[j])>2) flags[j/64]|=uint64_t(1)<<(j%64);
            }
            for (int j=0;j<words;++j) excluded[j]|=flags[j];
        }
        Masks result;
        for (int j=0;j<words;++j) {
            auto bits=~excluded[j];
            if (j==words-1 && masks.size()%64) bits&=(uint64_t(1)<<(masks.size()%64))-1;
            while (bits) {
                result.push_back(masks[64*j+std::countr_zero(bits)]);
                bits&=bits-1;
            }
        }
        return result;
    }
};

// Recursively choose an increasing subsequence of the candidate indices.
bool possible(Masks& fixed,const Masks& pool,int need,int target, Masks* witness=nullptr) {
    if (!need) {
        if (target==0 && witness) *witness=fixed;
        return target==0;
    }
    for (size_t i=0; i+need<=pool.size(); ++i) {
        int upper=0;
        for (int j=0;j<need;++j) upper+=std::popcount(pool[i+j]);
        if (upper<target) return false;
        Mask x=pool[i];
        Masks available;
        for (size_t j=i+1; j<pool.size();++j) {
            Mask pair=x&pool[j];
            if (std::all_of(fixed.begin(),fixed.end(),[pair](Mask a){
                    return std::popcount(a&pair)<3;
                })) available.push_back(pool[j]);
        }
        fixed.push_back(x);
        bool yes=possible(fixed,available,need-1,target-std::popcount(x),witness);
        fixed.pop_back();
        if (yes) return true;
    }
    return false;
}

int main(int argc,char** argv) {
    if (argc!=3 && argc!=4) return 2;
    if (argc==4 && std::string(argv[3])!="--show") return 2;
    bool column=std::string(argv[1])=="column";
    std::string mode=argv[2];
    bool regular=mode=="regular139";
    if (mode!="6" && mode!="7" && !regular) return 2;
    int border=regular?0:std::stoi(mode);
    if ((!column && std::string(argv[1])!="row") || (regular && !column)) return 2;
    int n=column?16:15, k=column && !regular?7:8, high=column?9:8, low=regular?8:(column?7:6);
    std::vector<WeightLayer> layers;
    for (int d=high;d>=low;--d) layers.emplace_back(n,d);
    Masks blocks(n);
    size_t total=0, heavy_exclusions=0, relaxed_completions=0;
    while (std::cin>>blocks[0]) {
        for (int i=1;i<n;++i) if (!(std::cin>>blocks[i])) return 2;
        Masks fixed(9), pairs;
        int target=139-border-9;
        for (int i=0;i<n;++i) {
            target-=std::popcount(blocks[i]);
            for (int j=0;j<i;++j)
                if (std::popcount(blocks[i]&blocks[j])>2) throw std::logic_error("invalid projection");
            for (int j=0;j<9;++j) fixed[j]|=((blocks[i]>>j)&1u)<<i;
        }
        for (int j=0;j<9;++j) for (int i=0;i<j;++i) pairs.push_back(fixed[i]&fixed[j]);
        Masks pool=layers[0].allowed(pairs);
        int heavy=target-(high-1)*k;
        ++total;
        if (heavy>0 && !possible(fixed,pool,heavy,heavy*high)) {
            ++heavy_exclusions;
            continue;
        }
        for (int d=high-1;d>=std::max(low,target-(k-1)*high);--d) {
            Masks more=layers[high-d].allowed(pairs);
            pool.insert(pool.end(),more.begin(),more.end());
        }
        Masks witness;
        if (possible(fixed,pool,k,target,&witness)) {
            ++relaxed_completions;
            if (argc==4) {
                // Reinsert the bit for the marked line in the nine fixed lines.
                std::cout<<"core";
                for (size_t j=0;j<witness.size();++j)
                    std::cout<<' '<<(witness[j]|(j<9 ? (1u<<n) : 0u));
                std::cout<<std::endl;
            }
        }
    }
    std::cout<<total<<" projections, "<<heavy_exclusions
             <<" excluded using maximum-weight lines alone, "<<relaxed_completions
             <<" admit a completion before final degree tests\n";
}
