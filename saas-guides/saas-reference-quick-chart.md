# Reference Chart / Quick Reference

This one-pager is intended for printing or side-by-side use.

## HTTP Status Cheatsheet

| Code | Meaning |
|------|---------|
| 200  | OK — success |
| 201  | Created |
| 400  | Bad Request — validation failed |
| 401  | Unauthorized — invalid/missing token |
| 403  | Forbidden — insufficient scope |
| 404  | Not Found |
| 409  | Conflict — versioning, duplicates |
| 429  | Too Many Requests — rate limited |
| 5xx  | Server error — retry with backoff |

## Roles & Permissions (Example)

| Role  | Scope | Capabilities |
|-------|-------|--------------|
| Owner | Org   | Billing, SSO, global policies |
| Admin | Space | Invite, manage members, configure integrations |
| User  | Space | Create/edit content, run reports |
| Viewer| Space | Read-only dashboards |
