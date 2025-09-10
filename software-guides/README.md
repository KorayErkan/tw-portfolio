# Software Guides (Portfolio Sample)

**Audience:** Software developers, system administrators, and end users
**Purpose:** Demonstrate comprehensive software documentation practices through a complete documentation site for an imaginary cloud management platform.

## What's Inside

This collection showcases professional technical writing for the fictional _CloudFlow_ platform by Goodweb, Inc., covering multiple documentation types within a unified system:

- **Conceptual Architecture** — High-level system overview and design principles
- **Installation Setup Guide** — Complete deployment procedures for different environments
- **User Manual** — End-user interface guide with workflows and feature explanations
- **Security Compliance** — Security protocols, audit procedures, and compliance requirements
- **Maintenance Troubleshooting** — Diagnostic procedures and problem resolution
- **Quick Reference Chart** — Command and configuration quick-lookup tables
- **Release Notes** — Version history with features, fixes, and upgrade guidance

## How to View This Documentation

This folder is a self-contained documentation site that requires local web serving to view properly.

### Prerequisites

- Node.js (v16 or later recommended)
- npm (included with Node)

### Steps

1. Open a terminal in the `software-guides` folder
2. Install the serve package (first time only):
   ```bash
   npx serve
   ```
   (This will download serve@14.x automatically if not already present)
3. Start the local web server:
   ```bash
   npx serve .
   ```
4. Open http://localhost:3000 (or the port shown in the terminal)

### Notes

- The sidebar navigation is driven by `toc.json`
- All styles are defined in `css/custom.css`
- Content files are rendered dynamically into the site structure

## Highlights
- Integrated documentation site with consistent navigation and styling
- Multiple document types demonstrating versatility in technical communication
- Realistic scenarios based on actual enterprise software requirements
- Professional presentation suitable for client or stakeholder review
- Self-contained structure suitable for local preview or web deployment
