# Excluding 226 ones on 23 × 23

The maximum number of ones in a 23 × 23 matrix avoiding an all-ones 3 × 3 submatrix is **225**. The [witness](witness-225.txt) gives the lower bound. Deleting each row of a square of weight $w$ gives $22w\le23\cdot217$ by the [rectangular upper bound](../z22x23-k33/218.md). It suffices to exclude 226.

## The marked eleven-row

Use the [local restrictions at 226](226.md), in both orientations. All degrees are at least nine. At least eight rows and eight columns have degree nine. Call a column high if its degree is at least ten, and give it weight $c-9$. A nine-row meets a nine-column and has total incident weight at most ten. A ten-row with at least five high entries has incident weight at most eight. Every longer row has at most five high entries, and if it has five their weight is at most eight. Two lines of the same orientation meet at most six times, or at most five if either has degree nine. The induced submatrix on nine-rows and nine-columns avoids an all-ones 2 × 2.

Consider a long row with **exactly five high entries of total weight at least six**. Mark those five columns and six of its nine-columns. The 22 other rows give blocks of total load at least 94. If these blocks all have size at most five, there are 844 eligible projections with exactly six points of load eight. None admits an extra column on the marked row and none accepts the missing columns at weight 226. The [projection replay](verify_226.py) checks all 844.

A block of size six must consist of precisely the six marked nine-columns. Six shared columns have capacity 54, so none can be high. Seven shared columns are impossible. If the marked row has a seventh nine-column, change one of the chosen six. A second row witnessing the new six must be different from the row witnessing the first six, but the two witnesses and the marked row would have at least five common columns. Thus a choice with no six-block would exist. Consequently the row in question has degree **exactly eleven** and shares precisely six nine-columns with a second high row. The two rows supply twelve entries on these columns, and each other row must supply exactly two of the remaining 42.

We now establish that such an eleven-row or the transposed eleven-column must occur and that the two orientations are incompatible.

## Counting incidences by degree

The positive excesses above nine partition nineteen on each side. For a profile pair let $a,b$ count nine-rows and nine-columns and let $x$ be the number of entries between them. The four totals in the submatrices obtained by separating nine-lines from high lines are $x$, $9a-x$, $9b-x$ and $226-9(a+b)+x$.

The preliminary checker distributes each of these totals as evenly as possible to lower-bound pair and triple counts. Write $P_k(t,m)$ for the sum of $\binom{n_i}{k}$ at the balanced distribution of $t$ entries over $m$ bins. The following tests and their transposes leave 358 unordered degree-profile pairs.

* The nine-lines meet on both sides, giving $x\ge\max(a,b)$. Pairs of nine-rows occur at most once on nine-columns, so $P_2(x,b)\le\binom a2$. Each pair of rows covers, over its common columns, at most 42 units of $c-2$, since each of the other 21 rows extends the pair in at most two columns. This gives $7P_2(x,b)+8P_2(9a-x,23-b)\le42\binom a2$.
* Each triple of nine-rows, or of high rows, occurs at most twice. Sum the balanced triple counts on both classes of columns for each class of rows.
* A long row of degree $d$ needs at least $d-5$ nine-columns. A ten-row needs at least two. Count these incidences against $9b-x$. For the long rows also bound each subset size by $b$, each pair intersection by six, and each triple intersection by two. Bounding the total incidences of two or three subsets by one or two copies of $b$ plus their maximum common intersection gives the corresponding tests in the replay. For all long rows together apply the balanced pair and triple counts on the $b$ nine-columns.
* A long column contains at least $c-5$ nine-rows. On a nine-row incident to $s$ nine-columns, the sum of $c-10$ on its high columns is at most $1+s$. Hence $\sum_{c\ge11}(c-10)(c-5)\le a+x$.

For a surviving profile, a signature for a line of degree $d$ is the vector of numbers of its entries on each opposite degree class. A nonnegative integer variable counts lines with each permitted signature. The variables for a degree class sum to its multiplicity. Counts of entries between every row type and column type must agree when computed from either side.

For each multiset of two or three types the number of actual tuples of distinct lines is the product of the binomial coefficients for its multiplicities. A signature covers the same product using its own counts. For a triple, sum the covered counts over all signatures and allow at most twice the number of tuples. For a pair the ordinary multiplicity bound is five if a nine-line occurs, six otherwise. Also sum the covered pair counts weighted by $d-2$, allowing 42 per pair. For pairs of nine-lines the contribution from opposite nine-lines is at most one per pair.

| Test | Cases tested | Cases surviving |
|---|---:|---:|
| Degree signatures for the preliminary profile pairs | 358 | 30 |
| Forbid five high entries of weight at least six on every long line in both orientations | 30 | 0 |
| Mark the forced eleven-row and the second row on its six nine-columns, allowing transposition | 142 | 1 |
| In that orientation, also forbid such an eleven-column | 1 | 0 |

## Why the final orientation matters

For the third test, distinguish the pair of rows and the six nine-columns as new types, retaining their original degrees. The two marked rows each meet all six marked columns. Every other row meets exactly two. Every unmarked column meets at most one of the marked rows. An unmarked nine-column can meet at most three nine-rows, since their pairs of marked columns must be disjoint to avoid an all-ones 2 × 2 on nine-lines. At least one distinguished eleven-row meets five high columns of total weight at least six. The same signature and tuple counts now apply to the refined types.

The single surviving orientation has the following numbers of lines, with marked row degrees eleven and twelve.

| Degree | 9 | 10 | 11 | 12 |
|---|---:|---:|---:|---:|
| Rows | 12 | 4 | 6 | 1 |
| Columns | 12 | 5 | 4 | 2 |

If this matrix also had a long column with five high entries of total weight at least six, transposing would give a survivor with the two profile rows in the opposite order. The exhaustive oriented count gives only the order displayed. The final integer test consequently forbids such columns and finds no remaining assignment. This excludes 226.

## Replay

Run the following in this directory. The smaller numerical and structural inputs have their own linked replays.

```sh
python3 verify_226.py --jobs 2
python3 verify_profiles.py
```

The first checker requires a C++20 compiler and 64-bit nauty. The second uses OR-Tools and SciPy. For every integer system reported infeasible, a separate checker verifies the exclusion using integer bound propagation, nonnegative integer combinations of inequalities, and exhaustive splits of integer intervals. The linear-programming solver proposes multipliers and splits. The checker recomputes the contradiction using integer arithmetic. [Profile replay](verify_profiles.py) · [Integer checker](verify_linear.py) · [217 minimum-degree input](../z22x23-k33/min9.md)
