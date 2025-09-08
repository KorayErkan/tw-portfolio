# Security & Compliance Overview

**Author:** John Saysitall (portfolio sample)
**Version:** 0.1 — <update date here>

---

## Trust Model & Responsibilities

- **Vendor responsibilities:** Application security, infrastructure hardening, incident response protocols
- **Customer responsibilities:** Identity provider configuration, user access governance, endpoint protection

---

## Identity & Access Management

- Single Sign-On integration (SAML/OIDC protocols)
- Multi-Factor Authentication with conditional enforcement
- Role-Based Access Control implementing least privilege principles

---

## Data Protection

- **In transit:** TLS 1.2+ encryption for all network communications
- **At rest:** AES-256 encryption for databases and object storage systems
- **Key management:** Automated 12-month rotation cycles via dedicated KMS
- **Data residency:** Configurable EU/US regional data localization

---

## Compliance

- SOC 2 Type II certification with annual renewals
- ISO/IEC 27001 information security management certification
- GDPR-compliant Data Processing Addendum available
- Comprehensive audit trails with JSON/CSV export capabilities

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

- Comprehensive threat modeling integrated into design phases
- Automated SAST and dependency vulnerability scanning
- Annual third-party penetration testing assessments
- Secure CI/CD pipelines with cryptographically signed artifacts

```graphviz
// data-security-layers.dot
digraph G {
  graph [rankdir=TB, splines=true, bgcolor="transparent", nodesep=0.6, ranksep=0.8];
  node  [shape=rounded, style="filled,rounded", fillcolor="#161b22", color="#30363d", fontcolor="#c9d1d9", penwidth=1.2];
  edge  [color="#8b949e", arrowsize=0.8, penwidth=1.2];

  subgraph cluster_external {
    label="External Access";
    labelloc="t"; fontsize=12;
    color="#30363d"; fontcolor="#c9d1d9"; style="rounded,dashed";
    client [label="Client Applications"];
  }

  subgraph cluster_transport {
    label="Transport Security";
    labelloc="t"; fontsize=12;
    color="#30363d"; fontcolor="#c9d1d9"; style="rounded,dashed";
    tls [label="TLS 1.2+ Encryption", fillcolor="#0d1117", penwidth=1.6];
    waf [label="Web Application Firewall"];
  }

  subgraph cluster_application {
    label="Application Security";
    labelloc="t"; fontsize=12;
    color="#30363d"; fontcolor="#c9d1d9"; style="rounded,dashed";
    auth [label="SSO/MFA Authentication"];
    rbac [label="RBAC Authorization"];
    api [label="API Gateway"];
  }

  subgraph cluster_data {
    label="Data Security";
    labelloc="t"; fontsize=12;
    color="#30363d"; fontcolor="#c9d1d9"; style="rounded,dashed";
    encrypt [label="AES-256 Encryption", fillcolor="#0d1117", penwidth=1.6];
    kms [label="Key Management Service"];
    db [label="Encrypted Database", shape=folder];
  }

  client -> tls -> waf -> auth -> rbac -> api -> encrypt -> db;
  kms -> encrypt [label="key rotation", style=dotted];
}
```

---

## Incident Response

- **Response framework:** Containment, investigation, remediation, and communication protocols
- **Notification requirements:**
  - Regulatory compliance within 72 hours (GDPR mandates)
  - Customer breach notification within 24 hours of confirmation
- **RACI accountability:** Defined ownership across Operations, Security, Legal, and Communications teams
