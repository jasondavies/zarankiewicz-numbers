# The 18 × 20 K₃,₃ problem at weight 163

Deleting two rows from the [nine-regular 20 × 20 square](../z20-k33/witness-180.txt) gives 162 ones. The earlier [upper bound of 163 and seven-column reduction](../z20x21-k33/core-search.md) leaves six cases. Write $k$ for the number of columns of degree seven. All other columns have degree at least eight, and the earlier proof excludes $k=0$ and $k\ge7$. Removing the seven-columns leaves an 18 × $(20-k)$ core of weight $163-7k$. An entry can always be removed from a heavier matrix, so 163 is the only weight needed.

**The case $k=1$ is excluded. The current bounds are $162\le z(18,20)\le163$. At weight 163 the remaining counts are $k=2,3,4,5,6$.**

## Every row of the core has degree at most nine

Two rows cannot share six core columns. Six such columns require at least 48 ones, whereas the two rows supply 12 and the other sixteen can supply at most two each. On the support of a marked core row the seventeen other rows therefore give blocks of size at most five. Two blocks meet in at most two points and the load at every point is at least seven. The [eleven-point exclusion](../z18x19-k33/marked-search.md) rules out a row with eleven or more entries.

Mark an entire ten-row. The [ten-point enumerator](../z18-k33/ten_points.cpp) gives 978 projections at total load at least 70 on seventeen blocks. The remaining $10-k$ core columns all miss the mark. Their degrees range from eight to $\min(17,11+k)$, since the excess over degree eight in the core sums to $3+k$. Distinct column supports suffice, since two columns of a 163-one matrix cannot share seven rows. The [original argument](../z20x21-k33/core-search.md) uses $z(11,18)\le101$ to bound the other eleven rows. The border search enumerates every completion to the prescribed core weight.

| Seven-columns to restore | Marked core completions | Admit at least one seven-column | Admit all required columns |
|---:|---:|---:|---:|
| 1 | 7 | 0 | 0 |
| 2 | 35 | 0 | 0 |
| 3 | 56 | 5 | 0 |
| 4 | 0 | 0 | 0 |
| 5 | 0 | 0 | 0 |
| 6 | 0 | 0 | 0 |

Counts include repetitions under the choice of mark. Each proposed new column is a seven-subset of eighteen rows. It must intersect the common support of each pair of old columns in at most two rows. After accepting a candidate, apply the same test with that column included before accepting another. This checks triples containing one, two or three new columns. A positive control removes and restores the seven-columns of a 162-one witness.

## One seven-column

At $k=1$ the core has weight 156 on 18 × 19. A column has degree $8+e_j$, where the $e_j$ are nonnegative and sum to four. Core row degrees are at least six because $z(17,19)\le\lfloor19\cdot143/18\rfloor=150$. They are at most nine by the ten-row exclusion. At least twelve rows have degree nine, since eighteen eights would supply only 144 entries.

Let $H$ be the number of nine-rows, and let $W$ denote the sum of the column excesses on a row. Some nine-row has $W\ge2$. Any column of excess at least two meets a nine-row, since at most six rows have smaller degree. Otherwise four columns of degree nine contain 36 entries. If each nine-row met at most one, the other $18-H$ rows would have to contain at least $36-H$ incidences. For $H>12$ this exceeds $4(18-H)$. At $H=12$ all six other rows would contain all four columns, which is forbidden.

Choose a nine-row of largest $W$. It maximizes $2d+W$ over all rows of core degree $d$, since any row of degree at most eight scores at most 20 and the chosen row scores at least 20. The nine marked points have loads at least seven and total load $63+W\ge65$. There are 87,842 projections at this threshold. The [marked-core search](../z18x19-k33/marked_core.cpp) enumerates the ten missing core columns with the chosen score bound and tests every seven-column extension. The direct replay below needs only this single choice of mark.

The faster computation separates the partitions of the four excess units. If the largest excess is at least two, a nine-row meeting a column of largest excess can be used unless a different nine-row scores strictly higher. For excess profiles $(4),(3,1),(2,2),(2,1,1)$ this leaves respectively 0, 19, 9,327 and 9,901 marked projections. For $(1,1,1,1)$ there are 76,099 projections with $W=2$, 1,799 with $W=3$ and 21 with $W=4$. In the $W=2$ case the two remaining nine-columns are chosen first. The other eight missing columns form a clique of compatible eight-subsets. At each choice the search also checks triples using previously chosen columns. Two core columns may share at most five rows: six common rows would need at least $156-12\cdot9=48$ entries and could supply at most $12+17\cdot2=46$. The balanced profile yielded 17 completed cores at $W=2$ and three at higher $W$. Five more arose in the $(2,2)$ profile. These counts can include repeated matrices under different marks. None accepted a seven-column. The slower general-purpose replay checks the same exclusion directly without the profile split.

## Two seven-columns

The core is now an 18 × 18 square of weight 149. Every row has degree from six through nine, using $z(17,18)=143$. The deficits below nine sum to thirteen. The column excesses $e_j=c_j-8$ sum to five. Only the partitions $(1,1,1,1,1)$ and $(2,1,1,1)$ remain. They give the following possible full column degrees.

| Degree 7 | Degree 8 | Degree 9 | Degree 10 |
|---:|---:|---:|---:|
| 2 | 13 | 5 | 0 |
| 2 | 14 | 3 | 1 |

To see the exclusions, let $Q=\sum e_j^2$. A row score $2d+W$ sums over the eighteen rows to $2\cdot149+8\cdot5+Q\ge343$. A maximizing row scores at least 20 and has degree eight or nine.

* **Excess five in one column.** A column of size thirteen would leave five outside rows of degree at most nine. On its thirteen rows there must be at least $149-45-13=91$ incidences in the other seventeen columns. Counting pairs of these columns at each marked row gives at least $13\binom72=273$ incidences by convexity. Each pair occurs together on at most two marked rows, giving capacity $2\binom{17}2=272$.
* **Excesses four and one.** On a maximizing mark the point loads are seven plus some of these excesses. For degree eight the minimum load sum is 60, and for degree nine it is 65. Filtering the catalogues by the excess multiset and score 20 leaves 90 eight-point projections and zero nine-point projections. No projection completes.
* **A column of excess three.** In the profiles $(3,2)$ and $(3,1,1)$, a nine-row touching the eleven-column scores at least 21. Eight-rows score at most 21, so a maximizing nine-row can be used. Each profile leaves 19 projections and no completion. If the eleven-column misses every nine-row, its eleven rows all have degree at most eight. Their combined deficit below eight is at most two, since the deficit of the whole square below nine is thirteen. No other column can share six of these rows: six would need at least 46 ones and could have at most $12+16\cdot2=44$. Mark the eleven-column, giving seventeen blocks of size at most five, loads from five through seven and total at least 75. The 70 projections admit no completion to weight 149 by the seven remaining rows. These rows have degrees from seven through nine since at most two units of deficit below nine remain outside the mark.
* **Excesses two, two and one.** The two ten-columns jointly meet at least fourteen rows, since two columns cannot share seven. At most thirteen rows have degree below nine. Some nine-row therefore has $W\ge2$. Choose a nine-row maximizing $W$. It maximizes $3d+W$ since its score is at least 29 and an eight-row can score at most 29. The 9,898 projections with compatible marked excesses and score at least 29 give no completion.

### The 149-one core must be inclusion-maximal

If any zero of this core could be set to one, the resulting 150-one square would have minimum column degree eight. The previous square census counts one marked completion at ten points and five at nine points. The [six marks](square-marks.txt) account for all these completions. The replay checks that the marks satisfy the catalogue conditions, are inequivalent at each degree and recover the full census totals. [Coverage of the 150-one square census](../z18x19-k33/square-cores.md)

For each completion and each orientation, delete one of the 150 ones and test whether two seven-columns can be added. All 1,800 marked deletion tests fail. For a proposed seven-subset, record every pair of old columns with at least three common entries in the subset. A single deletion can repair all those pairs only if each overlap has size three, the deleted column belongs to every violating pair and its row belongs to every overlap. These conditions are also sufficient. This gives the legal seven-subsets after each deletion. Two of them can be used together precisely when their common rows intersect each surviving old column in at most two places.

Deleting two seven-columns from a putative 163-one matrix always gives 149 on 18 × 18. Inclusion-maximality here is proved for the case of exactly two seven-columns, in which every surviving column has degree at least eight. A 170-one matrix on 18 × 21 would have at least three seven-columns: the [previous reduction](../z20x21-k33/weight-186.md) forces at least two, and deleting one would leave 163.

## Replay

Run from this directory with Python 3.10+, C++20 and nauty. The upper bounds for the smaller dimensions and the pre-existing exclusions are linked above.

```sh
python3 verify_progress.py --stage ten --jobs 8
python3 verify_progress.py --stage one --jobs 8
python3 verify_progress.py --stage two --jobs 8
python3 verify_progress.py --stage maximal
```
