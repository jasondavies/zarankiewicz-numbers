# Four eight-one columns are impossible at 217

**Every 185-one matrix on 19 × 22 that avoids an all-ones 3 × 3 has a row of degree eight. Consequently a 217-one matrix on 22 × 23 has at most three eight-columns.**

To see the implication, delete all four eight-columns of a hypothetical four-column example and transpose. The resulting 19 × 22 core has 185 ones, minimum row degree nine and minimum column degree eight. [Deletion argument](eight-column-count.md)

Write the column degrees as $8+e_j$. Their excesses sum to nine. If $d_i$ is a row degree and $W_i$ the sum of the excesses on that row, then
$$
\sum_i(d_i+W_i)=185+8\cdot9+\sum_j e_j^2\ge266=19\cdot14.
$$
The [19-row projection bounds](../z19x21-k33/README.md) apply at this width. Every row has degree at most twelve. An eleven-row has $W_i\le2$ and a twelve-row has $W_i=0$.

Mark a row and take its incident columns as points. The remaining eighteen rows give blocks meeting pairwise in at most two points. Each block has at most five points because six columns need at least 48 entries and two rows sharing them allow only $12+17\cdot2=46$. Each point has load at least seven outside the mark, and their total load is $7d_i+W_i$.

* If any ten-row has $W_i\ge5$, its ten points have load at least 75. Exactly 24 projections qualify. None accepts twelve more columns at weight 185. Each additional column avoids the mark and has degree between eight and seventeen, since the total excess is nine. Distinct supports suffice since seven common rows require at least 63 entries and two columns sharing them allow only $14+20\cdot2=54$.
* If some row scores at least fifteen, it must now be a nine-row with $W_i\ge6$. There are 67,537 projections of load at least 69. Six have load at least 71. At most one unit of excess then lies outside the mark, so all thirteen missing columns have degree eight or nine. None of the six completes.
* Otherwise every row scores fourteen, every excess is zero or one, and there are nine columns of degree nine. There can be no eleven- or twelve-row. The weight forces fourteen ten-rows and five nine-rows. Mark any ten-row. It meets precisely four nine-columns, so its ten point loads consist of four eights and six sevens. There are 11,806 projections. The marked-core search enforces a score ceiling of fourteen on every row, minimum row degree nine, and a sum of squared column excesses of at most nine. None of these projections completes.

This leaves **67,531 nine-row projections**, of which 67,213 have load 69 and 318 have load 70. A maximizing row can always be chosen. Its score bounds every other row during completion. A completion to 185 must additionally admit four simultaneous eight-row extensions to give 217 on 23 × 22. The counts refer to marked projections and can include several marks from the same full matrix.

## A smaller exhaustive cover

Now maximize $2d_i+W_i$. Its sum over all rows is $442+Q$, where $Q=\sum_j e_j^2\ge9$. The maximum is at least 24. The preceding exclusions give $W_i\le7$ at degree nine and $W_i\le4$ at degree ten. The eleven- and twelve-row bounds still apply. A score above 24 therefore requires a nine-row with $W_i=7$. Its load is 70, giving 318 projections.

At peak 24, $Q\le19\cdot24-442=14$. The nine positive units of column excess occupy at least six distinct columns by Cauchy–Schwarz. A twelve-row meets only zero-excess columns. Two twelve-rows would together need at least nineteen such columns because they intersect at most five times. There are at most sixteen, so at most one twelve-row occurs.

If only nine- and twelve-rows reached 24, at least $451-19\cdot23=14$ rows would have one of those two degrees. The other at most five rows contribute at most ten units of row degree above nine, and the possible twelve-row supplies three more. The actual surplus is $185-19\cdot9=14$. This forces a maximizing row of degree ten or eleven.

An eleven-row at 24 has $W_i=2$, hence load 79. None of its 32 projections completes. A ten-row at 24 has $W_i=4$, hence load 74. Its marked excesses must satisfy $9+\sum_{j\text{ marked}}e_j(e_j-1)\le14$. Exactly 19,911 projections pass. Enforcing the peak score on every row also gives a total slack of just $14-Q$ below the peak.

Both families are exhausted. The 318 nine-row marks of load 70 gave zero cores at their maximizing score. All 19,911 ten-row marks at score 24 and $Q\le14$ also gave zero cores. Thus no qualifying 185-one core exists, even before the four extensions are tested.

The proof above uses only the size, weight and minimum degrees of the core. In an arbitrary 185-one matrix on 19 × 22, deleting a column leaves at most 177 on 19 × 21, so every column has at least eight entries. Deleting a row leaves at most [177 on 18 × 22](../z21x23-k33/eight-columns.md), so every row has at least eight entries. The exhaustion forces equality on some row. Deleting it gives 177 on 18 × 22, with minimum column degree seven. The [smaller deletion argument](eight-column-count.md) shows at least three columns there have degree seven. Thus every eight-row of the original 185-one matrix meets at least three eight-columns.

From this directory, replay the entire exclusion with `python3 verify_four_column_cover.py --part all --jobs 4 --cache /tmp/z185-four`. The checker reconstructs a 177-one core and recovers four eight-row extensions on a 215-one control. The [marked-core solver](../z18x19-k33/marked_core.cpp) checks the row-score bound. The independent `--part regular`, `--part nines` and `--part tens` runs replay the separate families and reuse the same cache.
