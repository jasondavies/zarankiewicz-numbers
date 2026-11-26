# Excluding weight 187 on 20 × 21

No 20 × 21 binary matrix with 187 ones avoids an all-ones 3 × 3 submatrix. Hence $z(20,21;3,3)\le186$. The argument treats all column profiles together, including the profile with four eight-columns excluded separately before. Counting forces a row whose neighbourhood lies in a catalogue of 1,221 projections, and none of them completes. [Earlier reductions](core-search.md) · [Replay driver](verify_rare_rows.py)

## Facts used

Suppose a 187-one matrix exists. The earlier reductions give the following. Every column has degree eight, nine or ten, and there are $q$, $23-2q$ and $q-2$ columns of these degrees with $4\le q\le7$. Every row has degree at least eight and at most one row has degree eight. Every row meets at most eight columns of degree nine or ten, and a nine-row meets at most two eight-columns. Since the total weight is 187, the row degrees satisfy $\sum_R(d_R-9)=7$. The separate exclusion of $q=4$ is not needed here. [Profiles](core-search.md)

**Two nine-rows cannot share two eight-columns.** Delete the two eight-columns. This leaves 171 ones on 20 × 19. Each of the two nine-rows now has degree seven, so deleting them as well would leave 157 ones on 18 × 19, above the maximum of 156. [18 × 19 result](../z18x19-k33/README.md)

**Two columns share at most five rows.** Six rows contain at least $8+5\cdot9=53$ ones, but two covering columns and the nineteen others supply at most $12+19\cdot2=50$.

## Row projections

For a row $R$ of degree $d$, take its columns as points. The other nineteen rows give nineteen blocks on these points. Two blocks meet in at most two points, since a common triple would form a forbidden submatrix with $R$. The load of a point is the degree of its column minus one, hence 7, 8 or 9 according as the column has degree eight, nine or ten. Write $e$ and $n_{10}$ for the numbers of eight-columns and ten-columns meeting $R$. The total load is
$$
7e+8(d-e-n_{10})+9n_{10}=8d-e+n_{10}.
$$

**Six shared columns.** Suppose rows $R$ and $R'$ share a set $W$ of six columns. The columns of $W$ contain at least 48 ones. Every other row meets at most two of them, so they contain at most $12+18\cdot2=48$. Equality forces every column of $W$ to have degree eight and every other row to meet exactly two columns of $W$. The same count shows that $R$ and $R'$ cannot share seven columns, so $R\cap R'=W$. The eight-row would meet no eight-column, so there is no eight-row. Every row other than $R$ and $R'$ meets at most $2+(q-6)\le3$ eight-columns. In particular $\{R,R'\}$ is the only pair of rows sharing six columns. Apart from this pair, every block in every projection has size at most five.

We use three catalogue facts about nineteen blocks of size at most five, pairwise meeting in at most two points, with loads between 7 and 9.

| Points | Condition | Projections |
|---:|---|---:|
| 9 | total at least 73, one or two loads of 7 | 1,219 |
| 10 | total at least 80 | 0 |
| 10 | total 79 | 2 |
| 11 | total at least 84 | 0 |

The two ten-point projections at total 79 both have four loads of 7 and three loads of 9. The nine-point projections split as 509, 8, 698 and 4 projections with $(e,n_{10})=(1,2),(1,3),(2,3),(2,4)$.

Call a row **special** if it is a nine-row with $n_{10}\ge e+1$, or a ten-row with $(e,n_{10})=(4,3)$. Consider a row outside a six-sharing pair.

- A nine-row has $1\le e\le2$ and total $72-e+n_{10}$. Unless it is special, $n_{10}\le e$.
- A ten-row has total $80-e+n_{10}\le79$. Equality occurs only for special rows, so otherwise $n_{10}\le e-2$.
- A row of degree $d\ge11$ meets at least $d-8$ eight-columns. Delete $d-11$ eight-column points from its projection. The remaining eleven points have total $8d-e+n_{10}-7(d-11)=d-e+n_{10}+77\le83$. Thus $n_{10}\le e-d+6$.
- The eight-row has $e=0$ and $n_{10}\le q-2$.

## Some row is special

Suppose first that no two rows share six columns and that no row is special. Set $c(8)=-(q-2)$, $c(9)=0$, $c(10)=2$ and $c(d)=d-6$ for $d\ge11$. Then every row satisfies $n_{10}\le e-c(d)$. Summing over rows gives $10(q-2)\le8q-\sum_Rc(d_R)$, or
$$
\sum_R c(d_R)\le20-2q.
$$
Let $s\in\{0,1\}$ be the number of eight-rows. The rows of degree at least ten have $\sum(d-9)=7+s$ and degree at most $q+8$. Since $c(d)\ge2(d-9)$ for $d\le12$, the left side is at least $14+2s-s(q-2)$ minus a small correction for rows of degree 13 or more. The replay checks every multiset of such degrees. In each case the left side exceeds $20-2q$.

Suppose instead that $R$ and $R'$ share six columns. Then $q\ge6$ and there is no eight-row. Every other row meets exactly two columns of $W$. In particular each other nine-row meets two eight-columns, both in $W$. By the pair restriction there are at most $\binom62=15$ such nine-rows. So at least three of the other eighteen rows have degree ten or more. Write $d_R=9+a$ and $d_{R'}=9+a'$. Both rows meet at least six eight-columns, so $a,a'\ge1$ and $a+a'\le4$. Each meets at most $\min(q-2,a+3)$ ten-columns. Every other row meets at most three eight-columns, so its degree is at most eleven and $c(d)\ge2(d-9)$. Assuming no special row,
$$
10(q-2)\le 8q-12-2(7-a-a')+\min(q-2,a+3)+\min(q-2,a'+3).
$$
This fails for $q=6,7$ and every admissible $a,a'$. The two rows $R,R'$ meet six eight-columns and so are not special themselves. Hence in either case some special row lies outside any six-sharing pair, and all its blocks have size at most five.

## Completing the special projections

Mark a special row. Its columns are completely known on all twenty rows. The other $21-d$ columns avoid the marked row and have degree eight, nine or ten. The border checker generates every such support that meets each pair of fixed columns in at most two rows. It then chooses distinct supports, checking all triples, until the weight reaches 187. Distinct supports suffice by the bound on shared rows. All 1,219 nine-row projections and both ten-row projections fail. [Border checker](../z16x18-k33/borders.cpp)

The catalogues come from the canonical block generator, extended to eleven points. A second nine-point generator first builds every canonical family of four- and five-blocks and then adds the smaller blocks. It reproduces the same 1,525 projections with loads 7 to 9 at total at least 73, which contain the 1,219 special ones. The replay checks the ten-point facts again with the independent five-family generator. It reproduces both projections at total 79 and nothing at 80. On eleven points a total of 84 needs at least eight five-blocks and $27-2m$ four-blocks when there are $m$ fives. None of the six families of eight or more fives admits enough mutually compatible fours. [Block generator](../z18x19-k33/small_points.cpp) · [Second nine-point generator](nine_large.cpp) · [Ten-point generator](../z18-k33/ten_points.cpp)

The replay includes two positive controls. Deleting a row of the 193-one square leaves twenty rows. Sixteen of their nine-point projections satisfy the same load conditions at total 72. Each is found in the generated catalogue after canonical relabelling. Given just the projection of one marked row of the 185-one rectangle, the border checker rebuilds a complete 185-one rectangle. This works for a nine-row and a ten-row, and every row and column triple of the output is checked. [193-one square](../z21-k33/witness-193.txt) · [185-one rectangle](witness-185.txt)

## Replay

From this directory, with Python 3.10+, C++20 and nauty, run

```sh
python3 verify_rare_rows.py --jobs 8
```

The replay takes a few minutes. It assumes the restrictions proved by `verify_bounds.py` and `verify_core_bounds.py --full`.
