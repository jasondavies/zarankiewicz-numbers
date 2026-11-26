# Bounds for the 20 × 21 Zarankiewicz number for K₃,₃

**The remaining values are 185, 186 and 187.** Removing an eight-one row from the 193-one square gives the lower bound. We also classify the extremal 20 × 20 squares and restrict the possible column degrees at 187. [185-one matrix](witness-185.txt) · [193-one square](../z21-k33/README.md)

## Excluding 188

Assume a 188-one matrix exists. Any heavier example can be reduced to that weight. Every column has degree at least eight since the 20 × 20 maximum is 180. At least one column has degree eight by averaging. Deleting it leaves an extremal square, with nine ones in every row and column. [20 × 20 result](../z20-k33/README.md)

Mark the eight incident rows of the deleted column. On those eight points the twenty columns of the square give blocks. Each point has load nine, so the total is 72. Two blocks meet in at most two points, since the marked column forbids a common triple. Each block has size at most five. Six marked rows would have degree ten each in the full matrix. Two covering columns and nineteen others could supply at most $12+19\cdot2=50$ entries on those six rows.

The canonical generator finds just **one** such projection, even allowing loads above nine. The border checker fixes the eight full rows and tries the twelve missing rows of degree nine on the twenty unmarked columns. No completion attains 188.

## The unique extremal 20 × 20 square

Mark one row of a 9-regular 20 × 20 square. The other nineteen rows give blocks on nine points, with every point load eight and total load 72. The blocks have size at most five. Two rows sharing six columns would have to accommodate $6\cdot9=54$ ones there, while they and the other eighteen rows can supply at most $12+18\cdot2=48$. Any two blocks meet in at most two points.

There are 1,136 canonical projections at total 72. Fixing their marked columns leaves eleven columns of weight nine to choose on nineteen unmarked rows. Over all projections the border enumeration returns **one completion**. Distinct missing column supports suffice, since identical nine-columns already violate the six-row bound by transposition. Every extremal square has some marked representative in this enumeration. The cyclic witness therefore represents the unique square up to independent row and column permutations.

In each orientation that square accepts a line of weight four and none of weight five. The verifier tests the supports directly. A support is legal exactly when it meets the common support of every pair of existing lines in at most two positions. Thus the largest 20 × 21 matrix containing an intact 180-one square has 184 ones.

## Necessary conditions at 187

A 187-one matrix has no seven-column. Deleting one would leave the extremal square, which cannot accept seven. The short replay also checks this without the full square census. Mark a row incident to the proposed seven-column. Six further rows must join it. Any two of their blocks on the nine marked points must meet in at most one point, since the new column will also be shared. Among the 1,136 projections there are 43 ways of choosing the six blocks, before removing possible duplicates. Fixing the new column along with the nine marked columns leaves eleven columns of weight nine. All 43 fail.

Every column must consequently have at least eight entries. As $187<8+20\cdot9$, at least two columns have degree eight. Suppose there were exactly two. Removing them leaves 171 ones on 20 × 19 and every remaining column has degree nine. All core rows have degree at most nine. Otherwise ten marked entries would induce nineteen blocks of size at most five on ten points, each point of load eight and total at least 80. This catalogue is empty. The size bound follows from the same 54-versus-48 count.

At least eleven core rows have degree nine, since ten nines and ten eights would give only 170. A nine-row cannot meet either deleted column. If it did, seven further rows would join it and their blocks on the marked nine points would be pairwise intersecting in at most one point. The verifier checks that none of the 1,136 projections admits seven such blocks. Thus the two eight-columns would both lie within the other nine rows and would share at least seven. Every full row has degree at least eight since $z(19,21;3,3)\le\lfloor21\cdot171/20\rfloor=179$. Seven shared rows need at least 56 ones, but the two covering columns and the nineteen others supply at most 52. This contradiction forces **at least three eight-columns**.

Deleting any two of these columns leaves an extremal 171-one 20 × 19 core. Up to relabelling, it must differ from a column deletion of the cyclic 180-one square. For that deletion the only eight-one supports are the nine eight-subsets of the removed column, and no pair can be added together. The short replay tests this last extension directly. [19 × 20 result](../z19x20-k33/README.md)

An alternative starting point for the 187 search is to delete **three** eight-columns. This leaves 163 ones on 20 × 18. All remaining columns have degree at least eight. All core rows have degree at least seven, since deleting one leaves at most 156 on 19 × 18. If there were exactly three eight-columns originally, the remaining column degrees would be seventeen nines and one ten. Adding three jointly legal eight-columns to any such 163-one core would give a 187-one witness. [18 × 19 maximum](../z18x19-k33/README.md)

The core search narrows 187 to four column profiles. The number of eight-columns is between four and seven, every other column has degree nine or ten, and at most one row has degree eight. After deleting any three eight-columns, the 163-one core must have between one and six seven-rows. [Core bounds, profile restrictions and replay](core-search.md)

## Replay

The first command checks the bounds and the weight-187 restrictions. The second also enumerates all extremal 20 × 20 squares. Both use Python 3.10+, C++20 and nauty.

```sh
python3 verify_bounds.py
python3 verify_bounds.py --census --jobs 8
```
