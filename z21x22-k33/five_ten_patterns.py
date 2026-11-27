"""Enumerate the five degree-ten columns of a 185-one candidate with no eight-column."""
from argparse import ArgumentParser
from itertools import permutations


def short_rows(misses):
    rows = [(7, 31)] if len(misses) == 2 else []
    start = 0
    for count in misses:
        rows.append((8, 31 ^ (((1 << count) - 1) << start)))
        start += count
    return rows


def column_group(short):
    for permutation in permutations(range(5)):
        transform = tuple(sum(((mask >> i) & 1) << j for i, j in enumerate(permutation))
                          for mask in range(32))
        if sorted((d, transform[m]) for d, m in short) == sorted(short):
            yield transform


def enumerate_patterns(short):
    group = list(column_group(short))
    residual = {}
    for mask in range(1, 32):
        size = mask.bit_count()
        if size <= 3:
            residual[mask] = (10, 5, 2)[size-1] - sum((v & mask) == mask for _, v in short)
    types = sorted((m for m in range(1,32) if m.bit_count()>=2),
                   key=int.bit_count, reverse=True)
    costs = {m:tuple(s for s in residual if (m & s) == s) for m in types}
    types = [m for m in types if min(residual[s] for s in costs[m]) > 0]
    values = [0] * 32
    seen = set()

    def choose(index, rows_left):
        total = sum(residual[1 << i] for i in range(5))
        if index == len(types):
            if total <= rows_left:
                values[0] = rows_left-total
                for i in range(5):
                    values[1 << i] = residual[1 << i]
                key = min(bytes(values[m] for m in transform) for transform in group)
                if key not in seen:
                    seen.add(key)
                    yield key
            return
        mask = types[index]
        if total > rows_left * mask.bit_count():
            return
        affected = costs[mask]
        maximum = min(rows_left, *(residual[m] for m in affected))
        for count in range(maximum+1):
            values[mask] = count
            yield from choose(index+1, rows_left-count)
            if count < maximum:
                for m in affected:
                    residual[m] -= 1
        for m in affected:
            residual[m] += maximum
        values[mask] = 0

    yield from choose(0, 21-len(short))


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--emit',action='store_true',help='print the high-column masks of all 21 rows')
    args = parser.parse_args()
    cases = [((1,1,1,1),381), ((2,1,1,1),5780), ((2,2,1,0),566),
             ((1,4),95), ((2,3),8372), ((1,3),1122), ((2,2),9513), ((1,2),1550)]
    for misses,expected in cases:
        short = short_rows(misses)
        n = 0
        for pattern in enumerate_patterns(short):
            n += 1
            if args.emit:
                print(*(m for _,m in short),*(m for m,k in enumerate(pattern) for _ in range(k)))
        if n != expected:
            raise RuntimeError((misses,n,expected))
        if not args.emit:
            print(misses,n,flush=True)
