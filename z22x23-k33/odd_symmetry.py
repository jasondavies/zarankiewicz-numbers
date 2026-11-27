"""Check necessary orbit counts for an odd-prime symmetry at weight 217."""
from functools import cache
from itertools import product
from math import comb


def triple_count(total, lines):
    quotient, remainder = divmod(total, lines)
    return (lines - remainder) * comb(quotient, 3) + remainder * comb(quotient + 1, 3)


@cache
def upper(rows, cols):
    if rows == 0 or cols == 0:
        return 0
    weight = rows * cols
    if rows > 1:
        weight = min(weight, rows * upper(rows - 1, cols) // (rows - 1))
    if cols > 1:
        weight = min(weight, cols * upper(rows, cols - 1) // (cols - 1))
    while (triple_count(weight, rows) > 2 * comb(cols, 3)
           or triple_count(weight, cols) > 2 * comb(rows, 3)):
        weight -= 1
    return weight


def fixed_lines(p, lines, opposite, orbits, exact_eights):
    # Process in descending degree inside the fixed submatrix, checking every prefix.
    # A state stores the last degree, fixed entries, incidences with opposite orbits,
    # full degree-eight lines, and consumed triples of opposite fixed positions.
    states = {(opposite, 0, 0, 0, 0)}
    for size in range(1, lines + 1):
        nxt = set()
        for last, weight, hits, eights, triples in states:
            for d in range(last + 1):
                used = triples + comb(d, 3)
                if weight + d > upper(size, opposite) or used > 2 * comb(opposite, 3):
                    continue
                for k in range(min(orbits, 2 * orbits - hits) + 1):
                    degree = d + p * k
                    if degree < 8:
                        continue
                    n = eights + (degree == 8) if exact_eights is not None else 0
                    if exact_eights is None or n <= exact_eights:
                        nxt.add((d, weight + d, hits + k, n, used))
        states = nxt
    return {(w, t) for _, w, t, e, _ in states if exact_eights is None or e == exact_eights}


def profiles(p, a, b):
    f, g = 22 - p * a, 23 - p * b
    # At most two fixed lines can meet each opposite moving orbit.
    r, c = max(0, f - 2 * b), max(0, g - 2 * a)
    if 8 * r > upper(r, g) or 8 * c > upper(c, f):
        return set()
    if max(6 * p * a, 7 * p * b) > upper(p * a, p * b):
        return set()
    row = fixed_lines(p, f, g, b, None)
    ans = set()
    for low in range(1, min(g, 2) + 1):
        col = fixed_lines(p, g, f, a, low)
        for h, w in row:
            if (217 - h) % p:
                continue
            for hc, z in col:
                if h != hc:
                    continue
                v = (217 - h) // p - w - z
                if (0 <= p * v <= upper(p * a, p * b)
                        and v + z >= 8 * a and v + w >= 9 * b):
                    ans.add((low, h, w, z, v))
    return ans


if __name__ == '__main__':
    for p in (3, 5, 7, 11, 13, 17, 19):
        print(p, [(22-p*a,23-p*b,len(q)) for a,b in product(range(1,22//p+1),
                  range(1,23//p+1)) if (q := profiles(p,a,b))])
