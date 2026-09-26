# Quick Reference

**Author:** John Saysitall  
**Version:** Orbitask 1.8.0 · August 2026

---

## Addresses

| What | Address |
|------|---------|
| Web app | `https://app.orbitask.example` |
| API (current) | `https://api.orbitask.example/v2` |
| Agent connection | `agent.orbitask.example:443` (outbound from the agent) |
| Downloads (CLI, agent) | `https://downloads.orbitask.example` |
| Service status | `https://status.orbitask.example` |

---

## API versions

| Version | Status | Notes |
|---------|--------|-------|
| **v2** | Current | Covers all endpoints since Orbitask 1.8.0 |
| **v1** | Deprecated | End of life **2026-11-16**. After that date, v1 calls return `410 Gone`. See [Release Notes](release-notes.md#deprecations) |

Rate limit: 1,000 requests per minute per API token. See [API errors and rate limits](maintenance-troubleshooting.md#api-errors-and-rate-limits).

---

## HTTP status codes

| Code | Meaning |
|------|---------|
| 200 | OK: the request succeeded |
| 201 | Created: the resource was created |
| 400 | Bad Request: input failed validation |
| 401 | Unauthorized: token missing, expired, or revoked |
| 403 | Forbidden: your role or token scopes do not allow this |
| 404 | Not Found: the resource does not exist, or you cannot see it |
| 409 | Conflict: the resource changed, or a duplicate exists |
| 410 | Gone: API v1 endpoint called after 2026-11-16 |
| 429 | Too Many Requests: wait for the `Retry-After` time |
| 5xx | Server error: retry with exponential backoff |

Orbitask error codes (`ORB001`–`ORB006`) are listed in [Error codes](user-manual.md#error-codes).

---

## Roles at a glance

Roles are assigned per workspace and inherited by every project. The full permissions table is in [Roles and permissions](user-manual.md#roles-and-permissions).

| Role | In short |
|------|----------|
| **Owner** | Everything, including SSO, SCIM, billing, and deleting the workspace |
| **Admin** | Manages members, project settings, webhooks, and agents |
| **Member** | Creates projects, tasks, comments, and reports |
| **Viewer** | Read-only access |

---

## CLI commands

| Task | Command |
|------|---------|
| Sign in | `orbitask login --workspace <WORKSPACE>` |
| Set a default | `orbitask config set default-project <PROJECT>` |
| List tasks | `orbitask task list --project <PROJECT> --status in-progress` |
| Create a task | `orbitask task create --title "<TITLE>" [--assignee <EMAIL>]` |
| Change task status | `orbitask task update <TASK-ID> --status <STATUS>` |
| Import tasks from CSV | `orbitask import tasks --file <FILE.csv> --project <PROJECT> [--dry-run]` |
| Export a project | `orbitask export project <PROJECT> --format json --output <FILE>` |
| Invite a member | `orbitask team invite <EMAIL> --role <owner\|admin\|member\|viewer>` |
| Create an API token | `orbitask auth token create --name <NAME> --scope <SCOPES>` |
| Send a test webhook | `orbitask webhook test <WEBHOOK-ID> --event task.created` |
| Check workspace health | `orbitask workspace health` |
| Create a diagnostics bundle | `orbitask diagnostics bundle --output <FILE.zip>` |
| Check the agent (on the agent host) | `orbitask-agent status` |

## CLI configuration

| Environment variable | Purpose | Default |
|----------------------|---------|---------|
| `ORBITASK_API_TOKEN` | Token used when you are not signed in interactively | None |
| `ORBITASK_API_URL` | API base URL | `https://api.orbitask.example/v2` |
| `ORBITASK_WORKSPACE` | Workspace to use | The one chosen at `orbitask login` |

---

## Request flow

![Client request flow through the API gateway](./img/visual-overview.svg)

## Example API calls

```bash
# Health check (no token needed)
curl -i https://api.orbitask.example/v2/health

# List projects
curl -H "Authorization: Bearer <TOKEN>" https://api.orbitask.example/v2/projects
```
