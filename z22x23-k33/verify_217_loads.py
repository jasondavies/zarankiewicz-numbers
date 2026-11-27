"""Replay the short-row and short-column load restrictions at 217 on 22 by 23."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0,str(ROOT/'z21x23-k33'))
from verify_209 import compile_cpp, catalogue, projections


def loads(line, points):
    masks = tuple(map(int,line.split()))
    return sorted(sum((v >> i) & 1 for v in masks) for i in range(points))


def exhaust(border, arguments, marks, jobs):
    shards = min(jobs,len(marks))
    def solve(i):
        batch = marks[i::shards]
        result = run([border,*map(str,arguments)],input=b'\n'.join(batch)+b'\n',
                     capture_output=True,check=True).stdout
        if result.splitlines() != [f'excluded {len(batch)}'.encode()]:
            raise RuntimeError(result[:1000])
    with ThreadPoolExecutor(shards) as workers:
        list(workers.map(solve,range(shards)))


def main(jobs):
    with TemporaryDirectory(prefix='z217-marks-') as directory:
        tmp = Path(directory)
        small = compile_cpp(ROOT/'z18x19-k33/small_points.cpp',tmp,True)
        five = compile_cpp(ROOT/'z17x18-k33/fives.cpp',tmp,True)
        dense = compile_cpp(ROOT/'z18-k33/ten_points.cpp',tmp,True)
        border = compile_cpp(ROOT/'z16x18-k33/borders.cpp',tmp)
        # Drop a degree-nine row from the stored 225 square. Mark a ten-column.
        # Reconstruct four outside ten-rows and check the entire recovered submatrix.
        square = (ROOT/'z23-k33/witness-225.txt').read_text().splitlines()
        remove = next(i for i,r in enumerate(square) if r.count('1')==9)
        grid = square[:remove]+square[remove+1:]
        j = next(j for j in range(23) if sum(r[j]=='1' for r in grid)==10)
        fixed = [r for r in grid if r[j]=='1']
        word = [sum((r[k]=='1') << i for i,r in enumerate(fixed)) for k in range(23) if k!=j]
        target = sum(r.count('1') for r in fixed)+40
        result = run([border,'inside','10','22','4','10','10',str(target),'--gain'],
                     input=(' '.join(map(str,word))+'\n').encode(),capture_output=True,check=True)
        data = result.stdout.split()
        if not data or data[0]!=b'completion':
            raise RuntimeError('failed to recover the four-row control')
        witness = tuple(map(int,data[1:]))
        if (len(witness)!=14 or max(witness)>=1<<23 or sum(m.bit_count() for m in witness)!=target
                or any((r&s&t).bit_count()>2 for r,s,t in combinations(witness,3))):
            raise RuntimeError('invalid four-row control')

        low = [v for v in catalogue(small,8,76,22,8) if loads(v,8)[1]>=9]
        assert len(low)==900
        exhaust(border,('inside',8,22,14,9,15,217,'--gain'),low,jobs)
        print('Eight-column: excluded 900 projections.',flush=True)

        marks = projections(five,dense,10,22,88,8,9)
        tens = [m for m in marks if loads(m,10)==[8]*2+[9]*8]
        assert len(tens)==23526
        exhaust(border,('inside',10,22,12,9,15,217,'--gain'),tens,jobs)
        print('Ten-column: excluded 23,526 projections.',flush=True)

        marks = projections(five,dense,9,21,79,8,15)
        nines = [m for m in marks if sum(int(v).bit_count() for v in m.split())==79]
        assert len(nines)==15766
        assert sum(loads(m,9)==[8]*2+[9]*7 for m in nines)==881
        exhaust(border,('inside',9,21,14,8,16,217,'--gain'),nines,jobs)
        print('Nine-row: excluded 15,766 projections.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=4)
    args=parser.parse_args()
    if not __debug__ or args.jobs<1:
        parser.error('enable assertions and use a positive job count')
    main(args.jobs)
