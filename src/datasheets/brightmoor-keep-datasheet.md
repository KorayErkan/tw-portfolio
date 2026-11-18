# Brightmoor Keep 3.2

**A private AI assistant that answers from your own documents, on your own servers.**

Banks and hospitals want generative AI, but they can't send contracts, patient records, or source code to a public cloud. Brightmoor Keep runs the language model, search index, and chat interface inside your network. Staff ask in plain language and get answers linked to their source paragraphs. No prompt, document, or answer leaves the building.

## Why teams choose Keep

| Requirement | How Keep meets it |
|-----------------------|-----------------------------------------------------------------|
| Data stays in-house | Model, index, and logs run on your hardware, even fully air-gapped. |
| Answers can be checked | Every answer cites its sources. With no source, Keep says so instead of guessing. |
| Permissions hold | Answers use only documents the user can already open, per Entra ID or AD groups. |
| Every answer is traceable | A tamper-evident audit log records each question, answer, source, and model version, and streams to your SIEM. |
| Cost is predictable | One annual license per GPU server. No per-user or per-token fees. |

## How it works

1. **Connect your sources:** SharePoint, SMB file shares, Confluence, Jira, PostgreSQL, and S3-compatible storage.
2. **Keep indexes them** and syncs changes every 15 minutes. Deleted documents leave the index on the next sync.
3. **Staff ask questions** in the web app, in Microsoft Teams, or through the REST API from your own tools.

## System requirements

| | Pilot | Standard | Large |
|------------------------|----------------------|----------------------|----------------------|
| Concurrent users | 50 | 300 | 1,500 |
| Indexed documents | 200,000 | 2 million | 10 million |
| GPU | 1 × NVIDIA L40S 48 GB | 2 × NVIDIA L40S 48 GB | 4 × NVIDIA H100 80 GB |
| CPU and RAM | 16 cores, 128 GB | 32 cores, 256 GB | 64 cores, 512 GB |
| Storage | 2 TB NVMe | 4 TB NVMe | 8 TB NVMe |

Sizing assumes the bundled Keep-M model and a median answer time under 4 seconds. Runs on Ubuntu 22.04 or 24.04 LTS or Red Hat Enterprise Linux 9, on one server or on Kubernetes 1.28+ via Helm. Air-gapped sites get an offline installer.

## Security and compliance

- **Encryption:** TLS 1.3 in transit and AES-256 at rest, with keys in your HSM or key manager over KMIP.
- **Sign-in:** SAML 2.0 or OpenID Connect, with admin, curator, and user roles.
- **Models:** bundled open-weight models, or your own via an OpenAI-compatible endpoint. Never trained on your data.
- **Regulation:** data never leaves your site (GDPR data residency), and answers are labeled as AI-generated and logged with their model (EU AI Act transparency). Keep supports compliance; it doesn't certify it.

## Editions

| | Team | Enterprise |
|-------------------------|-------------------------------|-------------------------------|
| GPU servers | 1 | Unlimited |
| Connectors | Any 3 | All, plus the connector SDK |
| Microsoft Teams app | No | Yes |
| High availability | No | Active-passive cluster |
| Support | Business hours, next business day | 24/7, 1-hour response for severity 1 |

## Start a pilot

A 30-day pilot license runs on your hardware, against your documents, with a Brightmoor engineer on call.

- **Sales and pilots:** <sales@brightmoor.example>, +44 20 7946 0123
- **Authorized reseller:** One-Stop Shopping, <https://www.one-stop-shopping.com>

*Datasheet BK-DS-3.2-EN, November 2026. Specifications may change without notice. Brightmoor Labs is fictional.*
