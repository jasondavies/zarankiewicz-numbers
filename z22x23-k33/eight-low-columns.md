# At least eight eight-columns at 193 on 20 × 22

Suppose a 20 × 22 matrix has 193 ones and avoids an all-ones 3 × 3. Every line has degree at least eight. The [five-column exclusion](six-low-columns.md) gives at least six columns of degree eight. We exclude exactly six and exactly seven. No minimum-degree-nine hypothesis on the rows is needed.

Let q count the eight-columns. For q=6 the remaining degrees are fifteen nines and one ten. For q=7 they are thirteen nines and two tens, or fourteen nines and one eleven. Write Q for the sum over columns of the squared excess above eight. These profiles have Q=19,21,23 respectively. On a row of degree d let W be the sum of its column excesses above eight, let l count its eight-columns, and let H be the sum of positive excesses above nine. Thus W=d−l+H.

A row of degree at least eleven has W at most six. A row of degree at least twelve has W at most four. These local projection bounds use the minimum column degree eight and the nineteen other rows. The arguments for these two bounds allow eight-rows. Since at most seven low columns exist, a row of degree twelve would have W at least five. Thus the degrees are 8,9,10,11. If x,y,z,w count these rows respectively, then y=7−2x+w and z=13+x−2w. [Eleven- and twelve-point bounds](three-columns.md)

## Selecting a row to mark

The maximum of d+W is at most nineteen. Indeed, an eight-row has W at most ten. A nine-row with W at least eleven or a ten-row with W at least nine has no six-block in its projection. A six-block means another row shares six marked columns. All six have degree eight and all other rows hit exactly two of the six. The outside matching argument gives W at most six on a nine-row with a six-block and at most eight on a ten-row with one. The resulting 27 high-load nine-point and twelve high-load ten-point projections of block size at most five have no 193-one completion, even allowing eight-rows. [Matching and direct completion checks](three-columns.md)

If a nine-row has W=10, it reaches the maximum nineteen. If none does and a ten-row has W=8, the latter reaches the maximum eighteen. Such a ten-row cannot have a six-block, since equality in the matching argument would require four degree-ten columns. Mark the maximizing row. The numbers of possible marks after matching the column degrees are in the table below. None completes, allowing all row degrees from eight. Hence suppose that W is at most nine on nine-rows and at most seven on ten-rows. It follows that l is at least H on a nine-row, 3+H on a ten-row, and 5+H on an eleven-row.

## Forcing an eleven-row

For q=6 each eleven-row contains at least five of the six low columns. Three such rows would share at least three columns, so w is at most two. The unique ten-column gives a total H of ten over all rows, of which at most x can fall on eight-rows. Consequently
$$48\ge 3z+5w+10-x=49+2x-w.$$
This forces x=0 and w equal to one or two. There is now at most w−1 units of slack in the lower bounds on l across all rows. In particular some eleven-row has l=5+H, hence W=6. At least one of the y=7+w nine-rows has l=H at most one. That row prevents any pair of rows from sharing six columns, since the six would have to be all six eight-columns and every other row would hit exactly two of them.

For q=7 each eleven-row omits at most two of the seven low columns. Any three eleven-rows must together omit at least five. Enlarge each omitted set arbitrarily to a pair. When w is at least three the resulting pairs are distinct and any three span at least five vertices. Each component of the graph of these pairs has at most two edges, since a connected group of three edges has at most four vertices. Seven vertices can therefore support at most four edges. Thus w is at most four in all cases.

On an eight-row we have l at least H−2. The sum of H across all rows is twenty at Q=21 and 22 at Q=23. Hence
$$56\ge 3z+5w+\sum H-2x=39+x-w+\sum H.$$
At Q=23 this requires w at least five. At Q=21 it requires w at least 3+x. As w is at most four, the total slack in the inequalities is at most one. Some eleven-row then has W=6. No pair of rows can share six columns, since an eleven-row outside that pair would meet at least four of the six low columns, exceeding two.

In both remaining cases mark an eleven-row with W=6. It maximizes 2d+W at 28. Its projection has block sizes at most five and load 83. At Q=19 the preceding proof gives minimum row degree nine. At Q=21 the completion checker allows eight-rows. The searches give zero completions.

| Marked row | Q=19 | Q=21 | Q=23 |
|---|---:|---:|---:|
| Nine, W=10 | 81 | 590 | 49 |
| Ten, W=8 | 4,629 | 10,465 | 1,691 |
| Eleven, W=6 | 90 | 124 | Excluded by counting |

The replay generates all projections at each stated load, intersects their point-load multisets with the column profile, and completes each using the maximizing score and Q. Run `python3 verify_eight_low_columns.py --jobs 4`. [Replay](verify_eight_low_columns.py)

By deleting an eight-column, a 201-one matrix on 20 × 23 must have at least nine eight-columns. In a 201-one matrix on 21 × 22 with q eight-columns, an eight-row avoids all of them and must hit at least 8−q columns of degree nine, by deleting the row. These are consequences for parents occurring in the 217 search.
