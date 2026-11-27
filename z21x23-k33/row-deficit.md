# A row-degree bound at 209 ones on 21 × 23

**Every admissible 209-one matrix has at least four units of row deficit below degree ten.** Equivalently its rows of degree above ten contribute at least three excess ones. This removes 74 more four-column starts from the cover and gives an additional necessary condition for starts 25, 46 and 62.

## Choosing a ten-column

Write $D=\sum_r(10-d_r)_+$ and $S=\sum_r(d_r-10)_+$. The weight identity gives $D=S+1$. Assume $D\le3$, so $S\le2$. Every row has degree between eight and twelve. The earlier reduction gives minimum column degree eight and at least four columns of degree eight. [Previous degree bounds](README.md)

No column can contain eleven rows. Mark eleven of its rows. The other 22 columns give blocks on the eleven marked points, with pairwise intersections of size at most two. Six marked rows need at least $60-D\ge57$ entries. If a second column contained all six, the two columns could supply twelve entries and the other 21 at most 42. Thus all blocks have size at most five. Their total size is at least $11\cdot9-D\ge96$. If two blocks have size at most four, discarding them leaves at least 88 incidences. Otherwise one can take twenty blocks of size five. Both possibilities contradict the eleven-point lemma for twenty blocks. [Eleven-point lemma](../z21-k33/README.md)

Consequently all columns have degree eight, nine or ten. The number of tens exceeds the number of eights by two, so there are at least six tens. Some ten-column carries at most two units of deficit. Otherwise $D=3$, and every ten-column contains all deficient rows. There are at least two such rows because each has degree at least eight. Five tens sharing those two rows need 50 incidences. The two rows can supply ten and the remaining nineteen at most 38.

## Exhausting the marked column

Mark the ten rows on the chosen ten-column. Let $d$ and $s$ be the deficit and excess on these rows alone. The other 22 columns induce blocks of size at most five by the same six-row bound. Their pairwise intersections have size at most two. The point loads are the ten full row degrees minus one, with total $90-d+s$. The eleven missing rows all avoid the mark. Two missing rows have distinct supports since seven shared columns of degree at least eight would need 56 entries against capacity $14+19\cdot2=52$.

| Excess on the mark | Deficit on the mark | Projections | Allowed missing row degrees | Completions to 209 |
|---:|---:|---:|---:|---:|
| 0 | 0 or 1 | 98 | 8–12 | 0 |
| 0 | 2 | 25,141 | 9–12 | 0 |
| 1 | 2 | 359 | 9–11 | 0 |
| 2 | 2 | 1 | 9–10 | 0 |

For $s=0$ generate all projections with loads from seven through nine and total at least 88, including families with no five-blocks. For $s>0$ the total is at least 89. Generating loads from seven through eleven gives 1,687 projections before filtering by $d\le2$ and $1\le s\le2$. Exactly the last two rows of the table survive. At most $3-d$ deficit units and $2-s$ excess units are available outside the mark. The border search excludes all 25,599 projections. This proves $D\ge4$.

## A smaller exhaustive cover

Consider a start with two rows $A,B$ common to the four marked eight-columns and three ordinary rows on a pair of the marks. Every ordinary row meets at most two marks and has at least eight entries in the 19 unmarked columns (the core). Let $p$ be the sum of the two central core degrees. Each core column meets at most two of the five rows on the marked pair, so $p+3\cdot8\le38$. Also $p\ge13$, since deleting $A,B$ from the 177-one core leaves at most 164 on the 19-square. Each central row has core degree at least six by the 171 bound on 19 × 20. [Five-row reduction](two-common-rows.md)

If the four marks were the only eight-columns, every ordinary row would have degree at most ten. Every longer row must meet at least three eights. The central rows have full degree at least ten, so all row excess would be $p-12\le2$, contradicting $S\ge3$. A fifth eight-column therefore exists.

Every core column contains at least $177-p-156=21-p\ge7$ ordinary rows, by deleting it from the ordinary 19-square. A fifth eight-column thus misses at least one of $A,B$. Replace any one mark by this column. The other three marks intersect precisely in $A,B$, so the new quartet has at most one common row. It is an eligible start because a central row of degree at least eleven contains the retained three marks. [18 × 19 bound](../z18x19-k33/README.md)

Of the 143 two-common-row starts, 20 with intersecting pairs of triples were already impossible. Of the other 123, exactly 75 have a triple on a pair. One of these is start 4, already proved impossible. The other 74 can all be omitted by the replacement above. An exhaustive cover now has **4,167 + 1,374 + 48 = 5,589 starts**. There are 21 individually excluded starts and 74 additional redundant starts.

For the 48 remaining starts one may assume every eight-column contains both common rows. Any other eight-column allows the same replacement, since at least one common row is long. There can be at most five eights under this assumption. Indeed each of the 19 ordinary rows meets at most two eights, and a row meeting $m$ eights contributes at most $2-m$ units of deficit. The common rows have degree at least ten. For $q$ eight-columns this gives $4\le D\le38-6q$. Hence $q$ is four or five. When $q=4$, each common row has degree at most twelve, so the two full degrees must be $(11,12)$ or $(12,12)$ to give $S\ge3$.

## The smaller rectangle forced by starts 25, 46 and 62

Permuting the marked columns gives each of these starts the five-row prefix and six side rows of start 4. In mask order 0, 1, 2, 3 the last ten row multiplicities are $(1+t,5-t,4-t,t)$ for $t=0,1,2,3$, corresponding to starts 4, 25, 46, 62. The side tests give the same 92 five-row templates. Of these, 86 have central core degrees $(6,7)$, three have $(6,8)$ and three have $(7,7)$.

The joint row search exhausts all four endings of the three $(7,7)$ templates. Templates 145, 151 and 152 have respectively 26, 540 and 6,680 placements of all six side rows. None completes. The replay uses the original single-ending enumeration as a control on these placement counts. [Search implementation](start4_search.cpp) · [Original row search and symmetry argument](start4.md)

Any completion at one of the three new starts therefore has a six-one central core row. Delete the four marked columns and this row, leaving 171 on 20 × 19. A fifth eight-column exists by the cover argument. After deleting the central row it contains at most eight ones. Deleting it leaves at least 163 on 20 × 18. The upper bound there is 163, so the extracted matrix has exactly 163 ones and the fifth eight-column missed the deleted row. Thus a 209-one example at any of these three starts would settle the smaller open value at its upper bound. [18 × 20 bounds](../z18x20-k33/README.md)

Independent completion attempts closed 59, 59 and 72 of the 92 templates for starts 25, 46 and 62 respectively. Each count includes 20 explicit empty clauses. The table records a single successful method per closed entry. The budgeted trials left 33, 33 and 20 open. The 5,589-start cover follows from the row-deficit argument alone. The 163-one implication additionally uses the three shared $(7,7)$ row searches. [Direct search table](shared-tail-search.tsv)

## Replay

Run from this directory with C++20, nauty and Python. The shared-tail replay also uses python-sat. The optional direct search regenerates and checks DRAT proofs using CaDiCaL and drat-trim. It can be restricted to one template with `--template`.

```sh
python3 verify_row_deficit.py --jobs 4
python3 verify_shared_tails.py
python3 verify_shared_tails.py --direct --solver /path/to/cadical --checker /path/to/drat-trim
```
