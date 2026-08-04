---
title: Observability
tags:
  - architecture
status: draft
---

# Observability

Enough to debug under time pressure, no more.

## Logging

- [ ] One structured line per pipeline stage: stage, duration, input id, outcome
- [ ] Errors carry the input id so a failure is reproducible from fixtures

## What we need to see live during the demo

| Signal | Why | Where shown |
|---|---|---|
| Pipeline stage timings | Spot the stall | {{LOCATION}} |
| Provider call success/failure | Know if we're on fallback | |
| {{SIGNAL}} | | |

> [!todo] Not filled in yet


> [!tip] Debuggability beats dashboards
> At a hackathon the win condition is "reproduce the failure from a fixture in
> under a minute". Build for that, not for graphs.

---
Related: [[03-Data-Flow]] · [[05-Demo-Reliability]] · [[07-Blocker-Log]] · [[08-Deployment]]
