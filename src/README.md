# Technical Writing Portfolio

Writing samples for developers, sysadmins, end users, technicians, and executives, across software and physical products. Each sample opens as a web page, and the longer manuals also have a PDF.

## Start here

Four samples that show the range in a few minutes:

- **[Orbitask documentation set](./software-guides/)**: eight cross-linked pages for one cloud product, from architecture to release notes, with one set of facts on every page. Readers: workspace admins, IT staff, and end users.
- **[How to back up a live SQLite database](./how-to-guides/back-up-a-live-sqlite-database.md)** ([PDF](./how-to-guides/back-up-a-live-sqlite-database.pdf)): why copying the file loses data, and two safe methods compared. Every command was checked against a sample database, built by a script in the guide's appendix.
- **[Kitchen oven installation and user manual](./user-manuals/kitchen-oven/user-manual.adoc)** ([PDF](./user-manuals/kitchen-oven/user-manual.pdf)): one manual, three readers (gas and electrical installers, household users, and service technicians), with gas and tip-over safety messages and troubleshooting split into user checks and technician-only procedures.
- **[MuseScore task guides](./user-assistance/)**: short visual guides for a real open-source program, with every screenshot taken in the version documented.

## All samples

| Sample | Readers | What it shows |
|---|---|---|
| [API documentation](./api-documentation/) | Developers | One fictional API documented for two languages, with an EBNF grammar of accepted URLs, parameter validation, and error handling |
| [How-to guides](./how-to-guides/) | Practitioners | One goal per guide, from a stated goal to a verified result, with trade-offs in a comparison table |
| [Installation guide](./installation-guide/) | Sysadmins, DevOps | GUI and PowerShell installation of a Windows server product, with expected output and a troubleshooting table |
| [Reference charts](./reference-charts/) | Developers, operators | A configuration file and a programming language, each condensed into scannable tables with a formal grammar |
| [Release notes](./release-notes/) | PMs, engineers, users | A feature release: upgrade steps, security fixes with severity, deprecations with removal versions, and known issues |
| [Software guides](./software-guides/) | Admins, IT staff, users | The Orbitask documentation set, viewed in a sidebar viewer, with SVG diagrams that work in light and dark themes |
| [System configuration guide](./system-configuration-guide/) | Sysadmins, network engineers | Server sizing, reverse proxy, certificates and licensing, through to an ordered decommissioning procedure |
| [Tutorials](./tutorials/) | Developers, learners | A PowerShell tutorial run against one sample folder, and an advanced Git tutorial on rebasing, cherry-picking, and recovery |
| [User assistance](./user-assistance/) | End users | MuseScore 3.6 task guides with highlighted screenshots and the expected result after each step |
| [User manuals](./user-manuals/) | Consumers, installers, technicians | A coffee machine, a cordless drill, a kitchen oven, and an industrial machine, with safety, lockout/tagout, and compliance content |

## How these samples are built

The portfolio is maintained as docs-as-code, the way a product's documentation should be:

- **Sources in plain text:** Markdown and AsciiDoc, versioned in Git and changed through pull requests.
- **Generated outputs:** HTML and PDF are built from the same source with Pandoc (XeLaTeX) and Asciidoctor PDF, so the two formats never drift apart.
- **Continuous publishing:** a GitHub Actions workflow publishes the site on every merge and rewrites source links to the generated pages.
- **Diagrams and screenshots as code:** diagrams are SVG files generated from Python scripts, with a dark-mode palette built in. Screenshot crops, highlights, and callouts are applied by script, so screenshots can be retaken for a new version without manual editing.

## Notes and credits

All companies, products, people, and contact details in the samples are fictional, and any resemblance to real ones is coincidental. The exception is MuseScore, a real open-source program, documented as it is.

I'm indebted to [Ugur Akinci](https://technicalcommunicationcenter.com/) for mentoring me on the fundamentals of technical writing, and on the structure, components, and layout of the documents here.
