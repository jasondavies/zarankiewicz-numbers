"""Exclude nine columns of degree eight at weight 209 on 21 x 23."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb, prod

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, hstack

N = 14
TARGET = 137


def column_tags(rows):
    return tuple(sum(((row >> j) & 1) << i for i, row in enumerate(rows))
                 for j in range(N))


@lru_cache(None)
def tag_permutations(k):
    tags = np.arange(1 << k)
    return np.array([sum(((tags >> i) & 1) << j for j, i in enumerate(order))
                     for order in permutations(range(k))], dtype=np.uint8)


def layout_key(rows):
    # Equal keys give a simultaneous row permutation and column permutation.
    tags = column_tags(rows)
    if len(rows) > 6:
        return bytes(sorted(tags))  # Keeping the row order can only duplicate work.
    images = np.sort(tag_permutations(len(rows))[:, tags], axis=1)
    return min(map(bytes, images))


def groups_of(rows):
    tags = column_tags(rows)
    return [tuple(i for i, t in enumerate(tags) if t == tag) for tag in sorted(set(tags))]


def row_options(rows, groups):
    """One representative for each count vector within the identical-column groups."""
    prefixes = [[sum(1 << j for j in g[:i]) for i in range(len(g) + 1)]
                for g in groups]
    pairs = [a & b for a, b in combinations(rows, 2)]
    masks, vectors = [], []
    for v in product(*(range(len(p)) for p in prefixes)):
        if sum(v) > 10:
            continue
        mask = sum(p[i] for p, i in zip(prefixes, v))
        if any((r & mask).bit_count() > 5 for r in rows):
            continue
        if any((p & mask).bit_count() > 2 for p in pairs):
            continue
        masks.append(mask)
        vectors.append(v)
    return masks, np.array(vectors, dtype=np.int64)


def choose(x, k):
    if k == 1:
        return x
    if k == 2:
        return x * (x - 1) // 2
    return x * (x - 1) * (x - 2) // 6


def high_bound(rows, groups, counts):
    sizes = list(map(len, groups))
    fixed = np.array([[len(g) * ((r >> g[0]) & 1) for g in groups] for r in rows])
    # Each group has total degree at least nine times its size.
    features = list(-counts.T)
    capacities = list(fixed.sum(axis=0) - 9 * np.array(sizes))
    for indices in combinations_with_replacement(range(len(groups)), 3):
        pattern = Counter(indices)
        triples = prod(comb(sizes[j], v) for j, v in pattern.items())
        if not triples:
            continue
        feature = prod(choose(counts[:, j], v) for j, v in pattern.items())
        if not feature.any():
            continue
        occupied = prod(choose(fixed[:, j], v) for j, v in pattern.items()).sum()
        features.append(feature)
        capacities.append(2 * triples - occupied)

    A, b = np.array(features), np.array(capacities)
    degree = counts.sum(axis=1)
    remaining = 21 - len(rows)
    # A penalized slack keeps the optimization feasible. Only the nonnegative
    # integer prices derived below are used to exclude a layout.
    constraints = hstack((csr_matrix(A), -np.ones((len(b), 1))), format="csr")
    fit = linprog(np.r_[-degree, 32], A_ub=constraints, b_ub=b,
                  A_eq=[np.r_[np.ones(len(degree)), 0]], b_eq=[remaining])
    if not fit.success:
        raise RuntimeError(fit.message)
    scale = 100_000
    prices = np.maximum(0, np.rint(-fit.ineqlin.marginals * scale)).astype(np.int64)
    # Bound every integer dot product before using fixed-width arithmetic.
    price_sum = sum(map(int, prices))
    magnitude = max(int(np.abs(A).max()), int(np.abs(b).max()), 1)
    if (remaining + 1) * (price_sum * magnitude + scale * 10) >= 2**63:
        raise ArithmeticError("Integer certificate exceeds int64")
    intercept = int((scale * degree - prices @ A).max())
    return sum(map(int.bit_count, rows)) + (int(prices @ b) + remaining * intercept) // scale


def degree_cap(deficits):
    # Discard the largest c-11 deficits to obtain the least deficient eleven.
    ordered = sorted(deficits, reverse=True)
    degree = 10
    while sum(ordered[degree - 10:]) >= 5:
        degree += 1
    return degree


def high_profiles(rows, groups):
    # The 14 high columns have 11 units of excess above nine.
    choices = []
    for g in groups:
        cap = degree_cap([10 - r.bit_count() for r in rows if r & (1 << g[0])])
        choices.append(list(combinations_with_replacement(range(cap - 8), len(g))))
    output = []
    def visit(i, excess, prefix):
        if i == len(groups):
            if excess == 0:
                output.append(prefix.copy())
            return
        for pattern in choices[i]:
            used = sum(pattern)
            if used <= excess:
                for j, v in zip(groups[i], pattern):
                    prefix[j] = 9 + v
                visit(i + 1, excess - used, prefix)
    visit(0, 11, [9] * N)
    return np.array(output, dtype=np.int16).reshape(-1, N)


def possible_degrees(rows, groups):
    """Can exactly these short rows occur? Apply necessary degree and crop tests."""
    profiles = high_profiles(rows, groups)
    fixed = np.array([[(r >> j) & 1 for j in range(N)] for r in rows], dtype=np.int16)
    for r in fixed:
        profiles = profiles[np.any(profiles[:, r == 0] > 10, axis=1)]
    for a, b in combinations(fixed, 2):
        # Each of the other 19 rows meets the common columns at most twice.
        profiles = profiles[(profiles[:, (a & b) == 1] - 2).sum(axis=1) <= 38]
    if len(profiles) == 0:
        return False
    high_sizes = fixed.sum(axis=1)
    for low in product(*(range(10 - d) for d in high_sizes)):
        degrees = high_sizes + low
        deficit = 10 - degrees
        if sum(deficit) < 7:
            continue
        caps = [degree_cap(deficit[col == 1]) for col in fixed.T]
        active = profiles[np.all(profiles <= caps, axis=1)]
        for i, j in combinations(range(len(rows)), 2):
            # Delete these rows and the two lightest remaining columns.
            # A row pair hits at most two low columns. Spreading two hits
            # maximizes the sum of the two lightest residual degrees.
            hits = low[i] + low[j]
            light_pair = ([8, 8], [7, 8], [7, 7])[hits]
            light = np.broadcast_to(light_pair, (len(active), 2))
            residuals = np.column_stack((active - fixed[i] - fixed[j], light))
            cheapest = np.partition(residuals, 1, axis=1)[:, :2].sum(axis=1)
            active = active[209 - degrees[i] - degrees[j] - cheapest <= 177]
            if len(active) == 0:
                break
        if len(active):
            return True
    return False


def main():
    layouts = {(degree,): ((1 << degree) - 1,) for degree in (8, 9)}
    while layouts:
        next_layouts = {}
        survivors = exact = 0
        k = len(next(iter(layouts.values())))
        for rows in layouts.values():
            groups = groups_of(rows)
            masks, counts = row_options(rows, groups)
            if k >= 3 and high_bound(rows, groups, counts) < TARGET:
                continue
            survivors += 1
            if k >= 4 and possible_degrees(rows, groups):
                exact += 1
                print("Unexcluded exact short-row set", rows, flush=True)
            for mask in masks:
                if 8 <= mask.bit_count() <= 9:
                    child = (*rows, mask)
                    next_layouts.setdefault(layout_key(child), child)
        detail = f", {exact} pass exact short-row tests" if k >= 4 else ""
        print(f"{k} rows: {len(layouts)} layouts, {survivors} retained{detail}", flush=True)
        if exact:
            raise RuntimeError("The endpoint is still open in this replay.")
        layouts = next_layouts
    print("Excluded nine eight-columns at weight 209.")


if __name__ == "__main__":
    main()
