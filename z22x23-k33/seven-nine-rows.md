# Exactly six nine-rows are impossible at 217

Suppose a 217-one rectangle has exactly six nine-rows. The [six-row bound](six-nine-rows.md) leaves only columns of degrees eight, nine and ten. There are k eight-columns and 10+k ten-columns, with k equal to one or two. Counting relative to degree ten gives exactly three units of row surplus on the rows of degree eleven or more. The possibilities are one thirteen-row, one twelve-row and one eleven-row, or three eleven-rows.

Let m count the nine-rows on a ten-column. Each m is at least three. When k=2 the six nine-rows can provide at most 36 incidences on the twelve tens, so each m is three. When k=1 the unique eight-column meets a nine-row. This follows from its deletion leaving a square with an eight-row and from the full rectangle having no eight-row. That nine-row also needs at least three nine-columns, so it meets at most five tens. The other five nine-rows meet at most six tens each. Thus the total surplus E of the m above three on the eleven ten-columns is at most two. In particular m is at most five in either case. [Unique short row in the parent](README.md) · [Bounds on nine-rows](nine-rows.md)

On each ten-column, at least five of its ten rows have degree at least ten. The incident sum of row excesses above nine is at most eight, so the incident sum of positive excesses above ten is at most m−2. In particular a column with m=3 meeting a long row must contain exactly three nine-rows, six ten-rows and one eleven-row. [Ten-point bound](min9.md)

## The marked ten-column

Suppose there is another long row. It must be outside this mark. The twelve outside rows consist of three nines and nine rows of degree ten or more. Choose one outside long row and restrict it to eleven entries. Restrict the other eight outside high rows to ten entries each. All selected entries are on the 22 unmarked columns. The ten marked rows have loads 8,8,8,9,9,9,9,9,9,10 on those columns. A six-point block would include at least three ten-or-longer rows and need at least 57 entries against capacity 54. The canonical catalogue has 129,226 projections of the required type.

For each projection, generate all admissible eleven-subsets and ten-subsets. Each can meet the common support of every pair of fixed rows in at most two positions. Choose an eleven-subset and then eight distinct ten-subsets, checking every triple with the rows already placed. Distinct supports suffice since any two full rows share at most six entries. None of the 129,226 marks allows this partial placement. The positive control recovers one eleven-row and three ten-rows on a real projection and checks every resulting triple. Run `python3 verify_six_nines.py --jobs 4`. [Replay](verify_six_nines.py) · [Row placement](ten_column_rows.cpp)

## Finishing the count

If there are at least two long rows, all their incidences on ten-columns must now be on columns with m above three. Their total number is at most the sum of m−2 over those columns, which is at most 2E and hence at most four. But any two long rows have at least 22 entries counted with multiplicity. There are 13−k columns outside the tens, and the rows intersect in at most five positions for k=1 or six for k=2. Together they can therefore have at most seventeen entries outside the tens. They would need at least five on the tens.

If there is just one long row, it has degree thirteen. Each ten-column it meets needs m at least five. None qualifies at k=2, and the eleven columns outside the tens are insufficient. At k=1 at most one qualifies, so the thirteen-row must use all twelve columns outside the tens. Some ten-row avoids the eight-column, since there are fifteen ten-rows. Its incident excess on high columns is at most four, forcing at least six nine-columns, all shared with the thirteen-row. Two rows cannot share six positions when there is just one eight-column. [High-column weights and intersection bound](min9.md)

Consequently every 217-one rectangle has at least seven nine-rows. Deleting any yields 208 on 21 × 23. At least five of these deletions avoid all eight-columns and leave both a row minimum of nine and a column minimum of eight.
