"""Exclude weight 226 by degree and incidence counts, after verify_226.py."""
from collections import Counter
from dataclasses import dataclass
from functools import cache
from itertools import combinations_with_replacement
from math import comb, prod
from ortools.sat.python import cp_model


def partitions(total, minimum=1):
    if total == 0:
        yield ()
    for x in range(minimum,total+1):
        for tail in partitions(total-x,x):
            yield (x,)+tail


@cache
def balanced(bins, total, order):
    assert bins > 0 and total >= 0
    q,r = divmod(total,bins)
    return (bins-r)*comb(q,order)+r*comb(q+1,order)


def margins(rows, cols, x):
    """x is the number of ones between the nine-rows and nine-columns."""
    a,b = 23-len(rows),23-len(cols)
    high_high = 226-9*(a+b)+x
    if high_high < 0:
        return False
    row_pairs = balanced(b,x,2)
    if row_pairs > comb(a,2):
        return False
    if 7*row_pairs+8*balanced(len(cols),9*a-x,2) > 42*comb(a,2):
        return False
    if balanced(b,x,3)+balanced(len(cols),9*a-x,3) > 2*comb(a,3):
        return False
    if balanced(b,9*b-x,3)+balanced(len(cols),high_high,3) > 2*comb(len(rows),3):
        return False
    # A long column of degree c requires at least c-5 nine-rows. The
    # total excess above ten on the high columns incident to nine-rows
    # is at most a+x, by the weight-ten bound.
    if sum((c-1)*(c+4) for c in cols if c>1) > a+x:
        return False
    needed = [r+4 for r in rows if r>1]
    if x+sum(needed)+2*rows.count(1) > 9*b:
        return False
    for k,cap in ((1,b),(2,b+6),(3,2*b+2)):
        if len(needed)>=k and sum(needed[-k:])>cap:
            return False
    n = len(needed)
    return (balanced(b,sum(needed),2)<=6*comb(n,2)
            and balanced(b,sum(needed),3)<=2*comb(n,3))


def initial_profiles():
    choices = [p for p in partitions(19) if 23-len(p)>=8]
    for i,rows in enumerate(choices):
        a = 23-len(rows)
        for cols in choices[i:]:
            b = 23-len(cols)
            for x in range(max(a,b,9*(a+b)-226),min(9*a,9*b)+1):
                if margins(rows,cols,x) and margins(cols,rows,x):
                    yield rows, cols
                    break


@dataclass(frozen=True)
class LineType:
    degree: int
    count: int
    marked: bool


def line_types(profile, marked):
    counts = Counter([9]*(23-len(profile)) + [9+x for x in profile])
    counts.subtract(marked)
    assert min(counts.values()) >= 0
    return tuple(LineType(d,n,flag) for group,flag in ((counts,False),(marked,True))
                 for d,n in sorted(group.items()) if n)


def compositions(total, limits):
    if not limits:
        if not total:
            yield ()
        return
    for k in range(min(total,limits[0])+1):
        for tail in compositions(total-k,limits[1:]):
            yield (k,)+tail


def needs_shared_six(d, high, weight):
    return d>=11 and high==5 and weight>=6


class Counts:
    """An integer bounded linear system. Each term is (variable index, coefficient)."""
    def __init__(self):
        self.upper = []
        self.inequalities = []

    def variable(self, maximum):
        self.upper.append(maximum)
        return len(self.upper)-1

    def bound(self, terms, rhs):
        self.inequalities.append((tuple((i,c) for i,c in terms if c),rhs))

    def equal(self, terms, rhs):
        self.bound(terms,rhs)
        self.bound([(i,-c) for i,c in terms],-rhs)

    def possible(self):
        model = cp_model.CpModel()
        vs = [model.new_int_var(0,u,'') for u in self.upper]
        for terms,rhs in self.inequalities:
            model.add(sum(c*vs[i] for i,c in terms)<=rhs)
        solver = cp_model.CpSolver()
        solver.parameters.num_workers = 1
        status = solver.solve(model)
        if status==cp_model.INFEASIBLE:
            from verify_linear import reject_integer_system
            reject_integer_system(self.upper,self.inequalities)
            return False
        assert status in (cp_model.FEASIBLE,cp_model.OPTIMAL)
        return True


def signatures(system, side, other, row_side, has_mark, forbid):
    tally = {}
    items = []
    limits = tuple(t.count for t in other)
    for i,line in enumerate(side):
        required = []
        options = []
        for s in compositions(line.degree,limits):
            low = sum(n for n,t in zip(s,other) if t.degree==9)
            high = line.degree-low
            weight = sum(n*(t.degree-9) for n,t in zip(s,other))
            if line.degree==9 and (low==0 or weight>10):
                continue
            if line.degree>=10 and high>=5 and weight>=9:
                continue
            if line.degree>=11 and high>=6:
                continue
            special = needs_shared_six(line.degree,high,weight)
            if forbid and special:
                continue
            if has_mark:
                on = sum(n for n,t in zip(s,other) if t.marked)
                if row_side and on!=(6 if line.marked else 2):
                    continue
                if not row_side:
                    if (line.marked and on!=2) or (not line.marked and on>1):
                        continue
                    if line.degree==9 and not line.marked and low>3:
                        continue
            v = system.variable(line.count)
            options.append((v,s))
            if special:
                required.append((v,-1))
        system.equal([(v,1) for v,s in options],line.count)
        if row_side and line.marked and line.degree==11:
            system.bound(required,-1)
        for j in range(len(other)):
            tally[i,j] = [(v,s[j]) for v,s in options if s[j]]
        items.extend((v,s,line.degree) for v,s in options)
    for order in (2,3):
        for indices in combinations_with_replacement(range(len(other)),order):
            mult = Counter(indices)
            ways = prod(comb(other[j].count,k) for j,k in mult.items())
            if not ways:
                continue
            counts = []
            for v,s,d in items:
                covered = prod(comb(s[j],k) for j,k in mult.items())
                if covered:
                    counts.append((v,covered,d))
            terms = [(v,c) for v,c,d in counts]
            if order==3:
                system.bound(terms,2*ways)
            else:
                nine = sum(other[j].degree==9 for j in indices)
                system.bound(terms,(5 if nine else 6)*ways)
                system.bound([(v,c*(d-2)) for v,c,d in counts],42*ways)
                if nine==2:
                    system.bound([(v,c) for v,c,d in counts if d==9],ways)
    return tally


def possible(a,b,pair=(),forbid_rows=False,forbid_cols=False):
    rows = line_types(a,Counter(pair))
    cols = line_types(b,{9:6} if pair else {})
    system = Counts()
    left = signatures(system,rows,cols,True,bool(pair),forbid_rows)
    right = signatures(system,cols,rows,False,bool(pair),forbid_cols)
    for i,j in left:
        system.equal(left[i,j]+[(v,-c) for v,c in right[j,i]],0)
    return system.possible()


def main():
    initial = list(initial_profiles())
    assert len(initial)==358
    possible_profiles = [(a,b) for a,b in initial if possible(a,b)]
    assert len(possible_profiles)==30
    print('358 degree-profile pairs reduced to 30.',flush=True)
    shared = []
    tests = 0
    for a,b in possible_profiles:
        assert not possible(a,b,forbid_rows=True,forbid_cols=True)
        for rows,cols in sorted({(a,b),(b,a)}):
            degrees = [9+r for r in rows]
            for d in sorted(set(degrees)):
                if 11 not in degrees or (d==11 and degrees.count(11)<2):
                    continue
                pair = tuple(sorted((11,d)))
                tests += 1
                if possible(rows,cols,pair):
                    shared.append((rows,cols,pair))
    assert tests==142 and len(shared)==1
    rows,cols,pair = shared[0]
    assert rows==(1,)*4+(2,)*6+(3,) and cols==(1,)*5+(2,)*4+(3,)*2 and pair==(11,12)
    assert rows!=cols and not possible(rows,cols,pair,forbid_cols=True)
    print('142 oriented shared-six cases reduced to one. Transposition excludes it.',flush=True)


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('enable assertions for verification')
    main()
