"""Exclude the marked ten-column in a 217-one rectangle with six nine-rows."""
from argparse import ArgumentParser
from itertools import combinations
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

from verify_217_loads import HERE, ROOT, compile_cpp, projections, loads, exhaust


def main(jobs):
    with TemporaryDirectory(prefix='z217-six-nines-') as directory:
        tmp=Path(directory)
        five=compile_cpp(ROOT/'z17x18-k33/fives.cpp',tmp,True)
        dense=compile_cpp(ROOT/'z18-k33/ten_points.cpp',tmp,True)
        solver=compile_cpp(HERE/'ten_column_rows.cpp',tmp)
        marks=[m for m in projections(five,dense,10,22,88,8,10)
               if loads(m,10)==[8]*3+[9]*6+[10]]
        assert len(marks)==129226
        result=run([solver,'3'],input=b'\n'.join(marks)+b'\n',capture_output=True,check=True)
        fields=result.stdout.split()
        assert fields[0]==b'completion'
        rows=tuple(map(int,fields[1:]))
        assert len(rows)==14 and max(rows)<1<<23 and rows[10].bit_count()==11
        assert all(r.bit_count()==10 for r in rows[11:])
        assert sum(r.bit_count() for r in rows[:10])==98
        assert all(((r>>22)&1)==(i<10) for i,r in enumerate(rows))
        assert all((r&s&t).bit_count()<=2 for r,s,t in combinations(rows,3))
        exhaust(solver,('8',),marks,jobs)
        print('Recovered the eleven-row plus three-tens control. Excluded all 129,226 marks.')


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=4)
    args=parser.parse_args()
    if not __debug__ or args.jobs<1:
        parser.error('enable assertions and use a positive job count')
    main(args.jobs)
