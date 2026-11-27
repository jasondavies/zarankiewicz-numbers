"""Check the excess bounds on rows of an extremal 201-one rectangle."""
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'z20x21-k33'))
from verify_bounds import compatible_groups, compile_cpp, catalogue
from extend_eights import transpose


def lifted_marks(blocks, points):
    # The low column also contains the marked row, stored in bit 20.
    keep = [r | (1 << 20) for r in transpose(blocks, points)]
    options = [c | (1 << 20) for c in compatible_groups(blocks, 7)]

    def add(fixed, pool):
        for i, col in enumerate(pool):
            if any((x & y & col).bit_count() > 2 for x, y in combinations(fixed, 2)):
                continue
            new = (*fixed, col)
            yield len(new), transpose(new, 21)[:20]
            yield from add(new, pool[i+1:])
    return list(add(keep, options))


def check(solver, n, records):
    raw = ''.join(' '.join(map(str, r))+'\n' for r in records).encode()
    args = ['inside', n, 20, 22-n, 8, 20, 201, '--enumerate']
    out = run([solver,*map(str,args)],input=raw,capture_output=True,check=True)
    assert out.stdout.splitlines() == [f'enumerated {len(records)}'.encode()]


def main(jobs):
    with TemporaryDirectory() as tmp:
        work = Path(tmp)
        small = compile_cpp(ROOT/'z18x19-k33/small_points.cpp', work, True)
        border = compile_cpp(ROOT/'z16x18-k33/borders.cpp', work)
        for points, load, count, touched, expected in [(9,76,2245,0,{}), (8,70,3768,19,{9:40}),
                                                     (7,64,283,41,{8:49}), (6,58,116,1,{7:2,8:1})]:
            data = catalogue(small, points, load, 20, 8)
            assert len(data) == count
            extra = {}
            active = 0
            high = []
            for line in data:
                blocks = tuple(map(int,line.split()))
                lifts = lifted_marks(blocks, points)
                if lifts:
                    active += 1
                if points == 9 or (points == 8 and sum(x.bit_count() for x in blocks) > load):
                    high.append(blocks)
                for n, record in lifts:
                    extra.setdefault(n,[]).append(record)
            assert active == touched and {n:len(r) for n,r in extra.items()} == expected
            for n, records in extra.items():
                check(border,n,records)
            if points>=8:
                assert len(high) == (2245 if points==9 else 41)
                batches = [high[i::jobs] for i in range(min(jobs,len(high)))]
                with ThreadPoolExecutor(jobs) as pool:
                    futures = [pool.submit(check,border,points,batch) for batch in batches]
                    for future in futures:
                        future.result()
            print(points,count,active,'marks admitting an extra low column',flush=True)


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('enable assertions')
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--jobs",type=int,default=1)
    args = parser.parse_args()
    if args.jobs < 1:parser.error("jobs must be positive")
    main(args.jobs)
