# The 17 × 18 Zarankiewicz number for K₃,₃ is 143

A 17 × 18 binary matrix can have **143 ones** while avoiding an all-ones 3 × 3 submatrix. Every 17 × 18 matrix with 144 or more ones contains such a submatrix. Rows and columns may be chosen anywhere in the matrix.

**Construction.** Append a column supported on rows **3, 5, 6, 15, 17** (numbered from one) of the 138-one square with a six-one row. The resulting matrix has 143 ones. The verifier checks that none of its 680 triples of rows has more than two common columns. [143-one witness](witness-143.txt) · [Original square](../z17-k33/witness-138-six.txt)

**Upper bound.** It suffices to exclude weight 144, because erasing ones preserves avoidance. Deleting a row or column and applying the known neighbouring bounds forces every row to have at least seven ones and every column to have at least six. The first part of the proof shows that a counterexample would have a column of degree nine, no larger column, and no two columns sharing more than five rows. Marking the nine-column splits the rows into nine meeting it and eight avoiding it. Enumerating the denser side of this split gives four cases and 23,029,030 projections in total. None can be completed to 144 ones. [Degree reductions](weight-144.md) · [Final enumeration and counts](final-search.md)

The starting ceiling of 145 follows from Jiuzeng Wei’s exact 16 × 18 value of 137. We also checked weight 145 directly. That calculation can be replayed separately and supplies the twelve-point block lemma used in the 144 proof. [Wei’s archive](https://doi.org/10.5281/zenodo.24553293) · [Independent 16 × 18 proof](../z16x18-k33/README.md) · [145-one calculation](weight-145.md)

As a consequence, $z(18,18;3,3)\le151$. An 18 × 18 matrix of weight 152 has a row of weight at most eight. Deleting it would leave at least 144 ones in 17 × 18. The [18 × 18 proof](../z18-k33/README.md) sharpens this to the exact value 150.

In the OEIS this gives a(17) = 144 in [A006621](https://oeis.org/A006621), Zarankiewicz's problem k_3(n,n+1).

[Download the proof with its witness matrix (PDF).](z17x18-exact.pdf)

## Replay

Use Python 3.10+, a C++20 compiler named `c++`, and the nauty development library and headers. From this directory run

```sh
python3 verify_exact.py --jobs 4
```

If nauty is not on the compiler's default search paths, pass its include and library paths through `CXXFLAGS` and `LDFLAGS` as described in the [top-level README](../README.md).

This checks the witness, regenerates the degree exclusions and final catalogues, and checks every completion. The search uses the smaller-grid bounds cited in the proof, including the [17 × 17 maximum of 138](../z17-k33/README.md). The checker also reconstructs a valid 143-one matrix from each side of the supplied witness as a positive control. The job count controls parallel border checks. The largest catalogue contains over twelve million projections and requires several gigabytes of memory during generation.
