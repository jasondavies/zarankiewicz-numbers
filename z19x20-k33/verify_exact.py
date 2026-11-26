"""Verify the cyclic 171-one witness and exclude weight 172 on 19 by 20."""
from itertools import combinations
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent / 'z16x18-k33'
sys.path.insert(0, str(SHARED))
from replay import catalogue, compile_cpp, line_bytes, read_witness, reject


def transpose(rows, width):
    return [sum(((r >> j) & 1) << i for i, r in enumerate(rows)) for j in range(width)]


def check_completion(binary, rows, width, mark, low, high):
    points = [j for j in range(width) if (rows[mark] >> j) & 1]
    blocks = [sum(((r >> j) & 1) << h for h, j in enumerate(points))
              for i, r in enumerate(rows) if i != mark]
    args = ['inside', len(points), len(blocks), width - len(points), low, high, 171]
    output = run([binary, *map(str, args)], input=line_bytes(blocks) + b'\n',
                 capture_output=True, check=True).stdout.split()
    assert output[0] == b'completion'
    cols = tuple(map(int, output[1:]))
    assert len(cols) == width and all(0 <= c < 1 << len(rows) for c in cols)
    assert sum(c.bit_count() for c in cols) == 171
    assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(cols, 3))


def main():
    rows = read_witness(HERE / 'witness-171.txt', 19, 20, 171)
    cols = transpose(rows, 20)
    assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(cols, 3))
    assert (20 * 156) // 19 == 164
    with TemporaryDirectory(prefix='z19x20-') as directory:
        tmp = Path(directory)
        generator = compile_cpp(HERE.parent / 'z18x19-k33/small_points.cpp', tmp, True)
        border = compile_cpp(SHARED / 'borders.cpp', tmp)
        check_completion(border, rows, 20, 0, 8, 9)
        check_completion(border, cols, 19, next(i for i, c in enumerate(cols) if c.bit_count() == 9), 9, 9)
        assert not catalogue(generator, 10, 80, 19, 8)
        eights = catalogue(generator, 8, 64, 18, 8)
        reject(border, ('inside', 8, 18, 12, 8, 12, 172), eights, 114, 1)
        nines = catalogue(generator, 9, 73, 19, 8)
        assert len(nines) == 90
        exact = [line for line in nines if sum(int(x).bit_count() for x in line.split()) == 73]
        reject(border, ('inside', 9, 19, 10, 9, 9, 172), exact, 81, 1)
    print('Exact value 171.')


if __name__ == '__main__':
    if not __debug__:
        sys.exit('Run with Python assertions enabled.')
    main()
