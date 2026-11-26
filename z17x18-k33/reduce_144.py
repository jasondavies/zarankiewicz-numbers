"""At weight 144 only maximum column degree nine survives; column pairs share at most five rows."""
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
from verify import HERE, SMALL, catalogue, cliques, compile_cpp, dense_blocks, line_bytes, reject, twelve_points
from replay import ten_point_check


def with_six(families):
    out = []
    for line in families:
        f = tuple(map(int,line.split()))
        m = len(f)
        for h in range(1<<11):
            if h.bit_count()!=6 or any((h&b).bit_count()!=2 for b in f):
                continue
            fours = [b for b in range(1<<11) if b.bit_count()==4 and (h&b).bit_count()==2
                     and all((b&a).bit_count()<=2 for a in f)]
            for q in range(max(0,21-2*m),17-m):
                for selection in cliques(fours,q):
                    blocks = (h,)+f+selection
                    assert len(blocks)==17  # All surviving cliques fill the projection.
                    loads = [sum((b>>j)&1 for b in blocks) for j in range(11)]
                    if (sorted(v for j,v in enumerate(loads) if h>>j&1)==[6]*4+[7]*2
                            and all(v>=7 for j,v in enumerate(loads) if not (h>>j&1))):
                        out.append(line_bytes(blocks))
    return out


def main(jobs):
    twelve_points()
    ten_point_check()
    with TemporaryDirectory(prefix='z17x18-144-') as tmp:
        tmp=Path(tmp)
        nine=compile_cpp(SMALL.parent/'z16x17-k33/catalogue.cpp',tmp,True)
        five=compile_cpp(HERE/'fives.cpp',tmp,True)
        outer=compile_cpp(SMALL/'outside_catalogue.cpp',tmp,True)
        border=compile_cpp(SMALL/'borders.cpp',tmp)
        reject(border,('inside',9,16,9,8,8,144),catalogue(nine,16,63,0,7,7),10,jobs)
        reject(border,('outside',5,17,12,7,18,144),catalogue(outer,5,50,7),310,jobs)
        f11=catalogue(five,11,5)
        good=dense_blocks(11,75,f11,load_floor=6,max_deficit=4)
        reject(border,('inside',11,17,6,7,17,144),good,10577,jobs)
        reject(border,('inside',11,17,6,8,17,144),with_six(f11),16,jobs)
        reject(border,('outside',7,17,10,7,18,144),catalogue(outer,7,64,7),277051,jobs)
        good=dense_blocks(10,71,catalogue(five,10,3),load_floor=6,max_deficit=4)
        assert len(good)==82422
        canon=run([five,'10','unique'],input=b'\n'.join(good)+b'\n',
                  check=True,capture_output=True).stdout.splitlines()
        reject(border,('inside',10,17,7,7,17,144),canon,1887,jobs)
    print('Every 144-one candidate has maximum column degree nine and column codegrees at most five.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=4)
    args=parser.parse_args()
    if not __debug__ or args.jobs<1:
        parser.error('enable Python assertions and use a positive job count')
    main(args.jobs)
