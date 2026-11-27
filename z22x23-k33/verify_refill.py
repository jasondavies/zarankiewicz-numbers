"""Test every choice of thirteen retained rows of the stored 225-one square."""
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from math import comb
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
import argparse
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'z23-k33'))
from construct import symmetries
sys.path.insert(0,str(ROOT/'z16x18-k33'))
from replay import compile_cpp


def representatives(generators, removed):
    images = [[1 << (p[i]-1) for i in range(1,24)] for p in generators]
    seen = set()
    reps = []
    for subset in combinations(range(23),removed):
        mask = sum(1<<i for i in subset)
        if mask in seen:
            continue
        reps.append(mask)
        pending = [mask]
        seen.add(mask)
        while pending:
            x = pending.pop()
            points = [i for i in range(23) if x>>i&1]
            for perm in images:
                y = sum(perm[i] for i in points)
                if y not in seen:
                    seen.add(y)
                    pending.append(y)
    assert len(seen) == comb(23,removed)
    return reps


def main(jobs):
    square = (ROOT/'z23-k33/witness-225.txt').read_text().splitlines()
    generators = symmetries()
    for a,b in generators:
        assert all(square[i][j]==square[a[i+1]-1][b[j+1]-1] for i in range(23) for j in range(23))
    with TemporaryDirectory() as folder:
        binary = compile_cpp(ROOT/'z22x23-k33/refill_rows.cpp',Path(folder))
        for side in (0,1):
            rows = [int(''.join(s),2) for s in (zip(*square) if side else square)]
            masks = representatives([g[side] for g in generators],10)
            assert len(masks) == 20371
            def solve(selected, target):
                data = ' '.join(map(str,rows))+'\n'+'\n'.join(map(str,selected))+'\n'
                return run([binary,str(target)],input=data,text=True,capture_output=True,check=True).stdout.split()
            control = next(m for m in masks if any((m>>i)&1 and r.bit_count()==9 for i,r in enumerate(rows)))
            tag, removed, *model = solve([control],216)
            matrix = list(map(int,model))
            assert tag=='solution' and int(removed)==control and len(matrix)==22
            assert all(0<=r<1<<23 for r in matrix) and sum(r.bit_count() for r in matrix)>=216
            assert all((a&b&c).bit_count()<=2 for a,b,c in combinations(matrix,3))
            assert all(rows[i] in matrix for i in range(23) if not control>>i&1)
            def check(i):
                shard=masks[i::jobs*4]
                assert solve(shard,217)==['excluded',str(len(shard))]
            with ThreadPoolExecutor(jobs) as pool:
                list(pool.map(check,range(jobs*4)))
            print(f'Orientation {side}: 20,371 orbits, 1,144,066 subsets, zero completions.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=3)
    args=parser.parse_args()
    if not __debug__ or args.jobs<1:
        parser.error('enable assertions and choose a positive job count')
    main(args.jobs)
