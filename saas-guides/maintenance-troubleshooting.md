# Maintenance & Troubleshooting

## Routine Maintenance

- Backups (policy/schedule/restore test)
- Data retention
- Key rotation

## Monitoring

- Health endpoints
- Log aggregation
- Alert thresholds

## Troubleshooting Playbooks

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Login loop | IdP misconfiguration | Re-check ACS URL, certificate, clock skew |
| Webhooks not firing | Firewall / DNS | Verify allowlist, retry policy |
| Slow exports | Large datasets | Start async export, paginate inputs |

## Escalation Matrix

Tiered support and SLAs.
