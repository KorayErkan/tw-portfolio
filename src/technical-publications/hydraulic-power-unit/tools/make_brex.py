"""Fill the VH-15 project BREX data module from the project SNS and the DML's code list.

The BREX shell is created once with s1kd-newdm (see README). This script rewrites its
<brexDmRef> and <content>, so rerun it whenever the SNS or the information code list changes.

- brexDmRef points to the Issue 7 default BREX, so `s1kd-brexcheck -l` checks both layers.
- snsRules come from sns/VH15-SNS.csv.
- contextRules narrow the default BREX to this project's values.

Usage: python tools/make_brex.py   (from the sample root)
"""

import csv
import re
from pathlib import Path
from xml.sax.saxutils import escape

import make_dml

ROOT = Path(__file__).resolve().parent.parent
CSDB = ROOT / "csdb"

DEFAULT_BREX = (
    '<dmCode modelIdentCode="S1000D" systemDiffCode="J" systemCode="04" subSystemCode="1" '
    'subSubSystemCode="0" assyCode="0301" disassyCode="00" disassyCodeVariant="A" '
    'infoCode="022" infoCodeVariant="A" itemLocationCode="D"/>'
)

ITEM_LOCATIONS = {
    "A": "Information related to items installed on the product",
    "C": "Information related to items on the bench",
    "D": "Information related to items installed on the product, on a removed major assembly, and on the bench",
}


def sns_rules():
    rows = list(csv.DictReader(open(ROOT / "sns/VH15-SNS.csv", encoding="utf-8", newline="")))
    tree = {}
    for r in rows:
        sub = tree.setdefault(r["SYSTEM"], {"title": None, "subs": {}})
        if r["SUBSYSTEM"] == "0":
            sub["title"] = r["TITLE"]
        sub["subs"].setdefault(r["SUBSYSTEM"], r["TITLE"])

    out = ["<snsRules>", "<snsDescr>"]
    for sys_code, s in tree.items():
        out += [f"<snsSystem><snsCode>{sys_code}</snsCode><snsTitle>{escape(s['title'])}</snsTitle>"]
        for sub_code, title in s["subs"].items():
            t = escape(title)
            out += [
                f"<snsSubSystem><snsCode>{sub_code}</snsCode><snsTitle>{t}</snsTitle>",
                f"<snsSubSubSystem><snsCode>0</snsCode><snsTitle>{t}</snsTitle>",
                f"<snsAssy><snsCode>00</snsCode><snsTitle>{t}</snsTitle></snsAssy>",
                "</snsSubSubSystem></snsSubSystem>",
            ]
        out += ["</snsSystem>"]
    out += ["</snsDescr>", "</snsRules>"]
    return "\n".join(out)


def rule(path, use, values=None):
    vals = "".join(
        f'<objectValue valueForm="single" valueAllowed="{v}">{escape(t)}</objectValue>'
        for v, t in (values or [])
    )
    return (
        "<structureObjectRule>"
        f'<objectPath allowedObjectFlag="2">{escape(path)}</objectPath>'
        f"<objectUse>{escape(use)}</objectUse>{vals}"
        "</structureObjectRule>"
    )


def context_rules():
    codes = sorted(make_dml.INFO_NAMES.items())
    rules = [
        rule("//dmIdent/dmCode/@modelIdentCode",
             "The model identification code is VH15 (fictional; not registered with NSPA).",
             [("VH15", "Varnholt VH-15 hydraulic power unit")]),
        rule("//dmIdent/dmCode/@infoCode",
             "Only the information codes in the project DML are allowed.", codes),
        rule("//dmIdent/dmCode/@itemLocationCode",
             "Item location codes A, C and D only. Training content (T) is out of scope.",
             sorted(ITEM_LOCATIONS.items())),
        rule("//security/@securityClassification",
             "All data modules are unclassified.", [("01", "Unclassified")]),
        rule("//language/@languageIsoCode",
             "Data modules are written in English only, to ASD-STE100.", [("en", "English")]),
    ]
    return (
        "<contextRules>\n"
        "<structureObjectRuleGroup>\n" + "\n".join(rules) + "\n</structureObjectRuleGroup>\n"
        "</contextRules>"
    )


def main():
    path = next(CSDB.glob("DMC-VH15-A-00-00-00-00A-022A-D_*.XML"))
    xml = path.read_text(encoding="utf-8")

    xml = re.sub(r"<brexDmRef>.*?</brexDmRef>",
                 f"<brexDmRef><dmRef><dmRefIdent>{DEFAULT_BREX}</dmRefIdent></dmRef></brexDmRef>",
                 xml, count=1, flags=re.S)

    common = (
        "<commonInfo><para>Business rules for the Varnholt VH-15 hydraulic power unit, a fictional "
        "product used as a portfolio sample. This BREX narrows the S1000D Issue 7 default BREX: "
        "it defines the project SNS and restricts codes and values to those the project uses."
        "</para></commonInfo>"
    )
    content = f"<content>\n<brex>\n{common}\n{sns_rules()}\n{context_rules()}\n</brex>\n</content>"
    xml = re.sub(r"<content>.*?</content>", content, xml, count=1, flags=re.S)

    path.write_text(xml, encoding="utf-8", newline="\n")
    print(f"Updated {path.name}")


if __name__ == "__main__":
    main()
