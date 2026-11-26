"""Emit ten-column restrictions for the weight-139 border check, one per line."""
from ten_columns import four_cliques, masks, next_fives


def families(prefix, size):
    if len(prefix) == size:
        yield prefix
        return
    for x in next_fives(prefix):
        yield from families(prefix + [x], size)


def cores():
    triples = masks(10, 3)
    # Seven bits per degree suffice to sum sixteen column incidences.
    score = {x: sum(((x >> j) & 1) << (7*j) for j in range(10)) for x in range(1024)}
    for m in (3, 4):
        for f in families([], m):
            for k in range(67 - 48 - 2*m, 17 - m):
                for q in four_cliques(f, k):
                    rows = f + q
                    base = sum(score[x] for x in rows)
                    tails = (t for t in triples if all((t & x) != t for x in rows)) if len(rows) < 16 else (0,)
                    for t in tails:
                        packed = base + score[t]
                        deficit = sum(max(0, 7 - ((packed >> (7*j)) & 127)) for j in range(10))
                        if deficit <= 3 and all(((packed >> (7*j)) & 127) >= 5 for j in range(10)):
                            yield rows + ([t] if t else [])


if __name__ == '__main__':
    for rows in cores():
        print(*rows)
