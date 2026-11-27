# Six eight-one columns are impossible at weight 209

A 209-one matrix on 21 × 23 avoiding an all-ones 3 × 3 must have **four or five columns of degree eight**. Deleting four of them leaves an extremal 177-one matrix on 21 × 19 with **zero or one** column of degree eight. The bounds on the extremal weight are still 207 and 209. [Previous reduction to four, five or six](seven-columns.md)

Let $q$ count the degree-eight columns (the low columns), and $n_d$ the rows of degree $d$. Write $D=2n_8+n_9$ for the total row deficit below ten and $F=D+n_8+n_{12}+3n_{13}$. Earlier results give $D\ge4$, $n_8\le1$, all row degrees between eight and thirteen, and $F\le10$. If $q=6$, the earlier lower bound is $D\ge6$. [Degree bounds](eight-columns.md) · [Deficit bounds](seven-columns.md)

## The short rows require at least eight deficit units when $q=6$

The seventeen high columns contain 161 ones. Give each high column of degree $c$ weight $e=c-9$, so their weights sum to eight. Let $W$ be the weight incident to a short row (degree eight or nine). A degree-eight row avoids the low columns, and a degree-nine row meets at most one.

Suppose $W\ge5$. Mark the eight high entries of the short row with largest weights. They capture at least five units since the total high weight on the board is only eight. Their loads on the other twenty rows total at least 69 and every load is at least eight. Two projected rows intersect in at most two points. Each projected row contains at most five points, since six shared high columns need at least 54 entries and two rows sharing them allow only $12+19\cdot2=50$. There are 181,521 projections on eight points. If the marked row uses a ninth high column, adding it gives 209 further projections by the previous clique enumeration. The unmarked high columns have at most three units of excess in total and thus degree at most twelve.

It remains to test a nine-row with $W=4$. Mark eight high entries capturing all four units. A ninth high entry may be chosen to have weight zero. The twenty other rows give 68 incidences on the eight points. The ninth entry has load seven if it is low and eight if it is high. The nine-point catalogue from the seven-column proof covers both cases, including the possibility of a low point. The remaining high columns have at most four units of excess, so their degrees are at most thirteen. [Projection enumeration and independent calibration](seven-columns.md)

| Test | Points on the mark | Projections | Missing high columns | Weight required on the tested columns | Completions |
|---|---:|---:|---:|---:|---:|
| $W\ge5$, eight high entries | 8 | 181,521 | 9 | 161 | 0 |
| $W\ge5$, nine high entries | 9 | 209 | 8 | 161 | 0 |
| Nine-row with $W=4$, ninth entry high | 9 | 2,186 | 8 | 161 | 0 |
| Nine-row with $W=4$, ninth entry low | 9 | 928,583 | 9 | 169 | 0 |

In the last line the tested columns include the low column of degree eight on the mark. Missing high columns avoid the marked row and have distinct supports. Two identical columns of degree at least nine would share nine rows requiring at least 72 entries, against a capacity of $18+21\cdot2=60$.

Consequently an eight-row carries at most four units and a nine-row at most three. Each positive-weight column carries at least three units of row deficit by the column deficit bounds. Counting weighted incidences with short rows gives
$$
24=3\sum_j e_j \le \sum_j e_j D_j \le 8n_8+3n_9=3D+2n_8.
$$
Here $D_j$ counts row deficit on column $j$. For $D\le7$ the right side is at most 23. Hence $D\ge8$. [Column deficit bounds](eight-columns.md)

## Deficit eight or greater forces an impossible low column

Suppose $D\ge8$. Then $n_{13}=0$ because $F\le10$. The net row excess of a column is the sum of $d-10$ over its incident rows. A low column has net excess at most three by the earlier projection bound. Suppose it attains three. Its eight rows have total degree 83. Mark them and project the remaining 22 columns onto these eight points. There are exactly 75 incidences, and each point has load at least eight because every marked row has degree at least nine. Blocks meet pairwise in at most two points. The earlier low-column argument bounds block size by five. [Marked-column proof](eight-columns.md)

The catalogue at load at least 75 has 306,203 projections, of which 304,162 have load exactly 75. For each we read off the eight marked row degrees. We enumerate all global row-degree counts permitted by $8\le D\le10$, $F\le10$, $n_8\le1$ and total weight 209. Exactly 219,831 marks fit one or more such profiles. Choosing $D,n_8,n_{12},n_{13}$ determines
$$
n_9=D-2n_8,\qquad n_{11}=D-1-2n_{12}-3n_{13},
$$
and $n_{10}$ fills the remaining rows. Subtract the marked degrees from these counts and discard profiles with any negative entry.

For each surviving profile, place just the missing rows of degrees ten through twelve on the 22 unmarked columns. Each candidate row may cover a given pair of marked rows at most twice. Enumerate all supports of the requested sizes obeying these 28 pair constraints. Next choose supports in descending degree and in a fixed order within each degree. After selecting a row, keep a candidate only if its intersection with the selected row and each previously fixed row has size at most two. Two missing rows cannot have identical supports since any seven shared columns would require at least 56 entries against capacity $14+19\cdot2=52$. The 207-one witness supplies a positive control for placing outside rows on the same kind of mark. [Row search](marked_low_rows.cpp) · [Replay](verify_six_columns.py)

No projection admits all the required rows of degrees at least ten. Hence under the assumption $D\ge8$ every low column has net excess at most two. Summing over all $q$ low columns gives net excess at least $2F-3$. A row of degree $10+s$ contributes at least $s(s+2)$, an eight-row contributes zero, and a nine-row contributes at worst minus one. Consequently
$$
13 \le 2D-3 \le 2F-3 \le 2q \le 12.
$$
This contradiction proves **$D\le7$ for every remaining 209-one matrix**, including those with four or five low columns. Six low columns require $D\ge8$ by the short-row calculation, so that case is closed.

## A further reduction for five low columns

When $q=5$, the eighteen high columns have total degree 169 and total excess seven. Suppose $D=4$. The eleven-row deficit bound forces every column to have degree at most ten, so there are exactly seven ten-columns. Each needs at least three units of row deficit. Some short row therefore meets at least six ten-columns, since $5D=20<21$. [Eleven-row deficit bound](parent-extensions.md)

Mark eight high entries on that row, including every one on a ten-column. In the other twenty rows each marked point has load eight or nine. At least six have load nine. There are 307 such eight-point projections (304 with six tens and three with seven). None accepts the ten missing high columns of degrees nine or ten at weight 169. If the row uses a ninth high entry, choose it on a nine-column. It must go through eight compatible blocks. There is just one such lift, which cannot accept the nine missing high columns either.

This leaves **$5\le D\le7$** at five low columns and **$4\le D\le7$** at four. Counting the nonnegative degree vectors under these bounds and the previous $2F\le3q+3$ gives the table below. The four-column case excludes thirteen-rows because each would need five low columns. Each entry counts candidate row-degree vectors before placing their ones.

| Number of low columns | $D=4$ | $D=5$ | $D=6$ | $D=7$ |
|---:|---:|---:|---:|---:|
| 4 | 4 | 5 | 3 | 1 |
| 5 | 0 | 8 | 7 | 5 |

The subsequent four-column proof excludes the sole profile at $D=7$ in the first row, leaving twelve profiles there. The extremal value on 21 × 23 is still between 207 and 209. [Four-column deficit-seven proof and replay](four-deficit-seven.md)

## Replay

From this directory, run with Python, C++20 and nauty installed. The two arguments to `--part` can also be run separately.

```sh
python3 verify_six_columns.py --part short --jobs 4
python3 verify_six_columns.py --part large --jobs 4
```
