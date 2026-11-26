# Excluding 157 ones on 18 × 19

Suppose that a binary matrix with 157 ones avoids an all-ones 3 × 3 submatrix. Call the number of columns containing exactly seven ones $k$. All columns have degree at least seven by the 18 × 18 maximum of 150. All rows have degree at least seven since deleting any row leaves at most 150 ones on 17 × 19. A seven-row and seven-column cannot meet, since deleting both would leave 144 ones on 17 × 18. The published bound of 85 on 18 × 9 gives $k\le9$, since deleting ten seven-columns would leave 87 ones. The [first reduction](README.md) and [square census](square-cores.md) exclude $k=0,1$. We handle $2\le k\le9$ below. [Small bounds, Table 4](https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf)

## Choosing a row

Remove all $k$ seven-columns to obtain the *core*, with $m=19-k$ columns, $T=157-7k$ ones and column degrees $c_j\ge8$. Let $e_j=c_j-8$, $E=\sum e_j=5+k$, and $Q=\sum e_j^2$. For a multiplier $\alpha$ chosen below, mark a row maximizing the score
$$
P_i=\alpha d_i+\sum_{j\ni i}e_j,
\qquad \sum_{i=1}^{18}P_i=\alpha T+8E+Q,
$$
where $d_i$ is the core degree of row $i$. Write $P$ for its score and $t$ for its degree. Its $t$ columns give $t$ points. The other seventeen rows induce seventeen blocks on the points. Counting all entries in these blocks gives $S=7t+(P-\alpha t)$.

Two rows of the core cannot share six columns. Such columns require at least 48 ones, whereas the two rows supply twelve and each of the other sixteen can supply at most two. Each block therefore has size at most five. Two blocks intersect in at most two points because a triple in the intersection would make a forbidden submatrix with the marked row. Every point has load at least seven. If the marked row had at least eleven points, any eleven would give such a block family of total load at least 77. The eleven-point catalogue is empty at that threshold. [Eleven-point enumeration](../z18-k33/README.md)

| Seven-columns $k$ | Restriction | $\alpha$ | Lower bound on $P$ | Marked degrees tested |
|---|---|---:|---:|---|
| 2, 3 | all | 2 | 20 | 6–10 |
| 4 | $Q\le12$ | 1 | 12 | 6–10 |
| 4 | $Q\ge13$ | 2 | 20 | 6–10 |
| 5 | all | 1 | 12 | 4–10 |
| 6, 7, 8 | all | 1 | 12 | 5–10 |
| 9 | all | 1 | 12 | 4–10 |

For $k=2,3$ we have $2T+8E+Q\ge2T+9E>18\cdot19$. A full row of degree seven loses no entries and a higher-degree row loses at most $k$. Hence $t\ge6$ for $k=2$, and $t\ge5$ for $k=3$. At $t=5$ the score bound would require $S\ge45$. Each block of size $b$ contributes at most $2+\binom b3$ incidences. Since every triple of points occurs at most once, $S\le34+\binom53=44$.

For $k=4$ we have $T=129$, $E=9$, and $t\ge4$. If $Q\le12$, then $Q-E=\sum e_j(e_j-1)\le3$. All positive excesses are one apart from at most one excess of two. The total score for $\alpha=1$ is at least $129+72+9=210>18\cdot11$. The marked score is at most $2t+1$, so $t\ge6$. If $Q\ge13$, then the total score for $\alpha=2$ is at least $258+72+13=343>18\cdot19$. The same block bound gives $S\le38$ for $t=4$ and $S\le44$ for $t=5$, below the required $5t+20$ in each case.

For $5\le k\le9$, take $\alpha=1$. Then $T+8E+Q\ge T+9E=202+2k>18\cdot11$. Deleting the marked row leaves an admissible matrix on $17\times m$. For $m=14,13,12,11,10$, the published upper bounds are $118,110,103,96,90$, respectively. Subtracting these from $T$ gives the minimum marked degrees in the table. [Collins et al., Table 4](https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf)

## Exhausting the cores

The score bound requires $S\ge 5t+20$ for $\alpha=2$, or $S\ge6t+12$ for $\alpha=1$. At ten points we use the larger catalogue with $S\ge70$ in both cases. These are the counts of distinct projections under permutations of the points and blocks.

| Points $t$ | Minimum $S$ | Projections |
|---:|---:|---:|
| 4 | 36 | 4,736 |
| 5 | 42 | 10,193 |
| 6 | 48 / 50 | 73,217 / 492 |
| 7 | 54 / 55 | 170,476 / 6,626 |
| 8 | 60 | 147,269 |
| 9 | 65 / 66 | 87,842 / 2,418 |
| 10 | 70 | 978 |

For up to eight points the generator builds block multisets in nonincreasing order of size and takes a canonical representative at each level. It allows repeated blocks of size at most two. The remaining blocks must be able to attain the minimum point loads and total load. For a specified additional total load, balanced block sizes minimize the number of triples used by convexity. For nine and ten points we reuse the catalogues from the smaller rectangles. [Small generator](small_points.cpp) · [Nine points](../z16x17-k33/catalogue.cpp) · [Ten points](../z18-k33/ten_points.cpp)

For each projection, the $t$ marked columns are fixed on all eighteen rows. The $m-t$ other columns omit the marked row. The checker tries every nonincreasing partition of their remaining excess into column degrees between eight and seventeen. For each degree it generates every support that meets each fixed pair of columns in at most two rows. It adds the supports one at a time, checking triples with previously chosen columns. Equal degrees can be taken in support-index order. No two full columns may coincide, since even seven shared rows require at least 49 ones, whereas the two columns supply fourteen and the other seventeen at most 34.

A row's available score is $P$ minus its score from the columns already fixed. No choice may make this negative. For a fixed degree profile the sum of all unused row capacities at completion is $18P-(\alpha T+8E+Q)$. The marked row already has capacity zero. If the remaining columns have total coefficient $W=\sum (\alpha+e_j)$, a row of current capacity $u$ must leave at least $\max(0,u-W)$ unused. The checker prunes if these lower bounds exceed the total unused capacity. It can force a particular row into the next column if omitting it would exceed the same total. All bounds follow from the choice of a maximum-score row.

Finally the checker enumerates all seven-subsets of the eighteen rows that meet every core column pair in at most two rows. It tries every set of $k$ such subsets, testing all triples involving the added columns. A successful result can be checked by counting the entries and intersecting every triple of the nineteen column masks. [Core search](marked_core.cpp) · [Extension search](seven_columns.hpp)

The replay includes a positive control. From a separate verified 156-one matrix, take two columns of degree eight out of the core. Each could be shortened to seven to give a legal weight-154 completion. Give the checker just a maximum-score marked projection of the core. It must reconstruct a complete weight-154 matrix, which is checked independently in Python. [Control matrix](witness-156-min8.txt) · [Replay driver](verify_exact.py)


## Results

| Seven-columns | Marked projections tested | Completed cores tested for extension |
|---:|---:|---:|
| 2 | 243,207 | 6 |
| 3 | 243,207 | 3,715 |
| 4, $Q\le12$ | 394,358 | 879,558 |
| 4, $Q\ge13$ | 243,207 | 212,075 |
| 5 | 409,287 | 52,498 |
| 6 | 404,551 | 1,224 |
| 7 | 404,551 | 127 |
| 8 | 404,551 | 6 |
| 9 | 409,287 | 1 |

No completed core admitted the required seven-columns. The counts include repeated occurrences of a core under different choices of mark or labelling. As a cross-check for $k=3$, an enumeration without the maximum-score capacity pruning returned 5,964 complete cores. An independent checker generated the individually legal seven-column supports for each core and tested their combinations. Of these cores 313 accepted a single seven-column and none accepted three. The $k=0,1$ reductions and the bound $k\le9$ now exhaust weight 157. Erasing entries preserves avoidance, so every heavier weight is excluded as well.
