"""Replay the 18 by 19 weight-157 proof, or a single seven-column count."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent


def local_module(name, filename):
    spec = spec_from_file_location(name, HERE / filename)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


first = local_module('z18x19_first', 'verify.py')
squares = local_module('z18x19_square_cores', 'verify_cores.py')
COUNTS = {
    (4, 36): 4736, (5, 42): 10193, (6, 48): 73217, (6, 50): 492,
    (7, 54): 170476, (7, 55): 6626, (8, 60): 147269,
    (9, 65): 87842, (9, 66): 2418, (10, 70): 978,
}

# Numbers of completed cores, including repetitions from distinct marked projections.
CORE_COUNTS = {
    (2, 2): 6, (3, 2): 3715, (4, 1): 879558, (4, 2): 212075,
    (5, 1): 52498, (6, 1): 1224, (7, 1): 127, (8, 1): 6, (9, 1): 1,
}


def verify_candidate(words, weight):
    cols = tuple(map(int, words))
    assert len(cols) == 19 and all(0 <= c < 1 << 18 for c in cols)
    assert sum(c.bit_count() for c in cols) == weight
    assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(cols, 3))
    return cols


def positive_control(check):
    # Remove one edge in each of two degree-eight columns of a 156 witness.
    # Forget all but the maximal-score projection, then reconstruct weight 154.
    rows = first.read_witness(HERE / 'witness-156-min8.txt', 18, 19, 156)
    cols = tuple(sum(((r >> j) & 1) << i for i, r in enumerate(rows)) for j in range(18, -1, -1))
    removed = [j for j, c in enumerate(cols) if c.bit_count() == 8][:2]
    assert len(removed) == 2 and min(c.bit_count() for c in cols) == 8
    core = [c for j, c in enumerate(cols) if j not in removed]
    scores = [sum(c.bit_count() - 6 for c in core if (c >> i) & 1) for i in range(18)]
    i = scores.index(max(scores))
    marked = [c for c in core if (c >> i) & 1]
    blocks = [sum(((c >> j) & 1) << h for h, c in enumerate(marked)) for j in range(18) if j != i]
    out = run([check, '2', str(len(marked)), '154', '2'],
              input=' '.join(map(str, blocks)), text=True, capture_output=True, check=True).stdout.split()
    assert out[0] == 'solution'
    verify_candidate(out[1:], 154)


def cases(k):
    # Each tuple is (score multiplier, minimum sum of squared excesses,
    # maximum sum of squared excesses, smallest possible marked degree).
    if k <= 3:
        return [(2, 0, 1000, 6)]
    if k == 4:
        return [(1, 0, 12, 6), (2, 13, 1000, 6)]
    minimum = {5: 4, 6: 5, 7: 5, 8: 5, 9: 4}[k]
    return [(1, 0, 1000, minimum)]


def exhaust(counts, jobs):
    with TemporaryDirectory(prefix='z18x19-marked-') as directory:
        tmp = Path(directory)
        cpp = first.compile_cpp
        small = cpp(HERE / 'small_points.cpp', tmp, True)
        nine = cpp(first.SMALL.parent / 'z16x17-k33/catalogue.cpp', tmp, True)
        ten = cpp(HERE.parent / 'z18-k33/ten_points.cpp', tmp, True)
        five = cpp(first.RECT / 'fives.cpp', tmp, True)
        check = cpp(HERE / 'marked_core.cpp', tmp)
        positive_control(check)
        assert not first.dense_blocks(11, 77, first.catalogue(five, 11, 9))
        cache = {}

        def projections(t, alpha):
            threshold = (6*t + 12) if alpha == 1 else (5*t + 20)
            if t == 10:
                threshold = 70
            key = (t, threshold)
            if key not in cache:
                if t < 9:
                    entries = first.catalogue(small, t, threshold)
                elif t == 9:
                    entries = first.catalogue(nine, 17, threshold, 0, 7, 17)
                else:
                    fives = first.catalogue(five, 10, 2)
                    entries = run([ten, '17'], input=b'\n'.join(fives) + b'\n',
                                  capture_output=True, check=True).stdout.splitlines()
                assert len(entries) == COUNTS[key], (key, len(entries))
                cache[key] = entries
            return cache[key]

        with ThreadPoolExecutor(max_workers=jobs) as workers:
            for k in counts:
                for alpha, lower, upper, smallest in cases(k):
                    total_cores = 0
                    for t in range(smallest, 11):
                        entries = projections(t, alpha)
                        args = [check, *map(str, (k, t, 157, alpha, lower, upper))]

                        def shard(batch):
                            words = run(args, input=b'\n'.join(batch) + b'\n', check=True,
                                        capture_output=True).stdout.split()
                            if words[0] == b'solution':
                                cols = verify_candidate(words[1:], 157)
                                raise RuntimeError(f'157-one witness, columns {cols}')
                            assert words[::2] == [b'excluded', b'cores', b'profiles']
                            assert int(words[1]) == len(batch)
                            return int(words[3])

                        # Short, interleaved batches balance slow projections across workers.
                        chunks = max(1, (len(entries) + 127) // 128)
                        cores = sum(workers.map(shard, (entries[i::chunks] for i in range(chunks))))
                        total_cores += cores
                        print(f'k={k} alpha={alpha} t={t}: {len(entries)} projections, '
                              f'{cores} completed cores, zero extensions.', flush=True)
                    assert total_cores == CORE_COUNTS[k, alpha], (k, alpha, total_cores)


def main(case, jobs):
    first.read_witness(HERE / 'witness-156.txt', 18, 19, 156)
    if case in (None, 0):
        first.main(True, jobs)
    if case in (None, 1):
        squares.main(jobs)
    if case is None or case >= 2:
        exhaust(range(2, 10) if case is None else [case], jobs)
    if case is None:
        print('Exact value 156.')
    else:
        print(f'Seven-column count {case} excluded.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=int, choices=range(10))
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('use a positive job count and enable assertions')
    main(args.case, args.jobs)
