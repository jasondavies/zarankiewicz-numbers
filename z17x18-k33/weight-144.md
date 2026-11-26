# What a 144-one matrix would have to look like

**Its maximum column degree is exactly nine. Every pair of columns shares at most five rows.** The [final search](final-search.md) exhausts the remaining marked-column family.

Every row has degree at least seven by the 16 × 18 upper bound of 137, and every column has degree at least six by the 17 × 17 upper bound of 138. At most four rows have degree seven, since deleting five sevens would leave 109 ones on 12 × 18. The ceilings used for smaller rectangles are listed in [Collins et al., Table 4](https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf).

Two rows cannot share seven columns. Those columns would contain at most $14+2\cdot15=44$ ones, while the remaining eleven columns can contain at most 96. Thus all full rows are distinct, including the missing rows chosen by the border checker.

## The exceptional pair

If two columns share six rows, those rows have at least $4\cdot7+2\cdot8=44$ ones. The common columns supply twelve and the other sixteen columns supply at most two each, giving equality. Four of the rows have degree seven and two have degree eight. Every other column meets these six rows in exactly two. Seven shared rows are impossible by the same count. Moreover, there is at most one such column pair in the entire matrix. Its intersection must include all four seven-rows, and two distinct pairs would put at least three columns in all four rows.

## Large marked columns

Mark a column of degree $t$. As in the [145 proof](weight-145.md), let $S$ be the number of ones the marked rows have on the seventeen other columns. Each projected block has size at most five, except possibly one six-block. Thus $7t-4\le S\le86$, and $t\le12$.

- **Twelve.** At most twelve five-blocks fit on twelve points, by the pencil argument in the 145 proof. Hence $S\le4\cdot17+12+2=82$. The five outside rows contain at least 50 ones and each has degree at least seven. Their 310 projections have no completion.
- **Eleven, without a six-block.** The six outside rows have at most 58 ones. Thus $S\ge75$. The marked side has point loads at least six, with at most four units of total deficit below seven. All 10,577 generated projections fail the border check.
- **Eleven, with a six-block $H$.** The sixteen other blocks each meet $H$ in exactly two points. Write $m,q$ for their numbers of fives and fours. Then $75\le S\le70+m$ and $S\le54+2m+q$. For every family of at least five compatible fives on eleven points, the verifier tries every possible six-set meeting each five in two and all compatible cliques of at least $21-2m$ fours. Every surviving clique fills all seventeen blocks. Enforcing loads $6,6,6,6,7,7$ on $H$ and loads at least seven elsewhere leaves 16 projections. No border completes them.
- **Ten, with $S\le70$.** The seven outside rows contain at least 64 ones. Their 277,051 projections with minimum row degree seven have no completion.
- **Ten, with $S\ge71$ and no six-block.** The five- and four-block enumeration gives 82,422 labelled projections with the required loads. Relabelling the ten points gives 1,887 distinct projections. All fail the border check.

For the remaining ten-column case suppose a six-block $H$ occurs and $S\ge71$. There are four points outside $H$. Each of the sixteen ordinary blocks uses an edge (a two-element set) of $H$. An ordinary five-block uses three of the four outside points. Different five-blocks use different outside triples, and every two such triples share two points, so the associated edges of $H$ must be disjoint.

For a pair $P$ of outside points, ordinary fours with outside trace $P$ must use mutually disjoint edges of $H$. They must also avoid the edges of every five-block whose outside triple contains $P$. If $f_P$ such fives exist, at most $3-f_P$ fours use $P$. Summing over the six pairs gives $q\le18-3m$. Hence $S\le54+2m+q\le72-m$. With no five-block, $S\le70$. Consequently $m=1$, $q=15$, and all six matching bounds are attained. The two endpoints of the unique five-block’s edge can occur in at most three ordinary fours, one for each outside pair not contained in its triple. Including the five-block and the two exceptional columns gives either endpoint row degree at most six, a contradiction.

## Degrees at most nine

If every column had degree at most eight, all eighteen would have degree exactly eight. Two rows could not share six columns, as those six would have 48 ones against a capacity of 42. Ten chosen entries in a row would require 70 further ones on their columns across sixteen blocks. The ten-point five/four bound excludes this: with at most four fives the ceiling is 68, and for five or six fives there are too few compatible fours. A nine-row exists by total weight. Marking it gives sixteen blocks on nine points with every load exactly seven. There are ten projections and none extends by nine further eight-columns.

Finally, if a pair of columns of degrees $c,d$ shared six rows, the other eleven rows would contain exactly 100 ones. On the sixteen columns outside the pair these rows would have $100-(c-6)-(d-6)=112-c-d$ ones. Since $z(11,16;3,3)\le92$, this requires $c+d\ge20$, contradicting the maximum column degree of nine.

To replay these exclusions run

```sh
python3 reduce_144.py --jobs 4
```
