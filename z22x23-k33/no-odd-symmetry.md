# Every automorphism group at weight 217 on 22 × 23 is a 2-group

Suppose a 22 × 23 binary matrix has 217 ones and no all-ones 3 × 3. Its group of simultaneous row and column permutations has order a power of two, possibly one. The prime-order argument excludes primes at least five. The first order-three exhaustion excludes four fixed rows and two fixed columns. This leaves four fixed rows and five fixed columns, which we exclude below. The conclusion then follows from Cauchy's theorem. [Prime-order reduction](odd-symmetry.md) · [Two fixed columns](four-fixed-rows.md)

## Enumerating the fixed rows and columns

There are six moving row orbits and six moving column orbits, all of length three. Each moving line has degree at least nine since there are at most two eight-rows and at most two eight-columns. A fixed line meets an opposite moving orbit in all three positions or none. Each orbit can consequently touch at most two fixed lines.

Two fixed rows cannot both touch the same two moving column orbits. Six common moving columns would require at least 54 entries, while the two rows supply twelve and the twenty others at most forty. Two fixed columns cannot both touch the same two moving row orbits either. The six common moving rows need at least 54 entries. The two columns supply twelve and the other 21 can supply at most 42. This forces every other column to meet exactly two of the six rows. A third fixed column meets those rows in a multiple of three.

First enumerate the fixed 4 × 5 corner up to permuting its rows and columns. Its weight is 1 modulo 3. For each orientation, enumerate the six sets of fixed neighbours of the moving orbits as a multiset. Every set has size at most two and the pairs are distinct by the preceding argument. The full degrees of fixed lines are their corner degrees plus three times the numbers of incident moving orbits. The checker enforces the degree minima, counts of degree-eight lines, minimum row degree eight after deleting the eight-columns, and the known upper bounds after deleting any subsets of fixed rows and fixed columns. The 18 × 18 moving submatrix has weight at most 150.

For each pair of fixed rows, let S be their shared fixed columns together with the three columns of a common moving orbit if that orbit exists. The sum of degrees on S is at most 2|S|+40, since every other row contributes at most two. Likewise two columns share at most six rows, since seven rows need at least 56 entries while the two columns and the other 21 supply at most 56, with equality requiring all seven rows to have degree eight. At most two such rows exist. Two eight-columns share at most five rows. Canonicalizing the two strip multisets under permutations preserving the corner leaves 222,504 configurations. [Degree and deletion bounds](README.md) · [Two eight-columns](short-overlap.md)

## From block sizes to actual entries

The moving submatrix is a 6 × 6 array of 3 × 3 circulants. Each has row sum zero, one or two. The word-domain, pair and triple tests used in the two-fixed-column proof apply here as well. They retain 48 fixed configurations and 515 block-size arrays. For each array we enumerate all relative cyclic shifts. In a size-one block the first row is a rotation of 001, and in a size-two block it is a rotation of 110. The next two rows use the successive rotations.

Place the six row orbits in order. Independent rotations on previously unused column orbits normalize the first nonempty block on each. Rotating the new row orbit also normalizes one block in an already used column orbit, if any. Try every phase on the other shared blocks. On adding an orbit, check all triples of new and old rows. The old rows form an invariant set, so it suffices to fix the new representative when there is one new row, or the pair of new representatives when there are two. The three new rows themselves must also meet in at most two columns. All 515 arrays fail, after 119,025 nonterminal phase-search nodes. As a positive control the same search reconstructs a complete 216-one matrix, which is checked by counting entries and intersecting every row triple.

Run the following two commands with NumPy and a C++20 compiler. Each regenerates its input. [Five fixed columns replay](verify_five_fixed_columns.py) · [Block and phase checker](order_three_blocks.hpp)

```sh
python3 verify_order_three.py --jobs 4
python3 verify_five_fixed_columns.py --jobs 4
```
