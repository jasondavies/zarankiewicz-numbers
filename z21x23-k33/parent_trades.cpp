// Exhaust small parallel-line replacements in an extremal parent, with the other part labelled.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Mask = std::uint32_t;
using Lines = std::vector<Mask>;
int degree(Mask m) { return std::popcount(m); }

Lines transpose(const Lines& lines, int width) {
    Lines other(width);
    for (size_t i = 0; i < lines.size(); ++i)
        for (Mask bits = lines[i]; bits; bits &= bits - 1)
            other[std::countr_zero(bits)] |= Mask(1) << i;
    return other;
}

class Supports {
    std::array<std::array<Mask,21>,21> forbidden{};
    void visit(Mask rest, Mask chosen, int left, Lines& out) const {
        if (!left) {
            out.push_back(chosen);
            return;
        }
        while (degree(rest) >= left) {
            Mask bit = rest & -rest;
            rest ^= bit;
            Mask next = rest;
            for (Mask used = chosen; used; used &= used - 1)
                next &= ~forbidden[std::countr_zero(used)][std::countr_zero(bit)];
            visit(next, chosen | bit, left-1, out);
        }
    }
public:
    explicit Supports(const Lines& lines) {
        for (size_t i = 0; i < lines.size(); ++i) for (size_t j = 0; j < i; ++j) {
            Mask common = lines[i] & lines[j];
            for (Mask a = common; a; a &= a-1) {
                Mask b = a & (a-1);
                for (; b; b &= b-1)
                    forbidden[std::countr_zero(a)][std::countr_zero(b)] |= b & (b-1);
            }
        }
    }
    Lines get(int width, int weight) const {
        Lines out;
        visit((Mask(1)<<width)-1, 0, weight, out);
        return out;
    }
};

class Search {
    const Lines base;
    const bool rows;
    const int width, minimum;
    unsigned long long subsets=0, solutions=0;

    void fill(Lines& fixed, const Lines& pool, int left, int weight) {
        if (!left) {
            if (weight) return;
            ++solutions;
            std::cout << "case";
            for (Mask m : (rows ? transpose(fixed,width) : fixed)) std::cout << ' ' << m;
            std::cout << '\n';
            return;
        }
        for (size_t i=0; i<pool.size(); ++i) {
            Mask a=pool[i];
            int d=degree(a);
            if (left*d < weight) break;
            if (d+(left-1)*minimum > weight) continue;
            Lines next;
            if (left>1) {
                for (size_t j=i; j<pool.size(); ++j) {
                    Mask common=a&pool[j];
                    if (std::none_of(fixed.begin(),fixed.end(),[=](Mask c){return degree(common&c)>2;}))
                        next.push_back(pool[j]);
                }
            }
            fixed.push_back(a);
            fill(fixed,next,left-1,weight-d);
            fixed.pop_back();
        }
    }

    void erase(int start, int left, Mask dropped) {
        if (left) {
            for (int i=start; i+left<=int(base.size()); ++i)
                erase(i+1,left-1,dropped|(Mask(1)<<i));
            return;
        }
        ++subsets;
        Lines fixed, removed;
        int required=0;
        for (size_t i=0; i<base.size(); ++i) {
            if (dropped&(Mask(1)<<i)) {
                removed.push_back(base[i]);
                required+=degree(base[i]);
            } else fixed.push_back(base[i]);
        }
        Supports legal(fixed);
        int count=int(removed.size());
        Lines pool;
        for (int d=std::min(width,required-(count-1)*minimum); d>=minimum; --d) {
            for (Mask m : legal.get(width,d)) {
                // A restored support can be matched to an original line. That case
                // occurs at a smaller deletion count, including when masks repeat.
                if (std::find(removed.begin(),removed.end(),m)==removed.end()) pool.push_back(m);
            }
        }
        fill(fixed,pool,count,required);
    }

public:
    Search(const Lines& cols,bool use_rows)
        : base(use_rows ? transpose(cols,21) : cols), rows(use_rows),
          width(use_rows ? 19 : 21), minimum(use_rows ? 6 : 7) {}
    void run() {
        for (int k=1; k<=6; ++k) {
            subsets=solutions=0;
            erase(0,k,0);
            std::cout<<"level "<<k<<' '<<subsets<<' '<<solutions<<'\n';
        }
    }
};

int main(int argc,char** argv) {
    if (argc!=2 || (std::string(argv[1])!="rows" && std::string(argv[1])!="columns")) return 2;
    Lines cols;
    for (Mask m; std::cin>>m;) {
        if (m>>21) return 2;
        cols.push_back(m);
    }
    if (cols.size()!=19) return 2;
    Search(cols,std::string(argv[1])=="rows").run();
}
