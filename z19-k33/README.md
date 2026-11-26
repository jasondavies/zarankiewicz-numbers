# The 19 × 19 Zarankiewicz number for $K_{3,3}$ is 164

A 19 × 19 binary matrix can have **164 ones** while avoiding an all-ones 3 × 3. Adding an eight-one row to the [second 156-one rectangle](../z18x19-k33/witness-156-min8.txt) gives the [164-one square](witness-164.txt). Each side has nine lines of degree eight, eight of degree nine and two of degree ten. Among the 969 triples of rows, 100 share no column, 322 share one, and 547 share two. The counts for triples of columns are the same.

For the upper bound, delete each of the nineteen rows in turn. Every resulting 18 × 19 rectangle contains at most 156 ones. Each entry of the square survives eighteen deletions, so a square of weight $w$ satisfies
$$
18w\le19\cdot156=2964,\qquad w\le164.
$$
Thus 165 ones force an all-ones 3 × 3. [Computer-assisted proof of the rectangular maximum](../z18x19-k33/README.md)

To check the witness against every triple in both orientations, run

```sh
python3 verify_exact.py
```

To also replay the rectangular upper bound, run

```sh
python3 ../z18x19-k33/verify_exact.py --jobs 8
```
