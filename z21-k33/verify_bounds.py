"""Verify the 21 by 21 bounds and the small-line condition at 194 and 195."""
from itertools import combinations
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'z17x18-k33'))
from verify import catalogue, cliques, compile_cpp, read_witness, reject


def main():
    rows = read_witness(HERE / 'witness-193.txt', 21, 21, 193)
    transpose = [sum(((r >> j) & 1) << i for i, r in enumerate(rows)) for j in range(21)]
    assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(transpose, 3))
    cut = read_witness(ROOT / 'z20x21-k33/witness-185.txt', 20, 21, 185)
    assert rows[1:] == cut
    assert (21 * 187) // 20 == 196
    with TemporaryDirectory(prefix='z21-') as folder:
        tmp = Path(folder)
        fives = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
        ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
        border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)
        large = catalogue(fives, 11, 8)
        assert len(large) == 6
        for line in large:
            base = tuple(map(int, line.split()))
            fours = [x for x in range(1 << 11) if x.bit_count() == 4
                     and all((x & b).bit_count() <= 2 for b in base)]
            assert next(cliques(fours, 28 - 2*len(base)), None) is None
        for minimum, count, targets in ((82, 149, (196, 195)), (81, 5636, (194,))):
            large = catalogue(fives, 10, minimum - 80)
            projections = run([ten, '9', '20', str(minimum), '8'],
                              input=b'\n'.join(large) + b'\n', capture_output=True,
                              check=True).stdout.splitlines()
            for weight in targets:
                reject(border, ('inside', 10, 20, 11, 9, 10, weight), projections, count, 4)
    print('193 <= z(21,21;3,3) <= 195. At weights 194 and 195 some row or column has degree at most eight.')


if __name__ == '__main__':
    if not __debug__:
        sys.exit('Run with Python assertions enabled.')
    main()
