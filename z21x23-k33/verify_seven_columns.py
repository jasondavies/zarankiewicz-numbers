"""Exclude seven eight-one columns in a 209-one matrix on 21 x 23."""
from argparse import ArgumentParser
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

from verify_eight_columns import ROOT, catalogue, compatible_groups, compile_cpp, high_marks, reject


def check_generator(projector, canon, eight_point_marks):
    # Independently append a ninth point through seven blocks at total 69.
    # The unused tenth point lets the existing canonicalizer compare both lists.
    extensions = []
    for line in eight_point_marks:
        blocks = tuple(map(int, line.split()))
        if sum(b.bit_count() for b in blocks) != 69:
            continue
        for selected in compatible_groups(blocks, 7):
            family = [b | (((selected >> i) & 1) << 8) for i, b in enumerate(blocks)]
            if all(b.bit_count() <= 5 for b in family):
                extensions.append(' '.join(map(str, family)).encode())

    def keys(lines):
        data = b'\n'.join(lines) + b'\n'
        return set(run([canon, '10', 'unique'], input=data, capture_output=True,
                       check=True).stdout.splitlines())

    control = catalogue(projector, 7, 69)
    assert len(control) == len(keys(control)) == 4629
    assert keys(control) == keys(extensions)
    print('The two enumerations agree on all 4,629 calibration projections.', flush=True)


def check_counts():
    # e = column degree - 9, on the positive-weight columns only.
    surviving_profiles = set()
    for positive in range(1, 10):
        for weights in combinations_with_replacement(range(1, 10), positive):
            if sum(weights) != 9:
                continue
            demand = sum(e * (3 if e == 1 else e + 3) for e in weights)
            specials = tuple(e for e in weights if e > 1)
            for eight_rows in (0, 1):
                for short in range(max(1, eight_rows), 11):
                    if 3 * short + 5 * eight_rows < demand:
                        continue
                    surviving_profiles.add(specials)
                    # Each eleven-column meets at least five short rows, or
                    # at least four if it contains the single eight-row.
                    assert all(e == 2 for e in specials)
                    for hits in range(eight_rows * len(specials) + 1):
                        others = 5 * len(specials) - 2 * hits
                        if others > (short - eight_rows) * len(specials):
                            continue
                        required = (short - eight_rows) * comb(5, 3) + 10 * others
                        if eight_rows:
                            required += comb(4 + hits, 3)
                        assert required > 2 * comb(16 - positive, 3)
    assert surviving_profiles == {(), (2,), (2, 2)}


def main(jobs, six_deficit):
    with TemporaryDirectory(prefix='z209-seven-') as directory:
        temp = Path(directory)
        small = compile_cpp(ROOT / 'z18x19-k33/small_points.cpp', temp, True)
        border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', temp)
        if six_deficit:
            # Under D <= 5, every column has degree <= 11. A short row of
            # excess >= 5 would have one of the following high-column marks.
            high_marks(small, border, jobs, eight_columns=6, floor=69, max_missing=11)
            assert 5 * 4 < 3 * (161 - 17 * 9)
            print('With six eight-columns the row deficit is at least six.')
            return
        canon = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', temp, True)
        projector = compile_cpp(Path(__file__).with_name('nine_row_projections.cpp'), temp, True)
        marks = high_marks(small, border, jobs, eight_columns=7, floor=69)
        check_generator(projector, canon, marks)
        for ninth, missing, weight, count in ((8, 7, 153, 2186), (7, 8, 161, 928583)):
            families = catalogue(projector, ninth, 68)
            reject(border, ('inside', 9, 20, missing, 9, 14, weight, '--gain'),
                   families, count, jobs)
    check_counts()
    print('Excluded seven eight-columns on the full board and three in the parent.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--six-deficit', action='store_true',
                        help='check the deficit bound for six eight-columns instead')
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use at least one worker')
    main(args.jobs, args.six_deficit)
