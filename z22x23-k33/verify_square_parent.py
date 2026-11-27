"""Restrict minimum-degree-nine square parents of a 217-one rectangle."""
from collections import Counter
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

from verify_three_profiles import Counts, partitions, signatures, tuple_bounds
from verify_min9 import catalogue, compile_cpp, projections, compatible_groups
from extend_eights import admissible, legal_supports, transpose

ROOT = Path(__file__).resolve().parent.parent
CAPS = {9: 7, 10: 4, 11: 1, 12: 1, 13: 1}


def enough_nines(rows, cols):
    if sum(n*d*(d-9) for d,n in cols.items()) > sum(n*CAPS[d] for d,n in rows.items()):
        return False
    required = sorted(d-1 for d,n in rows.items() if d >= 11 for _ in range(n))
    return ((not required or required[-1] <= cols[9]) and
            (len(required) < 2 or sum(required[-2:]) <= cols[9]+5))


def possible(rows, cols):
    system = Counts()
    row = signatures(system, rows, cols, 9, CAPS)
    col = signatures(system, cols, rows, 9, CAPS)
    for i,d in enumerate(rows):
        for j,t in enumerate(cols):
            system.equal([(v,s[j]) for v,s in row[d]] + [(v,-s[i]) for v,s in col[t]], 0)
    tuple_bounds(system, row, cols, 5, 40)
    tuple_bounds(system, col, rows, 5, 40)
    return system.possible()


def check_profiles():
    profiles = [Counter([9]*(22-len(p)) + [9+x for x in p])
                for p in partitions(11) if max(p) <= 4]
    checked = 0
    survivors = []
    for i,rows in enumerate(profiles):
        for cols in profiles[i:]:
            if enough_nines(rows,cols) and enough_nines(cols,rows):
                checked += 1
                if possible(rows,cols):
                    assert cols == rows
                    survivors.append(sorted(rows.elements()))
    assert checked == 21
    assert survivors == [[9]*11+[10]*11] + [[9]*(d+1)+[10]*(20-d)+[d] for d in (11,12,13)]
    print('21 profile pairs checked, four pass the incidence counts.', flush=True)


def check_marks(points, marks, border):
    result = run([border,'inside',str(points),'21',str(22-points),'9','13','209','--enumerate'],
                 input=b'\n'.join(marks)+b'\n', capture_output=True, check=True)
    lines = result.stdout.splitlines()
    assert lines.pop() == f'enumerated {len(marks)}'.encode()
    assert all(next(compatible_groups(tuple(map(int,b.split())),8),None) is None for b in marks)
    valid = 0
    for line in lines:
        kind, *fields = line.split()
        assert kind == b'completion' and len(fields) == 22
        cols = tuple(map(int,fields))
        rows = transpose(cols,22)
        assert sum(c.bit_count() for c in cols) == 209 and admissible(cols)
        if min(r.bit_count() for r in rows) < 9:
            continue
        valid += 1
        assert next(legal_supports(rows,22,8),None) is None
        assert next(legal_supports(cols,22,8),None) is None
    assert (len(lines),valid) == ((70,35) if points == 10 else (0,0))
    print(f'{len(marks)} marks on {points} points, {valid} eligible completions, zero extensions.',flush=True)


def main():
    check_profiles()
    with TemporaryDirectory(prefix='square-parent-') as folder:
        tmp = Path(folder)
        fives = compile_cpp(ROOT/'z17x18-k33/fives.cpp',tmp,True)
        ten = compile_cpp(ROOT/'z18-k33/ten_points.cpp',tmp,True)
        small = compile_cpp(ROOT/'z18x19-k33/small_points.cpp',tmp,True)
        lift = compile_cpp(ROOT/'z22-k33/lift_eight.cpp',tmp,True)
        border = compile_cpp(ROOT/'z16x18-k33/borders.cpp',tmp)
        for points,total,count in ((11,90,338),(10,85,13205)):
            marks = projections(fives,ten,points,21,total,8,21)
            assert len(marks) == count
            check_marks(points,marks,border)
        bases = catalogue(small,8,72,21,8)
        assert len(bases) == 326456
        marks = run([lift,'217'],input=b'\n'.join(bases)+b'\n',capture_output=True,
                    check=True).stdout.splitlines()
        assert len(marks) == 234
        check_marks(9,marks,border)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('enable assertions for verification')
    main()
