# The 22 × 22 Zarankiewicz number for K₃,₃ is 210

The [210-one matrix](witness-210.txt) is obtained by appending a nine-one row to the [201-one rectangle](../z21x22-k33/witness-201.txt). Every triple of rows has at most two common columns.

For the upper bound, delete each of the 22 rows in turn. Each one survives 21 deletions, and every resulting rectangle has at most 201 ones. Thus a square of weight w satisfies 21w ≤ 22 · 201, giving w ≤ 210. [Proof of the rectangular bound and joint replay](../z21x22-k33/README.md)

The extremal square is unique up to row and column permutations. It admits no seven-one extension on either side. [Classification proof and replay](unique.md)
