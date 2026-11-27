# Quick bounds on 23 × 24 and 24 × 24

For matrices avoiding an all-ones 3 × 3, the bounds from this check are **230–234 on 23 × 24** and **240–243 on 24 × 24**.

Index both coordinates modulo 24. In row $i$, put ones at $i+S$ for $S=\{0,1,2,3,5,8,11,13,17,18\}$. This gives 240 ones. Every triple of rows intersects in at most two columns. Removing any row gives 230.

## Rectangle

Delete each column in turn. Every entry survives 23 deletions, giving $23w\le24\cdot225$ by the [23 × 23 result](../z23-k33/README.md). At weight 234 every column has degree at least nine. At least six have degree nine, since 24 tens would give 240. Deleting any of those columns gives an extremal 225-one square. In both orientations of the stored square, exactly one extension has size five, and none has size six. Every larger extension would contain a six-subset. A 234-one rectangle therefore requires a different 225-one square, even allowing row and column permutations and transposition.

## Square

A square with more than 240 ones has a row of degree at least eleven. Suppose all columns have degree at least ten, and mark eleven columns on that row. Each other row restricts to a block of size at most five. Indeed six common columns would require 60 ones, whereas the two rows and all 22 remaining rows could supply at most $12+22\cdot2=56$ on those columns. Two blocks intersect in at most two points, since three rows share at most two columns. Each marked point occurs in at least nine of the 23 blocks, so their total size is at least 99.

Let $m$ and $q$ count the five-blocks and four-blocks. Then $99\le92+m$ and $99\le69+2m+q$. Enumerate the 21 compatible five-block families on eleven points with $m\ge7$, up to relabelling. Only families with $m=7$ admit the required $30-2m$ compatible four-blocks. In this case all 23 blocks are specified. Among the 18 selections examined for these family representatives, thirteen have minimum point load eight and five have minimum seven. None reaches the required nine.

Hence every square above 240 has a column of degree at most nine and, by transposition, a row of degree at most nine. Deleting one gives
$$
z(24,24)\le \max\{240,z(23,24)+9\}\le243.
$$

Run `python3 verify_bounds.py` in this directory with C++20 and nauty installed. The replay checks the cyclic construction, the extensions of the stored square, and the eleven-point obstruction. [Verifier](verify_bounds.py)
