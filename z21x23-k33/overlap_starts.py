"""Four-column starts with two common rows, and the five-row refinement."""
from functools import lru_cache
from itertools import combinations, permutations
from four_columns import PAIRS, patterns

EDGES = tuple(combinations(range(5), 2))
TYPES = tuple(1 << j for j in range(5)) + tuple((1 << i) | (1 << j) for i, j in EDGES)
ROW_PAIR = tuple(combinations(range(3), 2))


def excluded_by_count(start):
    """Two size-three groups incident to the same marked column."""
    triples = [pair for pair in PAIRS if start[pair] == 3]
    return any(a & b for a, b in combinations(triples, 2))


@lru_cache(maxsize=1)
def double_starts():
    return [start for start in patterns() if start[15] == 2]


@lru_cache(maxsize=1)
def five_templates():
    # The first two rows meet all four marked columns. The next three meet
    # the chosen pair. Independent permutations of these two row sets are safe.
    orders = []
    for first in permutations(range(2)):
        for last in permutations(range(2, 5)):
            perm = first + last
            orders.append([1 << v for v in perm] +
                          [(1 << perm[i]) | (1 << perm[j]) for i, j in EDGES])
    answers = set()

    def fill(degrees, single, at, counts):
        if at == len(EDGES):
            if any(degrees):
                return
            a = [0] * 32
            if single is not None:
                a[1 << single] = 1
            for mask, n in zip(TYPES[5:], counts):
                a[mask] = n
            answers.add(min(tuple(a[m] for m in order) for order in orders))
            return
        i, j = EDGES[at]
        for n in range(min(degrees[i], degrees[j], 2 if at == 0 else 4) + 1):
            if j == 4 and degrees[i] != n:
                continue
            remaining = degrees.copy()
            remaining[i] -= n
            remaining[j] -= n
            fill(remaining, single, at + 1, counts + (n,))

    for a, b in ((7, 6), (8, 6), (7, 7)):
        for tail in ([8, 8, 8], [9, 8, 8]):
            d = [a, b] + tail
            if sum(d) > 38:
                continue
            for singleton in range(5) if sum(d) == 37 else (None,):
                left = d.copy()
                if singleton is not None:
                    left[singleton] -= 1
                fill(left, singleton, 0, ())
    return sorted(answers)


def fits_three(counts, prefix, other):
    """Can the three rows on one side each take at least eight further ones?"""
    # Each of the three rows shares one marked column with all five fixed rows.
    # Its intersections with those five rows limit it to one cell per edge type.
    forbidden = 0
    for k, (r, s) in enumerate(ROW_PAIR):
        for f, mask in enumerate(prefix):
            if (other[r] & other[s] & mask).bit_count() == 2:
                forbidden |= 1 << (5 * k + f)
    triple_used = (other[0] & other[1] & other[2]).bit_count() == 2
    need = [8] * 3
    groups = []
    for vertices, n in zip(TYPES, counts):
        if not n:
            continue
        shared = 15
        for f in range(5):
            if vertices >> f & 1:
                shared &= prefix[f]
        allowed = sum(1 << j for j, mask in enumerate(other)
                      if vertices.bit_count() == 1 or (shared & mask).bit_count() < 2)
        if n >= allowed.bit_count():
            for j in range(3):
                need[j] -= (allowed >> j) & 1
            continue
        options = []
        # Distinct positions within a type are interchangeable. Use the
        # fewest collisions possible for each choice of participating rows.
        for selected in range(7, -1, -1):
            if selected & ~allowed:
                continue
            if selected.bit_count() <= n:
                options.append((selected, 0, False))
            elif n == 2:
                options.extend((selected, vertices << (5 * k), False) for k in range(3))
            else:
                collisions = sum(vertices << (5 * k) for k, (r, s) in enumerate(ROW_PAIR)
                                 if selected >> r & selected >> s & 1)
                options.append((selected, collisions, selected == 7))
        groups.append((n, allowed, options))
    groups.sort(key=lambda x: x[0])
    available = [[sum(g[1] >> r & 1 for g in groups[i:]) for r in range(3)]
                 for i in range(len(groups) + 1)]

    def visit(i, needs, used, triple):
        if max(needs) <= 0:
            return True
        if any(n > a for n, a in zip(needs, available[i])):
            return False
        for selected, colliding, three in groups[i][2]:
            if used & colliding or triple and three:
                continue
            new_needs = tuple(n - ((selected >> r) & 1) for r, n in enumerate(needs))
            if visit(i + 1, new_needs, used | colliding, triple or three):
                return True
        return False

    return visit(0, need, forbidden, triple_used)


def refine(start):
    pair = next(m for m in PAIRS if start[m] == 3)
    prefix = (15, 15, pair, pair, pair)
    rows = [m for m, n in enumerate(start) for _ in range(n)]
    sides = [[m for m in rows if m & pair == bit] for bit in (1, 2, 4, 8) if bit & pair]
    assert all(len(side) == 3 for side in sides)
    return [i for i, t in enumerate(five_templates())
            if all(fits_three(t, prefix, side) for side in sides)]


if __name__ == '__main__':
    starts = double_starts()
    assert len(starts) == 143 and sum(map(excluded_by_count, starts)) == 20
    leaves = refine(starts[4])
    assert len(five_templates()) == 892 and len(leaves) == 92
    print('20 of 143 starts excluded by counting. Start 4 has 92 of 892 five-row templates left.')
