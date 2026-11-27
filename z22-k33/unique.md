# Uniqueness of the 210-one 22 × 22 square

**Up to row and column permutations, there is exactly one extremal square.** It is the [stored 210-one matrix](witness-210.txt). It has no seven-one row or column extension. Thus every 217-one matrix on 22 × 23 has minimum column degree at least eight. A seven-column would leave an extremal square on deletion, and a shorter column would exceed the square maximum. [Rectangular problem](../z22x23-k33/README.md)

## An incidence count forces one of two projections

All degrees are at least nine since removing a line leaves at most [201 ones on 21 × 22](../z21x22-k33/README.md). Two rows share at most five columns. Six shared columns need 54 entries, but the two rows and their twenty companions can supply at most 52. For a row of degree $d$, the other 21 rows therefore supply at most 105 entries in its columns, while each column needs at least eight. Thus $d\le13$ on both sides.

Give columns of degree $c$ weight $c-9$ and let $W$ be the sum of incident weights on a row. If a row of degree at least eleven had $W\ge2$, we could mark eleven entries capturing two units. The other 21 rows give 338 possible projections on these columns, with all point loads at least eight and total load at least 90. No projection admits an additional column through the row, since none has eight blocks with pairwise intersections of size at most one. None accepts the eleven missing columns away from the row. Distinct missing supports suffice throughout because any pair intersects in at most five points. Thus $W\le1$ on a long row, and the same holds after transposition.

The positive excesses above degree nine on each side partition twelve into parts of size at most four. If there are $b$ nine-columns and long row degrees $d_i$, their required numbers of nine-columns are $u_i=d_i-1$. Each $u_i\le b$, and $u_i+u_j-b\le5$. Distribute $\sum_i u_i$ incidences as evenly as possible on the $b$ columns to lower bound the number of pairs and triples of long rows covered. For $l$ long rows these counts cannot exceed $5\binom l2$ and $2\binom l3$. Checking both orientations leaves the following seven pairs of profiles. A dash denotes no long line. The other lines have degree nine or ten, with their counts fixed by the weight.

| Long row degrees | Long column degrees |
|---|---|
| – | – |
| – | 11 |
| 11 | 11 |
| 11 | 12 |
| 12 | 12 |
| 12 | 13 |
| 13 | 13 |

On each profile, in either orientation, $\sum_j c_j(c_j-9)>7n_9+4n_{10}+l$, where $n_d$ counts rows of degree $d$. The left hand side counts total incident weight. Since a long row has $W\le1$, there is a ten-row with $W\ge5$ or a nine-row with $W\ge8$.

## Completing the marked rows

* A ten-row of weight at least five gives ten points and 21 blocks with point loads between eight and twelve, total at least 85 and pairwise intersections at most two. Of 13,205 projections exactly one completion is returned at weight 210 with the twelve missing columns of degree 9–13.
* On a nine-row of weight at least eight, omit an entry of smallest column degree. Its degree is nine or ten since there is at most one long column. The remaining eight entries retain at least eight units of weight. If the omitted column has degree ten, all eight retained columns have weight at least one. The eight-point catalogue at total load 72 and minimum load eight contains 326,456 projections. To restore the ninth point, choose eight or nine blocks of size at most four meeting pairwise in at most one point. Enforce the degree range, the minimum-degree choice, the total nine-point load of at least 80, and at most one long column. Up to point and block permutations there are 81 lifts. None completes to weight 210.

This exhausts both alternatives in a fixed orientation. The stored witness verifies existence. Testing all $\binom{22}{7}$ possible supports on each side of the unique square gives zero admissible seven-one extensions.

Run `python3 verify_unique.py` with Python 3.10+, C++20 and nauty. It regenerates all catalogues, enumerates every completion and checks the extensions on both the reconstructed square and the stored witness. [Replay](verify_unique.py) · [Ninth-point extension](lift_eight.cpp)
