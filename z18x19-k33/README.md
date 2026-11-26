# The 18 × 19 Zarankiewicz number for K₃,₃ is 156

**The maximum is 156 ones.** The [156-one witness](witness-156.txt) extends the [150-one square](../z18-k33/README.md) by a column with ones in rows 1, 2, 4, 7, 16 and 18 (numbered from one). Every triple of rows has at most two common ones. A hypothetical 157-one matrix would have between two and nine columns of degree seven. The exhaustive marked-row search excludes every one of these cases. A second 156-one matrix extends to an extremal 164-one square. [Marked-row proof](marked-search.md) · [19 × 19 corollary](../z19-k33/README.md) · [Square census and two-column reduction](square-cores.md)

In the OEIS this gives a(18) = 157 in [A006621](https://oeis.org/A006621), Zarankiewicz's problem k_3(n,n+1).

## Excluding 158

Suppose a matrix of weight 158 exists. Any heavier example could be reduced to that weight. Every column has degree at least eight by the 18 × 18 result. Every row has degree at least eight too. Indeed, the [17 × 18 maximum of 143](../z17x18-k33/README.md) gives $z(17,19;3,3)\le\lfloor19\cdot143/18\rfloor=150$ by summing over all single-column deletions.

Two rows cannot share six columns. Those columns have at least 48 ones, while two covering rows and sixteen other rows could supply at most $12+2\cdot16=44$. Also, all columns are distinct. Even at weight 157, two columns sharing seven rows could supply only fourteen ones there, and the seventeen other columns at most 34. The seven rows require at least 49 since every row has degree at least seven.

Mark a row of maximum degree and take $t$ points in it. The other seventeen rows give blocks on these points. Each block has size at most five and two blocks intersect in at most two points. The load of a point is its column degree minus one. Write $S$ for the total load. At weight 158 the sum of all column degrees above eight is six. Hence every load is between seven and thirteen.

- If the marked row has at least eleven entries, choose eleven of them. Their load is at least 77. The [eleven-point check](../z18-k33/README.md) rules this out.
- At maximum row degree ten, mark the whole row. Then $S\ge70$. Allowing loads up to thirteen gives 978 distinct ten-point projections. None extends by the nine missing columns to 158.
- At maximum row degree nine, there are fourteen rows of degree nine and four of degree eight. Write $e_j=c_j-8$ for column $j$ of degree $c_j$. Each column with $e_j>0$ meets at least $c_j-4\ge5$ of the fourteen high-degree rows. Thus these rows together see at least $5\sum_j e_j=30$ units of column excess, counting an incidence with column $j$ as $e_j$ units. Some nine-row sees at least three units. Mark this row, giving $S\ge9\cdot7+3=66$. None of the 2,418 resulting projections admits the ten missing columns of a 158-one matrix.

Maximum degree at most eight would give at most 144 ones. The [ten-point generator](../z18-k33/ten_points.cpp) and [nine-point generator](../z16x17-k33/catalogue.cpp) canonicalize the block multisets. The [border checker](../z16x18-k33/borders.cpp) completes the other columns on the seventeen unmarked rows and checks every triple.

## Reducing the 157-one case

Suppose first that every column has degree at least eight. The total column excess above eight is now five. The eleven-point argument still applies, and the 978 ten-point projections again give no completion. If the maximum row degree is nine, there are $13+x$ nine-rows and $5-x$ lower-degree rows, where $x$ is the number of seven-rows and $0\le x\le2$. Every column of positive excess meets at least four of the nine-rows. They therefore see at least twenty units of excess among at most fifteen rows. Marking a nine-row with at least two such units gives $S\ge65$. All 87,842 projections with loads from seven through twelve fail the completion test.

Consequently a 157-one matrix must have a seven-one column. Deleting it leaves an extremal 150-one square. Conversely, a legal seven-one extension of any such square settles the value at 157. A row of degree seven must avoid every column of degree seven, because deleting an incident pair would leave 144 ones on 17 × 18. The [square census](square-cores.md) further excludes a unique seven-one column. The [marked-row proof](marked-search.md) excludes all remaining counts of seven-one columns, completing the upper bound.

## Replay

With Python 3.10+, a C++20 compiler and nauty installed, run

```sh
python3 verify_exact.py --jobs 8
```

If nauty is not on the compiler's default search paths, pass its include and library paths through `CXXFLAGS` and `LDFLAGS` as described in the [top-level README](../README.md).

The driver verifies the witness, regenerates the projection catalogues and exhausts every case at 157. To replay just one case, add `--case 0` through `--case 9`. A full replay uses the 17 × 18 and 18 × 18 upper bounds proved in the adjacent directories. The [PDF](z18x19-exact.pdf) includes the witness and the proof.
