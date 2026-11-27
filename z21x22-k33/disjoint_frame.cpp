#include "../z18x19-k33/seven_columns.hpp"
#include <algorithm>
#include <array>
int main(){
    unsigned long long exact=0, families=0, lows=0, frames=0;
    std::string s;while(std::getline(std::cin,s)){
        std::istringstream in(s);Lines rows;for(Mask r;in>>r;)rows.push_back(r);if(rows.size()!=20)return 2;
        Lines cols(8);for(int i=0;i<20;++i)for(Mask m=rows[i];m;m &= m-1)cols[std::countr_zero(m)]|=1u<<i;
        Mask hi=0;bool ok=true;
        for(int j=0;j<8;++j){int k=std::popcount(cols[j]);if(k==9)hi|=1u<<j;else if(k!=8)ok=false;}
        if(!ok||std::popcount(hi)!=5)continue;
        ++exact;Mask lo=255^hi;
        Mask choices=0;
        for(int i=0;i<20;++i)if(std::popcount(rows[i]&lo)==2)choices|=1u<<i;
        if(std::popcount(choices)<5)continue;
        bool keep=false;
        for(int a=0;a<20;++a)for(int b=0;b<a;++b)for(int c=0;c<b;++c){
            Mask u=rows[a]&hi,v=rows[b]&hi,w=rows[c]&hi;
            if(((u&v)|(v&w)|(u&w))!=hi || (u&v&w))continue;
            Mask three=(1u<<a)|(1u<<b)|(1u<<c);++lows;
            Mask avail=choices&~three;
            if(std::popcount(avail)<5)continue;
            std::array<Mask,3> buckets{};int idx=0;
            for(Mask t=lo;t;t&=t-1){int j=std::countr_zero(t);buckets[idx++]=avail&~cols[j];}
            // Three pairs of low columns occur among the five ten-rows with multiplicities 2,2,1.
            for(int single=0;single<3;++single){
                Mask g=buckets[single],h=buckets[(single+1)%3],k=buckets[(single+2)%3];
                for(Mask r=g;r;r&=r-1)for(Mask i=h;i;i&=i-1)for(Mask j=i&(i-1);j;j&=j-1)
                    for(Mask m=k;m;m&=m-1)for(Mask n=m&(m-1);n;n&=n-1){
                    Mask ten=(r&-r)|(i&-i)|(j&-j)|(m&-m)|(n&-n);
                    Mask cc=three|ten;bool good=true;
                    for(int x=0;x<8 && good;++x)for(int y=0;y<x;++y)if(std::popcount(cc&cols[x]&cols[y])>2){good=false;break;}
                    if(good){keep=true;++frames;std::cout<<cc<<' '<<ten;for(Mask b:rows)std::cout<<' '<<b;std::cout<<'\n';}
                }
            }
        }
        families+=keep;
    }
    std::cerr<<"exact "<<exact<<" triples "<<lows<<" families "<<families<<" frames "<<frames<<"\n";
}
