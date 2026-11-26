"""Independently finish the two surviving marked projections and verify the lower bound."""
from collections import Counter
from itertools import combinations
from pathlib import Path

# A column has been marked and placed at bit 16. These are its nine incident
# rows. Derived from the two survivors printed by audit_core_catalogue --show.
PREFIXES = [
    [76947, 78435, 82261, 84493, 71081, 99894, 104646, 123128, 130816],
    [76947, 78435, 82709, 84045, 71081, 99894, 104646, 123128, 130816],
]


def finish(prefix):
    pairs = [a & b for a,b in combinations(prefix, 2)]
    allowed = [m for m in range(1 << 16) if 7 <= m.bit_count() <= 9
               and all((m & p).bit_count() <= 2 for p in pairs)]
    allowed.sort(key=int.bit_count, reverse=True)
    counts = Counter()

    def visit(rows, pool, n, weight):
        if not n:
            if weight:
                return
            # Test all possible extra rows, even for a core that would fail
            # a degree restriction.
            pairs = [a & b for a,b in combinations(rows, 2)]
            largest = max(m.bit_count() for m in range(1 << 17)
                          if all((m & p).bit_count() <= 2 for p in pairs))
            counts[largest] += 1
            return
        for i, x in enumerate(pool):
            if len(pool)-i < n or sum(m.bit_count() for m in pool[i:i+n]) < weight:
                break
            if x.bit_count() + 7*(n-1) > weight:
                continue
            choices = [y for y in pool[i+1:] if all((x & y & r).bit_count() <= 2 for r in rows)]
            visit(rows + [x], choices, n-1, weight-x.bit_count())

    visit(prefix, allowed, 7, 132-sum(r.bit_count() for r in prefix))
    return counts


def lower_bound(filename):
    lines = Path(__file__).with_name(filename).read_text().splitlines()
    assert len(lines) == 17 and all(len(r) == 17 and set(r) <= {'0','1'} for r in lines)
    assert sum(r.count('1') for r in lines) == 138
    triples = list(combinations(range(17), 3))
    for a,b,c in triples:
        common = [lines[a][j] == lines[b][j] == lines[c][j] == '1' for j in range(17)]
        assert not any(common[i] and common[j] and common[k] for i,j,k in triples)
    print(f'{filename}: 138 ones, all {len(triples)**2:,} choices of a 3 by 3 checked')


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run with Python assertions enabled')
    lower_bound('witness-138.txt')
    lower_bound('witness-138-six.txt')
    for p in PREFIXES:
        result = finish(p)
        assert result and max(result) < 7
        print('Largest appendable row sizes and counts of cores:', sorted(result.items()))
