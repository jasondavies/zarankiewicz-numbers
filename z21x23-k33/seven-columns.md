# Seven eight-one columns are impossible at weight 209

A 209-one matrix on 21 × 23 avoiding an all-ones 3 × 3 must have **four, five or six columns of degree eight**. Deleting any four leaves an extremal 177-one parent on 21 × 19 with **zero, one or two** eight-one columns. Here we exclude seven on the full board. [Earlier degree and deletion bounds](eight-columns.md)

## What the short rows can contain

Suppose seven columns have degree eight. The other sixteen, called high columns, have total degree 153. Give a high column of degree $c$ the weight $e=c-9$. These weights sum to nine. A short row has full degree eight or nine. Let $W$ be the sum of the weights on its high entries. We show that **an eight-row has $W\le4$ and a nine-row has $W\le3$**.

An eight-row avoids the seven low columns and a nine-row meets at most one. If $W\ge5$, mark eight high entries carrying at least five units, dropping a zero-weight entry if there are nine high entries and such an entry exists. The other twenty rows give twenty blocks on the mark. Each point has load at least eight, and the loads total at least $64+5=69$. The blocks have size at most five and meet pairwise in at most two marked points. Indeed, six shared columns would need at least $6\cdot9$ incidences against the capacity $12+19\cdot2=50$ of two rows sharing them. Three common points of two blocks would form a forbidden submatrix with the marked row.

There are 181,521 eight-point projections. None accepts eight missing high columns at weight 153. If there is a ninth high entry, its column must go through at least eight blocks meeting pairwise in at most one of the first eight points. The 209 resulting nine-point projections all fail to accept seven missing high columns. This proves $W\le4$ for every short row. [Projection checker](verify_seven_columns.py)

It remains to exclude a **nine-row with $W=4$**. Mark eight high entries capturing all four units. If the ninth entry is high, one can take it to have weight zero, since nine positive weights on the row would already exceed four. The other twenty rows have exactly 68 incidences on the first eight points. The ninth point has load seven if it is low and eight if it is high. Even with one low column a six-point block needs at least $5\cdot9+8=53$ incidences, again exceeding 50.

| Ninth column on the mark | Nine-point projections | Additional high columns required | Target on the tested columns | Completions |
|---|---:|---:|---:|---:|
| Degree nine | 2,186 | 7 | 153 | 0 |
| Degree eight | 928,583 | 8 | 161 | 0 |

In the second line the test includes the low column on the mark, so the target is $153+8$. In both lines the missing columns avoid the marked row and have total excess five above degree nine. It suffices to allow each degree from nine through fourteen. Their supports are distinct. Two identical columns would share at least nine rows of degree at least eight, requiring at least 72 incidences against capacity $18+21\cdot2=60$.

## Enumerating the nine-point projections

First enumerate the blocks of size five and four on the eight high points, up to point permutations. Add fives before fours. Each remaining block has size at most three. Keep every family whose twenty blocks could still reach 68 incidences. There are 89 such families of large blocks. For each, choose which blocks also contain the ninth point. Enforce the five-point size limit and pairwise intersection limit of two after this choice.

If $n$ small blocks still have to supply $w$ incidences on the first eight points, their multiplicities $b_i$ by size obey $b_0+b_1+b_2+b_3=n$ and $3b_0+2b_1+b_2=3n-w$. Enumerate these counts and their splits between blocks containing and avoiding the ninth point. Place every compatible multiset of supports with those counts and keep load at least eight on every original point. Equal supports of full size at most two are allowed. Canonicalizing the completed nine-point families preserves feasibility since the missing high columns see exactly these fixed incidences. At load 69 through seven blocks, independently lifting the ordinary eight-point catalogue gives the same set of 4,629 projections. [Generator](nine_row_projections.cpp) · [Calibration and completion checks](verify_seven_columns.py)

## Only three column profiles remain, and each exceeds triple capacity

Let $K$ be the number of short rows and $a$ the number of eight-rows. We know $a\le1$. Each short row meets the seven low columns at most once. If there were eleven short rows, the remaining ten rows would have at least $56-11=45$ ones in those seven columns, exceeding $z(7,10;3,3)\le44$. Thus $K\le10$. [Deletion bound for eight-rows](eight-columns.md) · [Collins et al., Table 4](https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf)

Write $D_j$ for the row deficit on column $j$, where a row of degree $d$ contributes $(10-d)_+$. Counting weighted incidences on short rows gives
$$
\sum_j e_jD_j\le 3(K-a)+8a=3K+5a\le35.
$$
Every ten-column carries at least three deficit units. A column of degree $c\ge11$ carries at least $c-6$, by the eleven-row deficit bound. Charging three per weight unit uses 27. An eleven-column costs at least four extra units and a twelve-column costs at least nine extra. Larger degrees cost still more. We can therefore have zero, one or two eleven-columns, with all other high degrees nine or ten. [Column deficit bounds](eight-columns.md)

Each nine-row contains at least eight high entries. Since $W\le3$, at least five of them are nine-columns. An eight-row has at least four nine-columns. Each eleven-column on either row forces one extra nine-column, since an eleven-column uses two weight units. A nine-row therefore covers at least ten triples of nine-columns plus ten per incident eleven-column. An eight-row on $h$ eleven-columns covers at least $\binom{4+h}{3}$ triples.

| Eleven-columns | Nine-columns | Minimum weighted deficit | Minimum triples required | Maximum available |
|---:|---:|---:|---:|---:|
| 0 | 7 | 27 | 74 | 70 |
| 1 | 8 | 31 | 120 | 112 |
| 2 | 9 | 35 | 170 | 168 |

For zero eleven-columns, $3K+5a\ge27$ requires at least nine nine-rows when $a=0$, or at least seven nine-rows as well as the eight-row when $a=1$. The latter case already gives $7\cdot10+4=74$. For one eleven-column we must have an eight-row and $K\ge9$. The eight-row and eight nine-rows supply at least 84 triples. The column needs five deficit units. If it contains the eight-row, it also contains at least three nine-rows, adding at least $6+30=36$ triples. If it misses the eight-row, at least five nine-rows contribute.

With two eleven-columns, equality forces $K=10$ and $a=1$. The baseline from nine nine-rows and the eight-row is 94. If the eight-row meets both eleven-columns, the nine-rows supply at least six incidences with them, adding at least 60 triples. The eight-row itself adds at least $\binom63-\binom43=16$ more. Meeting fewer eleven-columns only increases the required count. The available count is twice the number of triples of nine-columns, since three occurrences give a forbidden all-ones $3\times3$. All three profiles are impossible.

The bounds on $z(21,23;3,3)$ remain 207 and 209. Two eight-one columns in the parent give six on the full board and seventeen high columns of total weight 161. The subsequent deficit argument excludes this case. [Six-column proof](six-columns.md)

## A deficit bound for the three remaining cases

Let $q$ be the number of eight-one columns, $n_d$ the number of rows of degree $d$, and $D=2n_8+n_9$ the total deficit below degree ten. Each low column has net row excess at most three. Sum these excesses over the $q$ low columns. A row of degree $10+s$ meets at least $s+2$ of them, an eight-row misses all of them, and a nine-row meets at most one. The total positive row excess is $D-1$ and the maximum row degree is thirteen. Hence
$$
3q \ge 3(D-1)+2n_{12}+6n_{13}-n_9
    =2(D+n_8+n_{12}+3n_{13})-3.
$$
The quantity $D+n_8+n_{12}+3n_{13}$ is therefore at most **7, 9 and 10** when $q$ is **4, 5 and 6**, respectively. [Degree and net-excess bounds](eight-columns.md)

For $q=6$ we can also prove $D\ge6$. Suppose $D\le5$. Every column then has degree at most eleven by the column deficit bound. Repeat the load-69 test with seventeen high columns of total weight 161, allowing missing degrees nine through eleven. All 181,521 eight-point projections and all 209 nine-point lifts fail. Every short row therefore has $W\le4$. The seventeen high columns have total excess $161-9\cdot17=8$ and each positive-weight column carries at least three deficit units. This gives $24\le\sum_j e_jD_j\le4D\le20$, a contradiction. Thus the next case requires $6\le D\le10$.

## Replay

From this directory run with Python, a C++20 compiler and nauty installed.

```sh
python3 verify_seven_columns.py --jobs 4
python3 verify_seven_columns.py --six-deficit --jobs 4
```
