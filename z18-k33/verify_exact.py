"""Verify z(18,18;3,3) = 150 using a marked column on either side of the square."""
from itertools import combinations
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
import sys

HERE = Path(__file__).resolve().parent
RECT = HERE.parent / 'z17x18-k33'
sys.path.insert(0, str(RECT))
from verify import SMALL, catalogue, compile_cpp, dense_blocks, read_witness, reject


def main():
    rows = read_witness(HERE / 'witness-150.txt', 18, 18, 150)
    triples = [sum(1 << p for p in t) for t in combinations(range(18), 3)]
    # Check the column-triple formulation independently of the row-triple test.
    assert all(sum((row & t) == t for row in rows) <= 2 for t in triples)
    with TemporaryDirectory(prefix='z18-proof-') as directory:
        tmp = Path(directory)
        five = compile_cpp(RECT / 'fives.cpp', tmp, True)
        ten = compile_cpp(HERE / 'ten_points.cpp', tmp, True)
        nine = compile_cpp(SMALL.parent / 'z16x17-k33/catalogue.cpp', tmp, True)
        border = compile_cpp(SMALL / 'borders.cpp', tmp)
        assert not dense_blocks(11, 77, catalogue(five, 11, 9))
        print('Eleven-point case excluded.', flush=True)
        five_families = catalogue(five, 10, 2)
        tens = run([ten], input=b'\n'.join(five_families) + b'\n',
                   capture_output=True, check=True).stdout.splitlines()
        reject(border, ('inside', 10, 17, 8, 8, 10, 151), tens, 978, 4)
        nines = catalogue(nine, 17, 66, 0, 7, 8)
        reject(border, ('inside', 9, 17, 9, 8, 9, 151), nines, 1821, 4)
        # Same neighbourhood and border search, one lower target, must return
        # a genuine extremal square. Check its dimensions, weight and triples.
        trial = run([border, 'inside', '10', '17', '8', '8', '10', '150'],
                    input=b'\n'.join(tens) + b'\n', capture_output=True, check=True)
        first, *masks = trial.stdout.split()
        assert first == b'completion'
        solution = list(map(int, masks))
        assert len(solution) == 18 and all(0 <= r < 1 << 18 for r in solution)
        assert sum(r.bit_count() for r in solution) == 150
        assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(solution, 3))
    print('Exact value 150.')


if __name__ == '__main__':
    if not __debug__:
        sys.exit('Run with Python assertions enabled.')
    main()
