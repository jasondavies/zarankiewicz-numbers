"""Exclude six degree-eight columns on a 209-one 21 x 23 matrix."""
from argparse import ArgumentParser
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from itertools import product

from verify_eight_columns import ROOT, catalogue, compatible_groups, compile_cpp, high_marks, reject
from verify_209 import read_witness

HERE = Path(__file__).resolve().parent


def row_profiles():
    profiles = []
    for deficit in range(8, 11):
        for eights in (0, 1):
            for twelves in range(11 - deficit - eights):
                nines = deficit - 2 * eights
                elevens = deficit - 1 - 2 * twelves
                tens = 21 - eights - nines - elevens - twelves
                profile = (eights, nines, tens, elevens, twelves)
                assert min(profile) >= 0
                assert sum(d * n for d, n in enumerate(profile, 8)) == 209
                profiles.append(profile)
    return profiles


def marked_row_control(binary):
    # The 207-one witness has a degree-eight column with twelve outside tens.
    square = read_witness(ROOT / 'z23-k33/witness-225.txt', 23, 23, 225)
    rows = sorted(square, key=int.bit_count, reverse=True)[:21]
    mark = next(j for j in range(23) if sum(r >> j & 1 for r in rows) == 8)
    inside = [r for r in rows if r >> mark & 1]
    assert sum(r.bit_count() == 10 and not (r >> mark & 1) for r in rows) >= 4
    blocks = [sum(((r >> j) & 1) << i for i, r in enumerate(inside))
              for j in range(23) if j != mark]
    request = ' '.join(map(str, [*blocks, 4, 0, 0])).encode()
    answer = run([binary], input=request + b'\n', capture_output=True, check=True)
    assert answer.stdout.rstrip() == b'survives ' + request


def check_large_deficit(marks, binary, jobs):
    marked_row_control(binary)
    profiles = row_profiles()
    cases = []
    exact = 0
    for line in marks:
        blocks = tuple(map(int, line.split()))
        if sum(b.bit_count() for b in blocks) != 75:
            continue
        exact += 1
        degrees = [1 + sum(b >> j & 1 for b in blocks) for j in range(8)]
        if max(degrees) > 12:
            continue
        counts = Counter(degrees)
        outside = {tuple(n - counts[d] for d, n in enumerate(profile[2:], 10))
                   for profile in profiles
                   if all(n >= counts[d] for d, n in enumerate(profile, 8))}
        if outside:
            tail = ' '.join(str(n) for option in sorted(outside) for n in option)
            cases.append(line.rstrip() + b' ' + tail.encode())

    assert len(marks) == 306203 and exact == 304162
    assert len(cases) == 219831

    def check(part):
        result = run([binary], input=b'\n'.join(part) + b'\n',
                     capture_output=True, check=True)
        if result.stdout.strip() != f'excluded {len(part)}'.encode():
            raise RuntimeError(result.stdout.decode())

    with ThreadPoolExecutor(jobs) as pool:
        list(pool.map(check, (cases[i::jobs] for i in range(min(jobs, len(cases))))))
    print(f'{exact:,} exact-load marks. {len(cases):,} fit a row profile. '
          'None admits the required outside rows of degree at least ten.', flush=True)


def check_deficit_four(border, marks, jobs):
    q, expected, lifted_count = 5, 307, 1
    direct, lifted = [], []
    for line in marks:
        blocks = tuple(map(int, line.split()))
        excess = sum(b.bit_count() for b in blocks) - 64
        if not q + 1 <= excess <= q + 2:
            continue
        if any(sum(b >> j & 1 for b in blocks) > 9 for j in range(8)):
            continue
        direct.append(line)
        for group in compatible_groups(blocks, 8):
            family = [b | ((group >> i & 1) << 8) for i, b in enumerate(blocks)]
            lifted.append(' '.join(map(str, family)).encode())
    for points, rows, count in ((8, direct, expected), (9, lifted, lifted_count)):
        reject(border, ('inside', points, 20, 23-q-points, 9, 10, 209-8*q, '--gain'),
               rows, count, jobs)


def remaining_profiles():
    # Count degree vectors allowed by the stated inequalities at q = 4 and 5.
    for q, lower, expected in ((4, 4, (4, 5, 3, 1)), (5, 5, (8, 7, 5))):
        counts = Counter()
        for deficit in range(lower, 8):
            for a, twelves, thirteens in product(range(2), range(4), range(3)):
                elevens = deficit - 1 - 2*twelves - 3*thirteens
                nines = deficit - 2*a
                tens = 21 - a - nines - elevens - twelves - thirteens
                if min(nines, tens, elevens) < 0 or (thirteens and q < 5):
                    continue
                if 2*(deficit + a + twelves + 3*thirteens) <= 3*q + 3:
                    counts[deficit] += 1
        assert tuple(counts[d] for d in range(lower, 8)) == expected


def main(part, jobs):
    remaining_profiles()
    with TemporaryDirectory(prefix='z209-six-') as folder:
        temp = Path(folder)
        small = compile_cpp(ROOT / 'z18x19-k33/small_points.cpp', temp, True)
        if part in ('large', 'all'):
            binary = compile_cpp(HERE / 'marked_low_rows.cpp', temp)
            check_large_deficit(catalogue(small, 8, 75, 22, 8), binary, jobs)
        if part in ('short', 'all'):
            border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', temp)
            projector = compile_cpp(HERE / 'nine_row_projections.cpp', temp, True)
            eight_points = high_marks(small, border, jobs, eight_columns=6, floor=69, max_missing=12)
            for ninth, missing, target, count in ((8, 8, 161, 2186), (7, 9, 169, 928583)):
                marks = catalogue(projector, ninth, 68)
                reject(border, ('inside', 9, 20, missing, 9, 13, target, '--gain'),
                       marks, count, jobs)
            assert all(3*d + 2*a < 24 for d in range(6, 8) for a in (0, 1))
            print('Excluded deficits six and seven.', flush=True)
            check_deficit_four(border, eight_points, jobs)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--part', choices=('short', 'large', 'all'), default='all')
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use at least one worker')
    main(args.part, args.jobs)
