"""Check the 19 by 21 upper bound and necessary conditions at weight 186."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from math import comb
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

from extend_178 import longest_extension
from extend_eights import admissible, extend, transpose
from verify_rare_rows import ROOT, catalogue, cliques, compile_cpp, loads, parse, projection, read_witness, reject


def bounded_tens(five, ten, count, minimum, low, high):
    families = catalogue(five, 10, minimum - 4 * count)
    return run([ten, *map(str, (high, count, minimum, low))],
               input=b'\n'.join(families) + b'\n', capture_output=True, check=True).stdout.splitlines()


def eleven_points(five):
    families = catalogue(five, 11, 8)
    assert len(families) == 6
    for line in families:
        base = parse(line)
        compatible = [b for b in range(1 << 11) if b.bit_count() == 4
                      and all((a & b).bit_count() <= 2 for a in base)]
        assert next(cliques(compatible, 28 - 2 * len(base)), None) is None


def check_179(small, five, ten, border, jobs):
    square = read_witness(ROOT / 'z21-k33/witness-193.txt', 21, 21, 193)
    witness = [r for r in square if r.bit_count() != 8]
    assert len(witness) == 19 and sum(r.bit_count() for r in witness) == 177
    assert admissible(witness) and admissible(transpose(witness, 21))
    extra = longest_extension(witness)
    assert len(extra) == 2 and sum(r.bit_count() for r in extra) == 16
    assert admissible(witness + list(extra))
    mark = next(i for i, r in enumerate(witness) if r.bit_count() == 10)
    _, blocks = projection(witness, 21, mark)
    line = ' '.join(map(str, blocks)).encode() + b'\n'
    tag, *words = run([border, 'inside', '10', '18', '11', '8', '9', '177', '--gain'],
                      input=line, capture_output=True, check=True).stdout.split()
    cols = list(map(int, words))
    assert tag == b'completion' and len(cols) == 21 and all(c < 1 << 19 for c in cols)
    assert sum(c.bit_count() for c in cols) == 177 and admissible(cols)
    assert admissible(transpose(cols, 19))

    # Mark a column instead, as in the 168,725-case search.
    witness_columns = transpose(witness, 21)
    mark = next(i for i, c in enumerate(witness_columns) if c.bit_count() == 9)
    _, blocks = projection(witness_columns, 19, mark)
    line = ' '.join(map(str, blocks)).encode() + b'\n'
    tag, *words = run([border, 'inside', '9', '20', '10', '9', '10', '177', '--gain'],
                      input=line, capture_output=True, check=True).stdout.split()
    rows = list(map(int, words))
    assert tag == b'completion' and len(rows) == 19 and all(0 <= r < 1 << 21 for r in rows)
    assert sum(r.bit_count() for r in rows) == 177 and admissible(rows)
    assert admissible(transpose(rows, 21))

    eleven_points(five)
    assert not catalogue(small, 11, 80, 18, 7)
    nine = catalogue(small, 9, 70, 18, 7)
    tens = bounded_tens(five, ten, 18, 75, 7, 9)
    reject(border, ('inside', 9, 18, 12, 8, 10, 179, '--gain'), nine, 324, jobs)
    reject(border, ('inside', 10, 18, 11, 8, 10, 179, '--gain'), tens, 18, jobs)
    print('177 <= z(19,21;3,3) <= 178.', flush=True)


def regular_core(small, border, jobs):
    assert not catalogue(small, 10, 80, 19, 8)
    balanced = [line for line in catalogue(small, 9, 72, 19, 8)
                if sum(b.bit_count() for b in parse(line)) == 72]
    assert len(balanced) == 1136

    def check_batch(batch):
        result = run([border, 'inside', '9', '19', '9', '9', '9', '162', '--enumerate'],
                     input=b'\n'.join(batch) + b'\n', capture_output=True, check=True)
        lines = result.stdout.splitlines()
        assert lines.pop() == f'enumerated {len(batch)}'.encode()
        for line in lines:
            tag, *words = line.split()
            cols = list(map(int, words))
            assert tag == b'completion' and len(cols) == 18
            assert all(0 <= c < 1 << 20 and c.bit_count() == 9 for c in cols)
            assert admissible(cols)
            assert extend(transpose(cols, 20), weight=7) is None
        return len(lines)

    with ThreadPoolExecutor(max_workers=jobs) as workers:
        batches = [balanced[i::jobs] for i in range(min(jobs, len(balanced)))]
        assert sum(workers.map(check_batch, batches)) == 55
    # Positive control in the same dimensions: restore three columns after thinning to sevens.
    witness = read_witness(ROOT / 'z20x21-k33/witness-185.txt', 20, 21, 185)
    cols = transpose(witness, 21)
    restored = extend(transpose(cols[3:], 20), weight=7)
    assert restored is not None and admissible(restored)
    print('All 55 marked completions with eighteen nine-columns reject three seven-columns.', flush=True)


def eight_row_cases(small, five, ten, border, jobs):
    # At most one eight-row among eleven marked rows; all nine missing rows have degree >= 9.
    marks = [line for line in catalogue(small, 11, 87, 20, 7)
             if loads(parse(line), 11).count(7) <= 1]
    reject(border, ('inside', 11, 20, 9, 9, 16, 186, '--gain'), marks, 3, jobs)

    # Eighteen-row deletion at 170, under the hypothesis that all columns have degree >= 8.
    tens = bounded_tens(five, ten, 17, 70, 7, 17)
    reject(border, ('inside', 10, 17, 11, 8, 10, 170, '--gain'), tens, 978, jobs)


def force_nine():
    # Minimum triple usage on the low columns, with zero or one eleven-row.
    for a, expected in ((0, 66), (1, 24)):
        counts = []
        for seven in (0, 1):
            for tens in range(10):
                low = tens + 3 - seven
                nines = 18 + seven - 2 * tens
                entries = 60 - 9 * a - 2 * nines - tens
                if entries <= (6 - a) * low:
                    d, r = divmod(entries, low)
                    counts.append((low - r) * comb(d, 3) + r * comb(d + 1, 3))
        assert min(counts) == expected > 2 * comb(6 - a, 3)


def exhaust_nines(border, nines, jobs):
    groups = {h: [] for h in range(3, 7)}
    for line in nines:
        h = sum(b.bit_count() for b in parse(line)) - 72
        groups[h].append(line)
    assert [len(group) for group in groups.values()] == [166480, 2186, 56, 3]

    def check(batch):
        h, lines = batch
        result = run([border, 'inside', '9', '20', '11', '9', str(min(11, 15 - h)), '186', '--gain'],
                     input=b'\n'.join(lines) + b'\n', capture_output=True, check=True)
        if result.stdout.strip() != f'excluded {len(lines)}'.encode():
            raise RuntimeError(result.stdout.decode())
        return len(lines)

    batches = []
    for h in sorted(groups, reverse=True):
        group = groups[h]
        parts = (len(group) + 149) // 150
        batches.extend((h, group[i::parts]) for i in range(parts))
    with ThreadPoolExecutor(max_workers=jobs) as workers:
        assert sum(workers.map(check, batches)) == 168725
    print('Every 186-one rectangle has an eight-row.', flush=True)


def high_rows(small, five, ten, border, jobs):
    tens = bounded_tens(five, ten, 20, 82, 8, 15)
    reject(border, ('inside', 10, 20, 9, 9, 14, 178, '--gain'), tens, 159, jobs)
    reject(border, ('inside', 10, 20, 10, 9, 13, 186, '--gain'), tens, 159, jobs)
    nines = catalogue(small, 9, 75, 20, 8)
    dense = [line for line in nines if sum(b.bit_count() for b in parse(line)) >= 76]
    reject(border, ('inside', 9, 20, 10, 9, 12, 178, '--gain'), dense, 2245, jobs)
    nine = [line for line in nines if max(loads(parse(line), 9)) >= 11]
    reject(border, ('inside', 9, 20, 11, 9, 12, 186, '--gain'), nine, 2215, jobs)
    force_nine()
    exhaust_nines(border, nines, jobs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use a positive job count')
    with TemporaryDirectory(prefix='z186-') as folder:
        tmp = Path(folder)
        small = compile_cpp(ROOT / 'z18x19-k33/small_points.cpp', tmp, True)
        five = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
        ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
        border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)
        check_179(small, five, ten, border, args.jobs)
        regular_core(small, border, args.jobs)
        eight_row_cases(small, five, ten, border, args.jobs)
        high_rows(small, five, ten, border, args.jobs)
