# The 209-one parent with every line of degree at least nine

Suppose a 217-one rectangle has just one eight-column. Delete it, obtaining a 209-one square with all columns of degree at least nine. In this note assume that all its rows also have degree at least nine. The only remaining possibilities for the row degrees and column degrees are the same on both sides:

* eleven nines and eleven tens;
* twelve nines, nine tens and one eleven. In this case the eleven-row contains exactly one ten-column, and the eleven-column contains exactly one ten-row.

The case with an eight-row in the square is separate.

## Local restrictions in the square

Any pair of rows meets in at most five columns. Six would require at least 54 incidences on those columns, against a capacity of 12 on the pair and 40 elsewhere. The argument also applies to columns. Thus a degree-$d$ row has $8d\le21\cdot5$ and $d\le13$.

Assign each column its excess over nine, and let $W$ sum the incident excess on a given row. In an extendable parent, $W\le7$ on a nine-row, $W\le4$ on a ten-row, and $W\le1$ on a longer row. These bounds also hold for columns, whether the extension is by a row or a column. To verify this symmetric assertion, use the nine-, ten- and eleven-point marks from the [217 projection argument](min9.md), this time completing to a **square of weight 209**. A mark violating a bound contains nine, ten or eleven points of total load at least 80, 85 or 90 on the remaining 21 lines. On a longer row choose the eleven heaviest columns. No missing column can pass through the marked row: it would need eight other blocks meeting pairwise in at most one point. For the remaining columns enumerate all distinct supports of size 9 through 13, all avoiding the marked row. Repeated columns are impossible by the pair-intersection bound.

| Mark | Projections | Marked completions with both minima at least nine | Admit an extra eight-row or eight-column |
|---|---:|---:|---:|
| 9 | 234 | 0 | 0 |
| 10 | 13,205 | 35 | 0 |
| 11 | 338 | 0 | 0 |

## Counting the degree profiles

On each side the excess over nine sums to eleven. Each long line of degree $d$ contains at least $d-1$ nine-lines. These required subsets for any two long lines meet in at most five. The total incident excess is at most the sum of the line bounds. These tests leave 21 unordered profile pairs.

For each degree, count lines by their numbers of incidences in the opposite degree classes. Enforce the line bounds and agreement on each degree-class incidence total. Each pair of lines occurs together at most five times and each triple at most twice. For any fixed pair of columns, summing $d-2$ over rows of degree $d$ containing the pair gives at most 40, since each of the other twenty columns contributes at most twice. Impose the same bounds in the other orientation. Seventeen of the 21 integer systems are infeasible. The four survivors have identical profiles on both sides: the all-nine-or-ten profile, or one line of degree $d\in\{11,12,13\}$ with $d+1$ nines and $20-d$ tens.

## Excluding degrees twelve and thirteen

Let $R,C$ be the unique long row and column. They miss each other since their weight bounds are one. At most two of the $d+1$ nine-columns lie outside $R$. A ten-row hitting $C$ would spend $d-9$ units of its weight allowance of four there. It could meet at most $13-d$ ten-columns and would require at least $d-4$ nine-columns. At most five of those nine-columns lie on $R$, so it can reach at most seven. This rules out the hit for $d\ge12$. By transposition, $R$ also misses the ten-columns.

There is now just one nine-column outside $R$. Every ten-row needs at least six nine-columns, so it contains that outside column. Dually all ten-columns contain the unique nine-row $r$ outside $C$. For $d=12$ these eight ten-columns give $r$ weight at least eight, exceeding its allowance of seven. For $d=13$ they occupy seven cells of $r$, leaving at most two on $R$. The columns of $R$ need $13\cdot8=104$ further incidences. The other rows supply at most $2+20\cdot5=102$.

For $d=11$, if $R$ misses all ten-columns, only one nine-column lies outside it. Any ten-row hitting $C$ needs at least seven nine-columns and can reach at most six. So $C$ misses all ten-rows as well. As before, all nine ten-columns would then contain the single nine-row outside $C$, exceeding its weight allowance. Hence each long line meets exactly one ten-line.

Run `python3 verify_square_parent.py` to regenerate the marks, check extension in both orientations, and certify the 17 infeasible integer systems. [Replay](verify_square_parent.py)

The eleven-line alternative has since been excluded on all 36,171 projections. [Final profile reduction](last-profile.md)
