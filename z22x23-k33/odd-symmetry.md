# Restrictions on odd-prime symmetries at weight 217

A 217-one matrix on 22 × 23 avoiding an all-ones 3 × 3 cannot have a row-and-column automorphism of prime order five or greater. For order three, the fixed-row and fixed-column counts must be (4,2) or (4,5). The two cases are excluded by the [full order-three check](no-odd-symmetry.md).

Let p be an odd prime and suppose there are a moving row orbits and b moving column orbits. Both must be positive, since three identical lines of degree at least eight would give a forbidden submatrix. Write f=22−pa and g=23−pb. Every full row has degree at least eight. The one or two columns of degree eight must each be fixed, so all moving columns have degree at least nine. [Degree restrictions](README.md)

A moving orbit meets at most two opposite fixed lines. Three such lines would contain the entire orbit. Thus at least max(0,f−2b) fixed rows live entirely on the g fixed columns, with the analogous restriction on fixed columns. The moving submatrix contains at least max(6pa,7pb) entries, since each moving line loses at most two entries on restricting to moving positions.

For an upper bound U(m,n), start at mn, apply row and column deletion bounds recursively, and count triples in both directions. For example, on m rows of total weight w the sum of the binomial coefficients of order three of the row degrees is minimized when the degrees differ by at most one. This minimum cannot exceed twice the number of triples of columns.

On the fixed submatrix enumerate the row degrees d in decreasing order. If a row meets k moving orbits, its full degree is d+pk. Use the corresponding column test, requiring exactly one or two eights. Bound each prefix of s fixed lines by the corresponding U, and use the triple bound on these lines. Write h for the fixed submatrix weight and w,z for the numbers of incidences of fixed rows with moving column orbits and of fixed columns with moving row orbits respectively. Each such incidence represents p entries. If the moving submatrix has weight pv then

$$217=h+p(w+z+v),\qquad v+z\ge8a,\qquad v+w\ge9b.$$

Run `python3 odd_symmetry.py` to enumerate the integer possibilities. Only p=3 survives, with 25 aggregate profiles at (4,2) and 49 at (4,5). These are necessary conditions. A profile need not have a realizing matrix. Primes greater than 22 cannot move a row.

The (4,2) case is now excluded. The subsequent [five-fixed-column exhaustion](no-odd-symmetry.md) also excludes (4,5). [Exhaustion and replay](four-fixed-rows.md)
