"""Add numbered callout badges (and optional leader lines) to a manual illustration.

Usage:
    python callouts.py SPEC.json

SPEC.json:
{
  "input":  "path/to/source.png",         # relative to the spec file
  "output": "path/to/result.png",
  "radius": 60,                            # badge radius in source pixels
  "erase":  [[x0, y0, x1, y1], ...],       # optional: boxes to repaint (e.g. AI watermarks)
  "margin": {"top": 0, "bottom": 0, "left": 0, "right": 0, "color": [255, 255, 255]},
  "callouts": [
    {"n": 1, "x": 900, "y": 500, "tx": 1000, "ty": 520},   # badge centre; tx/ty = leader target
    {"n": 2, "x": 300, "y": 800}                             # no leader
  ],
  "dimensions": [                          # optional dimension arrows with a label
    {"x0": 10, "y0": 10, "x1": 200, "y1": 10, "label": "100 mm", "lx": 105, "ly": -30}
  ]
}

All coordinates are in *source* image pixels (before margins are added).
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

BADGE_FILL = (24, 48, 82)      # dark navy — reads on both steel and light-grey backgrounds
BADGE_RING = (255, 255, 255)
LEADER = (24, 48, 82)
FONT_CANDIDATES = ["arialbd.ttf", "segoeuib.ttf", "ArialNova-Bold.ttf", "DejaVuSans-Bold.ttf"]


def font(size):
    for name in FONT_CANDIDATES:
        for base in ("", r"C:\Windows\Fonts"):
            try:
                return ImageFont.truetype(os.path.join(base, name), size)
            except OSError:
                continue
    return ImageFont.load_default()


def erase(im, box):
    """Repaint a box by stretching the column just left of it across (keeps vertical gradients)."""
    x0, y0, x1, y1 = box
    src = max(x0 - 3, 0)
    px = im.load()
    for y in range(y0, y1):
        c = px[src, y]
        for x in range(x0, x1):
            px[x, y] = c


def arrowhead(d, x, y, fx, fy, size, color):
    import math
    ang = math.atan2(y - fy, x - fx)
    pts = [(x, y)]
    for s in (+0.45, -0.45):
        pts.append((x - size * math.cos(ang + s), y - size * math.sin(ang + s)))
    d.polygon(pts, fill=color)


def main(spec_path):
    base = os.path.dirname(os.path.abspath(spec_path))
    spec = json.load(open(spec_path, encoding="utf-8"))
    im = Image.open(os.path.join(base, spec["input"])).convert("RGB")

    for box in spec.get("erase", []):
        erase(im, box)

    m = {"top": 0, "bottom": 0, "left": 0, "right": 0, "color": [255, 255, 255], **spec.get("margin", {})}
    if any(m[k] for k in ("top", "bottom", "left", "right")):
        canvas = Image.new("RGB", (im.width + m["left"] + m["right"], im.height + m["top"] + m["bottom"]), tuple(m["color"]))
        canvas.paste(im, (m["left"], m["top"]))
        if m.get("extend", True):
            # stretch the edge pixels outward so the margin continues the background gradient
            W, H = canvas.size
            l, t, r_, b = m["left"], m["top"], m["right"], m["bottom"]
            if t: canvas.paste(canvas.crop((0, t, W, t + 1)).resize((W, t)), (0, 0))
            if b: canvas.paste(canvas.crop((0, H - b - 1, W, H - b)).resize((W, b)), (0, H - b))
            if l: canvas.paste(canvas.crop((l, 0, l + 1, H)).resize((l, H)), (0, 0))
            if r_: canvas.paste(canvas.crop((W - r_ - 1, 0, W - r_, H)).resize((r_, H)), (W - r_, 0))
        im = canvas
    ox, oy = m["left"], m["top"]

    r = spec.get("radius", 60)
    lw = max(3, r // 9)
    d = ImageDraw.Draw(im)
    f = font(int(r * 1.15))

    for dim in spec.get("dimensions", []):
        x0, y0, x1, y1 = dim["x0"] + ox, dim["y0"] + oy, dim["x1"] + ox, dim["y1"] + oy
        d.line([(x0, y0), (x1, y1)], fill=LEADER, width=lw)
        arrowhead(d, x0, y0, x1, y1, lw * 5, LEADER)
        arrowhead(d, x1, y1, x0, y0, lw * 5, LEADER)
        lf = font(int(r * 0.9))
        lx, ly = (x0 + x1) / 2 + dim.get("lx", 0), (y0 + y1) / 2 + dim.get("ly", 0)
        tb = d.textbbox((lx, ly), dim["label"], font=lf, anchor="mm")
        pad = r // 4
        d.rounded_rectangle([tb[0] - pad, tb[1] - pad, tb[2] + pad, tb[3] + pad], radius=pad, fill=(255, 255, 255), outline=LEADER, width=max(2, lw // 2))
        d.text((lx, ly), dim["label"], font=lf, fill=LEADER, anchor="mm")

    # leaders first so badges sit on top of them
    for c in spec["callouts"]:
        if "tx" in c:
            x, y, tx, ty = c["x"] + ox, c["y"] + oy, c["tx"] + ox, c["ty"] + oy
            d.line([(x, y), (tx, ty)], fill=LEADER, width=lw)
            d.ellipse([tx - lw * 1.6, ty - lw * 1.6, tx + lw * 1.6, ty + lw * 1.6], fill=LEADER, outline=BADGE_RING, width=max(1, lw // 3))
    for c in spec["callouts"]:
        x, y = c["x"] + ox, c["y"] + oy
        d.ellipse([x - r, y - r, x + r, y + r], fill=BADGE_FILL, outline=BADGE_RING, width=lw)
        d.text((x, y + r * 0.04), str(c["n"]), font=f, fill=(255, 255, 255), anchor="mm")

    out = os.path.join(base, spec["output"])
    im.save(out, optimize=True, **({"quality": 90, "progressive": True} if out.lower().endswith((".jpg", ".jpeg")) else {}))
    print(f"wrote {out} ({im.width}x{im.height})")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
