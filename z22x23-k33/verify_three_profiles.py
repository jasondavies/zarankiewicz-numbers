"""Find necessary degree profiles for a 193-one core with no maximizing ten-row."""
from collections import Counter
from itertools import combinations_with_replacement
from math import comb, prod
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'z23-k33'))
from verify_profiles import Counts, compositions, partitions


def profiles():
    row_caps = {9: 9, 10: 8, 11: 6, 12: 4, 13: 4}
    for r in partitions(13):
        if max(r) > 4:
            continue
        rows = Counter([9]*(20-len(r)) + [9+x for x in r])
        for c in partitions(17):
            squares = sum(x*x for x in c)
            if squares > 31:
                continue
            cols = Counter([8]*(22-len(c)) + [8+x for x in c])
            if sum(n*(18-d-row_caps[d]) for d,n in rows.items()) > 31-squares:
                continue
            needed = sorted(d-1 for d,n in cols.items() if d >= 11 for _ in range(n))
            if sum(needed) > 9*rows[9] or (needed and needed[-1] > rows[9]):
                continue
            if len(needed) >= 2 and sum(needed[-2:]) > rows[9]+5:
                continue
            yield rows, cols


def signatures(system, left, right, base, caps):
    groups = {}
    for d, n in left.items():
        choices = []
        for counts in compositions(d, tuple(right.values())):
            if sum(a*(v-base) for a,v in zip(counts,right)) <= caps[d]:
                choices.append((system.variable(n), counts))
        system.equal([(i,1) for i,_ in choices], n)
        groups[d] = choices
    return groups


def tuple_bounds(system, groups, opposite, pair_cap, weight_cap):
    for size in (2,3):
        for ix in combinations_with_replacement(range(len(opposite)),size):
            multiplicities = Counter(ix)
            def tuples(counts):
                return prod(comb(counts[j],k) for j,k in multiplicities.items())
            quota = tuples(tuple(opposite.values()))
            if not quota:
                continue
            terms = [(v,tuples(s)) for group in groups.values() for v,s in group]
            system.bound(terms,quota*(2 if size == 3 else pair_cap))
            if size == 2:
                weighted = [(v,(d-2)*tuples(s)) for d,group in groups.items() for v,s in group]
                system.bound(weighted,quota*weight_cap)


def feasible(rows, cols):
    system = Counts()
    row = signatures(system, rows, cols, 8, {9:9, 10:7, 11:6, 12:4, 13:4})
    col = signatures(system, cols, rows, 9, {8:10, 9:7, 10:4, 11:1, 12:1, 13:1})
    for i, d in enumerate(rows):
        for j, t in enumerate(cols):
            system.equal([(v,s[j]) for v,s in row[d]] + [(v,-s[i]) for v,s in col[t]], 0)
    tuple_bounds(system, row, cols, 5, 40)
    tuple_bounds(system, col, rows, 6, 36)
    return system.possible()


def main():
    cases = list(profiles())
    assert len(cases) == 302
    surviving = [(tuple(r.items()), tuple(c.items())) for r,c in cases if feasible(r,c)]
    assert surviving == [
        (((9,7),(10,13)), ((8,5),(9,17))),
        (((9,8),(10,11),(11,1)), ((8,6),(9,15),(10,1))),
        (((9,9),(10,9),(11,2)), ((8,6),(9,15),(10,1))),
        (((9,10),(10,7),(11,3)), ((8,7),(9,13),(10,2))),
    ]
    print('Certified 298 exclusions among 302 degree-profile pairs. Four survive.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    main()
