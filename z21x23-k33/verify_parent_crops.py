"""Check every 177-one crop of the stored witnesses and its extension number."""
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from subprocess import run

import networkx as nx
from parent_extensions import extensions, admissible, read_parent

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0,str(ROOT/'z16x18-k33'))
from replay import compile_cpp


def crops(rows):
    # Both orientations matter even for a square whose two parts have the same size.
    for a in (rows,list(zip(*rows))):
        if len(a)<21 or len(a[0])<19:
            continue
        for selected in combinations(range(len(a)),21):
            cols = [sum(int(a[i][j])<<k for k,i in enumerate(selected)) for j in range(len(a[0]))]
            ordered = sorted(cols,key=int.bit_count,reverse=True)
            best = sum(c.bit_count() for c in ordered[:19])
            assert best<=177
            if best<177:
                continue
            cut = ordered[18].bit_count()
            fixed = [c for c in ordered if c.bit_count()>cut]
            for tail in combinations([c for c in ordered if c.bit_count()==cut],19-len(fixed)):
                yield tuple(sorted((*fixed,*tail)))


def graph(cols):
    g = nx.Graph()
    g.add_nodes_from(range(21),part=0)
    g.add_nodes_from(range(21,40),part=1)
    g.add_edges_from((i,21+j) for j,c in enumerate(cols) for i in range(21) if c&(1<<i))
    return g


def same(a,b):
    return nx.is_isomorphic(a,b,node_match=lambda v,w:v['part']==w['part'])


def main(trades):
    classes = []
    sources = [('z19x21-k33',177,1),('z20x21-k33',185,1),('z21-k33',193,2),
               ('z21x22-k33',201,4),('z22-k33',210,20),('z22x23-k33',216,6),('z23-k33',225,10)]
    for d,wt,expected in sources:
        rows = (ROOT/d/f'witness-{wt}.txt').read_text().splitlines()
        seen = Counter()
        for cols in crops(rows):
            g = graph(cols)
            idx = next((i for i,(rep,_) in enumerate(classes) if same(g,rep)),len(classes))
            if idx==len(classes):
                classes.append((g,cols))
            seen[idx] += 1
        assert seen == {int(wt>=216):expected}
    assert len(classes)==2
    for (_,cols),expected in zip(classes,[(3,3),(4,2)]):
        options,packed = extensions(cols)
        assert (len(options),len(packed))==expected
        if len(options)==4:
            pairs = [(a,b) for a,b in combinations(options,2) if admissible((*cols,a,b))]
            assert len(pairs)==2 and set(pairs[0]).isdisjoint(pairs[1])
        print(f'Parent with {len(options)} individually legal columns accepts {len(packed)} together.')
    square = (ROOT/'z23-k33/witness-225.txt').read_text().splitlines()
    example = (HERE/'parent-from-225.txt').read_text().splitlines()
    assert example==[''.join(x for j,x in enumerate(r,1) if j not in (7,11,14,18))
                     for i,r in enumerate(square,1) if i not in (21,23)]
    assert same(graph(read_parent(HERE/'parent-from-225.txt')),classes[1][0])
    grid = [r for i,r in enumerate(square) if i not in (8,12)]
    cols = [sum(int(c)<<i for i,c in enumerate(col)) for col in zip(*grid)]
    hidden = [i for i,c in enumerate(cols) if c.bit_count()==8][:4]
    parent = [c for i,c in enumerate(cols) if i not in hidden]
    assert len(parent)==19 and sum(map(int.bit_count,parent))==175
    pool,added = extensions(parent)
    assert set(cols[i] for i in hidden)<=set(pool) and len(added)==4
    assert admissible((*parent,*added)) and sum(map(int.bit_count,(*parent,*added)))==207
    print('Positive control recovered a four-column extension from 175 to 207.')
    if trades:
        with TemporaryDirectory(prefix='z177-trades-') as folder:
            exe=compile_cpp(HERE/'parent_trades.cpp',Path(folder))
            for idx,(rep,cols) in enumerate(classes):
                for orientation in ('columns','rows'):
                    data=' '.join(map(str,cols))+'\n'
                    result=run([exe,orientation],input=data,text=True,capture_output=True,check=True)
                    counts={}
                    for line in result.stdout.splitlines():
                        tag,*values=line.split()
                        if tag=='case':
                            case=tuple(map(int,values))
                            assert len(case)==19 and sum(map(int.bit_count,case))==177 and admissible(case)
                            assert same(rep,graph(case))
                        elif tag=='level':
                            k,subsets,solutions=map(int,values)
                            assert subsets==comb(19 if orientation=='columns' else 21,k)
                            counts[k]=solutions
                        else:
                            raise RuntimeError(line)
                    assert counts=={k:int(idx==1 and orientation=='columns' and k==6) for k in range(1,7)}
                    print(f'Parent {idx+1}, {orientation}: verified all replacements through six.',flush=True)


if __name__=='__main__':
    from argparse import ArgumentParser
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--trades',action='store_true',help='also exhaust all replacements of up to six parallel lines')
    if not __debug__:
        parser.error('enable assertions')
    main(parser.parse_args().trades)
