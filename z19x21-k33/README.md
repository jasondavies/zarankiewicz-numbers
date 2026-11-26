# The 19 × 21 Zarankiewicz number for K₃,₃ is 177

**The exact maximum is 177.** Deleting the two eight-one rows of the 193-one square attains it. The exhaustive search below excludes 178. Deleting entries preserves avoidance, so every greater weight is also excluded. [177-one witness](witness-177.txt) · [193-one square](../z21-k33/witness-193.txt)

The same exclusion gives **185 on 20 × 21** and **193 on 21 × 21**. A hypothetical 186-one rectangle or 194-one square would contain a 178-one 19 × 21 matrix after deleting one or two parallel eight-lines. The existing witnesses attain both lower endpoints. [Eight-line reductions](../z20x21-k33/weight-186.md) · [185-one witness](../z20x21-k33/witness-185.txt)

## Remove the seven-columns

Suppose a 19 × 21 matrix of weight 178 avoids an all-ones 3 × 3. Each column has at least seven entries, by the [19 × 20 maximum of 171](../z19x20-k33/README.md). The number $s$ of seven-columns is at most two, since deleting three would leave 157 entries on 19 × 18, whose [maximum is 156](../z18x19-k33/README.md). Remove precisely those $s$ columns. The resulting core has $m=21-s$ columns, $T=178-7s$ entries and all column degrees at least eight. Deleting a core row leaves at most 170, 163 or 156 entries on 18 × 21, 18 × 20 or 18 × 19 respectively. Subtracting from $T$ gives minimum core row degree eight in each case. [The 18-row bounds](../z20x21-k33/core-search.md)

Write $e_j=c_j-8$ for the excess of column $j$. Set $E=\sum_j e_j=10+s$, $Q=\sum_j e_j^2$, and let $W_i$ be the sum of the column excesses incident to row $i$. Then
$$
\sum_i W_i=8E+Q,\qquad Q-E=\sum_j e_j(e_j-1)\ge0.
$$

Mark a core row of degree $d$. Use its columns as points and the other eighteen rows as blocks on those points. Two blocks intersect in at most two points. Every block has size at most five because six core columns need at least 48 entries, whereas two covering rows and seventeen others can supply at most $12+17\cdot2=46$. The point loads are at least seven, and their total is $7d+W_i$. Thus $7d\le90$ and $d\le12$.

For $d\ge11$ one has $W_i\le2$. Otherwise eleven of the marked columns retain at least three units of excess, giving a projection of load at least 80 on eleven points, which the catalogue excludes. Moreover a twelve-row has $W_i=0$. If $W_i>0$, remove a zero-excess point, leaving an eleven-point projection of load at least 78. Among its eighteen blocks, restoring the point needs seven blocks of size at most four, pairwise intersecting in at most one point. **None of the 4,048 canonical projections admits seven such blocks.** The replay generates the projections by fixing the five-blocks first, then checks the admissible block subsets directly. At total load 79 or higher there are 32 projections.

## Two choices of marked row

For $\alpha=1,2$ mark a row maximizing $P_i=\alpha d_i+W_i$. Its score bounds every other row's score during completion. For a mark of degree $d$ and score $P$, the required projection load is $7d+P-\alpha d$.

For $\alpha=1$ the score sum is $268+2s+(Q-E)>19\cdot14$. An eleven- or twelve-row cannot reach 15. The search tests all maximizing nine- and ten-rows at score at least 15, using respectively 67,537 projections of load at least 69 and 24 projections of load at least 75. If these searches fail, every maximizing row has degree eight. Consequently some eight-row has $W\ge7$. If any nine-row has $W\ge6$, some eight-row has $W\ge8$ because a nine-row cannot even tie for the maximum. This last conclusion is used to prune the second search.

For $\alpha=2$ the sum of the scores is $446-5s+(Q-E)$. Thus the peak is at least 24, except possibly when $s=2$ and $Q=E$, since every positive value of $Q-E$ is at least two. At peak 24 or higher the possible marked degrees and loads are as follows.

| Marked degree | Minimum load | Projections |
|---:|---:|---:|
| 8 | 64 | 19,363 |
| 9 | 69 | 67,537 |
| 10 | 74 | 20,250 |
| 11 | 79 | 32 |

A twelve-row can only have score 24, with twelve degree-eight columns. Two such rows would require at least $12+12-5=19$ degree-eight columns. Even for $s=0$ this leaves at most two columns to carry the excess. Two columns could not carry $16+E\ge26$ entries on nineteen rows, since seven common rows would need at least 56 entries against a capacity of at most $14+19\cdot2=52$. If fewer than two columns have positive excess, include an eight-column in the pair. This proves there is at most one twelve-row. If only a twelve-row attains 24, the total score is at most $19\cdot23+1=438$. But its twelve zero-excess columns force $Q-E\ge2(E-(m-12))=2+4s$, giving a total of at least $448-s$. Therefore a mark in the table suffices.

**A smaller eight-point search when $s=0$.** At peak 24 one can use a nine-, ten- or eleven-row. Otherwise assume that only eight- and twelve-rows attain 24. Some eight-row must attain it by the preceding argument. Its deletion leaves 170 ones on 18 × 21, including at least two seven-columns, by the [170-one restriction](../z20x21-k33/weight-186.md). The row therefore meets at least two eight-columns. Its $W=8$ comes from at most six positive terms, forcing $Q-E\ge4$. The total slack below score 24 is at most $19\cdot24-446-4=6$. Hence at most six rows have degree nine, ten or eleven. With at most one twelve-row the total row excess over eight can be at most $6\cdot3+4=22$, below the required 26. This contradiction means an eight-row need only be tested at score 25 or higher when $s=0$. Its load is at least 65, leaving just **467** projections.

**The remaining low-score case when $s=2$.** If the peak is below 24 then $Q=E=12$, all columns have degree eight or nine, and the score sum is 436. Eighteen rows score 23 and one scores 22. At least seven rows have degree eight since the core weight is 164. At least one of these eight-rows therefore scores 23. Its eight point loads are one seven and seven eights. There are **10,057** such projections. The replay fixes $Q=12$ in this search.

## Completion and checks

For each marked projection the search reconstructs the marked columns, enumerates the degree profiles of the missing core columns and tries compatible supports on the eighteen unmarked rows. Equal-weight columns are chosen in order. Distinct supports suffice since two full columns cannot share seven rows. Each core row must obey the chosen peak score. At a complete core the checker enumerates all $s$ compatible seven-columns. Distinct core counts may include repetitions under different choices of mark.

For the second nine-row search the replay requires an eight-row with excess at least eight. For the second ten-row search it requires one of excess at least seven. At each recursion the largest remaining column weights bound the excess that can still be assigned to a row ending at degree eight. When all remaining column coefficients agree, an unspent row capacity has a known residue modulo that coefficient. The sum of these unavoidable residues is a lower bound on the total unused score. [Completion engine](../z18x19-k33/marked_core.cpp) · [Seven-column extensions](../z18x19-k33/seven_columns.hpp)

The positive controls start with the 177-one matrix, optionally thin one or two columns to seven, and reconstruct a solution from an actual maximizing row in both scoring systems. Every returned matrix is checked against every row triple and every column triple.

## Exhaustion

| Seven-columns | Marked cases checked over both scoring systems | Extensions to 178 |
|---:|---:|---:|
| 0 | 155,847 | 0 |
| 1 | 174,743 | 0 |
| 2 | 184,800 | 0 |
| **Total** | **515,390** | **0** |

The case counts include repeated projections tested under different marks or score restrictions. In the recorded run one complete core reached the one-column extension test, and nineteen reached the two-column test. A second checker generated all seven-subsets of the nineteen rows and independently confirmed that none of these cores admits the required extension. The number of intermediate cores can decrease with stronger pruning. [Independent support test](../z20x21-k33/extend_eights.py)

From this directory run the following command to replay all three cases. The optional cache keeps completed batches keyed by the compiled solver, parameters and full input. Use `--sevens 2`, `--sevens 1` or `--sevens 0` to replay one case.

```sh
python3 verify_weight_178.py --jobs 8 --cache /tmp/z178-replay
```

If nauty is not on the compiler's default search paths, pass its include and library paths through `CXXFLAGS` and `LDFLAGS` as described in the [top-level README](../README.md).
