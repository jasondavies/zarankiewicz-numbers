"""Verify a 156-one witness and exclude 158 ones on 18 by 19."""
import argparse
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
import sys

HERE = Path(__file__).resolve().parent
RECT = HERE.parent / 'z17x18-k33'
sys.path.insert(0, str(RECT))
from verify import SMALL, catalogue, compile_cpp, dense_blocks, read_witness, reject


def main(regular_157, jobs):
    read_witness(HERE / 'witness-156.txt', 18, 19, 156)
    with TemporaryDirectory(prefix='z18x19-') as directory:
        tmp = Path(directory)
        five = compile_cpp(RECT / 'fives.cpp', tmp, True)
        ten = compile_cpp(HERE.parent / 'z18-k33/ten_points.cpp', tmp, True)
        nine = compile_cpp(SMALL.parent / 'z16x17-k33/catalogue.cpp', tmp, True)
        border = compile_cpp(SMALL / 'borders.cpp', tmp)
        assert not dense_blocks(11, 77, catalogue(five, 11, 9))
        five_families = catalogue(five, 10, 2)
        tens = run([ten, '13'], input=b'\n'.join(five_families) + b'\n',
                   capture_output=True, check=True).stdout.splitlines()
        reject(border, ('inside', 10, 17, 9, 8, 14, 158), tens, 978, jobs)
        nines = catalogue(nine, 17, 66, 0, 7, 13)
        reject(border, ('inside', 9, 17, 10, 8, 14, 158), nines, 2418, jobs)
        if regular_157:
            reject(border, ('inside', 10, 17, 9, 8, 14, 157), tens, 978, jobs)
            nines = catalogue(nine, 17, 65, 0, 7, 12)
            reject(border, ('inside', 9, 17, 10, 8, 13, 157), nines, 87842, jobs)
            print('A 157-one matrix must contain a column of degree seven.')
    print('156 <= z(18,19;3,3) <= 157.')


if __name__ == '__main__':
    if not __debug__:
        sys.exit('Run with Python assertions enabled.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--regular-157', action='store_true',
                        help='also exclude 157 with every column of degree at least eight')
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error('the job count must be positive')
    main(args.regular_157, args.jobs)
