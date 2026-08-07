---
title: ADR-007 Cloud Run Eligibility Gate
tags:
  - adr
status: active
---

# ADR-007 — Cloud Run Eligibility Gate

## Status

Accepted — [[00-Source-of-Truth-PRD|PRD]] §29, approved for version 2.1.

Supersedes any earlier decision treating Cloud Run as a deployment preference or
a sponsor-only nicety.

## Context

Earlier vault revisions treated Google Cloud Run as the preferred deployment
target — a sponsor alignment choice, weighed against effort like any other.

Retrieved registration material states it differently: **deployment on Google
Cloud Run is the only stated eligibility gate**
([[06-Hackathon-Compliance-Checklist]], organizer-stated). That is not a
preference. It is a pass/fail condition applied before the work is judged on its
merits.

The failure mode this guards against is specific and common: a team with a
working local system, a good demo, and no deployed URL at 8:30 PM. Every
judging dimension in [[00-Source-of-Truth-PRD|PRD]] §2.3 is worth zero if the submission is
incomplete.

## Decision

**A publicly reachable Cloud Run agent is a hard eligibility gate, not a
deployment preference.** Per [[00-Source-of-Truth-PRD|PRD]] §2.2 the service shall:

- Be publicly reachable without judge authentication
- Return HTTP 200 from `GET /health`
- Expose at least one working real-source analysis endpoint
- Identify the deployed revision and active processing mode
- Remain available during the demo window

Failure to satisfy §2.2 means the submission is not hackathon-complete **even
when the local application works**.

Two consequences follow, both locked in §29:

1. Deployment moves into the **pre-event** readiness baseline ([[00-Source-of-Truth-PRD|PRD]] §11.1),
   with a public revision verified from a logged-out browser before arrival. It
   is not a Friday task.
2. Anything that endangers the deployed agent is subordinate to it. The Next.js
   dashboard is preferred **but not allowed to endanger the Cloud Run agent**
   (§29). CPU-first; GPU is optional.

## Consequences

**Positive**
- The one disqualifying condition is closed before the event starts.
- Forces the platform constraints — `0.0.0.0:$PORT`, statelessness, public
  invoker, billing enabled — to surface in rehearsal instead of on stage.
- A known-good revision and rollback command exist before they are needed.

**Negative**
- Pre-event hours go to infrastructure rather than product.
- A cloud project with billing enabled must exist on a personal Gmail account,
  with the cost exposure that implies ([[06-Risk-Register]]).
- Deployed-path bugs are slower to diagnose than local ones.

**Accepted trade-off**
- The dashboard is explicitly demotable. If the frontend threatens the deployed
  agent, the frontend loses — see [[03-Scope-Ladder]].

## Alternatives considered

| Alternative | Why not |
|---|---|
| Deploy on Friday during the build window | Puts the one disqualifying condition on the critical path, at the hour with least slack |
| Any other host, or a tunnel to a laptop | Not Cloud Run; fails the stated gate regardless of reachability |
| Local demo plus a recording | §2.2 is explicit — a working local application is not hackathon-complete |
| Cloud Run with authentication enabled | A judge who cannot reach it has not seen it. §2.2 requires public reachability |

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[06-Hackathon-Compliance-Checklist]] · [[08-Deployment]] · [[ADR-006-Real-Source-P0-with-Captured-Fallback]] · [[ADR-004-Single-Orchestrated-Pipeline]] · [[03-Scope-Ladder]] · [[00-ADR-Index]]
