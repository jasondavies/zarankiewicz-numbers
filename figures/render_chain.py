"""Draw the extremal matrices from 17 × 17 to 19 × 19 side by side as chain.svg.

Where a witness is an earlier matrix plus one line, that line is outlined.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# (witness, rows, columns, caption lines, earlier matrix it extends or None)
PANELS = [
    ('z17-k33/witness-138-six.txt', 17, 17, ['previously ≤ 141'], None),
    ('z17x18-k33/witness-143.txt', 17, 18, ['previously ≤ 148', '138 square + one column'],
     'z17-k33/witness-138-six.txt'),
    ('z18-k33/witness-150.txt', 18, 18, ['previously ≤ 156'], None),
    ('z18x19-k33/witness-156.txt', 18, 19, ['150 square + one column'], 'z18-k33/witness-150.txt'),
    ('z19-k33/witness-164.txt', 19, 19, ['second 156 rectangle', '+ one row'],
     'z18x19-k33/witness-156-min8.txt'),
]
CELL, GAP = 10, 2
PITCH = CELL + GAP
MARGIN, BETWEEN, TOP = 8, 36, 64
ROWS = max(m for _, m, _, _, _ in PANELS)

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


def read(name, m=None, n=None):
    # Same format check as the verifiers: lines of equal length made of 0 and 1.
    rows = (ROOT / name).read_text().splitlines()
    m = m or len(rows)
    n = n or len(rows[0])
    if not (len(rows) == m and all(len(r) == n and set(r) <= {'0', '1'} for r in rows)):
        raise ValueError(f'{name} is not a {m} by {n} matrix of 0s and 1s')
    return rows


def extra_line(small, large):
    """('column', j) or ('row', i) if deleting that line of `large` gives `small`."""
    if len(small) == len(large):
        for j in range(len(large[0])):
            if [r[:j] + r[j + 1:] for r in large] == small:
                return 'column', j
    if len(small) + 1 == len(large):
        for i in range(len(large)):
            if large[:i] + large[i + 1:] == small:
                return 'row', i
    return None


def panel(rows, x0, title, lines, marked):
    out = [f'<text class="title" x="{x0}" y="{MARGIN + 15}">{title}</text>']
    for k, line in enumerate(lines):
        out.append(f'<text class="sub" x="{x0}" y="{MARGIN + 33 + 14 * k}">{line}</text>')
    for i, row in enumerate(rows):
        for j, bit in enumerate(row):
            cls = 'one' if bit == '1' else 'zero'
            out.append(f'<rect class="{cls}" x="{x0 + j * PITCH}" y="{TOP + i * PITCH}" '
                       f'width="{CELL}" height="{CELL}" rx="2"/>')
    if marked:
        kind, k = marked
        if kind == 'column':
            x, y, w, h = x0 + k * PITCH, TOP, CELL, len(rows) * PITCH - GAP
        else:
            x, y, w, h = x0, TOP + k * PITCH, len(rows[0]) * PITCH - GAP, CELL
        out.append(f'<rect class="mark" x="{x - 2.5}" y="{y - 2.5}" '
                   f'width="{w + 5}" height="{h + 5}" rx="3"/>')
    return out


def main():
    body, x = [], MARGIN
    for name, m, n, lines, base in PANELS:
        rows = read(name, m, n)
        marked = None
        if base:
            marked = extra_line(read(base), rows)
            if marked is None:
                raise ValueError(f'{name} is not {base} plus one line')
        ones = sum(r.count('1') for r in rows)
        body += panel(rows, x, f'{m} × {n} = {ones}', lines, marked)
        x += n * PITCH - GAP + BETWEEN
    width = x - BETWEEN + MARGIN
    height = TOP + ROWS * PITCH - GAP + MARGIN
    svg = '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="t">',
        '<title id="t">Extremal binary matrices with no all-ones 3 by 3 submatrix: '
        '17 by 17 with 138 ones; 17 by 18 with 143, the first matrix plus an outlined column; '
        '18 by 18 with 150; 18 by 19 with 156, the 150-one square plus an outlined column; '
        'and 19 by 19 with 164, a second 156-one rectangle plus an outlined row.</title>',
        f'<style>{STYLE}</style>',
        *body,
        '</svg>',
    ])
    (Path(__file__).resolve().parent / 'chain.svg').write_text(svg + '\n')


if __name__ == '__main__':
    main()
