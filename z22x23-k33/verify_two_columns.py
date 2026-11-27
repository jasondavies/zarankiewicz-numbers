"""Prove the 201-to-193 reduction and test the stored parents for extensions."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from itertools import combinations_with_replacement
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'z20x21-k33'))
from extend_eights import admissible, legal_supports, transpose
from verify_rare_rows import catalogue, compile_cpp, read_witness


def main(jobs, cache):
    from verify_four_column_cover import marked_batch
    if cache:
        cache.mkdir(parents=True, exist_ok=True)
    square = tuple(read_witness(ROOT / 'z22-k33/witness-210.txt', 22, 22, 210))
    assert admissible(square) and admissible(transpose(square,22))
    checked = 0
    for rows in (square, transpose(square,22)):
        for i, row in enumerate(rows):
            if row.bit_count() != 9:
                continue
            others = rows[:i] + rows[i+1:]
            candidates = set(legal_supports(others,22,8))
            assert candidates == {row ^ (1 << j) for j in range(22) if row >> j & 1}
            for a in candidates:
                for b in candidates:
                    assert any((a & b & r).bit_count() >= 3 for r in others)
            checked += 1
    assert checked == 20
    small_square = tuple(read_witness(ROOT/'z21-k33/witness-193.txt',21,21,193))
    for rows in (small_square,transpose(small_square,21)):
        cols = transpose(rows,21)
        first = list(legal_supports(cols,21,8))
        assert len(first) == 1
        core = transpose((*cols,first[0]),21)
        assert min(r.bit_count() for r in core) >= 9
        pool = list(legal_supports(core,22,8))
        assert len(pool) == 9
        assert not any(all((a&b&r).bit_count() <= 2 for r in core)
                       for a,b in combinations_with_replacement(pool,2))

        # Mixed construction: add a row to the 201 rectangle and then a column.
        examined = 0
        for r in pool:
            new_cols = transpose((*core,r),22)
            if min(c.bit_count() for c in new_cols) >= 9:
                examined += 1
                assert next(legal_supports(new_cols,22,8),None) is None
        assert examined > 0

    with TemporaryDirectory(prefix='z201-min9-') as folder:
        tmp = Path(folder)
        five = compile_cpp(ROOT/'z17x18-k33/fives.cpp',tmp,True)
        ten = compile_cpp(ROOT/'z18-k33/ten_points.cpp',tmp,True)
        border = compile_cpp(ROOT/'z16x18-k33/borders.cpp',tmp)
        marked = compile_cpp(ROOT/'z18x19-k33/marked_core.cpp',tmp)
        seeds = catalogue(five,10,1)
        marks = run([ten,'9','20','81','8','10'],input=b'\n'.join(seeds)+b'\n',
                    capture_output=True,check=True).stdout.splitlines()
        assert len(marks) == 5636
        heavy = [b for b in marks if sum(int(x).bit_count() for x in b.split()) >= 82]
        assert len(heavy) == 149
        seeds82 = catalogue(five,10,2)
        unrestricted = run([ten,'11','20','82','8','10'],input=b'\n'.join(seeds82)+b'\n',
                           capture_output=True,check=True).stdout.splitlines()
        assert len(unrestricted) == 159
        result = run([border,'inside','10','20','12','9','10','201','--enumerate'],
                     input=b'\n'.join(unrestricted)+b'\n',capture_output=True,check=True)
        assert result.stdout.splitlines() == [b'enumerated 159']
        heavy_set = set(heavy)
        remaining = [b for b in marks if b not in heavy_set]
        assert len(remaining) == 5487
        digest = sha256(marked.read_bytes()).digest()
        def check(i):
            cores = marked_batch(marked,(0,10,201,1,31,31,22,21,0,-1),
                                 remaining[i::32],cache,digest)
            assert not cores
        with ThreadPoolExecutor(jobs) as pool:
            list(pool.map(check,range(32)))
    print('Checked 159 high-load and 5,487 unit-excess marks. Every 201-one rectangle has an eight-column.')
    print('All twenty oriented deletions admit exactly nine eight-rows apiece. No pair coexists.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=4)
    parser.add_argument('--cache',type=Path)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use a positive job count')
    main(args.jobs,args.cache)
