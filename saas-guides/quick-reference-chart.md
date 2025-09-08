# Reference Chart / Quick Reference

**Author:** Koray Erkan (portfolio sample)
**Version:** 0.1 — <update date here>

---

## HTTP Status Cheatsheet

| Code | Meaning |
|------|---------|
| 200  | OK — success |
| 201  | Created |
| 400  | Bad Request — validation failed |
| 401  | Unauthorized — invalid/missing token |
| 403  | Forbidden — insufficient scope |
| 404  | Not Found |
| 409  | Conflict — versioning or duplicates |
| 429  | Too Many Requests — rate limited |
| 5xx  | Server error — retry with backoff |

---

## Roles & Permissions (Example)

| Role   | Scope | Capabilities |
|--------|-------|--------------|
| Owner  | Org   | Billing, SSO, global policies |
| Admin  | Space | Invite, manage members, configure integrations |
| User   | Space | Create/edit content, run reports |
| Viewer | Space | Read-only dashboards |

---

## Example API Calls

```bash
# Health check
curl -i https://api.acmecloud.example/v1/health

# Get projects
curl -H "Authorization: Bearer <TOKEN>" https://api.acmecloud.example/v1/projects
```

---

## Visual Overview

// visual-overview.dot
```graphviz
digraph G {
  graph [rankdir=LR, splines=true, bgcolor="transparent", nodesep=0.8, ranksep=0.8];
  node  [shape=rounded, style="filled,rounded", fillcolor="#161b22", color="#30363d", fontcolor="#c9d1d9", penwidth=1.2];
  edge  [color="#8b949e", arrowsize=0.9, penwidth=1.3];

  client [label="Client"];
  apigw  [label="API Gateway"];
  svc    [label="Service"];

  client -> apigw -> svc;
}
```
