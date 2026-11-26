"""Replay the 163-one core restrictions and the strengthened column bound at 187."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from math import comb
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'z17x18-k33'))
from verify import cliques, catalogue, compile_cpp, dense_blocks, read_witness, reject
from verify_bounds import compatible_groups
from extend_eights import admissible, extend, transpose


def check_extension():
    witness = read_witness(HERE / 'witness-185.txt', 20, 21, 185)
    columns = transpose(witness, 21)
    removed = [j for j, c in enumerate(columns) if c.bit_count() == 8][:3]
    assert len(removed) == 3
    rows = transpose([c for j, c in enumerate(columns) if j not in removed], 20)
    result = extend(rows)
    assert result is not None and sum(r.bit_count() for r in result) == 185 and admissible(result)
    assert tuple(r % (1 << 18) for r in result) == rows


def check_marked_control(binary, rows):
    columns = transpose(rows, 20)
    high = [c for c in columns if c.bit_count() >= 8]
    k = len(columns) - len(high)
    scores = [sum(c.bit_count() - 7 for c in high if (c >> i) & 1) for i in range(18)]
    i = scores.index(max(scores))
    selected = [c for c in high if (c >> i) & 1]
    blocks = [sum(((c >> r) & 1) << j for j, c in enumerate(selected)) for r in range(18) if r != i]
    words = run([binary, *map(str, (k, len(selected), 162, 1, 0, 10000, 20))],
                input=' '.join(map(str, blocks)), text=True, check=True, capture_output=True).stdout.split()
    assert words[0] == 'solution'
    found = tuple(map(int, words[1:]))
    assert len(found) == 20 and all(0 <= c < 1 << 18 for c in found)
    assert sum(c.bit_count() for c in found) == 162 and admissible(found)


def check_sevens(k, jobs, core, projections):
    total = cores = 0
    with ThreadPoolExecutor(jobs) as workers:
        for t in range(3 if k == 10 else 4, 11):
            data = projections(t)
            n = min(96, (len(data) + 255) // 256)
            def shard(batch):
                words = run([core, *map(str, (k, t, 163, 1, 0, 10000, 20))],
                            input=b'\n'.join(batch) + b'\n', capture_output=True, check=True).stdout.split()
                if words[::2] != [b'excluded', b'cores', b'profiles'] or int(words[1]) != len(batch):
                    raise RuntimeError(words)
                return int(words[3])
            cores += sum(workers.map(shard, (data[i::n] for i in range(n))))
            total += len(data)
    print(f'{k} seven-rows: {total} projections, {cores} high cores, zero completions.', flush=True)
    expected = {7: (409287, 136123), 8: (409287, 7165), 9: (409287, 209), 10: (410481, 52)}
    assert (total, cores) == expected[k]


def exclude_eleven(five, border, jobs):
    projections = []
    families = catalogue(five, 11, 7)
    assert len(families) == 21
    for line in families:
        base = tuple(map(int, line.split()))
        pool = [b for b in range(1 << 11) if b.bit_count() == 4 and
                all((b & a).bit_count() <= 2 for a in base)]
        for fours in cliques(pool, 27 - 2 * len(base)):
            assert len(base) == 7 and len(fours) == 13
            blocks = base + fours
            deficit = sum(max(0, 8 - sum((b >> j) & 1 for b in blocks)) for j in range(11))
            if deficit <= 1:
                projections.append(' '.join(map(str, blocks)).encode())
    reject(border, ('inside', 11, 20, 9, 9, 17, 187, '--gain'), projections, 12, jobs)


def exclude_many_eights(small, border, jobs):
    for q in range(8, 12):
        possible = []
        for s in (0, 1):
            for h in range(1, 8 + s):
                required = 8*q - 2*(20 - h - s)
                d, r = divmod(required, q)
                triples = (q - r)*comb(d, 3) + r*comb(d + 1, 3)
                if required <= q*h and triples <= 2*comb(h, 3):
                    possible.append((s, h, required))
        assert possible == ([(0, 7, 38), (1, 8, 42)] if q == 8 else [])
    # Published z(7,8)=37 and z(8,8)=42 force the second case and equality.
    assert not catalogue(small, 7, 43, 12, 6)
    eight = catalogue(small, 8, 48, 12, 6)
    assert len(eight) == 1 and all(int(x).bit_count() == 4 for x in eight[0].split())
    reject(border, ('inside', 8, 12, 4, 7, 8, 85), eight, 1, jobs)


def four_eights(five, ten, nine, border, jobs):
    tens = run([ten, '7', '16', '67', '5'], input=b'\n'.join(catalogue(five, 10, 3)) + b'\n',
               capture_output=True, check=True).stdout.splitlines()
    reject(border, ('inside', 10, 16, 10, 6, 8, 155), tens, 519, jobs)
    thin_nines = catalogue(nine, 16, 62, 1, 6, 7)
    totals = [sum(int(x).bit_count() for x in line.split()) for line in thin_nines]
    assert totals.count(62) == 4018 and totals.count(63) == 10 and len(totals) == 4028
    zero = [line for line, total in zip(thin_nines, totals) if total == 63]
    reject(border, ('inside', 9, 16, 11, 6, 8, 155, '--gain'), zero, 10, jobs)


def main(jobs, cases, full):
    check_extension()
    square = read_witness(ROOT / 'z20-k33/witness-180.txt', 20, 20, 180)
    assert sum(r.bit_count() for r in square[2:]) == 162
    large = read_witness(ROOT / 'z21-k33/witness-193.txt', 21, 21, 193)
    assert sum(sorted(r.bit_count() for r in large)[3:]) == 168
    with TemporaryDirectory(prefix='z20x21-cores-') as directory:
        tmp = Path(directory)
        source = ROOT / 'z18x19-k33'
        small = compile_cpp(source / 'small_points.cpp', tmp, True)
        five = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
        ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
        border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)
        assert not dense_blocks(11, 77, catalogue(five, 11, 9))
        tens = run([ten, '17'], input=b'\n'.join(catalogue(five, 10, 2)) + b'\n',
                   capture_output=True, check=True).stdout.splitlines()
        for weight in (163, 164):
            reject(border, ('inside', 10, 17, 10, 8, weight - 152, weight), tens, 978, jobs)

        assert not catalogue(small, 10, 80, 19, 8)
        nines = catalogue(small, 9, 72, 19, 8)
        assert len(nines) == 1226
        three = [line for line in nines if sum(int(b).bit_count() for b in line.split()) <= 73]
        reject(border, ('inside', 9, 19, 9, 9, 10, 163), three, 1217, jobs)
        assert all(next(compatible_groups(tuple(map(int, line.split())), 7), None) is None
                   for line in nines)
        if full:
            reject(border, ('inside', 9, 19, 12, 8, 19, 187, '--gain'), nines, 1226, jobs)
        nine = compile_cpp(ROOT / 'z16x17-k33/catalogue.cpp', tmp, True)
        exclude_eleven(five, border, jobs)
        exclude_many_eights(small, border, jobs)
        four_eights(five, ten, nine, border, jobs)
        core = compile_cpp(source / 'marked_core.cpp', tmp)
        check_marked_control(core, square[2:])
        if cases:
            cache = {10: tens}
            def projections(t):
                if t not in cache:
                    cache[t] = (catalogue(nine, 17, 66, 0, 7, 17) if t == 9 else
                                catalogue(small, t, 6*t + 12))
                return cache[t]
            for k in cases:
                check_sevens(k, jobs, core, projections)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--full', action='store_true', help='also exclude any row on nine heavy columns at 187')
    parser.add_argument('--sevens', type=int, nargs='+', choices=range(7, 11), default=[])
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and supply a positive job count')
    main(args.jobs, args.sevens, args.full)
