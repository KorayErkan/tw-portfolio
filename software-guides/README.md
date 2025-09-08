# Software Guides

This folder contains **software documentation** for an imaginary product (_CloudFlow_ by Goodweb, Inc.), showcasing comprehensive technical writing capabilities.

The chapters represent fictional scenarios crafted to demonstrate professional documentation standards and real-world applicability.

## Running This Documentation Locally

This folder is set up as a self-contained documentation site.

### Prerequisites
- [Node.js](https://nodejs.org/) (v16 or later recommended)
- `npm` (comes with Node)

### Steps
1. Open a terminal in the `software-guides` folder.
2. Install the `serve` package (first time only):
   ```bash
   npx serve
   ```
(This will download serve@14.x automatically if not already present.)
3. Start the local web server:
   ```bash
   npx serve .
   ```
4. Open http://localhost:3000 (or the port shown in the terminal).

### Notes

- The sidebar navigation is driven by toc.json.
- Markdown files (.md) are rendered dynamically into HTML.
- All styles are defined in css/custom.css. Adjust this file to change the look and feel.

---

**Author:** Koray Erkan (portfolio sample)
