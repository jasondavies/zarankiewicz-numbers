"""Replay the 16 by 17 K3,3-free lower and upper bounds."""
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

from completions import Extensions

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'z17-k33'))
from ten_columns import check_128_core, four_cliques, possible_fives


def witness():
    lines = (HERE / 'witness-132.txt').read_text().splitlines()
    assert len(lines)==16 and all(len(r)==17 and set(r)<={'0','1'} for r in lines)
    assert sum(r.count('1') for r in lines)==132
    cols = list(combinations(range(17),3))
    for a,b,c in combinations(lines,3):
        common = [x==y==z=='1' for x,y,z in zip(a,b,c)]
        assert not any(common[i] and common[j] and common[k] for i,j,k in cols)
    print('132 ones, all 380800 choices of a 3 by 3 checked', flush=True)


def column_bound():
    check_128_core()
    counts = Counter()
    for blocks in possible_fives([]):
        m = len(blocks)
        if m >= 5:
            assert next(four_cliques(blocks, 69-48-2*m), None) is None
            counts[m] += 1
    assert counts == {5:12,6:12}
    print('Ten-point check, families tested by number of five-sets:', dict(counts), flush=True)


def verify(directory):
    binary = directory / 'catalogue'
    run(['c++','-O3','-std=c++20',HERE/'catalogue.cpp','-lnauty','-o',binary], check=True)
    # These two projections also have independently checked completions at 130.
    controls = {'row':(15,51,89,108,154,165,198,240,312,330,340,353,396,401,418),
                'column':(3,23,57,106,154,165,198,201,240,269,306,323,344,356,404,424)}
    for mark, expected in [('row',29),('column',4201)]:
        output = run([binary,mark], check=True, capture_output=True, text=True).stdout
        entries = [tuple(map(int,line.split())) for line in output.splitlines()]
        assert len(entries)==len(set(entries))==expected
        column = mark=='column'
        engine = Extensions(16 if column else 15)
        assert engine.complete(controls[mark], column, 130) is not None
        for blocks in entries:
            if (rows := engine.complete(blocks, column)) is not None:
                raise AssertionError(f'Valid weight-133 matrix in row masks: {rows}')
        print(f'{mark}: all {expected} projections excluded at 133', flush=True)


if __name__=='__main__':
    if not __debug__:
        raise RuntimeError('Run with Python assertions enabled')
    witness()
    column_bound()
    with TemporaryDirectory(prefix='z16x17-') as tmp:
        verify(Path(tmp))
    print('Exact value 132.')
