# Which 177-one parents can accept four eight-one columns?

Let $P$ be an admissible 21 × 19 matrix of weight 177. If four new columns of weight eight can be added simultaneously, then $P$ has minimum column degree eight and **at most one of its 19 columns has degree eight**. In the completed 21 × 23 matrix the number $q$ of eight-columns is four or five. The short-row exhaustion below excludes nine. Weighted counts exclude eight and seven, and the six-column case forces contradictory row deficits. [Six-column proof](six-columns.md) [Eight-column proof](eight-columns.md) · [Seven-column proof](seven-columns.md) These restrictions apply to every choice of the four added columns. The numerical bounds on $z(21,23;3,3)$ remain 207 and 209. [Parent reduction and minimum degrees](README.md)

## How the short rows bound the number of eight-columns

Call a full column *high* if its degree is at least nine. Write $n=23-q$. Deleting all eight-columns leaves $209-8q=8n+25$ ones in the high columns. Every pair of rows shares at most five high columns. Six such columns would require at least 54 incidences, whereas two rows containing all six and the other nineteen rows can supply at most $12+19\cdot2=50$. Every row has at most ten high entries, since a row longer than ten meets at most eight high columns. [Long-row bound](README.md)

Write $D=\sum(10-d)_+$ over full row degrees $d$. The earlier proof gives $D\ge4$. Each row has degree at least eight. An eight-row avoids all eight-columns, and a nine-row meets at most one of them. Consequently there are at least two short rows (degree eight or nine), and each contains eight or nine high entries. Their union has size at least $8+8-5=11$. [Row-deficit proof](row-deficit.md)

* **Eleven high columns.** Two short rows must each contain eight high entries and share exactly five. Up to relabelling there is one layout. The integer certificate below bounds the total high entries by 109. The required total is 113.
* **Twelve high columns and at least three short rows.** Sort three short rows by high degree, and permute high columns. There are ten layouts satisfying the pair bound and the forbidden-triple condition. Their certified upper bounds range from 113 to 120. The required total is 121.
* **Twelve high columns and exactly two short rows.** These must both have degree eight, giving $D=4$. The argument below bounds every column degree by ten, which permits at most 120 high entries.

This leaves $n\ge13$. The thirteen-column case is excluded below.

### A large column must contain the deficient rows

Suppose a column contains eleven marked rows with at most four units of deficit among them. Each other column restricts to a block on those eleven points, and two such blocks meet in at most two points. A block of size six is impossible. Six rows require at least $60-4=56$ incidences, but two columns covering them permit at most $12+21\cdot2=54$.

The total block size is at least $11\cdot9-4=95$. The eleven-point lemma forbids twenty blocks of total size 88 or more. If the total of the 22 blocks were at least 96, discard two of size at most four, or take twenty fives when fewer than two blocks have size at most four. Thus the total is exactly 95. A block of size three or less is impossible by discarding it and another block of size at most four, or again taking twenty fives. There must be seven fives and fifteen fours. [Eleven-point lemma](../z21-k33/README.md)

Equality at 95 requires exactly four deficit units and zero row excess on the eleven marked rows. Each marked point therefore has load between seven and nine.

The existing five-block generator gives 15 families of exactly seven fives up to point permutation. Trying every compatible choice of fifteen fours yields 168 projections before filtering and ten with the necessary point loads (counts may repeat isomorphic projections). In none of the ten projections can seven blocks be chosen with pairwise intersections of size at most one. A further row on the marked column would require seven such blocks, since it has degree at least eight. Thus the marked column has degree exactly eleven. The ten missing rows miss the mark. Their degrees can range from eight through twenty-two. The border search rejects all ten projections even with that full degree range. Its missing rows may be taken distinct because two identical rows of degree ten or more would in particular share seven columns, requiring at least 56 entries against capacity 52. Consequently **every choice of eleven rows on a column must carry at least five deficit units**, independently of the deficit of the whole matrix. In particular every column has degree at most ten at $D=4$. When $D\le6$, every column of degree at least eleven must contain every eight-row, since omitting one leaves at most four deficit units. [Replay](verify_parent_bound.py)

### Exact certificates for high-column layouts

For a fixed tuple of short rows on the high columns, group the high columns by the subset of fixed rows they meet. The certificate assigns a nonnegative integer weight to each selected type of column triple and a nonpositive weight to each selected type of single column. An ordinary row's cost is the sum of the weights of the triples and columns it contains.

A triple has residual capacity two minus the number of fixed rows covering it. A single column has residual demand nine minus its fixed degree. Multiplying these by the corresponding signed weights and summing gives an upper bound $B$ on the total cost of all ordinary rows. For positive integer scale $s$, enumerate all subsets $R$ of the high columns that satisfy the row-degree, fixed-row pair and fixed-row triple bounds. Put $b=\max_R(s|R|-\mathrm{cost}(R))$. For $k$ fixed rows, the total number of high entries is at most
$$
\sum_{i=1}^k |R_i|+\left\lfloor\frac{B+(21-k)b}{s}\right\rfloor .
$$
Linear programming supplied the weights. Verification enumerates the layouts independently and uses only integer arithmetic to check each bound. In the file, a one-tag key represents the magnitude of a negative single-column weight. A three-tag key represents a positive triple weight. A tag is the binary incidence mask on the fixed rows. [Weights](high-column-bounds.json) · [Integer checker](verify_parent_bound.py)

### Excluding ten eight-columns

At $q=10$, the thirteen high columns need 129 ones. Three short rows have 44 possible layouts up to column permutation with their degrees in increasing order (ties may represent the same unordered layout). The certificates exclude 35. For the nine remaining layouts there are 67 placements of a fourth short row of at least the preceding high degree. Every placement has at most 126 high entries. Under this hypothesis there could therefore be only two or three short rows. They would carry $4\le D\le6$, with at least one eight-row. By the large-column argument above, that eight-row meets every column of degree above ten.

Mark its eight columns, all high. Let $E$ be the total column excess above ten among the 13 high columns. Their weight is 129, one short of 130, so exactly $E+1$ have degree nine. The mark captures all $E$ positive excess and at most $E+1$ negative units. Its eight point loads (column degrees minus one) thus total at least $8\cdot9+E-(E+1)=71$, and each load is at least eight. The 20 other rows give blocks of size at most five on the mark, with pairwise intersections at most two.

There are **41** such projections. The other five high columns all miss this eight-row and have degree nine or ten. The border search tests every completion to weight 129 on the high columns alone. None succeeds. Distinct supports suffice because duplicate high columns in a full solution would share at least nine rows of degree at least eight, exceeding the capacity of two columns on those rows and at most two incidences on each other column.

This excludes $q=10$. At this stage every possible parent has zero through five eight-one columns. The next two steps exclude the upper endpoint. [Projection and border replay](verify_parent_bound.py)

## Forcing four short rows when the parent has five eight-columns

Suppose the full matrix has nine eight-columns. The fourteen high columns have weight 137. Then **$D\ge7$** is necessary, so at least four rows have full degree eight or nine.

To see this, assume $D\le6$. At most five high columns have degree above ten, since the total excess above degree nine on the fourteen high columns is $137-14\cdot9=11$. If there is an eight-row, it meets all columns of degree above ten by the large-column argument. If all short rows have degree nine there are $D$ of them. A column of degree above ten must contain at least five, again by that argument. For $D=4$ there are no such columns, for $D=5$ all five rows are covered by each, and for $D=6$ each such column can miss at most one of six short rows. At most five columns cannot collectively miss all six. In every case choose a short row containing all columns of degree above ten.

This row has eight or nine high entries. Mark eight of them, including every column of degree above ten. If $E$ is total high-column excess above ten, there are $E+3$ nine-columns, since $14\cdot10-137=3$. The marked loads total at least $8\cdot9+E-(E+3)=69$. All loads are at least eight. The twenty blocks on the eight points have size at most five and intersect pairwise in at most two points.

There are 181,521 projections. If the row has only eight high entries, none permits the six missing high columns of degree nine or ten at the required weight of 137. If the row has a ninth high entry, its column has degree nine or ten. Its eight or nine other entries must select blocks meeting pairwise in at most one point, to respect triples with the marked row. Trying every such selection gives 209 augmented projections, allowing repeated representatives. None accepts the five remaining high columns. This excludes $D\le6$ at the endpoint. [Replay with the frontier option](verify_parent_bound.py)

## Excluding five eight-columns in the parent

Assume the full matrix has nine eight-columns. There are fourteen high columns of total weight 137. Let a short row mean a row of full degree eight or nine. Each short row **misses some high column of degree at least eleven**. Indeed, the eight-point projection in the preceding section excluded every short row containing all such columns. Its enumeration depends only on the high columns and the marked row. The assumption $D\le6$ was used to find such a row, and plays no part in excluding it once chosen.

Place the short rows on the fourteen high columns. Each has high degree eight or nine. At each placement, group columns by the subset of previously placed rows containing them. The number of selected columns in every group specifies the new row up to permutations within the groups. Discard masks that meet a placed row in more than five positions or meet two placed rows in more than two. The signed column and triple prices described above bound the total high weight for every completion. This test permits further short rows. Generate every surviving layout's children even when it fails the separate test for an *exact* set of short rows.

| Short rows placed | Layouts reached | Layouts allowing 137 by the high-weight bound | Layouts passing as the exact set of short rows |
|---:|---:|---:|---:|
| 4 | 189 | 30 | 0 |
| 5 | 427 | 8 | 0 |
| 6 | 15 | 1 | 0 |
| 7 | 1 | 1 | 0 |

No eighth short row fits the last layout. The earlier deficit bound guarantees at least four. The proof of the final column of the table uses the following integer tests.

* Assign each high column a degree $c_j\ge9$, with $\sum_j(c_j-9)=11$. Columns with identical marked incidence may have their degrees sorted. A pair of marked rows can have at most 38 incidences from the other nineteen rows on its common high columns, giving $\sum_{j\text{ common}}(c_j-2)\le38$.
* Enumerate whether each marked row has zero or one entry in the nine eight-columns, subject to full degree eight or nine and $D\ge7$. All deficit lies on these rows when the set is exact. For $c_j\ge11$, remove the largest $c_j-11$ incident deficits. The sum left must be at least five by the eleven-row result above. Every marked row must also miss a column with $c_j\ge11$.
* Delete any two marked rows with full degrees $a,b$. Among the 23 residual columns the two lightest must have total degree at least $209-a-b-177$, by the exact maximum on $19\times21$. The residual degrees of the fourteen high columns are determined. If the rows have zero, one or two entries in the low columns, the two lightest low degrees are at most $(8,8)$, $(7,8)$ or $(7,7)$ in the sense of the sums of the cheapest one and two. With two hits on the same column the actual pair is $(6,8)$, which only strengthens the test. For instance, two full eight-rows cannot share a nine-column. That column would drop to seven while every low column still has degree eight. [19 × 21 bound](../z19x21-k33/README.md)

Together the tests exclude every layout as a complete set of short rows. At this stage a 209-one matrix has four through eight eight-one columns. At eight, the fifteen high columns would have weight 145. A further short-row argument excludes this endpoint, leaving zero through three eight-columns in the parent. [Four-eight parent exclusion](eight-columns.md) [Exhaustive checker](verify_nine_eights.py)

## Testing concrete parents

An eight-subset of the 21 rows is an individually legal new column exactly when it meets the intersection of every pair of old columns in at most two rows. The checker enumerates all such eight-subsets and tries adding up to four together. At each addition it rechecks compatibility with the enlarged matrix. A successful result at four prints the full matrix. [Extension checker](parent_extensions.py)

The 177-, 185-, 193-, 201-, 210-, 216- and 225-one witnesses in the repository give respectively 1, 1, 2, 4, 20, 6 and 10 crops of size 21 × 19 and weight 177, counting both orientations and labelled deletions. For each choice of 21 rows, take all choices of nineteen columns of maximum total degree if that total is 177. The upper bound of 177 makes this exhaustive for each source. Partition-preserving bipartite graph isomorphism identifies two parents among the 44 crops.

| Parent | Individually legal eight-columns | Maximum simultaneously addable |
|---|---:|---:|
| Stored 177-one witness | 3 | 3 |
| Parent extracted from the 225-one square | 4 | 2 |

The four candidates in the second example form precisely two compatible pairs, with no candidate belonging to both pairs. To obtain the example, remove rows 21 and 23 and columns 7, 11, 14 and 18 of the square (one-based). A separate positive control removes four eight-columns from a 207-one grid and recovers a valid extension from 175 to 207. [Second parent](parent-from-225.txt) · [Source square](../z23-k33/witness-225.txt) · [Crop replay](verify_parent_crops.py)

Both parents are isolated, up to row and column permutations, under replacement of **up to six whole rows or up to six whole columns** at weight 177. For each choice of deleted parallel lines, the search generates every legal support for a replacement line and tests all multiset completions of the required total weight. If an old line is restored it can be matched to its replacement, so the case already occurs with fewer deletions. Repeated new masks are allowed. In a 177-one parent a row has degree at least six by $z(20,19)=171$, and a column has degree at least seven by $z(21,18)\le170$. Through six deletions the only changed labelled multiset occurs once, for six columns of the second parent. It is isomorphic to that parent. Simultaneous changes on both axes and other components remain possible. [Replacement enumerator](parent_trades.cpp)

## Replay

Run from this directory. The bound uses Python, C++20 and nauty. The nine-eight-column checker uses NumPy and SciPy. It rounds the proposed LP prices to nonnegative integers, checks an overflow bound and evaluates each exclusion by integer arithmetic. The crop and replacement checks also use NetworkX. The standalone parent checker takes either orientation of the matrix and uses the Python standard library.

```sh
python3 verify_parent_bound.py
python3 verify_parent_bound.py --frontier --jobs 4
OPENBLAS_NUM_THREADS=1 python3 verify_nine_eights.py
python3 verify_parent_crops.py --trades
python3 parent_extensions.py parent-from-225.txt
```
