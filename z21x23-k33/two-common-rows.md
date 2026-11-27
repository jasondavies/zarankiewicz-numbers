# Two rows common to four eight-one columns

Start 4 has since been excluded. The counts and timeouts below record the earlier pilot. The current cover contains 5,589 starts after a further reduction by changing the choice of marked columns. [Row-deficit proof](row-deficit.md) [Complete proof and replay](start4.md)

At weight 209 there are 143 four-column starts in which two rows contain all four marked columns. The counting argument below excludes 20 whole starts. This leaves 123 in this group and 5,664 of the original 5,684 across all groups. A single matrix can give more than one start. These counts measure the size of the cover and say little about the fraction of search time remaining. The bounds are still $207\le z(21,23;3,3)\le209$. [Initial reduction and smaller bounds](README.md)

## A column cannot support two groups of three

Call the two common rows $A,B$, the other 19 rows ordinary, and the 19 unmarked columns the core. Each ordinary row contains at most two marks, since $A,B$ already contain every triple of marks. Every ordinary row has at least eight ones in the core. Indeed an eight-row avoids all eight-columns, a nine-row meets at most one, and every other row has degree at least ten. The core has exactly 177 ones. Let $p$ be the combined core degree of $A,B$. Removing them leaves at most 164 on $19\times19$, so $p\ge13$.

Suppose that three ordinary rows $X$ contain a pair of marks $i,j$ and three ordinary rows $Y$ contain a different pair $i,k$. The triples are disjoint and both lie on $i$. For a core column containing $d$ of $A,B$, its capacity on $X$ is $2-d$, since the column and the two marks $i,j$ may have at most two rows in common. The same holds for $Y$ using $i,k$. On each of $X,Y$, capacity over all core columns is $38-p$ and demand is at least 24. If $p>14$ this is already impossible. Otherwise each triple can miss capacity at most $14-p$ times.

Let $c$ core columns contain both $A,B$. Exactly $19-p+c$ contain neither. At least $19-p+c-2(14-p)=p+c-9\ge4$ of these contain two rows of $X$ and two of $Y$. Two such columns using the same pair in $X$ also share a row in $Y$, since two pairs of a three-element set intersect. Together with $i$ they give a forbidden all-ones $3\times3$. Thus there are at most three such columns, a contradiction.

The 20 excluded start IDs are 1, 9, 23, 28, 44, 47, 50, 52, 55, 60, 78, 98, 99, 100, 103, 109, 115, 116, 119 and 120. IDs start at zero after filtering the four-column enumerator to the 143 starts with two common rows. [Enumerator](four_columns.py) · [Counting check](overlap_starts.py)

## Fixing five rows

Of the 123 starts left in this group, 75 have a pair of marked columns containing a triple $X$ of ordinary rows. Fix these three rows and $A,B$. Each core column contains at most two of the five fixed rows. They require at least $13+3\cdot8=37$ of 38 available incidences. Every core column therefore contains a pair of fixed rows, with the possible exception of one column containing a singleton.

Both $A,B$ have core degree at least six, since deleting just one leaves at most 171 on $20\times19$. Their unordered core degrees are consequently $(6,7),(6,8)$ or $(7,7)$. Each row in $X$ has core degree eight, except that one can have nine. Two full rows can share at most six columns. Seven shared columns would need at least 56 ones but the two rows and the other nineteen rows could supply at most $14+19\cdot2=52$. Thus the pair type $AB$ occurs at most twice in the core and each other pair at most four times.

Enumerating type multiplicities up to permutations of $A,B$, permutations of $X$, and permutations of core columns gives 892 templates. Each of the two chosen marks contains three further ordinary rows. Each of these rows can use at most one column of any pair type, since it shares this mark with both endpoints. The replay checks whether each triple separately can place eight ones per row, respecting its triple intersections with the fixed rows and within the triple. Failing this necessary test excludes a template. For start 4, both triples pass on exactly 92 templates. The same set of 92 identifiers was obtained with an independent C++ implementation during the pilot. [Five-row enumerator](overlap_starts.py)

### Degree bounds used by the completion solver

The 19 ordinary rows have at least eight core entries apiece. On these rows each core column has at least $21-p$ entries, since deleting it leaves at most 156 ones on $19\times18$. Two core columns share at most five ordinary rows. Six shared ordinary rows would require at least 48 core entries and have room for only $12+17\cdot2=46$. Likewise, when $p=13$ two ordinary rows cannot share six core columns, which would require 48 entries on ordinary rows against the same capacity of 46. When $p=14$ they cannot share seven, which would require 49 against a capacity of 48. [The 156 bound](../z18x19-k33/README.md)

For two core columns, the rows common to both can together use at most 34 entries in the other 17 core columns. Each shared fixed row of core degree $d$ uses $d-2$ of that budget, and each shared unknown row uses at least six. For a marked column and a core column the corresponding budget is 36, with costs $d-1$ and at least seven. These inequalities give cardinality constraints on just the unknown cells. Grouping core columns with the same pattern of fixed rows gives additional lower bounds on how many entries each remaining row must supply in the group.

## Local completion benchmark

The full encoding tested each of the 143 four-column starts with Glucose 4 and a two-second solving cutoff. All 143 timed out, using 302.05 CPU seconds in aggregate including construction. A positive control took 21 rows of the stored 225-one square, hid four whole columns and reconstructed their total weight. The model passed a direct check of all row triples. The control concerns a smaller weight. [Control witness](../z23-k33/witness-225.txt)

| Start 4 completion experiment | Cases run | Solver cutoff per case | UNSAT |
| --- | ---: | ---: | ---: |
| Fix five rows in the full encoding | 92 | 2 s | 1 |
| Eliminate fixed rows and add degree and pair bounds | 92 | 3 s | 62 |
| Add column-group capacity bounds on the remaining cases | 30 | 15 s | 23 |
| Count row incidences jointly inside equal column types | 7 | 75 s | 2 |
| Same grouped pilot formula, Kissat 4.0.4 | 5 | 150 s | 1 |

In total SAT solvers returned UNSAT for **88 distinct templates out of 92**. The four still open for start 4 are **145, 150, 151 and 152**. No full matrix was found. The UNSAT entries are solver results without retained proof traces. The 20 whole-start exclusions above have a separate counting proof. The 88 template results refine just one of the 123 surviving starts.

The runs used a Ryzen 7 9700X and python-sat 1.9.dev15. The TSV records the pilot encoding and time for each case. The first four encodings include construction in the recorded elapsed times. The grouped Glucose timing covers its solving call, and the Kissat cutoff covers the subprocess including construction. The replay below packages the strengthened encodings. Clause ordering and hardware affect which cases finish at short cutoffs. [Per-case results](overlap-benchmark.tsv) · [SAT replay and DIMACS exporter](overlap_sat.py)

### Replay

Run from this directory. The enumeration uses the Python standard library. The SAT runs also require python-sat.

```sh
python3 overlap_starts.py
python3 overlap_sat.py --control --seconds 15
python3 overlap_sat.py --seconds 2 --jobs 4
python3 overlap_sat.py --start 4 --refine --grouped --seconds 15 --jobs 4
python3 overlap_sat.py --start 4 --template 145 --grouped --dimacs /tmp/start4-145.cnf
```

Each of the four unresolved templates admits ten placements for a chosen sixth row up to permutations within fixed column types. Two more Glucose runs, at five and eight seconds per placement, returned UNSAT for 15 distinct placements out of 40. The surviving placement IDs are listed below. Both implementations used the same four lists of ten placements in identical order.

| Template | Sixth-row placements still open |
| ---: | --- |
| 145 | 6, 7, 8 |
| 150 | 2, 3, 4, 5, 6, 7, 8 |
| 151 | 1, 4, 5, 6, 7, 8 |
| 152 | 0, 1, 2, 3, 4, 5, 6, 7, 8 |

For any selected template, adding `--split` to a solving command enumerates placements of one further row up to permutations within each fixed column type. These placements cover every completion of the template. The same templates and splits can be compared across budgets or used for proof-logging runs.

Use `--sixth ID` with `--template` to solve or export an individual placement.
