# The two-column case needs an extremal matrix with maximum row extension eight

Deleting the two eight-columns and transposing gives 201 ones on 21 × 22. Suppose this matrix admitted any nine-row. Adding it would give the [unique 210-one square](../z22-k33/unique.md). Thus the core would be a nine-row deletion of that square, allowing both orientations.

The square has ten nine-rows in each orientation. In each of the twenty deletion tests, the admissible eight-rows are exactly the nine eight-subsets of the deleted row. No two can coexist, including two copies of the same support. The check tries every eight-subset of the 22 positions and checks every pair of admissible supports against the remaining rows. [Replay](verify_two_columns.py)

Consequently a 201-one core of any solution must admit two compatible eight-rows and have maximum admissible row size exactly eight. A larger admissible row would contain an admissible nine-row.

## An extremal square inside the core

At least one column of the transposed 201-one core has degree eight. To prove this, suppose all its rows and columns have degree at least nine. No two rows can share six columns. Six would need at least 54 entries, while the two rows and nineteen others can supply at most 50. A row with at least eleven entries would give twenty blocks of size at most five on eleven points, every point having load at least eight. The [eleven-point lemma](../z21-k33/README.md) excludes this. The 21 rows are therefore nine nines and twelve tens.

A column of core degree $t\ge11$ can have at most one unit of incident row excess above nine. This column is a row of the original rectangle and all its $t$ entries in the core are in columns originally of degree at least nine. It would require at least $t-1$ nine-rows in the core, exceeding nine. [High-column weight bound](min9.md) Thus the 22 columns have degrees nine and ten, exactly three having degree ten. Their thirty entries cannot all be in the nine nine-rows.

Mark a ten-row hitting as many ten-columns as possible. Marked point loads are eight or nine on twenty outside rows. If the mark meets two or more ten-columns, its total load is at least 82. All 149 projections with maximum point load nine give zero completions. Otherwise it meets exactly one ten-column and has load 81. Let $H$ count the ten-columns hit by a row. The mark maximizes $2d+H$ at 21, because a nine-row has $H\le3$. The same score equals $d+W$ with $W$ measured above baseline eight. Setting $Q=31$ forces precisely nineteen nines and three tens: this is the minimum sum of squared column excesses at total excess 25. All 5,487 load-81 projections with this score bound give zero completions.

Deleting an eight-column leaves an extremal 193-one square on 21 × 21. In particular any viable 201-one core has an extremal square parent on the smaller side. The stored [193-one witness](../z21-k33/witness-193.txt) has just one eight-column extension in each orientation. The resulting core admits nine individual eight-rows and no compatible pair. A solution therefore requires another extremal 193-one square up to row and column permutations and transposition. The same [replay](verify_two_columns.py) checks this witness and both marked catalogues.

The reduction to a 193-one square now holds for **every** extremal 201-one rectangle. It also applies in the one-column case if the 209-one parent has an eight-row. [Stronger proof](../z21x22-k33/smaller-parent.md)
