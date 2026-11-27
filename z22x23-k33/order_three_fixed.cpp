// Compute the block sizes of the six moving rows and columns on a fixed order-three frame.
#include <sstream>
#include "order_three_blocks.hpp"
struct Word {
    array<unsigned char,6> d{};
    int weight=0, packed=0;
};
vector<Word> all_words(){
 vector<Word> ans;
 for(int code=0;code<729;++code){
  int x=code;Word w;
  for(int j=0;j<6;++j,x/=3){int v=x%3;w.d[j]=v;w.weight+=v;if(v)w.packed|=1<<j;if(v==2)w.packed|=256<<j;}
  ans.push_back(w);
 }
 return ans;
}
static vector<Word> words;
using Domain=vector<int>;
using Pools=array<Domain,6>;
Domain domain(const vector<unsigned>& corner,const vector<unsigned>& strips,unsigned u,
              const vector<int>& degrees,int fixed_count,bool row,unsigned low){
 Domain pool;vector<unsigned> fixed(fixed_count),incident(fixed_count);
 for(int i=0;i<fixed_count;++i){
  for(unsigned j=0;j<corner.size();++j)if(corner[j]>>i&1)fixed[i]|=1u<<j;
  for(int j=0;j<6;++j)if(strips[j]>>i&1)incident[i]|=1u<<j;
 }
 int fixed_weight=0;for(unsigned j=0;j<degrees.size();++j)if(u>>j&1)fixed_weight+=degrees[j];
 for(int wi=0;wi<729;++wi){
  const auto& w=words[wi];if(w.weight+pc(u)<9 || (row && w.weight+pc(u&~low)<8))continue;
  unsigned a=w.packed&255,b=w.packed>>8;
  if(fixed_weight+9*pc(b)>2*(pc(u)+pc(b)+(row?20:21)))continue;
  bool ok=true;
  for(int i=0;i<fixed_count&&ok;++i){
   if(pc(incident[i]&b)+pc(fixed[i]&u)>2)ok=false;
   for(int k=0;k<i&&ok;++k){unsigned joint=incident[i]&incident[k];
    if(pc(joint&a)+pc(joint&b)+pc(fixed[i]&fixed[k]&u)>2)ok=false;
   }
  }
  if(ok)pool.push_back(wi);
 }
 return pool;
}
bool propagate(Pools& r,Pools& c,int total){
 while(true){
  bool change=false;
  for(Pools* group:{&r,&c}){
   int lo[6],hi[6],floor=0,ceil=0;
   for(int i=0;i<6;++i){lo[i]=100;hi[i]=-1;
    for(int w:(*group)[i]){lo[i]=min(lo[i],words[w].weight);hi[i]=max(hi[i],words[w].weight);}
    if(hi[i]<0)return false;floor+=lo[i];ceil+=hi[i];
   }
   if(total<floor||total>ceil)return false;
   for(int i=0;i<6;++i){auto &d=(*group)[i];int n=d.size();erase_if(d,[&](int w){return words[w].weight+floor-lo[i]>total||words[w].weight+ceil-hi[i]<total;});change|=(n!=(int)d.size());}
  }
  for(int trans=0;trans<2;++trans){
   auto& a=trans?c:r;auto& b=trans?r:c;
   for(int i=0;i<6;++i){int allow[6]{};for(int j=0;j<6;++j)for(int w:b[j])allow[j]|=1<<words[w].d[i];
    int n=a[i].size();erase_if(a[i],[&](int w){for(int j=0;j<6;++j)if(!(allow[j]>>words[w].d[j]&1))return true;return false;});
    if(a[i].empty())return false;change|=(n!=(int)a[i].size());
   }
  }
  if(!change)return true;
 }
}
int main(){
 words=all_words();string line;long long cases=0, candidate_frames=0, weight_arrays=0, phase_nodes=0;
 while(getline(cin,line)){
  ++cases;istringstream src(line);vector<unsigned> C(5),U(6),V(6),R(4);vector<int> dr(4),dc(5);
  for(auto& x:C)src>>x;for(auto& x:U)src>>x;for(auto& x:V)src>>x;
  if(!src)return 2;
  int h=0,total=0;unsigned low=0;
  for(int j=0;j<5;++j){h+=pc(C[j]);dc[j]=pc(C[j]);for(auto u:U)dc[j]+=3*((u>>j)&1);if(dc[j]==8)low|=1<<j;}
  total=(217-h)/3;
  for(auto x:U)total-=pc(x);for(auto x:V)total-=pc(x);
  for(int i=0;i<4;++i){for(int j=0;j<5;++j)R[i]|=((C[j]>>i)&1)<<j;dr[i]=pc(R[i]);for(auto x:V)dr[i]+=3*((x>>i)&1);}
  Pools row,col;for(int i=0;i<6;++i){row[i]=domain(C,V,U[i],dc,4,true,low);col[i]=domain(R,U,V[i],dr,5,false,0);}
  if(!propagate(row,col,total))continue;
  array<int,6> order{0,1,2,3,4,5};stable_sort(order.begin(),order.end(),[&](int x,int y){return pair(row[x].size(),U[x])<pair(row[y].size(),U[y]);});
  ostringstream data;for(auto x:C)data<<x<<' ';for(int i:order)data<<U[i]<<' ';for(auto v:V)data<<v<<' ';data<<total<<' ';
  for(int i:order){data<<row[i].size()<<' ';for(int w:row[i])data<<words[w].packed<<' ';}
  for(auto& c:col){data<<c.size()<<' ';for(int w:c){int v=0;for(int i=5;i>=0;--i)v=3*v+words[w].d[order[i]];data<<v<<' ';}}
  istringstream stream(data.str());
  Quotient search;
  search.g=5;search.require_phases=true;
  search.load(stream);
  if(!stream)return 2;
  if(search.search(0,0,search.capacity)){
   cout<<"witness";for(auto row:search.fixed_full)cout<<' '<<row;
   for(auto orbit:search.placed)for(auto row:orbit)cout<<' '<<row;
   cout<<'\n';return 0;
  }
  candidate_frames+=(search.weight_arrays>0);
  weight_arrays+=search.weight_arrays;phase_nodes+=search.phase_nodes;
 }
 cout<<cases<<' '<<candidate_frames<<' '<<weight_arrays<<' '<<phase_nodes<<'\n';
}
