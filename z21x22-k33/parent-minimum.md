# Every 201-one extremal matrix on 21 × 22 has row minimum nine

An eight-row in a 201-one matrix would leave 193 ones on 20 × 22, with at least two further eight-rows. Delete all three to obtain 177 on 18 × 22. The columns there have degree at least seven by the 18 × 21 bound. At least three have degree seven, since deleting zero, one or two seven-columns would otherwise give 177, 170 or 163 on eighteen rows with minimum column degree eight. All three cases were previously excluded. [Two eight-rows at 193](../z22x23-k33/short-rows.md) · [Eighteen-row exclusions](../z21x23-k33/eight-columns.md)

Restore any one of the three removed rows. The result has 185 ones on 19 × 22, so every column has degree at least eight by the 19 × 21 maximum of 177. Each restored row must therefore hit all the seven-columns. This puts an all-ones 3 × 3 on the three removed rows. A row smaller than eight is impossible by the 193 upper bound on 20 × 22. Thus every row has degree at least nine, and averaging forces equality somewhere. In particular the bound 2t+H at most 21 on the high columns holds for every row of every such rectangle. [Incident excess bounds](row-excess.md)

## Consequence on 20 × 23

At 201 on 20 × 23 every row would have degree at least nine by the upper bound of 192 on 19 × 23. At least nine columns would have degree eight. Deleting any such column leaves a 193-one 20 × 22 matrix with at least two eight-rows, so each eight-column must contain at least two nine-rows. A nine-row can meet at most one eight-column, since deleting two of them leaves 185 on 20 × 21 whose rows have degree at least eight. At least eighteen of the twenty rows must therefore be nines. [Column bound](../z22x23-k33/eight-low-columns.md) · [19 × 23 bound](../z21x23-k33/eight-columns.md)

After deleting an eight-column a row of degree d in the remaining matrix needs at least 7d incidences on its columns among the nineteen other rows. No pair of rows can share seven columns, so 7d is at most 114 and d is at most sixteen. In the full 20 × 23 matrix every row therefore has degree at most seventeen. Even eighteen nines and two seventeens have only 196 entries. This proves the upper bound 200.
