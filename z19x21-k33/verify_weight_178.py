"""Search the three seven-column cases at weight 178 on 19 by 21."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from itertools import combinations_with_replacement
import os
from pathlib import Path
import re
from subprocess import run
import sys
from tempfile import NamedTemporaryFile, TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'z20x21-k33'))
from extend_178 import longest_extension
from extend_eights import admissible, legal_supports, transpose
from verify_bounds import compatible_groups
from verify_rare_rows import catalogue, compile_cpp, parse, projection, read_witness


def dense(generator, five, points, total):
    families = catalogue(five, points, total - 72)
    return run([generator, '18', '18', str(total), '7', str(points)],
               input=b'\n'.join(families) + b'\n', capture_output=True, check=True).stdout.splitlines()


def catalogues(small, five, generator, cases):
    eleven = dense(generator, five, 11, 78)
    assert len(eleven) == 4048
    for line in eleven:
        blocks = [b for b in parse(line) if b.bit_count() <= 4]
        assert next(compatible_groups(blocks, 7), None) is None
    high = [line for line in eleven if sum(b.bit_count() for b in parse(line)) >= 79]
    assert len(high) == 32 and not catalogue(small, 11, 80, 18, 7)
    ten = dense(generator, five, 10, 74)
    high_ten = [line for line in ten if sum(b.bit_count() for b in parse(line)) >= 75]
    nine = catalogue(small, 9, 69, 18, 7)
    assert (len(ten), len(high_ten), len(nine)) == (20250, 24, 67537)
    eight = catalogue(small, 8, 63 if 2 in cases else 64, 18, 7)
    regular, dense_eight, higher_eight = [], [], []
    for line in eight:
        blocks = parse(line)
        total = sum(b.bit_count() for b in blocks)
        if total >= 64:
            dense_eight.append(line)
            if total >= 65:
                higher_eight.append(line)
        elif all(sum((b >> j) & 1 for b in blocks) <= 8 for j in range(8)):
            regular.append(line)
    assert (len(dense_eight), len(higher_eight)) == (19363, 467)
    if 2 in cases:
        assert len(eight) == 547481 and len(regular) == 10057
    return nine, ten, high_ten, high, dense_eight, higher_eight, regular


def checked_matrix(words, goal, sevens):
    cols = tuple(map(int, words))
    assert len(cols) == 21 and all(0 <= c < 1 << 19 for c in cols)
    assert sum(c.bit_count() for c in cols) == goal and admissible(cols)
    assert sum(c.bit_count() == 7 for c in cols) == sevens
    rows = transpose(cols, 19)
    assert admissible(rows)
    return rows


def controls(solver):
    square = read_witness(ROOT / 'z21-k33/witness-193.txt', 21, 21, 193)
    rows = tuple(r for r in square if r.bit_count() != 8)
    stored = read_witness(ROOT / 'z19x21-k33/witness-177.txt', 19, 21, 177)
    assert rows == tuple(stored) and admissible(transpose(rows, 21))
    # Fix the column deletions and maximizing marks of six known satisfiable inputs.
    # Their order makes it quick to recover witnesses under the searcher's support order.
    tests = [((), 1, 14), ((), 2, 10), ((17,), 1, 3), ((19,), 2, 1),
             ((8, 11), 1, 11), ((8, 11), 2, 9)]
    for remove, alpha, mark in tests:
        s = len(remove)
        keep = [j for j in range(21) if j not in remove]
        core = tuple(sum(((r >> j) & 1) << h for h, j in enumerate(keep)) for r in rows)
        assert min(r.bit_count() for r in core) >= 8
        degree = [c.bit_count() for c in transpose(core, len(keep))]
        excess = [sum(d - 8 for j, d in enumerate(degree) if r >> j & 1) for r in core]
        goal = sum(r.bit_count() for r in core) + 7 * s
        scores = [alpha * r.bit_count() + w for r, w in zip(core, excess)]
        assert scores[mark] == max(scores)
        points, blocks = projection(core, len(keep), mark)
        requirement = max((w for r, w in zip(core, excess) if r.bit_count() == 8), default=-1)
        args = [s, len(points), goal, alpha, 0, 10000, 21, 19, 8, requirement]
        result = run([solver, *map(str, args)], input=' '.join(map(str, blocks)).encode() + b'\n',
                     capture_output=True, check=True).stdout.split()
        assert result[0] == b'solution'
        checked_matrix(result[1:], goal, s)
    print('Reconstructed and verified six control matrices.', flush=True)


class Witness(Exception):
    def __init__(self, rows):
        self.rows = rows


def check_exclusion(output, size, s):
    lines = output.splitlines()
    if not lines:
        raise RuntimeError('empty solver output')
    last = lines.pop()
    if last.startswith(b'solution '):
        raise Witness(checked_matrix(last.split()[1:], 178, s))
    match = re.fullmatch(rb'excluded (\d+) cores (\d+) profiles (\d+)', last)
    if not match or int(match[1]) != size or int(match[2]) != len(lines):
        raise RuntimeError(f'invalid batch result: {last!r}')
    for line in lines:
        tag, *words = line.split()
        cols = tuple(map(int, words))
        assert s and tag == b'core' and len(cols) == 21 - s
        assert all(0 <= c < 1 << 19 and c.bit_count() >= 8 for c in cols)
        assert sum(c.bit_count() for c in cols) == 178 - 7 * s and admissible(cols)
        supports = list(legal_supports(cols, 19, 7))
        if s == 1:
            assert not supports
        else:
            assert not any(all((a & b & c).bit_count() <= 2 for c in cols)
                           for a, b in combinations_with_replacement(supports, 2))
    return len(lines)


def search_family(solver, solver_id, parameters, entries, jobs, cache):
    s = parameters[0]
    # Small batches allow workers to share the hard projections evenly.
    parts = (len(entries) + 63) // 64

    def check(i):
        batch = entries[i::parts]
        data = b'\n'.join(batch) + b'\n'
        tail = [*map(str, parameters), '--emit-cores']
        record = None
        if cache:
            name = sha256(solver_id + ' '.join(tail).encode() + b'\n' + data).hexdigest()
            record = cache / name
        if record and record.is_file():
            return check_exclusion(record.read_bytes(), len(batch), s)
        out = run([solver, *tail], input=data, capture_output=True, check=True).stdout
        cores = check_exclusion(out, len(batch), s)
        if record:
            with NamedTemporaryFile(dir=cache, delete=False) as f:
                f.write(out)
            os.replace(f.name, record)
        return cores

    pool = ThreadPoolExecutor(max_workers=jobs)
    try:
        cores = sum(pool.map(check, range(parts)))
    finally:
        pool.shutdown(wait=True, cancel_futures=True)
    print(f's={s}, mark={parameters[1]}, multiplier={parameters[3]}: '
          f'{len(entries):,} projections excluded ({cores:,} completed cores).', flush=True)


def main(cases, jobs, cache):
    if cache:
        cache.mkdir(exist_ok=True, parents=True)
    with TemporaryDirectory(prefix='z178-') as tmp:
        tmp = Path(tmp)
        five = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
        dense_gen = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
        small = compile_cpp(ROOT / 'z18x19-k33/small_points.cpp', tmp, True)
        solver = compile_cpp(ROOT / 'z18x19-k33/marked_core.cpp', tmp)
        controls(solver)
        nine, ten, high_ten, eleven, eight, high_eight, regular = catalogues(small, five, dense_gen, cases)
        solver_id = sha256(solver.read_bytes()).digest()
        for s in cases:
            families = [(1, 9, nine, 10000, -1), (1, 10, high_ten, 10000, -1),
                        (2, 8, eight if s else high_eight, 10000, -1),
                        (2, 9, nine, 10000, 8), (2, 10, ten, 10000, 7),
                        (2, 11, eleven, 10000, -1)]
            if s == 2:
                families.append((2, 8, regular, 12, -1))
            for alpha, t, entries, qmax, required in families:
                search_family(solver, solver_id, (s, t, 178, alpha, 0, qmax, 21, 19, 8, required),
                              entries, jobs, cache)
            print(f'Excluded weight 178 with exactly {s} seven-columns.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--sevens', type=int, choices=(0, 1, 2), nargs='+', default=[2, 1, 0])
    parser.add_argument('--cache', type=Path, help='reuse completed batches from this solver build')
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and choose a positive job count')
    try:
        main(list(dict.fromkeys(args.sevens)), args.jobs, args.cache)
    except Witness as found:
        print('Verified 178-one matrix:')
        print('\n'.join(f'{r:021b}' for r in found.rows))
        extra = longest_extension(found.rows)
        assert admissible(found.rows + extra)
        print(f'Compatible eight-row additions: {len(extra)}')
        for row in extra:
            print(f'{row:021b}')
    else:
        if set(args.sevens) == {0, 1, 2}:
            print('The exact maxima on 19 x 21, 20 x 21 and 21 x 21 are 177, 185 and 193.')
