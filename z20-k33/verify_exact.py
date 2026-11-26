"""Verify the 20 by 20 cyclic construction and apply the 19 by 20 bound."""
from itertools import combinations
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    rows = (here / 'witness-180.txt').read_text().splitlines()
    base = {0, 2, 3, 6, 7, 8, 9, 11, 15}
    assert rows == [''.join('1' if (j-i) % 20 in base else '0' for j in range(20))
                    for i in range(20)]
    assert rows[:-1] == (here.parent / 'z19x20-k33/witness-171.txt').read_text().splitlines()
    for lines in (rows, [''.join(col) for col in zip(*rows)]):
        masks = [int(line, 2) for line in lines]
        assert all(m.bit_count() == 9 for m in masks)
        assert sum(m.bit_count() for m in masks) == 180
        assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(masks, 3))
    assert 20 * 171 == 19 * 180
    print('180-one square verified in both orientations. The 19 by 20 maximum of 171 gives optimality.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with Python assertions enabled.')
    main()
