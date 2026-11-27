"""Rule out ten high-column entries on a row of a 201-one 21 by 22 rectangle."""
from argparse import ArgumentParser
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'z22x23-k33'))
from verify_second_reduction import control, compile_cpp, catalogue
sys.path.insert(0, str(ROOT / 'z21x23-k33'))
from parent_extensions import extensions
from extend_eights import admissible


def load(mark):
    return sum(int(x).bit_count() for x in mark.split())


def complete(batches, command, jobs, profiles=None):
    def solve(batch):
        result = run(command, input=b'\n'.join(batch) + b'\n', capture_output=True, check=True)
        *cores, summary = result.stdout.splitlines()
        expected = f'enumerated {len(batch)}'
        if profiles is not None:
            expected += f' cores {len(cores)} profiles {profiles * len(batch)}'
        assert summary == expected.encode()
        return cores
    with ThreadPoolExecutor(jobs) as pool:
        return [core for group in pool.map(solve, batches) for core in group]


def batches(marks, size=100):
    return [marks[i:i+size] for i in range(0, len(marks), size)]


def main(jobs, counts):
    with TemporaryDirectory() as directory:
        work = Path(directory)
        five = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', work, True)
        ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', work, True)
        border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', work)
        weighted = compile_cpp(ROOT / 'z18x19-k33/marked_core.cpp', work)
        gain = compile_cpp(HERE / 'high_column_gain.cpp', work)
        control(weighted)
        all_marks = []
        for minimum, cap, expected in [(82,20,159), (81,9,5487), (80,8,79801)]:
            families = catalogue(five, 10, max(1, minimum-80))
            if minimum == 80:
                families.insert(0, b'')
            marks = run([ten, str(cap), '20', str(minimum), '8', '10'],
                        input=b'\n'.join(families)+b'\n', capture_output=True,
                        check=True).stdout.splitlines()
            if minimum == 81:
                marks = [mark for mark in marks if load(mark) == 81]
            assert len(marks) == expected
            all_marks.extend(marks)
            for q in sorted(counts & {2, 3}):
                width, weight, excess = 22-q, 201-8*q, 3+q
                if minimum == 80:
                    args = [0,10,weight,excess,excess,excess**2,width,21,6,-1,'--nine-column-cores']
                    cores = complete(batches(marks), [weighted,*map(str,args)], jobs,
                                     profiles=7 if q == 2 else 11)
                else:
                    args = ['inside',10,20,width-10,9,9+excess-(minimum-80),weight,'--enumerate']
                    cores = complete(batches(marks), [border,*map(str,args)], jobs)
                assert len(cores) == int(q == 3 and minimum == 82)
                for core in cores:
                    tag, *words = core.split()
                    cols = tuple(map(int, words))
                    assert tag == b'completion' and len(cols) == width
                    assert all(0 <= c < 1<<21 for c in cols)
                    assert sum(c.bit_count() for c in cols) == weight and admissible(cols)
                    supports, best = extensions(cols)
                    assert (len(supports),len(best)) == (4,2)
                    # These columns realize the required excess at q=3.
                    fixed = cols[:10]
                    mark = ' '.join(str(sum(((c>>i)&1)<<j for j,c in enumerate(fixed)))
                                    for i in range(20)).encode()
                    control_result = run([gain,'3'], input=mark+b'\n', capture_output=True, check=True)
                    assert control_result.stdout.strip() == mark
                print(q, minimum, len(marks), len(cores), 'cores, zero extensions', flush=True)

        if 4 in counts:
            def screen(batch):
                out = run([gain,'4'],input=b'\n'.join(batch)+b'\n',capture_output=True,check=True)
                passed = out.stdout.splitlines()
                assert set(passed) <= set(batch)
                assert out.stderr.strip() == f'{len(batch)} projections, {len(passed)} survive'.encode()
                return passed
            with ThreadPoolExecutor(jobs) as pool:
                kept = [mark for group in pool.map(screen,batches(all_marks)) for mark in group]
            assert Counter(map(load,kept)) == {80:66,81:35,82:12}
            for q in range(4,12):
                args = ['inside',10,20,12-q,9,20,201-8*q,'--enumerate']
                assert not complete(batches(kept,8),[border,*map(str,args)],jobs)
            print('113 projections checked at every remaining positive width, zero cores', flush=True)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=4)
    parser.add_argument('--group',choices=('2','3','4+','all'),default='all')
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use a positive job count')
    main(args.jobs,{2,3,4} if args.group == 'all' else {int(args.group[0])})
