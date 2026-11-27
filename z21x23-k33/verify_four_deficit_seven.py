"""Exclude deficit seven with four degree-eight columns at weight 209."""
from argparse import ArgumentParser
from pathlib import Path
from tempfile import TemporaryDirectory

from verify_209 import ROOT, catalogue, compile_cpp, reject
from verify_six_columns import marked_row_control


def check(marks, search, jobs):
    marked_row_control(search)
    requests = []
    for line in marks:
        blocks = tuple(map(int, line.split()))
        if sum(b.bit_count() for b in blocks) != 75:
            continue
        degrees = sorted(1 + sum(b >> j & 1 for b in blocks) for j in range(8))
        if degrees == [9, 10, 10, 10, 11, 11, 11, 11]:
            # Missing rows of degree 10, 11 and 12, respectively.
            requests.append(line.rstrip() + b' 5 2 0')
    assert len(marks) == 306203
    reject(search, (), requests, 25389, jobs)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use at least one worker')
    with TemporaryDirectory(prefix='z209-four-') as folder:
        temp = Path(folder)
        small = compile_cpp(ROOT / 'z18x19-k33/small_points.cpp', temp, True)
        search = compile_cpp(Path(__file__).with_name('marked_low_rows.cpp'), temp)
        check(catalogue(small, 8, 75, 22, 8), search, args.jobs)
