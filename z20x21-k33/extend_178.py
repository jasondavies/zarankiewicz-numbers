"""Test whether a 178-one 19 by 21 matrix extends to 186 or 194 ones."""
import argparse
from pathlib import Path

from extend_eights import admissible, legal_supports


def longest_extension(rows):
    candidates = list(legal_supports(rows, 21, 8))
    for i, a in enumerate(candidates):
        for b in candidates[i:]:
            if all((a & b & old).bit_count() <= 2 for old in rows):
                return (a, b)
    return tuple(candidates[:1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('matrix', type=Path, help='nineteen lines of twenty-one binary digits')
    args = parser.parse_args()
    strings = args.matrix.read_text().splitlines()
    if len(strings) != 19 or any(len(s) != 21 or set(s) - {'0', '1'} for s in strings):
        parser.error('expected a 19 by 21 binary matrix')
    rows = tuple(int(s, 2) for s in strings)
    if sum(r.bit_count() for r in rows) != 178 or not admissible(rows):
        parser.error('expected exactly 178 ones and no all-ones 3 by 3 submatrix')
    extra = longest_extension(rows)
    result = rows + extra
    if not admissible(result):
        raise RuntimeError('invalid extension')
    print(f'{len(extra)} eight-row(s) can be added, giving {178 + 8 * len(extra)} ones.')
    if extra:
        print('\n'.join(f'{r:021b}' for r in result))
