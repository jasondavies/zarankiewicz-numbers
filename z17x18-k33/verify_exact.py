"""Check the 143 witness and exhaust every 144-one candidate."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
from itertools import combinations, islice
from pathlib import Path
from subprocess import PIPE, Popen, run
from tempfile import TemporaryDirectory

import reduce_144
from verify import HERE, SMALL, compile_cpp, read_witness


def check_positive_controls(border, witness):
    mark = next(j for j in range(18) if sum(row >> j & 1 for row in witness) == 9)
    for side in ['inside', 'outside']:
        fixed = [row for row in witness if bool(row >> mark & 1) == (side == 'inside')]
        blocks = [sum(((row >> j) & 1) << i for i, row in enumerate(fixed))
                  for j in range(18) if j != mark]
        args = [side, len(fixed), 17, 17 - len(fixed), 7, 17 + int(side == 'outside'), 143]
        result = run([border, *map(str, args), '--gain'], input=' '.join(map(str, blocks)),
                     text=True, capture_output=True, check=True).stdout.split()
        assert result and result[0] == 'completion', side
        rows = list(map(int, result[1:]))
        assert len(rows) == 17 and all(0 <= r < 1 << 18 for r in rows)
        assert sum(r.bit_count() for r in rows) == 143
        assert all((a & b & c).bit_count() <= 2 for a, b, c in combinations(rows, 3))


def streaming_check(commands, border, args, expected, jobs):
    def check(rows):
        output = run([border, *map(str, args), '--gain'], input=b''.join(rows),
                     capture_output=True, check=True).stdout.strip()
        if output != f'excluded {len(rows)}'.encode():
            raise RuntimeError(output.decode())
        return len(rows)

    with ExitStack() as stack:
        stream = None
        children = []
        for command in commands:
            child = stack.enter_context(Popen(list(map(str, command)), stdin=stream, stdout=PIPE))
            if stream is not None:
                stream.close()
            stream = child.stdout
            children.append(child)
        count = 0
        with ThreadPoolExecutor(max_workers=jobs) as workers:
            while True:
                batch = []
                for _ in range(2 * jobs):
                    rows = list(islice(stream, 4096))
                    if not rows:
                        break
                    batch.append(rows)
                if not batch:
                    break
                count += sum(workers.map(check, batch))
        stream.close()
        if any(child.wait() != 0 for child in children):
            raise RuntimeError('catalogue generator failed')
    assert count == expected, (count, expected)
    print(*args, 'excluded', count, flush=True)


def main(jobs):
    witness = read_witness(HERE / 'witness-143.txt', 17, 18, 143)
    reduce_144.main(jobs)
    with TemporaryDirectory(prefix='z17x18-final-') as directory:
        tmp = Path(directory)
        nine = compile_cpp(SMALL.parent / 'z16x17-k33/catalogue.cpp', tmp, True)
        outer = compile_cpp(SMALL / 'outside_catalogue.cpp', tmp, True)
        lift = compile_cpp(HERE / 'outside_eight.cpp', tmp, True)
        border = compile_cpp(SMALL / 'borders.cpp', tmp)
        check_positive_controls(border, witness)
        streaming_check([[nine, 17, 65, 4, 6, 17]], border,
                        ('inside', 9, 17, 8, 7, 17, 144), 3_671_498, jobs)
        for degree, threshold, count in [(7, 64, 7_298_758), (8, 63, 12_057_949), (9, 63, 825)]:
            streaming_check([[outer, 7, threshold, degree], [lift, degree, 7, 71, 74]], border,
                            ('outside', 8, 17, 9, 7, 18, 144), count, jobs)
    print('Exact value 143.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error('enable assertions and use a positive job count')
    main(args.jobs)
