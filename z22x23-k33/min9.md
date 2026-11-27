# A 217-one rectangle must have a line of degree eight

The [210-square classification](../z22-k33/unique.md) and the [upper bound of 209 on 21 × 23](../z21x23-k33/README.md) give minimum degree eight on both sides. Suppose all degrees were at least nine. Give each column of degree $c$ weight $c-9$, summing to ten over all columns. Write $W$ for the total weight on a row. The corresponding row excesses over nine sum to nineteen.

Any two rows share at most five columns, since six columns need 54 entries against capacity $12+20\cdot2=52$. Thus a row has degree at most thirteen by counting the at least eight other entries on each of its columns among 21 rows of intersection at most five. Two columns share at most six rows.

## Four local restrictions

| Mark | Reason for the choice | Projections checked for completion | Result |
|---|---|---:|---|
| Eleven columns on a long row | $W\ge2$, choose the eleven heaviest | 338 | No completion |
| An entire ten-row | $W\ge5$ | 13,205 | No completion |
| An entire nine-row | $W\ge8$ | 234 | No completion |
| Eleven rows of a long column | Six marked rows have degree at least ten | 389 | No completion |

The first two use the [22-square projection argument](../z22-k33/unique.md), with width 23, total 217 and unmarked column degrees 9–19. For a nine-row, drop an entry on a column of minimum degree. This degree is nine or ten because the total column excess is ten. The remaining eight entries retain eight units of weight. Lift the 326,456 eight-point projections as in the square proof, allowing multiple long columns and a point load as large as eighteen. The last row of the table uses the [eleven-point mark on 22 blocks](../z23-k33/226.md), with eleven missing lines and target 217. Thus a row of degree at least eleven has $W\le1$, a ten-row has $W\le4$, a nine-row has $W\le7$, and a column of degree $c\ge11$ has at least $c-5$ nine-rows.

## Restrictions that survive the presence of eight-lines

In **any** 217-one rectangle, assign weight $c-9$ to columns of degree $c\ge9$. In a row let $t$ count its entries on these columns and let $W$ sum their weights. The replay establishes the following bounds.

| $t$ | At least 9 | At least 10 | At least 11 |
|---|---:|---:|---:|
| Upper bound on $W$ | 7 | 4 | 1 |

Choose the nine, ten or eleven heaviest eligible columns. If $W$ exceeds the corresponding bound, those selected columns capture at least eight, five or two units respectively, since weights are nonnegative integers. Their blocks have size at most five because six eligible columns need 54 entries against capacity 52. The same three catalogues apply. For the nine-point construction the omitted minimum-load point has load at most nine. If all nine loads were ten or more, the 21 blocks of total size at least 90 would consume more than the 84 available triples. The eight retained points have total load at most 74, since at 75 the balanced distribution already consumes 57 triples against capacity 56. Their individual loads are consequently at most eighteen. If the minimum omitted load is nine then all eight retained points have positive weight.

None of the 234, 13,205 or 338 projections admits seven blocks meeting pairwise in at most one point. Thus even an eight-column cannot pass through the marked row outside the chosen points. Testing all missing columns with degrees eight to 21 excludes every projection.

For a column, choose ten or eleven of its incident rows of degree at least nine. Among ten chosen rows, at least five high rows and total weight at least nine are impossible. Among eleven chosen rows, six high rows are impossible. Here a high row has degree at least ten and its weight is its degree minus nine. The two projection counts are 1,390 and 389. None has a seven-block extension and neither catalogue completes with missing row degrees eight to 22.

## The remaining three spectra

Enumerate the partitions of nineteen and ten on the two sides. Write $a,b$ for the numbers of nine-rows and nine-columns, $t$ for the number of ten-rows and $l$ for the number of longer rows. The total incident column weight is at most $7a+4t+l$. Each long row of degree $d$ needs at least $d-1$ nine-columns and each long column needs at least $c-5$ nine-rows. Two required subsets must fit with intersection at most five on the row side or six on the column side. Distributing the required incidences evenly gives a lower bound on their covered pairs and triples, with pair multiplicity at most five or six and triple multiplicity at most two.

| $a$ | $b$ | Long row degrees | Long column degrees |
|---:|---:|---|---|
| 5 | 13 | 12 | None |
| 6 | 13 | 13 | None |
| 6 | 14 | 13 | 11 |

Let $d$ be the single long row degree. It hits $h=0$ or 1 ten-columns and no longer columns, leaving $b-d+h$ nine-columns outside it. Each ten-row needs at least six nine-columns since $W\le4$, with one extra needed for every eleven-column it hits. It can use at most five cells of the long row. If one of these lies on the marked ten-column, only four can lie on marked nine-columns. The outside nine-columns must therefore hold at least
$$
t+\sum_{c\ge11}(c-a)+h(9-a)
$$
entries on ten-rows, with $c$ ranging over the long columns. The long row avoids each eleven-column, and a ten-column on the long row has nine other entries. This lower bound exceeds $9(b-d+h)$ in all six cases. Run `python3 verify_min9.py` to regenerate the four catalogues and verify the counts. [Replay](verify_min9.py)

In a 226-one square every line has degree at least nine. Deleting any nine-row must create an eight-column in the resulting 217-one rectangle. Hence every nine-row meets a nine-column, and vice versa by transposition.

## There must specifically be an eight-column

Suppose every column has degree at least nine. The preceding proof forces an eight-row. Let $e$ count eight-rows and $a$ count nine-rows. Deleting one eight-row leaves 209 on 21 × 23. That parent has at most one eight-row, so $e$ is one or two. Its row deficit $D=2(e-1)+a$ is between four and seven, its maximum row degree is thirteen, and the total row excess above ten is $D-1$. At $D=4$ the parent has four eight-columns. A thirteen-row needs at least five of them. [209-one profiles](../z21x23-k33/six-columns.md) · [Long-row restriction](../z21x23-k33/README.md)

The eight columns of an eight-row have total load at most 74 on the other 21 rows. At 75 the 21 blocks consume at least 57 distinct triples from eight points, exceeding the 56 available. Thus its weight is at most ten. Write $R$ for the multiset of long-row degrees, $t$ for the number of ten-rows and $b$ for the number of nine-columns. The other row bounds give
$$
\sum_j c_j(c_j-9)\le 10e+7a+4t+|R|.
$$
Each long row needs $d-1$ nine-columns. As in the preceding count, these subsets fit into $b$ points, meet pairwise in at most five points and in triples in at most two. Enumerate the partitions of $D-1$ on the long rows and the partitions of ten on the high columns. Just four combinations remain. All four have $D=4$ and a thirteen-row, contradicting the parent restriction.

Hence **every 217-one rectangle has an eight-column**. Deleting it leaves 209 on 22 × 22. Conversely, any such square admitting one additional eight-one column settles the rectangle at 217. [Replay](verify_min9.py)

The 209-one parent must itself be inclusion-maximal. Otherwise adding a cell gives the unique [210-one square](../z22-k33/unique.md). The verifier examines every eight-position support in both orientations of that square. If two existing columns meet the support in four or more rows, a single deletion cannot make the support admissible. If they meet it in three rows, the deleted cell must belong to one of those two columns and one of those three rows. Intersect these choices over all offending pairs. For every support the choices run out. Thus none of the single-cell deletions of the unique extremal square admits an eight-one extension.
