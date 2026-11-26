# Excluding 145 ones on 17 × 18

The preceding ceiling was 145. At weight 146 some row has at most eight ones and deleting it contradicts the 16 × 18 maximum of 137. At weight 145, every row has at least eight ones, at least eight rows have exactly eight, and deletion of any one of these gives an extremal 137-one core. We test all possible extensions by choosing a marked column in the putative larger matrix. This avoids enumerating extremal cores with a row of weight below eight. [Wei’s earlier bounds](https://doi.org/10.5281/zenodo.24553293) · [Independent 16 × 18 proof](../z16x18-k33/README.md)

## Mark a column of maximum degree

Some column has degree $t\ge9$ because $145>18\cdot8$. Two columns cannot share six rows. Those rows would have at least 48 ones, but two columns supply twelve and every other column supplies at most two. The seventeen other columns thus restrict to blocks of size at most five on the $t$ marked rows. Two blocks intersect in at most two points. Write $S$ for their total size. Each point has load at least seven, so $7t\le S\le85$ and $t\le12$. The $17-t$ rows outside the marked column have $145-t-S$ ones on the remaining seventeen columns.

- **Twelve.** The five outside rows contain at most 52 ones. At 53 ones, distributing them evenly among seventeen columns would already cover $15\binom33+2\binom43=23$ row triples with multiplicity, against a capacity of $2\binom53=20$. Thus $S\ge81$, requiring at least thirteen five-blocks. The pencil argument below excludes thirteen.
- **Eleven.** Six outside rows contain at most 58 ones, so $S\ge76$. Enumerating compatible families of fives, then their compatible fours, gives no such projection with every load at least seven. [Six-row ceiling, Collins et al., Table 4](https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf)
- **Ten.** If $S\ge71$, the same enumeration yields 24 projections with the required loads. For $S\le70$, the seven outside rows contain at least 65 ones. There are 1,096 outside projections up to isomorphism with all seven degrees at least eight.
- **Nine.** If $S\ge65$, enumerate the marked side on nine points. There are 87,842 projections with every point load at least seven. If $S\le64$, enumerate instead the eight outside rows, which have 72 or 73 ones. The upper limit follows from $S\ge63$. Delete a minimum outside row, of degree eight or nine. At degree eight the seven-row remainder has at least 64 ones and minimum row degree eight. At degree nine it has at least 63 ones and minimum degree nine. Generate each seven-row family, then try all legal supports of the deleted row. For a triple of columns already covered twice, selecting two makes the third forbidden. Among columns with identical seven-row traces it suffices to select an initial segment. Canonicalizing the eight-row results yields 81,345 projections in the first case and 824 in the second. None extends.

The exhaustive border counts are 24 and 1,096 for a ten-column, and 87,842, 81,345 and 824 for a nine-column. All five return zero. A higher-weight matrix would yield a 145-one matrix by erasing entries.

## Why thirteen five-blocks on twelve points are impossible

Thirteen blocks give 65 incidences, so some point belongs to at least six blocks. It cannot belong to seven. Deleting it from seven blocks would give seven four-sets on eleven points, any two intersecting at most once. Balancing 28 incidences over the eleven points already requires 23 intersections, exceeding the 21 pairs of blocks.

Deleting that point from its six blocks leaves six four-sets with 24 incidences. The minimum possible number of intersections is 15, exactly the number of block pairs. Thus nine points occur twice, two occur three times, and each pair of blocks meets once. Each block meets its five partners at four points, so it contains exactly one point of multiplicity three. The two triple points partition the six blocks into groups of three. The nine double points correspond to the nine cross-group pairs. This determines the six original blocks up to isomorphism. Of the 51 further five-sets compatible with them and avoiding the distinguished point, no seven are pairwise compatible. The replay checks this clique assertion directly.

## Completing a projection

The fixed side specifies complete rows on seventeen coordinates, together with their marked-column entry. Missing rows contain the marked column exactly in the outside case. Each candidate must make legal triples with every two fixed rows, and selecting it imposes the same check on all later choices. Repeated missing rows are impossible at weight 145. Identical rows of degree at least eight would cover seven columns, whose degrees sum to at least 49 by the 17 × 17 maximum of 138. Two covering rows and the other fifteen could supply at most $14+2\cdot15=44$ ones there. [Square bound](../z17-k33/README.md)

For ten and eleven points, [the five-block generator](fives.cpp) constructs each family by appending another legal five-set and canonicalizing the bipartite incidence graph with a distinguished point shore. It retains the relabelled list of blocks. If $m$ five-sets and $q$ four-sets occur, $S\le51+2m+q$; this determines the smallest four-set clique to enumerate. The replay then tries all compatible smaller blocks, allowing repetition at sizes zero through two. The outside generator and the border search are shared with the independent 16 × 18 proof.

The command `python3 verify.py --jobs 4` replays this separate exclusion.
