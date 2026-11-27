# At least six nine-rows at weight 217

Suppose a 22 × 23 matrix has 217 ones and avoids an all-ones 3 × 3. Its minimum row degree is nine. Write k for its number of eight-columns, which is one or two. Every eight-column meets at most one nine-row. On a nine-row that hits an eight-column, at least 4−k other positions are on nine-columns. These facts follow by deleting an eight-column, then a short row of the resulting square. [Nine-row incidence bounds](nine-rows.md)

## Three projection tests

For a marked row or column, restrict the other parallel lines to its support. Two restricted lines meet in at most two points. Point loads are the corresponding full perpendicular degrees minus one. Each remaining perpendicular line avoids the marked line. The three searches below enumerate these missing lines using the original triple condition, distinct supports and total weight 217.

| Mark | Projection on the other parallel lines | Marks tested | Completions |
|---|---|---:|---:|
| Eight-column with incident row degrees summing to at least 84 | 8 points, 22 blocks, minimum load 8 and at most one load 8 | 900 | 0 |
| Ten-column meeting two nine-rows and eight ten-rows | 10 points, 22 blocks, loads two eights and eight nines | 23,526 | 0 |
| Nine-row avoiding the eight-columns, incident excess above nine equal to seven | 9 points, 21 blocks, minimum load 8 and total load 79 | 15,766 | 0 |

All three marks have block size at most five. In the first two, six common rows would require at least 58 entries, but two columns containing them and the 21 other columns can supply at most 54. In the third, six marked columns have degree at least nine and need 54 entries, against capacity 52. Distinct missing row supports suffice because two rows cannot share seven columns. Two columns cannot share seven rows either. For the first two searches a full row has at most thirteen entries in columns of degree at least nine, since each such entry contributes at least eight incidences on the 21 outside rows and each outside row can share at most five such positions. Thus the row degree is at most fifteen. In the last search a column of degree c receives at least 8c outside incidences from its rows, while the other 22 columns share at most six rows each. Hence c is at most sixteen.

The nine-point generator enumerates all five-block families, including the empty one, and completes each by four-blocks and smaller blocks. Among the 15,766 marks are 881 with exactly seven degree-ten and two degree-nine columns. The full test also includes longer columns. Run `python3 verify_217_loads.py --jobs 4`. [Replay](verify_217_loads.py)

## Counting nine-rows

It follows that every eight-column has total incident row degree at most 83. Every ten-column must meet at least three nine-rows. Indeed, when it meets at most two, the earlier ten-point weight bound forces exactly two nine-rows and eight ten-rows, now excluded. Every nine-row avoiding low columns has incident excess at most six, since larger excesses above seven were previously excluded. Each nine-row therefore meets at most six columns of degree ten or more. For a row hitting an eight-column, the bound follows from its 4−k necessary nine-columns. [Earlier excess bounds](min9.md)

Suppose there were at most five nine-rows. No column could have degree at least eleven, since it would contain at least six entries on ten-or-longer rows, violating the earlier eleven-point restriction. The entire column profile then consists of eights, nines and precisely 10+k tens. The tens need at least 3(10+k) incidences with nine-rows, while at most five such rows provide at most thirty. This proves the assertion. In particular any 217-one matrix gives at least six deletions to 208 on 21 × 23. At most k of these nine-rows can hit a low column, so at least four deletions produce an extremal 208-one parent with **minimum row degree nine and minimum column degree eight**.

If there are exactly six nine-rows, all high columns have degree ten. A column of degree at least eleven needs at least c−5 nine-rows, so its degree could only be eleven and it would contain all six. There cannot be three such columns. If there were two, the six rows shared by them have total degree 54. Every other column must contain exactly two of the six to achieve that sum, contradicting the three needed by each ten-column. At least one ten-column would exist by the total weight. With exactly one eleven-column there are 8+k ten-columns. Each nine-row avoiding low columns could meet at most four tens, since it already spends two units of excess on the eleven-column. Each nine-row hitting a low could meet at most 3+k tens, by its required nine-columns and the eleven-column. Across six nine-rows the upper bounds are 24 at k=1 and 26 at k=2, less than 3(8+k) in each case.
