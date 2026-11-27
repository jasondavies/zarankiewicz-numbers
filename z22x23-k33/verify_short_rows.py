"""Replay the final minimum-degree-nine exclusion at 193 on 20 by 22."""
from collections import Counter
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

from verify_six_low_columns import ROOT, catalogue, compile_cpp, transpose


def main():
    with TemporaryDirectory(prefix='z193-short-row-') as tmp:
        work = Path(tmp)
        five = compile_cpp(ROOT/'z17x18-k33/fives.cpp',work,True)
        dense = compile_cpp(ROOT/'z18-k33/ten_points.cpp',work,True)
        complete = compile_cpp(ROOT/'z18x19-k33/marked_core.cpp',work)
        seeds = catalogue(five,11,7)
        output = run([dense,'19','19','83','7','11'],input=b'\n'.join(seeds)+b'\n',
                     capture_output=True,check=True)
        marks = []
        profile = Counter([7]*8+[8]*11+[9]*3)
        for line in output.stdout.splitlines():
            loads = [x.bit_count() for x in transpose(tuple(map(int,line.split())),11)]
            if sum(loads)==83 and Counter(loads)<=profile:
                marks.append(line)
        assert len(marks)==131
        command = [complete,'0','11','193','2','23','23','22','20','9','-1','--all-cores']
        out = run(command,input=b'\n'.join(marks)+b'\n',capture_output=True,check=True).stdout
        assert out.splitlines()==[b'enumerated 131 cores 0 profiles 174']
        print('All 131 eleven-row marks excluded.')


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('enable assertions')
    main()
