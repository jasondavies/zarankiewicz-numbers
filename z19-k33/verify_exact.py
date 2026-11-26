"""Verify the 19 by 19 construction and the deletion bound from z(18,19)=156."""
from collections import Counter
from itertools import combinations
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    rows = (here / 'witness-164.txt').read_text().splitlines()
    assert len(rows) == 19 and all(len(r) == 19 and set(r) <= {'0', '1'} for r in rows)
    assert rows[:-1] == (here.parent / 'z18x19-k33/witness-156-min8.txt').read_text().splitlines()
    for lines in (rows, [''.join(col) for col in zip(*rows)]):
        masks = [int(line, 2) for line in lines]
        assert sum(mask.bit_count() for mask in masks) == 164
        assert Counter((a & b & c).bit_count() for a, b, c in combinations(masks, 3)) == {
            0: 100, 1: 322, 2: 547,
        }
    assert (19 * 156) // 18 == 164
    print('164-one square verified in both orientations. The 18 by 19 maximum of 156 implies optimality.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Enable Python assertions for verification.')
    main()
