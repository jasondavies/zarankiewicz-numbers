"""Verify the two witnesses and the 21 × 23 obstruction to weights 219 and 228."""
import argparse
from itertools import combinations
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'z17x18-k33'))
from verify import catalogue, cliques, compile_cpp, read_witness, reject


def check_both_sides(file, height, width, weight):
    rows = read_witness(file, height, width, weight)
    columns = [sum(((r >> j) & 1) << i for i, r in enumerate(rows)) for j in range(width)]
    assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(columns, 3))
    return rows


def check_extension_control():
    # Hide the final nine-one row of the known 210-one square and recover it.
    square = read_witness(ROOT / 'z22-k33/witness-210.txt', 22, 22, 210)
    core = read_witness(ROOT / 'z21x22-k33/witness-201.txt', 21, 22, 201)
    assert square[:-1] == core
    pairs = {a & b for a, b in combinations(core, 2)}
    recovered = []
    for subset in combinations(range(22), 9):
        support = sum(1 << j for j in subset)
        if all((support & pair).bit_count() <= 2 for pair in pairs):
            recovered.append(support)
    assert recovered == [square[-1]]


def main(jobs):
    rect = check_both_sides(HERE / 'witness-216.txt', 22, 23, 216)
    square = check_both_sides(ROOT / 'z23-k33/witness-225.txt', 23, 23, 225)
    assert square[:-1] == rect and square[-1].bit_count() == 9
    constructed = run([sys.executable, ROOT / 'z23-k33/construct.py'], capture_output=True, check=True)
    assert constructed.stdout.splitlines() == (ROOT / 'z23-k33/witness-225.txt').read_bytes().splitlines()
    check_extension_control()
    assert 23*201//22 == 210 and 22*209//21 == 218 and 23*218//22 == 227
    with TemporaryDirectory(prefix='z22x23-') as folder:
        tmp = Path(folder)
        fives = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
        ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
        borders = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)
        large = catalogue(fives, 11, 8)
        assert len(large) == 6
        for family in large:
            blocks = tuple(map(int, family.split()))
            fours = [b for b in range(1 << 11) if b.bit_count() == 4
                     and all((b & a).bit_count() <= 2 for a in blocks)]
            assert next(cliques(fours, 28 - 2*len(blocks)), None) is None
        families = catalogue(fives, 10, 2)
        projections = run([ten, '11', '20', '82', '8'], input=b'\n'.join(families) + b'\n',
                          capture_output=True, check=True).stdout.splitlines()
        reject(borders, ('inside', 10, 20, 13, 9, 10, 210), projections, 159, jobs)
    print('Initial deletion bounds: 216 <= z(22,23;3,3) <= 218 and 225 <= z(23,23;3,3) <= 227.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable Python assertions and use a positive job count')
    main(args.jobs)
