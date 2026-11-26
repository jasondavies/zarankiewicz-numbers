# The 16 × 17 Zarankiewicz number for K₃,₃ is 132

A 16 × 17 binary matrix can have **132 ones** while avoiding an all-ones 3 × 3 submatrix. Every such matrix with at least 133 ones contains an all-ones 3 × 3. The selected rows and columns may be anywhere in the matrix.

The [proof PDF](z16x17-exact.pdf) includes the matrix. The [witness](witness-132.txt) is obtained by deleting the six-one row of the [17 × 17 construction](../z17-k33/witness-138-six.txt). The verifier checks all 380,800 choices of three rows and three columns. Afrasyab had already established the lower bound and recorded the interval from 132 to 133. A subsequent SAT search reported unresolved branches at maximum row degrees nine and ten. [Afrasyab, §3](https://arxiv.org/html/2608.08154v1) · [Earlier SAT search](https://slopdealer.com/research/papers/ml-091/)

## Upper bound

Suppose a matrix with exactly 133 ones exists. Deleting individual ones from any heavier example would give such a matrix. Write the degree of a row or column for its number of ones.

**Minimum degrees.** Deleting one or two rows and using the upper bounds 126 for 15 × 17 and 118 for 14 × 17 shows that each row has degree at least seven and at most one row has degree seven. Every column has degree at least five since the 16 × 16 maximum is 128. At degree five, deleting that column leaves the unique extremal 128-one square. Testing all 4,368 five-subsets against a representative, in both orientations, shows that none can be appended. Thus every column has degree at least six. These are the only external numerical bounds and uniqueness assertion needed. [Collins et al., Table 4](https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf)

**Every column has degree at most nine.** A pair of columns cannot share six rows. These rows contain at least 47 ones, while the two columns account for twelve on them and the other fifteen columns for at most thirty. Now mark any ten entries of a column of degree at least ten. The other sixteen columns restrict to sets of size at most five on the ten points, with pairwise intersections at most two. Their total size is at least 69, since the ten rows have at least 79 ones.

Let $m$ be the number of five-sets and $q$ the number of four-sets. The sign vectors that equal $+1$ on a five-set and $-1$ elsewhere have squared norm ten and pairwise inner product at most $-2$. The squared norm of their sum is at most $10m-2m(m-1)$, so $m\le6$. The projected total is at most $64+m$, forcing $m\ge5$. It is also at most $48+2m+q$. For $m=5$ this requires at least eleven four-sets, and for $m=6$ it requires at least nine. Enumerating the five-sets successively, up to permutations of points with identical previous incidences, gives twelve generated families in each case. The verifier exhausts the compatible four-sets in each family and finds no compatible selection of the required size.

**Split on a nine-column.**

- **If a nine-column exists**, mark it. Its nine incident rows are the points. Each of the sixteen other columns gives a block on these points, of size at most five. Two blocks share at most two points because the marked column supplies their third common column. The point loads (degrees excluding the marked column) are at least six, with at most one unit of total deficit below seven. Thus the blocks have total size at least 62. A point may occur in any number of the sixteen blocks, subject to these constraints. In particular, this branch allows rows of degree ten and higher.
- **If every column has degree at most eight**, the total column deficit below eight is exactly three. Six columns would then contain at least 45 ones, whereas two rows covering those columns and the remaining fourteen rows could supply at most 40. Thus any two rows share at most five columns. If a row contained ten chosen entries, the other fifteen rows would supply at least 67 ones on those columns. Their restrictions have size at most five and intersection at most two. The same sign-vector bound permits at most six five-sets, so they can supply at most $15\cdot4+6=66$ ones. This excludes a ten-row. Since $133>16\cdot8$, a nine-row exists. Mark it. Its nine incident columns are now points, and the other fifteen rows are blocks with sizes at most five and pair intersections at most two. The point loads are five through seven with total deficit below seven at most three. Their sum is at least 60.

## Exhaustive check

The catalogue generator chooses a distinguished point occurring in a maximum number $p$ of four-blocks. If there are $q$ four-blocks, then $4q\le9p$. Removing that point from its four-blocks leaves triples on eight points with pairwise intersections at most one. Each of the eight points can occur in at most three triples, so $p\le8$. The generator enumerates these triple families and their orbits under all permutations of the eight points. It then adds five-blocks, the remaining four-blocks, and finally blocks of size at most three. Four five-blocks would have twenty incidences on nine points, forcing at least thirteen pairwise intersections counted with multiplicity where at most twelve are available. Therefore there are at most three five-blocks. Repetitions of blocks of size zero, one, and two are included. At every completed large-block stage and again at the end, an isomorphism key records the actual relabelled multiset of blocks.

The nine points now specify nine complete lines. All extra lines avoid the marked entry position. In the column case, seven more rows must be chosen on sixteen positions. Every weight from seven through sixteen is allowed. In the row case, eight more columns must be chosen on fifteen positions, each of weight six through eight. Extra lines can be chosen without replacement. Two identical extra rows of weight $d$ would give $6d\le2d+28$ by summing their columns, hence $d\le7$, while at most one row has degree seven. Two identical extra columns of degree at least six are excluded by the column-pair bound above.

For each pair of fixed lines, the checker removes every candidate containing three common positions of that pair. Each time it selects another line, it applies the same test to the newly fixed pairs. It branches on the largest remaining weight and prunes when too few lines of sufficient weight can coexist to reach the required total. A complete selection would reconstruct the 133-one matrix.

| Marked line | Other blocks on its nine points | Distinct projections | Completions with 133 ones |
|---|---:|---:|---:|
| Column | 16 | 4,201 | 0 |
| Row | 15 | 29 | 0 |

The two cases exhaust the possibilities, proving $z(16,17;3,3)=132$. The rectangular calculation searches directly for the 133-one matrix. The square-extension question is therefore unnecessary.

## Replay

From this directory, with Python 3.10 or newer, a C++20 compiler named `c++`, and the nauty development headers and library installed, run

```sh
python3 verify_exact.py
```

The replay uses the [ten-point routines](../z17-k33/ten_columns.py) and [128-one core representative embedded in the previous witness](../z17-k33/bordered-137.txt). It compiles [the catalogue generator](catalogue.cpp) in a temporary directory and checks every projection with [the bitset completion search](completions.py). Both orientations also have a positive control at weight 130. A second implementation derived from the square search was used during the calculation and produced the same two catalogues and exclusions.

As a further consequence, $z(16,18;3,3)\le139$. A 140-one matrix on eighteen columns has a column of degree at most seven. Deleting it would leave at least 133 ones on seventeen columns.
