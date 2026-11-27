# The 21 × 22 Zarankiewicz number for K₃,₃ is 201

The [201-one matrix](witness-201.txt) extends the [193-one square](../z21-k33/witness-193.txt) by one column. The proof uses the previously established maxima of [185 on 20 × 21](../z20x21-k33/README.md) and [193 on 21 × 21](../z21-k33/README.md).

In the OEIS this gives a(21) = 202 in [A006621](https://oeis.org/A006621), Zarankiewicz's problem k_3(n,n+1).

## Why 202 forces a particular ten-row

Write the weight of a matrix for its total number of ones and the degree of a row or column for its number of ones. Summing the weights after deleting each column in turn bounds the 21 × 22 maximum by ⌊22 · 193 / 21⌋ = 202. The same argument bounds the 20 × 22 maximum by ⌊22 · 185 / 21⌋ = 193. A 202-one matrix on 21 × 22 must therefore have minimum degree nine on both sides.

Two rows can share at most five columns. Six shared columns require at least 54 ones, while the two rows contribute 12 and the other 19 rows contribute at most two each. Likewise two columns cannot share six rows, since 12 + 2 · 20 = 52 < 54. These arguments use the prohibition on an all-ones 3 × 3 submatrix.

If a row has degree at least eleven, mark eleven of its columns. Each of the other twenty rows meets them in a block of size at most five. Two of these blocks meet in at most two points, and each marked point occurs in at least eight blocks. This contradicts the [eleven-point lemma](../z21-k33/README.md), which excludes total load at least 88. The replay checks its six families again. Hence exactly thirteen rows have degree ten and eight have degree nine.

Write the column degrees as 9 + eⱼ. The nonnegative excesses sum to four. Some ten-row meets columns of total excess at least two. If a column has excess at least two, its degree is at least eleven and it must meet a ten-row. Otherwise four columns have degree ten. If each ten-row met at most one of those four columns, the eight nine-rows would have at least 40 − 13 = 27 incidences with them. Distributing 27 incidences as evenly as possible gives five rows with three and three rows with four. These already cover 5 + 3 · 4 = 17 triples, whereas the four columns allow at most 2 · 4 = 8 triple occurrences.

## Exhaustion

Mark the ten columns of such a ten-row. On the other twenty rows they give twenty blocks on ten points, each of size at most five and each pair meeting in at most two points. Every point load is between 8 and 12, and their sum is at least 82. At least two blocks have size five, since twenty blocks of size four contribute only 80. The existing block enumerator generates 159 projections up to relabelling, all of total load 82. The twelve missing columns all miss the marked row. Each has degree at least nine and at most eleven, since at most two excess units remain. The border checker tries compatible sets of twelve such columns with the required weight. None of the 159 projections admits a completion. A repeated missing column would contradict the pair bound.

Run the joint replay from this directory with Python 3.10+, C++20 and nauty. It rebuilds the enumeration programs, checks both witness matrices and the eleven-point lemma, regenerates the projections, and exhausts their borders. The proofs of the two input maxima are linked above.

```sh
python3 verify_exact.py
```

If nauty is not on the compiler's default search paths, pass its include and library paths through `CXXFLAGS` and `LDFLAGS` as described in the [top-level README](../README.md).

Every extremal 201-one rectangle contains an extremal 193-one square, obtained by deleting an eight-column. [Proof and replay](smaller-parent.md)

In fact every extremal 201-one rectangle has at least two eight-columns. Their deletion leaves an extremal 185-one rectangle on 21 × 20. [Eight-lines theorem for 193](../z21-k33/eight-lines.md)

In every extremal 201-one rectangle on 21 × 22, each row meets at most nine columns of degree at least nine. This restricts both extension orders at 217. [High-column bound and replay](high-columns.md)

Every 201-one rectangle has at least three eight-columns. [Proof and exhaustive replay](three-low-columns.md) · [Bounds on high entries per row](high-columns.md) · [Incident column excess](row-excess.md)

Every 201-one rectangle has minimum row degree nine. The same deletion bounds give at most 200 on 20 × 23. [Short-row proof](parent-minimum.md)
