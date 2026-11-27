"""Replay restrictions on weight 209 for the 21 by 23 K3,3 problem."""
import argparse
from collections import Counter
from math import comb
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory

from four_columns import patterns

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'z16x18-k33'))
from replay import catalogue, compile_cpp, read_witness, reject
sys.path.insert(0, str(ROOT / 'z20x21-k33'))
from extend_eights import admissible, legal_supports, transpose


def projections(fives, ten, points, blocks, total, floor, cap):
    required = total - 4 * blocks
    five_sets = catalogue(fives, points, max(1, required))
    if required <= 0:
        five_sets.insert(0, b'')  # Explicitly include the empty five-block family.
    args = [ten, *map(str, (cap, blocks, total, floor, points))]
    return run(args, input=b'\n'.join(five_sets) + b'\n', capture_output=True,
               check=True).stdout.splitlines()


def compatible_group(blocks, count):
    # A new column through the mark can use only blocks meeting pairwise in at most one point.
    if not count:
        return True
    for i, a in enumerate(blocks):
        if len(blocks) - i < count:
            break
        neighbors = [b for b in blocks[i + 1:] if (a & b).bit_count() <= 1]
        if compatible_group(neighbors, count - 1):
            return True
    return False


def extension_checks():
    core = read_witness(ROOT / 'z21x22-k33/witness-201.txt', 21, 22, 201)
    columns = transpose(core, 22)
    assert next(legal_supports(columns, 21, 8), None) is None
    # Recover an actual eight-one column by hiding it from the stored core.
    j = next(i for i, c in enumerate(columns) if c.bit_count() == 8)
    assert columns[j] in legal_supports(columns[:j] + columns[j+1:], 21, 8)
    # For the two extremal parents forced by three or by four low columns,
    # count every admissible additional eight-column on the stored parent.
    for subdir, width, weight, count in [('z20x21-k33', 20, 185, 2),
                                         ('z19x21-k33', 19, 177, 3)]:
        parent = read_witness(ROOT / subdir / f'witness-{weight}.txt', width, 21, weight)
        options = list(legal_supports(parent, 21, 8))
        assert len(options) == count < 23 - width
        assert admissible(parent + tuple(options))
    square = read_witness(ROOT / 'z23-k33/witness-225.txt', 23, 23, 225)
    rows = sorted(square, key=int.bit_count, reverse=True)[:21]
    assert sum(r.bit_count() for r in rows) == 207


def main(jobs):
    extension_checks()
    with TemporaryDirectory(prefix='z209-') as folder:
        tmp = Path(folder)
        fives = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
        ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
        border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)
        # Mark ten rows on a column, under the assumption that all rows have degree <= 10.
        short = projections(fives, ten, 10, 22, 89, 8, 9)
        assert len(short) == 98
        assert all(not compatible_group(list(map(int, line.split())), 8) for line in short)
        reject(border, ('inside', 10, 22, 11, 9, 10, 209), short, 98, min(jobs, 2))

        # Mark eleven columns of a row, at most two of those columns of degree eight.
        candidates = projections(fives, ten, 11, 20, 86, 7, 20)
        scarce = []
        three_low = []
        for line in candidates:
            blocks = list(map(int, line.split()))
            loads = [sum((b >> i) & 1 for b in blocks) for i in range(11)]
            if loads.count(7) == 3 and max(loads) <= 9:
                three_low.append(line)
            if loads.count(7) <= 2:
                assert not compatible_group(blocks, 7)
                scarce.append(line)
        assert len(candidates) == 105383 and len(scarce) == 990
        # The maximum possible degree outside the marked row is twenty.
        reject(border, ('inside', 11, 20, 12, 8, 20, 209, '--gain'), scarce, 990, jobs)
        # Exactly three eight-columns gives five tens and fifteen nines.
        # An eleven-row meeting a ten-column would be in this relation.
        assert len(three_low) == 11354
        reject(border, ('inside', 11, 20, 12, 9, 10, 209, '--gain'), three_low, 11354, jobs)
        # Some ten-column carries at most two units of row deficit.
        # At deficit zero or one the other rows can have degree eight.
        reject(border, ('inside', 10, 22, 11, 8, 11, 209, '--gain'), short, 98, min(jobs, 2))
        last = projections(fives, ten, 10, 22, 88, 7, 9)
        deficit_two = [line for line in last if sum(int(b).bit_count() for b in line.split()) == 88]
        assert len(last) == 25239 and set(last) - set(deficit_two) == set(short)
        # The mark already contains two deficit units, leaving no eight-row outside it.
        reject(border, ('inside', 10, 22, 11, 9, 11, 209, '--gain'), deficit_two, 25141, jobs)
    q, r = divmod(209 - 15 * 8, 21)
    assert (21-r) * comb(q, 3) + r * comb(q+1, 3) == 114 > 2 * comb(8, 3)
    assert Counter(p[15] for p in patterns()) == {0: 4167, 1: 1374, 2: 143}
    print('5,684 four-column starts cover all remaining possibilities.')
    print('209 requires a row of degree at least 11 and between 4 and 14 eight-one columns.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use a positive job count')
    main(args.jobs)
