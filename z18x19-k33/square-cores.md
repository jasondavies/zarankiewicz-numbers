# Reducing 157 to two columns on a 143-one core

A 157-one matrix must have a seven-one column by the [first reduction](README.md). Removing it leaves a 150-one square. We enumerate the 150-one squares with minimum degree at least eight on **one** side and test all seven-one extensions, in both orientations.

## Choosing a marked row

Orient the square so all columns have degree at least eight. Every row has degree at least seven by the 17 × 18 maximum. The column excesses $e_j=c_j-8$ sum to six. Marking points in one row gives seventeen blocks on those points. Their sizes are at most five, since two rows sharing six columns would have to accommodate at least 48 ones on those columns, where at most 44 are possible. Point loads are the column degrees minus one, hence between seven and thirteen. As in the 18 × 18 proof, eleven marked points are impossible, and for ten marked points the catalogue with total load at least 70 has 978 entries.

If the maximum row degree is nine, let $x$ be the number of seven-rows. There are $H=6+x$ nine-rows and $L=12-x$ other rows. We claim that some nine-row meets columns of total excess at least two.

Suppose otherwise. Each nine-row meets at most one positive-excess column, and that column has excess one. If all six positive excesses equal one, the six nine-columns have at least $54-H=48-x$ incidences on the $L$ other rows. Add $x$ singleton rows to this submatrix. This would give at least 48 ones in a 12 × 6 matrix. Even 46 is impossible: balancing 46 incidences on twelve rows requires at least $10\binom43+2\binom33=42$ covered column triples, while the capacity is $2\binom63=40$.

Any column of excess at least two lies entirely among the $L$ other rows. There can be only one. Two columns of degree at least ten on at most twelve rows share at least eight rows, yet even seven common rows would require at least 49 ones against a capacity of $14+16\cdot2=46$. Write $a$ for the excess of the unique such column. Its degree $8+a\le12-x$ implies $2\le a\le4-x$ and $x\le2$. Two columns now cannot even share six rows: those rows have at least $48-x\ge46$ ones and can hold at most 44.

Each of the $6-a$ remaining nine-columns therefore meets at most five of the $8+a$ rows of the distinguished column. It must meet at least $9-5-(L-8-a)=a+x$ nine-rows. Their total capacity is $6+x$ under our supposition. But $(6-a)(a+x)>6+x$ for every integer $2\le a\le4-x$. This proves the claim.

Consequently the chosen nine-row has total load at least $9\cdot7+2=65$. There are 87,842 nine-point projections. Maximum row degree eight is impossible at weight 150.

## Exhausting extensions

On each projection the border checker enumerates every choice of the missing columns, whose degrees are between eight and fourteen. No two can be identical, since their degree would already force seven shared rows. For every resulting square, try all $\binom{18}{7}=31,824$ supports of a proposed column, then repeat on the transpose. A support is legal precisely when it intersects the common support of every pair of existing columns in at most two rows.

The 978 ten-point projections gave one completion. The 87,842 nine-point projections gave five completions before identifying possible isomorphisms. All six passed the independent square and weight checks. None accepted a seven-one extension in either orientation. Thus a putative 157-one matrix cannot have exactly one seven-column: deleting that column would leave a square whose other columns all have degree at least eight. It must have **at least two**. Deleting any two leaves a 143-one matrix on 18 × 17. Conversely, adding two jointly legal seven-columns to any such core gives 157. A degree-six row of that core must meet both new columns. Meeting neither would leave it with degree six. If it met just one, the final seven-row and that seven-column would be incident, which would leave 144 ones on 17 × 18 after deleting the pair.

From the 18 × 19 directory, replay the square search or test an individual core with

```sh
python3 verify_cores.py --jobs 6
python3 test_core.py ../z17x18-k33/witness-143.txt
```

The core checker accepts either orientation and prints the full 157-one witness if a pair succeeds.
