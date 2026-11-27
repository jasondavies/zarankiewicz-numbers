"""Exclude total row deficit at most three at weight 209 and count the reduced cover."""
import argparse
from collections import Counter, defaultdict
from pathlib import Path
from tempfile import TemporaryDirectory

from four_columns import PAIRS, patterns
from overlap_starts import excluded_by_count
from verify_209 import ROOT, compile_cpp, projections, reject


def check_projections(tmp, jobs):
    fives = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
    ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
    border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)

    # Each marked row has degree one more than its point load.
    short = projections(fives, ten, 10, 22, 88, 7, 9)
    assert len(short) == 25239
    groups = defaultdict(list)
    for line in short:
        total = sum(int(b).bit_count() for b in line.split())
        groups[0 if total >= 89 else 2].append(line)
    assert set(groups) == {0, 2}
    for key, floor, count in [(0, 8, 98), (2, 9, 25141)]:
        reject(border, ('inside', 10, 22, 11, floor, 12, 209, '--gain'),
               groups[key], count, jobs)

    # A long row in the mark increases the total load to at least 89.
    tall = projections(fives, ten, 10, 22, 89, 7, 11)
    assert len(tall) == 1687
    groups.clear()
    for line in tall:
        blocks = tuple(map(int, line.split()))
        loads = [sum((b >> j) & 1 for b in blocks) for j in range(10)]
        deficit = sum(max(0, 9-d) for d in loads)
        excess = sum(max(0, d-9) for d in loads)
        if deficit <= 2 and 1 <= excess <= 2:
            groups[deficit, excess].append(line)
    assert {key: len(v) for key, v in groups.items()} == {(2, 1): 359, (2, 2): 1}
    for (deficit, excess), lines in groups.items():
        low = max(8, 10 - (3-deficit))
        high = 10 + (2-excess)
        reject(border, ('inside', 10, 22, 11, low, high, 209, '--gain'),
               lines, len(lines), jobs)


def check_cover():
    starts = list(patterns())
    assert Counter(s[15] for s in starts) == {0: 4167, 1: 1374, 2: 143}
    double = [s for s in starts if s[15] == 2]
    impossible = {i for i,s in enumerate(double) if excluded_by_count(s)}
    triple = {i for i,s in enumerate(double) if any(s[p] == 3 for p in PAIRS)}
    assert len(impossible) == 20 and impossible <= triple
    assert len(triple - impossible) == 75 and {4, 25, 46, 62} <= triple - impossible
    retained = set(range(len(double))) - triple
    assert len(retained) == 48 and 4167 + 1374 + len(retained) == 5589
    print('Retained two-common-row IDs:', *sorted(retained))
    print('The cover has 5,589 starts. Total row deficit is at least four.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and choose a positive job count')
    with TemporaryDirectory(prefix='z209-deficit-') as folder:
        check_projections(Path(folder), args.jobs)
    check_cover()
