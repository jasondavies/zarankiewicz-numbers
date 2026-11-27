"""Classify all 210-one 22-squares and test seven-one extensions."""
from itertools import combinations
from math import comb
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT/'z21x23-k33'))
from verify_209 import compile_cpp, projections, reject, catalogue, read_witness
from verify_parent_bound import compatible_groups
sys.path.insert(0, str(ROOT/'z22x23-k33'))
from verify_218 import partitions, least


def check_profiles():
    choices = [p for p in partitions(12) if max(p) <= 4]
    def possible(row_excess, col_excess):
        nine_columns = 22-len(col_excess)
        required = [8+x for x in row_excess if x > 1]
        n = len(required)
        if n and required[-1] > nine_columns:
            return False
        if n >= 2 and sum(required[-2:])-nine_columns > 5:
            return False
        return (least(nine_columns, sum(required), 2) <= 5*comb(n, 2)
                and least(nine_columns, sum(required), 3) <= 2*comb(n, 3))
    count = 0
    for i, a in enumerate(choices):
        for b in choices[i:]:
            if not (possible(a, b) and possible(b, a)):
                continue
            count += 1
            for rows, cols in ((a,b), (b,a)):
                tens = rows.count(1)
                nines = 22-len(rows)
                longs = len(rows)-tens
                assert longs <= 1
                assert sum((9+x)*x for x in cols) > 7*nines+4*tens+longs
    assert count == 7


def completions(border, marks, points, expected):
    assert len(marks) == expected
    args = [border, 'inside', str(points), '21', str(22-points), '9', '13', '210', '--enumerate']
    lines = run(args, input=b'\n'.join(marks)+b'\n', capture_output=True, check=True).stdout.splitlines()
    assert lines.pop() == f'enumerated {expected}'.encode()
    matrices = []
    for line in lines:
        tag, *fields = line.split()
        assert tag == b'completion' and len(fields) == 22
        rows = tuple(map(int, fields))
        assert all(0 <= x < 1 << 22 for x in rows)
        assert sum(x.bit_count() for x in rows) == 210
        assert all((a & b & c).bit_count() <= 2 for a,b,c in combinations(rows, 3))
        matrices.append(rows)
    return matrices


def check_extensions(rows):
    cols = [sum(((r >> j) & 1) << i for i,r in enumerate(rows)) for j in range(22)]
    for lines in (rows,cols):
        common = {a&b for a,b in combinations(lines,2)}
        for points in combinations(range(22),7):
            support = sum(1 << i for i in points)
            assert any((support & pair).bit_count() >= 3 for pair in common)


def main():
    check_profiles()
    stored = read_witness(HERE/'witness-210.txt', 22, 22, 210)
    check_extensions(stored)
    with TemporaryDirectory() as folder:
        tmp = Path(folder)
        fives = compile_cpp(ROOT/'z17x18-k33/fives.cpp', tmp, True)
        ten = compile_cpp(ROOT/'z18-k33/ten_points.cpp', tmp, True)
        small = compile_cpp(ROOT/'z18x19-k33/small_points.cpp', tmp, True)
        border = compile_cpp(ROOT/'z16x18-k33/borders.cpp', tmp)
        lift = compile_cpp(HERE/'lift_eight.cpp', tmp, True)
        large = projections(fives, ten, 11, 21, 90, 8, 12)
        for line in large:
            assert next(compatible_groups(tuple(map(int, line.split())), 8), None) is None
        reject(border, ('inside',11,21,11,9,13,210,'--gain'), large, 338, 1)
        squares = completions(border, projections(fives, ten, 10, 21, 85, 8, 12), 10, 13205)
        assert len(squares) == 1
        check_extensions(squares[0])
        marks = catalogue(small, 8, 72, 21, 8)
        assert len(marks) == 326456
        result = run([lift], input=b'\n'.join(marks)+b'\n', capture_output=True, check=True)
        assert not completions(border, result.stdout.splitlines(), 9, 81)
    print('One 210-one square up to row and column permutations. Zero seven-one extensions.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('enable assertions for verification')
    main()
