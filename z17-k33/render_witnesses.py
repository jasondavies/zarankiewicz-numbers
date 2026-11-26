"""Draw both 138-one witnesses side by side as witnesses.svg, with line degrees."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
WITNESSES = [('witness-138.txt', 'First witness'), ('witness-138-six.txt', 'Second witness')]
CELL, GAP = 16, 2
PITCH = CELL + GAP
GRID = 17 * PITCH - GAP
LABEL = 22          # room for the degree labels
PANEL = GRID + LABEL
MARGIN, BETWEEN, TOP = 8, 40, 48

STYLE = """
  text { font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; }
  .title { font-size: 14px; font-weight: 600; fill: #0b0b0b; }
  .sub, .deg { font-size: 11px; fill: #52514e; }
  .deg { font-variant-numeric: tabular-nums; }
  .one { fill: #2a78d6; }
  .zero { fill: #e8e7e3; }
  @media (prefers-color-scheme: dark) {
    .title { fill: #f0efec; }
    .sub, .deg { fill: #c3c2b7; }
    .one { fill: #3987e5; }
    .zero { fill: #2e2e2b; }
  }
"""


def read(name):
    # Same format check as lower_bound in check_final_cores.py.
    rows = (HERE / name).read_text().splitlines()
    if not (len(rows) == 17 and all(len(r) == 17 and set(r) <= {'0', '1'} for r in rows)):
        raise ValueError(f'{name} is not a 17 by 17 matrix of 0s and 1s')
    return rows


def degree_range(rows):
    rows_deg = [r.count('1') for r in rows]
    cols_deg = [sum(r[j] == '1' for r in rows) for j in range(17)]
    lo, hi = min(rows_deg + cols_deg), max(rows_deg + cols_deg)
    side = 'on each side' if sorted(rows_deg) == sorted(cols_deg) else 'overall'
    return f'Degrees {lo} to {hi} {side}'


def panel(rows, x0, title):
    subtitle = degree_range(rows)
    out = [f'<text class="title" x="{x0}" y="{MARGIN + 14}">{title}</text>',
           f'<text class="sub" x="{x0}" y="{MARGIN + 32}">{subtitle}</text>']
    for i, row in enumerate(rows):
        y = TOP + i * PITCH
        for j, bit in enumerate(row):
            cls = 'one' if bit == '1' else 'zero'
            out.append(f'<rect class="{cls}" x="{x0 + j * PITCH}" y="{y}" '
                       f'width="{CELL}" height="{CELL}" rx="2"/>')
        out.append(f'<text class="deg" x="{x0 + GRID + 6}" y="{y + CELL - 4}">'
                   f'{row.count("1")}</text>')
    for j in range(17):
        degree = sum(r[j] == '1' for r in rows)
        out.append(f'<text class="deg" x="{x0 + j * PITCH + CELL / 2}" '
                   f'y="{TOP + GRID + 16}" text-anchor="middle">{degree}</text>')
    return out


def main():
    width = 2 * MARGIN + 2 * PANEL + BETWEEN
    height = TOP + GRID + 16 + MARGIN
    body = []
    for k, (name, title) in enumerate(WITNESSES):
        body += panel(read(name), MARGIN + k * (PANEL + BETWEEN), title)
    svg = '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="t">',
        '<title id="t">Two 17 by 17 binary matrices with 138 ones and no all-ones '
        '3 by 3 submatrix. Filled squares are ones; row and column degrees are '
        'printed at the right and bottom.</title>',
        f'<style>{STYLE}</style>',
        *body,
        '</svg>',
    ])
    (HERE / 'witnesses.svg').write_text(svg + '\n')


if __name__ == '__main__':
    main()
