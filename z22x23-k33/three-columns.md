# A six-column intersection in the three-column case

If a 217-one matrix has exactly three eight-columns, deleting them and transposing leaves 193 ones on 20 × 22. The twenty rows have degree at least nine and the twenty-two columns have degree at least eight. Let $d_R$ be a row degree and $W_R$ the sum, on its support, of the column excesses above eight. These excesses sum to seventeen, so
$$
\sum_R(d_R+W_R)=193+8\cdot17+\sum_j e_j^2\ge346.
$$
Some row therefore scores at least eighteen.

Suppose rows $R,S$ share six columns. Those columns need at least 48 ones. The two rows provide twelve and each of the other eighteen rows can provide at most two. All six columns therefore have degree eight, every other row meets exactly two of them, and $R,S$ cannot share a seventh. Deleting both rows and all six columns leaves $157-d_R-d_S$ ones on 18 × 16. Since the [maximum is 137](../z16x18-k33/README.md), $d_R+d_S\ge20$.

View each of the eighteen other rows as an edge on the six shared columns, joining the two it meets. Multiple edges are allowed. Take any two columns of $R$ outside the shared six. The edges of rows covering both form a matching. If two edges shared a vertex, the two corresponding rows and $R$ would share three columns. Hence every pair of outside columns occurs together at most three times among the eighteen rows.

If $d_R=9$, the three outside columns have total load $21+W_R$ on those rows. Each row with $x$ outside entries contributes at least $x-1$ pairs and all pairs together can occur at most nine times. Thus $21+W_R-18\le9$, or **$W_R\le6$**. In particular a nine-row attaining score eighteen cannot share six columns with any other row.

If $d_R=10$, the four outside columns have load $28+W_R$. Their six pairs occur at most eighteen times, giving **$W_R\le8$**. At equality the total load is 36. Every one of the eighteen rows covers exactly two outside columns, since any unequal distribution with mean two uses more than eighteen pairs. Each of the six pairs of outside columns occurs three times and gives a perfect matching on the six shared columns. Each outside column belongs to three pairs, so all four have degree ten.

These are restrictions on candidate 193-one cores. The [degree-profile proof](three-profile-proof.md) completes this case.

The three perfect matchings on the six vertices associated with pairs containing a given outside column must be edge-disjoint. Otherwise two of the eighteen rows share the same edge and an outside column. Fix the matchings of the first two pairs sharing an outside column. Any ordered pair of disjoint perfect matchings is equivalent under permutation of the six vertices because its union is an alternating six-cycle. This leaves 82 assignments to test. **None completes to 193.** The missing twelve columns have degree at least eight and at most seventeen, since the ten marked columns already use eight of the seventeen units of excess. Distinct supports suffice since two columns sharing six rows would require at least 54 entries against a capacity of 52. Thus a maximizing nine- or ten-row of score at least eighteen has no six-block in its projection.

## Eleven marked points

Choose eleven columns of a row. If their weight is at least seven, their projection has load at least 84. The [nineteen-block catalogue](../z20x21-k33/rare-rows.md) excludes this whenever the largest block has size at most five. A block of size seven is impossible by the six-column count. Suppose there is a six-block. Relative to its six vertices there are five outside points. The eighteen other rows cover each outside pair at most three times, so there are at most thirty pair occurrences. A load of at least 42 on those five points requires at least thirty pairs. Equality forces twelve two-point blocks and six three-point blocks on the outside points. Every outside pair occurs three times, as a perfect matching of the six vertices.

At a fixed vertex, six of the eighteen rows are incident. Their outside subsets contain each of the ten outside pairs exactly once, by the matching property. Exactly two of the six subsets must be triples, since $3x+(6-x)=10$. The two triples meet in exactly one point. The other four subsets are the uncovered pairs. This gives fifteen possible types for each vertex.

Enumerate the six vertex types as an unordered multiset. A triple that occurs must occur at exactly two vertices, as it belongs to a single row joining those vertices. For each remaining pair, match the vertices where it occurs. Retain the minimum point load seven. There are 150 eligible multisets and 6,930 matching assignments. Every assignment has two projected rows sharing at least three points. **No eleven-point projection of load 84 exists even allowing a six-block.**

Consequently every core row with at least eleven entries has $W_R\le6$. If it had seven units, its eleven heaviest columns would retain at least seven. The subsequent profile calculation handles the other marked projections. Run `python3 verify_three_columns.py` to replay these two exclusions.

## A nine-row or a ten-row suffices

Every row of degree at least twelve has $W_R\le4$. Otherwise choose twelve columns capturing at least five units. Each block of size six on these points consists entirely of zero-excess columns. Any three such blocks have union of size at least $18-3\cdot2=12$, whereas at least one of the twelve points has positive excess. Thus there are at most two six-blocks. If there are two they share a zero-excess point since their union has size at most eleven. Drop a zero-excess point meeting each six-block, or a lowest-weight point if there is no six-block. The eleven retained points still capture at least five units, and their projection has no six-block. Its load is at least 82. Across all 68,281 such projections, none contains seven blocks meeting pairwise in at most one point. The dropped column requires just such a group, since at least seven other rows cover it.

Degrees twelve and thirteen consequently score at most seventeen. To score eighteen, a fourteen-row would need at least four units of excess and total load at least 102. Among nineteen blocks it needs at least seven six-blocks, since nineteen fives give only 95. Their 42 incidences are on at most thirteen zero-excess points. These cover more than 42 pairs of blocks, exceeding $2\binom72=42$. Indeed even distributing 42 incidences on fourteen points needs 42 pairs, with equality only if every point has multiplicity three. A fifteen-row reaching score eighteen has at least three units and at least ten six-blocks. Their sixty incidences on at most fourteen zero-excess points likewise exceed $2\binom{10}2=90$ pairs (equality on fifteen points requires four apiece). A sixteen-row needs at least seventeen six-blocks even at zero excess. Their 102 incidences on sixteen points need at least $10\binom62+6\binom72=276$ pairs, above $2\binom{17}2=272$. Higher degrees already require more than $19\cdot6$ incidences.

Thus a maximizing row has degree nine or ten, and the six-block exclusions show all its projected blocks have size at most five. This gives an exhaustive cover for the three-column case. A nine-row needs load at least 72, giving 621,106 projections. A ten-row needs load at least 78, giving 14,748. These are counts of possible marks before the 193-one completion and the three simultaneous extensions are checked.

The 27 nine-row projections of load at least 74 and the twelve ten-row projections of load 79 give zero completions. At most six and eight units of excess, respectively, remain outside those marks. This leaves 621,079 nine-row marks and 14,736 ten-row marks. If the peak score is nineteen, only the 2,191 nine-row marks of load 73 qualify. At peak eighteen the sum of squares of the column excesses is at most $20\cdot18-193-8\cdot17=31$.

The marked-core search exhausted all 2,191 nine-row marks at peak nineteen with no completion. Thus **the peak is exactly eighteen**, leaving 618,888 nine-row projections of load 72 and 14,736 ten-row projections of load 78 before further pruning.

The [completion proof](three-profile-proof.md) excludes all remaining possibilities.
