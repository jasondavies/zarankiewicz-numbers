"""Ten-point checks behind the degree bounds at weight 139 in marked-nine.md.

The 16 by 17 replay in ../z16x17-k33 also imports these routines.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path


def masks(n, k):
    return [sum(1 << p for p in t) for t in combinations(range(n), k)]


FIVES = masks(10, 5)
FOURS = masks(10, 4)


def next_fives(rows):
    # Permute columns with identical incidence in all previously selected rows.
    groups = {}
    for i in range(10):
        key = tuple(x >> i & 1 for x in rows)
        groups.setdefault(key, []).append(i)
    for x in FIVES:
        if any((x & r).bit_count() > 2 for r in rows):
            continue
        if all([x >> j & 1 for j in g] == sorted((x >> j & 1 for j in g), reverse=True)
               for g in groups.values()):
            yield x


def four_cliques(rows, size):
    pool = [v for v in FOURS if all((v & x).bit_count() <= 2 for x in rows)]
    neighbors = [sum(1 << j for j, b in enumerate(pool) if j > i and (a & b).bit_count() <= 2)
                 for i, a in enumerate(pool)]

    def visit(left, chosen):
        if len(chosen) == size:
            yield chosen
            return
        while len(chosen) + left.bit_count() >= size:
            bit = left & -left
            left ^= bit
            i = bit.bit_length() - 1
            yield from visit(left & neighbors[i], chosen + [pool[i]])

    yield from visit((1 << len(pool)) - 1, [])


def possible_fives(prefix):
    if len(prefix) >= 4:
        yield prefix
    if len(prefix) < 6:
        for x in next_fives(prefix):
            yield from possible_fives(prefix + [x])


def largest_inside_extension(rows):
    # Two rows on an additional column of the marked row may share at most
    # one old column, since they already share the additional column.
    def best(pool):
        return max((1 + best([s for s in pool[i + 1:] if (s & r).bit_count() <= 1])
                    for i, r in enumerate(pool)), default=0)
    return best(rows)


def check_128_core():
    # Collins et al. give uniqueness up to bipartite isomorphism. Test both
    # orientations of the leading square of our existing 137-one witness.
    path = Path(__file__).with_name('bordered-137.txt')
    rows = [int(s[:16], 2) for s in path.read_text().splitlines()[:16]]
    assert len(rows) == 16 and sum(x.bit_count() for x in rows) == 128
    assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(rows, 3))
    cols = [sum(((x >> j) & 1) << i for i, x in enumerate(rows)) for j in range(16)]
    for side in (rows, cols):
        pairs = [a & b for a, b in combinations(side, 2)]
        assert not any(all((x & p).bit_count() <= 2 for p in pairs) for x in masks(16, 5))


def main():
    check_128_core()
    checked = Counter()
    # Ten marked entries of a large row need at least 67 projected ones.
    # Exclude five or six five-sets, so the projected weight is at most 68.
    for f in possible_fives([]):
        m = len(f)
        # 5m + 4q + 3(16-m-q) = 48 + 2m + q.
        if m >= 5:
            assert next(four_cliques(f, 67 - 48 - 2*m), None) is None
    # Degree eleven: omit one seven. The projection has four five-sets, twelve
    # four-sets and loads 6, 6, 7, ..., 7. Restoring the omitted column needs six
    # rows meeting pairwise in at most one old point, but at most three exist.
    for f in possible_fives([]):
        if len(f) != 4:
            continue
        for q in four_cliques(f, 12):
            cols = [sum(((x >> j) & 1) << i for i, x in enumerate(f + q))
                    for j in range(10)]
            if sorted(c.bit_count() for c in cols) != [6, 6] + [7]*8:
                continue
            checked['ten-column cores'] += 1
            assert largest_inside_extension(f + q) == 3
    print(dict(checked))
    assert checked == {'ten-column cores': 120}


if __name__ == '__main__':
    main()
