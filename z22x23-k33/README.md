# The 22 × 23 Zarankiewicz number for K₃,₃ is 216

**The maximum is 216.** The [216-one rectangle](witness-216.txt) is obtained by deleting the last row of the [225-one square](../z23-k33/README.md). Here $z$ counts ones in a matrix avoiding an all-ones 3 × 3 submatrix.

In the OEIS this gives a(22) = 217 in [A006621](https://oeis.org/A006621), Zarankiewicz's problem k_3(n,n+1).

The final proof excludes 217 by bounding the sum of incident row excesses on each column, then counting the weighted incidences with nine-rows in two ways. Both possible counts of eight-columns give a contradiction. Run `python3 verify_217.py --jobs 4` for the final projection checks. [Proof of the exact value](exact.md) · [Replay](verify_217.py)

## Earlier reductions at 217 and 218

Every 217-one example would contain a 177-one parent on 19 × 21. Its first two eight-column extensions share at most five rows. [Parent reduction](../z21x22-k33/177-parent.md) · [Overlap bound and replay](short-overlap.md)

The [218-one exclusion](218.md) reduces the question to whether the witness can be improved by one. Replay it with `python3 verify_218.py --jobs 4`.

Every 217-one candidate now requires at least seven nine-rows. Each ten-column meets at least three of them. Deleting a nine-row in at least five ways gives 208 on 21 × 23 with minimum degrees nine on rows and eight on columns. [Degree bounds](six-nine-rows.md) · [Six-nine-row exclusion and replay](seven-nine-rows.md)

## Why 219 is impossible

First consider 21 × 23. Summing over single-column deletions gives $z(21,23)\le\lfloor23\cdot201/22\rfloor=210$ by the [21 × 22 result](../z21x22-k33/README.md). At weight 210, every column would have degree at least nine. Two rows could share at most five columns. Six shared columns would need at least 54 ones, while the two rows and the other nineteen could supply at most $12+19\cdot2=50$.

A row of degree at least eleven would give, on eleven of its columns, twenty blocks from the other rows. Each block has size at most five, two blocks intersect in at most two points, and the total size is at least 88. The [eleven-point lemma](../z21-k33/README.md) excludes this. Hence every row has degree ten, as the 21 row degrees sum to 210.

Write the column degrees as $9+e_j$. The nonnegative excesses sum to three. Over all rows the sum of incident excess is $\sum_j(9+e_j)e_j\ge30$, so some row meets at least two units of excess. Mark its ten columns. The twenty other rows give a projection on ten points with block sizes at most five, intersections at most two, point loads between eight and eleven, and total load at least 82. At least two blocks have size five, since twenty fours give only 80.

The ten-point enumerator returns 159 projections up to relabelling. The thirteen missing columns all avoid the marked row. They have degree nine or ten, since at most one excess unit remains. Their supports are distinct. Even two columns sharing six rows would require at least 60 entries on those rows, whereas at most $12+21\cdot2=54$ are possible. Exhausting the thirteen missing columns over all 159 projections gives zero completions to weight 210. The replay regenerates the projections and the eleven-point check from source.

Thus $z(21,23)\le209$. Row deletion now gives $z(22,23)\le\lfloor22\cdot209/21\rfloor=218$. A rectangle at 218 would have a nine-one row: every row has at least nine, and 22 tens would already total 220. Deleting such a row would attain 209 on 21 × 23.

At 209 the smaller rectangle requires at least four columns of degree eight, whose deletion leaves an extremal 177-one matrix on 21 × 19. [Restrictions at 209](../z21x23-k33/README.md)

## Replay

From this directory run the following with Python 3.10+, C++20 and nauty installed. The verifier checks every row triple and every column triple in both witnesses, checks the deletion between them, recovers a known nine-one extension as a positive control, and replays the obstruction on 21 × 23. The smaller exact input and its dependencies have separate replays linked above.

```sh
python3 verify_bounds.py --jobs 4
```

If nauty is not on the compiler's default search paths, pass its include and library paths through `CXXFLAGS` and `LDFLAGS` as described in the [top-level README](../README.md).

At 217 every column has at least eight ones. A seven-column would extend the unique extremal square, which has no such extension. [22 × 22 classification](../z22-k33/unique.md)

Every 217-one rectangle has a column of degree exactly eight. Deleting it leaves a 209-one 22 × 22 parent. The parent must be inclusion-maximal. An eight-one column extension of any such parent would settle the rectangle at 217. [Projection and degree-profile proof](min9.md)

A 217-one rectangle has **exactly one or two eight-columns**. Deleting all of them gives a core of weight 209 on 22 × 22 or 201 on 22 × 21, respectively. Every remaining column has degree at least nine and every row has degree at least eight. Five or more eight-columns are impossible by deletion, and four would require a 185-one matrix on 19 × 22 with minimum row degree nine. The final three-column exclusion uses degree profiles and completes a search on 193-one cores. [Five-column deletion](eight-column-count.md) · [Four-column exclusion](four-column-cover.md) · [Three-column projections](three-columns.md) · [Three-column exclusion and replays](three-profile-proof.md)

In the two-column case the transposed 201-one core must contain a 193-one square different from the stored extremal witness in both orientations. Its maximum admissible row has size exactly eight. [201-one extension test](two-columns.md)

In the one-column case, if every row of the 209-one parent has degree at least nine, just two degree profiles remain. The same profile occurs on both sides. [209-one square parent](square-parent.md)

The two-column case and the one-column case whose square parent has an eight-row both contain a 193-one square. The stored 193-one square fails both extension tests. [Common reduction](../z21x22-k33/smaller-parent.md)

A 217-one rectangle cannot retain any thirteen complete rows of the known 225-one square, allowing row and column permutations and either orientation of the square. For each set of thirteen retained rows, nine new rows may be chosen freely. They have degree at least eight by the 21 × 23 bound, and repeated supports would share too many columns. Enumerate all supports compatible with two retained rows, then check each new pair against the retained and previously added rows. The 1,144,066 choices of retained rows form 20,371 orbits in each orientation. A positive control recovers a 216-one rectangle. Run `python3 verify_refill.py --jobs 3` to replay. [Whole-row replacement search](verify_refill.py)

Of the two minimum-degree-nine square-parent profiles just described, the one containing an eleven-line is excluded. Only eleven nines and eleven tens on each side remain. [Exclusion and remaining search](last-profile.md)

The common 201-one branch always contains a 185-one rectangle on 21 × 20, together with two compatible eight-columns. The other branch is the single nine-and-ten 209-one profile. [Reduction through 193](../z21-k33/eight-lines.md)

The remaining nine-and-ten 209-one profile is now excluded as well. **Every 217-one rectangle would contain an extremal 201-one rectangle on 21 × 22 (possibly transposed), and an extremal 185-one rectangle on 21 × 20.** [Completed exceptional profiles](last-profile.md)

In every extremal 201-one rectangle on 21 × 22, each row meets at most nine columns of degree at least nine. This restricts both extension orders at 217. [High-column bound and replay](../z21x22-k33/high-columns.md)

Every 201-one parent has at least three eight-columns. Hence two extension orders cover 217: from 177 on 21 × 19 add three eight-columns, then two eight-rows or an eight-row and an eight-column. [185-one obstruction and exhaustive replay](../z21x22-k33/three-low-columns.md)

Every 217-one rectangle has an automorphism group of order a power of two, allowing the trivial group. The prime-order reduction and the two order-three exhaustions exclude every odd prime. [Prime orders](odd-symmetry.md) · [Two fixed columns](four-fixed-rows.md) · [Five fixed columns and full result](no-odd-symmetry.md)

At weight 193 on 20 × 22, at least eight columns have degree eight, even allowing eight-rows. At weight 201 on 20 × 23, at least nine do. [Five-column exclusion](six-low-columns.md) · [Six- and seven-column exclusions](eight-low-columns.md)

Every 217-one rectangle has minimum row degree nine. In particular, at least four different row deletions would give 208 on 21 × 23, and at least one row has degree eleven or more. [Nine-row incidence count](nine-rows.md) Its 201-one parent always has minimum row degree nine as well. In the one-eight-column case its 209-one square parent has a unique eight-row, which the restored eight-column must hit. In the two-eight-column case, on transposing the rectangle write the final two eight-rows as A and B. Restoring either alone to the 201-one parent produces a 209-one square with at most one eight-column, since deleting any eight-column leaves a transposed 201-one parent of minimum column degree nine. Thus A and B each cover at least q−1 of the parent's q eight-columns. [193-one short rows](short-rows.md) · [201-one parent](../z21x22-k33/parent-minimum.md) · [Exclusion of 209 on 21 × 23](../z21x23-k33/no-209.md)
