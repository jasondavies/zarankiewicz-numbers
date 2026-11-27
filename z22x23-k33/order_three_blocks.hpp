#pragma once
#include <algorithm>
#include <cstdlib>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
int pc(unsigned x){return popcount(x);}
struct Option {
 unsigned occupied,double_blocks,row_hits; int weight,id;
 array<unsigned char,7> digits{};
 array<unsigned char,300> capacity{};
};
struct Quotient{
 int g,b,total,constraints=0;unsigned corner[5]{},row_hits[6]{},col_hits[7]{};
 vector<Option> rows[6]; int trie[7][7][730]{}, min_column[7][7][730]{},max_column[7][7][730]{}; unsigned low_columns=0;
 array<unsigned char,300> capacity{}; array<array<int,3>,300> triples{};
 array<int,7> low{},high{}; array<int,7> code{}; array<Option*,6> chosen{};

 int p3[7]={1,3,9,27,81,243,729};
 unsigned fixed_entries[4]{},fixed_strips[4]{};
 std::vector<unsigned char> pair_cache;int option_count=0;
 int rot(int x,int t){return ((x<<t)|(x>>(3-t)))&7;}
 // Pack the 21 intersection budgets for two moving row orbits.
 struct Score {
  uint64_t part[2]{};
  void set(int position,unsigned value){part[position/16]|=uint64_t(value)<<(4*(position%16));}
 };
 struct Phase { Score trace[3]; };
 // Each four-bit lane is at most six before adding one block, and at most eight after.
 // Subtracting from cap+8 cannot borrow. The high bit stays set exactly at allowed lanes.
 bool fits(const Phase* p,int count,Score score,Score cap,int nchoices){
  if(!count)return true;
  constexpr uint64_t high_bits=0x8888888888888888ULL;
  for(int k=0;k<nchoices;++k){
   Score next{{score.part[0]+p->trace[k].part[0],score.part[1]+p->trace[k].part[1]}};
   if(((cap.part[0]-next.part[0]) & (cap.part[1]-next.part[1]) & high_bits)!=high_bits)continue;
   if(fits(p+1,count-1,next,cap,3))return true;
  }
  return false;
 }
 // Normalize the first orbit independently on every column orbit.
 // The second orbit then has three possible relative shifts on each shared block.
 bool compatible_phases(const Option& x,const Option& y){
  unsigned both=x.row_hits&y.row_hits;int fixed=pc(both);
  unsigned char cap[32]{};Phase parts[7];
  for(int t=0;t<3;++t){
   cap[t]=(pc(both&low_columns)==2?6:5)-fixed;
   cap[3+t]=cap[6+t]=2-fixed;
   for(int r=0;r<4;++r)cap[9+3*r+t]=2-pc(fixed_entries[r]&both);
  }
  int n=0;
  for(int j=0;j<b;++j){
   int a=x.digits[j],bval=y.digits[j];
   if(!a||!bval)continue;
   int left=a==1?1:6,right=bval==1?1:6;
   for(int d=0;d<3;++d){
    unsigned char add[32]{};
    int v=rot(right,d);
    for(int t=0;t<3;++t){
     add[t]=pc(left&rot(v,t));
     add[3+t]=pc(left&rot(left,1)&rot(v,t));
     add[6+t]=pc(v&rot(v,1)&rot(left,t));
     for(unsigned s=col_hits[j];s;s&=s-1)add[9+3*countr_zero(s)+t]=add[t];
    }
    for(int h=0;h<21;++h)parts[n].trace[d].set(h,add[h]);
   }
   ++n;
  }
  Score bound;for(int h=0;h<32;++h)bound.set(h,8+cap[h]);
  return fits(parts,n,Score{},bound,1);
 }

 void load(std::istream& source){
  if(g!=2 && g!=5)std::abort();
  b=(g==2?7:6);
  for(int j=0;j<g;++j)source>>corner[j];for(auto& u:row_hits)source>>u;for(int j=0;j<b;++j)source>>col_hits[j];source>>total;
  for(int r=0;r<4;++r){for(int j=0;j<g;++j)fixed_entries[r]|=((corner[j]>>r)&1)<<j;for(int j=0;j<b;++j)fixed_strips[r]|=((col_hits[j]>>r)&1)<<j;}
  int n=g+b;
  for(int j=0;j<g;++j){int load=pc(corner[j]);for(unsigned u:row_hits)load+=3*((u>>j)&1);if(load==8)low_columns|=1u<<j;}
  // Each column triple can occupy two rows. Capacities here are multiplied by nine.
  for(int x=0;x<n;++x)for(int y=x;y<n;++y)for(int z=y;z<n;++z){
   if((x==y&&x<g)||(y==z&&y<g))continue;
   auto f=[&](int j){return j<g?corner[j]:col_hits[j-g];};
   capacity[constraints]=18-9*pc(f(x)&f(y)&f(z));
   triples[constraints++]=array<int,3>{x,y,z};
  }
  for(int i=0;i<6;++i){
   int n;source>>n;
   while(n--){
    int word;source>>word;Option op{};op.occupied=word&255;op.double_blocks=word>>8;op.row_hits=row_hits[i];op.weight=pc(op.occupied)+pc(op.double_blocks);
    for(int j=0;j<7;++j)op.digits[j]=((op.occupied>>j)&1)+((op.double_blocks>>j)&1);
    for(int h=0;h<constraints;++h){
     // Three moving rows times nine, averaged over distinct representatives
     // of the specified column groups (sampling without replacement).
     int k=0,val=27;
     while(k<3){
      int j=triples[h][k],e=k+1;
      while(e<3&&triples[h][e]==j)++e;
      int mult=e-k;
      if(j<g)val*=((op.row_hits>>j)&1);
      else{
       int s=op.digits[j-g];
       if(mult==3)val=0;
       else val=val*(mult==2?int(s==2):s)/3;
      }
      k=e;
     }
     op.capacity[h]=val;
    }
    int h=constraints;
    for(int j=0;j<b;++j)for(int k=0;k<=j;++k){
     op.capacity[h++]=(j==k?int(op.digits[j]==2):op.digits[j]*op.digits[k]);
    }
    op.id=option_count++;rows[i].push_back(op);
   }
  }
  for(int j=0;j<b;++j)for(int k=0;k<=j;++k){
   capacity[constraints++]=(j==k?1:3)*(6-pc(col_hits[j]&col_hits[k]));
  }
  pair_cache.resize(option_count*option_count);
  for(int i=5;i>=0;--i){
   int lo=100,hi=0;for(const auto& r:rows[i]){lo=min(lo,r.weight);hi=max(hi,r.weight);}
   low[i]=low[i+1]+lo;high[i]=high[i+1]+hi;
  }
  // Record which ternary column prefixes can still reach a legal column word.
  for(int j=0;j<b;++j){
   int n;source>>n;while(n--){int v;source>>v;
    int sum=0;for(int x=v;x;x/=3)sum+=x%3;
    for(int d=1;d<=6;++d){
     int k=v%p3[d];
     if(!trie[j][d][k])min_column[j][d][k]=sum;
     trie[j][d][k]=1;
     min_column[j][d][k]=min(min_column[j][d][k],sum);max_column[j][d][k]=max(max_column[j][d][k],sum);
    }
   }
  }
 }
 // Check every older row orbit with the candidate, and average triple
 // intersections across each choice of three distinct moving row orbits.
 bool compatible(const Option& w,int at){
  for(int i=0;i<at;++i){
   const auto& x=*chosen[i];auto both=w.row_hits&x.row_hits;int pair=pc(both);
   if(3*pair+pc(w.double_blocks&x.occupied)+pc(w.double_blocks&x.double_blocks)>6 || 3*pair+pc(x.double_blocks&w.occupied)+pc(x.double_blocks&w.double_blocks)>6)return false;
   auto dot=[&](unsigned mask){return pc(w.occupied&x.occupied&mask)+pc(w.occupied&x.double_blocks&mask)+pc(w.double_blocks&x.occupied&mask)+pc(w.double_blocks&x.double_blocks&mask);};
   int overlap=dot(255);
   if(overlap+3*pc(both&~low_columns)>15 || (pc(both&low_columns)<2 && overlap+3*pair>15))return false;
   for(int r=0;r<4;++r){
    if(3*pc(both&fixed_entries[r])+dot(fixed_strips[r])>6)return false;
   }
   auto& value=pair_cache[x.id*option_count+w.id];
   if(!value)value=compatible_phases(x,w)?1:2;
   if(value==2)return false;
   for(int k=0;k<i;++k){
    const auto& y=*chosen[k];
    if(9*pc(both&y.row_hits)+dot(y.occupied)+dot(y.double_blocks)>18)return false;
   }
  }
  return true;
 }
 bool require_phases=false;
 // The six moving row orbits are placed one at a time. The occupied positions
 // of a size-one block are one cyclic bit; those of a size-two block are its complement.
 using Orbit = array<unsigned,3>;
 array<Orbit,6> placed{};
 unsigned fixed_full[4]{};
 long long weight_arrays=0, phase_nodes=0;
 bool phase_search(int at,unsigned old_columns,vector<unsigned>& known){
  if(at==6)return true;
  ++phase_nodes;
  const Option& x=*chosen[at];
  unsigned shared=x.occupied&old_columns;
  unsigned varying=shared&(shared-1); // Fix one phase by rotating this new row orbit.
  int variants=1;for(unsigned s=varying;s;s&=s-1)variants*=3;
  for(int code=0;code<variants;++code){
   int val=code;Orbit next{x.row_hits,x.row_hits,x.row_hits};
   for(int j=0;j<b;++j){
    if(!x.digits[j])continue;
    int shift=0;if(varying>>j&1){shift=val%3;val/=3;}
    int base=rot(x.digits[j]==1?1:6,shift);
    for(int k=0;k<3;++k)next[k]|=unsigned(rot(base,k))<<(g+3*j);
   }
   // The placed rows are closed under the order-three action. Only one
   // representative of each triple involving the new row orbit is required.
   bool good=true;
   for(unsigned a:known){
    if(pc(a&next[0]&next[1])>2){good=false;break;}
   }
   if(!good)continue;
   for(size_t i=0;i<known.size()&&good;++i)
    for(size_t j=0;j<i;++j)if(pc(known[i]&known[j]&next[0])>2){good=false;break;}
   if(!good || pc(next[0]&next[1]&next[2])>2)continue;
   placed[at]=next;known.insert(known.end(),next.begin(),next.end());
   if(phase_search(at+1,old_columns|x.occupied,known))return true;
   known.resize(known.size()-3);
  }
  return false;
 }
 bool phase_lift(){
  ++weight_arrays;
  vector<unsigned> known;
  for(int i=0;i<4;++i){
   unsigned v=fixed_entries[i];for(int j=0;j<b;++j)if(col_hits[j]>>i&1)v|=7u<<(g+3*j);
   fixed_full[i]=v;known.push_back(v);
  }
  return phase_search(0,0,known);
 }

 bool search(int i,int weight,const array<unsigned char,300>& cap){
  if(i==6)return weight==total && (!require_phases || phase_lift());

  for(auto& w:rows[i]){

   bool canonical=true;
   for(int k=0;k<i;++k)if(row_hits[i]==row_hits[k] && w.digits<chosen[k]->digits){canonical=false;break;}
   if(!canonical)continue;
   int t=weight+w.weight;
   if(t+low[i+1]>total||t+high[i+1]<total)continue;
   bool ok=true;int clo=0,chi=0;array<int,7> next{};
   for(int j=0;j<b&&ok;++j){
    next[j]=code[j]+w.digits[j]*p3[i];
    if(!trie[j][i+1][next[j]])ok=false;
    clo+=min_column[j][i+1][next[j]];chi+=max_column[j][i+1][next[j]];
    for(int k=0;k<j&&ok;++k)if(col_hits[k]==col_hits[j]&&code[k]==code[j]&&w.digits[k]>w.digits[j])ok=false;
   }
   if(!ok || clo>total || chi<total || !compatible(w,i))continue;
   array<unsigned char,300> room{};
   for(int h=0;h<constraints;++h){
    if(cap[h]<w.capacity[h]){ok=false;break;}
    room[h]=cap[h]-w.capacity[h];
   }
   if(!ok)continue;
   auto prev=code;code=next;chosen[i]=&w;
   if(search(i+1,t,room))return true;
   code=prev;
  }
  return false;
 }
};
