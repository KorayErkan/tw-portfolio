# Hydraulic power unit: S1000D technical publication

Maintenance data for the Varnholt VH-15, a fictional 5.5 kW industrial hydraulic power unit,
written to **S1000D Issue 7**. The data module list is derived from the product's bill of materials,
and every data module is checked automatically against the schema, the project's business rules,
and its numbering system.

**Status:** pilot in progress. 14 of the 17 pilot data modules are written, covering the whole unit,
the reservoir, and the return filter; 52 data modules are planned in all.

## How it's built

Each step's output is the next step's input, so a change to the BOM flows through to the list of
data modules that need writing or review.

| Step | Input | Tool | Output |
|---|---|---|---|
| 1. Bill of materials | CAD export: indented BOM, 45 parts in 3 levels | none | [`bom/VH15-0000_BOM.csv`](bom/VH15-0000_BOM.csv) |
| 2. Structure and maintenance decisions | BOM | none (engineering judgment) | Project SNS and part-to-SNS map in [`sns/`](sns/) |
| 3. Data management list | BOM, SNS, map | [`tools/make_dml.py`](tools/make_dml.py) | [`dml/VH15-DML.md`](dml/VH15-DML.md), [`dml/coverage.md`](dml/coverage.md) |
| 4. Business rules | SNS, information code list | [`tools/make_brex.py`](tools/make_brex.py) | Project BREX data module (information code 022) |
| 5. Data modules | DML | written by hand in ASD-STE100 style; shells from `s1kd-newdm` | [`csdb/`](csdb/) |
| 6. Checks | Data modules | [`tools/check.sh`](tools/check.sh) | Pass or fail |
| 7. Rendering | Data modules | [`tools/render_html.py`](tools/render_html.py) | HTML (in progress) |

## What the checks catch

| Problem | Caught by |
|---|---|
| A bought part has no maintenance decision, so no procedure covers it | Coverage report (`make_dml.py`) |
| A data module breaks the S1000D schema | Schema validation (`s1kd-validate`) |
| A code or value the project doesn't allow, such as an information code outside the DML | Project BREX, layered on the Issue 7 default BREX (`s1kd-brexcheck -l`) |
| A data module code that points outside the product structure | SNS check (`s1kd-brexcheck -S`) |

The coverage report lists 11 undecided parts on purpose: it shows the check doing its job.

## Folder layout

| Folder | Holds |
|---|---|
| `bom/` | The BOM export |
| `sns/` | Project SNS and the part-to-SNS map |
| `dml/` | Generated data management list and coverage report (don't edit) |
| `csdb/` | The data modules, plus the CSDB settings written by `s1kd-defaults` |
| `tools/` | Generators, checks, renderer, and the XML catalog for offline validation |

## Run the checks

Requirements: [s1kd-tools](https://github.com/kibook/s1kd-tools) 6.x, Python 3, and the Issue 7
flat schemas in `etc/s1000d-schemas/` at the repository root. The schemas aren't included; download
the Issue 7 package from the S1000D website.

```sh
python tools/make_dml.py    # rebuild the DML and coverage report
python tools/make_brex.py   # rebuild the project BREX
sh tools/check.sh           # schema, BREX and SNS checks
```

Open `hydraulic-power-unit.code-workspace` in VS Code with the Red Hat XML extension to get
schema validation and completion while editing.

## Limits

- The model identification code `VH15` isn't registered with NSPA, and the manufacturer code `VH000`
  isn't a registered CAGE code. Both are placeholders for a fictional product.
- The SNS is defined for this project, not taken from one of the maintained SNS in the specification.
- The CSDB is a folder managed with s1kd-tools, not a commercial CSDB product.
- There are no illustrations yet, so the illustrated parts data modules are planned but not written.
