"""Replay the conditional step from z(20,21) and z(21,21) to z(21,22) and z(22,22)."""
from itertools import combinations
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'z17x18-k33'))
from verify import catalogue, cliques, compile_cpp, read_witness, reject


def main():
    base = read_witness(ROOT / 'z21-k33/witness-193.txt', 21, 21, 193)
    rectangle = read_witness(HERE / 'witness-201.txt', 21, 22, 201)
    square = read_witness(ROOT / 'z22-k33/witness-210.txt', 22, 22, 210)
    assert tuple(r >> 1 for r in rectangle) == base and square[:-1] == rectangle
    assert 22 * 185 // 21 == 193 and 22 * 193 // 21 == 202
    assert 22 * 201 // 21 == 210
    with TemporaryDirectory() as folder:
        tmp = Path(folder)
        fives = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
        ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
        border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)

        # Replay the eleven-point lemma used to cap all row degrees at ten.
        families = catalogue(fives, 11, 8)
        assert len(families) == 6
        for family in families:
            blocks = tuple(map(int, family.split()))
            fours = [x for x in range(1 << 11) if x.bit_count() == 4
                     and all((x & b).bit_count() <= 2 for b in blocks)]
            assert next(cliques(fours, 28 - 2 * len(blocks)), None) is None

        families = catalogue(fives, 10, 2)
        projections = run([ten, '12', '20', '82', '8'], input=b'\n'.join(families) + b'\n',
                          check=True, capture_output=True).stdout.splitlines()
        # All cases here have the minimum total load. The border test also
        # accepts projections above the threshold if the catalogue changes.
        for line in projections:
            blocks = tuple(map(int, line.split()))
            assert len(blocks) == 20 and sum(b.bit_count() for b in blocks) == 82
            assert all((a & b).bit_count() <= 2 for a, b in combinations(blocks, 2))
        reject(border, ('inside', 10, 20, 12, 9, 11, 202), projections, 159, 1)
    print('z(21,22;3,3) = 201 and z(22,22;3,3) = 210')


if __name__ == '__main__':
    if not __debug__:
        sys.exit('Run with Python assertions enabled.')
    main()
