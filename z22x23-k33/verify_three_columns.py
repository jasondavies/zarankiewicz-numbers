"""Check the six-column projections at 193 ones on 20 by 22."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'z20x21-k33'))
from verify_rare_rows import catalogue, compile_cpp, projection, read_witness
from verify_bounds import compatible_groups


def subsets(n, k):
    return [sum(1 << i for i in points) for points in combinations(range(n), k)]


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first, *rest = vertices
    for i, second in enumerate(rest):
        edge = (1 << first) | (1 << second)
        for tail in matchings(rest[:i] + rest[i + 1:]):
            yield (edge, *tail)


def ten_marks():
    labels = subsets(4, 2)
    choices = tuple(frozenset(m) for m in matchings(list(range(6))))

    def choose(picked):
        i = len(picked)
        if i == len(labels):
            blocks = [63] + [(label << 6) | edge for label, m in zip(labels, picked) for edge in m]
            yield sorted(blocks)
            return
        for m in choices:
            if any(labels[i] & labels[j] and m & old for j, old in enumerate(picked)):
                continue
            yield from choose((*picked, m))
            # Two disjoint perfect matchings of K6 form an alternating six-cycle.
            if i < 2:
                break
    return choose(())


def eleven_marks():
    pairs = subsets(5, 2)
    triples = subsets(5, 3)
    types = [(a, b) for a, b in combinations(triples, 2) if (a & b).bit_count() == 1]
    profiles = placements = legal = 0
    for vertices in combinations_with_replacement(types, 6):
        frequency = Counter(t for vertex in vertices for t in vertex)
        if set(frequency.values()) != {2}:
            continue
        # Each outside point belongs to four pairs, each occurring three times.
        if any(12 - sum(bool(t & (1 << i)) for t in frequency) < 7 for i in range(5)):
            continue
        remaining = [[i for i, vertex in enumerate(vertices) if all(q & t != q for t in vertex)]
                     for q in pairs]
        if any(len(v) % 2 for v in remaining):
            continue
        profiles += 1
        forced = [(t << 6) | sum(1 << i for i, v in enumerate(vertices) if t in v)
                  for t in frequency]
        for choices in product(*(matchings(v) for v in remaining)):
            blocks = [63, *forced, *((q << 6) | e for q, m in zip(pairs, choices) for e in m)]
            assert len(blocks) == 19
            placements += 1
            if all((a & b).bit_count() <= 2 for a, b in combinations(blocks, 2)):
                legal += 1
    assert (profiles, placements, legal) == (150, 6930, 0)
    return profiles, placements


def main(jobs, cache):
    from verify_four_column_cover import marked_batch
    from extend_eights import admissible, transpose
    if cache:
        cache.mkdir(parents=True, exist_ok=True)
    profiles, placements = eleven_marks()
    with TemporaryDirectory(prefix='z193-six-') as directory:
        tmp = Path(directory)
        border = compile_cpp(ROOT / 'z16x18-k33/borders.cpp', tmp)
        small = compile_cpp(ROOT / 'z18x19-k33/small_points.cpp', tmp, True)
        five = compile_cpp(ROOT / 'z17x18-k33/fives.cpp', tmp, True)
        dense = compile_cpp(ROOT / 'z18-k33/ten_points.cpp', tmp, True)
        def projections(points, load):
            seeds = catalogue(five, points, load - 19*4)
            return run([dense, '19', '19', str(load), '7', str(points)],
                       input=b'\n'.join(seeds)+b'\n', capture_output=True, check=True).stdout.splitlines()

        assert not catalogue(small, 11, 84, 19, 7)
        elevens = projections(11, 82)
        assert len(elevens) == 68281
        for line in elevens:
            assert next(compatible_groups(tuple(map(int, line.split())), 7), None) is None
        nines = catalogue(small, 9, 72, 19, 7)
        tens = projections(10, 78)
        def totals(entries):
            return Counter(sum(int(x).bit_count() for x in line.split()) for line in entries)
        assert totals(nines) == {72:618888, 73:2191, 74:26, 75:1}
        assert totals(tens) == {78:14736, 79:12}
        for points, marks, threshold, high, count in ((9, nines, 74, 14, 27), (10, tens, 79, 16, 12)):
            top = [line for line in marks if sum(int(x).bit_count() for x in line.split()) >= threshold]
            assert len(top) == count
            result = run([border, 'inside', str(points), '19', str(22-points), '8', str(high),
                          '193', '--enumerate'], input=b'\n'.join(top)+b'\n', capture_output=True, check=True)
            assert result.stdout.splitlines() == [f'enumerated {count}'.encode()]
        peak = compile_cpp(ROOT / 'z18x19-k33/marked_core.cpp', tmp)
        witness = read_witness(ROOT / 'z20x21-k33/witness-185.txt', 20, 21, 185)
        degrees = [c.bit_count() for c in transpose(witness,21)]
        scores = [r.bit_count()+sum(d-8 for j,d in enumerate(degrees) if r >> j & 1) for r in witness]
        points, blocks = projection(witness,21,scores.index(max(scores)))
        result = run([peak,'0',str(len(points)),'185','1','0','10000','21','20','8','-1'],
                     input=(' '.join(map(str,blocks))+'\n').encode(), capture_output=True, check=True)
        tag, *words = result.stdout.split()
        control = tuple(map(int, words))
        assert tag == b'solution' and len(control) == 21 and all(0 <= c < 1<<20 for c in control)
        assert sum(x.bit_count() for x in control) == 185 and admissible(control) and admissible(transpose(control,20))
        peak_nines = [line for line in nines if sum(int(x).bit_count() for x in line.split()) == 73]
        assert len(peak_nines) == 2191
        result = run([peak, '0', '9', '193', '1', '0', '10000', '22', '20', '9', '-1',
                      '--all-cores'], input=b'\n'.join(peak_nines)+b'\n', capture_output=True, check=True)
        assert result.stdout.split()[:5] == [b'enumerated', b'2191', b'cores', b'0', b'profiles']
        digest = sha256(peak.read_bytes()).digest()
        def exhaust(marks, expected, points, multiplier, qmin, qmax):
            assert len(marks) == expected
            batches = (len(marks)+63)//64
            params = (0, points, 193, multiplier, qmin, qmax, 22, 20, 9, -1)
            def check(i):
                cores = marked_batch(peak, params, marks[i::batches], cache, digest)
                if cores:
                    raise AssertionError(f'Unexpected 193-one core {cores[0]}')
            with ThreadPoolExecutor(jobs) as pool:
                list(pool.map(check,range(batches)))
            print(f'{points}-point marks: checked {expected:,}, zero cores.',flush=True)

        def load(line):
            return sum(int(x).bit_count() for x in line.split())

        exhaust([line for line in elevens if load(line)==83],144,11,2,0,21)
        eight = catalogue(small, 8, 72, 21, 8)
        assert len(eight) == 326456
        pure = []
        for line in eight:
            blocks = tuple(map(int,line.split()))
            if sum(x.bit_count() for x in blocks) != 72:
                continue
            rows = transpose(blocks,8)
            if all(r.bit_count() == 9 for r in rows) and all(
                    (a&b).bit_count() <= 4 for a,b in combinations(rows,2)):
                pure.append(line)
        assert len(pure) == 627
        five_tens = compile_cpp(ROOT / 'z22x23-k33/five_tens.cpp', tmp)
        data = b'\n'.join(pure)+b'\n'
        control = run([five_tens,'3'],input=data,capture_output=True,check=True).stdout.split()
        assert control[0] == b'completion'
        low = int(control[1])
        rows = list(map(int,control[2:]))
        assert low.bit_count() == 4 and low < 1<<21 and len(rows) == 11
        assert all(r.bit_count()==10 and 0 <= r < 1<<22 for r in rows)
        assert all(r&1 for r in rows[:8]) and all(not r&1 for r in rows[8:])
        assert all(((r>>1)&low).bit_count()>=3 for r in rows[8:])
        assert admissible(rows) and admissible(transpose(rows,22))
        result = run([five_tens,'4'],input=data,capture_output=True,check=True)
        assert result.stdout.splitlines() == [b'excluded 627 choices 2143']
        print('Recovered three outside ten-rows. No mark accepts four.',flush=True)
        exhaust([line for line in tens if load(line)==78],14736,10,1,0,31)
        entries = list(ten_marks())
        assert len(entries) == 82
        for blocks in entries:
            assert len(blocks) == 19 and all((a&b).bit_count() <= 2 for a,b in combinations(blocks,2))
            assert sorted(sum(b >> j & 1 for b in blocks) for j in range(10)) == [7]*6 + [9]*4
        data = ''.join(' '.join(map(str, blocks)) + '\n' for blocks in entries)
        out = run([border,'inside','10','19','12','8','17','193','--enumerate'],
                  input=data, capture_output=True, check=True, text=True)
        assert out.stdout.splitlines() == ['enumerated 82']
    print(f'Eleven points: {profiles} profiles, {placements} assignments, zero valid projections.')
    print('No seven-block lift among 68,281 eleven-point marks. Cover: 621,106 nines and 14,748 tens.')
    print('Ten points: 82 six-block projections, zero completions at weight 193.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--cache', type=Path)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use a positive job count')
    main(args.jobs, args.cache)
