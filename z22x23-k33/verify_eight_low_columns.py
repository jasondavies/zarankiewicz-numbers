"""Exclude six and seven eight-columns at 193 on 20 by 22, allowing degree-eight rows."""
from argparse import ArgumentParser
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

from verify_six_low_columns import ROOT, catalogue, compile_cpp, transpose


def main(jobs):
    # Column degrees minus one, including unmarked columns.
    profiles = {19:[7]*6+[8]*15+[9], 21:[7]*7+[8]*13+[9]*2, 23:[7]*7+[8]*14+[10]}
    expected = {(9,19):81,(9,21):590,(9,23):49,(10,19):4629,(10,21):10465,
                (10,23):1691,(11,19):90,(11,21):124}
    with TemporaryDirectory(prefix='z193-eight-low-') as tmp:
        work = Path(tmp)
        small = compile_cpp(ROOT/'z18x19-k33/small_points.cpp',work,True)
        fives = compile_cpp(ROOT/'z17x18-k33/fives.cpp',work,True)
        ten = compile_cpp(ROOT/'z18-k33/ten_points.cpp',work,True)
        solver = compile_cpp(ROOT/'z18x19-k33/marked_core.cpp',work)
        border = compile_cpp(ROOT/'z16x18-k33/borders.cpp',work)
        for points,threshold in [(9,73),(10,78),(11,83)]:
            if points == 9:
                marks = catalogue(small,9,threshold,19,7)
            else:
                seeds = catalogue(fives,points,threshold-4*19)
                marks = run([ten,'19','19',str(threshold),'7',str(points)],
                            input=b'\n'.join(seeds)+b'\n',capture_output=True,check=True).stdout.splitlines()
            top = []
            by_profile = {q:[] for n,q in expected if n==points}
            for mark in marks:
                loads = [m.bit_count() for m in transpose(tuple(map(int,mark.split())),points)]
                if sum(loads)>threshold:
                    if points in (9,10):
                        top.append(mark)
                    continue
                for q,entries in by_profile.items():
                    if Counter(loads) <= Counter(profiles[q]):
                        entries.append(mark)
            if points in (9,10):
                assert len(top) == (27 if points==9 else 12)
                high = 14 if points==9 else 16
                output = run([border,'inside',str(points),'19',str(22-points),'8',str(high),
                              '193','--enumerate'],input=b'\n'.join(top)+b'\n',capture_output=True,check=True)
                assert output.stdout.splitlines() == [f'enumerated {len(top)}'.encode()]
            for q,entries in by_profile.items():
                assert len(entries) == expected[points,q]
                def solve(batch):
                    # At q=6 the last case has no eight-row. At q=7 we allow eight-rows throughout.
                    min_row = 9 if (points,q)==(11,19) else 8
                    cmd = [solver,'0',str(points),'193',str(2 if points==11 else 1),
                           str(q),str(q),'22','20',str(min_row),'-1','--all-cores']
                    out = run(cmd,input=b'\n'.join(batch)+b'\n',capture_output=True,check=True).stdout
                    fields = out.split()
                    assert len(fields)==6 and fields[:5]==[b'enumerated',str(len(batch)).encode(),b'cores',b'0',b'profiles']
                    assert int(fields[5])>=len(batch)
                with ThreadPoolExecutor(jobs) as pool:
                    list(pool.map(solve,(entries[i::jobs] for i in range(min(jobs,len(entries))))))
                print(f'{points} points, Q={q}: {len(entries)} marks, no completions.',flush=True)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=1)
    args = parser.parse_args()
    if not __debug__ or args.jobs<1:
        parser.error('enable assertions and use a positive job count')
    main(args.jobs)
