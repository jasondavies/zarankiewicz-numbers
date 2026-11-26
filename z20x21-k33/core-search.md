# Reductions at weight 187 on 20 × 21

A weight-187 matrix has at most one eight-one row. Its columns have degrees eight, nine and ten. If there are $q$ columns of degree eight, the counts at the three degrees are $(q,23-2q,q-2)$ with $4\le q\le7$. Every row meets at most eight of the columns of degree nine or ten. The four remaining column profiles are $(4,15,2)$, $(5,13,3)$, $(6,11,4)$ and $(7,9,5)$.

## The 18 × 20 and 18 × 21 bounds

Consider a $K_{3,3}$-free 18 × 20 matrix of weight 163 or 164 in which all columns have degree at least eight. Two rows cannot share six columns. Those columns need at least 48 entries, and the two rows and sixteen remaining rows supply at most $12+16\cdot2=44$. Mark entries in a row. The other seventeen rows give blocks of size at most five, with pairwise intersections at most two and every point of load at least seven. The eleven-point catalogue is empty at total load 77. Hence all rows have degree at most ten. At least one has degree ten by averaging. [Earlier projection proof](../z18x19-k33/marked-search.md)

Mark this ten-row. There are 978 canonical projections. Completing each requires ten further columns, each of degree at least eight and at most $w-19\cdot8$. Distinct column supports suffice. Even seven common rows of two columns could carry at most $14+18\cdot2=50$ entries, leaving at most 110 on the other eleven rows. The border checker excludes both weights on all 978 projections.

At 164 every column must have degree at least eight by $z(18,19)=156$. Deleting two rows from the 9-regular weight-180 square attains 162. This gives **$162\le z(18,20)\le163$**, and any 163-one example has a seven-one column. At 171 on 18 × 21, every column would have degree at least eight by the new upper bound. An eight-column exists by averaging. Deleting it leaves 163 on 18 × 20 with every column still at least eight, already excluded. Thus **$z(18,21)\le170$**. A 187-one rectangle has all rows of degree at least eight by $z(19,21)\le179$, and deleting two rows of degree eight would contradict this new bound. [18 × 19 result](../z18x19-k33/README.md) · [20 × 20 witness](../z20-k33/witness-180.txt)

## Which columns can occur at 187?

Call a column heavy if its degree is at least nine. Every column has degree at least eight by the earlier reduction. A row cannot meet ten heavy columns. Marking ten of them gives nineteen blocks, each of size at most five because six heavy columns need at least 54 entries against a capacity of $12+18\cdot2=48$. The blocks intersect pairwise in at most two points and have total at least 80, with every load at least eight. The catalogue is empty.

A row meeting nine heavy columns induces one of 1,226 projections. An eight-column through that row would require seven other rows whose blocks intersect pairwise in at most one marked point. None of the projections has such a set. The row therefore has exactly nine entries in the full matrix. The border checker tries the twelve omitted columns of weight at least eight on nineteen rows and excludes all 1,226 projections at 187. Distinct columns suffice since two columns sharing seven full rows could supply at most $14+19\cdot2=52$ entries on them, below 56. The heavy columns therefore contain at most $20\cdot8=160$ entries. The eight-columns must contain at least 27, so there are at least four. A shorter independent check for exactly three removes the three eight-columns. The remaining seventeen nines and one ten have 163 entries and force a nine-row. Its marked total is 72 or 73. All 1,217 such projections fail even to complete the heavy matrix.

To exclude columns of degree eleven or more, mark eleven of their rows. Two columns cannot share six rows, since six rows now need at least $8+5\cdot9=53$ entries, against $12+19\cdot2=50$. The twenty blocks on the mark thus have size at most five. Their total is at least 87 and their deficits below point load eight sum to at most one. With $m$ five-blocks, one needs $m\ge7$ and at least $27-2m$ four-blocks. There are 21 canonical five-block families to test. Only the case of seven fives and thirteen fours survives the four-block test. Of the resulting projections, twelve have the necessary point loads. Each has total 87, so the marked rows consist of one eight and ten nines. This also excludes degree twelve or greater, since eleven rows could then be marked while avoiding the sole eight. The other nine rows have degree at least nine, with 89 entries between them. The border checker excludes all twelve completions. Missing rows of degree at least nine cannot coincide, as any two full rows sharing nine columns would require at least 72 entries there against $18+18\cdot2=54$.

## Excluding eight or more eight-columns

An eight-row avoids every eight-column, since deleting an incident pair would leave 172 entries on 19 × 20. A nine-row meets at most two eight-columns, since deleting three that it meets and then the row would leave 157 entries on 19 × 18. Write $s$ for the number of eight-rows and $h$ for the number of rows of degree at least ten. We have $0\le s\le1$ and $1\le h\le7+s$ by the total weight. There are $20-s-h$ nine-rows. On the $h$ higher rows the $q$ eight-columns must contain at least $L=8q-2(20-s-h)$ entries.

These columns can cover each triple of the $h$ rows at most twice. If $L=qd+r$ with $0\le r<q$, convexity gives the necessary conditions
$$
L\le qh,\qquad (q-r)\binom d3+r\binom{d+1}3\le 2\binom h3.
$$
All cases at $q=9,10,11$ fail. At $q=8$ the only survivors $(s,h,L)$ are $(0,7,38)$ and $(1,8,42)$. The first exceeds $z(7,8)=37$. In the second, equality holds because $z(8,8)=42$, so each of the eleven nine-rows meets exactly two eight-columns. Together with the sole eight-row, these rows give a **12 × 13** matrix on the heavy columns, with row degrees $8,7,\ldots,7$ and total 85. [Collins et al., Table 4](https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf)

No pair of columns of this submatrix can share five rows. Five rows need at least 35 entries, whereas two covering columns and the other eleven provide at most $10+11\cdot2=32$. On the support of any column, the twelve other columns therefore give blocks of size at most four. The marked rows each have at least six entries outside the mark, forcing marked degree at most eight. A column of degree eight forces twelve four-blocks of total 48. There is one canonical projection, and it cannot accept the other four rows at weight 85. Distinct missing rows suffice, as a pair sharing seven columns allows only $14+10\cdot2=34$ entries there and the other six columns have at most 48. If all column degrees are at most seven, at least seven columns have degree seven, since the total is 85. The eight-row meets one of them. Mark it to obtain twelve blocks on seven points with point loads at least six and total 43. The catalogue is empty. This excludes $q=8$.

## The first remaining profile has four eights, fifteen nines and two tens

Delete the four eight-columns. The resulting 20 × 17 matrix has weight 155. For row $i$ let $d_i$ be its heavy degree and $u_i=8-d_i$. The deficits are nonnegative and sum to five. A row of full degree eight avoids every eight-column, since deleting an incident eight-row and eight-column would leave 172 on 19 × 20. A row of full degree nine meets at most two eight-columns, since deleting three that it meets, and then the row, would leave 157 on 19 × 18. Every other row retains at least six entries. Consequently $0\le u_i\le2$. [19 × 20 result](../z19x20-k33/README.md)

For any remaining column $C$ let $D(C)=\sum_{i\in C}u_i$. Its projection on its rows has total $7|C|-D(C)$ on sixteen blocks. Blocks have size at most five. If two heavy columns covered the same six rows, those six rows would require at least $6\cdot8-5=43$ heavy entries against $12+15\cdot2=42$.

* If a ten-column has $D(C)\le3$, its projection has total at least 67 and point loads between five and seven. There are 519 projections. None accepts the other ten rows of degrees six through eight. Distinct rows suffice since six shared heavy columns need at least 54 entries against a capacity of 48. Both ten-columns must therefore have $D(C)\ge4$.
* A nine-column with $D(C)\le1$ has total at least 62 and loads between six and seven. Of 4,028 projections, ten have total 63. None of these ten accepts the remaining eleven rows. Thus every nine-column has $D(C)\ge1$.
* The sum of $D(C)$ over all seventeen columns is $\sum_i d_i u_i\le7\sum_i u_i=35$. After the two tens, at most 27 remains for the fifteen nines. At least **three** nines must therefore have $D(C)=1$. Each contains one row of heavy degree seven and eight rows of heavy degree eight. There are **4,018** possible projections around such a nine-column. A completion must realize at least three of them on distinct columns of the same matrix.

There cannot be two rows of heavy degree six. If there were, the other deficit would be a single row of degree seven. Each ten-column needs deficit at least four and must contain both six-rows. Both six-rows also meet all four eight-columns to reach full degree ten, as established above. They would share two ten-columns and four eight-columns requiring 52 entries, against a capacity of 48. The only remaining heavy row profiles are five sevens and fifteen eights, or one six, three sevens and sixteen eights.

## Counting seven-rows after deleting three eight-columns

Any three eight-columns can be removed from a hypothetical 187 matrix, giving a 20 × 18 matrix with 163 entries. Work in its transpose and write $k$ for the number of seven-columns. Every column has at least seven entries by $z(18,19)=156$. We excluded $k=0$ above. If $k\ge11$, deleting eleven sevens leaves 86 on 18 × 9, exceeding the published upper bound of 85. Also two columns cannot share seven rows. Their seven rows would supply at most 50 entries and the remaining 11 × 20 submatrix has at most $\lfloor20\cdot101/18\rfloor=112$ by averaging over sets of eighteen columns. [Collins et al., Table 4](https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf)

Remove all $k$ sevens, leaving $m=20-k$ columns of degree $8+e_j$, $T=163-7k$ entries and $E=\sum e_j=3+k$. Mark a row maximizing $P_i=d_i+\sum_{j\ni i}e_j$. For $7\le k\le10$, $\sum_iP_i=T+8E+\sum e_j^2\ge T+9E=190+2k>198$, so the maximum is at least twelve. For a marked row of degree $t$ the projection on its columns has total at least $6t+12$. As above $t\le10$. Deleting the marked row and applying the published bounds on $17\times m$ gives $t\ge4,4,4,3$ respectively. At ten points we use the larger catalogue at total 70. The established marked-row checker reconstructs the other columns and tests all sets of $k$ seven-columns. [Algorithm and score pruning](../z18x19-k33/marked-search.md)

| $k$ | Marked projections | Completed high-degree cores tested | Completions to 163 |
|---:|---:|---:|---:|
| 7 | 409,287 | 136,123 | 0 |
| 8 | 409,287 | 7,165 | 0 |
| 9 | 409,287 | 209 | 0 |
| 10 | 410,481 | 52 | 0 |

Core counts include repetitions under the choice of mark. This leaves $1\le k\le6$. An independent extension checker tries all eight-subsets of the twenty rows and tests every compatible triple of new columns. Its positive control deletes three eight-columns from the 185 witness and recovers a valid 185-one completion. [Extension checker](extend_eights.py)

## Replay

From this directory, run the following commands. The first checks the small reductions and the cases with exactly three or four eight-columns described above. The second also checks the general heavy-row restriction and the four complete seven-row branches.

```sh
python3 verify_core_bounds.py --jobs 8
python3 verify_core_bounds.py --jobs 8 --full --sevens 7 8 9 10
```
