// c++ -O3 -std=c++20 six_row_core.cpp -lnauty -o /tmp/six-row-core
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
#include <nauty/nauty.h>

using Mask = unsigned;
using Blocks = std::vector<Mask>;
int size_of(Mask m) { return std::popcount(m); }

// The first nine vertices of the incidence graph are the points. Return
// actual relabelled blocks as the key, so equality always certifies isomorphism.
Blocks canonical(const Blocks& blocks, bool marked_point) {
    const int n = 9 + blocks.size();
    graph g[32]{}, canon[32]{};
    int lab[32], ptn[32], orbits[32];
    for (int i=0; i<n; ++i) { lab[i]=i; ptn[i]=(i!=8 && i!=n-1); }
    if (marked_point) ptn[7]=0;
    for (int i=9; i<n; ++i)
        for (int j=0; j<9; ++j)
            if (blocks[i-9] & (1u<<j)) { ADDONEEDGE(g,i,j,1); }
    DEFAULTOPTIONS_GRAPH(opt);
    opt.getcanon=TRUE;
    opt.defaultptn=FALSE;
    statsblk stats;
    densenauty(g,lab,ptn,orbits,&opt,&stats,1,n,canon);
    for (int j=0;j<9;++j)
        if (lab[j]>=9) throw std::logic_error("point partition changed");
    if (marked_point && lab[8]!=8) throw std::logic_error("distinguished point changed");
    Blocks out(blocks.size());
    for (int i=0; i<int(blocks.size()); ++i)
        for (int j=0; j<9; ++j)
            out[i]|=((blocks[i]>>lab[j])&1u)<<j;
    std::sort(out.begin(),out.end());
    return out;
}

bool fits(Mask x, const Blocks& fixed) {
    for (Mask b:fixed) if (size_of(x&b)>2) return false;
    return true;
}
using Families = std::set<Blocks>;
Families augment(const Families& old, int weight, bool through_pivot) {
    Families result;
    for (auto blocks:old)
        for (Mask x=0; x<512; ++x) {
            if (size_of(x)!=weight || (through_pivot && !(x&256)) || !fits(x,blocks)) continue;
            blocks.push_back(x);
            result.insert(canonical(blocks,true));
            blocks.pop_back();
        }
    return result;
}

struct Search {
    // In column mode the marked column contains nine of the sixteen rows.
    // In row mode there are no degree-nine core columns, and a nine-row is marked.
    bool column;
    int nblocks, border, core_weight, max_sevens, min_sum, max_load, deficit_budget;
    std::array<Blocks,6> masks;
    Families skeletons, projections;
    std::map<int,size_t> projection_weights;
    uint64_t full_cores=0, witnessed=0;
    bool found=false, catalogue_only=false;
    std::ofstream catalogue;

    Search(bool mark_column, int border_degree) : column(mark_column), nblocks(column?16:15),
        border(border_degree), core_weight(border==-1?139:(border==8?129:139-border)),
        max_sevens(border==8 || border==-1?0:(border==6?1:2)),
        min_sum(column?63-max_sevens:(border==8?60:63-(136-core_weight))), max_load(column?8:7),
        deficit_budget(column?max_sevens:(border==8?3:136-core_weight)) {
        for (Mask x=0; x<512; ++x)
            if (size_of(x)<=5) masks[size_of(x)].push_back(x);
    }

    bool degrees_possible(const Blocks& b, int missing) const {
        int deficit=0;
        for (int i=0; i<9; ++i) {
            int d=0;
            for (Mask x:b) d+=(x>>i)&1;
            if (d>max_load || d+missing<(column?6:5)) return false;
            deficit+=std::max(0,7-d-missing);
        }
        return deficit<=deficit_budget;
    }

    // Enumerate further lines of the core, then test six-row extension.
    void check_core(const Blocks& fixed) {
        if (border==-1) {
            int sum=0;
            for (size_t i=0;i<fixed.size();++i) {
                sum+=size_of(fixed[i]);
                for (size_t j=0;j<i;++j) for (size_t k=0;k<j;++k)
                    if (size_of(fixed[i]&fixed[j]&fixed[k])>2) throw std::logic_error("invalid matrix");
            }
            if (fixed.size()!=17 || sum!=core_weight) throw std::logic_error("wrong size or weight");
            for (auto r:fixed) {
                for (int j=0;j<17;++j) std::cout<<((r>>j)&1u);
                std::cout<<'\n';
            }
            ++witnessed;
            found=true;
            return;
        }
        Blocks rows;
        if (column) rows=fixed;
        else {
            for (int j=0;j<=nblocks;++j) {
                Mask x=0;
                for (int i=0;i<int(fixed.size());++i) x|=((fixed[i]>>j)&1u)<<i;
                rows.push_back(x);
            }
        }
        int total=0, sevens=0;
        for (Mask r:rows) {
            int d=size_of(r);
            if (d<7 || d>9) return;
            total+=d; sevens+=(d==7);
        }
        if (rows.size()!=16 || total!=core_weight || sevens>max_sevens) return;
        for (int j=0;j<17;++j) {
            int d=0;
            for (Mask r:rows) d+=(r>>j)&1;
            if (d<6 || d>(column?9:8)) return;
        }
        ++full_cores;
        for (Mask x=0;x<(1u<<17);++x) {
            if (size_of(x)!=border) continue;
            bool ok=true;
            for (int i=0;i<16 && ok;++i) for (int j=0;j<i;++j)
                if (size_of(x&rows[i]&rows[j])>2) {ok=false;break;}
            if (!ok) continue;
            ++witnessed;
            rows.push_back(x);
            for (size_t i=0; i<rows.size(); ++i)
                for (size_t j=0; j<i; ++j)
                    for (size_t k=0; k<j; ++k)
                        if (size_of(rows[i]&rows[j]&rows[k])>2) throw std::logic_error("invalid witness");
            for (Mask r:rows) {
                for (int j=0;j<17;++j) std::cout<<((r>>j)&1u);
                std::cout<<'\n';
            }
            found=true;
            return;
        }
    }

    void extend(Blocks& fixed, const Blocks& pool, int needed, int weight) {
        if (!needed) { if (!weight) check_core(fixed); return; }
        for (size_t i=0; i+needed<=pool.size() && !found; ++i) {
            int upper=0;
            for (int k=0;k<needed;++k) upper+=size_of(pool[i+k]);
            if (upper<weight) break;
            Mask x=pool[i];
            if (size_of(x)+(needed-1)*(column?7:6)>weight) continue;
            Blocks next;
            for (size_t j=i+1;j<pool.size();++j) {
                Mask p=x&pool[j];
                if (std::all_of(fixed.begin(),fixed.end(),[p](Mask r){return size_of(p&r)<=2;}))
                    next.push_back(pool[j]);
            }
            fixed.push_back(x);
            extend(fixed,next,needed-1,weight-size_of(x));
            fixed.pop_back();
        }
    }

    void complete(const Blocks& blocks, int weight) {
        Blocks fixed(9,1u<<nblocks);
        for (int j=0;j<nblocks;++j)
            for (int i=0;i<9;++i) fixed[i]|=((blocks[j]>>i)&1u)<<j;
        // Build all extra lines as independent sets of the forbidden triples.
        // For a triple contained in a fixed pair, the third bit cannot follow
        // the first two. The marked column/row is zero in every extra line.
        Mask forbid[16][16]{};
        for (int i=0;i<9;++i) for (int j=0;j<i;++j) {
            Mask common=(fixed[i]&fixed[j])&((1u<<nblocks)-1);
            for (Mask s=common; s; s&=s-1) {
                int a=std::countr_zero(s);
                for (Mask t=s&(s-1); t; t&=t-1)
                    forbid[a][std::countr_zero(t)]|=t&(t-1);
            }
        }
        Blocks pool;
        int high=column?9:8;
        int needed=column && border>0?7:8;
        int target=core_weight-weight-9;
        if (target>high*needed) return;
        int low=std::max(border==-1?8:(column?7:6),target-(needed-1)*high);
        auto visit=[&](auto&& self, Mask chosen, Mask left, int d)->void {
            if (d>=low) pool.push_back(chosen);
            if (d==high) return;
            while (d+size_of(left)>=low && left) {
                Mask bit=left & -left;
                left^=bit;
                int j=std::countr_zero(bit);
                Mask next=left;
                for (Mask s=chosen; s; s&=s-1) next&=~forbid[std::countr_zero(s)][j];
                self(self,chosen|bit,next,d+1);
            }
        };
        visit(visit,0,(1u<<nblocks)-1,0);
        std::stable_sort(pool.begin(),pool.end(),[](Mask a,Mask b){return size_of(a)>size_of(b);});
        extend(fixed,pool,needed,target);
    }

    void small(Blocks& b, int weight, int remaining, int start, const Blocks& options) {
        if (found || weight+3*remaining<min_sum || !degrees_possible(b,remaining)) return;
        if (!remaining) {
            if (int(b.size())!=nblocks) throw std::logic_error("wrong projection length");
            auto key=canonical(b,false);
            if (projections.insert(key).second) {
                if (catalogue.is_open()) {
                    for (auto x:key) catalogue << x << ' ';
                    catalogue << '\n';
                }
                ++projection_weights[weight];
                if (!catalogue_only) complete(key,weight);
            }
            return;
        }
        for (int i=start;i<int(options.size());++i) {
            Mask x=options[i];
            if (weight+size_of(x)+3*(remaining-1)<min_sum) break;
            if (!fits(x,b)) continue;
            b.push_back(x);
            small(b,weight+size_of(x),remaining-1,i+(size_of(x)>=3),options);
            b.pop_back();
        }
    }

    void off_pivot(Blocks& b, const Blocks& pool, int p, int q, int weight) {
        if (found || !degrees_possible(b,nblocks-int(b.size()))) return;
        if (weight+3*(nblocks-int(b.size()))>=min_sum) {
            auto key=canonical(b,false);
            if (skeletons.insert(key).second) {
                Blocks options;
                for (int d=3;d>=0;--d)
                    for (auto x:masks[d]) if (fits(x,key)) options.push_back(x);
                small(key,weight,nblocks-int(key.size()),0,options);
            }
        }
        if (int(b.size())==nblocks) return;
        // The pivot lies in at least as many fours as any other point.
        if (4*(q+1)>9*p) return;
        for (size_t i=0;i<pool.size();++i) {
            int possible=std::min(nblocks-int(b.size()),int(pool.size()-i));
            if (weight+3*(nblocks-int(b.size()))+possible<min_sum) break;
            Mask x=pool[i];
            bool ok=true;
            for (int j=0;j<8;++j) if (x&(1u<<j)) {
                int count=1;
                for (auto y:b) if (size_of(y)==4) count+=(y>>j)&1u;
                if (count>p) {ok=false;break;}
            }
            if (!ok) continue;
            Blocks next;
            for (size_t j=i+1;j<pool.size();++j) if (size_of(x&pool[j])<=2) next.push_back(pool[j]);
            b.push_back(x);
            off_pivot(b,next,p,q+1,weight+4);
            b.pop_back();
        }
    }

    void run(int min_fives, int max_fives) {
        Families fives{{}};
        for (int m=0; m<=max_fives && !found; ++m) {
            if (m) fives=augment(fives,5,false);
            if (m<min_fives) continue;
            auto inside=fives;
            for (int p=0;p<=8 && !inside.empty() && !found;++p) {
                // q fours must satisfy 3*nblocks+2*m+q >= min_sum.
                if (9*p>=4*(min_sum-3*nblocks-2*m)) {
                    for (auto b:inside) {
                        Blocks pool;
                        for (Mask x:masks[4]) if (!(x&256) && fits(x,b)) pool.push_back(x);
                        off_pivot(b,pool,p,p,5*m+4*p);
                        if (found) break;
                    }
                }
                if (p<8) inside=augment(inside,4,true);
            }
            std::cout<<"fives "<<m<<", cumulative projections "<<projections.size()
                     <<", complete cores "<<full_cores<<", witnesses "<<witnessed<<std::endl;
        }
        for (auto [w,n]:projection_weights) std::cout<<"weight "<<w<<": "<<n<<'\n';
    }
};
int main(int argc,char** argv) {
    if ((argc<5 || argc>7) || (std::string(argv[1])!="row" && std::string(argv[1])!="column")) return 2;
    std::string mode=argv[2];
    int border;
    if (mode=="regular139") border=-1;
    else if (mode=="control137" || mode=="8") border=8;
    else if (mode=="6" || mode=="7") border=std::stoi(mode);
    else return 2;
    int lo=std::stoi(argv[3]), hi=std::stoi(argv[4]);
    if (border<=0 && std::string(argv[1])!="column") return 2;
    if (lo<0 || lo>hi || hi>3) return 2;
    Search search(std::string(argv[1])=="column",border);
    if (argc==7) {
        if (std::string(argv[6])!="--catalogue-only") return 2;
        search.catalogue_only=true;
        std::cout<<"Catalogue only, completion disabled\n";
    }
    if (argc>=6) {
        search.catalogue.open(argv[5]);
        if (!search.catalogue) throw std::runtime_error("cannot write catalogue");
    }
    search.run(lo,hi);
}
