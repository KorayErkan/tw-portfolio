"""Generate the VH-15 illustrated parts data modules (941) from the BOM.

One IPD per assembly that has a figure. The figure's callout numbers are the BOM item numbers
within the assembly (BOM item 1.4 is callout 4), so the BOM, the figure and the parts list can't
drift apart: change the BOM, rerun this script and make_figures.py, and all three agree.

The IPD shells are created once with s1kd-newdm (see README). This script rewrites the DOCTYPE
(to declare the figure's ICN entity) and the <content>.

Usage: python tools/make_ipd.py   (from the sample root)
"""

import csv
import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
CSDB = ROOT / "csdb"
MFR = "VH000"

# SNS system -> (BOM item of the assembly, figure title, ICN)
IPDS = {
    "10": ("1", "Reservoir", "ICN-VH000-HPU1001-001-01"),
    "40": ("4", "Return filter", "ICN-VH000-HPU4001-001-01"),
}


def doctype(icns):
    """Internal DTD subset declaring each ICN as an unparsed SVG entity."""
    ents = "".join(f'<!ENTITY {i} SYSTEM "{i}.SVG" NDATA svg>' for i in icns)
    return f'<!DOCTYPE dmodule [<!NOTATION svg SYSTEM "image/svg+xml">{ents}]>'


def set_doctype(xml, icns):
    return re.sub(r"<!DOCTYPE dmodule(\s*\[.*?\])?\s*>", lambda m: doctype(icns), xml, count=1, flags=re.S)


def csn(system, item, indenture, pn, qty, descr, top=False):
    return (f'<catalogSeqNumber systemCode="{system}" subSystemCode="0" subSubSystemCode="0" assyCode="00" '
            f'figureNumber="01" figureNumberVariant="A" item="{item:03d}" indenture="{indenture}">'
            f'<itemSeqNumber itemSeqNumberValue="00A">'
            f'<reasonForSelection reasonForSelectionValue="{0 if top else 1}"/>'
            f'<quantityPerNextHigherAssy>{qty}</quantityPerNextHigherAssy>'
            f'<partRef manufacturerCodeValue="{MFR}" partNumberValue="{escape(pn)}"/>'
            f'<partSegment><itemIdentData><descrForPart>{escape(descr)}</descrForPart></itemIdentData></partSegment>'
            f'</itemSeqNumber></catalogSeqNumber>')


def main():
    bom = list(csv.DictReader(open(ROOT / "bom/VH15-0000_BOM.csv", encoding="utf-8", newline="")))
    for system, (top, title, icn) in IPDS.items():
        rows = [r for r in bom if r["ITEM NO."] == top or r["ITEM NO."].startswith(top + ".")]
        entries = []
        for r in rows:
            parts = r["ITEM NO."].split(".")
            if len(parts) == 1:
                entries.append(csn(system, 0, 1, r["PART NUMBER"], "REF", r["DESCRIPTION"], top=True))
            else:
                entries.append(csn(system, int(parts[1]), len(parts), r["PART NUMBER"], r["QTY."], r["DESCRIPTION"]))
        content = (f'<content>\n<illustratedPartsCatalog>\n<figure id="fig-0001"><title>{title}</title>'
                   f'<graphic infoEntityIdent="{icn}"/></figure>\n' + "\n".join(entries)
                   + "\n</illustratedPartsCatalog>\n</content>")
        f = next(CSDB.glob(f"DMC-VH15-A-{system}-00-00-00A-941A-A_*.XML"))
        xml = f.read_text(encoding="utf-8")
        xml = set_doctype(xml, [icn])
        xml = re.sub(r"<content>.*?</content>", lambda m: content, xml, count=1, flags=re.S)
        f.write_text(xml, encoding="utf-8", newline="\n")
        print(f"Updated {f.name}: {len(entries)} items, figure {icn}")


if __name__ == "__main__":
    main()
