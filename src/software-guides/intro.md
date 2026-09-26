# Introduction

**Author:** John Saysitall  
**Version:** Orbitask 1.8.0 · August 2026

---

## Welcome to Orbitask

Orbitask is a cloud-based project-management service. Teams use it to plan work in projects, track tasks from backlog to done, and report on progress. Organizations that need to connect on-premises systems can add a small self-hosted agent.

---

## What Orbitask does

Orbitask gives each organization one or more workspaces where teams can:

- **Manage projects**: Group related work, milestones, and dashboards.
- **Assign and track tasks**: Set owners, due dates, priorities, and status.
- **Work together**: Invite teammates and control access with four workspace roles.
- **Report on progress**: Export summaries and analytics as CSV or PDF.
- **Connect other systems**: Use the REST API, webhooks, your identity provider, and the self-hosted agent.

---

## Key features

### Workspaces and access

- Workspaces contain projects, members, and settings.
- Four roles (Owner, Admin, Member, Viewer) are assigned per workspace; projects inherit them. See [Roles and permissions](user-manual.md#roles-and-permissions).

### Task management

- Tasks with descriptions, due dates, priorities, tags, and dependencies
- Bulk updates from the web app, CLI, or API
- A configurable status workflow, from **Backlog** to **Done**

### Integrations

- Single sign-on with SAML 2.0 or OpenID Connect (Okta, Microsoft Entra ID, Google Workspace)
- SCIM user provisioning (Okta; Microsoft Entra ID in preview)
- REST API v2 with rate limiting and idempotent writes
- Signed webhooks for task, project, and member events
- CSV import and connectors for S3-compatible object storage

### Scale

- Up to 10,000 users per workspace. Larger organizations use several workspaces under an Enterprise plan.

---

## How this documentation is organized

| Page | Read it when you want to |
|------|--------------------------|
| [Conceptual Architecture](conceptual-architecture.md) | Understand the components and how data flows |
| [Installation & Setup](installation-setup-guide.md) | Set up a workspace, SSO, SCIM, and the agent |
| [User Manual](user-manual.md) | Use projects, tasks, reports, the CLI, API, and webhooks |
| [Maintenance & Troubleshooting](maintenance-troubleshooting.md) | Keep a workspace healthy and fix common problems |
| [Quick Reference](quick-reference-chart.md) | Look up status codes, API versions, and CLI commands |
| [Security & Compliance](security-compliance.md) | Review encryption, retention, and incident handling |
| [Release Notes](release-notes.md) | See what changed in 1.8.0 and what to do about it |

---

## Getting help

- **Help center:** `https://help.orbitask.example`
- **Support:** `support@orbitask.example`, or **Help → Contact support** in the app
- **Service status:** `https://status.orbitask.example`

---

*Orbitask is a fictional product created for portfolio demonstration. All names, URLs, and figures are imaginary.*
