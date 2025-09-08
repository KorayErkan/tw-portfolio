# Maintenance & Troubleshooting

**Author:** Koray Erkan (portfolio sample)
**Version:** 0.1 — <update date here>

---

## Routine Maintenance

- [ ] Verify backups complete successfully (weekly)
- [ ] Perform test restores (monthly)
- [ ] Review data retention policies (quarterly)
- [ ] Rotate API keys and secrets (annually or on compromise)

---

## Monitoring

- [ ] Check health endpoints (`/health`, `/status`)
- [ ] Aggregate logs in SIEM/ELK stack
- [ ] Review alerts against thresholds (CPU, memory, latency, error rates)

Example health check:

```bash
curl -s https://api.acmecloud.example/v1/health | jq
```

```graphviz
// webhooks-eventing-topology.dot
digraph G {
  graph [rankdir=LR, splines=true, bgcolor="transparent", nodesep=0.7, ranksep=0.8];
  node  [shape=rounded, style="filled,rounded", fillcolor="#161b22", color="#30363d", fontcolor="#c9d1d9", penwidth=1.2];
  edge  [color="#8b949e", arrowsize=0.85, penwidth=1.2];

  subgraph cluster_prod {
    label="Producer (SaaS)";
    labelloc="t"; fontsize=12;
    color="#30363d"; fontcolor="#c9d1d9"; style="rounded,dashed";
    svc1 [label="Projects Service"];
    svc2 [label="Reporting Service"];
    svc3 [label="Auth Service"];
  }

  bus   [label="Event Bus\n(topic: project.*, report.*, user.*)", shape=folder, fillcolor="#0d1117", penwidth=1.6];
  xform [label="Webhook Formatter\n(JSON payload, HMAC-SHA256)"];
  retry [label="Retry Worker\n(exp backoff)"];
  dlq   [label="Dead-letter Queue"];

  subgraph cluster_cust {
    label="Customer Side";
    labelloc="t"; fontsize=12;
    color="#30363d"; fontcolor="#c9d1d9"; style="rounded,dashed";
    wh1 [label="Endpoint A\nhttps://hooks.example.com/inbound"];
    wh2 [label="Endpoint B\nhttps://api.partner.tld/webhooks"];
    mon [label="Monitoring / SIEM\n(status, latency, failure rate)"];
  }

  // flows
  svc1 -> bus; svc2 -> bus; svc3 -> bus;
  bus  -> xform [label="event"];
  xform -> wh1  [label="POST (HMAC header)"];
  xform -> wh2  [label="POST (HMAC header)"];

  // retry paths on non-2xx
  wh1 -> retry [label="non-2xx", color="#d29922"];
  wh2 -> retry [label="timeout", color="#d29922"];
  retry -> wh1  [label="re-deliver"];
  retry -> wh2  [label="re-deliver"];
  retry -> dlq  [label="max attempts", color="#f85149"];

  // observability
  xform -> mon  [label="delivery metrics"];
  retry -> mon  [label="retries, DLQ"];
}
```

---

## Troubleshooting Playbooks

| Symptom            | Likely Cause        | Resolution |
|--------------------|---------------------|------------|
| Login loop         | IdP misconfiguration | Verify ACS URL, certificate, and system clock |
| Webhooks not firing| Firewall / DNS       | Check firewall allowlist, retry policy |
| Slow exports       | Large datasets       |
