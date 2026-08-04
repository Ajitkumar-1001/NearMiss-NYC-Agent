---
title: Live Feeds
tags:
  - research
status: draft
---

# Live Feeds

Real-time sources. Treated as an enhancement, never a demo dependency.

## Candidates

| Feed | Endpoint | Auth | Rate limit | Latency | Reliability |
|---|---|---|---|---|---|
| {{FEED}} | {{ENDPOINT}} | | | | |

> [!todo] Not filled in yet


## Failure behaviour

If a feed is down mid-demo the system must degrade to fixtures without a visible
error. Covered by [[05-Demo-Reliability]] and enforced through
[[07-Provider-Adapters]].

## Open questions

- [ ] Terms of use permit our access pattern? → [[02-Rules-and-Constraints]]
- [ ] Do we need to cache/replay to avoid rate limits?

---
Related: [[01-Datasets]] · [[07-Provider-Adapters]] · [[05-Demo-Reliability]] · [[03-Data-Flow]]
