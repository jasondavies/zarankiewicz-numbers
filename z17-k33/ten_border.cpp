// c++ -O3 -std=c++20 ten_border.cpp -lnauty -o /tmp/ten-border
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <set>
#include <vector>
#include <nauty/nauty.h>

using Masks = std::vector<unsigned>;

// Reconstruct the actual incidence matrix in the chosen order. A repeated
// key is therefore an explicit row/column relabelling, even for tied vertices.
Masks key(const Masks& rows) {
    graph g[26]{}, canon[26]{};
    int lab[26], ptn[26], orbits[26];
    for (int i=0; i<26; ++i) { lab[i]=i; ptn[i]=(i!=15 && i!=25); }
    for (int r=0; r<16; ++r)
        for (int c=0; c<10; ++c)
            if (rows[r] & (1u<<c)) { ADDONEEDGE(g,r,16+c,1); }
    DEFAULTOPTIONS_GRAPH(options);
    options.getcanon=TRUE;
    options.defaultptn=FALSE;
    statsblk stats;
    densenauty(g,lab,ptn,orbits,&options,&stats,1,26,canon);
    Masks result;
    for (int i=0; i<16; ++i) {
        unsigned m=0;
        if (lab[i]>=16) std::abort();
        for (int j=0; j<10; ++j) {
            if (lab[16+j]<16) std::abort();
            m |= ((rows[lab[i]] >> (lab[16+j]-16)) & 1u) << j;
        }
        result.push_back(m);
    }
    return result;
}

bool extend(Masks& fixed, const Masks& pool, int needed, int weight) {
    if (!needed) return weight<=0;
    for (size_t i=0; i+needed<=pool.size(); ++i) {
        int bound=0;
        for (int j=0; j<needed; ++j) bound+=std::popcount(pool[i+j]);
        if (bound<weight) break;
        unsigned x=pool[i];
        Masks next;
        for (size_t j=i+1; j<pool.size(); ++j) {
            unsigned pair=x & pool[j];
            if (std::all_of(fixed.begin(),fixed.end(),[pair](unsigned z){
                return std::popcount(z & pair)<=2;
            })) next.push_back(pool[j]);
        }
        fixed.push_back(x);
        if (extend(fixed,next,needed-1,weight-std::popcount(x))) return true;
        fixed.pop_back();
    }
    return false;
}

int main() {
    std::set<Masks> seen;
    Masks rows(16);
    unsigned long total=0, survivors=0;
    while (std::cin>>rows[0]) {
        for (int i=1; i<16; ++i) if (!(std::cin>>rows[i])) return 2;
        ++total;
        if (!seen.insert(key(rows)).second) continue;
        Masks cols(10), pairs;
        for (int c=0; c<10; ++c)
            for (int r=0; r<16; ++r) cols[c]|=((rows[r]>>c)&1u)<<r;
        int weight=10, deficit=0;
        for (int c=0; c<10; ++c) {
            int d=std::popcount(cols[c])+1;
            weight+=d-1;
            deficit+=std::max(0,8-d);
            for (int j=0; j<c; ++j) pairs.push_back(cols[c]&cols[j]);
        }
        Masks pool;
        for (int d=10; d>=8-(3-deficit); --d)
            for (unsigned m=0; m<(1u<<16); ++m)
                if (std::popcount(m)==d && std::all_of(pairs.begin(),pairs.end(),[m](unsigned p){
                    return std::popcount(m&p)<=2;
                })) pool.push_back(m);
        if (extend(cols,pool,7,139-weight)) {
            ++survivors;
            if (survivors==1) {
                std::cout<<"First completion (columns on 16 rows, marked row uses first ten):";
                for (auto c:cols) std::cout<<" "<<c;
                std::cout<<std::endl;
            }
        }
    }
    std::cout<<"Cores "<<total<<", inequivalent keys "<<seen.size()
             <<", keys admitting a border "<<survivors<<std::endl;
    return total==37048 && seen.size()==519 && survivors==0 ? 0 : 1;
}
