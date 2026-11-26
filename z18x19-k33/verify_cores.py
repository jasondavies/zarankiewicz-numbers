"""Exclude seven-one extensions from extremal squares with one side of minimum degree eight."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
RECT = HERE.parent / 'z17x18-k33'
sys.path.insert(0, str(RECT))
from verify import SMALL, catalogue, compile_cpp, dense_blocks


def extension(rows, candidates):
    pairs = {a & b for a, b in combinations(rows, 2) if (a & b).bit_count() >= 3}
    return next((s for s in candidates if all((s & p).bit_count() <= 2 for p in pairs)), None)


def check_square(rows, candidates):
    assert len(rows) == 18 and all(0 <= r < 1 << 18 for r in rows)
    assert sum(r.bit_count() for r in rows) == 150
    assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(rows, 3))
    columns = [sum(((r >> j) & 1) << i for i, r in enumerate(rows)) for j in range(18)]
    for orientation in (rows, columns):
        support = extension(orientation, candidates)
        if support is not None:
            raise RuntimeError(f'157-one completion: {[*orientation, support]}')


def enumerate_and_check(border, t, projections, expected, completions, candidates, jobs):
    assert len(projections) == expected
    args = [border, 'inside', str(t), '17', str(18 - t), '8', '14', '150', '--enumerate']

    def shard(part):
        data = run(args, input=b'\n'.join(part) + b'\n', capture_output=True, check=True)
        lines = data.stdout.splitlines()
        assert lines.pop() == f'enumerated {len(part)}'.encode()
        for line in lines:
            tag, *masks = line.split()
            assert tag == b'completion'
            check_square(tuple(map(int, masks)), candidates)
        return len(lines)

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        total = sum(pool.map(shard, [projections[i::jobs] for i in range(min(jobs, expected))]))
    assert total == completions, (total, completions)
    print(f'{t}-row: {expected} projections, {total} completions, zero seven-one extensions.', flush=True)


def main(jobs):
    candidates = tuple(sum(1 << j for j in pos) for pos in combinations(range(18), 7))
    with TemporaryDirectory(prefix='z18x19-cores-') as directory:
        tmp = Path(directory)
        five = compile_cpp(RECT / 'fives.cpp', tmp, True)
        ten = compile_cpp(HERE.parent / 'z18-k33/ten_points.cpp', tmp, True)
        nine = compile_cpp(SMALL.parent / 'z16x17-k33/catalogue.cpp', tmp, True)
        border = compile_cpp(SMALL / 'borders.cpp', tmp)
        assert not dense_blocks(11, 77, catalogue(five, 11, 9))
        fives = catalogue(five, 10, 2)
        tens = run([ten, '13'], input=b'\n'.join(fives) + b'\n',
                   capture_output=True, check=True).stdout.splitlines()
        enumerate_and_check(border, 10, tens, 978, 1, candidates, jobs)
        nines = catalogue(nine, 17, 65, 0, 7, 13)
        enumerate_and_check(border, 9, nines, 87842, 5, candidates, jobs)
    print('Any 157-one matrix has at least two columns of degree seven.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use a positive job count')
    main(args.jobs)
