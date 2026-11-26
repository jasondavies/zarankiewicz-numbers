"""Test every pair of seven-one columns on a 143-one 18 by 17 core."""
import argparse
from itertools import combinations
from pathlib import Path


def find_pair(columns, points=18, degree=7):
    intersections = {a & b for a, b in combinations(columns, 2) if (a & b).bit_count() >= 3}
    allowed = []
    for support in combinations(range(points), degree):
        mask = sum(1 << j for j in support)
        if all((mask & p).bit_count() <= 2 for p in intersections):
            allowed.append(mask)
    for a, b in combinations(allowed, 2):
        if all((c & a & b).bit_count() <= 2 for c in columns):
            return len(allowed), (a, b)
    return len(allowed), None


def main(path):
    grid = path.read_text().splitlines()
    if len(grid) == 18 and all(len(row) == 17 for row in grid):
        grid = [''.join(row) for row in zip(*grid)]
    if len(grid) != 17 or any(len(r) != 18 or set(r) - {'0', '1'} for r in grid):
        raise ValueError('expected an 18 by 17 binary core or its transpose')
    # The seventeen input masks are columns of the 18 by 17 core.
    columns = tuple(int(row, 2) for row in grid)
    if sum(c.bit_count() for c in columns) != 143:
        raise ValueError('the core must have weight 143')
    if any((a & b & c).bit_count() > 2 for a, b, c in combinations(columns, 3)):
        raise ValueError('the core contains an all-ones 3 by 3')
    count, pair = find_pair(columns)
    print(f'{count} individually legal seven-one columns.')
    if pair is None:
        print('No pair extends this core.')
        return
    full = columns + pair
    assert sum(c.bit_count() for c in full) == 157
    assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(full, 3))
    print('157-one witness:')
    for j in range(17, -1, -1):
        print(''.join(str(c >> j & 1) for c in full))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('matrix', type=Path)
    main(parser.parse_args().matrix)
