# Four eight-one columns force row deficit at most six

In a 209-one matrix on 21 × 23 avoiding an all-ones 3 × 3, let $D$ be the sum of $10-d$ over rows of degree $d<10$. If exactly four columns have degree eight, then **$4\le D\le6$**. The previous degree bounds give $4\le D\le7$ and a unique row-degree profile at $D=7$, with seven nines, eight tens and six elevens. Every eleven-row meets at least three of the four eight-one columns, called the low columns. A nine-row meets at most one. On each low column the sum of $d-10$ over its eight incident rows is at most three. [Row profiles](six-columns.md) · [Low-column bound](eight-columns.md)

## Forcing the marked column

The four low columns have four triples, each usable by at most two rows. If one eleven-row met all four columns, that row alone would use four triple occurrences and the other five eleven-rows would use at least five more. Only eight are available. Thus each eleven-row meets exactly three low columns.

Group the six eleven-rows by the low column they miss. Each group has size at most two, because its rows share the other three columns. At least two groups must have size exactly two. Their missed columns each contain exactly four eleven-rows.

Now sum $d-10$ over all incidences with low columns. The eleven-rows contribute 18, and the seven nine-rows subtract at most seven. The sum is at least 11. Since each of the four columns contributes at most three, **at least three columns contribute exactly three**. One of these is among the at least two columns containing exactly four eleven-rows. On this column the four elevens contribute four, so exactly one nine-row and three ten-rows complete it.

## Exhausting the possible projections

Mark this low column and its eight incident rows. The other 22 columns restrict to 22 subsets of the marked rows. Their total size is $4(11-1)+3(10-1)+(9-1)=75$. Two subsets intersect in at most two marked rows, since the mark covers all eight. Each subset has size at most five by the low-column bound. Every marked row has load at least eight outside the mark. The existing eight-point catalogue at load at least 75 has 306,203 entries. Exactly **25,389** have the required marked degrees. [Catalogue and low-column proof](eight-columns.md)

Outside the mark, a completion must place five further ten-rows and two further eleven-rows, as well as six nine-rows. The row search tries every way to place the five tens and two elevens on the other 22 columns. Two missing rows have distinct supports since seven shared columns would need at least 56 entries and the two rows plus the other nineteen could supply at most $14+19\cdot2=52$. **None of the 25,389 projections admits the seven required rows.** The positive control recovers four outside ten-rows on a marked column from the 207-one witness. [Row search](marked_low_rows.cpp) · [Replay](verify_four_deficit_seven.py)

The four-column case now has four candidate row-degree profiles at $D=4$, five at $D=5$ and three at $D=6$. The five-column case has twenty across $D=5,6,7$. These counts refer to degree vectors before placing the entries. The numerical bounds remain $207\le z(21,23;3,3)\le209$.

Run from this directory with Python, a C++20 compiler and nauty installed.

```sh
python3 verify_four_deficit_seven.py --jobs 4
```
