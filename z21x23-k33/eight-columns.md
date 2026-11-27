# Eight eight-one columns at weight 209

In a 209-one matrix on 21 × 23 there is **at most one row of degree eight**, and **every row has degree at most thirteen**. **Exactly eight columns of degree eight is impossible.** The proof uses short rows (full degree eight or nine) to exclude every degree profile on the other fifteen columns, whose total weight would have to be 145. This step leaves zero through three eight-one columns in the parent. The subsequent nine-row enumeration excludes three. [Seven-column proof](seven-columns.md)

## Deleting short rows

Write $z(m,n)$ for the maximum avoiding an all-ones $3\times3$. On **eighteen rows** with every column of degree at least eight, every row has degree at most ten, independently of the width. Two rows cannot share six columns, since their twelve entries and at most two on each other row give 44 rather than the required 48. Eleven columns on a single row would therefore give seventeen blocks of size at most five on eleven points, meeting pairwise in at most two points and having total load at least 77. The eleven-point catalogue excludes this. [Eighteen-row argument](../z18x19-k33/marked-search.md)

On 18 × 22, consider weight 177 or 178 with minimum column degree eight. There are at least fifteen ten-rows and at least one column of degree nine or more. Some ten-row meets that column. Its ten marked points have load at least seven each, totalling at least 71 in the other seventeen rows. There are three projections. None accepts twelve more columns of degree at least eight at either weight. At weight 178 minimum column degree eight follows from $z(18,21)\le170$. Hence **$z(18,22)\le177$**. At weight 185 on 18 × 23 every column would then have degree at least eight, forcing total weight at most 180. Thus **$z(18,23)\le184$**. [18 × 21 bound](../z20x21-k33/core-search.md)

Moreover, **184 on 18 × 23 requires at least five seven-columns**. All columns have degree at least seven. Zero sevens gives at most 180. One seven leaves the excluded 177 with minimum column degree eight on 18 × 22. Two sevens leave 170 with minimum column degree eight on 18 × 21, already excluded. With three or four sevens, deleting three gives 163 on 18 × 20 with at most one seven-column, also excluded. [170-one restriction](../z20x21-k33/core-search.md) · [163-one restriction](../z18x20-k33/README.md)

Now suppose there are 193 ones on 19 × 23. Every row has degree at least nine. Every column has degree at least eight, since column deletion from $z(19,21)=177$ gives $z(19,22)\le185$. Put $e_j=c_j-8$ for each column, and $W_i=\sum_{j\ni i}e_j$. The sum of the excesses is nine. Over all nineteen rows the score $2d_i+W_i$ sums to
$$
2\cdot193+8\cdot9+\sum_j e_j^2\ \ge\ 467.
$$
Some row scores at least 25. The nineteen-row marked-line lemmas apply at any width when all columns have degree at least eight. Row degree is at most twelve, an eleven-row has $W_i\le2$, and a twelve-row has $W_i=0$. These rows score at most 24. Thus a maximizing row has degree nine or ten. [Score and marked-line lemmas](../z19x21-k33/README.md)

* A nine-row needs $W_i\ge7$. Its nine marked points have load at least 70 on the other eighteen rows. Deleting this row leaves 184 on 18 × 23, so at least five of its columns had degree eight. Their marked point loads are exactly seven. Of 324 projections at the load threshold, 21 satisfy this restriction. None completes.
* A ten-row needs $W_i\ge5$ and total marked load at least 75. None of the 24 projections completes.

In both cases each missing column avoids the marked row and has degree at least eight. Distinct missing supports suffice throughout the deletion proof. In the eighteen-row minimum-degree-eight tests every row has degree at least seven by the total and the upper bound of ten, with at most three units of deficit below ten. Eight common rows would already need at least 77 entries, above the two-column capacity of $16+20\cdot2=56$. In the nineteen-row test all rows have degree at least nine, giving the same contradiction. This proves **$z(19,23)\le192$**. Deleting two eight-rows from 209 ones would leave 193, so every possible 209-one matrix has at most one eight-row. [Replay](verify_eight_columns.py)

## Loads on columns of degree eight and ten

Write $D=\sum_r(10-d_r)_+$ and $S=\sum_r(d_r-10)_+=D-1$. The earlier bounds give $D\ge4$, at most eight eight-columns, and at least four. An eight-row avoids these columns, a nine-row meets at most one, and a row of degree $10+s$ with $s>0$ meets at least $s+2$. [Row and column bounds](parent-extensions.md)

Mark a column of degree exactly ten. If its ten rows carry at most two deficit units, any six of them need at least 58 ones. Two columns sharing six rows can supply only twelve entries there and at most two on each of the other 21 columns, giving 54. Thus the other 22 columns give blocks of size at most five meeting pairwise in at most two marked rows. Their loads total at least 88. At total 88 the marked rows have exactly two deficit units and no excess. There are 25,141 projections at this equality. At totals of at least 89 another 458 projections meet the deficit limit. None accepts the eleven remaining rows at weight 209. Distinct missing rows suffice since seven shared columns would need at least 56 ones against capacity 52. Thus **every ten-column carries at least three units of row deficit**.

If $D=4$, the eleven-row deficit lemma bounds all column degrees by ten. For $q$ eight-columns the number of ten-columns is $t=q+2$. Regard each unit of deficit as a copy of its row. The four copies can be divided into two pairs of distinct rows since each row contributes at most two copies. Two distinct rows can share at most four ten-columns, since five would need 50 entries against capacity $10+19\cdot2=48$. Each pair therefore contributes at most $t+4$ deficit incidences on the ten-columns. They need at least $3t$, forcing $t\le8$. In particular **$D\ge5$ at both $q=7$ and $q=8$**. [Eleven-row lemma](parent-extensions.md)

Now mark an eight-column. Its eight rows have degree at least nine. If another column shared six of them, those six rows would each have degree exactly nine by the capacity 54 above. Each meets only the marked eight-column among the low columns. A second shared low column is impossible. If the second column is high, another low column misses all six rows, preventing equality in the capacity 54. Once again all 22 blocks have size at most five, and every point has load at least eight. At total load at least 76 there are 2,041 projections, and none accepts thirteen remaining rows. Hence **the total full degree of the eight rows on any eight-column is at most 83**. Equivalently, the sum of $d_r-10$ there is at most three.

Suppose some row has degree $10+s$ with $s\ge4$. Choose six low columns on it. Their combined net excess is at most 18. There are at most two other low columns, so each other long row of excess $u$ meets at least $u$ of the six and contributes at least $u^2$. A nine-row contributes at worst minus one across all six, and an eight-row contributes zero. The number of nine-rows is at most $D$. Thus the net excess is at least
$$
6s+\sum_{\text{other long rows}} u^2-D
\ \ge\ 6s+(D-1-s)-D=5s-1\ \ge\ 19,
$$
a contradiction. This gives the upper bound of thirteen on every full row.

Finally, at $q=8$, ten short rows could contain at most ten of the 64 ones on the low columns. The remaining eleven rows would have at least 54 on just those eight columns, exceeding $z(8,11)\le53$. There are therefore at most nine short rows. The deficit lower bound of five and the single possible eight-row require at least four. If there are exactly nine short rows, at least seven of them must meet a low column, by $z(8,12)\le57$. [Collins et al., Table 4](https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf)

## Excluding the fifteen high columns

Assume $q=8$. Let $a$ be the number of eight-rows and $K$ the number of short rows. We have $a\le1$, $K\le9$ and $D=K+a\le10$. Give each high column of degree $c$ the weight $e=c-9$. These weights sum to ten. Write $W_r$ for the sum on the high entries of short row $r$.

**Every short row has $W_r\le4$.** Otherwise mark eight of its high entries capturing at least five units. The row has eight or nine high entries. In the nine-entry case drop a zero-weight entry if possible. If all nine weights are positive, any eight suffice. Every other row meets at most five of the marked columns, and two such rows share at most two marked columns. The twenty blocks on the mark have point loads at least eight and total load at least $8\cdot8+5=69$.

There are 181,521 projections. For a row with eight high entries, none accepts the seven remaining high columns at weight 145. For a row with nine high entries, the ninth column must select at least eight of the twenty blocks, pairwise meeting in at most one point. There are 206 selections of eight blocks, three of nine and none larger. None of the 209 enlarged projections accepts six more high columns at weight 145. These searches allow every missing degree from nine through twenty. Identical missing high columns would share at least nine rows of full degree at least eight, requiring at least 72 incidences where two columns and the other 21 can supply only $18+42=60$ on a chosen nine. [High-column replay](verify_eight_columns.py)

Write $D_j$ for the total row deficit on column $j$. Double counting the weighted incidences with short rows gives
$$
\sum_{j\text{ high}}(c_j-9)D_j=\sum_{r\text{ short}}(10-d_r)W_r\le4D\le40.
$$
A ten-column has $D_j\ge3$. For $c_j\ge11$ delete its $c_j-11$ largest incident deficits. The eleven rows left still carry at least five units. Each discarded deficit was at least one, so $D_j\ge c_j-6$. Charging three per unit of column weight already uses 30. Each eleven-column costs at least four more, a twelve-column costs nine more, and a column of degree at least thirteen costs at least sixteen more. This leaves just the four profiles below. [Eleven-row deficit lemma](parent-extensions.md)

| Degrees above ten | Nine-columns | Least weighted deficit | Least $K$ | Required triples of nine-columns | Available |
|---|---:|---:|---:|---:|---:|
| None | 5 | 30 | 7 | 28 | 20 |
| One eleven | 6 | 34 | 8 | 56 | 40 |
| Two elevens | 7 | 38 | 9 | 84 | 70 |
| One twelve | 7 | 39 | 9 | 96 | 70 |

For the last two columns of the table, each short row contains at least eight high entries. With $W_r\le4$ at least four are nine-columns. Each incidence with an eleven-column forces one additional nine-column in that row, and each incidence with a twelve-column forces two. Raising the number of nine-columns in a short row from $m$ to $m+1$ adds $\binom m2\ge6$ triples. Each eleven-column contains at least four short rows, and a twelve-column contains at least five, since at most one short row supplies two deficit units. The resulting lower counts exceed twice the number of distinct triples in every profile. A third occurrence of any triple gives a forbidden all-ones $3\times3$.

Hence **the full matrix must have four through seven eight-columns**. Deleting any four leaves a 177-one parent with **zero through three eight-columns**. The next endpoint has sixteen high columns carrying 153 ones. The same projection test at load 70 excludes 3,768 eight-point projections and three ninth-column extensions at this weight. Thus $W_r\le5$ on each short row. High-column weights sum to nine and every positive-weight column carries at least three deficit units, so $5D\ge27$ and **$D\ge6$ when $q=7$**. The stronger nine-row bound excludes this endpoint. [Seven-column proof](seven-columns.md)

## Replay

From this directory run the following command. Use `--part residuals`, `--part columns`, `--part high` or `--part next` to replay a single part. The column-load checks need several GB of memory per worker.

```sh
python3 verify_eight_columns.py --jobs 2
```
