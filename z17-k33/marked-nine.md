---
title: "The maximum number of ones in a 17 by 17 matrix avoiding an all-one 3 by 3 is 138"
date: "26 November 2026"
---

**Theorem.** In the maximum-ones convention, $z(17,17;3,3)=138$. Two explicit matrices establish the lower bound. A computer-assisted exhaustion excludes exactly 139 ones. Deleting individual ones preserves avoidance, so this excludes every larger weight as well. Row and column indices in the forbidden submatrix may be chosen arbitrarily.

The two witnesses have different line degrees. One has a ten on each side. The second has maximum degree nine and contains a six on each side. They are inequivalent even allowing transposition. Each matrix has been checked on all $\binom{17}{3}^2=462{,}400$ choices of rows and columns. The witness files are `witness-138.txt` and `witness-138-six.txt`. Padhi had already [reported the lower bound of 138](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6960039). The matrices used here were constructed locally.

## Degree bounds at weight 139

A line is a row or a column. The external inputs are the upper bounds 133, 126, 118 and 110 for 16, 15, 14 and 13 rows on seventeen columns, and the value 128 and uniqueness of its extremal graph on 16 by 16. These are given in [Collins, Riasanovsky, Wallace and Radziszowski, Table 4](https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf).

| External input | Status in Table 4 | Used for |
|---|---|---|
| $z(16,17;3,3)\le133$ | Exhaustive computation | Minimum degree six; core weight 133 |
| $z(15,17;3,3)\le126$ | Bound from the paper's lemmas | No two sixes on a shore; core row degrees |
| $z(14,17;3,3)\le118$ | Bound from the paper's lemmas | No six with two sevens; core row degrees |
| $z(13,17;3,3)\le110$ | Exhaustive computation | No four sevens on a shore |
| $z(16,16;3,3)=128$, unique extremal graph | Exact, marked unique | Core columns have degree at least six |

We did not rerun the computations behind these entries. The 128-one representative used here is checked to be $K_{3,3}$-free with 128 ones.

Deleting the lowest-degree lines implies that the minimum is at least six. On one shore there cannot be two sixes, a six with two sevens, or four sevens, since the matrices left by their deletion exceed the corresponding bounds. The total deficit below eight on either shore is therefore at most three. No two rows can share six columns. Those columns contain at least $48-3=45$ ones, whereas the two rows and the remaining fifteen can supply at most $12+30=42$. Transpose for the analogous bound on column pairs.

Here is the finite reduction that excludes degree ten or greater. Mark ten entries of a putative large row. Each of the other sixteen rows restricts to a set of size at most five on the ten points, and any two restrictions intersect in at most two. Write $m,q$ for the numbers of five-sets and four-sets. The total projected weight is at least $70-3=67$ and at most $48+2m+q$. The sign vectors of five-sets (positive on the set, negative elsewhere) have norm squared ten and mutual inner product at most $-2$. The squared norm of their sum gives $m\le6$.

The enumerator `ten_columns.py` excludes $m=5,6$ by exhausting the five-set families and testing for a clique of $67-48-2m$ four-sets meeting all intersection bounds. It chooses successive five-sets up to permutations of points with identical incidence in the previously selected sets. Thus the projected weight is at most 68. Any choice of ten points must contain at least two units of deficit. A marked row with at least eleven entries must consequently contain three degree-seven columns, since omitting a column of degree six would leave at most one unit of deficit. At twelve entries it could omit two sevens, so its degree could only be eleven. Omit one seven. The projection now has exactly 68 ones, four five-sets and twelve four-sets, and its point loads are two sixes and eight sevens. Exhaustion gives 120 generated cases. Restoring the omitted seven requires six of the sixteen projected rows meeting pairwise in at most one old point. Exhaustion gives a maximum of three in every case. Hence degree ten is an upper bound on both shores.

At degree exactly ten, the only possible size lists are three fives and thirteen fours, four fives and twelve fours, or four fives, eleven fours and a triple. Generate all these configurations subject to the point-degree and deficit bounds. This gives 37,048 cases and 519 distinct relabelling keys. Test all seven outside columns in nonincreasing order of weight for every key, enforcing the triple bound and the required total sum. No key extends. Two repeated columns of degree $d$ would imply $6d\le2d+30$ and hence $d\le7$. At least two deficit units are already on the marked ten columns, allowing at most one outside column below eight. Thus sampling outside columns without replacement covers every case. The programs for this step are `ten_cores_139.py` and `ten_border.cpp`. We have proved that every line in a 139-one example would have degree at most nine.

## Reduction to a marked line

If any line has degree six, transpose if necessary and delete a six-row. Otherwise, if a seven exists on either shore, orient and delete a seven-row. The case with all degrees at least eight is handled directly below. Call the resulting 16 by 17 matrix the core. The bounds on 15 by 17 and 14 by 17 give the following possible degrees for the sixteen core rows. For the seven-row branch, also use the previously proved upper bound of three sevens in the original matrix.

| Deleted row | Core weight | Core rows | Core columns |
|---|---:|---|---|
| Six | 133 | 7 to 9, at most one seven | 6 to 9 |
| Seven, after excluding six on either shore | 132 | 7 to 9, at most two sevens | 6 to 9 |

For a 133-one core, deleting a column leaves at most 128 ones, so its minimum column degree is at least five. At degree five the remaining square would be the unique 128-one 16 by 16 matrix. The leading square of `bordered-137.txt` represents it. The program `ten_columns.py` checks that all 4,368 ways to append a five-set fail in both orientations. Hence every core column has degree at least six. For the second, deleting one entry per column from degrees at least seven gives the stated minimum. A core contains a nine-row because its weight exceeds 16 times eight.

If the core has a nine-column, mark one and let its nine incident rows be the points. Each of the other sixteen columns determines a block on these nine points. If the core has no nine-column, mark a nine-row instead. Its nine incident columns are the points and the other fifteen rows are the blocks. Two distinct blocks share at most two points because the marked line supplies a third incidence. Every block has size at most five by the pair-intersection bound in the original square.

A point of core degree d occurs in exactly $d-1$ blocks. In the column-marked case the loads are 6 through 8, with at most one unit of deficit below seven for a 133-one core and at most two for a 132-one core. With a marked row and no nine-column the loads are 5 through 7. Across all seventeen core columns the deficit below eight is exactly 136 minus the core weight, so on the nine marked points the load deficit below seven is at most three or four. Thus the four minimum total block weights are 62, 61, 60 and 59 respectively (column-marked 133 and 132, then row-marked 133 and 132).

If both shores have minimum eight in the original square, mark a nine-column directly in the square. Such a column exists because $139>17\cdot8$. The sixteen blocks have point loads seven or eight. Complete the eight remaining rows at target 139, with row weights eight or nine. This uses the same enumeration and dispenses with a separate classification of this case.

## Exhaustion of the nine-point block systems

There are at most three five-blocks. Four would use twenty incidences across nine points, forcing at least thirteen pairwise intersections counted with multiplicity by convexity, while six block pairs allow at most twelve. Generate the five-blocks with one distinguished point. Let that point be one that occurs in as many four-blocks as possible. If there are q four-blocks, p of which contain that point, then $4q \le 9p$. Removing the point from these p blocks leaves triples on eight points meeting pairwise in at most one point. Each of the eight points occurs in at most three triples, so $p \le 8$.

First enumerate the four-blocks through the distinguished point, then the four-blocks off it, then the blocks of size at most three. Repetitions of blocks of size zero, one and two are allowed. At each stage retain all choices consistent with the intersection bound, load bounds and attainable total weight. A block system with m five-blocks and q four-blocks on b blocks has weight at most 3b + 2m + q. This gives the pruning test before p is fixed. At intermediate stages, add the remaining number of blocks times their largest allowed size to bound the final weight. The symmetry key is the actual relabelled multiset of blocks. Equal keys exhibit an isomorphism. Through-point generation preserves the distinguished point and the distinction is dropped once the four-blocks are complete.

## Restoring the other lines

The nine marked points now give nine fully specified lines, each incident with the marked line. The remaining seven rows (column-marked case) or eight columns (row-marked case) avoid it. Generate all masks of the permitted weights on the remaining sixteen or fifteen positions. A candidate mask must avoid every triple of positions already present in two fixed lines. Recursing in increasing position order, when a second bit of a forbidden triple is selected, remove its possible third bits. Thus every compatible mask occurs.

Choose the required number of additional lines in nonincreasing order of weight. A candidate must have triple intersection of size at most two with any two lines selected so far. If the heaviest available choices cannot achieve the target sum, prune. Extra lines may be taken distinct because any coincident pair of weight at least six would already share six entries in the original 139-one square. Check the core degrees and then try every possible support of the deleted row on any complete core. These degree restrictions apply to cores obtained from the hypothesised square. They do not classify unrestricted 16 by 17 matrices of these weights.

## Enumeration results

| Deleted row | Marked line | Distinct projections | Projections admitting the remaining line weights and triple bounds |
|---|---|---:|---:|
| Six | Column | 4,201 | 0 |
| Six | Row | 29 | 0 |
| Seven | Column | 671,685 | 2 |
| Seven | Row | 9,396 | 0 |
| None, minimum eight | Column | 12 | 0 |

The two surviving projections have two and one labelled completions to a 132-one core, respectively, in the retained ordering. The script `check_final_cores.py` enumerates their completions anew and checks every one of the 131,072 masks for a possible seventeenth row. In all three cases the largest appendable row has weight **six**. A seven was needed. This exhausts the alternatives for 139 and proves the theorem.

The separate checker `audit_core_catalogue.cpp` builds bitsets over all candidate masks at each weight. For each pair of fixed lines it removes every mask intersecting that pair in three or more entries. It first asks whether enough maximum-weight lines can even coexist. For the six-row branch this alone excludes all 4,230 projections. For the seven-row branch it also tests mixtures of line weights when needed. Its input is the catalogue produced by the common projection generator. The audit checks completion independently of the main completion routine. Both routines rely on the same generator, so completeness of the catalogue rests on that generator and on the coverage argument above. A separately implemented generator would be the most useful further check.

## A consequence for bipartite Ramsey numbers

The bipartite Ramsey number $b(2,2,3)$ is the least $b$ such that every colouring of the edges of $K_{b,b}$ with three colours contains a $K_{2,2}$ in the first or second colour or a $K_{3,3}$ in the third. Collins, Riasanovsky, Wallace and Radziszowski proved $17\le b(2,2,3)\le18$ and conjectured $b(2,2,3)=17$. They noted that $z(17;3)\le140$ would suffice. [Rowshan and Gholami](https://arxiv.org/abs/2108.03572) later proved the conjecture by a different argument, [published in *Mathematics*](https://doi.org/10.3390/math10050701). The theorem gives a short alternative proof. With $z(17,17;2,2)=74$ from the same paper, the three colour classes of such a colouring of $K_{17,17}$ would have at most $74+74+138=286<289$ edges.

## Witnesses

Each column of text below is one entire 17 by 17 matrix. The first was found by completing a ten-point projection at weight 138. The second comes from one of the final 132-one cores.

```text
11111111110000000    11001001001101001
11111000000011011    11000110010011001
11000111000101101    10101010100000101
10100100110110110    10110000010100101
10010010101000111    10010101101010001
10010001011011000    01101100011000011
10001010011101000    01100011000110011
10001001101110000    00011111000001111
01100010101011100    00000000111111111
01100001011100011    01110011111001000
01010100101101010    01111100100111000
01001100011010101    11010110001100110
00110110001110001    11001001110010110
00101101001001110    00001111011110000
00011011000110110    10100101010101010
00011000110101101    10101010001011010
00000011110011011    00011010110100000
```

## Replay

The shortest complete replay is `python3 verify_exact.py` from the [`z17-k33` directory of the repository](https://github.com/jasondavies/zarankiewicz-numbers/tree/main/z17-k33). It requires Python 3.10 or newer, a C++20 compiler, and the nauty development library. It verifies both explicit witnesses, reruns the ten-point check, generates each entire nine-point catalogue, and audits the final survivors. Temporary catalogues are removed after the run.

Recorded complete replays:

| Run | Source | Python | Compiler | nauty | Time |
|---|---|---|---|---|---:|
| External review | commit `eb51b4f` (originally `4bd72e9`) | 3.12.14 | G++ 14.2.0 | 2.9.3 | 8 min 37 s |
| Ubuntu 24.04 | this version | 3.12.3 | G++ 13.3.0 | 2.8.8 | 7 min 27 s |


For a separate replay using the primary completion routine, run the following commands in this directory.

```sh
g++ -O3 -std=c++20 six_row_core.cpp -lnauty -o /tmp/six-row-core
g++ -O3 -std=c++20 ten_border.cpp -lnauty -o /tmp/ten-border
python3 ten_columns.py
python3 ten_cores_139.py | /tmp/ten-border
/tmp/six-row-core column regular139 0 3
for border in 6 7; do
  for mark in column row; do
    /tmp/six-row-core "$mark" "$border" 0 3
  done
done
python3 check_final_cores.py
```

Use a shell with `set -o pipefail` for the pipeline. The final two numeric arguments to `six_row_core` are the inclusive range of five-block counts. Disjoint ranges may be run independently. To replay the independent completion audit, pass a fifth argument giving the catalogue output path and optionally a sixth, `--catalogue-only`, to skip the primary completion calculation. For example,

```sh
g++ -O3 -std=c++20 audit_core_catalogue.cpp -o /tmp/audit-nine
/tmp/six-row-core column 7 0 3 /tmp/seven.txt --catalogue-only
/tmp/audit-nine column 7 --show < /tmp/seven.txt
```

Two positive controls with an eight-entry border reconstruct valid 137-one matrices from scratch in the two orientations.

```sh
/tmp/six-row-core column control137 0 0
/tmp/six-row-core row control137 0 0
```

The last line of output from `six_row_core` gives its outcome. `RESULT EXHAUSTED` with exit status 0 means the search finished without finding a matrix. `RESULT FOUND n` with exit status 1 means it printed n matrices, as the positive controls do. `RESULT CATALOGUE` with exit status 0 means completion was disabled and only the catalogue was written.
