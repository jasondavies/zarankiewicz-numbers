"""Check the ten-row exclusions and the one-seven-column case at weight 163."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'z17x18-k33'))
from verify import catalogue, compile_cpp, read_witness
sys.path.insert(0, str(ROOT / 'z20x21-k33'))
from extend_eights import admissible, legal_supports, transpose


def add_sevens(columns, pool, left):
    if not left:
        return columns
    for i, a in enumerate(pool):
        if len(pool) - i < left:
            break
        following = [b for b in pool[i+1:] if all((a & b & c).bit_count() <= 2 for c in columns)]
        extension = add_sevens(columns + [a], following, left - 1)
        if extension is not None:
            return extension
    return None


def ten_row(tmp, jobs):
    fives = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
    ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
    border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)
    families = catalogue(fives, 10, 2)
    entries = run([ten, '17'], input=b'\n'.join(families) + b'\n',
                  capture_output=True, check=True).stdout.splitlines()
    assert len(entries) == 978
    expected = [(7, 0), (35, 0), (56, 5), (0, 0), (0, 0), (0, 0)]
    for k, counts in enumerate(expected, start=1):
        def batch(lines):
            args = ['inside', 10, 17, 10-k, 8, min(17, 11+k), 163-7*k, '--enumerate']
            out = run([border, *map(str, args)], input=b'\n'.join(lines) + b'\n',
                      capture_output=True, check=True).stdout.splitlines()
            assert out[-1] == f'enumerated {len(lines)}'.encode()
            single = 0
            for line in out[:-1]:
                tag, *data = line.split()
                cols = list(map(int, data))
                assert tag == b'completion' and len(cols) == 20-k and admissible(cols)
                assert all(0 <= x < 1 << 18 for x in cols)
                assert sum(x.bit_count() for x in cols) == 163-7*k
                pool = list(legal_supports(cols, 18, 7))
                single += bool(pool)
                found = add_sevens(cols, pool, k)
                if found is not None:
                    raise RuntimeError(f'163-one completion with column masks {found}')
            return len(out)-1, single
        n = min(len(entries), 4 * jobs)
        with ThreadPoolExecutor(jobs) as workers:
            results = list(workers.map(batch, (entries[i::n] for i in range(n))))
        observed = tuple(map(sum, zip(*results)))
        assert observed == counts, (k, observed)
        print(f'{k} sevens: {counts[0]} marked cores, {counts[1]} singly extendible, no completion.',
              flush=True)


def one_seven(tmp, jobs):
    nine = compile_cpp(ROOT / 'z16x17-k33/catalogue.cpp', tmp, True)
    core = compile_cpp(ROOT / 'z18x19-k33/marked_core.cpp', tmp)
    entries = catalogue(nine, 17, 65, 0, 7, 17)
    assert len(entries) == 87842
    def batch(lines):
        args = [core, '1', '9', '163', '2', '0', '10000', '20', '18', '6']
        out = run(args, input=b'\n'.join(lines) + b'\n', capture_output=True, check=True).stdout
        if not out.startswith(f'excluded {len(lines)} cores '.encode()):
            raise RuntimeError(out.decode())
    n = (len(entries) + 127) // 128
    with ThreadPoolExecutor(jobs) as workers:
        list(workers.map(batch, (entries[i::n] for i in range(n))))
    print('All 87,842 nine-row projections excluded for one seven-column.', flush=True)


def square_deletions(columns, supports):
    # An illegal seven-support survives the deletion only if the same entry
    # repairs every violated pair. Track eligible rows and columns separately.
    universe = (1 << 18) - 1
    entries = {(j, 1 << i): [] for j, col in enumerate(columns)
               for i in range(18) if col & (1 << i)}
    pairs = [(a & b, (1 << j) | (1 << h))
             for j, a in enumerate(columns) for h, b in enumerate(columns[:j])
             if (a & b).bit_count() >= 3]
    for s in supports:
        rows, endpoints = universe, universe
        for both, edge in pairs:
            common = both & s
            if common.bit_count() < 3:
                continue
            if common.bit_count() > 3:
                rows = 0
                break
            rows &= common
            endpoints &= edge
            if not (rows and endpoints):
                break
        if rows and endpoints:
            for (j, bit), pool in entries.items():
                if endpoints & (1 << j) and rows & bit:
                    pool.append(s)
    for (j, bit), pool in entries.items():
        cut = columns.copy()
        cut[j] ^= bit
        if add_sevens(cut, pool, 2) is not None:
            raise RuntimeError('A thinned square accepts two seven-columns')
    return len(entries)


def maximality(tmp):
    from itertools import combinations
    border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)
    canon = compile_cpp(ROOT / 'z20x21-k33/canonical.cpp', tmp, True)
    supports = [sum(1 << i for i in subset) for subset in combinations(range(18), 7)]
    cases = (HERE / 'square-marks.txt').read_text().splitlines()
    total = 0
    for t, count in ((9, 5), (10, 1)):
        marks = [line.partition(' ')[2] for line in cases if int(line.split()[0]) == t]
        assert len(marks) == count
        data = ('\n'.join(marks) + '\n').encode()
        canonical = run([canon, str(t)], input=data, capture_output=True, check=True).stdout
        assert len(set(canonical.splitlines())) == count
        for mark in marks:
            blocks = list(map(int, mark.split()))
            assert len(blocks) == 17 and all(0 <= b < 1 << t and b.bit_count() <= 5 for b in blocks)
            assert all((a & b).bit_count() <= 2 for a, b in combinations(blocks, 2))
            loads = [sum((b >> j) & 1 for b in blocks) for j in range(t)]
            assert min(loads) >= 7 and max(loads) <= 13 and sum(loads) >= (65 if t == 9 else 70)
        args = [border, 'inside', str(t), '17', str(18-t), '8', '14', '150', '--enumerate']
        out = run(args, input=data, capture_output=True, check=True).stdout.splitlines()
        assert out[-1] == f'enumerated {count}'.encode() and len(out)-1 == count
        for line in out[:-1]:
            tag, *data = line.split()
            cols = list(map(int, data))
            assert tag == b'completion' and len(cols) == 18 and admissible(cols)
            assert all(0 <= c < 1 << 18 for c in cols) and sum(c.bit_count() for c in cols) == 150
            for orientation in (cols, list(transpose(cols, 18))):
                total += square_deletions(orientation, supports)
    assert total == 1800
    print('All 1,800 one-entry deletions in the two orientations excluded.', flush=True)


def two_sevens(tmp, jobs):
    from collections import Counter
    small = compile_cpp(ROOT / 'z18x19-k33/small_points.cpp', tmp, True)
    nine = compile_cpp(ROOT / 'z16x17-k33/catalogue.cpp', tmp, True)
    fives = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
    ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
    border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)
    core = compile_cpp(ROOT / 'z18x19-k33/marked_core.cpp', tmp)

    families = catalogue(fives, 11, 7)
    low = run([ten, '7', '17', '75', '5', '11'], input=b'\n'.join(families) + b'\n',
              capture_output=True, check=True).stdout.splitlines()
    from verify import reject
    reject(border, ('inside', 11, 17, 7, 7, 9, 149), low, 70, jobs)

    # Check the degree-three score multiplier on a satisfiable instance.
    square = read_witness(ROOT / 'z20-k33/witness-180.txt', 20, 20, 180)
    heavy = [c for c in transpose(square[2:], 20) if c.bit_count() >= 8]
    mark = max(range(18), key=lambda i: sum(c.bit_count()-5 for c in heavy if (c >> i) & 1))
    selected = [c for c in heavy if (c >> mark) & 1]
    blocks = [sum(((c >> i) & 1) << j for j, c in enumerate(selected)) for i in range(18) if i != mark]
    params = (20-len(heavy), len(selected), 162, 3, 0, 10000, 20, 18)
    out = run([core, *map(str, params)], input=' '.join(map(str, blocks)), text=True,
              capture_output=True, check=True).stdout.split()
    cols = list(map(int, out[1:]))
    assert out[0] == 'solution' and len(cols) == 20 and all(0 <= x < 1 << 18 for x in cols)
    assert admissible(cols) and sum(x.bit_count() for x in cols) == 162

    for t, entries in ((8, catalogue(small, 8, 60)), (9, catalogue(nine, 17, 65, 0, 7, 17))):
        assert len(entries) == (147269 if t == 8 else 87842)
        profiles = [((4, 1), 2, 20, 90 if t == 8 else 0)]
        if t == 9:
            profiles.extend([((3, 2), 2, 21, 19), ((3, 1, 1), 2, 21, 19),
                             ((2, 2, 1), 3, 29, 9898)])
        for profile, alpha, minimum, expected in profiles:
            chosen = []
            full = Counter(profile)
            for line in entries:
                blocks = tuple(map(int, line.split()))
                excess = [sum((b >> j) & 1 for b in blocks)-7 for j in range(t)]
                if alpha*t + sum(excess) >= minimum and not (Counter(e for e in excess if e) - full):
                    chosen.append(line)
            assert len(chosen) == expected, (profile, t, len(chosen))
            q = sum(e*e for e in profile)
            def batch(lines):
                params = (2, t, 163, alpha, q, q, 20, 18, 6)
                out = run([core, *map(str, params)], input=b'\n'.join(lines)+b'\n',
                          capture_output=True, check=True).stdout
                if not out.startswith(f'excluded {len(lines)} cores '.encode()):
                    raise RuntimeError(out.decode())
            n = min(4*jobs, len(chosen))
            with ThreadPoolExecutor(jobs) as pool:
                list(pool.map(batch, (chosen[i::n] for i in range(n))))
            print(f'Two seven-columns, excess {profile}, mark {t}: excluded {expected}.', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--stage', choices=('ten', 'one', 'two', 'maximal', 'all'), default='all')
    args = parser.parse_args()
    if args.jobs < 1 or not __debug__:
        parser.error('use a positive job count and enable Python assertions')
    square = read_witness(ROOT / 'z20-k33/witness-180.txt', 20, 20, 180)
    columns = transpose(square[2:], 20)
    heavy = [c for c in columns if c.bit_count() >= 8]
    k = len(columns) - len(heavy)
    assert k > 0 and all(c.bit_count() >= 7 for c in columns)
    found = add_sevens(heavy, list(legal_supports(heavy, 18, 7)), k)
    assert found is not None and len(found) == 20 and admissible(found)
    assert sum(x.bit_count() for x in found) == 162
    with TemporaryDirectory() as directory:
        if args.stage in ('ten', 'all'):
            ten_row(Path(directory), args.jobs)
        if args.stage in ('maximal', 'all'):
            maximality(Path(directory))
        if args.stage in ('two', 'all'):
            two_sevens(Path(directory), args.jobs)
        if args.stage in ('one', 'all'):
            one_seven(Path(directory), args.jobs)


if __name__ == '__main__':
    main()
