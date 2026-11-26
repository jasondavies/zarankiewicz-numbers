# Zarankiewicz numbers

This repository collects exact values of Zarankiewicz numbers. Each value comes with explicit extremal matrices and a proof that can be replayed by computer.

The Zarankiewicz number $z(m,n;s,t)$ is the largest number of ones in an $m \times n$ binary matrix that contains no all-ones $s \times t$ submatrix. The rows and columns of the submatrix may be any $s$ rows and any $t$ columns, not necessarily adjacent. Equivalently, it is the largest number of edges in a bipartite graph with parts of sizes $m$ and $n$ that has no $K_{s,t}$ subgraph. This repository uses this maximum-ones convention throughout.

## Results

| Value | Directory | Contents |
|---|---|---|
| $z(17,17;3,3) = 138$ | [`z17-k33`](z17-k33) | Two inequivalent witnesses, a written proof, and a computer-assisted exhaustion ruling out 139 |
| $z(16,17;3,3) = 132$ | [`z16x17-k33`](z16x17-k33) | A witness and a computer-assisted exhaustion ruling out 133, reusing the ten-point routines from `z17-k33` |

[![The two 17 × 17 witnesses with 138 ones](z17-k33/witnesses.svg)](z17-k33)

## OEIS

These results give new terms of the following sequences. Some sequences count the least number of ones that forces an all-ones submatrix, which is one more than the Zarankiewicz number, and some count the complementary problem for zero submatrices.

| Sequence | Name | New term | From |
|---|---|---|---|
| [A350304](https://oeis.org/A350304) | Maximum number of 1's in an n X n binary matrix without an all-ones 3 X 3 submatrix | a(17) = 138 | `z17-k33` |
| [A001198](https://oeis.org/A001198) | Zarankiewicz's problem k_3(n) | a(17) = 139 | `z17-k33` |
| [A350237](https://oeis.org/A350237) | Minimum number of 1's in an n X n binary matrix with no zero 3 X 3 submatrix | a(17) = 289 − 138 = 151 | `z17-k33` |
| [A347473](https://oeis.org/A347473) | Maximum number of nonzero entries allowed in an n X n matrix to ensure there is a 3 X 3 zero submatrix | a(17) = 151 − 1 = 150 | `z17-k33` |
| [A006621](https://oeis.org/A006621) | Zarankiewicz's problem k_3(n,n+1) | a(16) = 133 | `z16x17-k33` |

The listed terms of A006621 stop at a(12), so a(13) to a(15) are needed before a(16) can be added.

## Layout

Each result has its own directory with a README describing the files and how to replay the verification. A directory typically contains:

- the witness matrices as plain text, one row per line;
- a written proof as a typeset PDF, with its Markdown source where there is one;
- the verification sources and a `verify_exact.py` script that replays the whole check.

`z17-k33` also has a zip bundle of the whole directory.

The replays need Python 3.10 or newer, a C++20 compiler available as `c++`, and the nauty headers and library. If nauty is not on the compiler's default search paths, as with Homebrew on Apple Silicon, pass them through `CXXFLAGS` and `LDFLAGS`:

```sh
CXXFLAGS=-I/opt/homebrew/include LDFLAGS=-L/opt/homebrew/lib python3 verify_exact.py
```

## License

The repository is licensed under [Apache-2.0](LICENSE). Cited papers are linked rather than redistributed.
