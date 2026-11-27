"""Replay the high-column restrictions on a hypothetical 226-one square."""
from argparse import ArgumentParser
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from subprocess import run

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/'z21x23-k33'))
from verify_209 import compile_cpp, projections, reject, catalogue, read_witness
from verify_parent_bound import compatible_groups


def verify(jobs):
    read_witness(Path(__file__).with_name('witness-225.txt'), 23, 23, 225)
    with TemporaryDirectory() as directory:
        tmp = Path(directory)
        fives = compile_cpp(ROOT/'z17x18-k33/fives.cpp', tmp, True)
        marks = compile_cpp(ROOT/'z18-k33/ten_points.cpp', tmp, True)
        borders = compile_cpp(ROOT/'z16x18-k33/borders.cpp', tmp)
        for points, total, raw, count in ((10,89,1391,1390), (11,94,1696,389)):
            entries = projections(fives, marks, points, 22, total, 8, 22)
            assert len(entries) == raw
            keep = []
            six_low = []
            for line in entries:
                blocks = tuple(map(int,line.split()))
                loads = [sum((b >> j) & 1 for b in blocks) for j in range(points)]
                if loads.count(8) <= 5:
                    assert next(compatible_groups(blocks, 8), None) is None
                    keep.append(line)
                elif points == 11 and loads.count(8) == 6:
                    assert next(compatible_groups(blocks, 8), None) is None
                    six_low.append(line)
            reject(borders, ('inside', points, 22, 23-points, 9, 22, 226, '--gain'),
                   keep, count, jobs)
            if points == 11:
                reject(borders, ('inside',11,22,12,9,22,226,'--gain'), six_low,844,jobs)
        small = compile_cpp(ROOT/'z18x19-k33/small_points.cpp', tmp, True)
        lift = compile_cpp(ROOT/'z22-k33/lift_eight.cpp', tmp, True)
        marks = catalogue(small, 8, 75, 22, 8)
        assert len(marks) == 306203
        data = run([lift, '226'], input=b'\n'.join(marks)+b'\n', capture_output=True, check=True)
        reject(borders, ('inside',9,22,14,9,22,226,'--gain'), data.stdout.splitlines(),596,jobs)



if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=2)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use a positive job count')
    verify(args.jobs)
