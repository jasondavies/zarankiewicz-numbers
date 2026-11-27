"""Decide whether a given 21-row, 19-column parent admits four eight-one columns."""
from argparse import ArgumentParser
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'z20x21-k33'))
from extend_eights import admissible, legal_supports


def pack(fixed, pool, count):
    if not count:
        return ()
    for i,a in enumerate(pool):
        # Include a itself so the search also handles controls where repetition is legal.
        next_pool = [b for b in pool[i:] if all((a & b & c).bit_count()<=2 for c in fixed)]
        rest = pack((*fixed,a), next_pool, count-1)
        if rest is not None:
            return (a,*rest)
    return None


def extensions(columns):
    if len(columns)!=19 or any(not 0<=c<1<<21 for c in columns) or not admissible(columns):
        raise ValueError('expected an admissible binary matrix with 21 rows and 19 columns')
    pool = list(legal_supports(columns,21,8))
    for k in (4,3,2,1,0):
        answer = pack(tuple(columns),pool,k)
        if answer is not None:
            assert len(answer)==k and admissible((*columns,*answer))
            return pool,answer


def read_parent(path):
    lines = path.read_text().splitlines()
    if all(len(s)==19 for s in lines) and len(lines)==21:
        lines = [''.join(x) for x in zip(*lines)]
    if len(lines)!=19 or any(len(s)!=21 or set(s)-{'0','1'} for s in lines):
        raise ValueError('supply 21 rows of 19 bits or the transposed representation')
    return tuple(int(s,2) for s in lines)


if __name__=='__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('matrix',type=Path)
    args = parser.parse_args()
    cols = read_parent(args.matrix)
    opts,witness = extensions(cols)
    print(f'{sum(map(int.bit_count,cols))} ones, {len(opts)} individual supports, '
          f'{len(witness)} simultaneous additions (searched up to four).')
    if len(witness)==4:
        for i in reversed(range(21)):
            print(''.join(str((c>>i)&1) for c in (*cols,*witness)))
