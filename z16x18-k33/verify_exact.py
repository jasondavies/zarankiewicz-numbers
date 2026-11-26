"""Recompute the 16 by 18 exclusion at 138. Run with assertions enabled."""
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
from replay import (HERE, catalogue, compile_cpp, controls, read_witness, regular_ten_rows,
                    reject, ten_point_check)


def main(jobs):
    rows = read_witness(HERE/'witness-137.txt',16,18,137)
    ten_point_check()
    with TemporaryDirectory(prefix='z16x18-proof-') as tmp:
        tmp = Path(tmp)
        nine = compile_cpp(HERE.parent/'z16x17-k33/catalogue.cpp',tmp,True)
        outside = compile_cpp(HERE/'outside_catalogue.cpp',tmp,True)
        border = compile_cpp(HERE/'borders.cpp',tmp)
        controls(border, rows)
        reject(border, ('inside',9,15,9,6,8,138), catalogue(nine,15,59,4,5,7),9396,jobs)
        reject(border, ('inside',10,15,8,8,8,138), regular_ten_rows(),2244,jobs)
        reject(border, ('inside',9,17,7,6,17,138), catalogue(nine,17,66,2,5,17),38442,jobs)
        for k,threshold,expected in [(7,64,280850),(6,56,229465),(5,48,37219)]:
            reject(border, ('outside',k,17,16-k,6,18,138),
                   catalogue(outside,k,threshold),expected,jobs)
    print('Exact value 137.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=4)
    args=parser.parse_args()
    if not __debug__ or args.jobs<1:
        parser.error('enable Python assertions and use a positive job count')
    main(args.jobs)
