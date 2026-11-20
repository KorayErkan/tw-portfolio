"""Generate the VH-15 illustrations as SVG files in csdb/, named by ICN.

Shaded isometric drawings, styled after a Gemini-generated concept image, drawn from 3D
coordinates so the geometry stays consistent. Callout numbers are the item numbers in the
matching illustrated parts data module (941), so the figure and the parts list stay in step.

  ICN-VH000-HPU1001-001-01.SVG   Reservoir (isometric view)
  ICN-VH000-HPU4001-001-01.SVG   Return filter (exploded isometric view)

Usage: python tools/make_figures.py   (from the sample root)
"""

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSDB = ROOT / "csdb"

C, S = math.cos(math.radians(30)), 0.5
V = (1 / math.sqrt(3), -1 / math.sqrt(3), 1 / math.sqrt(3))  # toward the viewer
INK = 'stroke="#1f2124" stroke-width="1.5" stroke-linejoin="round"'
THIN = 'stroke="#1f2124" stroke-width="0.9" fill="none"'
DASH = 'stroke="#1f2124" stroke-width="1" fill="none" stroke-dasharray="6 4"'
NSS = 'vector-effect="non-scaling-stroke"'

METAL = [(0, "#5d6168"), (0.2, "#a3a8ae"), (0.4, "#f1f2f4"), (0.62, "#bcc1c7"), (1, "#686c73")]
DARK = [(0, "#1b1d20"), (0.4, "#5a5e64"), (1, "#26282b")]
TOPS = [(0, "#f6f7f8"), (1, "#b9bdc2")]


class Drawing:
    def __init__(self, ox, oy):
        self.ox, self.oy = ox, oy
        self.defs, self.body, self.n = [], [], 0

    # -------------------------------------------------------------- projection
    def P(self, x, y, z):
        return self.ox + (x + y) * C, self.oy + (x - y) * S - z

    def grad(self, stops, p1, p2):
        self.n += 1
        gid = f"g{self.n}"
        st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
        self.defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{p1[0]:.1f}" '
                         f'y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}">{st}</linearGradient>')
        return f"url(#{gid})"

    def add(self, s):
        self.body.append(s)

    def poly(self, pts, fill="none", style=INK):
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        fill_attr = "" if "fill=" in style else f'fill="{fill}" '
        self.add(f'<polygon points="{d}" {fill_attr}{style}/>')

    def line(self, a, b, style=THIN):
        self.add(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" {style}/>')

    # -------------------------------------------------------------- planes
    def plane(self, face, origin):
        """Group transform for drawing in a face's local 2D coordinates (u, v), v up."""
        e, f = self.P(*origin)
        m = {"front": (C, S, 0, -1), "right": (C, -S, 0, -1), "top": (C, S, C, -S)}[face]
        return f'<g transform="matrix({m[0]:.4f} {m[1]:.4f} {m[2]:.4f} {m[3]:.4f} {e:.1f} {f:.1f})">'

    # -------------------------------------------------------------- solids
    def box(self, x, y, z, dx, dy, dz, light=1.0):
        top = [self.P(x, y, z + dz), self.P(x + dx, y, z + dz), self.P(x + dx, y + dy, z + dz), self.P(x, y + dy, z + dz)]
        front = [self.P(x, y, z), self.P(x + dx, y, z), self.P(x + dx, y, z + dz), self.P(x, y, z + dz)]
        right = [self.P(x + dx, y, z), self.P(x + dx, y + dy, z), self.P(x + dx, y + dy, z + dz), self.P(x + dx, y, z + dz)]
        self.poly(front, self.grad([(0, "#e4e6e9"), (0.55, "#c3c7cc"), (1, "#a1a5ab")], front[3], front[1]))
        self.poly(right, self.grad([(0, "#a9adb3"), (1, "#7d8187")], right[0], right[2]))
        self.poly(top, self.grad(TOPS, top[0], top[2]))

    def dashed_box(self, x, y, z, dx, dy, dz):
        c = [(x + i * dx, y + j * dy, z + k * dz) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
        for a in range(8):
            for b in range(a + 1, 8):
                if sum(p != q for p, q in zip(c[a], c[b])) == 1:
                    self.line(self.P(*c[a]), self.P(*c[b]), DASH)

    def _circle3(self, c, axis, r, n=72):
        ax = axis
        e1 = (1, 0, 0) if abs(ax[0]) < 0.9 else (0, 1, 0)
        # Gram-Schmidt
        d = sum(p * q for p, q in zip(e1, ax))
        e1 = tuple(p - d * q for p, q in zip(e1, ax))
        k = math.sqrt(sum(p * p for p in e1))
        e1 = tuple(p / k for p in e1)
        e2 = (ax[1] * e1[2] - ax[2] * e1[1], ax[2] * e1[0] - ax[0] * e1[2], ax[0] * e1[1] - ax[1] * e1[0])
        out = []
        for i in range(n):
            t = 2 * math.pi * i / n
            nrm = tuple(math.cos(t) * p + math.sin(t) * q for p, q in zip(e1, e2))
            out.append((tuple(ci + r * ni for ci, ni in zip(c, nrm)), nrm))
        return out

    def cylinder(self, base, axis, r, length, stops=METAL, ribs=0, cap_stops=TOPS, dashed=False, rings=0):
        top = tuple(b + length * a for b, a in zip(base, axis))
        c0, c1 = self._circle3(base, axis, r), self._circle3(top, axis, r)
        pts = [self.P(*p) for p, _ in c0 + c1]
        hull = convex_hull(pts)
        if dashed:
            self.poly(hull, "none", DASH)
            for cc in (c0, c1):
                self.poly([self.P(*p) for p, _ in cc], "none", DASH)
            return
        a0, a1 = self.P(*base), self.P(*top)
        ax, ay = a1[0] - a0[0], a1[1] - a0[1]
        k = math.hypot(ax, ay) or 1
        nx, ny = -ay / k, ax / k
        if abs(nx) < 1e-6 and abs(ny) < 1e-6:
            nx, ny = 1, 0
        proj = [(x - a0[0]) * nx + (y - a0[1]) * ny for x, y in hull]
        g = self.grad(stops, (a0[0] + nx * min(proj), a0[1] + ny * min(proj)),
                      (a0[0] + nx * max(proj), a0[1] + ny * max(proj)))
        self.poly(hull, g)
        # Thread rings or grooves along the length
        for i in range(1, rings + 1):
            c = tuple(b + length * i / (rings + 1) * a for b, a in zip(base, axis))
            ring = [self.P(*p) for p, nrm in self._circle3(c, axis, r) if sum(q * w for q, w in zip(nrm, V)) > 0]
            if len(ring) > 1:
                self.add(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in ring)}" {THIN}/>')
        # Ribs: knurling or pleats on the visible side
        if ribs:
            for i in range(ribs):
                p0, nrm = self._circle3(base, axis, r, ribs)[i]
                if sum(q * w for q, w in zip(nrm, V)) <= 0.05:
                    continue
                p1 = tuple(p + length * a for p, a in zip(p0, axis))
                inset = min(4, length * 0.15)
                q0 = tuple(p + inset * a for p, a in zip(p0, axis))
                q1 = tuple(p - inset * a for p, a in zip(p1, axis))
                self.line(self.P(*q0), self.P(*q1), 'stroke="#2a2c30" stroke-width="1.1" fill="none"')
        # Visible end cap
        vis = c1 if sum(a * w for a, w in zip(axis, V)) > 0 else c0
        cap = [self.P(*p) for p, _ in vis]
        xs, ys = [p[0] for p in cap], [p[1] for p in cap]
        self.poly(cap, self.grad(cap_stops, (min(xs), min(ys)), (max(xs), max(ys))))
        return vis

    def disc(self, center, axis, r, fill, style=INK):
        self.poly([self.P(*p) for p, _ in self._circle3(center, axis, r)], fill, style)

    # -------------------------------------------------------------- annotation
    def callout(self, n, anchor, tx, ty):
        x, y = anchor
        r = 15
        ang = math.atan2(y - ty, x - tx)
        sx, sy = tx + r * math.cos(ang), ty + r * math.sin(ang)
        self.add(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{sx:.1f}" y2="{sy:.1f}" stroke="#1f2124" stroke-width="0.9"/>'
                 f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#1f2124"/>'
                 f'<circle cx="{tx}" cy="{ty}" r="{r}" fill="#fff" stroke="#1f2124" stroke-width="1.2"/>'
                 f'<text x="{tx}" y="{ty + 5.5}" font-size="16" text-anchor="middle" fill="#1f2124">{n}</text>')

    def note(self, x, y, text, anchor="start"):
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="12" fill="#55595f" text-anchor="{anchor}">{text}</text>')

    def svg(self, w, h, title, icn):
        self.note(w - 12, h - 12, icn, "end")
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
                f'font-family="Century Gothic, Futura, Arial, sans-serif">\n<title>{title}</title>\n'
                f'<defs>{"".join(self.defs)}</defs>\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
                + "\n".join(self.body) + "\n</svg>\n")


def convex_hull(points):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


# ---------------------------------------------------------------------- reservoir
def reservoir():
    W, D, H = 330, 230, 220
    d = Drawing(150, 430)
    d.box(0, 0, 0, W, D, H)

    # Clean-out cover (item 2) and gasket (item 3) on the right side wall, 12 screws (items 8, 9)
    g = d.plane("right", (W, 0, 0))
    d.add(g + f'<rect x="34" y="37" width="162" height="146" fill="#2b2d31" stroke="#1f2124" stroke-width="1.2" {NSS}/></g>')
    plate = d.grad([(0, "#d6d9dd"), (0.5, "#b0b4ba"), (1, "#8d9197")], d.P(W, 40, 180), d.P(W, 190, 40))
    d.add(g + f'<rect x="40" y="43" width="150" height="134" fill="{plate}" stroke="#1f2124" stroke-width="1.4" {NSS}/>'
          f'<rect x="45" y="48" width="140" height="124" fill="none" stroke="#e9ebee" stroke-width="0.8" {NSS}/></g>')
    screws = [(u, v) for u in (54, 96, 134, 176) for v in (57, 163)] + [(u, v) for u in (54, 176) for v in (92, 128)]
    for u, v in screws:
        d.add(g + f'<circle cx="{u}" cy="{v}" r="6.5" fill="#cfd2d6" stroke="#1f2124" stroke-width="1" {NSS}/>'
              f'<circle cx="{u}" cy="{v}" r="4" fill="#3a3d42" stroke="none"/>'
              f'<circle cx="{u - 1.2}" cy="{v + 1.2}" r="1.3" fill="#9a9ea4" stroke="none"/></g>')

    # Level-temperature gauge (item 5) on the front wall
    f = d.plane("front", (0, 0, 0))
    d.add(f + f'<rect x="56" y="48" width="30" height="134" rx="5" fill="#3d4045" stroke="#1f2124" stroke-width="1.3" {NSS}/>'
          f'<rect x="64" y="70" width="14" height="90" rx="6" fill="#16181a" stroke="#0e0f10" {NSS}/>'
          f'<rect x="67" y="75" width="5" height="80" rx="2" fill="#7d838a" stroke="none"/>'
          + "".join(f'<circle cx="71" cy="{y}" r="5" fill="#c6c9cd" stroke="#1f2124" stroke-width="1" {NSS}/>'
                    f'<line x1="68" y1="{y}" x2="74" y2="{y}" stroke="#1f2124" stroke-width="1.2" {NSS}/>' for y in (60, 170))
          + "</g>")

    # Magnetic drain plug (item 6): threaded boss on the front wall
    plug = (W - 75, 0, 32)
    d.cylinder(plug, (0, -1, 0), 15, 10, METAL, rings=0)
    end = d.cylinder((W - 75, -10, 32), (0, -1, 0), 12, 16, METAL, rings=3)
    d.disc((W - 75, -26, 32), (0, -1, 0), 6.5, "#2b2d31")

    # Suction strainer (item 7), hidden inside the tank near the right wall
    d.cylinder((W - 70, D / 2, 18), (0, 0, 1), 22, 85, dashed=True)
    d.line(d.P(W - 70, D / 2, 103), d.P(W - 70, D / 2, 160), DASH)

    # Return filter, for orientation only (not part of this assembly)
    d.dashed_box(W - 120, D - 110, H, 70, 70, 75)
    rx, ry = d.P(W - 85, D - 75, H + 75)
    d.note(rx + 4, ry - 46, "Return filter (ref.)", "middle")

    # Filler-breather cap (item 4): foam filter band and knurled cap
    bx, by = 70, D / 2
    d.cylinder((bx, by, H), (0, 0, 1), 24, 22, DARK, cap_stops=DARK)
    d.cylinder((bx, by, H + 22), (0, 0, 1), 27, 26, METAL, ribs=40)

    calls = [
        (1, d.P(40, 25, H), 80, 120),
        (2, d.P(W, 170, 150), 800, 170),
        (3, d.P(W, 193, 100), 800, 330),
        (4, d.P(bx - 27, by, H + 36), 205, 60),
        (5, d.P(86, 0, 115), 70, 380),
        (6, d.P(W - 75, -26, 22), 470, 610),
        (7, d.P(W - 70, D / 2, 60), 640, 610),
        (8, d.P(W, 54, 163), 700, 70),
        (9, d.P(W, 176, 57), 800, 480),
    ]
    for n, a, tx, ty in calls:
        d.callout(n, a, tx, ty)
    icn = "ICN-VH000-HPU1001-001-01"
    return icn, d.svg(860, 650, "Reservoir", icn)


# ---------------------------------------------------------------------- return filter
def return_filter():
    d = Drawing(320, 600)

    # Reservoir top plate, for orientation, with the housing body hanging inside (hidden)
    d.box(-115, -100, -12, 230, 200, 12)
    d.cylinder((0, 0, -150), (0, 0, 1), 50, 138, dashed=True)
    d.note(*d.P(115, 100, 30), "Reservoir top (ref.)")

    # Centerline
    d.line(d.P(0, 0, -160), d.P(0, 0, 560), 'stroke="#1f2124" stroke-width="0.8" fill="none" stroke-dasharray="16 4 3 4"')

    # Housing (item 1): head with inlet pipe and gasket ring
    d.cylinder((0, 0, 0), (0, 0, 1), 72, 34, METAL)
    d.disc((0, 0, 34), (0, 0, 1), 60, "#2b2d31")
    d.disc((0, 0, 34), (0, 0, 1), 48, d.grad([(0, "#cfd2d6"), (1, "#8f9399")], d.P(-48, 0, 34), d.P(48, 0, 34)))
    d.disc((0, 0, 34), (0, 0, 1), 40, d.grad([(0, "#5d6168"), (1, "#b8bcc1")], d.P(-40, 0, 34), d.P(40, 0, 34)))
    d.cylinder((58, 0, 17), (1, 0, 0), 12, 96, METAL)
    d.disc((154, 0, 17), (1, 0, 0), 7, "#2b2d31")

    # Clogging indicator (item 3), shown off the housing
    d.line(d.P(-10, -74, 17), d.P(-10, -122, 17), DASH)
    d.box(-22, -152, 4, 26, 26, 26)
    d.disc((-9, -152, 17), (0, -1, 0), 8, d.grad([(0, "#f1f2f4"), (1, "#9ea2a8")], d.P(-17, -152, 25), d.P(-1, -152, 9)))

    # Filter element (item 2): end caps and pleated media
    d.cylinder((0, 0, 130), (0, 0, 1), 46, 14, METAL)
    d.cylinder((0, 0, 144), (0, 0, 1), 41, 160, [(0, "#3a3d42"), (0.4, "#8a8f96"), (1, "#3f4247")], ribs=64)
    d.cylinder((0, 0, 304), (0, 0, 1), 46, 14, METAL)

    # Filter cover (part of item 1): knurled cap
    d.cylinder((0, 0, 420), (0, 0, 1), 70, 38, METAL, ribs=48)

    for n, a, tx, ty in [
        (1, d.P(36, -52, 12), 540, 650),
        (2, d.P(30, -26, 230), 540, 330),
        (3, d.P(-22, -152, 30), 70, 520),
    ]:
        d.callout(n, a, tx, ty)
    ax, ay = d.P(48, -48, 440)
    d.line((ax, ay), (440, 80))
    d.add('<circle cx="{:.1f}" cy="{:.1f}" r="2.6" fill="#1f2124"/>'.format(ax, ay))
    d.note(444, 76, "Filter cover (part of item 1)")
    icn = "ICN-VH000-HPU4001-001-01"
    return icn, d.svg(660, 820, "Return filter", icn)


def main():
    for icn, content in (reservoir(), return_filter()):
        (CSDB / f"{icn}.SVG").write_text(content, encoding="utf-8")
        print(f"Wrote csdb/{icn}.SVG")


if __name__ == "__main__":
    main()
