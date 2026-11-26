# The 18 × 18 Zarankiewicz number for K₃,₃ is 150

An 18 × 18 binary matrix can have **150 ones** while avoiding an all-ones 3 × 3. Every such matrix with 151 ones contains an all-ones 3 × 3. The rows and columns of the forbidden submatrix may be chosen anywhere.

The [150-one witness](witness-150.txt) has three rows of degree ten and fifteen of degree eight, with the same degrees on the column side. The verifier checks both the row triples and the column triples. The computer-assisted upper bound uses the [17 × 18 maximum of 143](../z17x18-k33/README.md). An earlier published upper bound for the square was 156. [Collins et al., Table 4](https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf)

In the OEIS this gives a(18) = 150 in [A350304](https://oeis.org/A350304), 151 in [A001198](https://oeis.org/A001198), 174 in [A350237](https://oeis.org/A350237) and 173 in [A347473](https://oeis.org/A347473).

[Download the proof and witness matrix (PDF).](z18-exact.pdf)

## Reduction at 151

Suppose there is a matrix of weight 151. A heavier matrix could be reduced to that weight by erasing ones. Deleting any row or any column leaves at most 143 ones, so **every row and every column has degree at least eight**. If two columns shared six rows, those rows would contain at least 48 ones. The two columns supply twelve and each of the other sixteen supplies at most two, giving at most 44. Thus two columns meet in at most five rows. Transposition gives the same bound for two rows.

Choose a row or column of maximum degree and transpose to make it a column. Mark $t$ of its entries. Each of the seventeen other columns induces a block of size at most five on these points. Two blocks meet in at most two points, since three common points with the marked column would be forbidden. Each point lies in at least seven blocks. Let $S$ be the sum of the block sizes.

- **Maximum degree at least eleven.** Choose any eleven entries in the column. Then $S\ge77$. There must be at least nine five-blocks, since seventeen blocks of size at most four with eight bonuses contribute at most 76. The verifier enumerates the compatible families of fives, then the compatible fours and smaller blocks. No family has the required loads and weight. This also covers columns of degree twelve or more.
- **Maximum degree ten.** Mark all ten entries. Now $S\ge70$, and every point load is between seven and nine. There are **978** distinct block multisets meeting these conditions up to relabelling. None admits the eight additional rows of degrees eight through ten needed to reach 151.
- **Maximum degree nine.** Each side has seven lines of degree nine and eleven of degree eight. Look at the seven high-degree columns on the eleven low-degree rows. This $11\times7$ rectangle has at most 48 ones. Indeed, at weight 49 its eleven row sizes would cover at least $6\binom43+5\binom53=74$ column triples, while each of the $\binom73$ triples can be covered at most twice. The lower count follows by balancing the eleven row sizes. Thus at least $63-48=15$ entries of the seven high-degree columns meet high-degree rows. Some nine-column meets at least three such rows. Mark that particular column. Its nine point loads are seven or eight, with total at least $9\cdot7+3=66$. There are **1,821** distinct projections meeting the conditions. None admits nine further rows of degrees eight or nine and final weight 151.

Maximum degree at most eight could supply only 144 ones. This exhausts weight 151 and proves the upper bound.

## Enumeration and replay

The [ten-point generator](ten_points.cpp) starts from every compatible family of at least two fives. Given $m$ fives and $q$ fours, $S\le51+2m+q$, so $q\ge19-2m$. Distinguish a point of maximum frequency $p$ in the fours. The generator tries all point choices and grows the $p$ fours through that point, with $p\le9$ from the load bound. It removes duplicate families by canonical labelling of the incidence graph, using an extra singleton block to distinguish the point. It then tries the remaining fours avoiding the point with $4q\le10p$, and all compatible smaller blocks. Triples can occur once, pairs and smaller blocks can repeat. The generator checks all ten point loads and the total weight before recording the canonical projection.

The [nine-point generator](../z16x17-k33/catalogue.cpp) and [eleven-point enumeration](../z17x18-k33/verify.py) are shared with the earlier rectangular proofs. The [completion checker](../z16x18-k33/borders.cpp) tries distinct legal row supports on the seventeen unmarked columns for the remaining rows. Repeated rows of degree at least eight are already impossible by the row-pair bound. At each addition it rejects a support when some triple of fixed rows would have three common columns. For a positive control, the replay also runs the ten-column completion search at weight 150 and verifies the square it reconstructs.

From this directory, with Python 3.10+, a C++20 compiler named `c++`, and the nauty headers and library installed, run

```sh
python3 verify_exact.py
```

If nauty is not on the compiler's default search paths, pass its include and library paths through `CXXFLAGS` and `LDFLAGS` as described in the [top-level README](../README.md).
