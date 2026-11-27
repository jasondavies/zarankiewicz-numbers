#include "../z18x19-k33/seven_columns.hpp"
#include <algorithm>
#include <cstdint>

using Bits = std::vector<uint64_t>;
struct Search {
    Lines blocks,fixed,options;
    std::vector<Bits> by_cell,edges;
    int floor=9,ordinary=10;
    int degree[19],base[19],demand[19],words=0;
    std::vector<int> sum; // Entries of the ten fixed rows on a subset of columns.
    std::vector<unsigned char> legal;
    std::vector<Lines> compulsory_one,compulsory_two;
    bool meets_all(Mask p,const Lines& sets,int need) {
        for(Mask s:sets)if(std::popcount(s&p)<need)return false;
        return true;
    }
    // Every remaining row contributes at most two on a pair intersection.
    bool obligations(Mask common,int unknown,Lines& one,Lines& two) {
        int n=std::popcount(common);
        if(n>5)return false;
        if(n<3)return true;
        int need=floor*n-sum[common]-2*(unknown-1);
        if(need>2)return false;
        if(need==2)two.push_back(common);
        if(need==1)one.push_back(common);
        return true;
    }
    // Two new rows leave nine unassigned rows, each supplying at most two.
    bool pair_ok(Mask both) {
        if(std::popcount(both)<=2)return true;
        auto& v=legal[both];
        if(!v){
            v=1;
            if(std::popcount(both)>5 || (floor-2)*std::popcount(both)>sum[both]+18)v=2;
            for(Mask p:fixed)if(std::popcount(p&both)>2){v=2;break;}
        }
        return v==1;
    }
    bool search(const Bits& pool,const Lines& picked,int left) {
        if(!left)return true;
        int count=0;
        for(uint64_t w:pool)count+=std::popcount(w);
        if(count<left)return false;
        // Branch on a cell still required by at least one ordinary row.
        int pivot=-1,smallest=10000000;
        for(int i=0;i<19;++i){
            int need=demand[i]-degree[i];if(need<=0)continue;
            if(need>left)return false;
            int have=0;for(int w=0;w<words;++w)have+=std::popcount(pool[w]&by_cell[i][w]);
            if(have<need)return false;
            if(have-need<smallest){smallest=have-need;pivot=i;}
        }
        // Assign each completion to its earliest chosen supporter of the pivot.
        Bits unused=pool;
        for(int w=0;w<words;++w){
            uint64_t cand=pivot>=0?pool[w]&by_cell[pivot][w]:pool[w];
            for(;cand;cand&=cand-1){
                int v=w*64+std::countr_zero(cand);
                unused[w]&=~(uint64_t(1)<<(v%64));
                Mask p=options[v];
                bool ok=true;
                for(int i=0;i<19;++i){
                    int val=degree[i]+int((p>>i)&1);
                    if(base[i]+val>10 || val+left-1<demand[i]) {ok=false;break;}
                }
                if(!ok)continue;
                Bits next(words);
                if(left>1){
                    int room=0;
                    for(int i=0;i<words;++i){next[i]=unused[i]&edges[v][i];room+=std::popcount(next[i]);}
                    if(room<left-1)continue;
                    for(Mask q:picked){
                        Mask s=p&q;if(std::popcount(s)<=2)continue;
                        for(int j=0;j<words;++j)for(auto b=next[j];b;b&=b-1){
                            int k=std::countr_zero(b);
                            if(std::popcount(options[j*64+k]&s)>2){next[j]&=~(uint64_t(1)<<k);--room;}
                        }
                        if(room<left-1)break;
                    }
                    if(room<left-1)continue;
                }
                for(Mask x=p;x;x&=x-1)++degree[std::countr_zero(x)];
                Lines now=picked;now.push_back(p);
                if(search(next,now,left-1))return true;
                for(Mask x=p;x;x&=x-1)--degree[std::countr_zero(x)];
            }
        }
        return false;
    }
    bool run() {
        fixed.assign(10,0);
        for(int j=0;j<19;++j){
            for(Mask x=blocks[j];x;x&=x-1)fixed[std::countr_zero(x)]|=1u<<j;
            base[j]=std::popcount(blocks[j]); demand[j]=floor-(11-ordinary)-base[j];degree[j]=0;
        }
        sum.resize(1<<19);
        // Only sum values on masks of size at most five can occur.
        static std::vector<Mask> small;
        if(small.empty())for(Mask x=1;x<(1u<<19);++x)if(std::popcount(x)<=5)small.push_back(x);
        for(Mask x:small)sum[x]=sum[x&(x-1)]+base[std::countr_zero(x)];
        Lines must1,must2;
        for(int i=0;i<10;++i)for(int j=0;j<i;++j)
            if(!obligations(fixed[i]&fixed[j],11,must1,must2))return false;
        LineExtensions<19> ext;ext.fixed=fixed;ext.run(0,9);
        options.clear();compulsory_one.clear();compulsory_two.clear();
        for(Mask p:ext.allowed){
            if(!meets_all(p,must1,1)||!meets_all(p,must2,2))continue;
            Lines one,two;bool ok=true;
            for(Mask f:fixed){
                Mask s=f&p;int n=std::popcount(s);
                if(n>5){ok=false;break;}
                if(n<3)continue;
                int need=(floor-1)*n-sum[s]-18;
                if(need>2){ok=false;break;}
                if(need==2)two.push_back(s);
                else if(need==1)one.push_back(s);
            }
            if(ok){options.push_back(p);compulsory_one.push_back(one);compulsory_two.push_back(two);}
        }
        int size=options.size();if(size<ordinary)return false;
        words=(size+63)/64;
        by_cell.assign(19,Bits(words));edges.assign(size,Bits(words));legal.assign(1<<19,0);
        for(int i=0;i<size;++i){
            Mask p=options[i];
            for(Mask x=p;x;x&=x-1)by_cell[std::countr_zero(x)][i/64]|=uint64_t(1)<<(i%64);
            for(int j=0;j<i;++j){
                Mask q=options[j];
                if(pair_ok(p&q) && meets_all(p,compulsory_one[j],1) && meets_all(p,compulsory_two[j],2) &&
                        meets_all(q,compulsory_one[i],1) && meets_all(q,compulsory_two[i],2)){
                    edges[i][j/64]|=uint64_t(1)<<(j%64);
                    edges[j][i/64]|=uint64_t(1)<<(i%64);
                }
            }
        }
        Bits free(words,~uint64_t(0));if(size%64)free.back()=(uint64_t(1)<<(size%64))-1;
        return search(free,{},ordinary);
    }
};
int main(int argc,char**argv){
    if(argc!=1 && argc!=3)return 2;
    Search solver;
    if(argc==3){
        solver.ordinary=std::stoi(argv[1]);
        solver.floor=std::stoi(argv[2]);
        if(solver.ordinary<1 || solver.ordinary>11 || solver.floor<1 || solver.floor>10)return 2;
    }
    int n=0,passed=0;std::string s;
    while(std::getline(std::cin,s)){
        std::istringstream in(s);solver.blocks.clear();
        for(Mask x;in>>x;){if(x>=1024)return 2;solver.blocks.push_back(x);}
        if(solver.blocks.size()!=19)return 2;
        if(solver.run()){std::cout<<s<<'\n';++passed;}++n;
    }
    std::cerr<<n<<" marks, "<<passed<<" survive\n";
}
