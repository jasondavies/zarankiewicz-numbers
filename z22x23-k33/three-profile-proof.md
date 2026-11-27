# Degree profiles of the 193-one core

Work with the transposed 20 × 22 core of a putative 217-one rectangle having exactly three eight-columns. Its row degrees $d$ are at least nine and its column degrees $t$ are at least eight. On a row let $W$ be the sum of the incident column excesses $e=t-8$. The [projection proof](three-columns.md) gives peak $d+W=18$, with $W\le6$ for degrees at least eleven and $W\le4$ for degrees at least twelve. Write $Q=\sum e^2\le31$.

There are at most twelve eight-columns in the core. Their number is $5+\sum_{e>0}(e-1)$, and $Q\ge17+2\sum_{e>0}(e-1)$. A fourteen-row needs at least three blocks of size six in its projection since $14\cdot7>19\cdot5+2$. All three consist of eight-columns, and their union has size at least twelve. This forces twelve eight-columns and $Q=31$. But then the sum of the scores is $193+8\cdot17+31=360$, requiring every row to score eighteen, already excluded for a fourteen-row. A fifteen-row would require at least ten six-blocks on at most twelve points. Their sixty incidences would cover at least $12\binom52=120$ pairs of blocks, above $2\binom{10}2=90$. Larger degrees have already been excluded. Thus $d\le13$.

On a core column of degree $t$, sum the incident row excesses $d-9$. This column represents a row of the full rectangle with $t$ ones on its high columns. The bounds on the sum are $7,4,1$ for $t=9,10,\ge11$, respectively. At $t=8$ the bound is ten because the other 21 full rows in the eight-point projection cannot have total load 75. At 75 they use at least 57 triples, above the 56 available. [Full-rectangle restrictions](min9.md)

Suppose no ten-row scores eighteen. Its incident weight is then at most seven. Enumerate partitions of the 13 row excesses and 17 column excesses, with the row ceilings above and $Q\le31$. The total slack below score eighteen is $31-Q$. Columns of degree at least eleven require $t-1$ nine-rows each and any two columns share at most five rows. These elementary filters leave 302 profile pairs.

For each pair, count row and column signatures by their incidences with the opposite degree classes. The counts in each class sum to its multiplicity, and both signatures must give the same number of cells between each pair of degree classes. For each triple of types, its occurrences cannot exceed twice the number of triples of distinct lines of these types. Two columns share at most five rows, and two rows share at most six columns. Over the rows shared by any pair of columns the sum of $d-2$ is at most 40, since each of the other twenty columns meets the pair in at most two rows. The corresponding bound for a pair of rows is 36. The integer checker independently certifies 298 infeasible systems. [Profile replay](verify_three_profiles.py) · [Integer certificate checker](../z23-k33/verify_linear.py)

| Row counts at degrees 9, 10, 11 | Column counts at degrees 8, 9, 10 | Slack below the sum of the individual score ceilings |
|---|---|---:|
| 7, 13, 0 | 5, 17, 0 | 1 |
| 8, 11, 1 | 6, 15, 1 | 0 |
| 9, 9, 2 | 6, 15, 1 | 1 |
| 10, 7, 3 | 7, 13, 2 | 0 |

The score ceilings here are eighteen on a nine-row and seventeen on the other two degrees. In the first profile some nine-row scores eighteen and all nine of its columns have degree nine. In each of the other profiles an eleven-row attains $W=6$. Such a row maximizes $2d+W$ at 28, since nine- and ten-rows reach at most 27.

None of these latter three profiles permits two rows to share six columns. Such a pair would share six eight-columns, and each other row would meet exactly two of those six. At least seven nine-rows attain $W=9$ in each profile. For such a nine-row the number of eight-columns it meets equals its number of ten-columns. In the one-ten-column profiles, such a row outside the sharing pair could not meet two eight-columns. In the two-ten-column profile all ten nine-rows attain the ceiling. At least eight outside the pair would have to meet both ten-columns, which can share at most five rows.

The eleven-row therefore has a projection on eleven points of load 83 with blocks of size at most five. There are 144 such projections. None completes at peak $2d+W=28$ with $Q\le21$. The first profile requires one of 1,136 nine-row projections with all point loads eight. Together with the 14,736 ten-row marks at score eighteen, these smaller lists cover every candidate.


## The five eight-columns in the first profile

The thirteen ten-rows each meet at least three of the five eight-columns, since each row has weight at most seven on the seventeen nine-columns. The eight-columns carry forty entries, only one more than $13\cdot3$. Thus across the seven nine-rows there is at most one incidence with those columns. Choose an eight-column whose eight entries all lie on ten-rows.

Mark those eight rows. Every marked point occurs nine times among the other 21 columns. No two rows share six columns, since a pair sharing six would force six eight-columns and there are only five. On the mark each pair of points can therefore occur in at most four other columns. Out of 326,456 eight-point projections of load at least 72 there are 627 with the required point loads and pair counts. Each block of the projection has size at most five, since two columns sharing six rows would need at least 54 entries against capacity 52.

Choose which four of the 21 unmarked columns are the remaining eight-columns. Each marked ten-row meets two or three of these four, and their total incidences with the mark are at most seventeen. Over all 627 projections there are 2,143 such choices. The five outside ten-rows avoid the mark and must each use at least three of the four chosen columns. Exhaust all ten-subsets of the 21 unmarked positions compatible with each pair of fixed rows, then choose distinct supports, checking triple intersections after each addition. Even four outside ten-rows cannot coexist for any choice. A positive control recovers three together and independently checks both orientations. [Support search](five_tens.cpp)

Finally the search over the 14,736 maximizing ten-row projections of load 78, with minimum core row degree nine and $Q\le31$, gives **zero cores**. This excludes the three-eight-column case. The profile and column replays together perform all the checks, including a reconstructed 185-one positive control.

Install the [profile replay dependencies](../README.md#replaying-the-proofs) first. From this directory with the environment active, the first command checks all 302 degree-profile pairs and certifies 298 exclusions. The second checks the column cases.

```sh
python3 verify_three_profiles.py
python3 verify_three_columns.py --jobs 4 --cache /tmp/z193-three
```
