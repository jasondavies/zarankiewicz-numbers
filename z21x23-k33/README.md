# The 21 × 23 Zarankiewicz number is 207 or 208

Deleting two nine-rows from the [225-one square](../z23-k33/README.md) gives 207. A 209-one matrix would give incompatible bounds on the number of nine-rows, so the upper bound is 208. [Exclusion of 209](no-209.md)

The earlier reductions below describe a hypothetical 209-one matrix. The [initial exclusion of 210](../z22x23-k33/README.md) already gave an upper bound of 209. At weight 209 every column has at least eight entries by the [21 × 22 maximum of 201](../z21x22-k33/README.md). Every row has at least eight entries by the deletion bound of 201 on 20 × 23.

## A row of degree at least eleven is necessary

If every row had degree at most ten, twenty rows would have degree ten and one would have degree nine. Some column has degree at least ten, since 23 nines total only 207. Mark ten of its rows. On these ten points the other 22 columns give blocks meeting pairwise in at most two points. No block has six points. Six marked rows need at least 59 entries, but the two columns and the other 21 can supply at most $12+21\cdot2=54$. Point loads are eight or nine and total at least 89.

There are 98 projections up to relabelling. Another row on the marked column would need at least eight blocks meeting pairwise in at most one point. None of the 98 projections admits such a choice. The marked column therefore has exactly ten rows. All eleven missing rows avoid it, have degree nine or ten, and have distinct supports (two rows sharing even seven columns would require 56 entries against a capacity of 52). None of the 98 projections completes to 209.

## Every long row contains at most eight columns of degree above eight

Suppose a row of degree at least eleven contains nine columns of degree at least nine. Mark eleven of its columns, choosing at least nine of degree at least nine. The twenty other rows give blocks of size at most five. Six marked columns need at least $4\cdot9+2\cdot8=52$ entries, exceeding $12+19\cdot2=50$. Two blocks meet in at most two points. Every point load is at least seven, at most two loads are seven, and the total is at least 86.

Of the 105,383 projections at total load at least 86 and minimum load seven, 990 satisfy that final restriction on the number of sevens. None admits seven blocks meeting pairwise in at most one point. This means a further column through the marked row is impossible, since it would require seven more rows there. So the twelve missing columns avoid the mark. Each has degree at least eight, and their supports must be distinct. Eight shared rows would require at least 64 entries against a capacity of $16+21\cdot2=58$. The border search allows every degree from eight through twenty. None completes the matrix.

Consequently any row of degree $10+s$ with $s\ge1$ contains at least $s+2$ eight-one columns. In particular the cases with zero, one and two eight-one columns are excluded. At the other end, deleting fifteen eight-one columns would leave 89 entries on eight columns. Across the 21 rows these entries would use at least $16\binom43+5\binom53=114$ triples of columns, while only $2\binom83=112$ are available. Hence at most fourteen such columns are possible.

## A restriction on the remaining cases

An eight-row avoids every eight-column. Otherwise deleting the incident row and column leaves 194 on 20 × 22, whose upper bound is 193. A nine-row meets at most one eight-column, since deleting it and two incident eight-columns leaves 186 on 20 × 21. Write $S$ for the total row excess above ten from the long rows. The total deficit below ten is $S+1$. Summing row excess $d-10$ over the entries in all eight-columns gives at least $3S-(S+1)=2S-1>0$. Thus some eight-column meets eight rows of total degree at least 81, all of degree at least nine.

With exactly three eight-columns every long row has degree eleven and contains all three. There are at most two such rows by the forbidden-submatrix condition. Deleting the three columns leaves an extremal 185-one matrix on 21 × 20. With four or more eight-columns, deleting any four leaves an extremal 177-one matrix on 21 × 19.

## Exactly three eight-columns

Let $h$ be the number of eleven-rows, either one or two. The deficit of the shorter rows below ten is $h+1\le3$. If a column had degree at least eleven, mark eleven of its rows. Each of the 22 other columns meets them in at most five points. Six rows need at least $60-3=57$ ones and two columns sharing them allow at most 54. The total size of these 22 blocks is at least $11\cdot9-3=96$. Some twenty of them then have total size at least 88. Indeed we may delete two blocks of size at most four, or take twenty fives if fewer than two such blocks exist. This contradicts the [eleven-point lemma](../z21-k33/README.md). The full column degrees are therefore three eights, fifteen nines and five tens.

Each eleven-row meets the three eights. If it also met a ten, its eleven-point projection would have total load at least 86, exactly three loads of seven, and all loads at most nine. The catalogue above contains 11,354 such projections. None accepts the twelve missing columns, all of degree nine or ten. Thus **every eleven-row uses the three eights and eight nines, avoiding all five tens**.

Some ten-column carries at most two units of row deficit below ten. Otherwise all five ten-columns must each see at least three units. There are at most three units in total, spread across at least two rows when there are three. Both rows would cover all five tens. Those columns need 50 incidences and the two rows together with the other nineteen can supply only $10+19\cdot2=48$.

Mark the ten rows on this column. They all have degree at most ten, since the long rows avoid the tens. No other column meets them in six points, by the six-row bound of 57 versus 54 above. At deficit zero or one the possible projections are the earlier 98. None completes even with missing row degrees eight through eleven. At deficit two the twenty-two blocks have total load 88. The point loads are either one seven and nine nines, or two eights and eight nines. There are **25,141** projections. This catalogue includes the possibility of zero five-blocks. At most one unit of deficit remains outside the marked column, so the eleven missing rows have degrees nine through eleven. None completes to 209. This excludes the entire case of exactly three eight-columns.

## Earlier reduction to four or five eight-columns

The parent-extension argument tightens the number of eight-columns to four or five. Deleting any four gives an extremal 177-one matrix on 21 × 19 with zero or one eight-column of its own. [Proof, two parent classes and extension checker](parent-extensions.md) Conversely, any such extremal matrix that admits four simultaneous eight-one column extensions gives 209 and settles the auxiliary problem. This gives a single extension problem covering every remaining case. Every 209-one matrix has at most one eight-row and maximum row degree thirteen. Counting the six low columns forces a row deficit of at most seven, while the short rows require at least eight. [Six-column exclusion and replay](six-columns.md) With four eight-columns the deficit is at most six, leaving twelve candidate row-degree profiles. [Four-column deficit-seven proof](four-deficit-seven.md) [Deletion bounds](eight-columns.md) · [Seven-column exclusion and replay](seven-columns.md)

The stored 185-one parent has exactly two possible eight-one extensions, and the stored 177-one parent has exactly three. In each case these extensions coexist and give 201 ones. Reaching 209 would require one more eight-column than either parent admits. Other extremal parents remain possible.

### An exhaustive list of four-column starts

We can choose the four eight-columns so that some long row meets at least three. The multiplicities of the sixteen possible row patterns determine the four columns up to row permutation. Four-column permutations further identify equivalent patterns. No two eight-columns can share six rows, since each shared row meets two eights and therefore has degree at least ten. For a pair sharing $t$ rows, let $b$ be the incidences of the other two marked columns on those rows. These rows need at least $10t$ entries, while the 19 remaining columns can supply at most two each. Hence $8t\le38+b$. In case of equality the shared rows all have degree ten, ruling out a long row in that pair.

Enforcing these constraints, the column degrees, and the upper bound of two on each triple intersection leaves **5,684** four-column patterns up to row and column permutations. Grouped by the size of the common intersection of all four columns, the counts are 4,167 at zero, 1,374 at one, and 143 at two. Run `python3 four_columns.py --emit` to print the 16 row multiplicities for each pattern in mask order 0 through 15. These are necessary starting configurations. A single full matrix may have several choices of four columns. [Four-column enumerator](four_columns.py)

A counting argument excludes 20 of the 143 starts with two common rows. An exhaustive completion search excludes start 4. The row-deficit bound then shows that 74 other starts can be omitted because every completion would also appear with fewer common rows. The reduced cover contains **48 in this group and 5,589 across all three groups**. [Row-deficit proof, reduced cover and replay](row-deficit.md) [Counting proof and pilot benchmark](two-common-rows.md) · [Complete start-4 proof and replay](start4.md)

Run the following from this directory with Python 3.10+, C++20 and nauty. It rebuilds the enumerators, checks the projection counts and completions, and tests each stored parent for extensions. The smaller exact bounds have separate replays. [20 × 21](../z20x21-k33/README.md) · [19 × 21](../z19x21-k33/README.md)

```sh
python3 verify_209.py --jobs 4
```

The [201-one minimum-degree theorem](../z21x22-k33/parent-minimum.md) supplies the final contradiction for both profiles. [Exclusion of 209](no-209.md)
