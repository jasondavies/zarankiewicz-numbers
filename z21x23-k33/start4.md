# Exclusion of four-column start 4

No 209-one, all-ones-$3\times3$-free matrix on $21\times23$ can contain start 4. Here 4 is the zero-based index among the 143 starts with two rows common to all four marked eight-one columns. The sixteen row multiplicities, in binary mask order, are $(1,5,4,0,3,0,0,0,0,1,2,0,3,0,0,2)$. Together with the 20 earlier counting exclusions, this left 122 of 143 starts in this group and 5,663 across the full cover. A later reduction omits 74 redundant starts, leaving 48 in this group and 5,589 overall. [Row-deficit proof and shared-tail replay](row-deficit.md) The other two groups still contain 4,167 and 1,374 starts. The numerical bounds remain $207\le z(21,23;3,3)\le209$. [Initial cover](README.md) · [Counting exclusions and five-row reduction](two-common-rows.md)

## Where the proof splits

The common rows have marked mask 15. Three more rows have mask 12 and lie on both columns of that marked pair. The previous enumeration gives 892 possible five-row templates and reduces them to 92 by testing the two groups of three rows on the individual marks. The replay regenerates these 92 IDs and checks that the manifest accounts for each exactly once in the following three ways.

| Method | Five-row templates |
| --- | ---: |
| The grouped encoding contains an explicit empty clause | 20 |
| An archived DRAT certificate verifies against the regenerated whole-template CNF | 67 |
| Exhaustive row placement in C++ | 5 |
| **Total** | **92** |

The five templates in the row search are 120, 145, 150, 151 and 152. Template 145 **also** has a second proof using all ten sixth-row CNFs. The verifier tries all $2^{19}$ labelled core patterns for a row of marked mask 4. Exactly 2,592 meet the five fixed rows and have at least eight ones. Counting entries in each equal-column group gives the same ten representatives as the split generator. CaDiCaL 3.1.0 returned UNSAT on the three previously unresolved placements, 6, 7 and 8, in 17.75, 12.64 and 14.43 seconds of wall time respectively on a Ryzen 7 9700X. All ten trimmed proofs were rechecked with drat-trim and independently via conversion to LRAT and lrat-check. The manifest records SHA-256 hashes of the regenerated inputs and retained proof bytes. [Manifest](start4-proofs/manifest.tsv)

## The row search

In start 4 the remaining sixteen rows have known marked masks. Three have mask 4, three on the opposite mark have masks 9, 10 and 10, and the last ten have masks 0 (one row), 1 (five rows) and 2 (four rows). Every row outside the two common rows has at least eight core entries. Selecting all three rows on each side jointly makes the late branches small enough to exhaust directly.

For each mask, the search enumerates the $2^{19}$ possible core bit patterns. It retains all that have at least eight ones and share at most two full columns with each pair of fixed rows. When adding a new row it filters future candidates against every new triple. Two rows can share at most six columns, since seven shared columns need at least 56 ones and would have capacity at most $14+19\cdot2=52$. The search can therefore discard any pair with more than six common ones.

The first six new rows are placed in mask order $10,10,9,4,4,4$. Within a group of equal marked masks the rows are interchangeable. Core columns that agree on all rows already fixed are interchangeable too. We may impose descending lexicographic order on each set of interchangeable rows and columns. A lexicographically greatest row-major matrix among the permitted permutations has both properties. The code checks column order on adjacent columns with equal fixed prefixes and row order on adjacent rows of the same mask.

For the last ten rows the search maintains one candidate list per mask. Each list stays in decreasing weight order. The sum of the largest required weights from each list bounds the weight attainable below the current node. Every core column needs at least eight entries. If its deficit equals the number of rows still missing, every subsequent row must contain it. Each choice is checked against the fixed rows before recursion. These tests cover every possible completion.

| Template | Placements of the first side visited | Placements of both sides visited | Completions reaching 209 |
| ---: | ---: | ---: | ---: |
| 120 | 6 | 6 | 0 |
| 145 | 10 | 26 | 0 |
| 150 | 56 | 2,020 | 0 |
| 151 | 12 | 540 | 0 |
| 152 | 88 | 6,680 | 0 |

## Replay

Run from this directory with C++20, Python 3.10+, python-sat (1.9.dev15 was used), and drat-trim. The replay rebuilds the row search in a temporary directory, regenerates the formulas, checks their hashes and verifies every archived proof. The proof archives named in the manifest are not stored in this repository, which keeps only their hashes; place them in `start4-proofs/` before replaying. The values on 22 × 23 and 23 × 23 do not depend on this search. Use the actual paths to your checker binaries. The optional LRAT check converts the selected DRAT proofs before checking them with a second program.

```sh
python3 verify_start4.py --checker /path/to/drat-trim
python3 verify_start4.py --template 145 --checker /path/to/drat-trim --lrat-check /path/to/lrat-check
```

The certificates cover the encoded subproblems. The reduction from matrices to these formulas uses the smaller extremal bounds and degree arguments in the preceding proof. [SAT encoding](overlap_sat.py) · [C++ search](start4_search.cpp) · [Replay](verify_start4.py)

## Reusing the placements

After permuting the four marked columns, starts 25, 46 and 62 have the same five fixed marked row masks and the same six side masks as start 4. They differ in the last ten rows. In mask order $0,1,2,3$ the tail multiplicities are $(1,5,4,0)$ for start 4, $(2,4,3,1)$ for start 25, $(3,3,2,2)$ for start 46 and $(4,2,1,3)$ for start 62. The initial side-placement enumeration can serve all four. The numerical completion result above uses the start-4 tail.
