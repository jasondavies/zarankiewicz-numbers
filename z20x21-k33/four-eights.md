# Excluding the column profile (4, 15, 2) at weight 187

A 20 × 21 matrix avoiding an all-ones 3 × 3 submatrix cannot have four columns of weight eight, fifteen of weight nine and two of weight ten. The profiles at 187 still open are $(5,13,3)$, $(6,11,4)$ and $(7,9,5)$.

## The five-row obstruction

Delete the four eight-columns. The two-column enumeration below reconstructs a single possible 155-one heavy matrix up to relabelling, under the previously proved necessary conditions. Its five rows of heavy degree seven all lie in **both ten-columns**. In the saved matrix these are rows 1, 2, 9, 11 and 12 and columns 15 and 16, counting from one. Each of these rows needs at least two entries in the four deleted columns. A full row has degree at least eight, and a full eight-row must avoid all eight-columns. A single new column meeting three of the five rows would already form a forbidden submatrix with the two tens. The four columns can therefore supply at most eight of the ten required entries. [Heavy matrix](heavy-155.txt) · [Earlier degree reductions](core-search.md)

An independent direct check of the same matrix finds zero legal eight-one supports among all $\binom{20}{8}=125{,}970$ possibilities. It finds five legal seven-one supports.

## Why two marked columns suffice

Write $d_i$ for the heavy degree of row $i$ and $D(C)=\sum_{i\in C}(8-d_i)$. The possible row profiles are five sevens and fifteen eights, or one six, three sevens and sixteen eights. Each ten-column has $D\ge4$, each nine-column has $D\ge1$, and at least three nine-columns have $D=1$. Any two distinct columns of this last kind can be marked. Each contains one seven-row and eight eight-rows. On its nine rows we know the complete incidence pattern of the other sixteen columns up to labelling. There are 4,018 such projections in the earlier catalogue. Every block in them has size two through five, so the marked columns overlap in two through five rows. [Projection census](core-search.md)

Fix possible projections at both marks, including the block each mark induces in the other projection. On their common rows the two descriptions must agree. For each ordering of the common rows record the location of their degree-seven row, if present, and the sorted multiset of traces of the fifteen other columns. Take a least such record. We fix a minimizing order on the left and keep every distinct minimizing column ordering on the right. Any genuine identification takes one minimizing ordering to another. Repeated catalogue entries as the two marks are allowed. Ordering their catalogue indices removes exchanges between different entries.

Within each equal-trace group the column bijection is still unknown. For each right-only row, try every target subset of the required size in each group. Split the group by membership in the row before proceeding to the next row. This represents every possible column bijection by its action on the rows. Reject a new row when it shares a triple of columns with two fixed left rows. Reject a pair of new rows when they share a triple with one fixed left row. All triples of rows contained in either input projection have already been checked. [Join implementation](join_nines.cpp)

## Completing a joined pair

If the overlap is $s$, the union fixes $18-s$ complete rows, leaving $s+2$ rows supported on fifteen columns. Try both possible heavy row profiles. A new support must meet each intersection of two fixed rows in at most two positions. Choose the supports in descending order of weight and recheck this condition as rows are added. Equal weights use increasing support index. Two missing rows cannot coincide, since any six shared heavy columns would need at least 54 entries while the two covering rows and eighteen others supply at most 48.

A column with $h$ known entries and $n$ unfilled rows must satisfy $h\le10$ and $h+n\ge9$. If $h+n=9$ the next row must contain it, and if $h=10$ the next row must omit it. To bound the largest possible final deficit of a ten-column, assign its remaining entries to the largest deficits left. At least two columns must still be capable of reaching degree ten and deficit four. At a leaf we check all seventeen column degrees and the necessary deficits. These conditions also imply the existence of the required third nine-column of deficit one. [Completion implementation](heavy_completion.hpp)

| Shared rows | Matching ordered descriptions tested | Valid joined projections | Completions to 155 |
|---:|---:|---:|---:|
| 2 | 1,327 | 0 | 0 |
| 3 | 31,956,572 | 1,747 | 8 |
| 4 | 529,580,879 | 2,504,059 | 8 |
| 5 | 145,995 | 48,441 | 0 |

The counts include repetitions through different markings and compatible relabellings. All sixteen completions agree after sorting their rows in the labels returned by this replay. The checker also verifies the five-row obstruction on every emitted matrix individually.

## Replay

The replay regenerates the catalogue with two different block enumerators and compares the sets of canonical projections. It checks the marked-pair search on independently relabelled projections cut from the 193-one square, and recovers the complete 155-one matrix from just two of its projections. It also checks every row triple of each output and tests the single-column extensions directly. Run from this directory with Python, C++20 and nauty. Pass `--overlap 3` to run one overlap. [Replay driver](verify_four_eights.py)

```sh
python3 verify_four_eights.py --jobs 8
```
