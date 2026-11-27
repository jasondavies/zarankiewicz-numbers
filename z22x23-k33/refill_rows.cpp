#include "../z18x19-k33/seven_columns.hpp"
#include <algorithm>

bool choose(Lines& fixed, const Lines& pool, int left, int target) {
    if (!left) return target <= 0;
    for (size_t i=0; i+left<=pool.size(); ++i) {
        int bound=0;
        for (int k=0;k<left;++k) bound+=std::popcount(pool[i+k]);
        if (bound<target) break;
        Mask add=pool[i];
        Lines next;
        int weight=std::popcount(add);
        if (left>1) {
            for (size_t j=i+1; j<pool.size();++j) {
                if ((left-1)*std::popcount(pool[j]) < target-weight && next.empty()) break;
                Mask shared=pool[j]&add;
                if (std::popcount(shared)>2 && std::any_of(fixed.begin(),fixed.end(),
                        [shared](Mask r){return std::popcount(shared&r)>2;})) continue;
                next.push_back(pool[j]);
            }
        }
        fixed.push_back(add);
        if (choose(fixed,next,left-1,target-weight)) return true;
        fixed.pop_back();
    }
    return false;
}

int main(int argc,char** argv) {
    if(argc!=2) return 2;
    const int target=std::stoi(argv[1]);
    Lines original(23);
    for(Mask& r:original) if (!(std::cin>>r)) return 2;
    unsigned omit; long long cases=0;
    while(std::cin>>omit){
        Lines rows;
        int need=target;
        for(int j=0;j<23;++j) if(!(omit>>j&1)) {
            rows.push_back(original[j]);
            need-=std::popcount(original[j]);
        }
        int left=22-rows.size();
        if(left<1 || left>20) return 2;
        LineExtensions<23> ext;
        ext.fixed=rows;
        // Construct the forbidden triples once; subsequent layers reuse them.
        ext.run(0,23);
        Lines pool;
        for(int d=23;d>=8;--d){
            if(int(pool.size())<left){
                int upper=(left-static_cast<int>(pool.size()))*d;
                for(Mask r:pool) upper+=std::popcount(r);
                if(upper<need) break;
            }else if(std::popcount(pool.front())*(left-1)+d<need) break;
            ext.allowed.clear();
            ext.supports((1u<<23)-1,0,d);
            pool.insert(pool.end(),ext.allowed.begin(),ext.allowed.end());
        }
        ++cases;
        if(choose(rows,pool,left,need)){
            std::cout<<"solution "<<omit;
            for(Mask r:rows)std::cout<<' '<<r;
            std::cout<<'\n'; return 0;
        }
    }
    std::cout<<"excluded "<<cases<<'\n';
}
