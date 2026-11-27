"""SAT completion of a 21 by 23 start, optionally fixing several entire rows."""
import argparse
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations, groupby, permutations, product
import json
from pathlib import Path
from threading import Timer
from time import monotonic, process_time

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Glucose4

from overlap_starts import PAIRS, TYPES, double_starts, five_templates, refine


class Encoding:
    def __init__(self, n, width):
        self.pool = IDPool()
        self.x = [[self.pool.id() for _ in range(width)] for _ in range(n)]
        self.clauses = []

    def cardinality(self, cells, bound, minimum=False):
        if minimum and bound <= 0 or not minimum and bound >= len(cells):
            return
        if bound < 0 or bound > len(cells):
            self.clauses.append([])
            return
        encode = CardEnc.atleast if minimum else CardEnc.atmost
        kind = EncType.seqcounter if len(cells) < 100 else EncType.cardnetwrk
        self.clauses.extend(encode(cells, bound, vpool=self.pool, encoding=kind).clauses)

    def order(self, a, b):
        # Prefix equality forces the next pair of bits to be in descending order.
        prefix = []
        for k, (u, v) in enumerate(zip(a, b)):
            self.clauses.append(prefix + [u, -v])
            if k + 1 < len(a):
                equal = self.pool.id()
                self.clauses.extend((prefix + [u, v, equal], prefix + [-u, -v, equal]))
                prefix = [-equal]

    def intersections(self, a, b):
        y = [self.pool.id() for _ in a]
        self.clauses.extend([[-u, -v, z] for u, v, z in zip(a, b, y)])
        return y


def direct(prefix, width, weight, target=True):
    enc = Encoding(len(prefix), width)
    x, cap = enc.x, enc.cardinality
    cols = list(zip(*x))
    for a, b in zip(cols, cols[1:]):
        enc.order(a, b)
    for i in range(1, len(x)):
        if prefix[i] == prefix[i-1]:
            enc.order(x[i-1], x[i])
    cap(sum(x, []), weight, True)
    if target:
        for mask, row in zip(prefix, x):
            cap(row, 6 if mask == 15 else 8, True)
        cap([v for m, row in zip(prefix, x) if m == 15 for v in row], 13, True)
        for col in cols:
            cap(col, 8, True)
    for i, j, k in combinations(range(len(x)), 3):
        left = 2 - (prefix[i] & prefix[j] & prefix[k]).bit_count()
        if left < 0:
            enc.clauses.append([])
            continue
        z = []
        for a, b, c in zip(x[i], x[j], x[k]):
            clause = [-a, -b, -c]
            if left:
                z.append(enc.pool.id())
                clause.append(z[-1])
            enc.clauses.append(clause)
        if left:
            cap(z, left)
    return enc


def initial_rows(start, template):
    pair = next(m for m in PAIRS if start[m] == 3)
    prefix = [15, 15, pair, pair, pair]
    prefix += [m for m, n in enumerate(start) if m not in (pair, 15) for _ in range(n)]
    columns = [m for m, n in zip(TYPES, template) for _ in range(n)]
    layouts = (tuple(sorted((tuple((m >> j) & 1 for j in a+b) for m in columns), reverse=True))
               for a in permutations(range(2)) for b in permutations(range(2, 5)))
    return prefix, list(zip(*max(layouts)))


def next_row(prefix, fixed):
    # Independent permutations inside each current column type put the new
    # row's ones first. Fixed rows always precede the unknown rows in this order.
    cut = len(fixed)
    groups = [(bits, len(list(g))) for bits, g in groupby(zip(*fixed))]
    candidates = []
    for mask in sorted(set(prefix[cut:])):
        limits = []
        for bits, count in groups:
            incident = [i for i, bit in enumerate(bits) if bit]
            limits.append(min([count] + [2 - (mask & prefix[i] & prefix[j]).bit_count()
                                         for i, j in combinations(incident, 2)]))
        cost = 1
        for lim in limits:
            cost *= lim + 1
        candidates.append((cost, mask, limits))
    _, mask, limits = min(candidates)
    tail = prefix[cut:].copy()
    tail.remove(mask)
    updated = prefix[:cut] + [mask] + tail
    for sig in product(*(range(k+1) for k in limits)):
        if sum(sig) < 8:
            continue
        if any(sum(k for k, (bits, _) in zip(sig, groups) if bits[i] and bits[j]) >
               2 - (mask & prefix[i] & prefix[j]).bit_count() for i, j in combinations(range(cut), 2)):
            continue
        row = tuple(bit for k, (_, count) in zip(sig, groups) for bit in [1]*k + [0]*(count-k))
        yield updated, fixed + [row]


def grouped_bounds(enc, rem, old, fixed, floors, weight):
    """Count incidences jointly over columns with the same fixed rows."""
    cols = list(zip(*fixed))
    row_totals = [[] for _ in rem]
    for bits, group in groupby(range(19), lambda j: cols[j]):
        js = list(group)
        hit = [f for f, bit in enumerate(bits) if bit]
        group_total = []
        for mask, row, total in zip(rem, enc.x, row_totals):
            limit = min([len(js)] + [2 - (mask & old[f] & old[g]).bit_count()
                                    for f, g in combinations(hit, 2)])
            cells = [row[j] for j in js]
            for h in range(1, limit+1):
                # z holds exactly when this row meets the group at least h times.
                if len(cells) == 1:
                    z = cells[0]
                else:
                    z = enc.pool.id()
                    for subset in combinations(cells, h):
                        enc.clauses.append([-v for v in subset] + [z])
                    for subset in combinations(cells, len(cells)-h+1):
                        enc.clauses.append([-z, *subset])
                total.append(z)
                group_total.append(z)
        enc.cardinality(group_total, len(js)*floors[js[0]], True)
    for total in row_totals:
        enc.cardinality(total, 8, True)
    enc.cardinality(sum(row_totals, []), weight, True)

    # Each chosen column through a fixed and a new row consumes triple
    # intersections with at least floor[j]-1 additional new rows.
    for i, (row, mask) in enumerate(zip(enc.x, rem)):
        for f, fixed_mask in enumerate(old):
            js = [j for j, bit in enumerate(fixed[f]) if bit]
            limit = sum(2 - (fixed_mask & mask & m).bit_count() for k, m in enumerate(rem) if k != i)
            for size in range(1, len(js)+1):
                for subset in combinations(js, size):
                    costs = [floors[j]-1 for j in subset]
                    cost = sum(costs)
                    if cost > limit >= cost - min(costs):
                        enc.clauses.append([-row[j] for j in subset])


def restricted(prefix, fixed, grouped=False):
    cut = len(fixed)
    old, rem = prefix[:cut], prefix[cut:]
    enc = Encoding(len(rem), 19)
    x, cap = enc.x, enc.cardinality
    cols = list(zip(*fixed))
    xt = list(zip(*x))
    degrees = [sum(row) for row in fixed]
    central = sum(degrees[:2])
    floors = [max(8 - sum(c), 21 - central - sum(c[2:])) for c in cols]
    cap(sum(x, []), 177-sum(degrees), True)
    for i, row in enumerate(x):
        cap(row, 8, True)
        if i and rem[i] == rem[i-1]:
            enc.order(x[i-1], row)
        for f, g in combinations(range(cut), 2):
            cap([row[j] for j, c in enumerate(cols) if c[f] and c[g]],
                2 - (rem[i] & old[f] & old[g]).bit_count())
    for j, c in enumerate(cols):
        cap(xt[j], floors[j], True)
        if j and cols[j-1] == c:
            enc.order(xt[j-1], xt[j])
        for bit in (1, 2, 4, 8):
            used = sum(degrees[f]-1 for f in range(cut) if c[f] and old[f] & bit)
            cap([row[j] for row, mask in zip(x, rem) if mask & bit], (36-used)//7)

    for bits, it in groupby(range(19), lambda j: cols[j]):
        js = list(it)
        hit = [f for f, bit in enumerate(bits) if bit]
        limits = [min([len(js)] + [2-(mask & old[f] & old[g]).bit_count()
                                  for f, g in combinations(hit, 2)]) for mask in rem]
        slack = sum(limits) - len(js)*floors[js[0]]
        if slack < 0:
            enc.clauses.append([])
            return enc
        for row, limit in zip(x, limits):
            cap([row[j] for j in js], limit-slack, True)

    for i, k in combinations(range(len(rem)), 2):
        common = rem[i] & rem[k]
        y = enc.intersections(x[i], x[k])
        cap(y, min(6-common.bit_count(), 5 if central == 13 else 6))
        for f, mask in enumerate(old):
            cap([v for v, bit in zip(y, fixed[f]) if bit], 2-(common & mask).bit_count())
        for l in range(k+1, len(rem)):
            left = 2-(common & rem[l]).bit_count()
            if not left:
                enc.clauses.extend([[-a, -b] for a, b in zip(y, x[l])])
            else:
                cap(enc.intersections(y, x[l]), left)
    for j, k in combinations(range(19), 2):
        hit = [f for f in range(cut) if cols[j][f] and cols[k][f]]
        y = enc.intersections(xt[j], xt[k])
        cap(y, min((34-sum(degrees[f]-2 for f in hit))//6, 5-sum(f >= 2 for f in hit)))
        for bit in (1, 2, 4, 8):
            cap([v for v, mask in zip(y, rem) if mask & bit], 2-sum(bool(old[f]&bit) for f in hit))
    if grouped:
        grouped_bounds(enc, rem, old, fixed, floors, 177-sum(degrees))
    return enc


def run(enc, prefix, fixed, width, weight, seconds):
    cpu, wall = process_time(), monotonic()
    with Glucose4(bootstrap_with=enc.clauses) as solver:
        timer = Timer(seconds, solver.interrupt)
        timer.start()
        try:
            answer = solver.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel()
            timer.join()
        result = dict(status={True:'SAT', False:'UNSAT', None:'UNKNOWN'}[answer],
                      cpu=round(process_time()-cpu, 3), wall=round(monotonic()-wall, 3))
        if answer:
            values = set(solver.get_model())
            masks = [sum(v << j for j, v in enumerate(row)) for row in fixed]
            masks += [sum((v in values) << j for j, v in enumerate(row)) for row in enc.x]
            assert sum(v.bit_count() for v in masks) >= weight
            assert len(masks) == len(prefix)
            board = [(a << width) | b for a, b in zip(prefix, masks)]
            assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(board, 3))
            result['rows'] = board
        return result


def solve_case(task):
    index, leaf, path, seconds, grouped, dimacs = task
    start = double_starts()[index]
    if leaf is None:
        prefix = [m for m in sorted(range(16), key=lambda m: (m != 15, m)) for _ in range(start[m])]
        fixed = []
        enc = direct(prefix, 19, 177)
    else:
        prefix, fixed = initial_rows(start, five_templates()[leaf])
        for j in path:
            prefix, fixed = list(next_row(prefix, fixed))[j]
        enc = restricted(prefix, fixed, grouped)
    if dimacs:
        CNF(from_clauses=enc.clauses).to_file(dimacs)
        return dict(start=index, template=leaf, path=path, dimacs=dimacs)
    return dict(start=index, template=leaf, path=path, **run(enc, prefix, fixed, 19, 177, seconds))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start', type=int, choices=range(143), metavar='0..142')
    refinement = parser.add_mutually_exclusive_group()
    refinement.add_argument('--refine', action='store_true', help='test every surviving five-row template')
    refinement.add_argument('--template', type=int, help='test one five-row template')
    split = parser.add_mutually_exclusive_group()
    split.add_argument('--sixth', type=int, help='select a single sixth-row placement within a template')
    split.add_argument('--split', action='store_true', help='split each selected template on another row')
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--seconds', type=float, default=2)
    parser.add_argument('--grouped', action='store_true', help='add redundant counts for each column type')
    parser.add_argument('--dimacs', metavar='FILE', help='export one selected instance for an external SAT solver')
    parser.add_argument('--control', action='store_true')
    args = parser.parse_args()
    if not __debug__ or args.seconds <= 0 or args.jobs < 1:
        parser.error('enable assertions and use positive budgets')
    if args.sixth is not None and (args.template is None or args.sixth < 0):
        parser.error('--sixth requires a nonnegative index and --template')
    if args.grouped and not (args.refine or args.template is not None):
        parser.error('--grouped requires a five-row search')
    if args.dimacs and (args.start is None or args.split or args.refine or args.control):
        parser.error('--dimacs requires a single selected instance')
    if args.control:
        root = Path(__file__).resolve().parent.parent
        rows = [int(s, 2) for s in (root/'z23-k33/witness-225.txt').read_text().splitlines()][2:]
        prefix = [s >> 4 for s in rows]
        target = sum((s & 15).bit_count() for s in rows)
        print(json.dumps(run(direct(prefix, 4, target, False), prefix, [], 4, target, args.seconds)))
        return
    if (args.refine or args.template is not None or args.split) and args.start is None:
        parser.error('specify a start for the five-row search')
    if args.split and not (args.refine or args.template is not None):
        parser.error('choose --refine or --template to split')
    jobs = []
    for i in range(143) if args.start is None else [args.start]:
        start = double_starts()[i]
        if (args.refine or args.template is not None) and not any(start[m] == 3 for m in PAIRS):
            parser.error('this start has no size-three group')
        leaves = refine(start) if args.refine else [args.template]
        if args.template is not None and args.template not in refine(start):
            parser.error('this template was excluded by the three-row test or is out of range')
        for h in leaves:
            paths = [()]
            if args.split or args.sixth is not None:
                pre, rows = initial_rows(start, five_templates()[h])
                paths = [(k,) for k, _ in enumerate(next_row(pre, rows))]
                if args.sixth is not None:
                    if args.sixth >= len(paths):
                        parser.error('sixth-row index exceeds number of placements')
                    paths = [paths[args.sixth]]
            jobs.extend((i, h, path, args.seconds, args.grouped, args.dimacs) for path in paths)
    with ProcessPoolExecutor(args.jobs) as pool:
        for result in pool.map(solve_case, jobs, chunksize=1):
            print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
