"""Verify the 20 by 21 bounds and necessary conditions at weight 187."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'z16x18-k33'))
from replay import catalogue, compile_cpp, read_witness, reject


def compatible_groups(blocks, size):
    # With the marked row in the new column, two other selected rows may
    # share at most one of the marked row's old columns.
    neighbors = [sum(1 << j for j in range(i + 1, len(blocks))
                     if (b & blocks[j]).bit_count() <= 1) for i, b in enumerate(blocks)]

    def choose(pool, left, picked):
        if left == 0:
            yield picked
            return
        while pool.bit_count() >= left:
            bit = pool & -pool
            pool ^= bit
            yield from choose(pool & neighbors[bit.bit_length()-1], left-1, picked | bit)

    return choose((1 << len(blocks)) - 1, size, 0)


def square_census(border, projections, jobs):
    def shard(batch):
        args = [border, 'inside', '9', '19', '11', '9', '9', '180', '--enumerate']
        lines = run(args, input=b'\n'.join(batch) + b'\n', capture_output=True,
                    check=True).stdout.splitlines()
        assert lines.pop() == f'enumerated {len(batch)}'.encode()
        result = []
        for line in lines:
            tag, *masks = line.split()
            assert tag == b'completion'
            rows = list(map(int, masks))
            assert len(rows) == 20 and all(0 <= r < 1 << 20 and r.bit_count() == 9 for r in rows)
            assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(rows, 3))
            result.append(rows)
        return result

    with ThreadPoolExecutor(max_workers=jobs) as workers:
        batches = [projections[i::jobs] for i in range(min(jobs, len(projections)))]
        squares = [sq for found in workers.map(shard, batches) for sq in found]
    assert len(squares) == 1
    rows = squares[0]
    cols = [sum(((r >> j) & 1) << i for i, r in enumerate(rows)) for j in range(20)]
    for lines in (rows, cols):
        pairs = [a & b for a, b in combinations(lines, 2)]
        for weight in (4, 5):
            supports = (sum(1 << j for j in group) for group in combinations(range(20), weight))
            possible = any(all((s & p).bit_count() <= 2 for p in pairs) for s in supports)
            assert possible == (weight == 4)
    print('Unique extremal 20 by 20 square. Largest single-line extension in either orientation: four.')


def main(census, jobs):
    read_witness(HERE / 'witness-185.txt', 20, 21, 185)
    square = read_witness(ROOT / 'z20-k33/witness-180.txt', 20, 20, 180)
    cols = [sum(((r >> j) & 1) << i for i, r in enumerate(square)) for j in range(20)]
    pairs = [a & b for a, b in combinations(cols[1:], 2)]
    options = []
    for points in combinations(range(20), 8):
        mask = sum(1 << j for j in points)
        if all((mask & p).bit_count() <= 2 for p in pairs):
            options.append(mask)
    assert len(options) == 9 and all(m & ~cols[0] == 0 for m in options)
    assert all(any((x & y & c).bit_count() > 2 for c in cols[1:]) for x, y in combinations(options, 2))
    with TemporaryDirectory(prefix='z20x21-') as folder:
        tmp = Path(folder)
        small = compile_cpp(ROOT / 'z18x19-k33/small_points.cpp', tmp, True)
        border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)
        eights = catalogue(small, 8, 72, 20, 9)
        reject(border, ('inside', 8, 20, 12, 9, 9, 188), eights, 1, jobs)
        assert not catalogue(small, 10, 80, 19, 8)
        projections = catalogue(small, 9, 72, 19, 8)
        assert len(projections) == 1226
        balanced = []
        augmented = []
        for line in projections:
            blocks = tuple(map(int, line.split()))
            assert next(compatible_groups(blocks, 7), None) is None
            if sum(b.bit_count() for b in blocks) != 72:
                continue
            balanced.append(line)
            for extra in compatible_groups(blocks, 6):
                tagged = [b | ((extra >> j & 1) << 9) for j, b in enumerate(blocks)]
                augmented.append(' '.join(map(str, tagged)).encode())
        assert len(balanced) == 1136
        reject(border, ('inside', 10, 19, 11, 9, 9, 187), augmented, 43, jobs)
        if census:
            square_census(border, balanced, jobs)
    print('185 <= z(20,21;3,3) <= 187. Weight 187 requires at least three degree-eight columns.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--census', action='store_true', help='also classify all extremal 20 by 20 squares')
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use a positive job count')
    main(args.census, args.jobs)
