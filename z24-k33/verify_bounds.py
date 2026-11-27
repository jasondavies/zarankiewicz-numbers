"""Verify the quick K3,3 bounds on 23 by 24 and 24 by 24."""
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'z17x18-k33'))
from verify import catalogue, cliques, compile_cpp, read_witness
sys.path.insert(0, str(ROOT/'z20x21-k33'))
from extend_eights import admissible, legal_supports, transpose


def eleven_points(tmp):
    fives = compile_cpp(ROOT/'z17x18-k33/fives.cpp', tmp, True)
    families = catalogue(fives, 11, 7)
    assert len(families) == 21
    totals = Counter()
    for line in families:
        base = tuple(map(int, line.split()))
        m = len(base)
        fours = [v for v in range(1 << 11) if v.bit_count() == 4
                 and all((v & b).bit_count() <= 2 for b in base)]
        # 23 blocks, load >= 99. A five adds two and a four adds one above three.
        for selection in cliques(fours, 30 - 2*m):
            # Only the seven-five case reaches this stage. All 23 blocks are specified.
            assert m == 7 and len(base + selection) == 23
            minimum = min(sum((b >> i) & 1 for b in base + selection) for i in range(11))
            assert minimum < 9
            totals[minimum] += 1
    assert totals
    return totals


def main():
    seed = (0, 1, 2, 3, 5, 8, 11, 13, 17, 18)
    square = tuple(sum(1 << ((j+i) % 24) for j in seed) for i in range(24))
    assert admissible(square) and sum(r.bit_count() for r in square) == 240
    assert sum(r.bit_count() for r in square[:-1]) == 230
    parent = read_witness(ROOT/'z23-k33/witness-225.txt', 23, 23, 225)
    for lines in (parent, transpose(parent,23)):
        assert len(list(legal_supports(lines, 23, 5))) == 1
        assert not any(legal_supports(lines, 23, 6))
    with TemporaryDirectory() as directory:
        print('Minimum point loads in the surviving block systems:', dict(eleven_points(Path(directory))))
    assert 24*225//23 == 234
    assert 234+9 == 243
    print('230 <= z(23,24) <= 234; 240 <= z(24,24) <= 243.')


if __name__ == '__main__':
    if not __debug__:
        sys.exit('Enable Python assertions to verify these bounds.')
    main()
