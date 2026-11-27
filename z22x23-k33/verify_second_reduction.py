"""Check the low-column condition for extremal 193-one squares or the 209 long-line branch."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
import argparse
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'z16x18-k33'))
from replay import read_witness,compile_cpp,catalogue
sys.path.insert(0,str(ROOT/'z20x21-k33'))
from extend_eights import transpose,admissible
from verify_four_column_cover import marked_batch


def control(marked):
    rows=read_witness(ROOT/'z22-k33/witness-210.txt',22,22,210)
    cols=transpose(rows,22)
    for multiplier in (3,4):
        def score(r):
            return multiplier*r.bit_count()+sum(c.bit_count()-9 for j,c in enumerate(cols) if r>>j&1)
        r=max(rows,key=score)
        points=[j for j in range(22) if r>>j&1]
        blocks=[sum((x>>j&1)<<i for i,j in enumerate(points)) for x in rows if x!=r]
        data=' '.join(map(str,blocks))+'\n'
        out=run([marked,'0',str(len(points)),'210',str(multiplier),'12','12','22','22','9','-1',
                 '--nine-column-cores'],input=data,text=True,capture_output=True,check=True).stdout.splitlines()
        assert out[-1]=='enumerated 1 cores 1 profiles 1'
        tag,*fields=out[0].split()
        recovered=tuple(map(int,fields))
        assert tag=='core' and len(recovered)==22 and max(recovered)<1<<22
        assert sum(c.bit_count() for c in recovered)==210 and admissible(recovered)


def replay(part,jobs,cache):
    if cache: cache.mkdir(exist_ok=True,parents=True)
    with TemporaryDirectory(prefix='joint-parent-') as work:
        tmp=Path(work)
        five=compile_cpp(ROOT/'z17x18-k33/fives.cpp',tmp,True)
        ten=compile_cpp(ROOT/'z18-k33/ten_points.cpp',tmp,True)
        border=compile_cpp(ROOT/'z16x18-k33/borders.cpp',tmp)
        marked=compile_cpp(ROOT/'z18x19-k33/marked_core.cpp',tmp)
        digest=sha256(marked.read_bytes()).digest()
        control(marked)
        def marks(n,blocks,load,cap):
            fives=catalogue(five,n,max(1,load-4*blocks))
            if load==4*blocks: fives.insert(0,b'')
            return run([ten,*map(str,(cap,blocks,load,8,n))],input=b'\n'.join(fives)+b'\n',
                       capture_output=True,check=True).stdout.splitlines()
        def exact(mark,load):
            return [b for b in mark if sum(int(x).bit_count() for x in b.split())==load]
        def reject_marked(cases,params,batches):
            def check(i):
                assert not marked_batch(marked,params,cases[i::batches],cache,digest,'--nine-column-cores')
            with ThreadPoolExecutor(jobs)as pool:list(pool.map(check,range(batches)))
            print(f'{len(cases)} marked projections excluded at weight {params[2]}.',flush=True)
        if part=='209':
            data=marks(11,21,89,9)
            assert len(data)==36420
            data=exact(data,89)
            assert len(data)==36171
            reject_marked(data,(0,11,209,3,13,13,22,22,9,-1),120)
        if part=='balanced':
            candidates=marks(10,21,84,9)
            assert len(candidates)==786700
            candidates=exact(candidates,84)
            assert len(candidates)==780162
            seven=compile_cpp(HERE/'seven_tens.cpp',tmp)
            def screen(i):
                shard=candidates[i::1024]
                res=run([seven],input=b'\n'.join(shard)+b'\n',capture_output=True,check=True)
                passed=res.stdout.splitlines()
                assert res.stderr.decode().strip()==f'{len(shard)} marks, {len(passed)} survive'
                assert set(passed)<=set(shard)
                return passed
            with ThreadPoolExecutor(jobs) as pool:
                survivors=[b for part_result in pool.map(screen,range(1024)) for b in part_result]
            assert len(survivors)==34
            out=run([seven,'--control'],input=survivors[0]+b'\n',capture_output=True,check=True)
            tag,*fields=out.stdout.split()
            cols=tuple(map(int,fields))
            assert tag==b'placement' and len(cols)==17 and admissible(cols)
            assert all(0<=x<1<<22 for x in cols)
            assert all(x>>21 for x in cols[:10]) and all(x<1<<21 and x.bit_count()==10 for x in cols[10:])
            reject_marked(survivors,(0,10,209,3,11,11,22,22,9,-1),1)
        if part=='193':
            heavy=marks(10,20,82,12)
            # Up to four units of excess; the maximum load is twelve.
            assert len(heavy)==159
            unit=exact(marks(10,20,81,9),81)
            assert len(unit)==5487
            for data,cap in ((heavy,11),(unit,12)):
                out=run([border,'inside','10','20','11','9',str(cap),'193','--enumerate'],
                        input=b'\n'.join(data)+b'\n',capture_output=True,check=True)
                assert out.stdout.splitlines()==[f'enumerated {len(data)}'.encode()]
            zero=marks(10,20,80,8)
            assert len(zero)==79801
            reject_marked(zero,(0,10,193,4,4,16,21,21,8,-1),160)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('part',choices=('193','209','balanced'))
    parser.add_argument('--jobs',type=int,default=4)
    parser.add_argument('--cache',type=Path)
    args=parser.parse_args()
    if not __debug__ or args.jobs<1:parser.error('enable assertions and use a positive job count')
    replay(args.part,args.jobs,args.cache)
