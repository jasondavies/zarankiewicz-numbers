"""Certify infeasibility using integer bounds, verified linear combinations and splits.

Floating-point linear programming only proposes multipliers or a branching variable.
All exclusions are checked in Python integer arithmetic.
"""
from math import floor


def propagate(constraints, lo, hi):
    changed = True
    while changed:
        changed = False
        for terms,rhs in constraints:
            gap = rhs-sum(c*(lo[i] if c>0 else hi[i]) for i,c in terms)
            if gap<0:
                return False
            for i,c in terms:
                width = gap//abs(c)
                if hi[i]-lo[i]>width:
                    if c>0:
                        hi[i] = lo[i]+width
                    else:
                        lo[i] = hi[i]-width
                    changed = True
    return True


def certify(weights, constraints, lo, hi):
    for scale in (10**5,10**8,10**12):
        acc = [0]*len(lo)
        rhs = 0
        for y,(terms,b) in zip(weights,constraints,strict=True):
            k = max(0,round(y*scale))
            if k:
                rhs += k*b
                for i,c in terms:
                    acc[i] += k*c
        if sum(c*(lo[i] if c>0 else hi[i]) for i,c in enumerate(acc)) > rhs:
            return True
    return False


def reject_integer_system(upper, constraints):
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix, vstack
    import numpy as np

    def prove(lo,hi):
        if not propagate(constraints,lo,hi):
            return
        active = [i for i in range(len(lo)) if lo[i]!=hi[i]]
        assert active, 'integral assignment passed every inequality'
        index = {i:j for j,i in enumerate(active)}
        fixed = set(range(len(lo)))-set(active)
        reduced = []
        for terms,b in constraints:
            rhs = b-sum(c*lo[i] for i,c in terms if i in fixed)
            var = tuple((index[i],c) for i,c in terms if i in index)
            if sum(c*(hi[active[j]] if c>0 else lo[active[j]]) for j,c in var)>rhs:
                reduced.append((var,rhs))
        low = [lo[i] for i in active]
        high = [hi[i] for i in active]
        augmented = reduced + [(((j,1),),u) for j,u in enumerate(high)] + [
            (((j,-1),),-l) for j,l in enumerate(low) if l]
        rr,cc,coeff = [],[],[]
        for k,(terms,b) in enumerate(augmented):
            for j,c in terms:
                rr.append(k)
                cc.append(j)
                coeff.append(c)
        mat = coo_matrix((coeff,(rr,cc)),shape=(len(augmented),len(active))).tocsr()
        rhs = np.array([b for _,b in augmented],dtype=float)
        lp = linprog(np.zeros(len(active)),A_ub=mat,b_ub=rhs,bounds=(0,None),method='highs')
        if lp.status==2:
            dual = linprog(np.ones(len(augmented)),A_ub=vstack((-mat.T,rhs.reshape(1,-1))),
                           b_ub=[0]*len(active)+[-1],bounds=(0,None),method='highs')
            if dual.success and certify(dual.x,augmented,low,high):
                return
        # Either half can be excluded separately. The split covers every integer.
        if lp.success:
            j = max(range(len(active)),key=lambda k:abs(lp.x[k]-round(lp.x[k])))
            value = floor(lp.x[j])
        else:
            j = max(range(len(active)),key=lambda k:high[k]-low[k])
            value = (high[j]+low[j])//2
        i = active[j]
        value = max(lo[i],min(hi[i]-1,value))
        left_hi, right_lo = hi.copy(), lo.copy()
        left_hi[i] = value
        right_lo[i] = value+1
        prove(lo.copy(),left_hi)
        prove(right_lo,hi.copy())

    prove([0]*len(upper),list(upper))
