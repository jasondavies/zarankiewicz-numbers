# The maximum on 22 × 23 is 216

The stored [matrix with 216 ones](witness-216.txt) has no all-ones 3 × 3. From any matrix with more than 217 ones, erasing entries gives a matrix with exactly 217 ones and preserves avoidance. We exclude 217 by double-counting two sums of degrees. The only new computational steps are the local column tests below.

## Restrictions used

Suppose the matrix has 217 ones. Write $d_r$ and $c_j$ for its row and column degrees. All rows have degree at least nine. There are $k\in\{1,2\}$ columns of degree eight, and every other column has degree at least nine. Each eight-column contains at most one nine-row. At least seven rows have degree nine. A nine-row avoiding all eight-columns has incident column excess $\sum_{j\sim r}(c_j-9)$ at most six. Every ten-column meets at least three nine-rows. A column of degree $c\ge11$ meets at least $c-5$ nine-rows. [Column counts and degree minima](README.md) · [Nine-row incidences](nine-rows.md) · [Degree excess bounds](six-nine-rows.md) · [At least seven nine-rows](seven-nine-rows.md) · [Long-column bound](min9.md)

Two columns share at most five rows. If they share six, those six rows require at least 54 ones. The two columns supply twelve, and each other column supplies at most two, for a total of at most 54. Thus all six rows have degree nine and each other column meets exactly two of them. An eight-column exists, and it would contain either six or two of these nine-rows. Both violate its bound of one.

Every row has degree at most fifteen. If it meets $t$ columns of degree at least nine, it has at least $8t$ incidences there with the other 21 rows. Each other row shares at most five such columns, since six columns of degree at least nine require 54 entries and two rows containing them can supply at most $12+20\cdot2=52$ with the remaining rows. Hence $t\le13$, with at most two additional eight-columns.

## Column scores

Give row $r$ the nonnegative weight $d_r-9$. Define the score of column $j$ to be $W_j=\sum_{r\sim j}(d_r-9)$. The following are necessary for a matrix of weight 217.

| Column degree | 8 | 9 | 10 or greater |
|---|---:|---:|---:|
| Maximum score | 11 | 9 | 7 |

The eight-column bound is the known upper bound of 83 on its incident row degrees, less $8\cdot9$. [Eight-column replay](six-nine-rows.md)

For degree nine, mark its nine rows. For degree ten or greater and score at least eight, mark the ten heaviest incident rows. Their score is at least eight, since weights are nonnegative integers. The other 22 columns restrict to blocks of at most five marked points by the intersection bound. Two blocks meet in at most two marked points. The load of a point is its row degree minus one, between eight and fourteen.

For nine points the forbidden score starts at ten, giving total load at least $9\cdot8+10=82$. For ten points the forbidden score starts at eight, giving total load at least 88. A ten-point mark with score at least nine and at least five positive-weight points is already excluded. [Earlier ten-point restriction](min9.md)

| Points | Total load at least | Canonical projections | Eligible after the earlier restriction | Eligible projections admitting the required outside rows |
|---|---:|---:|---:|---:|
| 9 | 82 | 60,469 | 60,469 | 0 |
| 10 | 88 | 453,448 | 452,058 | 0 |

To enumerate the projections, take every compatible family of five-point blocks up to relabelling, including the empty family. Complete each family with four-point and smaller blocks, allowing repeated blocks of size at most two. Canonicalize the resulting multisets under relabelling of the marked points. [Five-block enumeration](../z17x18-k33/fives.cpp) · [Dense projection enumeration](../z18-k33/ten_points.cpp)

If the marked column has degree greater than ten, a further incident row needs eight entries among the 22 outside columns. Each pair among those eight blocks can already share at most one marked point, since the new row also meets the marked column. Equivalently, these eight positions must be a clique when adjacency means intersection at most one. None of the 452,058 eligible ten-point marks admits an eight-clique. This disposes of every longer column with score at least eight.

For a full mark of $p=9$ or 10 rows, let $M$ be their total degree and $h$ the number of nine-rows among them. The remaining $22-p$ rows avoid the marked column. Relative to nine entries each they must supply gain $217-M-9(22-p)$. At most $22-p-\max(0,7-h)$ of them can contribute positive gain. Enumerate supports of sizes 10 through 15 on the 22 outside positions. Reject supports incompatible with any two marked rows. Choose longer rows in descending size and then choose ten-rows, enforcing the triple intersection bound with every previously chosen row. Distinct supports suffice because two equal outside supports of size at least ten would share at least eight columns of degree at least nine. A true completion supplies a compatible choice reaching the gain within the available slots. No eligible projection in either catalogue does so.

Run the final replay from this directory with Python 3.10+, C++20 and nauty installed. It regenerates both catalogues, checks the 216-one witness, recovers partial placements from the witness, and runs the exclusions. The prior lemmas have their own linked replays. [Replay](verify_217.py) · [Column tests](column_scores.cpp)

```sh
python3 verify_217.py --jobs 4
```

## Two incompatible incidence counts

Let $a$ count the nine-rows and $m$ the columns of degree at least ten. Call those columns high. For a high column set $e_j=c_j-9$. Write $E=\sum e_j=10+k$ and $D=\sum(e_j-1)=E-m$. The first equality follows by counting the 217 ones relative to nine in every column.

First sum the column scores. On the row side the sum is $\sum_r d_r(d_r-9)$. The rows of degree at least ten have degrees $10+s_r$ with $s_r\ge0$ and $\sum s_r=a-3$. Since $s^2\ge s$ for every nonnegative integer $s$, we obtain
$$
\sum_j W_j=10(22-a)+11\sum s_r+\sum s_r^2\ \ge\ 184+2a.
$$
The column bounds give
$$
\sum_j W_j\le 11k+9(23-k-m)+7m=207+2k-2m.
$$
By integrality $a+m\le11+k$, or equivalently $a\le D+1$.

Next count the weighted incidences of high columns with nine-rows, giving each such incidence weight $e_j$. Write $T$ for their total. A ten-column contributes at least three. A column with $e\ge2$ meets at least $4+e$ nine-rows. Its contribution exceeds or equals $3e+6(e-1)$ because $e(e+4)-3e-6(e-1)=(e-2)(e-3)\ge0$ for integer $e\ge2$. Summing gives $T\ge3E+6D$.

A nine-row avoiding the eight-columns contributes at most six. At most $k$ nine-rows meet any eight-column, and each contributes at most the entire weight $E=10+k\le12$. Hence $T\le6a+6k\le6D+6+6k$. Combining with the lower bound requires $3(10+k)\le6+6k$, or $k\ge8$. Both possibilities $k=1,2$ are excluded.

Thus $z(22,23;3,3)=216$. It also follows immediately that $z(23,23;3,3)\le\lfloor23\cdot216/22\rfloor=225$, since each entry survives 22 of the 23 single-row deletions. The [225-one square](../z23-k33/witness-225.txt) attains the bound.
