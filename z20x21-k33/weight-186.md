# Restrictions at weight 186 on 20 × 21

Every 186-one rectangle has a row of degree exactly eight. Deleting it leaves a 178-one matrix on 19 × 21. A 194-one square must contain two parallel eight-lines: the [square proof](../z21-k33/README.md) supplies one after transposing if necessary, and its deletion leaves a 186-one rectangle, whose eight-row is parallel to the first. Thus all three upper endpoints can be tested from the same 19 × 21 cores. An individual core gives 186 exactly when one eight-row can be added, and 194 exactly when two can be added together.

## Bounding the 19 × 21 submatrix

We obtain $177\le z(19,21;3,3)\le178$. Delete the two eight-rows of the [193-one square](../z21-k33/witness-193.txt) for the lower bound. For the upper bound it suffices to exclude exactly 179, since deleting entries preserves the forbidden-submatrix condition.

Suppose the weight is 179. Every row has degree at least nine by the [18 × 21 upper bound of 170](core-search.md), and every column has degree at least eight by the [19 × 20 maximum of 171](../z19x20-k33/README.md). Two rows cannot cover six common columns. These columns need at least 48 entries and can have at most $12+17\cdot2=46$. Two columns likewise cannot share six rows, since $54>12+19\cdot2$. Marking eleven rows of one column would give twenty blocks on eleven points, of sizes at most five, pairwise intersections at most two and total at least 88. The [eleven-point packing bound](../z21-k33/README.md) excludes this. Hence the column degrees are eight, nine and ten.

Let $h$ be the number of ten-columns. There are $10+h$ eight-columns and $11-2h$ nine-columns. Give a column of degree $d$ weight $d-8$, and let $W(R)$ be the sum of these weights on row $R$. Then $\sum_R W(R)=99+2h$. Mark a row of degree $d$. Each of the other eighteen rows gives a block of size at most five on the marked columns. Two blocks share at most two points, each point has load at least seven, and the total load is $7d+W(R)$. In particular $7d\le90$, so $d\le12$. At eleven marked points the eighteen-block catalogue is empty at load 80. A row with $d\ge11$ therefore has $W(R)\le2$, since we could retain three units of weight on a subset of eleven points.

There must now be a nine-row with $W\ge7$ or a ten-row with $W\ge5$. Otherwise the upper bounds on $W$ at degrees 9, 10, 11 and 12 would be 6, 4, 2 and 2 respectively. The row excess over nine sums to eight. With $n_{12}$ twelve-rows, the sum of those upper bounds is $98+2n_{12}$. As $n_{12}\le2$, this is too small if $h\ge2$. If $h=1$, two twelve-rows would each meet at least ten of the eleven eight-columns and have at least nine columns in common. If $h=0$, a twelve-row is required and contains all ten eight-columns. At least one further row has degree ten or more, since the twelve-row uses only three units of excess. This other row meets at least six eight-columns, again impossible.

The forced nine-row gives total load at least 70 and the ten-row gives at least 75. We enumerate 324 nine-point projections and 18 ten-point projections (for the latter, point loads are seven through nine). For each we fix the marked columns and exhaust the choices for the missing columns of degrees eight through ten. Their supports are distinct by the column intersection bound. None completes to 179. As a positive control the same border search reconstructs a 177-one example.

## The columns of a 186-one rectangle

Every row now has degree at least eight. Every column has degree at least seven. Deleting a column of degree at most five would exceed the 20 × 20 maximum, and deleting a six-column would leave the [unique 180-one square](README.md), which accepts at most four more entries in a column. There is at most one seven-column, since deleting two would leave 172 on 20 × 19. A seven-column avoids every eight-row. Deleting both when incident would leave 172 on 19 × 20.

To test the possibility of eighteen nine-columns, keep just those columns. This gives a 20 × 18 core of weight 162. Two rows cannot share six core columns since $54>12+18\cdot2$. A row of degree at least ten would therefore give nineteen blocks on ten points of load eight each, which is impossible by the empty catalogue at 80. Some row has degree nine by averaging. Mark this row. Its nineteen blocks give one of 1,136 canonical projections with nine points all of load eight. Two core columns cannot have identical supports. The nine common rows could then supply at most $18+16\cdot2=50$ entries between them, and the remaining eleven rows at most 99.

Enumerating the nine missing core columns over all 1,136 projections gives 55 completions, counted with the choice of mark and possible isomorphisms. For each completion we try every seven-subset of the twenty rows that can be added as a column, and test every mutually compatible triple, allowing repeated supports. No triple works. Any extension by three columns of degree at least seven would still work after each one was thinned to seven. This excludes every 186-one rectangle containing eighteen nine-columns.

With no seven-column, at least three eights are needed to get down from $21\cdot9=189$ to 186. Exactly three would leave eighteen nines, now excluded. With one seven-column, at least one eight is needed. Exactly one eight leaves nineteen nines. Exactly two eights leave seventeen nines and one ten, a [previously excluded 163-one core](core-search.md). Thus there are at least four eights, or one seven and at least three eights.

## If every row of the rectangle has degree at least nine

Put $e(R)=d(R)-9$, so the total excess is six. For a column $C$ write $H(C)=\sum_{R\ni C}e(R)$. Two columns cannot share six rows because $54>12+19\cdot2$. A column meeting eleven rows is excluded by the same eleven-point packing at 88 used above. The possible column degrees are now seven through ten. On the $t$ rows of a marked column the other twenty columns give blocks of sizes at most five, pairwise intersections at most two, and total load $8t+H(C)$.

* A ten-column has $H\le1$. At $H\ge2$ the ten-point catalogue has 159 projections with loads between eight and fourteen. At most four units of excess remain, so missing rows have degree nine through thirteen. None completes to 186.
* A nine-column cannot contain a row of degree at least twelve. Such a row would yield one point of load at least eleven and total load at least 75. There are 2,215 such projections, and none admits the eleven remaining rows of degrees nine through twelve.

In these searches two missing rows cannot have identical supports. Nine common columns would need at least 63 entries, against the capacity $18+18\cdot2=54$.

If a row has degree at least twelve it must therefore lie entirely in columns of degree below nine. With no seven-column, writing $h$ for the number of tens gives $h+3$ eights and $18-2h$ nines, hence at most twelve low columns. With one seven there are $h+1$ eights and $19-2h$ nines, hence at most eleven low columns. Only one possibility remains: twelve eight-columns all on this row, and nine ten-columns. Every other row meets at most six of those twelve eight-columns, since seven shared columns require 56 entries against a capacity of $14+18\cdot2=50$. The three remaining units of row excess cannot include another row of excess at least two, since it could meet no ten-column. Hence there are three ten-rows, each requiring at least four incidences with the nine ten-columns. Each ten-column admits at most one such incidence. This contradiction proves the maximum row degree is eleven.

## A nine-column is forced

Continue to assume that every row has degree at least nine. Write $a$ for the number of eleven-rows, so there are $6-2a$ ten-rows and $0\le a\le3$. Call these $6-a$ rows the high rows. We show that some nine-column has $H\ge3$.

Let $s$ indicate the presence of a seven-column and let $h$ count the tens. There are $L=h+3-s$ low columns (degree seven or eight) and $N=18+s-2h$ nine-columns. Suppose all nine-columns have $H\le2$.

For $a=0,1$, the high rows carry $60-9a$ entries. At most $2N+h$ of them lie outside the low columns. Put $T=60-9a-2N-h$. Distributing $T$ entries among $L$ columns as evenly as possible minimizes the number of triples of high rows occurring together. With $T=dL+r$ the minimum is $(L-r)\binom d3+r\binom{d+1}3$. Checking $0\le h\le9$ and $s=0,1$, discarding $T>(6-a)L$, gives at least 66 triple occurrences for $a=0$ and at least 24 for $a=1$. Each triple can occur only twice, so the respective budgets are 40 and 20.

For $a\ge2$ fix two eleven-rows $P,Q$. They avoid the tens, and whenever one meets a nine-column it is the only high row there. Let $u$ be the number of zeros in these two rows on low columns and let $v$ be the number of nine-columns avoiding both. Counting their 22 entries gives $u+v=2L+N-22=2-s$. A third high row meets at most $u+2$ low columns, since it shares at most two columns with both $P,Q$. It meets at most $v$ nines. When $a=3$, the third eleven-row also avoids the tens, giving at most four entries. When $a=2$, the other two high rows are tens. Together they have at most $2(u+2+v)+h\le17$ entries, but they need twenty.

Thus a nine-column with $H\ge3$ is unavoidable. Its twenty-block projection has minimum load eight and total at least 75. There are 168,725 canonical projections, all with $H$ between three and six. The search fixes the nine incident rows and tries all eleven missing rows of degree nine through eleven, with their maximum degree also bounded by $15-H$. None completes to 186. This excludes every rectangle in which all rows have degree at least nine.

## What remains after deleting the eight-row

Deleting an eight-row of a 186-one rectangle leaves 178 on 19 × 21. Every 178-one matrix there has minimum row degree eight or more and minimum column degree seven or more, by the bounds of 170 on 18 × 21 and 171 on 19 × 20. At most two columns have degree seven, since deleting three would leave 157 on 19 × 18. Thus a seven-column gives an extremal 171-one core on 19 × 20, and two give an extremal 164-one square on 19 × 19. An eight-row in a 178-one matrix avoids each seven-column, since deleting both when incident would leave 164 on 18 × 20.

Every row of a 178-one matrix has degree at most thirteen. Two rows sharing seven columns would require at least $7\cdot8-2=54$ entries on those columns against a capacity of $14+17\cdot2=48$. If two rows share six columns, both seven-columns must belong to the intersection, since the capacity is $12+17\cdot2=46$. Therefore, among the eighteen blocks on a marked row of degree $d$, all size-six blocks contain the same two points. Their other four points are pairwise disjoint. For $d\ge14$ the total load is at most $90+\lfloor(d-2)/4\rfloor\le94$, but at least $7d-2\ge96$.

Two further restrictions distinguish the cases with one or more eight-rows in the original 186-one rectangle.

* With exactly one eight-row every column has degree at most ten. Two columns sharing six rows would require at least 53 entries there against a capacity of 50. Any column contains at most ten rows of degree nine or higher by the eleven-point bound at 88. Thus an eleven-column would contain the unique eight-row; its twenty blocks have total at least 87, minimum point load seven, and at most one point of load seven. Just three projections meet these conditions. None admits nine more rows of degree at least nine. The maximum degree sixteen used in the replay follows because the positive row excess above nine sums to seven. Deleting the eight-row leaves a 178-one core in which all nineteen rows have degree at least nine. Any ten-column of that core meets at most one unit of row excess over nine. Otherwise it induces one of the same 159 projections at total 82, even allowing point loads up to fifteen. At most five units of excess remain for the nine missing rows. All 159 fail at weight 178. Likewise a nine-column of the core meets at most three units of excess. The 2,245 projections at total 76 or more leave at most three units on the ten missing rows, and none completes.
* With two or more eight-rows, deleting any two gives a 170-one matrix on 18 × 21. Every column there has degree at least seven by the bound of 163 on 18 × 20. There must in fact be at least two seven-columns. A sole seven-column would leave 163 on 18 × 20 with all columns of degree at least eight, [already excluded](core-search.md). If all columns had degree at least eight, any two rows would share at most five columns, since $48>12+16\cdot2$. The seventeen-block catalogue on eleven points is empty at load 77, so every row has degree at most ten. Some row has degree ten by averaging. Its ten-point projection has total at least 70 and minimum point load seven. The 978 possibilities all fail to admit eleven more columns. Their degrees must lie between eight and ten because the total column excess above eight is two. Two such missing columns cannot coincide: their eight common rows could supply at most $16+19\cdot2=54$ entries, leaving at least 116 on ten rows. Those ten rows can supply at most 100 entries by the row-degree bound just proved. [The 18 × 20 proof and eleven-point catalogue](core-search.md)

In particular, a full eight-column can meet at most one eight-row in a 186-one rectangle. Otherwise deleting two incident eight-rows would leave a column of degree six in the 170-one submatrix.

## Replay

From this directory run:

```sh
python3 verify_weight_186.py --jobs 8
```

The replay compiles the existing canonical block generators and border enumerator, checks the 177-one witness, and tests the three-column extension routine on a deletion of the 185-one witness. The numerical bounds for smaller rectangles and the 163-one core exclusion are established in the linked earlier proofs.

To test a 178-one witness, run `python3 extend_178.py matrix.txt`. The checker tries all eight-subsets of the 21 columns as new rows, then tests the legal pairs. It prints a largest extension through two additions. As a control the main replay deletes both eight-rows from the 193-one square, reconstructs two legal rows and verifies the resulting square.
