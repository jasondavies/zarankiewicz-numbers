# Bounds for the 21 × 21 Zarankiewicz number for K₃,₃

**The remaining values are 193, 194 and 195.** The witness has two lines of degree eight, thirteen of degree nine and six of degree ten on each side. Every triple of rows and every triple of columns has at most two common entries. Removing the first row gives the 185-one rectangle. [193-one matrix](witness-193.txt) · [20 × 21 bounds](../z20x21-k33/README.md)

## Upper bound and reduction to the rectangle

Deleting each row in turn gives $20w\le21\cdot187$, so $w\le196$. At 196 every row and column must have degree at least nine, since deleting one with degree at most eight would leave at least 188 on 20 × 21. We now exclude weights 194, 195 and 196 under the common hypothesis that every line has degree at least nine.

No two rows share six columns. Six columns need at least 54 ones and the two rows together with nineteen others supply at most 50. The transpose gives the same bound for column pairs. If a line has degree at least eleven, mark eleven of its entries. The other twenty lines give blocks of size at most five, pairwise intersections at most two, and total size at least 88. At least eight blocks must be fives, since twenty fours give only 80. There are six canonical families of at least eight compatible fives on eleven points. With $m$ fives one would need at least $88-60-2m=28-2m$ fours, even allowing every other block three entries. None of the six families admits that many mutually compatible fours. Thus every degree is nine or ten.

Let $h=w-189$, the number of ten-rows and also of ten-columns. At 196 and 195 some ten-row meets at least two ten-columns. At 194 some ten-row meets at least one. To see this, suppose each ten-row meets at most one ten-column for $h=7,6$, or none for $h=5$. Consider the incidences of the ten-rows on the $21-h$ nine-columns. The following minimum triple counts are obtained by distributing the required incidences as evenly as possible. Each triple of the $h$ rows can occur at most twice.

| $h$ | Nine-columns | Required incidences | Least covered row triples | Capacity $2\binom h3$ |
|---:|---:|---:|---:|---:|
| 7 | 14 | 63 | 98 | 70 |
| 6 | 15 | 54 | 42 | 40 |
| 5 | 16 | 50 | 22 | 20 |

Mark the ten columns of the chosen ten-row. Its twenty blocks have point loads eight or nine and total load at least 82 at weights 196 and 195, or at least 81 at weight 194. There are 149 canonical projections at threshold 82 and 5,636 at threshold 81. Completing each projection requires eleven more columns of degree nine or ten on twenty unmarked rows. The border checker excludes every completion at the corresponding weights. Repeated missing columns would violate the bound on column-pair intersections.

This excludes 196 unconditionally. At 195 some line has degree eight, since degree seven would leave 188 after deletion. Deleting it gives exactly 187 on 20 × 21. At 194 a line of degree at most eight leaves at least 186. Hence if the rectangular maximum is 185 then the square maximum is exactly 193.

## Replay

Run the following from this directory with Python 3.10+, C++20 and nauty installed. The square upper bound uses the rectangular upper bound, whose replay is linked above.

```sh
python3 verify_bounds.py
```
