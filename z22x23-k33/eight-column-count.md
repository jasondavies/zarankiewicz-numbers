# At most four columns can have degree eight at weight 217

Suppose five columns each contain eight ones. Deleting them leaves 177 ones on 22 × 18. If we instead delete any four of these columns, we get 185 ones on 22 × 19. Every row of this latter matrix has degree at least eight, since deleting a shorter row would exceed the [21 × 19 maximum of 177](../z19x21-k33/README.md).

Consequently every row of the 177-one matrix has degree at least seven. A row of degree seven must have contained **all five** deleted columns. Restoring any one of the five must raise its degree to at least eight. At most two rows can do this, since three such rows would share five columns.

On the other hand, 177 ones on 22 × 18 require at least three seven-rows under this minimum degree. If there are none, transpose and use the [177-one exclusion with minimum column degree eight on 18 × 22](../z21x23-k33/eight-columns.md). If there is one, deleting it and transposing gives 170 on 18 × 21 with minimum column degree eight, already excluded. If there are two, deleting both and transposing gives 163 on 18 × 20 with minimum column degree eight, also excluded. [170- and 163-one exclusions](../z20x21-k33/core-search.md)

Thus the number $k$ of eight-columns is between one and four, using the [lower bound on their number](min9.md). Removing all of them gives the following exhaustive targets. Every surviving column has degree at least nine. Every surviving row has at least eight ones, since deleting a row of the core leaves at most $209-8k$ at each of the four widths. These bounds are respectively 201, 193, 185 and 177. [Smaller maxima](../results-through-22.md)

| Eight-columns to add | Core dimensions | Required core weight |
|---:|---|---:|
| 1 | 22 × 22 | 209 |
| 2 | 22 × 21 | 201 |
| 3 | 22 × 20 | 193 |
| 4 | 22 × 19 | 185 |

Testing a core means finding $k$ eight-column supports that are admissible together with it. The row and column conditions above apply to the core before those columns are added.

The [subsequent exhaustive check](four-column-cover.md) excludes the last row of the table, leaving $k=1,2,3$.
