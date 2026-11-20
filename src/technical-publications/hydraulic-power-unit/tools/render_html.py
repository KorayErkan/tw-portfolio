"""Render an S1000D descriptive or procedural data module to a standalone HTML page.

A first, minimal renderer for reviewing content. It covers the elements the VH-15 pilot
uses; anything else is rendered as plain text.

Usage: python tools/render_html.py <DM file> <output.html>
"""

import sys
import xml.etree.ElementTree as ET
from html import escape

CSS = """
body { font-family: Calibri, Arial, sans-serif; max-width: 46em; margin: 2em auto; padding: 0 1em;
       color: #1a1a1a; line-height: 1.45; }
header { border-bottom: 2px solid #0b5394; margin-bottom: 1.2em; }
.dmc { font-family: Consolas, monospace; font-size: .85em; color: #555; }
h1 { margin: .2em 0 .1em; } h1 small { display: block; font-size: .55em; color: #0b5394; }
h2 { color: #0b5394; border-bottom: 1px solid #ccd; padding-bottom: .15em; margin-top: 1.6em; }
table { border-collapse: collapse; width: 100%; margin: .4em 0 1em; }
th, td { border: 1px solid #bbc; padding: .3em .5em; text-align: left; vertical-align: top; }
th { background: #eef2f8; }
.warning, .caution { border: 2px solid; padding: .5em .8em; margin: .6em 0; }
.warning { border-color: #b00020; background: #fff1f1; }
.caution { border-color: #c77700; background: #fff8e6; }
.warning b, .caution b { display: block; text-align: center; letter-spacing: .1em; }
ol.steps > li { margin: .35em 0; }
.ref { font-family: Consolas, monospace; font-size: .85em; background: #eef2f8; padding: 0 .25em; }
.meta { font-size: .85em; color: #555; }
"""


def code_str(c, prefix="DMC"):
    a = c.attrib
    return (f"{prefix}-{a['modelIdentCode']}-{a['systemDiffCode']}-{a['systemCode']}-"
            f"{a['subSystemCode']}{a['subSubSystemCode']}-{a['assyCode']}-{a['disassyCode']}"
            f"{a['disassyCodeVariant']}-{a['infoCode']}{a['infoCodeVariant']}-{a['itemLocationCode']}")


def inline(el):
    """Text of a paragraph-level element, with dmRefs and lists rendered."""
    out = [escape(el.text or "")]
    for child in el:
        if child.tag == "dmRef":
            out.append(f'<span class="ref">{code_str(child.find(".//dmCode"))}</span>')
        elif child.tag == "randomList":
            out.append("<ul>" + "".join(f"<li>{inline(li.find('para'))}</li>"
                                        for li in child.findall("listItem")) + "</ul>")
        else:
            out.append(inline(child))
        out.append(escape(child.tail or ""))
    return "".join(out)


def notices(parent):
    html = []
    for n in parent:
        if n.tag in ("warning", "caution"):
            paras = "".join(f"<p>{inline(p)}</p>" for p in n.findall("warningAndCautionPara"))
            html.append(f'<div class="{n.tag}"><b>{n.tag.upper()}</b>{paras}</div>')
    return "".join(html)


def conditions(group):
    rows = []
    for c in group:
        if c.tag == "noConds":
            return "<p>None.</p>"
        text = inline(c.find("reqCond"))
        ref = c.find("dmRef")
        rows.append(f"<li>{text}"
                    + (f' See <span class="ref">{code_str(ref.find(".//dmCode"))}</span>.' if ref is not None else "")
                    + "</li>")
    return "<ul>" + "".join(rows) + "</ul>"


def item_table(group, kind):
    if group is None or group.find(f"no{kind}") is not None or not len(group):
        return "<p>None.</p>"
    rows = []
    for d in group.iter():
        if d.tag.endswith("Descr") and d.tag != "supportEquipDescrGroup":
            ref = d.find("supplyRef")
            ident = (d.findtext(".//partNumber") or (ref.get("supplyNumber") if ref is not None else "")
                     or (d.find("toolRef").get("toolNumber") if d.find("toolRef") is not None else ""))
            rows.append(f"<tr><td>{escape(d.findtext('name', ''))}</td><td class='ref'>{escape(ident)}</td>"
                        f"<td>{escape(d.findtext('reqQuantity', ''))}</td></tr>")
    return ("<table><tr><th>Name</th><th>Identification</th><th>Quantity</th></tr>"
            + "".join(rows) + "</table>")


def steps(parent):
    items = []
    for s in parent.findall("proceduralStep"):
        body = notices(s) + "".join(f"<p>{inline(p)}</p>" for p in s.findall("para"))
        sub = steps(s)
        items.append(f"<li>{body}{sub}</li>")
    return f'<ol class="steps">{"".join(items)}</ol>' if items else ""


def levelled(parent, level=2):
    html = []
    for lp in parent.findall("levelledPara"):
        html.append(f"<h{level}>{escape(lp.findtext('title', ''))}</h{level}>")
        html += [f"<p>{inline(p)}</p>" for p in lp.findall("para")]
        html.append(levelled(lp, level + 1))
    return "".join(html)


def main(src, dst):
    root = ET.parse(src).getroot()
    code = code_str(root.find(".//dmIdent/dmCode"))
    tech = root.findtext(".//dmTitle/techName")
    info = root.findtext(".//dmTitle/infoName")
    iss = root.find(".//dmIdent/issueInfo").attrib
    d = root.find(".//dmAddressItems/issueDate").attrib

    body = []
    proc = root.find(".//content/procedure")
    desc = root.find(".//content/description")
    if proc is not None:
        pre = proc.find("preliminaryRqmts")
        body += ["<h2>Required conditions</h2>", conditions(pre.find("reqCondGroup")),
                 "<h2>Support equipment</h2>", item_table(pre.find("reqSupportEquips"), "SupportEquips"),
                 "<h2>Supplies</h2>", item_table(pre.find("reqSupplies"), "Supplies"),
                 "<h2>Spares</h2>", item_table(pre.find("reqSpares"), "Spares"),
                 "<h2>Safety</h2>", notices(pre.find(".//safetyRqmts")) or "<p>None.</p>",
                 "<h2>Procedure</h2>", steps(proc.find("mainProcedure")),
                 "<h2>Requirements after job completion</h2>",
                 conditions(proc.find("closeRqmts/reqCondGroup"))]
    elif desc is not None:
        body.append(levelled(desc))

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(tech)}: {escape(info)}</title><style>{CSS}</style></head>
<body><header><div class="dmc">{code}</div>
<h1>{escape(tech)}<small>{escape(info)}</small></h1>
<p class="meta">Issue {iss['issueNumber']}-{iss['inWork']} · {d['year']}-{d['month']}-{d['day']} ·
Varnholt VH-15 hydraulic power unit (fictional)</p></header>
{"".join(body)}
</body></html>"""
    open(dst, "w", encoding="utf-8").write(page)
    print(f"Wrote {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
