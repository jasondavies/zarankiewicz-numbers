"""Exclude a 217-one rectangle with all lines of degree at least nine."""
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory
from math import comb

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT/'z21x23-k33'))
from verify_209 import compile_cpp, projections, reject, catalogue
from verify_parent_bound import compatible_groups
sys.path.insert(0, str(HERE))
from verify_218 import partitions, least


def spectra():
    for rows in partitions(19):
        if max(rows) > 4:
            continue
        a = 22-len(rows)
        long_rows = [9+r for r in rows if r > 1]
        n = len(long_rows)
        for cols in partitions(10):
            b = 23-len(cols)
            long_cols = [9+c for c in cols if c > 1]
            m = len(long_cols)
            if sum((9+c)*c for c in cols) > 7*a+4*rows.count(1)+n:
                continue
            # Long rows need d-1 nine-columns; long columns need d-5 nine-rows.
            possible = True
            for ds,offset,points,cap in ((long_rows,1,b,5),(long_cols,5,a,6)):
                loads = [d-offset for d in ds]
                if (loads and loads[-1] > points or
                    len(loads)>=2 and sum(loads[-2:])-points > cap or
                    least(points, sum(loads), 2) > cap*comb(len(loads), 2) or
                    least(points, sum(loads), 3) > 2*comb(len(loads), 3)):
                    possible = False
            if possible:
                yield a,b,long_rows,long_cols


def counts():
    profiles = list(spectra())
    assert profiles == [(5,13,[12],[]),(6,13,[13],[]),(6,14,[13],[11])]
    for a,b,(d,),long_cols in profiles:
        tens = 21-a
        for hit in (0,1):
            # Each long column has at least its degree minus a entries on ten-rows.
            needed = tens + sum(c-a for c in long_cols) + hit*(9-a)
            assert needed > 9*(b-d+hit)


def force_eight_column():
    # If a full eight-row is present, deleting it gives weight 209.
    residual = []
    for e in (1,2):
        for deficit in range(4,8):
            a = deficit-2*(e-1)
            for surplus in partitions(deficit-1):
                long = tuple(10+x for x in surplus)
                if max(long)>13:
                    continue
                tens = 22-e-a-len(long)
                required = tuple(d-1 for d in long)
                for excess in partitions(10):
                    b = 23-len(excess)
                    if sum((9+x)*x for x in excess)>10*e+7*a+4*tens+len(long):
                        continue
                    if required[-1]>b or (len(long)>=2 and sum(required[-2:])-b>5):
                        continue
                    if (least(b,sum(required),2)>5*comb(len(long),2) or
                            least(b,sum(required),3)>2*comb(len(long),3)):
                        continue
                    residual.append((deficit,long))
    assert residual==[(4,(13,))]*4
    # At deficit four the 209 parent has four low columns. A thirteen-row
    # in a 209 parent needs at least five of them.


def check_saturated_parent():
    from itertools import combinations
    from verify_209 import read_witness
    witness = read_witness(ROOT/'z22-k33/witness-210.txt',22,22,210)
    mask = (1<<22)-1
    transpose = [sum(((r>>j)&1)<<i for i,r in enumerate(witness)) for j in range(22)]
    for columns in (witness,transpose):
        pairs = [(left&right,(1<<i)|(1<<j))
                 for (i,left),(j,right) in combinations(enumerate(columns),2)]
        for indices in combinations(range(22),8):
            proposed = sum(1<<j for j in indices)
            rows_left = cols_left = mask
            for common,which in pairs:
                hit = common & proposed
                overlap = hit.bit_count()
                if overlap < 3:
                    continue
                if overlap > 3:
                    break
                rows_left &= hit
                cols_left &= which
                if not rows_left or not cols_left:
                    break
            else:
                raise AssertionError('a single deletion could allow this column')


def main():
    check_saturated_parent()
    counts()
    force_eight_column()
    with TemporaryDirectory() as folder:
        tmp = Path(folder)
        fives = compile_cpp(ROOT/'z17x18-k33/fives.cpp', tmp, True)
        ten = compile_cpp(ROOT/'z18-k33/ten_points.cpp', tmp, True)
        small = compile_cpp(ROOT/'z18x19-k33/small_points.cpp', tmp, True)
        border = compile_cpp(ROOT/'z16x18-k33/borders.cpp', tmp)
        lift = compile_cpp(ROOT/'z22-k33/lift_eight.cpp', tmp, True)
        long_marks = projections(fives,ten,11,21,90,8,21)
        assert all(next(compatible_groups(tuple(map(int,line.split())),7),None) is None for line in long_marks)
        # Every 217-one rectangle has minimum column degree eight.
        reject(border, ('inside',11,21,12,8,21,217,'--gain'), long_marks,338,2)
        tens = projections(fives,ten,10,21,85,8,21)
        assert all(next(compatible_groups(tuple(map(int,line.split())),7),None) is None for line in tens)
        reject(border, ('inside',10,21,13,8,21,217,'--gain'), tens,13205,3)
        for points,total,count in ((11,94,389),(10,89,1390)):
            entries = []
            for line in projections(fives,ten,points,22,total,8,22):
                blocks = tuple(map(int,line.split()))
                loads = [sum(b>>j & 1 for b in blocks) for j in range(points)]
                if loads.count(8) <= 5:
                    assert next(compatible_groups(blocks,7),None) is None
                    entries.append(line)
            reject(border, ('inside',points,22,22-points,8,22,217,'--gain'), entries,count,2)
        marks = catalogue(small,8,72,21,8)
        assert len(marks)==326456
        data = run([lift,'217'], input=b'\n'.join(marks)+b'\n', capture_output=True, check=True)
        nines = data.stdout.splitlines()
        assert all(next(compatible_groups(tuple(map(int,line.split())),7),None) is None for line in nines)
        reject(border, ('inside',9,21,14,8,21,217,'--gain'), nines,234,2)
    print('Every 217-one rectangle has a column of degree eight.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('enable assertions for verification')
    main()
