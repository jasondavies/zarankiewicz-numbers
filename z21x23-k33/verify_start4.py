"""Verify the complete cover of start 4 at weight 209 on 21 by 23."""
import argparse
import csv
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

from pysat.formula import CNF
from overlap_sat import double_starts, five_templates, initial_rows, next_row, refine, restricted

HERE = Path(__file__).resolve().parent


def bits(row):
    return sum(bit << j for j, bit in enumerate(row))


def check_sixth_partition(prefix, fixed):
    """Test all labelled sixth rows before quotienting columns of equal type."""
    representatives = list(next_row(prefix, fixed))
    assert len(representatives) == 10 and all(pre[5] == 4 for pre, _ in representatives)
    old = [(mask << 19) | bits(row) for mask, row in zip(prefix, fixed)]
    pairs = [a & b for a, b in combinations(old, 2)]
    groups = {}
    for j, col in enumerate(zip(*fixed)):
        groups[col] = groups.get(col, 0) | (1 << j)

    def signature(core):
        return tuple((g & core).bit_count() for g in groups.values())

    actual = set()
    labelled = 0
    for core in range(1 << 19):
        if core.bit_count() < 8:
            continue
        board_row = (4 << 19) | core
        if all((board_row & pair).bit_count() <= 2 for pair in pairs):
            actual.add(signature(core))
            labelled += 1
    assert labelled == 2592
    assert actual == {signature(bits(rows[-1])) for _, rows in representatives}
    assert len(actual) == len(representatives)
    return representatives


def digest(path):
    h = sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def check_proof(cnf, proof, scratch, checker, lrat_checker):
    flags = ['-i', '-w']
    lrat = scratch / 'proof.lrat'
    if lrat_checker:
        flags += ['-L', str(lrat)]
    result = subprocess.run([checker, str(cnf), str(proof), *flags],
                            capture_output=True, text=True)
    if result.returncode or 's VERIFIED' not in result.stdout.splitlines():
        raise RuntimeError(f'DRAT verification failed: {result.stdout[-1000:]} {result.stderr}')
    if lrat_checker:
        result = subprocess.run([lrat_checker, str(cnf), str(lrat)], capture_output=True, text=True)
        if result.returncode or 'c VERIFIED' not in result.stdout.splitlines():
            raise RuntimeError(f'LRAT verification failed: {result.stdout[-1000:]} {result.stderr}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checker', default='drat-trim')
    parser.add_argument('--lrat-check', help='also convert each selected proof to LRAT and recheck it')
    parser.add_argument('--cxx', default='c++')
    parser.add_argument('--template', type=int, help='restrict the replay to one template')
    args = parser.parse_args()
    if not __debug__:
        parser.error('run with assertions enabled')
    folder = HERE / 'start4-proofs'
    with (folder / 'manifest.tsv').open() as f:
        manifest = list(csv.DictReader(f, delimiter='\t'))
    start = double_starts()[4]
    allowed = refine(start)
    assert len(allowed) == 92 and sorted(int(r['template']) for r in manifest if r['sixth']=='') == allowed
    assert sorted((int(r['template']), int(r['sixth'])) for r in manifest if r['sixth']!='') == [(145,i) for i in range(10)]
    if args.template is not None:
        if args.template not in allowed:
            parser.error('template outside the surviving 92')
        manifest = [r for r in manifest if int(r['template']) == args.template]
    fixed_cases = {h: initial_rows(start, five_templates()[h]) for h in allowed}
    sixth = check_sixth_partition(*fixed_cases[145]) if any(r['sixth'] for r in manifest) else []
    with tempfile.TemporaryDirectory() as temp:
        scratch = Path(temp)
        inputs = []
        archived = {}
        empty = 0
        for record in manifest:
            h = int(record['template'])
            prefix, fixed = fixed_cases[h]
            if record['sixth'] != '':
                prefix, fixed = sixth[int(record['sixth'])]
            if record['method'] == 'row-search':
                assert prefix == [15,15,12,12,12,0,1,1,1,1,1,2,2,2,2,4,4,4,9,10,10]
                inputs.append((h, [(m << 19) | bits(row) for m,row in zip(prefix,fixed)]))
            elif record['method'] == 'empty-clause':
                enc = restricted(prefix, fixed, True)
                assert [] in enc.clauses
                cnf = scratch / 'empty.cnf'
                CNF(from_clauses=enc.clauses).to_file(str(cnf))
                assert digest(cnf) == record['cnf_sha256']
                empty += 1
            elif record['method'] == 'drat':
                members = archived.setdefault(record['archive'], {})
                assert record['member'] not in members
                members[record['member']] = (record, prefix, fixed)
            else:
                raise ValueError(record['method'])
        if inputs:
            exe = scratch / 'start4_search'
            subprocess.run([args.cxx, '-std=c++20', '-O3', '-march=native', str(HERE/'start4_search.cpp'),
                            '-o', str(exe)], check=True)
            data = ''.join(' '.join(map(str,[h,*rows]))+'\n' for h, rows in inputs)
            native = subprocess.run([exe], input=data, text=True, capture_output=True)
            if native.returncode:
                raise RuntimeError(f'row search returned {native.returncode}: {native.stderr}')
            summaries = [tuple(map(int,line.split())) for line in native.stdout.splitlines()]
            assert [r[0] for r in summaries] == [h for h,_ in inputs] and all(len(r)==4 for r in summaries)
            for h, first, both, nodes in summaries:
                print(f'{h}: row search exhausted {first} placements of the first three rows '
                      f'and {both} placements of all six ({nodes} tail nodes).', flush=True)
        checked = 0
        for archive, members in sorted(archived.items()):
            seen = set()
            with tarfile.open(folder/archive, 'r|xz') as stream:
                for entry in stream:
                    if entry.name not in members:
                        continue
                    assert entry.isfile() and entry.name not in seen
                    record, prefix, fixed = members[entry.name]
                    cnf, proof = scratch/'case.cnf', scratch/'case.drat'
                    enc = restricted(prefix,fixed,True)
                    CNF(from_clauses=enc.clauses).to_file(str(cnf))
                    with stream.extractfile(entry) as source, proof.open('wb') as out:
                        shutil.copyfileobj(source,out)
                    assert digest(cnf) == record['cnf_sha256'] and digest(proof) == record['proof_sha256']
                    check_proof(cnf, proof, scratch, args.checker, args.lrat_check)
                    seen.add(entry.name)
            assert seen == members.keys()
            checked += len(seen)
            print(f'{archive}: {len(seen)} proofs checked.',flush=True)
    print(f'Verified {len(inputs)} row searches, {empty} explicit empty clauses and {checked} DRAT proofs.')


if __name__ == '__main__':
    main()
