"""Exclude weight 218 on 22 x 23 using the 209-one deletion bounds."""
from argparse import ArgumentParser
from itertools import combinations, product
from math import comb
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'z21x23-k33'))
from verify_209 import compile_cpp, projections, reject, read_witness
from verify_parent_bound import compatible_groups


def partitions(total, floor=1):
    if total == 0:
        yield ()
    for term in range(floor, total+1):
        for tail in partitions(total-term, term):
            yield (term,) + tail


def least(bins, total, order):
    """Convex lower bound on the number of subsets within the bins."""
    assert bins > 0 and total >= 0
    q, r = divmod(total, bins)
    return (bins-r)*comb(q, order) + r*comb(q+1, order)


def short_rows_possible(a, high, b, s):
    # s is the total number of high entries in the a nine-rows.
    nine_entries = 9*a - s
    if least(b, nine_entries, 2) > comb(a, 2):
        return False
    loads = [3 if d == 10 else d-6 for d in high]
    if max(loads) > a or sum(loads) > s:
        return False
    for _ in range(s-sum(loads)):
        loads[loads.index(min(loads))] += 1
    return (sum(comb(x, 3) for x in loads) + least(b, nine_entries, 3)
            <= 2*comb(a, 3))


def check_counts():
    survivors = set()
    for a, twelves, thirteens in product(range(5, 9), range(4), range(3)):
        elevens = a-2-2*twelves-3*thirteens
        if elevens < 0:
            continue
        long = (11,)*elevens + (12,)*twelves + (13,)*thirteens
        tens = 22-a-len(long)
        deficit = a-1
        allowed = {q for q, lo, hi in ((4, 4, 6), (5, 5, 7))
                   if lo <= deficit <= hi and 2*(deficit+twelves+3*thirteens) <= 3*q+3
                   and (not thirteens or q == 5)}
        for k in (0, 1):
            for excess in partitions(11+k):
                high = tuple(9+x for x in excess)
                b = 23-k-len(high)
                for n in range(a+1):
                    # n nine-rows leave five eight-columns, the rest leave four.
                    if (n and 5 not in allowed) or (n < a and 4 not in allowed):
                        continue
                    s = (5+k)*a-n
                    if not short_rows_possible(a, high, b, s):
                        continue
                    for hit in product(range(k+1), repeat=len(long)):
                        h = sum(hit)
                        if sum((d-10)*x for d, x in zip(long, hit)) > 3:
                            continue
                        if any(long[i]-8-hit[i] + long[j]-8-hit[j] - (q-k) > 2
                               for i, j in combinations(range(len(long)), 2)
                               for q, count in ((4, a-n), (5, n)) if count):
                            continue
                        cap = sum(1 + int(d == 11 and x) for d, x in zip(long, hit))
                        nine = sum(long)-h-cap
                        if (least(b, nine, 2) > 5*comb(len(long), 2) or
                                least(b, nine, 3) > 2*comb(len(long), 3)):
                            continue
                        needed = sum(high)-s-cap
                        triples = n*comb(4+k, 3) + (a-n)*comb(5+k, 3)
                        if triples + least(tens, needed, 3) > 2*comb(len(high), 3):
                            continue
                        survivors.add((a, k, long, high, n, h))
    assert len(survivors) == 7
    for a, k, long, high, n, h in survivors:
        assert k == 1 and h == 3 and high[-2] >= 11
        core_nines = a + 8-h
        assert high[-1] + high[-2] - 2 > core_nines + 5
    print('Excluded all seven remaining degree and deletion patterns.', flush=True)


def check_marks(marks, border, jobs):
    pure, mixed = [], []
    assert len(marks) == 52885
    for line in marks:
        blocks = list(map(int, line.split()))
        degrees = [1+sum(x >> j & 1 for x in blocks) for j in range(11)]
        if degrees.count(8) > 1 or sum(max(0, d-9) for d in degrees) > 12:
            continue
        assert next(compatible_groups(blocks, 7), None) is None
        (mixed if min(degrees) == 8 else pure).append(line)
    for rows, extra, target, count in ((pure, 12, 218, 338), (pure, 11, 210, 338),
                                       (mixed, 12, 218, 3794)):
        reject(border, ('inside', 11, 21, extra, 9, 14, target, '--gain'), rows, count, jobs)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use at least one worker')
    read_witness(Path(__file__).with_name('witness-216.txt'), 22, 23, 216)
    check_counts()
    with TemporaryDirectory(prefix='z218-') as folder:
        temp = Path(folder)
        fives = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', temp, True)
        eleven = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', temp, True)
        border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', temp)
        check_marks(projections(fives, eleven, 11, 21, 90, 7, 21), border, args.jobs)
