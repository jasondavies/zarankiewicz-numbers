"""Exclude exactly five eight-columns at weight 193 on 20 x 22."""
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'z20x21-k33'))
from verify_rare_rows import catalogue, compile_cpp
from extend_eights import transpose


def main(jobs):
    with TemporaryDirectory(prefix='z193-six-low-') as tmp:
        work = Path(tmp)
        small = compile_cpp(ROOT/'z18x19-k33/small_points.cpp', work, True)
        fives = compile_cpp(ROOT/'z17x18-k33/fives.cpp', work, True)
        ten = compile_cpp(ROOT/'z18-k33/ten_points.cpp', work, True)
        weighted = compile_cpp(ROOT/'z18x19-k33/marked_core.cpp', work)
        outside = compile_cpp(HERE/'five_tens.cpp', work)

        assert not catalogue(small, 11, 84, 19, 7)
        marks = run([ten, '8', '19', '78', '7'], input=b'\n'.join(catalogue(fives,10,2))+b'\n',
                    capture_output=True, check=True).stdout.splitlines()
        assert len(marks) == 882
        for line in marks:
            cols = transpose(tuple(map(int,line.split())),10)
            assert sorted(x.bit_count() for x in cols) == [7]*2+[8]*8

        def check(entries):
            cmd = [weighted, '0', '10', '193', '1', '17', '17', '22', '20', '8', '-1', '--all-cores']
            out = run(cmd,input=b'\n'.join(entries)+b'\n',capture_output=True,check=True).stdout
            assert out.splitlines() == [f'enumerated {len(entries)} cores 0 profiles {len(entries)}'.encode()]
        with ThreadPoolExecutor(jobs) as pool:
            list(pool.map(check,(marks[i::jobs] for i in range(min(jobs,len(marks))))))

        pure = []
        for line in catalogue(small,8,72,21,8):
            cols = transpose(tuple(map(int,line.split())),8)
            if all(c.bit_count()==9 for c in cols) and all((a&b).bit_count()<=4 for a,b in combinations(cols,2)):
                pure.append(line)
        assert len(pure)==627
        data = b'\n'.join(pure)+b'\n'
        assert run([outside,'3'],input=data,capture_output=True,check=True).stdout.startswith(b'completion ')
        assert run([outside,'4'],input=data,capture_output=True,check=True).stdout.splitlines()==[b'excluded 627 choices 2143']
        print('Excluded all 882 ten-row marks and all 2,143 choices on the 627 eight-point marks.')


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('enable assertions')
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=1)
    args=parser.parse_args()
    if args.jobs<1:parser.error('jobs must be positive')
    main(args.jobs)
