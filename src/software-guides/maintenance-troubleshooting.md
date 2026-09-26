# Maintenance and Troubleshooting

**Author:** John Saysitall  
**Version:** Orbitask 1.8.0 · August 2026

> **Who this is for:** Workspace Owners and Admins.
> Orbitask runs and maintains the service itself: servers, databases, service backups, and failover. This guide covers what you control: your workspace, members, integrations, and self-hosted agents. For service-wide incidents, check `https://status.orbitask.example`.

---

## Routine maintenance

| Task | How often | Where | Role needed |
|------|-----------|-------|-------------|
| [Check workspace health](#check-workspace-health) | Weekly | **Admin → Workspace health** | Admin |
| Review members and remove people who have left | Monthly | **Admin → Members** | Admin |
| [Rotate API tokens and webhook secrets](#rotate-api-tokens-and-webhook-secrets) | Every 12 months, and when someone with access leaves | **Settings → API tokens**, **Admin → Webhooks** | Admin |
| [Update self-hosted agents](#update-the-agent) | Within 30 days of each release | Agent host | Admin (plus `sudo` on the host) |
| [Export your data](#export-your-data) | Monthly, or as your retention policy requires | **Admin → Data export** | Owner |
| Review the audit log | Monthly | **Admin → Audit log** | Owner |
| Read the [release notes](release-notes.md) for deprecations | Each release | This documentation | Any |

> **Upcoming deadline:** API v1 stops working on **2026-11-16**. Use the **API v1 calls** tile in workspace health to find integrations that still use it.

Role details are in [Roles and permissions](user-manual.md#roles-and-permissions).

### Check workspace health

1. Go to **Admin → Workspace health**.
2. Review each tile. Tiles turn yellow at the warning level and red at the critical level.

| Tile | Healthy | Warning | Critical | If it is not healthy |
|------|---------|---------|----------|----------------------|
| **API latency (p95)**, your workspace | Under 500 ms | 500–999 ms | 1,000 ms or more | Check the status page; see [API errors and rate limits](#api-errors-and-rate-limits) |
| **Webhook success rate** (24 h) | 99% or more | 95–98.9% | Under 95% | See [Webhook delivery failures](#webhook-delivery-failures) |
| **Agents** | All **Healthy** | Any **Degraded** | Any **Offline** for 15 minutes | See [Agent troubleshooting](#agent-troubleshooting) |
| **SCIM sync** | Last sync succeeded | Warnings in last sync | Last sync failed | See [SSO and SCIM issues](#sso-and-scim-issues) |
| **API v1 calls** (7 days) | 0 | Any | — | Move the listed integrations to API v2 |

The same data is available from the CLI:

```bash
orbitask workspace health
```

### Rotate API tokens and webhook secrets

**API tokens**

1. Create a new token with the same scopes: `orbitask auth token create --name "ci-integration-2026" --scope "projects:read,tasks:write"`.
2. Update the integration to use the new token and confirm that it works.
3. Revoke the old token: `orbitask auth token revoke <OLD-TOKEN-ID>`.

**Webhook signing secrets**

1. In **Admin → Webhooks**, open the webhook and click **Rotate secret**. For 24 hours, Orbitask signs each request with both the old and the new secret, so the `Orbitask-Signature` header contains two `v1` values.
2. Deploy the new secret to your endpoint within those 24 hours. The verification code in [Verifying webhook signatures](user-manual.md#verifying-webhook-signatures) accepts either value.
3. Click **Expire old secret**, or let it expire automatically.

### Update the agent

Agents 1.7.x keep working with Orbitask 1.8.0, but update within 30 days of a release to get fixes.

1. Download and verify the new version as in [Install the agent](installation-setup-guide.md#install-the-agent), steps 1–2.
2. Replace the binary and restart the service:

   ```bash
   tar -xzf orbitask-agent_1.8.0_linux_amd64.tar.gz
   sudo install -m 0755 orbitask-agent /usr/local/bin/orbitask-agent
   sudo systemctl restart orbitask-agent
   ```

3. Run `orbitask-agent status`. *Result:* `Agent: 1.8.0` and `Connection: connected`.

You do not need to enroll the agent again.

### Monitor the agent from your own tools

**Admin → Workspace health** alerts Admins by email when an agent goes offline. If you also want your own monitoring to check the agent, run a check every minute with cron. For example, save this script as `/usr/local/bin/check-orbitask-agent`:

```bash
#!/bin/sh
# Exits non-zero, and logs to syslog, if the Orbitask agent is not running and connected.
if ! systemctl is-active --quiet orbitask-agent; then
  logger -p user.err "orbitask-agent: service is not running"
  exit 1
fi
if ! orbitask-agent status --quiet; then
  logger -p user.warning "orbitask-agent: running but not connected"
  exit 2
fi
```

Make it executable (`sudo chmod 0755 /usr/local/bin/check-orbitask-agent`) and add this line to root's crontab with `sudo crontab -e`:

```text
* * * * * /usr/local/bin/check-orbitask-agent
```

Point your log monitoring at the `orbitask-agent:` messages.

### Export your data

Orbitask backs up the service so it can recover from its own failures. Those backups are not a way to restore individual items you deleted. For your own records, compliance archives, or leaving the service, export your data.

1. Go to **Admin → Data export** and click **Export workspace**. Choose JSON (full fidelity, including comments and history) and **Include attachments**.
   Or use the CLI:

   ```bash
   orbitask export workspace --format json --include-attachments --output acme-eng-2026-09.zip
   ```

2. Wait for the email with the download link. Large workspaces can take several hours. Links expire after 7 days.
3. Check the export. The archive contains `manifest.json` with an item count and a SHA-256 checksum for each file:

   ```bash
   orbitask export verify acme-eng-2026-09.zip
   ```

   *Result:* `Export OK: 12 projects, 4,318 tasks, 1,902 attachments`.
4. Store the export somewhere your organization controls, with access limited to the people who need it. The export contains personal data.

How long Orbitask keeps deleted items and logs is described in [Data retention](security-compliance.md#data-retention).

---

## Troubleshooting

Before you start, check `https://status.orbitask.example`. If there is an active incident, you do not need to troubleshoot your workspace.

### Agent troubleshooting

Start with the agent's own status and logs on the host:

```bash
orbitask-agent status
journalctl -u orbitask-agent --since "1 hour ago"
orbitask-agent check-connectivity
```

`check-connectivity` tests DNS, the proxy (if configured), TLS, and authentication, and names the first step that fails.

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `Service: inactive` or `failed` | The service stopped or cannot start | Run `sudo systemctl start orbitask-agent`, then read `journalctl` for the error |
| `DNS lookup failed for agent.orbitask.example` | Internal DNS cannot resolve the domain | Ask your network team to allow resolution of `*.orbitask.example` |
| `TLS handshake failed` or `certificate signed by unknown authority` | A proxy inspects TLS traffic | Exempt `agent.orbitask.example` from TLS inspection, or add your proxy's CA with `orbitask-agent config set tls.ca_file /path/to/ca.pem` |
| `401 agent credentials rejected` | The agent was removed in **Admin → Connectors**, or its credentials were revoked | Create a new enrollment token and run `sudo orbitask-agent enroll --token <TOKEN> --force` |
| Agent shows **Degraded** | Clock drift of more than 5 minutes, or disk more than 90% full | Enable NTP on the host; free disk space under `/var/lib/orbitask-agent` |

### SSO and SCIM issues

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Sign-in loops back to the sign-in page | Redirect URI, ACS URL, or audience does not match | Compare the IdP settings with [Single sign-on](installation-setup-guide.md#single-sign-on-saml-or-oidc) |
| `Assertion expired` or `Token not yet valid` | Clock drift between the IdP and Orbitask | Make sure the IdP's clock is synchronized with NTP |
| SAML sign-in fails after working before | The IdP signing certificate changed or expired | Upload the IdP's new metadata in **Admin → Security → Single sign-on** |
| New employees cannot sign in: `No account` | SCIM has not provisioned them yet | In **Admin → Security → Provisioning**, click **Sync now** and read the sync log |
| Users have the wrong role | IdP group mapped to the wrong role, or the user is in several mapped groups | Check the group mappings. When a user is in several groups, Orbitask gives the highest role |
| Microsoft Entra ID groups do not sync | Entra ID SCIM is in preview and syncs only assigned groups, not nested groups | Assign the groups directly to the Orbitask application in Entra ID |

If SSO is broken and nobody can sign in, an Owner can still sign in at `https://app.orbitask.example/login?sso=bypass` with the email address and password set when the workspace was created, then fix or turn off **Require SSO**.

### Webhook delivery failures

1. Go to **Admin → Webhooks**, open the webhook, and select **Deliveries**.
2. Filter by **Failed** and open a delivery to see the request, the response status, and the response body your endpoint returned.
3. Use this table to find the cause:

| What the delivery log shows | Likely cause | What to do |
|-----------------------------|--------------|------------|
| `Timeout after 10 s` | Your endpoint does slow work before responding | Return `2xx` right away and process the event in the background |
| `Connection refused` or `DNS error` | Endpoint is down, or its address changed | Check that the URL is correct and reachable from the internet |
| `401` or `403` from your endpoint | Your signature check rejects the request | Verify against the **raw** body, use the current secret, and make sure your server clock is correct (tolerance is 300 s) |
| `4xx` other than 401/403 | Your endpoint rejects the payload | Check your endpoint's logs for the reason |
| `5xx` | Your endpoint failed | Fix the endpoint; Orbitask keeps retrying for about 24 hours |

1. After you fix the endpoint, redeliver failed events: select them and click **Redeliver**, or run `orbitask webhook redeliver --webhook wh_123 --status failed --since 2026-09-01`.

Because events can arrive more than once after a redelivery, de-duplicate them by their `id` field.

### API errors and rate limits

Each API token can make up to 1,000 requests per minute. Every response includes these headers:

| Header | Meaning |
|--------|---------|
| `X-RateLimit-Limit` | Requests allowed per minute (1000) |
| `X-RateLimit-Remaining` | Requests left in the current minute |
| `X-RateLimit-Reset` | Unix time when the limit resets |
| `Retry-After` | On a `429` response only: seconds to wait before retrying |

When you receive an error:

- **429 Too Many Requests (ORB003):** Wait for the `Retry-After` time, then retry. Spread bulk jobs over time or use bulk endpoints such as `/v2/tasks/bulk-update`.
- **5xx errors:** Retry with exponential backoff (for example, 1 s, 2 s, 4 s, up to 5 attempts). Send an `Idempotency-Key` header with writes so that a retry cannot create a duplicate.
- **410 Gone (ORB006):** The request used API v1 after 2026-11-16. Change the URL from `/v1/` to `/v2/`; see [Release Notes](release-notes.md#deprecations).
- Until then, API v1 responses include `Deprecation` and `Sunset` headers, which many HTTP clients can log as warnings.

The full list of error codes is in [Error codes](user-manual.md#error-codes).

### Slow reports and exports

- Filter large reports by project, date range, or status.
- Reports with more than 10,000 rows always run in the background; Orbitask emails a link when they are ready.
- Scheduled reports run between 00:00 and 06:00 in the workspace time zone. Stagger them if many start at the same time.

---

## Contact support

If you cannot fix a problem, contact support with a diagnostics bundle. It helps support find the cause without back-and-forth.

1. **Create a workspace diagnostics bundle.** Go to **Admin → Workspace health → Download diagnostics**, or run:

   ```bash
   orbitask diagnostics bundle --since "24 hours ago" --output orbitask-diag.zip
   ```

   The bundle contains workspace settings, recent error logs, webhook delivery results, and SSO/SCIM sync logs. It does **not** contain task content, comments, attachments, or secrets; tokens and secrets are redacted.
2. **If the problem involves the agent**, also create an agent bundle on the host:

   ```bash
   sudo orbitask-agent diagnostics --output orbitask-agent-diag.tar.gz
   ```

3. **Open a support request** from **Help → Contact support**, or email `support@orbitask.example`. Include:
   - What you expected and what happened instead
   - When it started, and whether anything changed around that time
   - The request ID (`X-Request-Id` header) of a failing API call, if you have one
   - The diagnostics bundles

| Severity | Example | First response: Standard plan | First response: Enterprise plan |
|----------|---------|-------------------------------|---------------------------------|
| **Critical** | No one in the workspace can sign in | 4 hours | 1 hour, 24/7 |
| **High** | Webhooks or an agent have stopped working | 8 business hours | 4 hours |
| **Normal** | A report is slow; a how-to question | 2 business days | 1 business day |
