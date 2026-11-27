"""Replay deletion bounds and degree restrictions at weight 209 on 21 x 23."""
from argparse import ArgumentParser
from pathlib import Path
from tempfile import TemporaryDirectory

from verify_parent_bound import compatible_groups

from verify_209 import ROOT, catalogue, compile_cpp, projections, reject


def loads(line, points):
    blocks = tuple(map(int, line.split()))
    return [sum((block >> j) & 1 for block in blocks) for j in range(points)]


def residuals(small, fives, ten, border, jobs):
    eighteen = projections(fives, ten, 10, 17, 71, 7, 17)
    for weight in (177, 178):
        reject(border, ('inside', 10, 17, 12, 8, 17, weight, '--gain'),
               eighteen, 3, jobs)

    nine = catalogue(small, 9, 70, 18, 7)
    assert len(nine) == 324
    nine = [line for line in nine if loads(line, 9).count(7) >= 5]
    heavy = projections(fives, ten, 10, 18, 75, 7, 18)
    for degree, entries, count in ((9, nine, 21), (10, heavy, 24)):
        reject(border, ('inside', degree, 18, 23 - degree, 8, 18, 193, '--gain'),
               entries, count, jobs)
    print('Excluded 193 on 19 x 23. A 209-one matrix has at most one eight-row.')


def column_marks(small, fives, ten, border, jobs):
    # With local deficit at most two, load 88 forces every point load <= 9.
    capped = projections(fives, ten, 10, 22, 88, 7, 9)
    equal = [line for line in capped if sum(loads(line, 10)) == 88]
    higher = projections(fives, ten, 10, 22, 89, 7, 22)
    higher = [line for line in higher if sum(max(0, 9 - w) for w in loads(line, 10)) <= 2]
    assert (len(equal), len(higher)) == (25141, 458)
    reject(border, ('inside', 10, 22, 11, 8, 22, 209, '--gain'),
           equal + higher, 25599, jobs)

    low = catalogue(small, 8, 76, 22, 8)
    reject(border, ('inside', 8, 22, 13, 8, 22, 209, '--gain'), low, 2041, jobs)
    print('A ten-column carries at least three deficit units. '
          'The eight rows on an eight-column have total degree at most 83.')


def high_marks(small, border, jobs, eight_columns=8, floor=None, max_missing=20):
    # Mark the eight high entries with largest total excess on a short row.
    if floor is None:
        floor = 69 if eight_columns == 8 else 70
    expected, lifts = {69: (181521, 209), 70: (3768, 3)}[floor]
    width = 23 - eight_columns
    weight = 209 - 8 * eight_columns
    marks = catalogue(small, 8, floor, 20, 8)
    reject(border, ('inside', 8, 20, width - 8, 9, max_missing, weight, '--gain'), marks, expected, jobs)
    augmented = []
    counts = {}
    for line in marks:
        blocks = tuple(map(int, line.split()))
        for size in range(8, 21):
            choices = list(compatible_groups(blocks, size))
            if not choices:
                break  # A larger clique would contain one of this size.
            counts[size] = counts.get(size, 0) + len(choices)
            for mask in choices:
                lifted = [b | (((mask >> i) & 1) << 8) for i, b in enumerate(blocks)]
                augmented.append(' '.join(map(str, lifted)).encode())
    if floor == 69:
        assert counts == {8: 206, 9: 3}
    reject(border, ('inside', 9, 20, width - 9, 9, max_missing, weight, '--gain'), augmented, lifts, jobs)
    print(f'{eight_columns} eight-columns, missing degrees at most {max_missing}: '
          f'each short row has high-column excess at most {floor - 65}.')
    return marks


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--part', choices=('residuals', 'columns', 'high', 'next', 'all'), default='all')
    parser.add_argument('--jobs', type=int, default=2)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use at least one worker')
    with TemporaryDirectory(prefix='z209-eight-') as directory:
        tmp = Path(directory)
        small = compile_cpp(ROOT / 'z18x19-k33/small_points.cpp', tmp, True)
        fives = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
        ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
        border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)
        if args.part in ('residuals', 'all'):
            residuals(small, fives, ten, border, args.jobs)
        if args.part in ('columns', 'all'):
            column_marks(small, fives, ten, border, args.jobs)
        if args.part in ('high', 'all'):
            high_marks(small, border, args.jobs)
        if args.part in ('next', 'all'):
            high_marks(small, border, args.jobs, 7)
