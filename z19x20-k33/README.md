# The 19 × 20 Zarankiewicz number for K₃,₃ is 171

A 19 × 20 binary matrix can have **171 ones** while avoiding an all-ones 3 × 3. The witness consists of nineteen consecutive rows of the 9-regular cyclic square on twenty points. The proof below excludes 172. Erasing entries preserves avoidance, so this excludes every heavier matrix as well. [171-one witness](witness-171.txt) · [Cyclic construction](../z20-k33/README.md)

In the OEIS this gives a(19) = 172 in [A006621](https://oeis.org/A006621), Zarankiewicz's problem k_3(n,n+1).

## Degree bounds at 172

Use the known maxima of 156 on 18 × 19 and 164 on 19 × 19. Summing over all twenty column deletions in an admissible 18 × 20 matrix gives $z(18,20;3,3)\le\lfloor20\cdot156/19\rfloor=164$. Thus in a hypothetical 172-one matrix every row and every column has degree at least eight. An eight-row and an eight-column cannot meet. Deleting both would leave $172-8-8+1=157$ ones on 18 × 19. [18 × 19 proof](../z18x19-k33/README.md) · [19 × 19 proof](../z19-k33/README.md)

## Case 1. There is an eight-row

Mark its eight columns. Each has degree at least nine by the nonincidence just proved. The other eighteen rows induce eighteen blocks on these eight points. Each point occurs at least eight times, giving total block size at least 64. Two blocks meet in at most two points, since the corresponding rows together with the marked row would otherwise give a forbidden triple. Each block has size at most five. Indeed, any six columns need at least 48 entries, while two rows covering all six could supply twelve and each of the other seventeen at most two, giving at most 46.

There are **114** such block multisets up to permutations of the points and blocks. For each, the eight marked columns are fully known. The missing twelve columns avoid the mark and each has degree at least eight. Each has degree at most twelve, because the marked columns already supply at least 72 ones and the eleven other missing columns require at least 88. The border checker tries every compatible choice attaining weight 172. None succeeds.

## Case 2. All rows have degree at least nine

Since $172=19\cdot9+1$, one row has degree ten and the other eighteen have degree nine. We first show that every column has degree at most nine. If a column covered ten rows, mark any ten of them. The other nineteen columns induce nineteen blocks on these ten points. Any pair of blocks meets in at most two points. A block cannot have size six or more, since six marked rows require at least 54 ones, while two columns covering them and eighteen other columns could supply at most $12+18\cdot2=48$. Each point has load at least eight. The catalogue of nineteen such blocks on ten points with total size at least 80 is **empty**.

Consequently twelve columns have degree nine and eight have degree eight. The ten-row must meet a nine-column. Mark this column and take its nine rows as points. The other nineteen columns again give blocks of size at most five with pairwise intersections at most two. Eight points have load eight and the point from the ten-row has load nine. Their total load is exactly 73. The generator returns 90 multisets with minimum point load eight and total at least 73, of which **81** have total exactly 73. In every case the ten missing rows omit the marked column and have degree nine. None of the 81 projections admits a completion.

## Exhaustion and replay

The generator adds blocks in nonincreasing order of size, including repeated pairs, singletons and empty blocks. It identifies isomorphic partial multisets by canonical labelling of the bipartite incidence graph with separate point and block parts. It prunes when the remaining blocks cannot meet the required point loads or total size. Each triple of points may appear at most once. Balancing the sizes of the remaining blocks gives a lower bound on how many additional triples they use, by convexity of $\binom d3$. [Projection generator](../z18x19-k33/small_points.cpp)

For each surviving projection, the checker generates every missing line support of the specified degrees that meets each pair of fixed lines in at most two positions. It then chooses distinct supports in index order, testing intersections with previously chosen lines and the target weight. Distinct supports suffice. Two identical missing columns in Case 1 would share at least seven rows, which require at least 56 ones and could contain at most $14+18\cdot2=50$. Two identical missing rows in Case 2 would share at least six columns, already excluded by the 46-entry bound. The replay also reconstructs a legal 171-one rectangle from a projection of the witness in each orientation and checks both returned completions. [Border checker](../z16x18-k33/borders.cpp) · [Replay driver](verify_exact.py)

From this directory run

```sh
python3 verify_exact.py
```

The replay uses the Python, C++20 and nauty dependencies listed in the [repository README](../README.md).
