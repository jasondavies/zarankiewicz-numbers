"""Draw the 17 × 17, 17 × 18 and 18 × 18 extremal matrices side by side as chain.svg."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PANELS = [
    ('z17-k33/witness-138-six.txt', 17, 17, 'previously ≤ 141'),
    ('z17x18-k33/witness-143.txt', 17, 18, 'previously ≤ 148 · 138 square + one column'),
    ('z18-k33/witness-150.txt', 18, 18, 'previously ≤ 156'),
]
CELL, GAP = 12, 2
PITCH = CELL + GAP
MARGIN, BETWEEN, TOP = 8, 44, 52

STYLE = """
  text { font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; }
  .title { font-size: 15px; font-weight: 600; fill: #0b0b0b; }
  .sub { font-size: 11px; fill: #52514e; }
  .one { fill: #2a78d6; }
  .zero { fill: #e8e7e3; }
  .mark { fill: none; stroke: #0b0b0b; stroke-width: 1.5; }
  @media (prefers-color-scheme: dark) {
    .title { fill: #f0efec; }
    .sub { fill: #c3c2b7; }
    .one { fill: #3987e5; }
    .zero { fill: #2e2e2b; }
    .mark { stroke: #f0efec; }
  }
"""


def read(name, m, n):
    # Same format check as the verifiers: m lines of n characters 0 or 1.
    rows = (ROOT / name).read_text().splitlines()
    if not (len(rows) == m and all(len(r) == n and set(r) <= {'0', '1'} for r in rows)):
        raise ValueError(f'{name} is not a {m} by {n} matrix of 0s and 1s')
    return rows


def extra_column(small, large):
    """Index of the column of `large` whose removal gives `small`, if any."""
    for j in range(len(large[0])):
        if [r[:j] + r[j + 1:] for r in large] == small:
            return j
    return None


def panel(rows, x0, title, subtitle, marked):
    out = [f'<text class="title" x="{x0}" y="{MARGIN + 15}">{title}</text>',
           f'<text class="sub" x="{x0}" y="{MARGIN + 33}">{subtitle}</text>']
    for i, row in enumerate(rows):
        for j, bit in enumerate(row):
            cls = 'one' if bit == '1' else 'zero'
            out.append(f'<rect class="{cls}" x="{x0 + j * PITCH}" y="{TOP + i * PITCH}" '
                       f'width="{CELL}" height="{CELL}" rx="2"/>')
    if marked is not None:
        out.append(f'<rect class="mark" x="{x0 + marked * PITCH - 2.5}" y="{TOP - 2.5}" '
                   f'width="{CELL + 5}" height="{len(rows) * PITCH - GAP + 5}" rx="3"/>')
    return out


def main():
    matrices = [read(name, m, n) for name, m, n, _ in PANELS]
    marked = [None, extra_column(matrices[0], matrices[1]), None]
    if marked[1] is None:
        raise ValueError('the 17 by 18 witness is not the 17 by 17 witness plus a column')
    body, x = [], MARGIN
    for rows, (_, m, n, prev), mark in zip(matrices, PANELS, marked):
        ones = sum(r.count('1') for r in rows)
        body += panel(rows, x, f'{m} × {n} = {ones}', prev, mark)
        x += max(n * PITCH - GAP, 7 * len(prev)) + BETWEEN
    width = x - BETWEEN + MARGIN
    height = TOP + 18 * PITCH - GAP + MARGIN
    svg = '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="t">',
        '<title id="t">Extremal binary matrices with no all-ones 3 by 3 submatrix: '
        '17 by 17 with 138 ones, 17 by 18 with 143 ones, which is the first matrix plus '
        'one outlined column, and 18 by 18 with 150 ones.</title>',
        f'<style>{STYLE}</style>',
        *body,
        '</svg>',
    ])
    (Path(__file__).resolve().parent / 'chain.svg').write_text(svg + '\n')


if __name__ == '__main__':
    main()
