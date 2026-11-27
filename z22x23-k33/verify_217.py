"""Replay the final column score bounds and check the 216-one lower bound."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

from verify_217_loads import HERE, ROOT, compile_cpp, projections


def check_batch(solver, mode, points, marks, passed=0, target=217, min_nines=7):
    result = run([solver, mode, str(points), str(target), str(min_nines)],
                 input=b'\n'.join(marks)+b'\n', capture_output=True, check=True)
    expected = f'{len(marks)} tested, {passed} passed\n'.encode()
    if result.stderr != expected or len(result.stdout.splitlines()) != passed:
        raise RuntimeError((mode, points, result.stderr, result.stdout[:300]))


def controls(solver):
    rows = (HERE/'witness-216.txt').read_text().splitlines()
    assert len(rows) == 22 and all(len(r)==23 and set(r)<={'0','1'} for r in rows)
    assert sum(r.count('1') for r in rows)==216
    assert all((a&b&c).bit_count()<=2 for a,b,c in combinations(map(lambda r:int(r,2), rows),3))
    def mark(fixed, j):
        blocks = [sum((r[k]=='1') << i for i,r in enumerate(fixed)) for k in range(23) if k!=j]
        return ' '.join(map(str,blocks)).encode()
    for points in (9,10):
        j = next(j for j in range(23) if sum(r[j]=='1' for r in rows)==points)
        fixed = [r for r in rows if r[j]=='1']
        # Hide all outside rows and recover four units of gain from the eighteen tens.
        target = sum(r.count('1') for r in fixed)+9*(22-points)+4
        check_batch(solver,'outside',points,[mark(fixed,j)],1,target,4)
        if points==10:
            check_batch(solver,'through',9,[mark(fixed[:-1],j)],1)


def check_marks(solver, points, marks, jobs):
    def check(start):
        chunk = marks[start:start+256]
        if points==10:
            check_batch(solver,'through',points,chunk)
        check_batch(solver,'outside',points,chunk)
    with ThreadPoolExecutor(jobs) as pool:
        list(pool.map(check, range(0,len(marks),256)))
    print(f'{points}-point projections excluded: {len(marks):,}',flush=True)


def main(jobs):
    with TemporaryDirectory(prefix='z217-column-scores-') as directory:
        tmp = Path(directory)
        five = compile_cpp(ROOT/'z17x18-k33/fives.cpp',tmp,True)
        dense = compile_cpp(ROOT/'z18-k33/ten_points.cpp',tmp,True)
        solver = compile_cpp(HERE/'column_scores.cpp',tmp)
        controls(solver)
        print('216-one witness and positive controls verified.',flush=True)
        nines = projections(five,dense,9,22,82,8,14)
        assert len(nines)==60469
        check_marks(solver,9,nines,jobs)
        tens = projections(five,dense,10,22,88,8,14)
        assert len(tens)==453448
        eligible = []
        for mark in tens:
            blocks = list(map(int,mark.split()))
            if sum(b.bit_count() for b in blocks)>88:
                if sum(sum((b>>i)&1 for b in blocks)>8 for i in range(10))>=5:
                    continue  # Excluded by the earlier ten-point restriction.
            eligible.append(mark)
        assert len(eligible)==452058
        check_marks(solver,10,eligible,jobs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=4)
    args = parser.parse_args()
    if not __debug__ or args.jobs<1:
        parser.error('enable assertions and use a positive job count')
    main(args.jobs)
