"""Check the order-three case with four fixed rows and two fixed columns at 217."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from functools import cache
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'z16x18-k33'))
from replay import compile_cpp
sys.path.insert(0, str(ROOT / 'z23-k33'))
from construct import symmetries, construct


@cache
def words(n):
    return np.array(list(product(range(3), repeat=n)), dtype=np.int8)


@cache
def domain(fixed_columns, moving_columns, incident, opposite_degrees, fixed_count,
           minimum, deleted):
    """Possible block sizes on one orbit, with fixed and moving roles transposed for columns."""
    values = words(len(moving_columns))
    keep = values.sum(axis=1) + (incident & ~deleted).bit_count() >= minimum
    # Every moving line has degree at least nine. Removing the low columns from
    # a row still leaves degree at least eight (the separate test above).
    keep &= values.sum(axis=1) + incident.bit_count() >= 9
    common_weight = sum(d for j, d in enumerate(opposite_degrees) if incident >> j & 1)
    doubles = (values == 2).sum(axis=1)
    # A pair from this orbit shares incident fixed lines and one position in
    # each size-two block. Other parallel lines contribute at most two there.
    parallel_count = 22 if fixed_count == 4 else 23
    keep &= common_weight + 9*doubles <= 2*(incident.bit_count() + doubles + parallel_count-2)
    fixed_masks = [sum(((v >> i) & 1) << j for j, v in enumerate(fixed_columns))
                   for i in range(fixed_count)]
    for i, mask in enumerate(fixed_masks):
        hit = [j for j, v in enumerate(moving_columns) if v >> i & 1]
        keep &= (values[:, hit] == 2).sum(axis=1) + (mask & incident).bit_count() <= 2
        for k in range(i):
            both = [j for j in hit if moving_columns[j] >> k & 1]
            keep &= values[:, both].sum(axis=1) + (mask & fixed_masks[k] & incident).bit_count() <= 2
    return values[keep]


def propagate(rows, columns, total):
    while all(len(pool) for pool in rows + columns):
        size = sum(map(len, rows + columns))
        for line in (rows, columns):
            sums = [v.sum(axis=1) for v in line]
            lower = [t.min() for t in sums]
            upper = [t.max() for t in sums]
            if not sum(lower) <= total <= sum(upper):
                return False
            for i, t in enumerate(sums):
                line[i] = line[i][(t >= total-sum(upper)+upper[i]) &
                                  (t <= total-sum(lower)+lower[i])]
        for parallel, opposite in ((rows, columns), (columns, rows)):
            for i, v in enumerate(parallel):
                keep = np.ones(len(v), dtype=bool)
                for j, other in enumerate(opposite):
                    available = np.bincount(other[:, i], minlength=3) > 0
                    keep &= available[v[:, j]]
                parallel[i] = v[keep]
                if not len(parallel[i]):
                    return False
        if sum(map(len, rows + columns)) == size:
            return True
    return False


def encode(corner, row_hits, col_hits, total, rows, columns):
    # Order the six moving row orbits by number of choices, preserving all labels.
    order = sorted(range(6), key=lambda i: (len(rows[i]), row_hits[i]))
    lines = [[len(corner), *corner, *(row_hits[i] for i in order), *col_hits, total]]
    digits = 2**np.arange(len(col_hits))
    for i in order:
        v = rows[i]
        lines.append([len(v), *((v > 0) @ digits + 256*((v == 2) @ digits))])
    for v in columns:
        lines.append([len(v), *(v[:, order] @ (3**np.arange(6)))])
    return ''.join(' '.join(map(str, line))+'\n' for line in lines).encode()


def frames():
    edges = tuple((1 << i) | (1 << j) for i, j in combinations(range(4), 2))
    strips = [(*edges, tail) for tail in (0, 1, 2, 4, 8)]
    for omit in edges:
        strips.append((*[e for e in edges if e != omit], *[1 << i for i in range(4) if omit >> i & 1]))
    for corner in ((3, 3), (3, 5), (3, 12)):
        transpose = tuple(sum(((c >> i) & 1) << j for j, c in enumerate(corner)) for i in range(4))
        for col_hits in strips:
            dr = tuple(r.bit_count()+3*sum(m >> i & 1 for m in col_hits) for i, r in enumerate(transpose))
            for row_hits in combinations_with_replacement(range(4), 6):
                dc = tuple(2+3*sum(u >> j & 1 for u in row_hits) for j in range(2))
                if min(dc) != 8:
                    continue
                low = sum((d == 8) << j for j, d in enumerate(dc))
                overlap = (corner[0] & corner[1]).bit_count() + 3*row_hits.count(3)
                if overlap > (5 if low == 3 else 6):
                    continue
                total = 71 - sum(m.bit_count() for m in row_hits+col_hits)
                if 3*total > 170:
                    continue
                rows = [domain(corner, col_hits, u, dc, 4, 8, low) for u in row_hits]
                columns = [domain(transpose, row_hits, w, dr, 2, 9, 0) for w in col_hits]
                if propagate(rows, columns, total):
                    yield encode(corner, row_hits, col_hits, total, rows, columns)


def planted():
    # A real 216-one matrix obtained from the 225 square using its order-three action.
    identity = tuple(range(24))
    pending = [(identity, identity)]
    group = set(pending)
    while pending:
        r, c = pending.pop()
        for a, b in symmetries():
            pair = tuple(a[i] for i in r), tuple(b[i] for i in c)
            if pair not in group:
                group.add(pair)
                pending.append(pair)
    r, c = min((r, c) for r, c in group if r != identity and
               all(r[r[r[i]]] == c[c[c[i]]] == i for i in identity))
    def orbits(perm):
        fixed = [i for i in range(1, 24) if perm[i] == i]
        moving = [(i, perm[i], perm[perm[i]]) for i in range(1, 24) if i < min(perm[i], perm[perm[i]])]
        return fixed, moving
    fr, mr = orbits(r)
    fc, mc = orbits(c)
    board = construct()
    entry = lambda i, j: int(board[i-1][j-1])
    removed = next(i for i in fr if sum(map(int, board[i-1])) == 9)
    fr.remove(removed)
    corner = tuple(sum(entry(i, j) << k for k, i in enumerate(fr)) for j in fc)
    row_hits = tuple(sum(entry(x[0], j) << k for k, j in enumerate(fc)) for x in mr)
    col_hits = tuple(sum(entry(i, x[0]) << k for k, i in enumerate(fr)) for x in mc)
    blocks = np.array([[sum(entry(x[0], j) for j in y) for y in mc] for x in mr])
    # Select the lexicographically least representative under exchanges within
    # equal fixed patterns. The row and column sorts each decrease row-major order.
    ri = sorted(range(6), key=lambda i: row_hits[i])
    ci = sorted(range(6), key=lambda j: col_hits[j])
    while True:
        old = ri[:], ci[:]
        ri.sort(key=lambda i: (row_hits[i], tuple(blocks[i, ci])))
        ci.sort(key=lambda j: (col_hits[j], tuple(blocks[ri, j])))
        if (ri, ci) == old:
            break
    x = blocks[np.ix_(ri, ci)]
    return encode(corner, tuple(row_hits[i] for i in ri), tuple(col_hits[j] for j in ci),
                  int(x.sum()), [v[None,:] for v in x], [v[None,:] for v in x.T])


def main(jobs):
    with TemporaryDirectory(prefix='z217-order-three-') as work:
        solver = compile_cpp(HERE / 'order_three_blocks.cpp', Path(work))
        control = run([solver], input=planted(), capture_output=True, check=True).stdout
        if control.strip() != b'possible':
            raise RuntimeError('failed to recover the planted weight array at 216')
        records = list(frames())
        if len(records) != 394:
            raise RuntimeError(f'unexpected number of frames: {len(records)}')
        def check(record):
            output = run([solver], input=record, capture_output=True, check=True).stdout
            if output.strip() != b'excluded':
                raise RuntimeError((output, record[:55]))
        with ThreadPoolExecutor(jobs) as pool:
            list(pool.map(check, records))
        print('216 control recovered; all 394 frames excluded.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=1)
    main(parser.parse_args().jobs)
