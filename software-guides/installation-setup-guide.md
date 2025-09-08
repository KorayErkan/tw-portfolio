# Installation and Setup Guide (SaaS + Optional Self-Hosted Agent)

**Author:** John Saysitall (portfolio sample)
**Version:** 0.1 — <update date here>

> 🎯 **Purpose**
> Ensure a smooth first-time setup. Audience: Admins/IT. Scope: prerequisites, installation, configuration, validation, rollback.

---

## Prerequisites

| Category | Requirement | Notes |
|----------|-------------|-------|
| Identity Provider | SAML or OIDC compatibility | Okta, Azure AD, Google Workspace supported |
| Network Connectivity | HTTPS egress to `*.goodweb.com` | Corporate firewall/proxy allowlist configuration required |
| Browser Support | Latest Chrome/Edge/Firefox/Safari | Cookie and local storage functionality enabled |
| Administrative Access | Organization Admin privileges | Required for SSO, SCIM, billing, and configuration management |
| (Agent) Operating System | Linux x86_64 (Ubuntu 20.04+/RHEL 8+) | Minimum: 2 vCPU, 4 GB RAM, 10 GB storage |
| (Agent) Network | Outbound HTTPS (443) only | No inbound connectivity requirements |

---

## Cloud Installation

1. **Organization registration**
   Navigate to `https://app.cloudflow.goodweb.com` and establish your organizational account.
2. **Domain ownership verification**
   Configure the provided TXT record in DNS management, then execute **Verify**.
3. **Billing configuration (optional)**
   Select subscription tier, configure payment method, designate invoice recipient.
4. **Administrative setup**
   Define organization name, timezone preferences, and default regional deployment.

---

## Optional: Self-Hosted Agent

### System Requirements

- Linux x86_64 architecture with 2 vCPU, 4 GB RAM, 10 GB storage minimum
- Outbound HTTPS connectivity (port 443) to `agent.cloudflow.goodweb.com`
- Systemd service management capability for daemon operations

### Install Example

```bash
curl -fsSL https://downloads.cloudflow.goodweb.com/agent/v1.2.3/agent-linux-amd64.tgz -o agent.tgz
tar xzf agent.tgz && sudo mv agent /usr/local/bin/agent
sudo systemctl enable --now agent
sudo systemctl status agent
```
![Agent Connectivity](./images/agent-connectivity.svg)

### Health Check

```bash
curl -I https://agent.cloudflow.goodweb.com/health
```

---

## Configuration

### Single Sign-On (SAML/OIDC)

- Configure Identity Provider parameters:
  - **ACS / Redirect URI:** `https://app.cloudflow.goodweb.com/auth/callback`
  - **Entity ID:** `https://app.cloudflow.goodweb.com`
- Import IdP metadata or establish client credential configuration.
- Execute pilot group testing before production enforcement.

![SSO Flow](./images/sso-flow.svg)

### SCIM Provisioning

- Activate SCIM functionality via **Admin → Provisioning**.
- Configure Identity Provider with base URL and bearer token authentication.
- Validate single group synchronization before full production deployment.

### API Keys and Webhooks

- **API Keys:** Generate with minimal required permissions following least-privilege principles.
- **Webhooks:** Configure endpoint URLs, validate 2xx response codes, establish retry policies.

---

## Validation and Smoke Tests

- [ ] Authenticate via SSO with pilot user account
- [ ] Establish workspace and initial project
- [ ] Execute teammate invitation workflow and validate sign-in
- [ ] Create and assign task, verify activity logging
- [ ] Generate CSV report export and validate data/timezone accuracy
- [ ] (Agent deployment) Confirm **Healthy** status in **Admin → Connectors**

---

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| SSO authentication loops | ACS/Audience configuration mismatch, clock synchronization issues | Validate IdP configuration parameters; ensure NTP synchronization |
| Post-SSO authorization failure | Role mapping not configured | Establish IdP group to application role mapping; execute resynchronization |
| Webhook delivery failures | Network firewall or proxy restrictions | Configure destination allowlists; verify retry policy settings |
| Export performance degradation | Large dataset processing overhead | Implement asynchronous exports; apply filtering or pagination |
| Agent connectivity issues | Authentication token expiration, network egress restrictions | Execute token rotation; verify outbound HTTPS/DNS connectivity |

---

## Rollback

1. Disable SSO enforcement, reverting to optional authentication.
2. Suspend SCIM user provisioning operations.
3. Terminate and uninstall agent service daemon.
4. Remove DNS TXT verification records during decommissioning.
5. Validate backup integrity and data exports before complete rollback execution.
