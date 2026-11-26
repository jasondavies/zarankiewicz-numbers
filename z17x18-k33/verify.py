"""Check the 143 witness and exclude 145 ones on 17 by 18."""
import argparse
from itertools import combinations
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import sys

HERE = Path(__file__).resolve().parent
SMALL = HERE.parent/'z16x18-k33'
sys.path.insert(0,str(SMALL))
from replay import catalogue, compile_cpp, line_bytes, read_witness, reject, ten_point_check


def cliques(pool, size):
    neighbors = [sum(1<<j for j in range(i+1,len(pool))
                     if (b&pool[j]).bit_count()<=2) for i,b in enumerate(pool)]

    def visit(available, left, picked):
        if not left:
            yield picked
            return
        while available.bit_count() >= left:
            bit = available & -available
            available ^= bit
            i = bit.bit_length()-1
            yield from visit(available & neighbors[i], left-1, picked+(pool[i],))

    return visit((1<<len(pool))-1,size,())


def twelve_points():
    def mask(points):
        return sum(1<<i for i in points)
    pencil = [mask([11,9,3*i,3*i+1,3*i+2]) for i in range(3)]
    pencil += [mask([11,10,i,i+3,i+6]) for i in range(3)]
    pool = [mask(p) for p in combinations(range(11),5)
            if all((mask(p)&b).bit_count()<=2 for b in pencil)]
    assert len(pool)==51 and next(cliques(pool,7),None) is None


def dense_blocks(points, threshold, families, *, load_floor=7, max_deficit=0):
    out = []
    for line in families:
        f = tuple(map(int,line.split()))
        m = len(f)
        if 5*m+4*(17-m)<threshold:
            continue
        pool = [b for b in range(1<<points) if b.bit_count()==4
                and all((b&a).bit_count()<=2 for a in f)]
        for q in range(max(0,threshold-51-2*m), min(17-m,len(pool))+1):
            for fours in cliques(pool,q):
                base = f+fours
                left = 17-len(base)
                needed = threshold-5*m-4*q
                # Two distinct masks of size at most three meet in at most two.
                # A triple can occur once; pairs and smaller blocks may repeat.
                choices = []
                if left:
                    choices = [b for size in range(3,max(-1,needed-3*(left-1)-1),-1)
                               for b in range(1<<points) if b.bit_count()==size
                               and all((a&b).bit_count()<=2 for a in base)]
                def tails(start, k, demand, prefix):
                    if k==0:
                        if demand<=0:
                            yield prefix
                        return
                    for i in range(start,len(choices)):
                        b = choices[i]
                        if k*b.bit_count()<demand:
                            break
                        yield from tails(i+int(b.bit_count()==3),k-1,
                                         demand-b.bit_count(),prefix+(b,))
                for blocks in tails(0,left,needed,base):
                    loads = [sum((b>>j)&1 for b in blocks) for j in range(points)]
                    if min(loads)>=load_floor and sum(max(0,7-v) for v in loads)<=max_deficit:
                        out.append(line_bytes(blocks))
    return out

def main(jobs):
    witness = read_witness(HERE/'witness-143.txt',17,18,143)
    original = (HERE.parent/'z17-k33/witness-138-six.txt').read_text().splitlines()
    assert [f'{b>>1:017b}' for b in witness]==original
    assert [i+1 for i,b in enumerate(witness) if b&1]==[3,5,6,15,17]
    twelve_points()
    ten_point_check()
    with TemporaryDirectory(prefix='z17x18-proof-') as tmp:
        tmp = Path(tmp)
        nine = compile_cpp(HERE.parent/'z16x17-k33/catalogue.cpp',tmp,True)
        outer = compile_cpp(SMALL/'outside_catalogue.cpp',tmp,True)
        five = compile_cpp(HERE/'fives.cpp',tmp,True)
        border = compile_cpp(SMALL/'borders.cpp',tmp)
        lift = compile_cpp(HERE/'outside_eight.cpp',tmp,True)
        assert not dense_blocks(11,76,catalogue(five,11,8))
        tens = dense_blocks(10,71,catalogue(five,10,3))
        reject(border,('inside',10,17,7,8,17,145),tens,24,jobs)
        outside = catalogue(outer,7,65)
        def enough(line):
            b = list(map(int,line.split()))
            return all(sum((x>>i)&1 for x in b)>=8 for i in range(7))
        reject(border,('outside',7,17,10,8,18,145),
               list(filter(enough,outside)),1096,jobs)
        reject(border,('inside',9,17,8,8,17,145),catalogue(nine,17,65,0,7,17),87842,jobs)
        for d, needed, prefix_count, expected in [(8,64,189495,81345),(9,63,51067,824)]:
            base = catalogue(outer,7,needed,d)
            assert len(base)==prefix_count
            lifted = run([lift,str(d)],input=b'\n'.join(base)+b'\n',
                         capture_output=True,check=True).stdout.splitlines()
            reject(border,('outside',8,17,9,8,18,145),lifted,expected,jobs)
    print('143 <= z(17,18;3,3) <= 144.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=4)
    args=parser.parse_args()
    if not __debug__ or args.jobs<1:
        parser.error('enable Python assertions and use a positive job count')
    main(args.jobs)
