# At most nine high-column entries on a row at 201

**In every 21 × 22 matrix of weight 201 avoiding an all-ones 3 × 3, each row meets at most nine columns of degree at least nine.** This applies to the 201-one rectangle in both surviving constructions for 217. [Reduction from 217](../z22x23-k33/last-profile.md)

Every column of the rectangle has at least eight ones by the bound of 193 on 21 × 21. Write q for the number with exactly eight and call the others high. We already know q is at least two. Removing the q columns leaves a matrix B with 21 rows, width 22−q, weight 201−8q and total column excess E = 3+q above nine. [Existence of two eight-columns](../z21-k33/eight-lines.md)

Two rows cannot share six high columns. The columns would contain at least 54 ones, whereas two rows covering them leave capacity only 50. Eleven high entries on a row are impossible by the twenty-block eleven-point lemma, since their point loads on the other twenty rows are all at least eight. Suppose a row meets ten high columns and mark them. Each of the twenty remaining rows gives a block of size at most five and two blocks share at most two points. Their total load is 80+H, where H is the sum of the marked columns' excesses above nine. [Eleven-point lemma](../z21-k33/README.md)

## Two or three eight-columns

The missing high columns avoid the marked row. For H at least two there are 159 projections, even allowing individual point loads through twenty. For H equal to one there are 5,487. Complete the high matrix using columns of degrees nine through 9+E−H, using H=2 as the lower bound for the first group. Distinct supports suffice since in the full 201 rectangle seven shared rows would need at least 56 entries against capacity 54. The minimum full row degree eight follows from the 20 × 22 upper bound of 193. [Deletion bounds](../z22x23-k33/eight-column-count.md)

If all ten-rows in B meet H=0, mark one of them. There are 79,801 projections with ten point loads of eight. The marked row maximizes Ed+H at 10E, with d its degree in B. Each nine-row or shorter row has H at most E. Enumerate all column profiles with squared excess between E and E² at that score bound. A minimum row degree of six suffices for the search. At q=3 it follows by removing a row of the 177-one matrix and using the maximum of 171 on 20 × 19. At q=2, restoring either eight-column gives a 193-one square with minimum degree eight, so every row of B actually has degree at least seven.

| Eight-columns removed | High matrix | Completions for H ≥ 2 | Completions for H = 1 | Completions in the H = 0 maximizing-row search |
|---:|---|---:|---:|---:|
| 2 | 185 on 21 × 20 | 0 | 0 | 0 across 558,607 marked profile tests |
| 3 | 177 on 21 × 19 | 1 | 0 | 0 across 877,811 marked profile tests |

The single 177-one completion accepts four individual eight-columns. The largest compatible subset has size two. Thus it cannot recover the required 201. In particular when q=3, removing the three eight-columns gives a 177-one parent whose 21 row degrees are all between six and nine. Their deficits below nine total twelve.

## Four or more eight-columns

For any projection the missing columns of degree ten or more must supply at least 7−H units of excess above nine, since E = 3+q. Generate their possible supports on the twenty unmarked rows. Each support must form an admissible triple with each pair of fixed columns. Two chosen columns share at most six rows, and every triple formed with an earlier column has intersection at most two. In decreasing order of excess, search for a compatible subset whose total excess reaches 7−H. This test allows any number of columns.

| Projection load | Surviving projections |
|---:|---:|
| 80 | 66 |
| 81 | 35 |
| 82 | 12 |
| Higher | 0 |

Starting from each of these 113 original projections, independently enumerate all 12−q missing high columns of degrees nine through twenty, at the required total weight 201−8q. Each of q = 4, 5, 6, 7, 8, 9, 10, 11 gives zero high matrices. At q=12 no high column would remain to supply the missing 15−H excess units, and q>12 leaves fewer than ten high columns in total. This exhausts q.

The full replay runs with `python3 verify_three_eights.py --jobs 4`. Use `--group 2`, `--group 3` or `--group 4+` for a single case. It includes recovery of an extremal 210-one square, a satisfiable excess test on the surviving 177-one matrix, and direct verification of its column extensions. [Excess search](high_column_gain.cpp) · [Replay](verify_three_eights.py)
