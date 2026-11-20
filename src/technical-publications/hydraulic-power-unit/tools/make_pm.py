"""Build the VH-15 maintenance manual publication module from the data modules in csdb/.

The PM shell is created once with s1kd-newpm (see README). This script rewrites its <content>:
one pmEntry per SNS system, descriptions first, then servicing, then remove/install pairs.
The BREX (022) isn't part of the publication.

Usage: python tools/make_pm.py   (from the sample root)
"""

import csv
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
CSDB = ROOT / "csdb"

# Order of information codes inside a system: what it is, how it works, then the tasks.
ORDER = ["040", "042", "241", "270", "340", "520", "720", "941"]


def sns_titles():
    rows = csv.DictReader(open(ROOT / "sns/VH15-SNS.csv", encoding="utf-8", newline=""))
    return {r["SYSTEM"]: r["TITLE"] for r in rows if r["SUBSYSTEM"] == "0"}


def main():
    titles = sns_titles()
    entries = {}
    for f in sorted(CSDB.glob("DMC-*.XML")):
        root = ET.parse(f).getroot()
        code = root.find(".//dmIdent/dmCode")
        if code.get("infoCode") not in ORDER:
            continue
        entries.setdefault(code.get("systemCode"), []).append(
            (root, code, root.findtext(".//dmTitle/techName"), root.findtext(".//dmTitle/infoName")))

    out = ["<content>"]
    for system in sorted(entries):
        def rank(e):
            info = e[1].get("infoCode")
            group = 0 if info in ("040", "042", "241") else 2 if info == "941" else 1
            return (group, ORDER.index(info) if group == 0 else 0,
                    e[1].get("subSystemCode"), e[1].get("disassyCode"), ORDER.index(info))

        dms = sorted(entries[system], key=rank)
        out.append(f"<pmEntry><pmEntryTitle>{escape(titles[system])}</pmEntryTitle>")
        for _, code, tech, info in dms:
            attrs = " ".join(f'{k}="{v}"' for k, v in code.attrib.items())
            out.append(f"<dmRef><dmRefIdent><dmCode {attrs}/></dmRefIdent><dmRefAddressItems><dmTitle>"
                       f"<techName>{escape(tech)}</techName><infoName>{escape(info)}</infoName>"
                       f"</dmTitle></dmRefAddressItems></dmRef>")
        out.append("</pmEntry>")
    out.append("</content>")

    pm = next(CSDB.glob("PMC-*.XML"))
    xml = pm.read_text(encoding="utf-8")
    xml = re.sub(r"<content>.*?</content>|<content/>", lambda m: "\n".join(out), xml, count=1, flags=re.S)
    pm.write_text(xml, encoding="utf-8", newline="\n")
    print(f"Updated {pm.name}: {sum(len(v) for v in entries.values())} data modules in {len(entries)} entries")


if __name__ == "__main__":
    main()
