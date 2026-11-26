"""Find an exact three-column extension of a binary 20 by 18 matrix."""
import argparse
from itertools import combinations
from pathlib import Path


def transpose(rows, width):
    return tuple(sum(((row >> j) & 1) << i for i, row in enumerate(rows))
                 for j in range(width))


def admissible(lines):
    return all((a & b & c).bit_count() <= 2 for a, b, c in combinations(lines, 3))


def extend(rows):
    if len(rows) != 20 or any(r < 0 or r >= 1 << 18 for r in rows) or not admissible(rows):
        raise ValueError('expected a K3,3-free 20 by 18 matrix')
    columns = transpose(rows, 18)
    pairs = sorted({a & b for a, b in combinations(columns, 2) if (a & b).bit_count() >= 3},
                   key=int.bit_count, reverse=True)
    candidates = []
    for points in combinations(range(20), 8):
        support = sum(1 << i for i in points)
        if all((support & p).bit_count() <= 2 for p in pairs):
            candidates.append(support)
    for i, a in enumerate(candidates):
        # Allow repeated supports in case the input core is sparse.
        neighbors = [b for b in candidates[i:] if all((a & b & c).bit_count() <= 2 for c in columns)]
        for j, b in enumerate(neighbors):
            for c in neighbors[j:]:
                if (a & b & c).bit_count() <= 2 and all((b & c & d).bit_count() <= 2 for d in columns):
                    result = transpose((*columns, a, b, c), 20)
                    assert admissible(result)
                    return result
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('matrix', type=Path)
    args = parser.parse_args()
    lines = args.matrix.read_text().splitlines()
    if len(lines) != 20 or any(len(s) != 18 or set(s) - {'0', '1'} for s in lines):
        parser.error('use twenty lines of eighteen binary digits')
    result = extend(tuple(int(s, 2) for s in lines))
    if result is None:
        print('No three-column extension.')
    else:
        for r in result:
            print(f'{r:021b}')


if __name__ == '__main__':
    main()
