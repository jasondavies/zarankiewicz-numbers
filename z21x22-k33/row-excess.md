# Excess on the high columns of a 201-one rectangle

In a 21 × 22 rectangle of weight 201 call a column high if its degree c is at least nine. On any row let t be its number of high entries and let H be the sum of c−9 on those entries. Every row has t at most nine. The following additional bounds hold. [Ten-point exclusion](high-columns.md)

| t | Maximum H allowed by these tests | Additional condition |
|---:|---:|---|
| 9 | 3 | |
| 8 | 6 | At H=6 the full row has degree eight. |
| 7 | 7 | |
| 6 | 9 | |

Mark the t high columns. On the twenty outside rows the point loads are at least eight, their sum is 8t+H, and two blocks intersect in at most two points. No block has six entries by the 54 versus 50 count for high columns. Every unmarked column through the marked row is a low column of degree eight. Its seven further rows must meet pairwise in at most one marked point. Enumerate every such seven-set and every combination of distinct new columns through the marked row that respects the triple condition. Distinctness follows since two columns of the full rectangle cannot share seven rows. Once all incident columns have been chosen, every other column avoids the marked row and may have degree eight through twenty.

| Points | Minimum projection load | Projections | Can add a low column through the mark | Augmented projections to complete |
|---:|---:|---:|---:|---|
| 9 | 76 | 2,245 | 0 | 0 |
| 8 | 70 | 3,768 | 19 | 40 with one extra column |
| 7 | 64 | 283 | 41 | 49 with one extra column |
| 6 | 58 | 116 | 1 | Two with one extra column and one with two |

Every augmented projection fails completion to 201. For t at most seven the marked row requires at least one additional entry because every full row has degree at least eight. For t equal to eight or nine, the possibility of no extra entry must also be tested to exclude the larger excess. All 41 eight-point projections of load at least 71, and all 2,245 nine-point projections of load at least 76, fail at weight 201.

One consequence is that **2t+H is at most 21 on every row incident to an eight-column**, and at most 22 on every row. For t=4,5 one uses the elementary inequality b ≤ 2 + C(b,3) on each outside block. Their total size is at most 40+C(t,3) because no triple of marked points occurs twice. At t=3 a pair of marked points occurs together on at most five outside rows, by the six-row upper bound for a pair of full columns. The total load is at most 20+15 by counting pairs within the blocks. The same argument gives at most 25 for t=2. At t=1 the column has degree at most 21. These estimates cover the smaller marks.

Run `python3 verify_row_excess.py --jobs 4` to regenerate the catalogues, list all incident extensions and check the completions. [Replay](verify_row_excess.py)

In fact equality at 22 requires a full eight-row with eight high entries and H=6. In the two-column reconstruction of 217 all original rows of the 201-one parent have degree at least nine, so every row there satisfies 2t+H ≤ 21. If the 201-one rectangle has exactly three eight-columns, its 21 × 19 high submatrix has weight 177. The deficits 9−t of its rows total twelve. A column of degree at least thirteen would have H at least four on each of its entries, so it would meet at least thirteen distinct rows of high degree t ≤ 8. Their deficits already exceed twelve. Thus **every column of this 177-one parent has degree at most twelve**.
