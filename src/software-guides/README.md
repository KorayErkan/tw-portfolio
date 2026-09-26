# Software Guides (Portfolio Sample)

**Audience:** Workspace administrators, IT staff, developers, and end users
**Purpose:** Show how a small, cross-linked documentation set for one software product fits together.

## What's inside

The set documents **Orbitask 1.8.0**, an imaginary cloud project-management service with an optional self-hosted agent. The product, its company, people, URLs (all under the reserved `.example` domain), and figures are fictional.

The pages, in reading order (the same order as the viewer's sidebar):

- **Introduction** — What Orbitask does and how this documentation set is organized
- **Conceptual Architecture** — Components, data model, integration points, and limits
- **Installation & Setup** — Workspace setup, self-hosted agent installation, SSO/SCIM configuration, validation, and rollback
- **User Manual** — Everyday use: projects, tasks, roles and permissions, reports, API, webhooks, keyboard shortcuts
- **Maintenance & Troubleshooting** — Routine tasks and fixes for workspace administrators (agent, SSO/SCIM, webhooks, API errors, data export, contacting support)
- **Quick Reference** — HTTP status codes, API versions, rate limits, and a CLI command table
- **Security & Compliance** — Shared responsibilities, access control, encryption, data retention, and incident notification
- **Release Notes** — Changes in 1.8.0 and the 1.7.x releases, including the API v1 deprecation

Diagrams are Graphviz sources (`img/*.dot`) rendered to SVG (`img/*.svg`).

## How to view this documentation

The pages are Markdown files rendered in the browser by `index.html`, which fetches them over HTTP. Opening `index.html` directly from disk does not work, so serve the folder with any local web server.

### Prerequisites

- Node.js 18 or later (includes `npx`), **or** Python 3

### Steps

1. Open a terminal in this folder (for example, `C:\Path\To\Portfolio\software-guides`).
2. Start a local web server:

   ```bash
   npx serve .
   ```

   The first run downloads the `serve` package; later runs reuse the cached copy. If you prefer Python, run `python -m http.server 3000` instead.
3. Open `http://localhost:3000` (or the port shown in the terminal).

Every page has its own address (for example, `http://localhost:3000/#/user-manual.md#roles-and-permissions`), so you can bookmark or share a section.

> **Note:** When you are done, stop the server with `Ctrl+C` in the terminal.

## Highlights

- One product, one set of facts: the version, role model, API versions, and URLs match on every page
- Cross-links between pages instead of repeated content (for example, one canonical roles table)
- Task-oriented procedures with expected results, plus reference tables for lookup
- Diagrams kept as source code, so they can be reviewed and updated like text
