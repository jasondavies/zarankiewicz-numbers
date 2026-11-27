"""Exclude 185 ones on 19 by 22 with minimum row degree nine and column degree eight."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import os
from pathlib import Path
import re
from tempfile import NamedTemporaryFile
from subprocess import run
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'z19x21-k33'))
from verify_weight_178 import dense
from verify_rare_rows import catalogue, compile_cpp, loads, parse, projection, read_witness
from extend_eights import admissible, legal_supports, transpose


def complete(solver, points, width, total, high, marks, enumerate_all):
    args = ['inside', points, 18, width - points, 8, high, total,
            '--enumerate' if enumerate_all else '--gain']
    return run([solver, *map(str, args)], input=b'\n'.join(marks) + b'\n',
               capture_output=True, check=True).stdout.splitlines()


def four_extensions(core):
    available = list(legal_supports(core, 22, 8))

    def extend(rows, options, left):
        if left == 0:
            return rows
        for i, a in enumerate(options):
            next_options = [b for b in options[i:] if
                            all((a & b & c).bit_count() <= 2 for c in rows)]
            answer = extend((*rows, a), next_options, left - 1)
            if answer:
                return answer
        return None

    return extend(core, available, 4)


def marked_batch(solver, params, marks, cache, digest, mode='--all-cores'):
    data = b'\n'.join(marks) + b'\n'
    args = [*map(str, params), mode]
    key = sha256(digest + ' '.join(args).encode() + b'\n' + data).hexdigest()
    record = cache / key if cache else None
    output = record.read_bytes() if record and record.exists() else run(
        [solver, *args], input=data, capture_output=True, check=True).stdout
    *lines, summary = output.splitlines()
    match = re.fullmatch(rb'enumerated (\d+) cores (\d+) profiles (\d+)', summary)
    assert match and int(match[1]) == len(marks) and int(match[2]) == len(lines)
    if record and not record.exists():
        with NamedTemporaryFile(dir=cache, delete=False) as tmp:
            tmp.write(output)
        os.replace(tmp.name, record)
    results = []
    for line in lines:
        tag, *words = line.split()
        cols = tuple(map(int, words))
        assert tag == b'core' and len(cols) == params[6]
        assert all(0 <= c < 1 << params[7] and c.bit_count() >= 8 for c in cols)
        rows = transpose(cols, params[7])
        assert all(r.bit_count() >= params[8] for r in rows)
        assert sum(c.bit_count() for c in cols) == params[2]
        assert admissible(cols) and admissible(rows)
        results.append(rows)
    return results


def main(part, jobs, cache):
    if cache:
        cache.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix='z185-cover-') as directory:
        tmp = Path(directory)
        border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)
        marked = compile_cpp(ROOT / 'z18x19-k33/marked_core.cpp', tmp)
        digest = sha256(marked.read_bytes()).digest()
        five = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
        ten = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
        small = compile_cpp(ROOT / 'z18x19-k33/small_points.cpp', tmp, True)

        rows = read_witness(ROOT / 'z19x21-k33/witness-177.txt', 19, 21, 177)
        point_set, blocks = projection(rows, 21, 14)
        mark = ' '.join(map(str, blocks)).encode()
        output = complete(border, len(point_set), 21, 177, 18, [mark], False)
        assert len(output) == 1
        tag, *words = output[0].split()
        columns = tuple(map(int, words))
        assert tag == b'completion' and len(columns) == 21
        assert all(0 <= c < 1 << 19 and c.bit_count() >= 8 for c in columns)
        assert sum(c.bit_count() for c in columns) == 177
        assert admissible(columns) and admissible(transpose(columns, 19))

        control = marked_batch(marked, (0, len(point_set), 177, 1, 0, 10000, 21, 19, 9, -1),
                               [mark], None, digest)
        assert control

        witness = read_witness(ROOT / 'z22x23-k33/witness-216.txt', 22, 23, 216)
        cols = list(transpose(witness, 23))
        j = next(i for i, col in enumerate(cols) if col.bit_count() == 9)
        cols[j] &= cols[j] - 1
        partial = tuple(col for col in cols if col.bit_count() != 8)
        assert len(partial) == 19
        restored = four_extensions(partial)
        assert restored and len(restored) == 23 and admissible(restored)
        assert admissible(transpose(restored, 22)) and sum(c.bit_count() for c in restored) == 215

        nine = catalogue(small, 9, 69, 18, 7)
        tens = dense(ten, five, 10, 74)
        high, regular = [], []
        for line in tens:
            degree = loads(parse(line), 10)
            if sum(degree) >= 75:
                high.append(line)
            elif max(degree) <= 8:
                regular.append(line)
        assert (len(nine), len(tens), len(high), len(regular)) == (67537, 20250, 24, 11806)
        assert complete(border, 10, 22, 185, 17, high, True) == [b'enumerated 24']
        top = [line for line in nine if sum(b.bit_count() for b in parse(line)) >= 71]
        assert len(top) == 6
        # At least eight of the nine excess units lie on the mark.
        assert complete(border, 9, 22, 185, 9, top, True) == [b'enumerated 6']
        print('Verified the controls and excluded 24 ten-row and six nine-row projections.', flush=True)

        def search(entries, params):
            groups = (len(entries) + 63) // 64
            def check(i):
                cores = marked_batch(marked, params, entries[i::groups], cache, digest)
                if cores:
                    raise AssertionError(f'Unexpected completed core: {cores[0]}')
                return len(cores)

            with ThreadPoolExecutor(jobs) as pool:
                core_count = sum(pool.map(check, range(groups)))
            print(f'Checked {len(entries):,} marks, {core_count:,} completed cores.', flush=True)

        eleven = dense(ten, five, 11, 79)
        assert len(eleven) == 32
        search(eleven, (0, 11, 185, 2, 0, 14, 22, 19, 9, -1))
        if part in ('regular', 'all'):
            search(regular, (0, 10, 185, 1, 0, 9, 22, 19, 9, -1))
        exceptional = [line for line in nine if sum(x.bit_count() for x in parse(line)) == 70]
        tight = []
        for line in tens:
            excess = [n - 7 for n in loads(parse(line), 10)]
            if sum(excess) == 4 and 9 + sum(e*(e-1) for e in excess) <= 14:
                tight.append(line)
        assert len(exceptional) == 318 and len(tight) == 19911
        if part in ('nines', 'remaining', 'all'):
            search(exceptional, (0, 9, 185, 2, 0, 10000, 22, 19, 9, -1))
        if part in ('tens', 'remaining', 'all'):
            search(tight, (0, 10, 185, 2, 0, 14, 22, 19, 9, -1))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--part', choices=('marks', 'regular', 'nines', 'tens', 'remaining', 'all'), default='all')
    parser.add_argument('--jobs', type=int, default=2)
    parser.add_argument('--cache', type=Path)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use a positive job count')
    main(args.part, args.jobs, args.cache)
