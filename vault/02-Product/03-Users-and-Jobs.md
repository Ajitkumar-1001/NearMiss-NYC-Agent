---
title: Users and Jobs
tags:
  - product
status: active
---

# Users and Jobs

> [!info] Source
> [[PRD]] §6 and §7.

## Primary user

- **Who:** a transportation-safety analyst.
- **Job to be done:** when they review a street-safety event, they want to
  understand what happened, why it may be risky, what evidence supports the
  alert, and how uncertain the system is, so they can decide whether the
  location deserves further investigation.
- **Today they:** review footage manually — slow, expensive, inconsistent — or
  work from lagging crash records that only describe harm already done.

## Supporting jobs

- Replay the relevant video segment with visible tracks.
- Identify the road users involved in the potential conflict.
- See the factors contributing to the risk score.
- Distinguish model observations from external historical context.
- Understand limitations and missing evidence.
- Export or share a structured event record.

## Secondary users

| User | Job | Priority |
|---|---|---|
| Urban planners | Evaluate intersection design | secondary |
| Vision Zero and transportation researchers | Study recurring conflict patterns | secondary |
| Civic-technology teams | Build on the structured event record | secondary |
| Traffic-operations teams | Prioritise locations for review | secondary |
| Community organizations | Document street-safety concerns with evidence | secondary |

## Non-users

Who we are explicitly not building for — keeps [[04-MVP-Scope]] honest. The MVP
is **not** designed for:

- Law-enforcement identification or automated enforcement
- Emergency dispatch
- Insurance adjudication
- Individual behaviour scoring
- Facial recognition or personal identification
- Fully autonomous infrastructure decisions

These are load-bearing constraints, not preferences — see
[[ADR-006-No-Identity-Recognition]] and [[10-Responsible-AI]].

---
Related: [[PRD]] · [[02-Problem-Statement]] · [[04-MVP-Scope]] · [[07-Demo-Story]] · [[ADR-006-No-Identity-Recognition]]
