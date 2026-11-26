# The 17 × 17 Zarankiewicz number for K₃,₃

A 17 × 17 binary matrix can contain at most **138 ones** while avoiding an all-ones 3 × 3 submatrix. Any three rows and any three columns may be chosen.

The [proof](marked-nine.md) gives the counting argument and the exhaustive cases. The [first witness](witness-138.txt) and [second witness](witness-138-six.txt) attain the bound and have different row-degree profiles. The [PDF](z17-exact.pdf) prints both matrices, and the [proof bundle](z17-proof.zip) includes the verification sources.

## Replay

From this directory, run the following with Python 3.10 or newer, a C++20 compiler available as `c++`, and the nauty development headers and library installed.

```sh
python3 verify_exact.py
```

The verifier checks both witnesses, rebuilds the finite catalogues, and checks the upper bound. Its final line ends with `Exact value 138.`
