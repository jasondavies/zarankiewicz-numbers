"""Exhaust order-three automorphisms with four fixed rows and five fixed columns at 217."""
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from functools import cache
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

from odd_symmetry import triple_count
from verify_order_three import HERE, compile_cpp, planted

# Upper bounds used on minors, indexed by the smaller dimension first.
BOUNDS = {(17,17):138, (17,18):143, (18,18):150, (18,19):156, (18,20):163,
          (18,21):170, (19,19):164, (19,20):171, (19,21):177, (20,20):180,
          (20,21):185, (21,21):193, (21,22):201, (21,23):209, (22,22):210,
          (22,23):217}


@cache
def upper(m, n):
    if min(m, n) == 0:
        return 0
    value = BOUNDS.get(tuple(sorted((m, n))), m*n)
    if m > 1:
        value = min(value, m * upper(m-1, n) // (m-1))
    if n > 1:
        value = min(value, n * upper(m, n-1) // (n-1))
    while triple_count(value,m) > 2*comb(n,3) or triple_count(value,n) > 2*comb(m,3):
        value -= 1
    return value


@cache
def actions(size):
    return [(perm, bytes(sum(((m >> i) & 1) << j for i,j in enumerate(perm))
                         for m in range(1 << size))) for perm in permutations(range(size))]


def corners():
    for cols in combinations_with_replacement(range(16), 5):
        if sum(map(int.bit_count, cols)) % 3 != 1:
            continue
        if any((a & b & c).bit_count() > 2 for a,b,c in combinations(cols, 3)):
            continue
        if all(cols <= tuple(sorted(t[c] for c in cols)) for _,t in actions(4)):
            yield cols


@cache
def incidence(degrees, columns):
    options = []
    for hits in product(*(range((8-d+2)//3, 7) for d in degrees)):
        if sum(hits) > 12:
            continue
        full = tuple(d+3*k for d,k in zip(degrees, hits))
        if columns and not 1 <= full.count(8) <= 2:
            continue
        if not columns and full.count(8) > 2:
            continue
        options.append((hits, full))
    return options


@cache
def strips(hits):
    """Six orbit neighbourhoods, with a distinct pair on every size-two strip."""
    edges = [(1 << i) | (1 << j) for i,j in combinations(range(len(hits)), 2)]
    answer = []
    for n in range(max(0, sum(hits)-6), min(6,len(edges))+1):
        for chosen in combinations(edges, n):
            remaining = [d - sum((e >> i) & 1 for e in chosen) for i,d in enumerate(hits)]
            if min(remaining) < 0:
                continue
            singles = [1 << i for i,d in enumerate(remaining) for _ in range(d)]
            answer.append(tuple(sorted((*chosen, *singles, *([0]*(6-n-len(singles)))))))
    return answer


def subset_sums(weights):
    return [sum(d for i,d in enumerate(weights) if mask >> i & 1)
            for mask in range(1 << len(weights))]


@cache
def stabilizer(corner):
    return [(r,c) for _,r in actions(4) for perm,c in actions(5)
            if all(r[x] == corner[perm[j]] for j,x in enumerate(corner))]


@cache
def normalize_column_strips(corner, v):
    options = [(tuple(sorted(r[x] for x in v)), c) for r,c in stabilizer(corner)]
    least = min(vv for vv,_ in options)
    return least, tuple({c for vv,c in options if vv == least})


def frames():
    seen = set()
    for corner in corners():
        rows = tuple(sum(((x >> i) & 1) << j for j,x in enumerate(corner)) for i in range(4))
        weight = sum(map(int.bit_count,corner))
        minors = [[upper(22-p.bit_count(),23-q.bit_count()) for q in range(32)] for p in range(16)]
        for col_hits, dc in incidence(tuple(map(int.bit_count,corner)), True):
            low = sum((d == 8) << j for j,d in enumerate(dc))
            # Minimum total weight of rows deleted by p for all column subsets q.
            requirements = []
            for p in range(16):
                deleted = subset_sums([d - (c & p).bit_count() for c,d in zip(corner,dc)])
                requirements.append(max(217 - minors[p][q] - deleted[q] for q in range(32)))
            bad_u = {(1 << i) | (1 << j) for i,j in combinations(range(5),2)
                     if 3+(corner[i]&corner[j]).bit_count() > (5 if dc[i]==dc[j]==8 else 6)}
            bad_v = set()
            for i,j in combinations(range(4),2):
                shared = rows[i] & rows[j]
                score = sum(d for k,d in enumerate(dc) if shared >> k & 1)
                if 27 + score > 40 + 2*(3+shared.bit_count()):
                    bad_v.add((1 << i) | (1 << j))
            for row_hits, dr in incidence(tuple(map(int.bit_count,rows)), False):
                target = (217-weight)//3 - sum(row_hits) - sum(col_hits)
                if 3*target > upper(18,18) or target+min(sum(row_hits),sum(col_hits)) < 54:
                    continue
                if any(d-(r&low).bit_count() < 8 for d,r in zip(dr,rows)):
                    continue
                if any(d < k for d,k in zip(subset_sums(dr), requirements)):
                    continue
                for v in strips(row_hits):
                    if not bad_v.isdisjoint(v):
                        continue
                    vv, transforms = normalize_column_strips(corner,v)
                    for u in strips(col_hits):
                        if not bad_u.isdisjoint(u):
                            continue
                        uu = min(tuple(sorted(c[x] for x in u)) for c in transforms)
                        seen.add(corner+uu+vv)
    return sorted(seen)


def main(jobs):
    with TemporaryDirectory(prefix='z217-five-fixed-') as tmp:
        blocks = compile_cpp(HERE/'order_three_blocks.cpp',Path(tmp))
        output = run([blocks,'--lift'],input=planted(),capture_output=True,check=True).stdout.split()
        matrix = list(map(int,output[1:]))
        if (output[0] != b'possible' or len(matrix) != 22 or max(matrix) >= 1<<23
                or sum(map(int.bit_count,matrix)) != 216
                or any((a&b&c).bit_count()>2 for a,b,c in combinations(matrix,3))):
            raise RuntimeError('failed to reconstruct a valid 216-one control')
        solver = compile_cpp(HERE/'order_three_fixed.cpp',Path(tmp))
        cases = frames()
        if len(cases) != 222504:
            raise RuntimeError(f'unexpected number of frames {len(cases)}')
        def solve(batch):
            data = ''.join(' '.join(map(str,case))+'\n' for case in batch).encode()
            output = run([solver],input=data,capture_output=True,check=True).stdout
            if output.startswith(b'witness'):
                raise RuntimeError(output)
            return tuple(map(int,output.split()))
        with ThreadPoolExecutor(jobs) as pool:
            totals = tuple(map(sum,zip(*pool.map(solve, (cases[i::jobs] for i in range(jobs))))))
        if totals != (222504,48,515,119025):
            raise RuntimeError(totals)
        print('Verified 216 control. At 217: frames, surviving frames, weight arrays, phase nodes:',*totals)
        print('No lift.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=1)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error('jobs must be positive')
    main(args.jobs)
