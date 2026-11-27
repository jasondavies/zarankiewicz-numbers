"""Print the 225-one witness by closing eight cells under two permutations."""

def permutation(cycles):
    image = list(range(24))
    for cycle in cycles:
        for a, b in zip(cycle, cycle[1:] + cycle[:1]):
            image[a] = b
    assert sorted(image) == list(range(24))
    return image


def symmetries():
    return [
        (permutation([(1, 4, 16, 14, 10), (2, 22), (3, 12, 20, 7, 19, 6, 17, 8, 11, 18), (9, 13, 21, 15, 23)]),
         permutation([(1, 21, 9, 6, 2), (3, 13, 4, 16, 20, 15, 17, 5, 12, 10), (7, 18, 14, 11, 22), (8, 23)])),
        (permutation([(1, 7), (2, 5), (3, 19), (4, 8), (6, 14), (9, 23), (10, 18), (11, 17), (12, 16), (13, 15)]),
         permutation([(1, 12), (2, 20), (3, 6), (4, 21), (5, 15), (7, 18), (8, 19), (9, 17), (10, 16), (14, 22)])),
    ]


def construct():
    generators = symmetries()
    seeds = [(1, 2), (1, 7), (1, 8), (1, 10), (2, 1), (9, 4), (9, 11), (9, 18)]
    ones = set()
    for seed, size in zip(seeds, [30, 30, 30, 60, 30, 30, 10, 5]):
        orbit = {seed}
        pending = [seed]
        while pending:
            row, col = pending.pop()
            for rows, cols in generators:
                cell = rows[row], cols[col]
                if cell not in orbit:
                    orbit.add(cell)
                    pending.append(cell)
        assert len(orbit) == size and ones.isdisjoint(orbit)
        ones.update(orbit)
    return [''.join('1' if (r, c) in ones else '0' for c in range(1, 24))
            for r in range(1, 24)]


if __name__ == '__main__':
    print('\n'.join(construct()))
