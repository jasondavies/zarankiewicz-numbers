#include "../z18x19-k33/seven_columns.hpp"
#include <algorithm>
#include <array>
struct Mark{
   Lines b;Mask hi,lo;
   std::array<Mask,20> compatible{},clique{};
   unsigned long long lifts=0,pairs=0;bool hit=false;
   std::vector<Mask> choices;
   void five(Mask avail,Mask taken,int left){
       if(!left){choices.push_back(taken);return;}
       while(std::popcount(avail)>=left){
           Mask bit=avail&-avail;avail^=bit;
           five(avail&clique[std::countr_zero(bit)],taken|bit,left-1);
       }
   }
   void test(Mask y){
       ++lifts;
       std::array<Mask,20> a;
       for(int i=0;i<20;++i){
          a[i]=b[i]|(((y>>i)&1)<<6);
          clique[i]=0;
       }
       for(int i=0;i<20;++i)for(int j=i+1;j<20;++j)if(std::popcount(a[i]&a[j])<=1)clique[i]|=1u<<j;
       Mask bothlow=64|lo;
       for(int i=0;i<20;++i)for(int j=0;j<i;++j){
           Mask group=a[i]|a[j];
           if((a[i]&a[j]) || (group&hi)!=hi || std::popcount(a[i])>3 || std::popcount(a[j])>3)continue;
           Mask avail=0, shared_ok=0;
           for(int t=0;t<20;++t)if(t!=i && t!=j && (a[t]&bothlow) && std::popcount(a[t]&a[i])<=1 && std::popcount(a[t]&a[j])<=1){
               avail|=1u<<t;if(!(a[t]&group))shared_ok|=1u<<t;
           }
           if(std::popcount(avail)+std::popcount(shared_ok)<10)continue;
           choices.clear();five(avail,0,5);
           for(size_t h=0;h<choices.size();++h)for(size_t k=0;k<h;++k){
               Mask common=choices[h]&choices[k];if(common&~shared_ok)continue;
               Mask seen=group;bool okay=true;
               for(Mask t=common;t;t&=t-1){auto m=a[std::countr_zero(t)];if(seen&m){okay=false;break;}seen|=m;}
               if(okay){
                   ++pairs;hit=true;Mask ab=(1u<<i)|(1u<<j);
                   std::cout<<ab<<' '<<(choices[h]|ab)<<' '<<(choices[k]|ab);
                   for(Mask v:a)std::cout<<' '<<v;std::cout<<'\n';
               }
           }
       }
   }
   void eight(Mask pool,Mask used,int left){
       
       if(!left){test(used);return;}
       while(std::popcount(pool)>=left){
           Mask bit=pool&-pool;pool^=bit;
           eight(pool&compatible[std::countr_zero(bit)],used|bit,left-1);
       }
   }
   bool run(){
       std::array<int,6> degrees{};for(auto x:b)for(;x;x&=x-1)++degrees[std::countr_zero(x)];
       hi=lo=0;for(int j=0;j<6;++j){if(degrees[j]==9)hi|=1u<<j;else if(degrees[j]==8)lo|=1u<<j;else return false;}
       if(std::popcount(hi)!=5)return false;
       Mask pool=0;
       for(int i=0;i<20;++i){
          compatible[i]=0;if(std::popcount(b[i])<5)pool|=1u<<i;
          for(int j=i+1;j<20;++j)if(std::popcount(b[i]&b[j])<=1)compatible[i]|=1u<<j;
       }
       hit=false;eight(pool,0,8);return hit;
   }
};
int main(){
   Mark m;std::string s;int n=0,k=0;
   while(std::getline(std::cin,s)){
      std::istringstream in(s);m.b.clear();for(Mask x;in>>x;)m.b.push_back(x);
      if(m.b.size()!=20)return 2;++n;
      if(m.run()){++k;}
   }
   std::cerr<<n<<" six-point marks, "<<m.lifts<<" lifts tested, "<<k<<" survive\n";
}
