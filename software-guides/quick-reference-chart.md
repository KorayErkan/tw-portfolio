# Reference Chart / Quick Reference

**Author:** Koray Erkan (portfolio sample)
**Version:** 0.1 — <update date here>

---

## HTTP Status Cheatsheet

| Code | Meaning |
|------|---------|
| 200  | OK — Request processed successfully |
| 201  | Created — Resource created successfully |
| 400  | Bad Request — Input validation failure |
| 401  | Unauthorized — Authentication token invalid/missing |
| 403  | Forbidden — Insufficient permissions for operation |
| 404  | Not Found — Requested resource does not exist |
| 409  | Conflict — Resource state conflict or duplicate |
| 429  | Too Many Requests — Rate limit exceeded |
| 5xx  | Server Error — Internal failure, implement retry logic |

---

## Roles & Permissions (Example)

| Role   | Scope | Capabilities |
|--------|-------|--------------|
| Owner  | Organization | Billing management, SSO configuration, global policy administration |
| Admin  | Workspace | Member invitation/management, integration configuration |
| User   | Workspace | Content creation/editing, report generation |
| Viewer | Workspace | Read-only dashboard and report access |

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
