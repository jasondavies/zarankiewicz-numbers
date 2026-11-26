# Completing the nine-column case at weight 144

By the [degree reductions](weight-144.md), it suffices to mark a column of degree nine, and no pair of columns shares six rows. Call its nine incident rows *inside* and the other eight *outside*. Write $S$ for the number of ones on the nine inside rows away from the marked column. The eight outside rows contain exactly $135-S$ ones. The following split covers every candidate.

| Fixed side | Condition | Projections up to row and column permutation |
|---|---|---:|
| Nine inside rows | $S\ge65$ | 3,671,498 |
| Eight outside rows | $S\le64$, minimum outside degree 7 | 7,298,758 |
| Eight outside rows | $S\le64$, minimum outside degree 8 | 12,057,949 |
| Eight outside rows | $S\le64$, minimum outside degree 9 | 825 |

Counts refer to the enumerated projections before completion. They include projections for which some necessary conditions on the opposite side may already be impossible.

## The inside enumeration

Each of the seventeen other columns gives a block on the nine points. Each block has size at most five because of its intersection with the marked column. Two blocks meet in at most two points, since a third common point would make a forbidden submatrix with the marked column. Point loads are the full row degrees minus one. They are at least six, and their total deficit below seven is at most four.

The [nine-point generator](../z16x17-k33/catalogue.cpp) enumerates these block multisets. Four blocks of size five would give twenty incidences on nine points. Even the most balanced distribution would require thirteen pairwise intersections counted with multiplicity, but the six block pairs allow only twelve. Thus there are at most three five-blocks. Choose a point of greatest frequency among the four-blocks. Deleting it from those that contain it gives triples on eight points, any two meeting at most once. A point is in at most three such triples, so there are at most eight triples. The generator tries all these families up to permutation, every compatible choice of at most three five-blocks, the remaining four-blocks, and the smaller blocks. A block of size at most two may repeat. It retains multisets of seventeen blocks satisfying the weight and load conditions. Canonical relabelling permutes points and blocks within their respective shores.

## The outside enumeration

Here the eight outside rows contain at least 71 ones. The $8\times17$ upper bound is 74, and every outside row has at least seven ones, so the minimum outside degree $d$ is seven, eight or nine. Delete a row of that degree. The remaining seven rows on seventeen columns have minimum degree at least $d$ and total weight at least $71-d$. For $d=9$ the minimum-degree condition itself gives the stronger lower bound 63. [Small rectangular upper bounds, Table 4](https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf)

The [seven-row generator](../z16x18-k33/outside_catalogue.cpp) produces these cores by adding columns in nonincreasing weight order. It rejects a new column when it shares three points with the intersection of two earlier columns. Canonical labelling removes duplicate cores. The [extension routine](outside_eight.cpp) adds back a row of exactly $d$ ones. It tries every support that avoids a column triple already covered twice. Columns identical on the seven old rows are interchangeable, so it suffices to choose an initial segment of each such class. Keeping final weights from 71 to 74 gives the three outside counts in the table.

## The completion test

The [border checker](../z16x18-k33/borders.cpp) reconstructs the opposite side, eight rows avoiding the mark or nine rows containing it. It enumerates row supports by descending weight. It checks every candidate against every pair of fixed rows, and after choosing a row, checks all pairs formed with that row before continuing. All rows have degree at least seven. Identical rows are impossible by the seven-common-columns argument in [the degree reductions](weight-144.md), so each candidate need only be used once.

For a faster upper bound, suppose $k$ more rows of total weight $T$ are needed. At a weight threshold $b$ they must contain a compatible subfamily of at most $k$ rows of weight above $b$, contributing at least $T-kb$ units of excess above $b$. This is necessary because all other chosen rows contribute zero or negative excess. The checker enumerates such subfamilies and prunes a node when even its largest remaining excesses cannot reach the target. Any branch passing this test still undergoes the full completion search.

None of the 23,029,030 projections admits a completion of weight 144. Together with the 143-one witness, this proves $z(17,18;3,3)=143$. As a check on the largest catalogue, deleting a further minimum row from the seven-row cores and regenerating them from smaller cores gave the same sorted list of 12,057,949 eight-row projections byte for byte.
