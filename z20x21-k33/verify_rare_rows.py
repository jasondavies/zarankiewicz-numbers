"""Exclude weight 187 on 20 by 21 through a row with a rare neighbourhood."""
import argparse
from collections import Counter
from itertools import combinations, combinations_with_replacement
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'z17x18-k33'))
from verify import catalogue, cliques, compile_cpp, read_witness, reject


def parse(line):
    return tuple(map(int, line.split()))


def loads(blocks, points):
    return [sum((b >> p) & 1 for b in blocks) for p in range(points)]


def kind(blocks, points):
    """Return (total, sevens, nines) when every load lies in 7..9, else None."""
    load = loads(blocks, points)
    if min(load) < 7 or max(load) > 9:
        return None
    return sum(load), load.count(7), load.count(9)


def counting_lemma():
    # Without a six-sharing pair and without a special row, every row satisfies
    # n10 <= e - c(d), so summing gives sum c(d) <= 20 - 2q. Check every
    # possible multiset of row degrees above nine.
    def c(d):
        return 2 if d == 10 else d - 6
    cases = 0
    for q in (4, 5, 6, 7):
        for s in (0, 1):
            excess = 7 + s
            for h in range(1, excess + 1):
                for high in combinations_with_replacement(range(10, q + 9), h):
                    if sum(d - 9 for d in high) != excess:
                        continue
                    cases += 1
                    assert -s * (q - 2) + sum(map(c, high)) > 20 - 2 * q, (q, s, high)
    # With a six-sharing pair R, R' of degrees 9 + a and 9 + a'.
    for q in (6, 7):
        for a in range(1, 4):
            for b in range(1, 5 - a):
                bound = 8*q - 12 - 2*(7 - a - b) + min(q - 2, a + 3) + min(q - 2, b + 3)
                assert bound < 10 * (q - 2), (q, a, b)
                cases += 1
    print(f'Counting lemma: {cases} degree configurations force a special row.', flush=True)


def catalogue_facts(small, five, ten, large):
    nine = catalogue(small, 9, 72, 19, 7)
    special = []
    types = Counter()
    for line in nine:
        k = kind(parse(line), 9)
        if k and k[0] >= 73 and k[1] in (1, 2):
            special.append(line)
            types[k[1], k[2]] += 1
    assert types == {(1, 2): 509, (1, 3): 8, (2, 3): 698, (2, 4): 4}, types
    assert not catalogue(small, 10, 80, 19, 7)
    ten79 = catalogue(small, 10, 79, 19, 7)
    assert len(ten79) == 12
    tens = [line for line in ten79 if kind(parse(line), 10)]
    assert len(tens) == 2 and all(kind(parse(t), 10) == (79, 4, 3) for t in tens)
    assert not catalogue(small, 11, 84, 19, 7)

    # Independent nine-point generator: fix the four- and five-blocks first.
    legal = {parse(line) for line in nine if (k := kind(parse(line), 9)) and k[0] >= 73}
    assert len(legal) == 1525
    assert {parse(line) for line in catalogue(large, 73, 7, 9)} == legal
    # Independent ten-point generator, seeded by families of five-blocks.
    # Nineteen blocks of size at most five with total 76 + m need m fives.
    other = run([ten, '9', '19', '79', '7'], input=b'\n'.join(catalogue(five, 10, 3)) + b'\n',
                capture_output=True, check=True).stdout.splitlines()
    assert {parse(x) for x in other} == {parse(x) for x in tens}
    other = run([ten, '9', '19', '80', '7'], input=b'\n'.join(catalogue(five, 10, 4)) + b'\n',
                capture_output=True, check=True).stdout.splitlines()
    assert not other
    # Eleven points: total 84 needs m >= 8 fives and at least 27 - 2m fours.
    families = catalogue(five, 11, 8)
    assert len(families) == 6
    for line in families:
        base = parse(line)
        need = 27 - 2 * len(base)
        assert 0 < need and len(base) + need <= 19
        pool = [b for b in range(1 << 11) if b.bit_count() == 4 and
                all((a & b).bit_count() <= 2 for a in base)]
        assert next(cliques(pool, need), None) is None
    print('Catalogue facts: 1,219 special nine-row projections, two special ten-row projections, '
          'nothing at ten points above 79 or eleven points above 83.', flush=True)
    return nine, special, tens


def projection(rows, width, i):
    support = [j for j in range(width) if rows[i] >> j & 1]
    blocks = [sum(((r >> j) & 1) << p for p, j in enumerate(support))
              for k, r in enumerate(rows) if k != i]
    return support, blocks


def controls(nine, canonical, border):
    # Real projections: delete one row of the 193 square and mark another.
    square = read_witness(ROOT / 'z21-k33/witness-193.txt', 21, 21, 193)
    found = set(map(parse, nine))
    tested = 0
    for k in range(21):
        rows = [r for i, r in enumerate(square) if i != k]
        degrees = [sum((r >> j) & 1 for r in rows) for j in range(21)]
        for i in range(20):
            support, blocks = projection(rows, 21, i)
            load = [degrees[j] - 1 for j in support]
            if len(support) != 9 or min(load) < 7 or max(load) > 9 or sum(load) < 72:
                continue
            assert sorted(loads(blocks, 9)) == sorted(load)
            line = ' '.join(map(str, blocks)).encode() + b'\n'
            key = parse(run([canonical, '9'], input=line, capture_output=True, check=True).stdout)
            assert key in found
            tested += 1
    assert tested == 16
    # The border checker must rebuild a 185-one rectangle from one marked row.
    witness = read_witness(HERE / 'witness-185.txt', 20, 21, 185)
    for i in (2, 0):
        support, blocks = projection(witness, 21, i)
        n = len(support)
        words = run([border, 'inside', str(n), '19', str(21 - n), '8', '10', '185'],
                    input=' '.join(map(str, blocks)).encode() + b'\n',
                    capture_output=True, check=True).stdout.split()
        assert words[0] == b'completion'
        columns = list(map(int, words[1:]))
        assert len(columns) == 21 and sum(c.bit_count() for c in columns) == 185
        assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(columns, 3))
        rows = [sum(((c >> r) & 1) << j for j, c in enumerate(columns)) for r in range(20)]
        assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(rows, 3))
    print(f'Controls: {tested} real nine-point projections found; two 185-one rectangles rebuilt.',
          flush=True)


def main(jobs):
    counting_lemma()
    with TemporaryDirectory(prefix='z20x21-rare-') as directory:
        tmp = Path(directory)
        small = compile_cpp(ROOT / 'z18x19-k33/small_points.cpp', tmp, True)
        five = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
        ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
        border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)
        canonical = compile_cpp(HERE / 'canonical.cpp', tmp, True)
        large = compile_cpp(HERE / 'nine_large.cpp', tmp, True)
        nine, special, tens = catalogue_facts(small, five, ten, large)
        controls(nine, canonical, border)
        reject(border, ('inside', 10, 19, 11, 8, 10, 187), tens, 2, jobs)
        reject(border, ('inside', 9, 19, 12, 8, 10, 187), special, 1219, jobs)
    print('No 20 by 21 matrix with 187 ones avoids an all-ones 3 by 3 submatrix.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and supply a positive job count')
    main(args.jobs)
