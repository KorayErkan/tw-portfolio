"""Generate the VH-15 illustrations as SVG files in csdb/, named by ICN.

Line drawings with numbered callouts. Callout numbers are the item numbers in the matching
illustrated parts data module (941), so the figure and the parts list stay in step.

  ICN-VH000-HPU1001-001-01.SVG   Reservoir (oblique view)
  ICN-VH000-HPU4001-001-01.SVG   Return filter (exploded view)

Usage: python tools/make_figures.py   (from the sample root)
"""

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSDB = ROOT / "csdb"

STROKE = 'stroke="#000" stroke-width="1.6" fill="#fff" stroke-linejoin="round"'
FACE = 'stroke="#000" stroke-width="1.6" fill="none" stroke-linejoin="round"'
THIN = 'stroke="#000" stroke-width="1" fill="none"'
HIDDEN = 'stroke="#000" stroke-width="1" fill="none" stroke-dasharray="6 4"'
CENTER = 'stroke="#000" stroke-width="0.8" fill="none" stroke-dasharray="14 3 2 3"'
REF = 'stroke="#000" stroke-width="1" fill="#fff" stroke-dasharray="3 3"'
NOTE = 'font-size="11" fill="#555"'


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'font-family="Arial, Helvetica, sans-serif">\n<title>{title}</title>\n'
            f'<rect width="{w}" height="{h}" fill="#fff"/>\n{body}\n</svg>\n')


def poly(points, style=STROKE):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polygon points="{pts}" {style}/>'


def line(p1, p2, style=THIN):
    return f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" {style}/>'


def text(x, y, s, anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" {NOTE} text-anchor="{anchor}">{s}</text>'


def callout(n, x, y, tx, ty):
    """Leader from a dot on the part (x, y) to a numbered circle at (tx, ty)."""
    r = 13
    ang = math.atan2(y - ty, x - tx)
    sx, sy = tx + r * math.cos(ang), ty + r * math.sin(ang)
    return (line((x, y), (sx, sy), 'stroke="#000" stroke-width="0.9"')
            + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="#000"/>'
            + f'<circle cx="{tx}" cy="{ty}" r="{r}" fill="#fff" stroke="#000" stroke-width="1.2"/>'
            + f'<text x="{tx}" y="{ty + 5}" font-size="14" text-anchor="middle">{n}</text>')


def icn_label(icn, w, h):
    return f'<text x="{w - 10}" y="{h - 10}" font-size="10" text-anchor="end" fill="#555">{icn}</text>'


def cylinder(cx, top, h, r, ry=8, style=STROKE, ribs=0):
    out = [f'<path d="M{cx - r},{top} L{cx - r},{top + h} A{r},{ry} 0 0 0 {cx + r},{top + h} '
           f'L{cx + r},{top} Z" {style}/>',
           f'<ellipse cx="{cx}" cy="{top}" rx="{r}" ry="{ry}" {style}/>']
    for k in range(1, ribs + 1):
        x = cx - r + k * (2 * r) / (ribs + 1)
        out.append(line((x, top + ry), (x, top + h + ry * 0.6)))
    return "\n".join(out)


# ------------------------------------------------------------------ reservoir, oblique view
# Front face in true shape (x to the right, z up); depth y recedes up and to the right at 30 degrees.
OX, OY, K = 110, 480, 0.6


def ob(x, y, z):
    a = math.radians(30)
    return OX + x + y * K * math.cos(a), OY - z - y * K * math.sin(a)


def reservoir():
    W, D, H = 330, 200, 210
    out = []

    # Hidden: suction strainer inside the tank, on the pump suction port near the right wall
    sx, sy = W - 70, D / 2
    out.append(poly([ob(sx - 16, sy, 20), ob(sx + 16, sy, 20), ob(sx + 16, sy, 90), ob(sx - 16, sy, 90)], HIDDEN))
    out.append(line(ob(sx, sy, 90), ob(sx, sy, 150), HIDDEN))

    # Tank faces (no fill, so the hidden strainer shows through as dashes)
    out.append(poly([ob(0, 0, 0), ob(W, 0, 0), ob(W, 0, H), ob(0, 0, H)], FACE))
    out.append(poly([ob(W, 0, 0), ob(W, D, 0), ob(W, D, H), ob(W, 0, H)], FACE))
    out.append(poly([ob(0, 0, H), ob(W, 0, H), ob(W, D, H), ob(0, D, H)], FACE))

    # Clean-out cover and gasket on the right (side) wall, with 12 screws
    cy0, cy1, cz0, cz1 = 35, D - 35, 40, H - 45
    out.append(poly([ob(W, cy0 - 5, cz0 - 5), ob(W, cy1 + 5, cz0 - 5), ob(W, cy1 + 5, cz1 + 5), ob(W, cy0 - 5, cz1 + 5)], THIN))
    out.append(poly([ob(W, cy0, cz0), ob(W, cy1, cz0), ob(W, cy1, cz1), ob(W, cy0, cz1)]))
    screws = []
    for t in range(4):
        yy = cy0 + 12 + t * (cy1 - cy0 - 24) / 3
        screws += [(yy, cz0 + 10), (yy, cz1 - 10)]
    for f in (1 / 3, 2 / 3):
        zz = cz0 + 10 + f * (cz1 - cz0 - 20)
        screws += [(cy0 + 12, zz), (cy1 - 12, zz)]
    for yy, zz in screws:
        x, y = ob(W, yy, zz)
        out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="2.6" ry="3.6" fill="#fff" stroke="#000" stroke-width="1.1"/>')

    # Level-temperature gauge on the front wall
    gx, gz0, gz1 = 75, 55, 165
    out.append(poly([ob(gx - 9, 0, gz0), ob(gx + 9, 0, gz0), ob(gx + 9, 0, gz1), ob(gx - 9, 0, gz1)]))
    for zz in (gz0 + 9, gz1 - 9):
        x, y = ob(gx, 0, zz)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#fff" stroke="#000" stroke-width="1.2"/>')
    out.append(line(ob(gx, 0, gz0 + 20), ob(gx, 0, gz1 - 20), 'stroke="#000" stroke-width="3"'))

    # Magnetic drain plug, low on the front wall
    dx = W - 60
    px, py = ob(dx, 0, 14)
    out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="#fff" stroke="#000" stroke-width="1.6"/>')
    out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3" fill="none" stroke="#000" stroke-width="1"/>')

    # Filler-breather cap on top
    cx, cy = ob(80, D / 2, H)
    out.append(f'<path d="M{cx - 16:.1f},{cy - 32:.1f} L{cx - 16:.1f},{cy:.1f} A16,6 0 0 0 {cx + 16:.1f},{cy:.1f} '
               f'L{cx + 16:.1f},{cy - 32:.1f} Z" {STROKE}/>')
    out.append(f'<ellipse cx="{cx:.1f}" cy="{cy - 32:.1f}" rx="16" ry="6" {STROKE}/>')
    for k in range(1, 4):
        out.append(line((cx - 16, cy - 32 + k * 8), (cx + 16, cy - 32 + k * 8)))

    # Return filter on top, for orientation only
    fx, fy = ob(W - 85, D - 70, H)
    out.append(f'<rect x="{fx - 22:.1f}" y="{fy - 44:.1f}" width="44" height="44" {REF}/>')
    out.append(text(fx, fy - 52, "Return filter (ref.)", "middle"))

    calls = [
        (1, *ob(35, 0, 110), 45, 330),                  # tank
        (2, *ob(W, (cy0 + cy1) / 2, cz1 - 25), 715, 150),  # clean-out cover
        (3, *ob(W, cy1 + 5, cz0 + 30), 715, 300),       # gasket
        (4, cx - 16, cy - 16, 215, 150),                # filler-breather cap
        (5, *ob(gx + 9, 0, 110), 45, 430),              # level-temperature gauge
        (6, px, py, 520, 535),                          # drain plug
        (7, *ob(sx, sy, 55), 330, 545),                 # suction strainer (hidden)
        (8, *ob(W, *screws[1]), 660, 95),               # screw
        (9, *ob(W, *screws[2]), 715, 420),              # washer
    ]
    out += [callout(n, x, y, tx, ty) for n, x, y, tx, ty in calls]
    icn = "ICN-VH000-HPU1001-001-01"
    out.append(icn_label(icn, 760, 570))
    return icn, svg(760, 570, "\n".join(out), "Reservoir")


# ------------------------------------------------------------------ return filter, exploded view
def return_filter():
    cx = 260
    out = [line((cx, 30), (cx, 430), CENTER)]

    # Filter cover, exploded upward
    out.append(cylinder(cx, 60, 30, 62, 12))
    for k in range(-3, 4):
        out.append(line((cx + k * 16, 72), (cx + k * 16, 90)))

    # Filter element: pleated cylinder with end caps
    out.append(cylinder(cx, 160, 190, 45, 10, ribs=11))
    out.append(cylinder(cx, 150, 10, 47, 10))
    out.append(cylinder(cx, 350, 10, 47, 10))

    # Housing: the body hangs inside the tank (hidden); head and flange sit on the tank top
    out.append(f'<rect x="{cx - 50}" y="484" width="100" height="120" {HIDDEN}/>')
    out.append(cylinder(cx, 440, 30, 80, 14))
    out.append(f'<rect x="{cx + 78}" y="446" width="70" height="26" {STROKE}/>')
    out.append(f'<ellipse cx="{cx + 148}" cy="459" rx="6" ry="13" {STROKE}/>')
    out.append(text(cx + 160, 463, "Inlet (from manifold)"))

    # Tank top, for orientation
    out.append(line((40, 484), (cx - 80, 484), 'stroke="#000" stroke-width="1.4"'))
    out.append(line((cx + 80, 484), (540, 484), 'stroke="#000" stroke-width="1.4"'))
    out.append(text(40, 502, "Reservoir top (ref.)"))

    # Clogging indicator on the housing head
    out.append(f'<rect x="{cx - 124}" y="430" width="26" height="26" rx="4" {STROKE}/>')
    out.append(f'<circle cx="{cx - 111}" cy="443" r="7" fill="#fff" stroke="#000" stroke-width="1.2"/>')
    out.append(line((cx - 98, 443), (cx - 80, 448)))

    calls = [
        (1, cx + 40, 462, 430, 560),    # housing
        (2, cx + 30, 260, 430, 250),    # element
        (3, cx - 116, 432, 90, 380),    # clogging indicator
    ]
    out += [callout(n, x, y, tx, ty) for n, x, y, tx, ty in calls]
    out.append(text(430, 95, "Filter cover (part of item 1)"))
    out.append(line((425, 91), (cx + 64, 78)))
    icn = "ICN-VH000-HPU4001-001-01"
    out.append(icn_label(icn, 560, 640))
    return icn, svg(560, 640, "\n".join(out), "Return filter")


def main():
    for icn, content in (reservoir(), return_filter()):
        (CSDB / f"{icn}.SVG").write_text(content, encoding="utf-8")
        print(f"Wrote csdb/{icn}.SVG")


if __name__ == "__main__":
    main()
