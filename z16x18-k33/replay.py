"""Shared helpers for the two direct marked-line proofs."""
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from pathlib import Path
from subprocess import run
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'z17-k33'))
from ten_columns import possible_fives, four_cliques


def compile_cpp(source, directory, nauty=False):
    binary = directory / source.stem
    args = ['c++', '-std=c++20', '-O3', '-march=native', str(source), '-o', str(binary)]
    if nauty:
        args.append('-lnauty')
    run(args, check=True)
    return binary


def catalogue(binary, *args):
    result = run([binary, *map(str, args)], capture_output=True, check=True)
    return result.stdout.splitlines()


def line_bytes(blocks):
    return ' '.join(map(str, blocks)).encode()


def reject(binary, parameters, entries, expected, jobs):
    assert len(entries) == expected, (len(entries), expected)
    def shard(rows):
        text = b'\n'.join(rows) + b'\n'
        command = [binary, *map(str, parameters)]
        result = run(command, input=text, capture_output=True, check=True)
        if result.stdout.strip() != f'excluded {len(rows)}'.encode():
            raise RuntimeError(result.stdout.decode())
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        list(pool.map(shard, [entries[i::jobs] for i in range(min(jobs,len(entries)))]))
    print(*parameters, 'excluded', expected, flush=True)


def read_witness(path, row_count, columns, weight):
    strings = path.read_text().splitlines()
    assert len(strings) == row_count
    assert all(len(s) == columns and set(s) <= {'0','1'} for s in strings)
    rows = tuple(int(s,2) for s in strings)
    assert sum(r.bit_count() for r in rows) == weight
    assert all((a&b&c).bit_count() <= 2 for a,b,c in combinations(rows,3))
    return rows


def controls(binary, rows):
    # Use the *same* physical column from the 137 witness in both directions.
    selected = next(j for j in range(18) if sum((r>>j)&1 for r in rows)==9)
    for mode in ['inside','outside']:
        fixed = [r for r in rows if bool(r&(1<<selected)) == (mode=='inside')]
        blocks = [sum(((r>>c)&1)<<i for i,r in enumerate(fixed))
                  for c in range(18) if c != selected]
        args = [binary,mode,str(len(fixed)),'17',str(16-len(fixed)),'5','12','137']
        output = run(args, input=line_bytes(blocks)+b'\n', capture_output=True, check=True).stdout.split()
        assert output and output[0]==b'completion'
        result = tuple(map(int, output[1:]))
        assert len(result)==16 and all(0<=r<1<<18 for r in result)
        assert sum(r.bit_count() for r in result)==137
        assert all((a&b&c).bit_count()<=2 for a,b,c in combinations(result,3))


def ten_point_check():
    # On ten points, m >= 5 five-sets give too few fours even for 64
    # incidences in 15 blocks. This also rules out 73 in 17 blocks.
    counts = {5:0,6:0}
    for f in possible_fives([]):
        m = len(f)
        if m >= 5:
            assert next(four_cliques(f,64-45-2*m),None) is None
            counts[m] += 1
    assert counts == {5:12,6:12}


def regular_ten_rows():
    result = set()
    for f in possible_fives([]):
        if len(f) != 4:
            continue
        for four in four_cliques(f,11):
            blocks = tuple(sorted(f+four))
            loads = [sum((b>>j)&1 for b in blocks) for j in range(10)]
            if min(loads) >= 5 and max(loads) <= 7:
                result.add(blocks)
    return list(map(line_bytes,sorted(result)))
