"""Enumerate four eight-one columns that can serve as the start of a 209-one matrix."""
import argparse
from collections import Counter
from itertools import permutations, product


PAIRS = (3, 5, 6, 9, 10, 12)
TRIPLES = (7, 11, 13, 14)
# Canonicalize the rarer row types first. Singleton and empty types are forced.
ORDER = (15,) + TRIPLES + PAIRS


def patterns():
    images = []
    for perm in permutations(range(4)):
        images.append(tuple(sum(1 << perm[j] for j in range(4) if m & (1 << j))
                            for m in ORDER))
    for quad in range(3):
        for triples in product(range(3 - quad), repeat=4):
            a = [0] * 16
            a[15] = quad
            for mask, value in zip(TRIPLES, triples):
                a[mask] = value
            # First fix the least ordering of the triple counts. Only its
            # stabilizer can still identify two pair-count vectors.
            prefix = (quad,) + triples
            if any(tuple(a[m] for m in image[:5]) < prefix for image in images):
                continue
            stabilizer = [image[5:] for image in images if tuple(a[m] for m in image[:5]) == prefix]
            domains = []
            for pair in PAIRS:
                triple_rows = sum(a[m] for m in TRIPLES if m & pair == pair)
                shared = quad + triple_rows
                # Two low columns share at most five rows. If they share five,
                # at least two more marked incidences are needed on those rows.
                limit = 5 if 2 * quad + triple_rows >= 2 else 4
                domains.append(range(limit - shared + 1))
            for pair_counts in product(*domains):
                for mask, value in zip(PAIRS, pair_counts):
                    a[mask] = value
                if any(tuple(a[m] for m in image) < pair_counts for image in stabilizer):
                    continue
                for col in (1, 2, 4, 8):
                    a[col] = 8 - sum(a[m] for m in ORDER if m & col)
                a[0] = 21 - sum(a[1:])
                if min(a) < 0:
                    continue
                # Choose the four columns to include at least three on a long row.
                # A pair whose shared rows already use its entire capacity cannot
                # contain that row, which needs at least eleven entries.
                tight = []
                for pair in PAIRS:
                    shared = sum(a[m] for m in ORDER if m & pair == pair)
                    other = sum((m.bit_count() - 2) * a[m] for m in ORDER if m & pair == pair)
                    if 8 * shared == 38 + other:
                        tight.append(pair)
                if any(a[m] and all(m & pair != pair for pair in tight)
                       for m in (15,) + TRIPLES):
                    yield tuple(a)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true', help='print row counts for masks 0 through 15')
    args = parser.parse_args()
    counts = Counter()
    for pattern in patterns():
        counts[pattern[15]] += 1
        if args.emit:
            print(*pattern)
    assert counts == {0: 4167, 1: 1374, 2: 143}
    if not args.emit:
        print(f'{sum(counts.values())} starts; by four-way intersection: {dict(sorted(counts.items()))}')
