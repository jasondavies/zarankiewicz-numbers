#include "../z18x19-k33/seven_columns.hpp"
#include <algorithm>
#include <array>
#include <numeric>
struct Solver{
    Lines cols, candidates, added;
    std::array<int,20> need{};
    std::vector<unsigned char> cache;
    bool pair_allowed(Mask a,Mask b){
        Mask h=a&b;if(std::popcount(h)<=2)return true;
        if(std::popcount(h)>5)return false;
        auto& state=cache[h];
        if(state==0){
            state=1;
            for(Mask c:cols)if(std::popcount(c&h)>2){state=2;break;}
        }
        if(state==2)return false;
        return std::none_of(added.begin(),added.end(),[h](Mask c){return std::popcount(c&h)>2;});
    }
    bool search(const Lines& options,int left){
        if(!left)return std::all_of(need.begin(),need.end(),[](int k){return !k;});
        Mask must=0,avoid=0;
        for(int i=0;i<20;++i){
            if(need[i]<0||need[i]>left)return false;
            if(need[i]==left)must|=1u<<i;
            if(need[i]==0)avoid|=1u<<i;
        }
        std::array<int,20> cover{};Lines pool;
        for(Mask p:options)if((p&must)==must && !(p&avoid)){
            pool.push_back(p);for(Mask s=p;s;s&=s-1)++cover[std::countr_zero(s)];
        }
        if((int)pool.size()<left)return false;
        int pivot=-1;
        for(int i=0;i<20;++i){
            if(cover[i]<need[i] || (int)pool.size()-cover[i]<left-need[i])return false;
            if(need[i] && (pivot<0 || cover[i]-need[i]<cover[pivot]-need[pivot]))pivot=i;
        }
        if(pivot<0)return false;
        Mask pbit=1u<<pivot;
        for(size_t i=0;i<pool.size();++i){
            Mask p=pool[i];if(!(p&pbit))continue;
            Lines next;
            for(size_t j=0;j<pool.size();++j){
                if(j<=i && (pool[j]&pbit))continue;
                if(pair_allowed(p,pool[j]))next.push_back(pool[j]);
            }
            if((int)next.size()<left-1)continue;
            for(Mask s=p;s;s&=s-1)--need[std::countr_zero(s)];
            added.push_back(p);
            if(search(next,left-1))return true;
            added.pop_back();
            for(Mask s=p;s;s&=s-1)++need[std::countr_zero(s)];
        }
        return false;
    }
    bool run(const Lines& b, Mask shortrows,Mask c,Mask d){
        cols.assign(7,0);added.clear();
        for(int i=0;i<20;++i)for(Mask s=b[i];s;s&=s-1)cols[std::countr_zero(s)]|=1u<<i;
        cols.push_back(c);cols.push_back(d);
        LineExtensions<20> ext;ext.fixed=cols;ext.run(0,9);
        for(auto &col:cols)col|=1u<<20;
        candidates.clear();
        for(Mask s:ext.allowed)if(std::none_of(cols.begin(),cols.end(),[s](Mask v){return std::popcount(s&v)>5;}))candidates.push_back(s);
        for(int i=0;i<20;++i)need[i]=9-((shortrows>>i)&1)-std::popcount(b[i]);
        cache.assign(1<<20,0);
        return search(candidates,13);
    }
};
int main(){
 Solver solver;std::string s;int seen=0;
 while(std::getline(std::cin,s)){
    std::istringstream in(s);Mask ab,c,t;if(!(in>>ab>>c>>t))return 2;Lines b;for(Mask a;in>>a;)b.push_back(a);
    if(b.size()!=20)return 2;++seen;
    if(solver.run(b,ab,c,t)){
        std::cout<<"solution";for(auto a:solver.cols)std::cout<<' '<<a;for(auto a:solver.added)std::cout<<' '<<a;std::cout<<'\n';return 0;
    }
 }
 std::cout<<"excluded "<<seen<<'\n';
}
