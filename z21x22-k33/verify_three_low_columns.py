"""Exclude a 185-one matrix on 21 x 20 with row minimum seven and column minimum nine."""
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from pathlib import Path
from random import Random
from subprocess import run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'z16x18-k33'))
from replay import catalogue, compile_cpp


def controls(solver, ordinary, minimum, rows):
    high = [i for i, r in enumerate(rows) if sum(r) == 9]
    col_degrees = list(map(sum, zip(*rows)))
    if len(high) < ordinary or min(col_degrees) < minimum or max(col_degrees) > 10:
        return False
    masks = [sum(x << j for j, x in enumerate(r)) for r in rows]
    assert all((x & y & z).bit_count() <= 2 for x, y, z in combinations(masks, 3))
    rng = Random(381)
    records = []
    for _ in range(50):
        chosen = rng.sample(high, ordinary)
        fixed = rng.sample([i for i in range(21) if i not in chosen], 10)
        if any((masks[i] & masks[j]).bit_count() > 5 for i, j in combinations(chosen + fixed, 2)):
            continue
        blocks = [sum(rows[i][j] << k for k, i in enumerate(fixed)) for j in range(19)]
        records.append(' '.join(map(str, blocks)).encode())
    if not records:
        return False
    data = b'\n'.join(records) + b'\n'
    answer = run([solver, str(ordinary), str(minimum)], input=data, capture_output=True, check=True)
    assert answer.stdout == data
    print(f'{len(records)} positive controls, {ordinary} ordinary rows, column minimum {minimum}', flush=True)
    return True


def main(jobs):
    with TemporaryDirectory(prefix='z185-marked-') as tmp:
        tmp = Path(tmp)
        five = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
        ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
        solver = compile_cpp(HERE / 'marked_nine_rows.cpp', tmp)
        def matrix(name):
            return list(zip(*[list(map(int, r)) for r in (ROOT / name).read_text().splitlines()]))
        assert controls(solver, 9, 9, matrix('z19x21-k33/witness-177.txt'))
        rows = matrix('z20x21-k33/witness-185.txt')
        assert any(controls(solver, 10, 8, [r[:j] + r[j+1:] for r in rows]) for j in range(20))
        families = catalogue(five, 10, 1)
        catalog = run([ten, '8', '19', '77', '5'], input=b'\n'.join(families) + b'\n',
                      capture_output=True, check=True).stdout.splitlines()
        records = [r for r in catalog if sum(int(x).bit_count() for x in r.split()) == 77]
        assert len(records) == 315583
        def check(batch):
            result = run([solver], input=b'\n'.join(batch)+b'\n', capture_output=True, check=True)
            assert result.stdout == b'' and result.stderr.strip() == f'{len(batch)} marks, 0 survive'.encode()
        with ThreadPoolExecutor(jobs) as pool:
            list(pool.map(check, (records[i::jobs] for i in range(jobs))))
        print(f'{len(records)} marked projections, zero completions', flush=True)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=1)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error('jobs must be positive')
    main(args.jobs)
