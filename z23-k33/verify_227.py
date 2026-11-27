"""Exclude 227 ones in a 23 by 23 K3,3-free binary matrix."""
from functools import cache
from itertools import combinations, combinations_with_replacement, product
from math import comb
from pathlib import Path


def profiles(a):
    # Erasing two nine-rows gives a 209-one rectangle with no eight-rows.
    deficit = a - 2
    for twelves, thirteens in product(range(4), range(3)):
        elevens = a - 3 - 2*twelves - 3*thirteens
        tens = 23 - a - elevens - twelves - thirteens
        if min(tens, elevens) < 0:
            continue
        f = deficit + twelves + 3*thirteens
        permitted = tuple(q for q, lo, hi in ((4, 4, 6), (5, 5, 7))
                          if lo <= deficit <= hi and 2*f <= 3*q+3 and
                          (not thirteens or q >= 5))
        if permitted:
            yield (a, tens, elevens, twelves, thirteens), permitted


@cache
def ten_sizes(a, count, floor, budget):
    if count == 0:
        return ((),)
    return tuple((k,) + tail for k in range(floor, a+1) if count*comb(k, 3) <= budget
                 for tail in ten_sizes(a, count-1, k, budget-comb(k, 3)))


@cache
def spectra(a, columns, permitted, matched):
    _, tens, elevens, twelves, thirteens = columns
    options = set()
    for sizes in ten_sizes(a, tens, 3, comb(a, 3)):
        low_pairs = sum(comb(k, 2) for k in sizes) + (a-1)*matched
        if not min(permitted)*comb(a, 2) <= low_pairs <= max(permitted)*comb(a, 2):
            continue
        for big in product(*(combinations_with_replacement(range(d-6, a+1), n)
                             for d, n in ((11, elevens), (12, twelves), (13, thirteens)))):
            longer = sum(big, ())
            total = sizes + longer
            if sum(total) == 9*a-matched and sum(comb(k, 3) for k in total) <= 2*comb(a, 3):
                options.add((sizes, tuple(sorted(longer))))
    return options


def cases():
    candidates = set()
    profiles_by_side = [item for a in range(6, 10) for item in profiles(a)]
    for (rows, qr), (columns, qc) in product(profiles_by_side, repeat=2):
        a, b = rows[0], columns[0]
        for matched in range(min(a, b)+1):
            if spectra(b, rows, qc, matched):
                for sizes, longer in spectra(a, columns, qr, matched):
                    candidates.add((a, b, matched, qr, sizes, longer))
    return candidates


@cache
def tables(a):
    triples = [sum(1 << i for i in points) for points in combinations(range(a), 3)]
    coverage = [sum(1 << i for i, t in enumerate(triples) if x & t == t)
                for x in range(1 << a)]
    by_size = [tuple(x for x in range(1 << a) if x.bit_count() == k) for k in range(a+1)]
    return coverage, by_size


def fits(case):
    a, b, matched, permitted, sizes, longer = case
    coverage, by_size = tables(a)
    sizes, longer = sorted(sizes, reverse=True), sorted(longer, reverse=True)
    # On k common nine-rows the two columns supply 2k, nine-columns supply
    # at most k altogether, and each other column supplies at most two.
    pair_cap = (42-2*b)//6
    def complete(big, tens):
        loads = [sum(x >> i & 1 for x in big+tens) for i in range(a)]
        if sorted(loads) != [8]*matched + [9]*(a-matched):
            return False
        for i, j in combinations(range(a), 2):
            bits = (1 << i) | (1 << j)
            q = (loads[i] == 8) + (loads[j] == 8) + sum(x & bits == bits for x in tens)
            if q not in permitted:
                return False
        return True

    def add_tens(big, pool, tens, occupied, first):
        i = len(tens)
        if i == len(sizes):
            return complete(big, tens)
        k = sizes[i]
        for j in range(first, len(pool[k])):
            x = pool[k][j]
            if not occupied & coverage[x]:
                start = j+1 if i+1 < len(sizes) and sizes[i+1] == k else 0
                if add_tens(big, pool, tens+[x], occupied | coverage[x], start):
                    return True
        return False

    def add_large(big, once, twice):
        if len(big) == len(longer):
            pool = {k: [x for x in by_size[k] if not coverage[x] & twice and
                        all((x & y).bit_count() <= pair_cap for y in big)] for k in set(sizes)}
            if any(len(pool[k]) < sizes.count(k) for k in pool):
                return False
            return add_tens(big, pool, [], 0, 0)
        # Points with identical histories are interchangeable at this stage.
        groups = {}
        for i in range(a):
            groups.setdefault(tuple(x >> i & 1 for x in big), []).append(i)
        for x in by_size[longer[len(big)]]:
            if coverage[x] & twice or any((x & y).bit_count() > pair_cap for y in big):
                continue
            if any(any(not (x >> i & 1) and (x >> j & 1) for i, j in zip(g, g[1:]))
                   for g in groups.values()):
                continue
            if add_large(big+[x], once | coverage[x], twice | (once & coverage[x])):
                return True
        return False
    return add_large([], 0, 0)


def check_witness():
    lines = Path(__file__).with_name('witness-225.txt').read_text().splitlines()
    assert len(lines) == 23 and all(len(s) == 23 and set(s) <= {'0', '1'} for s in lines)
    rows = [int(s, 2) for s in lines]
    assert sum(x.bit_count() for x in rows) == 225
    assert max((x & y & z).bit_count() for x, y, z in combinations(rows, 3)) <= 2


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('enable assertions for verification')
    check_witness()
    # The seven Fano lines and their complements supply the ten-blocks.
    # One full block gives every point load eight.
    assert fits((7, 7, 7, (5,), (3,)*7 + (4,)*7, (7,)))
    remaining = cases()
    assert len(remaining) == 68
    for case in sorted(remaining):
        assert not fits(case), case
    print('Verified the 225-one witness and excluded all 68 spectra at 227.')
