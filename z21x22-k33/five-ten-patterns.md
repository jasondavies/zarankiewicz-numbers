# The five ten-columns in a 185-one parent

Suppose a 201-one rectangle on 21 × 22 has exactly two eight-columns. Delete them. The 21 × 20 remainder has weight 185, its columns have degree at least nine, and its rows have degree at least seven. It therefore has five ten-columns and fifteen nine-columns. Every row has degree at most nine. Each ten-column meets at least three units of row deficit, measuring deficit from nine. Two columns meet in at most five rows. [Degree bounds and proof](177-parent.md)

Up to permutations of the five ten-columns and of rows of equal degree, there are 27,379 possible patterns on these columns satisfying those conditions and avoiding a 3 × 3 all-ones submatrix. Each pattern still requires completion by fifteen nine-columns, followed by the deleted columns and further extensions to reach 217.

The four units of row deficit split as 2+2, 2+1+1 or 1+1+1+1. Two rows cannot both meet all five tens, since the other nineteen rows could contribute at most 38 entries on them, short of the required 40. This excludes 2+2. For 2+1+1 the seven-row meets every ten, and each ten meets at least one eight-row. The two eight-rows miss disjoint, nonempty sets of tens. At most two tens contain all three short rows. Their two miss counts therefore sum to between three and five. For four eight-rows, each ten misses at most one. If there are u tens meeting all four, and row i misses m_i tens, the other three short rows share u+m_i tens. Hence every m_i is at most 2−u, and their sum is 5−u. These conditions give the following table, allowing permutations within each miss profile.

| Miss counts of the eight-rows | Patterns |
|---|---:|
| 1,1,1,1 | 381 |
| 2,1,1,1 | 5,780 |
| 2,2,1,0 | 566 |
| 1,4 | 95 |
| 2,3 | 8,372 |
| 1,3 | 1,122 |
| 2,2 | 9,513 |
| 1,2 | 1,550 |

Run `python3 five_ten_patterns.py` to regenerate the counts, or add `--emit` for the row masks. The program fixes the short rows and enumerates the multiset of remaining row masks. It bounds single-column, pair and triple loads by 10, 5 and 2 respectively. After fixing multiplicities of masks with at least two entries, the five singleton counts and the empty-row count are forced. It identifies patterns under all permutations of the five columns preserving the degree-labelled short rows.
