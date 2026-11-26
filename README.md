# Zarankiewicz numbers

This repository collects exact values of Zarankiewicz numbers. Each value comes with explicit extremal matrices and a proof that can be replayed by computer.

The Zarankiewicz number $z(m,n;s,t)$ is the largest number of ones in an $m \times n$ binary matrix that contains no all-ones $s \times t$ submatrix. The rows and columns of the submatrix may be any $s$ rows and any $t$ columns, not necessarily adjacent. Equivalently, it is the largest number of edges in a bipartite graph with parts of sizes $m$ and $n$ that has no $K_{s,t}$ subgraph. This repository uses this maximum-ones convention throughout.

## Results

| Value | Directory | Contents |
|---|---|---|
| $z(17,17;3,3) = 138$ | [`z17-k33`](z17-k33) | Two inequivalent witnesses, a written proof, and a computer-assisted exhaustion ruling out 139 |

[![The two 17 × 17 witnesses with 138 ones](z17-k33/witnesses.svg)](z17-k33)

## Layout

Each result has its own directory with a README describing the files and how to replay the verification. A directory typically contains:

- the witness matrices as plain text, one row per line;
- a written proof in Markdown, with a typeset PDF;
- the verification sources and one script that replays the whole check;
- a zip bundle of all of the above.

## License

The repository is licensed under [Apache-2.0](LICENSE). Cited papers are linked rather than redistributed.
