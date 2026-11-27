# Overlap of the eight-lines in the reconstruction of 217

The two eight-columns added to a 21 × 19 parent to obtain a 193-one square share at most five rows. The same bound holds for any two eight-columns of a 201-one 21 × 22 rectangle, and for the two eight-columns in the two-column branch of 217. [Reconstruction from 177](../z21x22-k33/177-parent.md)

If the columns share six rows, remove the two columns and choose six of their shared rows to remove. Each remaining column has at most two ones on the six rows. In the three applications this forces the following many ones in the complementary rectangle.

| Original matrix | Complement | Minimum | Upper bound |
|---|---|---:|---:|
| 193 on 21 × 21 | 15 × 19 | 193 − 16 − 38 = 139 | 138 |
| 201 on 21 × 22 | 15 × 20 | 201 − 16 − 40 = 145 | 144 |
| 217 on 22 × 23 | 16 × 21 | 217 − 16 − 42 = 159 | 158 |

For the last upper bound, successively average column deletions starting from 137 on 16 × 18. The integer bounds for widths 19, 20 and 21 are 144, 151 and 158. [16 × 18 bound](../z16x18-k33/README.md)

## The 15-row complements

Table 4 of Collins et al. gives upper bounds 124 and 132 on 14 × 18 and 15 × 18. Averaging line deletions gives upper bounds 130 and 136 on 14 × 19 and 14 × 20. We orient the matrices below with fifteen columns. [Published bounds](https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf)

At 139 on 19 × 15 each row has degree at least seven and each column at least nine. Two rows cannot share five columns, which need at least 45 entries but would have capacity 44. A marked row of degree d therefore has 18 outside blocks of size at most four on its d columns. Two blocks share at most two marked points. Each point has load at least eight, so d is at most nine. Some row has degree eight or nine by averaging. At these degrees the canonical generator yields respectively 114 projections and one projection. Enumerate the missing columns of degrees nine through thirteen on the eighteen outside rows. The upper degree 13 follows because only four units above nine are available in the whole matrix. None completes.

At 145 on 20 × 15 each row has degree at least seven by the preceding exclusion and each column has degree at least nine. Two rows share at most five columns, since six would need 54 entries against capacity 48. Ten marked entries on one row would give nineteen blocks on ten points with minimum load eight and total at least 80. There are no such projections. A nine-row gives 1,226 projections on nine points. None completes to 145 even with missing columns allowed any degree from nine through nineteen.

The remaining row degrees are seven and eight. Some column has degree at least ten. Two columns share at most five rows, as six rows require 42 ones against capacity 38. Mark a longest column. Its point loads on the fourteen outside columns are six and seven, so its degree is at most eleven. There are no eleven-point marks at load at least 66 and eleven ten-point marks at load at least 60. The latter all fail completion by rows of degree seven or eight. Distinct missing supports suffice in both proofs. Identical columns of size at least nine would leave each of the other columns at most two entries on those rows, and identical rows of size at least seven violate the row-pair bound.

Run `python3 verify_overlap.py` to regenerate each catalogue and check the exclusions. [Replay](verify_overlap.py)

## Consequence when two final eight-columns share five rows

Delete both final eight-columns from 217 and transpose to obtain U of weight 201 on 21 × 22. The five commonly occupied positions become five columns of U. Each has degree at least eight by the 193 bound on 21 × 21. Each of the 21 rows meets at most two of these columns, since the two deleted lines contain all five. Thus the sum of these five degrees is between 40 and 42. At least three of them are eight. In particular this overlap forces three parallel eight-columns in U. Deleting any three of these gives a 177-one parent directly, and when U has exactly two eight-columns the two final columns can share at most four rows.
