# Security & Compliance Overview

**Author:** Koray Erkan (portfolio sample)
**Version:** 0.1 — <update date here>

---

## Trust Model & Responsibilities

- **Vendor responsibilities:** application security, infrastructure hardening, incident response
- **Customer responsibilities:** identity provider configuration, user role assignment, endpoint security

---

## Identity & Access Management

- Single Sign-On (SAML / OIDC)
- Multi-Factor Authentication (MFA) enforcement
- Role-Based Access Control (RBAC) with least privilege

---

## Data Protection

- **In transit:** TLS 1.2+ encryption for all traffic
- **At rest:** AES-256 encryption for databases and object storage
- **Key management:** rotation every 12 months; managed by KMS
- **Data residency:** choice of EU/US regions

---

## Compliance

- SOC 2 Type II (renewed annually)
- ISO/IEC 27001 certified
- GDPR-compliant Data Processing Addendum (DPA)
- Audit trails exportable in JSON or CSV

Example audit log:

```json
{
  "timestamp": "2025-09-08T12:45:33Z",
  "user": "alice@example.com",
  "action": "ROLE_CHANGE",
  "target": "project:12345",
  "old_role": "viewer",
  "new_role": "admin"
}
```

---

## Secure SDLC Practices

- Threat modeling during design phase
- Automated static code analysis (SAST) and dependency scanning
- Penetration testing annually
- CI/CD pipelines with signed artifacts

---

## Incident Response

- **Runbook:** contain, investigate, remediate, communicate
- **Notification timelines:**
  - Regulatory notifications within 72 hours (GDPR)
  - Customer notification within 24 hours of confirmed breach
- **RACI matrix:** clearly defined ownership (Ops, Security, Legal, Comms)
