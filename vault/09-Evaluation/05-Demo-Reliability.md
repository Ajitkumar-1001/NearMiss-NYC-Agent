---
title: Demo Reliability
tags:
  - evaluation
status: draft
---

# Demo Reliability

The demo working is the highest-value property this project has. Treat it as a
requirement, not a hope.

## Guarantees

| Property | How it's guaranteed | Verified |
|---|---|---|
| Runs with network off | Fixture path ([[ADR-001-Deterministic-Demo-First]]) | [ ] |
| Provider outage invisible | Adapter fallback ([[07-Provider-Adapters]]) | [ ] |
| Same result every run | Deterministic fixtures, fixed seeds | [ ] |
| Resets in under {{RESET_SECONDS}}s | {{RESET_METHOD}} | [ ] |
| Runs on the demo machine | Rehearsed on it | [ ] |

## Failure drill

Rehearse these, don't just plan for them:

- [ ] Kill the network mid-demo → does it keep going?
- [ ] Force a provider error → is it visible to the audience?
- [ ] Restart from cold → how long to demo-ready?
- [ ] Laptop switches / projector resolution changes

## Rehearsals

| # | Date | Full run? | Broke on | Fixed |
|---|---|---|---|---|
| 1 | | | | |

> [!todo] Not filled in yet
> Two clean end-to-end rehearsals minimum — [[08-Definition-of-Done]].

---
Related: [[ADR-001-Deterministic-Demo-First]] · [[04-Demo-Script]] · [[05-QA-Checklist]] · [[06-Risk-Register]]
