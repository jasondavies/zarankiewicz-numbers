# A 193-one matrix on 20 × 22 has at least two eight-rows

Suppose all twenty rows have degree at least nine. Let q be the number of eight-columns. We have q at least eight. Write the other column degrees as 9+h. Their h sum to q−5. On a row let d be its degree, l its number of eight-columns, H its incident sum of h, and W its incident sum of column excesses above eight. Then W=d−l+H. [Eight-column lower bound](eight-low-columns.md)

The following earlier marked-row bounds use only the dimensions, weight and the row and column minima of nine and eight. The peak of d+W is eighteen. The exhaustive 14,736 ten-row marks show that a ten-row has W at most seven. At degrees eleven, twelve and thirteen the bounds are six, four and four. The argument excluding degrees fourteen and above uses the peak score, the column excess and the number of six-point blocks. All these tests precede the use of an embedding in a larger rectangle. [Projection bounds and peak](three-columns.md) · [Degree bound and ten-row replay](three-profile-proof.md)

Let a,b,c count rows of degrees 11,12,13. A nine-row has l at least H. At degrees 10,11,12,13 the lower bounds on l−H are respectively 3,5,8,9. Relative to three times the row surplus d−9, this saves at most 0,1,1,3 incidences respectively. The total surplus is thirteen. Summing H over all rows gives 9(q−5) plus the sum of the squared h. Hence
$$
a+b+3c\ \ge\ q-6+\sum h^2\ \ge\ 2q-11,
\qquad 2a+3b+4c\le13 .
$$
In particular the left side is at most nine. Two rows cannot share seven columns, since the two rows and the other eighteen can supply at most fifty entries where the columns need at least 56.

* At q at least eleven the required saving exceeds nine.
* At q=10 only three thirteen-rows could save nine. Two of these already meet at least eight of the same ten low columns.
* At q=9 the required saving is at least seven, so a thirteen-row exists. It contains all nine low columns, ruling out any further thirteen-row or twelve-row. At least four eleven-rows remain. Each meets at least five low columns, and any two meet there at most twice because of the thirteen-row. Their twenty or more incidences on nine columns require at least thirteen pair occurrences by convexity, exceeding the allowed twelve.
* At q=8 there is no thirteen-row. A twelve-row would contain all eight low columns. There could be only one, and the five or more low columns on each eleven-row would then intersect pairwise in at most two. The complementary sets within the eight would have to be disjoint triples whenever two occur, so at most two eleven-rows could coexist. This falls short of the required saving of five.

At q=8 we therefore have only nine-, ten- and eleven-rows, with five or six elevens. The h sum to three. If any h exceeds one then their squares sum to at least five, requiring at least seven elevens. Thus the profile is eight eights, eleven nines and three tens, with squared excess above eight equal to 23. The low-incidence inequality has slack at most one. Some eleven-row attains W=6. No two rows can share six columns. Those columns would all be eights and each other row would have to meet exactly two of them, whereas any eleven-row outside the pair would meet at least three. The marked eleven-row maximizes 2d+W at 28. Its eleven-point projection on the nineteen outside rows has load 83 and block sizes at most five. There are 131 compatible marks and none completes to 193. Run `python3 verify_short_rows.py`. [Replay](verify_short_rows.py)

This proves the existence of an eight-row. Deleting one gives 185 on 19 × 22, which itself has an eight-row. Thus there are at least two. [185-one obstruction](four-column-cover.md)
