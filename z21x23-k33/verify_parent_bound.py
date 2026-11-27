"""Verify that a 177-one parent of a 209-one matrix has at most five eight-columns."""
from argparse import ArgumentParser
from collections import Counter
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT/'z17x18-k33'))
from verify import catalogue, cliques, compile_cpp, reject
from verify_209 import compatible_group
sys.path.insert(0, str(ROOT/'z20x21-k33'))
from verify_bounds import compatible_groups


def check_marked_columns(tmp):
    fives = compile_cpp(ROOT/'z17x18-k33/fives.cpp', tmp, True)
    border = compile_cpp(ROOT/'z16x18-k33/borders.cpp', tmp)
    families = [tuple(map(int, line.split())) for line in catalogue(fives,11,7)]
    bases = [f for f in families if len(f)==7]
    assert len(bases)==15
    count = 0
    kept = []
    for base in bases:
        fours = [m for m in range(1<<11) if m.bit_count()==4
                 and all((m & b).bit_count()<=2 for b in base)]
        for extra in cliques(fours,15):
            blocks = base + extra
            count += 1
            loads = [sum((b>>j)&1 for b in blocks) for j in range(11)]
            if min(loads)>=7 and max(loads)<=9:
                assert not compatible_group(blocks,7)
                kept.append(' '.join(map(str,blocks)).encode())
    assert (count,len(kept)) == (168,10)
    reject(border, ('inside',11,22,10,8,22,209,'--gain'), kept,10,1)
    # At q=10 an eight-row meeting every column of degree above ten has load at least 71.
    small = compile_cpp(ROOT/'z18x19-k33/small_points.cpp', tmp, True)
    marks = catalogue(small,8,71,20,8)
    assert len(marks)==41
    reject(border, ('inside',8,20,5,9,10,129,'--gain'), marks,41,1)


def signature(rows,n):
    # With ordered fixed rows, a permutation of columns preserves exactly this multiset.
    return tuple(sorted(sum(((r>>i)&1)<<j for j,r in enumerate(rows)) for i in range(n)))


def layouts(n):
    degrees = (8,9)
    for a,b in combinations_with_replacement(degrees,2):
        for shared in range(max(0,a+b-n),6):
            rows = ((1<<a)-1, (1<<shared)-1 | (((1<<(b-shared))-1)<<a))
            if n==11:
                yield rows
                continue
            for m in range(1<<n):
                if not b <= m.bit_count() <= 9:
                    continue
                if max((r&m).bit_count() for r in rows)>5 or (rows[0]&rows[1]&m).bit_count()>2:
                    continue
                yield (*rows,m)


def check_certificate(entry):
    n,rows,den = entry['n'],entry['rows'],entry['den']
    assert type(den) is int and den>0
    assert all(0<=r<1<<n for r in rows)
    tags = [sum(((r>>i)&1)<<j for j,r in enumerate(rows)) for i in range(n)]
    weights = {tuple(map(int,k.split(','))): v for k,v in entry['weights'].items()}
    assert all(type(v) is int and v>=0 and len(k) in (1,3) for k,v in weights.items())
    # A positive triple price uses an upper bound. A negative point price uses a lower bound.
    prices = []
    for arity,sign in ((1,-1),(3,1)):
        for points in combinations(range(n),arity):
            price = sign*weights.get(tuple(sorted(tags[j] for j in points)),0)
            if price:
                prices.append((sum(1<<j for j in points),price,9 if arity==1 else 2))
    available = sum(v*(bound-sum((m&r)==m for r in rows)) for m,v,bound in prices)
    best = 0
    for s in range(1<<n):
        if s.bit_count()>10 or any((s&r).bit_count()>5 for r in rows):
            continue
        if any((s&r&t).bit_count()>2 for r,t in combinations(rows,2)):
            continue
        cost = sum(v for m,v,_ in prices if s&m==m)
        best = max(best,den*s.bit_count()-cost)
    return sum(r.bit_count() for r in rows) + (available+(21-len(rows))*best)//den


def check_five_eights(tmp, jobs):
    small = compile_cpp(ROOT/'z18x19-k33/small_points.cpp', tmp, True)
    border = compile_cpp(ROOT/'z16x18-k33/borders.cpp', tmp)
    marks = catalogue(small,8,69,20,8)
    assert len(marks)==181521
    reject(border, ('inside',8,20,6,9,10,137,'--gain'), marks,181521,jobs)
    nine=[]
    for line in marks:
        blocks=tuple(map(int,line.split()))
        eights=list(compatible_groups(blocks,8))
        if not eights:
            continue
        for chosen in (*eights,*compatible_groups(blocks,9)):
            augmented=[b | (((chosen>>i)&1)<<8) for i,b in enumerate(blocks)]
            nine.append(' '.join(map(str,augmented)).encode())
    assert len(nine)==209
    reject(border, ('inside',9,20,5,9,10,137,'--gain'), nine,209,jobs)
    print('A full matrix with nine eight-columns requires row deficit at least seven.')


def main(args):
    entries = json.loads((HERE/'high-column-bounds.json').read_text())
    for n in (11,12):
        cases = [e for e in entries if e['n']==n]
        sigs = {signature(e['rows'],n) for e in cases}
        assert sigs=={signature(r,n) for r in layouts(n)} and len(sigs)==len(cases)==(1 if n==11 else 10)
        bounds = [check_certificate(e) for e in cases]
        assert max(bounds)==(109 if n==11 else 120) and max(bounds)<8*n+25
        print(f'{n} high columns: {len(cases)} layouts, upper bound {max(bounds)}, need {8*n+25}.')
    # At ten full eight-columns the thirteen high columns have weight 129.
    n=13
    all_three = {signature(r,n):r for r in layouts(n)}
    three = [e for e in entries if e['n']==n and len(e['rows'])==3]
    ruled_out = {signature(e['rows'],n) for e in three}
    assert len(all_three)==44 and len(ruled_out)==len(three)==35 and ruled_out<=all_three.keys()
    assert max(map(check_certificate,three))<129
    four_keys=set()
    for key in all_three.keys()-ruled_out:
        rows=all_three[key]
        for m in range(1<<n):
            if not rows[-1].bit_count()<=m.bit_count()<=9 or any((m&r).bit_count()>5 for r in rows):
                continue
            if all((m&r&t).bit_count()<=2 for r,t in combinations(rows,2)):
                four_keys.add(signature((*rows,m),n))
    four = [e for e in entries if e['n']==n and len(e['rows'])==4]
    assert four_keys=={signature(e['rows'],n) for e in four} and len(four_keys)==len(four)==67
    assert max(map(check_certificate,four))==126
    print('13 high columns: 9 of 44 three-row layouts left; all 67 fourth-row layouts excluded.')
    with TemporaryDirectory(prefix='z177-deficit-') as folder:
        check_marked_columns(Path(folder))
        if args.frontier:
            check_five_eights(Path(folder),args.jobs)
    print('At most nine eight-one columns in the full matrix and at most five in the parent.')


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--frontier',action='store_true',help='also replay the five-eight-column parent restriction')
    parser.add_argument('--jobs',type=int,default=4,help='workers for the optional frontier exhaustion')
    args=parser.parse_args()
    if not __debug__ or args.jobs<1:
        parser.error('run with assertions enabled and use at least one worker')
    main(args)
