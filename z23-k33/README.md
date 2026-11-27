# The 23 × 23 Zarankiewicz number for K₃,₃ is 225

**The maximum is 225.** The [225-one matrix](witness-225.txt) has five lines of degree nine and eighteen of degree ten on each side. Deleting its last row gives the [216-one rectangle on 22 × 23](../z22x23-k33/witness-216.txt).

In the OEIS this gives a(23) = 225 in [A350304](https://oeis.org/A350304), 226 in [A001198](https://oeis.org/A001198), 304 in [A350237](https://oeis.org/A350237) and 303 in [A347473](https://oeis.org/A347473).

The exact rectangular value gives a short upper bound. Each entry survives 22 of the 23 single-row deletions, so a square of weight $w$ satisfies $22w\le23\cdot216$, or $w\le225$. [Proof that the rectangular maximum is 216](../z22x23-k33/exact.md)

The earlier square proof also works with the weaker rectangular bound. Deleting each row gives an upper bound of 226 from the [rectangular bound of 217](../z22x23-k33/218.md). At 226, local projections force a pair of rows or columns sharing six entries. The refined counts allow that pair in just one orientation, and transposition then excludes the final case. [Proof and replay for 226](exact.md) · [Marked-line restrictions](226.md) · [Earlier independent exclusion of 227](227.md)

## Construction

Start with the simultaneous row and column permutations preserving the known 210-one 22 × 22 square. A search with an extra fixed column and an order-20 subgroup found a 215-one 22 × 23 rectangle. Enumerating compatible additional rows found a ten-one row, giving 225. Removing a nine-one row instead yields 216 on the rectangle.

There is also a direct way to construct the square without a solver. Number rows and columns from one. The following two simultaneous permutations preserve the stored square. Omitted labels are fixed.

| Generator | Row cycles | Column cycles |
|---|---|---|
| A | (1 4 16 14 10)(2 22)(3 12 20 7 19 6 17 8 11 18)(9 13 21 15 23) | (1 21 9 6 2)(3 13 4 16 20 15 17 5 12 10)(7 18 14 11 22)(8 23) |
| B | (1 7)(2 5)(3 19)(4 8)(6 14)(9 23)(10 18)(11 17)(12 16)(13 15) | (1 12)(2 20)(3 6)(4 21)(5 15)(7 18)(8 19)(9 17)(10 16)(14 22) |

Place ones on the orbits of the following eight cells under A and B, and zeros elsewhere.

| Seed cell | (1,2) | (1,7) | (1,8) | (1,10) | (2,1) | (9,4) | (9,11) | (9,18) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Orbit size | 30 | 30 | 30 | 60 | 30 | 30 | 10 | 5 |

These disjoint orbits give 225 ones. Run `python3 construct.py` to print the binary matrix from the generators and seeds. [Construction script](construct.py)
