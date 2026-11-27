"""Check the shared row layouts and replay the three exceptional (7,7) templates."""
import argparse
import csv
from collections import Counter
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

from pysat.formula import CNF
from overlap_sat import initial_rows, restricted
from overlap_starts import double_starts, five_templates, refine
from verify_209 import compile_cpp
from verify_start4 import check_proof

HERE = Path(__file__).resolve().parent
STARTS = (4, 25, 46, 62)


def aligned_tail(t):
    start = double_starts()[STARTS[t]]
    perm = (0, 1, 2, 3) if t == 0 else (2, 0, 1, 3)
    aligned = [0]*16
    for m, count in enumerate(start):
        mask = sum(1 << perm[j] for j in range(4) if (m >> j) & 1)
        aligned[mask] = count
    assert aligned[:4] == [1+t, 5-t, 4-t, t]
    assert aligned[4:] == [3, 0, 0, 0, 0, 1, 2, 0, 3, 0, 0, 2]
    return [15, 15, 12, 12, 12] + [m for m,n in enumerate(aligned)
                                    if m not in (12, 15) for _ in range(n)]


def replay_sat(records, fixed, scratch, solver, checker):
    for h, methods in records.items():
        for t, method in enumerate(methods, start=1):
            if method not in ('empty', 'drat'):
                continue
            enc = restricted(aligned_tail(t), fixed[h], True)
            if method == 'empty':
                assert [] in enc.clauses
                continue
            cnf, proof = scratch/'case.cnf', scratch/'case.drat'
            CNF(from_clauses=enc.clauses).to_file(str(cnf))
            result = run([solver, str(cnf), str(proof)], capture_output=True)
            if result.returncode != 20:
                raise RuntimeError(f'expected UNSAT for start {STARTS[t]}, template {h}: {result.returncode}')
            check_proof(cnf, proof, scratch, checker, None)
            proof.unlink()
            print(f'Start {STARTS[t]}, template {h}: DRAT checked.', flush=True)


def main(args):
    # With pair 12 chosen, both triples depend only on these six side masks.
    for t in range(len(STARTS)):
        prefix = aligned_tail(t)
        assert [[m for m in prefix if m & 12 == bit] for bit in (4, 8)] == [[4,4,4], [9,10,10]]
    start = double_starts()[4]
    templates = five_templates()
    allowed = refine(start)
    assert len(templates) == 892 and len(allowed) == 92
    fixed = {h: initial_rows(start, templates[h])[1] for h in allowed}
    degrees = {h: tuple(sorted(map(sum, rows[:2]))) for h, rows in fixed.items()}
    assert Counter(degrees.values()) == {(6,7): 86, (6,8): 3, (7,7): 3}
    residual = [h for h in allowed if degrees[h] == (7,7)]
    assert residual == [145, 151, 152]
    template = args.template
    if template is not None and template not in fixed:
        raise ValueError('template outside the shared set of 92')
    selected = residual if template is None else [template]
    records = {}
    if args.direct:
        with (HERE/'shared-tail-search.tsv').open() as src:
            records = {int(r['template']): [r[str(i)] for i in STARTS[1:]]
                       for r in csv.DictReader(src, delimiter='\t')}
        assert sorted(records) == allowed
        assert all(m in ('open', 'row', 'empty', 'drat') for row in records.values() for m in row)
        if template is not None:
            records = {template: records[template]}
        selected = [h for h, methods in records.items() if 'row' in methods]
    data = []
    for h in selected:
        rows = [(m << 19) | sum(bit << j for j,bit in enumerate(row))
                for m,row in zip(aligned_tail(0), fixed[h])]
        data.append(' '.join(map(str, [h, *rows])))
    with TemporaryDirectory(prefix='z209-tails-') as folder:
        exe = compile_cpp(HERE/'start4_search.cpp', Path(folder))
        result = run([exe, '--shared-tails'], input=''.join(line+'\n' for line in data),
                     capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(f'search returned {result.returncode}: {result.stderr}')
        summaries = [list(map(int,line.split())) for line in result.stdout.splitlines()]
        assert [s[0] for s in summaries] == selected and all(len(s) == 7 for s in summaries)
        # Compare against the independently recorded original single-ending search.
        controls = {145: (10,26), 151: (12,540), 152: (88,6680)}
        for h, first, both, *_ in summaries:
            if h in controls:
                assert (first, both) == controls[h]
            print(f'Template {h}: {both} side placements exhausted for all four starts.', flush=True)
        if args.direct:
            replay_sat(records, fixed, Path(folder), args.solver, args.checker)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--template', type=int, help='run one selected template through the joint search')
    parser.add_argument('--direct', action='store_true', help='reproduce completed entries in the optional search table')
    parser.add_argument('--solver', default='cadical')
    parser.add_argument('--checker', default='drat-trim')
    args = parser.parse_args()
    if not __debug__:
        parser.error('enable assertions')
    main(args)
