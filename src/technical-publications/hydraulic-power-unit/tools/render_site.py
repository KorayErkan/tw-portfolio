"""Render the VH-15 publication to HTML: a contents page from the publication module and one
page per data module, styled with the portfolio CSS (common-light.css + s1000d.css).

References to data modules that exist become links; references to planned ones show their
title from the DML, marked as planned.

Usage: python tools/render_site.py   (from the sample root; writes html/)
"""

import re
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSDB, OUT = ROOT / "csdb", ROOT / "html"
CSS = ["../../../css/common-light.css", "../../../css/s1000d.css"]
PRODUCT = "Varnholt VH-15 hydraulic power unit (fictional)"


def code_str(c):
    a = c.attrib
    return (f"DMC-{a['modelIdentCode']}-{a['systemDiffCode']}-{a['systemCode']}-"
            f"{a['subSystemCode']}{a['subSubSystemCode']}-{a['assyCode']}-{a['disassyCode']}"
            f"{a['disassyCodeVariant']}-{a['infoCode']}{a['infoCodeVariant']}-{a['itemLocationCode']}")


def planned_titles():
    """DMC -> 'Tech name: info name', from the generated DML table."""
    titles = {}
    for line in (ROOT / "dml/VH15-DML.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| `(DMC-[^`]+)` \| ([^|]+) \| ([^|]+) \|", line)
        if m:
            titles[m.group(1)] = f"{m.group(2).strip()}: {m.group(3).strip()}"
    return titles


class Renderer:
    def __init__(self, pages, planned):
        self.pages, self.planned = pages, planned  # pages: DMC -> (title)

    def ref(self, dmref):
        c = code_str(dmref.find(".//dmCode"))
        if c in self.pages:
            return f'<a href="{c}.html">{escape(self.pages[c])}</a>'
        return f'<span class="planned">{escape(self.planned.get(c, c))} (planned)</span>'

    def inline(self, el):
        out = [escape(el.text or "")]
        for child in el:
            if child.tag == "dmRef":
                out.append(self.ref(child))
            elif child.tag == "randomList":
                out.append("<ul>" + "".join(f"<li>{self.inline(li.find('para'))}</li>"
                                            for li in child.findall("listItem")) + "</ul>")
            else:
                out.append(self.inline(child))
            out.append(escape(child.tail or ""))
        return "".join(out)

    def notices(self, parent):
        html = []
        for n in parent if parent is not None else []:
            if n.tag in ("warning", "caution"):
                paras = "".join(f"<p>{self.inline(p)}</p>" for p in n.findall("warningAndCautionPara"))
                html.append(f'<div class="{n.tag}"><span class="notice-label">{n.tag.upper()}</span>{paras}</div>')
        return "".join(html)

    def conditions(self, group):
        if group is None or group.find("noConds") is not None:
            return '<p class="none">None.</p>'
        items = []
        for c in group:
            ref = c.find("dmRef")
            extra = f" Refer to {self.ref(ref)}." if ref is not None else ""
            items.append(f"<li>{self.inline(c.find('reqCond'))}{extra}</li>")
        return f'<ul class="conditions">{"".join(items)}</ul>'

    def items(self, group):
        if group is None or not any(e.tag.endswith("DescrGroup") for e in group):
            return '<p class="none">None.</p>'
        rows = []
        for d in group.iter():
            if d.tag in ("supportEquipDescr", "supplyDescr", "spareDescr"):
                ref = d.find("supplyRef") if d.find("supplyRef") is not None else d.find("toolRef")
                ident = d.findtext(".//partNumber") or (
                    ref.get("supplyNumber") or ref.get("toolNumber") if ref is not None else "")
                rows.append(f"<tr><td>{escape(d.findtext('name', ''))}</td><td><code>{escape(ident)}</code></td>"
                            f"<td>{escape(d.findtext('reqQuantity', ''))}</td></tr>")
        return "<table><tr><th>Name</th><th>Identification</th><th>Quantity</th></tr>" + "".join(rows) + "</table>"

    def steps(self, parent):
        lis = []
        for s in parent.findall("proceduralStep"):
            title = f'<span class="step-title">{escape(s.findtext("title"))}</span>' if s.find("title") is not None else ""
            body = self.notices(s) + "".join(f"<p>{self.inline(p)}</p>" for p in s.findall("para"))
            if not body and title:
                body = ""
            lis.append(f"<li>{title}{body}{self.steps(s)}</li>")
        return f'<ol class="steps">{"".join(lis)}</ol>' if lis else ""

    def levelled(self, parent, level=2):
        html = []
        for lp in parent.findall("levelledPara"):
            html.append(f"<h{level}>{escape(lp.findtext('title', ''))}</h{level}>")
            html += [f"<p>{self.inline(p)}</p>" for p in lp.findall("para")]
            html.append(self.levelled(lp, level + 1))
        return "".join(html)

    def body(self, root):
        proc = root.find(".//content/procedure")
        if proc is not None:
            pre = proc.find("preliminaryRqmts")
            return "".join([
                "<h2>Required conditions</h2>", self.conditions(pre.find("reqCondGroup")),
                "<h2>Support equipment</h2>", self.items(pre.find("reqSupportEquips")),
                "<h2>Supplies</h2>", self.items(pre.find("reqSupplies")),
                "<h2>Spares</h2>", self.items(pre.find("reqSpares")),
                "<h2>Safety</h2>", self.notices(pre.find(".//safetyRqmts")) or '<p class="none">None.</p>',
                "<h2>Procedure</h2>", self.steps(proc.find("mainProcedure")),
                "<h2>Requirements after job completion</h2>", self.conditions(proc.find("closeRqmts/reqCondGroup")),
            ])
        desc = root.find(".//content/description")
        return self.levelled(desc) if desc is not None else ""


def page(title, body):
    links = "\n".join(f'<link rel="stylesheet" href="{c}">' for c in CSS)
    return (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f"<title>{escape(title)}</title>\n{links}\n</head>\n<body>\n{body}\n</body>\n</html>\n")


def nav(prev, nxt, pages, where=""):
    p = f'<a href="{prev}.html">← {escape(pages[prev])}</a>' if prev else "<span></span>"
    n = f'<a href="{nxt}.html">{escape(pages[nxt])} →</a>' if nxt else "<span></span>"
    return f'<nav class="pub-nav {where}">{p}<a href="index.html">Contents</a>{n}</nav>'


def main():
    pm = ET.parse(next(CSDB.glob("PMC-*.XML"))).getroot()
    pm_title = pm.findtext(".//pmTitle")
    files = {code_str(ET.parse(f).getroot().find(".//dmIdent/dmCode")): f for f in CSDB.glob("DMC-*.XML")}

    order, sections = [], []
    for entry in pm.findall(".//content/pmEntry"):
        items = []
        for ref in entry.findall("dmRef"):
            c = code_str(ref.find(".//dmCode"))
            order.append(c)
            items.append((c, f"{ref.findtext('.//techName')}: {ref.findtext('.//infoName')}"))
        sections.append((entry.findtext("pmEntryTitle"), items))
    pages = {c: t for _, items in sections for c, t in items}
    r = Renderer(pages, planned_titles())

    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.html"):
        old.unlink()

    toc = "".join(
        f"<h2>{escape(title)}</h2><ul>"
        + "".join(f'<li><a href="{c}.html">{escape(t)}</a><span class="dmc">{c}</span></li>' for c, t in items)
        + "</ul>" for title, items in sections)
    (OUT / "index.html").write_text(page(pm_title, (
        f'<header class="dm-header"><div class="dmc">{escape(PRODUCT)}</div><h1>{escape(pm_title)}</h1></header>'
        "<p>Maintenance data written to S1000D Issue 7. Each page below is one data module, rendered from "
        'its XML source. See the <a href="../">README</a> for how the publication is built and checked.</p>'
        f'<div class="toc">{toc}</div>')), encoding="utf-8")

    for i, c in enumerate(order):
        root = ET.parse(files[c]).getroot()
        tech, info = root.findtext(".//dmTitle/techName"), root.findtext(".//dmTitle/infoName")
        iss = root.find(".//dmIdent/issueInfo").attrib
        d = root.find(".//dmAddressItems/issueDate").attrib
        prev = order[i - 1] if i else None
        nxt = order[i + 1] if i + 1 < len(order) else None
        head = (f'<header class="dm-header"><div class="dmc">{c}</div>'
                f'<h1>{escape(tech)}<span class="info-name">{escape(info)}</span></h1>'
                f'<div class="dm-meta">Issue {iss["issueNumber"]}-{iss["inWork"]} · '
                f'{d["year"]}-{d["month"]}-{d["day"]} · {escape(PRODUCT)}</div></header>')
        body = nav(prev, nxt, pages) + head + r.body(root) + nav(prev, nxt, pages, "bottom")
        (OUT / f"{c}.html").write_text(page(f"{tech}: {info}", body), encoding="utf-8")

    print(f"Wrote html/index.html and {len(order)} data module pages")


if __name__ == "__main__":
    main()
