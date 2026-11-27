"""Bound 15 by 19 and 15 by 20 to exclude overlaps of six on short lines."""
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'z16x18-k33'))
from replay import catalogue, compile_cpp, read_witness


def check(borders, width, outside, missing, floor, ceiling, weight, marks):
    result = run([borders, 'inside', *map(str, (width, outside, missing, floor, ceiling, weight)),
                  '--enumerate'], input=b'\n'.join(marks) + b'\n',
                 capture_output=True, check=True)
    assert result.stdout.splitlines() == [f'enumerated {len(marks)}'.encode()]


def main():
    with TemporaryDirectory() as directory:
        work = Path(directory)
        small = compile_cpp(ROOT / 'z18x19-k33/small_points.cpp', work, True)
        five = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', work, True)
        ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', work, True)
        borders = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', work)

        def dense(points, blocks, weight, minimum, maximum):
            seeds = catalogue(five, points, weight - 4 * blocks)
            out = run([ten, *map(str, (maximum, blocks, weight, minimum, points))],
                      input=b'\n'.join(seeds) + b'\n', capture_output=True, check=True)
            return out.stdout.splitlines()

        for degree, count in [(8, 114), (9, 1)]:
            raw = catalogue(small, degree, 8 * degree, 18, 8)
            marks = [m for m in raw if all(int(b).bit_count() <= 4 for b in m.split())]
            assert len(marks) == count
            check(borders, degree, 18, 15-degree, 9, 13, 139, marks)
        assert not dense(10, 19, 80, 8, 19)
        marks = catalogue(small, 9, 72, 19, 8)
        assert len(marks) == 1226
        check(borders, 9, 19, 6, 9, 19, 145, marks)
        assert not dense(11, 14, 66, 6, 7)
        marks = dense(10, 14, 60, 6, 7)
        assert len(marks) == 11
        check(borders, 10, 14, 10, 7, 8, 145, marks)

        # Mark two actual eight-rows and check the complementary count on the witness.
        rows = read_witness(ROOT / 'z21-k33/witness-193.txt', 21, 21, 193)
        from itertools import combinations
        pairs = [(a, b) for a, b in combinations(rows, 2) if a.bit_count() == b.bit_count() == 8]
        assert pairs and all((a & b).bit_count() <= 5 for a, b in pairs)
        print('Excluded 139 on 15 by 19 and 145 on 15 by 20.')


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('enable assertions')
    main()
