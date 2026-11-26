# The 20 × 20 Zarankiewicz number for K₃,₃ is 180

Index the rows and columns by the residues modulo 20. Let
$$
D=\{0,2,3,6,7,8,9,11,15\},\qquad X_{ij}=1\ \Longleftrightarrow\ j-i\pmod{20}\in D.
$$
Every row and column has nine ones, for a total of **180**. Intersecting every triple of rows gives at most two common columns. The verifier regenerates the matrix from $D$ and checks all 1,140 triples in each orientation. Removing its last row gives the 171-one witness on 19 × 20. [180-one witness](witness-180.txt) · [171-one rectangle](../z19x20-k33/witness-171.txt)

For the upper bound, delete each of the twenty rows in turn. Every rectangle that remains contains at most 171 ones. Every entry survives nineteen deletions, so a square of weight $w$ satisfies $19w\le20\cdot171=3420$, or $w\le180$. At equality every deletion must leave exactly 171 ones. Applying the same argument to columns shows that **every extremal square has nine ones in every row and every column**. [Rectangular upper bound](../z19x20-k33/README.md)

To check the construction, run

```sh
python3 verify_exact.py
```

To replay the rectangular upper bound as well, run

```sh
python3 ../z19x20-k33/verify_exact.py
```
