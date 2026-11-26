"""Exclude column counts (4, 15, 2) at weight 187 on 20 by 21."""
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
from replay import catalogue, compile_cpp, read_witness
from extend_eights import admissible, transpose

EXPECTED = {2: (0, 0), 3: (1747, 8), 4: (2504059, 8), 5: (48441, 0)}


def rooted(rows, col, *, shuffle=False):
    support = [i for i, r in enumerate(rows) if r >> col & 1]
    columns = [i for i in range(17) if i != col]
    if shuffle:
        columns.reverse()
        support = support[2:] + support[:2]
    assert len(support) == 9 and sorted(rows[i].bit_count() for i in support) == [7] + [8]*8
    blocks = [sum(((rows[r] >> j) & 1) << i for i, r in enumerate(support)) for j in columns]
    return ' '.join(map(str, blocks)).encode(), columns, support


def in_left_labels(rows, first, order):
    return sorted(sum(((r >> j) & 1) << i for i, j in enumerate(order)) |
                  (((r >> first) & 1) << 16) for r in rows)


def positive_controls(binary, heavy):
    # A control independent of the heavy census. Removing entries from the
    # 193 witness preserves avoidance. Keep the entries of both marked columns.
    square = read_witness(ROOT / 'z21-k33/witness-193.txt', 21, 21, 193)
    keep = [j for j in range(21) if j not in (3, 5, 8, 10)]
    rows = [sum(((r >> j) & 1) << i for i, j in enumerate(keep)) for r in square]
    a, b = 4, 12
    marks = (1 << a) | (1 << b)
    for i, r in enumerate(rows):
        if r & marks:
            while rows[i].bit_count() > 8 - int(i in (3, 13)):
                available = rows[i] & ~marks
                rows[i] ^= available & -available
    assert admissible(rows)
    first, order, inside = rooted(rows, a)
    second, other_order, other = rooted(rows, b, shuffle=True)
    overlap = len(set(inside) & set(other))
    expected = in_left_labels([rows[i] for i in sorted(set(inside) | set(other))], a, order)
    lines = run([binary, str(overlap), '0', '1', '--unions'],
                input=first + b'\n' + second + b'\n', capture_output=True, check=True).stdout.splitlines()
    success = False
    for line in lines[:-1]:
        tag, left, peer, right, back, *data = line.split()
        union = sorted(map(int, data))
        assert tag == b'union' and admissible(union)
        if (int(left), int(peer), int(right), int(back)) == (0, order.index(b), 1, other_order.index(a)):
            success |= union == expected
    assert lines[-1].startswith(b'counts ') and success

    # Feed only two projections of the certified 155 matrix to the full search.
    # This exercises both the join and the missing-row search.
    cols = transpose(heavy, 17)
    good = [j for j, c in enumerate(cols) if c.bit_count() == 9 and
            sum(8-heavy[i].bit_count() for i in range(20) if c >> i & 1) == 1]
    a, b = good[:2]
    first, order, inside = rooted(heavy, a)
    second, _, other = rooted(heavy, b, shuffle=True)
    overlap = len(set(inside) & set(other))
    lines = run([binary, str(overlap), '0', '1'], input=first + b'\n' + second + b'\n',
                capture_output=True, check=True).stdout.splitlines()
    expected = in_left_labels(heavy, a, order)
    assert any(sorted(map(int, line.split()[1:])) == expected for line in lines if line.startswith(b'heavy '))


def check_obstruction(rows):
    assert len(rows) == 20 and all(0 <= r < 1 << 17 for r in rows)
    assert sum(r.bit_count() for r in rows) == 155 and admissible(rows)
    assert sorted(r.bit_count() for r in rows) == [7]*5 + [8]*15
    cols = transpose(rows, 17)
    assert sorted(c.bit_count() for c in cols) == [9]*15 + [10]*2
    first, second = [c for c in cols if c.bit_count() == 10]
    sevens = sum(1 << i for i, r in enumerate(rows) if r.bit_count() == 7)
    assert first & second == sevens


def check_eight_subsets(rows):
    pairs = sorted({a & b for a, b in combinations(transpose(rows, 17), 2)
                    if (a & b).bit_count() >= 3}, key=int.bit_count, reverse=True)
    for weight, count in ((8, 0), (7, 5)):
        supports = (sum(1 << i for i in group) for group in combinations(range(20), weight))
        assert sum(all((p & s).bit_count() <= 2 for p in pairs) for s in supports) == count


def check_catalogue(entries, tmp):
    # A second generator starts from the empty block multiset and adds blocks
    # one at a time. It uses the same nauty labelling convention.
    small = compile_cpp(ROOT / 'z18x19-k33/small_points.cpp', tmp, True)
    alternative = set()
    for line in catalogue(small, 9, 62, 16, 6):
        blocks = tuple(map(int, line.split()))
        if sum(b.bit_count() for b in blocks) != 62:
            continue
        loads = [sum((b >> i) & 1 for b in blocks) for i in range(9)]
        if max(loads) == 7:
            alternative.add(blocks)
    assert {tuple(map(int, line.split())) for line in entries} == alternative
    assert len(alternative) == 4018


def main(jobs, chosen):
    heavy = read_witness(HERE / 'heavy-155.txt', 20, 17, 155)
    check_obstruction(heavy)
    check_eight_subsets(heavy)
    with TemporaryDirectory(prefix='z20x21-join-') as directory:
        tmp = Path(directory)
        binary = compile_cpp(HERE / 'join_nines.cpp', tmp)
        positive_controls(binary, heavy)
        generator = compile_cpp(ROOT / 'z16x17-k33/catalogue.cpp', tmp, True)
        entries = []
        for line in catalogue(generator, 16, 62, 1, 6, 7):
            blocks = tuple(map(int, line.split()))
            if sum(x.bit_count() for x in blocks) != 62:
                continue
            assert len(blocks) == 16 and all(2 <= x.bit_count() <= 5 for x in blocks)
            entries.append(line)
        assert len(entries) == 4018
        check_catalogue(entries, tmp)
        data = b'\n'.join(entries) + b'\n'
        with ThreadPoolExecutor(jobs) as workers:
            for overlap in chosen:
                def shard(first):
                    last = min(len(entries), first + 128)
                    lines = run([binary, *map(str, (overlap, first, last))], input=data,
                                capture_output=True, check=True).stdout.splitlines()
                    tag, aligns, unions, cores = lines.pop().split()
                    assert tag == b'counts' and int(cores) == len(lines)
                    found = set()
                    for line in lines:
                        tag, *words = line.split()
                        assert tag == b'heavy'
                        rows = tuple(sorted(map(int, words)))
                        check_obstruction(rows)
                        found.add(rows)
                    return int(aligns), int(unions), int(cores), found

                parts = list(workers.map(shard, range(0, len(entries), 128)))
                aligns, unions, cores = (sum(p[i] for p in parts) for i in range(3))
                found = set.union(*(p[3] for p in parts))
                assert (unions, cores) == EXPECTED[overlap], (overlap, unions, cores)
                if found:
                    assert found == {tuple(sorted(heavy))}
                print(f'Overlap {overlap}: {aligns:,} alignments, {unions:,} joined projections, '
                      f'{cores} completions.', flush=True)
    if set(chosen) == set(range(2, 6)):
        print('The (4, 15, 2) column profile is excluded at 187.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--overlap', nargs='+', type=int, choices=range(2, 6), default=range(2, 6))
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and specify a positive job count')
    main(args.jobs, args.overlap)
