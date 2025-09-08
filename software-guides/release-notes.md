# Release Notes / Changelog Template

**Author:** John Saysitall (portfolio sample)
**Version:** 0.1 — <update date here>

---

## How to Use

- Maintain **task-oriented** and **impact-focused** entries.
- Prioritize *upgrade notes*, *breaking changes*, and *deprecations* prominently.
- Apply consistent categorization tags (✨ New, ⚡ Improved, 🐛 Fixed, 🛡️ Security).

```graphviz
// version-upgrade-path.dot
digraph G {
  graph [rankdir=LR, splines=true, bgcolor="transparent", nodesep=0.8, ranksep=1.0];
  node  [shape=rounded, style="filled,rounded", fillcolor="#161b22", color="#30363d", fontcolor="#c9d1d9", penwidth=1.2];
  edge  [color="#8b949e", arrowsize=0.9, penwidth=1.3];

  // Version nodes
  v16 [label="v1.6.x\n(Legacy)"];
  v17 [label="v1.7.2\n(Bug fixes)", fillcolor="#d29922"];
  v18 [label="v1.8.0\n(Current)", fillcolor="#238636", fontcolor="#ffffff"];
  v19 [label="v1.9.0\n(Planned)", style=dashed];

  // API deprecation
  api_v1 [label="API v1\n(deprecated)", shape=box, fillcolor="#f85149"];
  api_v2 [label="API v2\n(current)", shape=box, fillcolor="#238636", fontcolor="#ffffff"];

  // Upgrade paths
  v16 -> v17 [label="security patches"];
  v17 -> v18 [label="features + fixes"];
  v18 -> v19 [label="90 days", style=dashed];

  // API evolution
  v17 -> api_v1 [style=dotted];
  v18 -> api_v2 [style=dotted];
  api_v1 -> api_v2 [label="migrate", color="#d29922"];

  // Notes
  note [label="⚠️ API v1 removal in 90 days", shape=note, fillcolor="#d29922"];
  api_v1 -> note [style=dotted, arrowhead=none];
}
```

---

## 2025-09-08 (v1.8.0)

### Highlights

- ✨ **New:** Project templates gallery with pre-configured workflows
- ⚡ **Improved:** Report generation performance enhanced by 30%
- 🛡️ **Security:** Mandatory SSO enforcement for administrator accounts

### Breaking Changes

- None in this release

### Details

- Introduced `/v2/reports` batch processing endpoint
- Enhanced CSV import validation messaging
- Resolved timezone inconsistencies in dashboard displays

### Upgrade Notes

- `GET /v1/reports` deprecated (removal in 90 days) → use `/v2/reports`

---

## 2025-08-15 (v1.7.2)

### Highlights

- 🐛 Critical bug fixes and stability improvements

### Details

- Eliminated duplicate activity feed notifications
- Resolved billing calculation precision errors
- Addressed XSS vulnerability in dashboard filter components

### Upgrade Notes

- No action required
