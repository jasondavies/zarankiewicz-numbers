# An independent proof that the 16 × 18 maximum is 137

Jiuzeng Wei released an exhaustive proof of this value on 26 November 2026. This directory gives a second proof using the two sides of a marked line. The lower witness extends Hou’s 132-one matrix by the row `111000101000000000`. Direct inspection of the 560 triples of rows checks the witness. [Wei’s archive](https://doi.org/10.5281/zenodo.24553293) · [Hou’s matrix](https://github.com/ShengtengHou/finite-zarankiewicz-seven-values/blob/main/verification/witnesses/z1518_132.txt) · [Witness](witness-137.txt)

## Degree bounds at weight 138

It suffices to exclude exactly 138 ones, since erasing ones preserves freeness. Each column has degree at least six by the [16 × 17 upper bound of 132](../z16x17-k33/README.md). Each row has degree at least six, from the 15 × 18 upper bound of 132. The row degrees have total deficit at most two below eight. Indeed, a six and a seven would leave at least 125 on 14 rows, and three sevens would leave 117 on 13 rows. The corresponding ceilings are 124 and 116. All the small-rectangle ceilings below come from [Collins et al., Table 4](https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf).

Two columns cannot share six rows. Those rows have at least 46 ones, but the two columns supply twelve and the sixteen remaining columns supply at most two each. Two rows cannot share seven columns either. The seven columns would contain at most 42 ones, leaving at least 96 on an 11 × 16 rectangle whose ceiling is 92.

Mark a column with degree $t$. Restrict each other column to the $t$ marked rows. The resulting seventeen blocks have sizes at most five, and two blocks intersect in at most two points. Writing $S$ for the sum of block sizes, we have $7t-2\le S\le85$. Hence $t\le12$. The rows outside the marked column form a $(16-t)\times17$ matrix with $138-t-S$ ones.

## Columns of degrees nine to twelve

- **Twelve.** The four outside rows have at most 42 ones. A column of size $a$ there satisfies $a\le2+\binom a3$, and each of the four row triples occurs at most twice. Thus $S\ge84$, requiring at least sixteen five-blocks. A point can lie in at most six five-blocks. Seven would leave seven four-sets on eleven points with pairwise intersections at most one. Distributing their 28 incidences as evenly as possible already gives 23 pair intersections, exceeding 21. Double-counting the five-block incidences gives at most $\lfloor12\cdot6/5\rfloor=14$ blocks.
- **Eleven.** There can be at most eleven five-blocks. Twelve would put 60 incidences on eleven points, forcing at least 135 pair intersections against a capacity of 132. Thus $S\le4\cdot17+11=79$, and the five outside rows have at least 48 ones.
- **Ten.** On ten points the balanced sign vectors of two distinct five-blocks have inner product at most $-2$. The squared norm of the sum gives at most six five-blocks. Write $m,q$ for the numbers of fives and fours. If $m\le4$, then $S\le72$. If $m=5,6$, the existing [ten-point check](../z17-k33/ten_columns.py) excludes even $19-2m$ mutually compatible fours. Since $S\le51+2m+q$, the same bound of 72 follows. The six outside rows therefore have at least 56 ones.
- **Nine.** For $S\ge66$ enumerate the blocks on the marked rows directly. Each point has load at least five, with total deficit at most two below seven. For $S\le65$ the seven outside rows have at least 64 ones.

## Every column has degree at most eight

The total column deficit below eight is six. Six columns carry at least 42 ones, so two rows cannot cover all six, as that would allow at most $12+2\cdot14=40$. If a row contains ten chosen columns, the other fifteen rows restrict to blocks of size at most five with intersections at most two. Their total is at least $70-6=64$. The ten-point check above rules out $m\ge5$ at this weight since $S\le45+2m+q$. Equality therefore requires precisely four fives and eleven fours. Every unit of column deficit lies in the ten selected columns. A larger row would allow choosing ten that omit a deficient column, so the row has exactly ten entries. All eight outside columns have weight eight.

Otherwise the maximum row degree is nine. At least ten rows have degree nine. Sum the column deficits over the entries in these rows. Even over all rows the sum is at most $6\cdot7=42$. Some nine-row therefore contains at most four units of deficit. Its nine incident columns have loads from five through seven after removing the marked row, totalling at least 59.

## Replaying the search

| Mark | Enumerated side | Projections checked | Completions at 138 |
|---|---|---:|---:|
| Nine-row | Inside | 9,396 | 0 |
| Ten-row | Inside | 2,244 | 0 |
| Nine-column | Inside | 38,442 | 0 |
| Nine-column | Outside | 280,850 | 0 |
| Ten-column | Outside | 229,465 | 0 |
| Eleven-column | Outside | 37,219 | 0 |

For inside projections, the fixed lines contain the marked position and the missing ones avoid it. For outside projections the fixed lines avoid that position and every missing line contains it. The outside generator adds the other columns in descending projected weight, allows repeated supports, and rejects a column exactly when it shares three positions with some *pair* already present. At each depth it retains one relabelling of each multiset under permutations of the marked points. The actual relabelled block list is the key. Pruning uses row floors and the published prefix ceilings. If a prefix of $j$ columns has upper bound $U$, subsequent columns each have at most $\lfloor U/j\rfloor$ ones by degree order.

The border checker filters supports against all fixed pairs, then chooses missing lines in decreasing weight and rechecks every new triple. Distinct missing supports suffice. Identical columns would share at least six rows. Identical rows of degree at least seven would share seven columns, and deleting two identical degree-six rows would leave 126 ones on 14 rows. One positive control in each orientation reconstructs a valid 137-one matrix. The ten-row enumeration may visit isomorphic projections under different labellings.

With Python 3.10+, a C++20 compiler and nauty installed, run

```sh
python3 verify_exact.py --jobs 4
```

The replay regenerates its catalogues in a temporary directory and checks the returned counts. It uses the nine-point generator from the 16 × 17 proof. All finite exclusions for the 16 × 18 upper bound run locally from source.
