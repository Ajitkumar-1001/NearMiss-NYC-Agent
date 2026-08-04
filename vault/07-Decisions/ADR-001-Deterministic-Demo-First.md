---
title: ADR-001 Deterministic Demo First
tags:
  - adr
status: active
---

# ADR-001 — Deterministic Demo First

## Status

Accepted — [[PRD]] §27, approved for v1.0.

## Context

Goal G4 ([[PRD]] §7) requires the core demo to survive the unavailability of
live feeds, Roboflow, Gemini, NYC Open Data, **or venue internet**. Every one of
those is a realistic failure on hackathon day, and three of them appear in
[[06-Risk-Register]] at High impact: live feed unavailable, no near-miss
occurring during a live window, and deployment failure.

A demo that depends on any of them is a demo that can be destroyed by someone
else's rate limit thirty seconds before judging. [[PRD]] §10.1 therefore defines
P0 as excluding all runtime external API dependencies, and §9 principle 2 states
it outright: deterministic demo first.

## Decision

The demo runs from committed fixtures and must work with the network disabled. Live data is an enhancement layered on top, never a dependency.

Concretely: P0 must work offline once the web application has loaded, and the
fixture path is the floor of the fallback ladder in [[PRD]] §17 — a failure at
any higher level degrades onto it without corrupting it.

## Consequences

**Positive**
- P0 is judgeable regardless of network, provider, or credential state.
- P1 and P2 are free to fail, because failing costs nothing that was guaranteed.
- Fixtures are the fallback path, so building them is not throwaway work.
- Development can start before any credential arrives.

**Negative**
- Fixtures must stay shape-identical to live output or the demo silently
  diverges from real behaviour — see fixture parity in [[06-Data-Model]].
- A fixture-driven demo can read as a mock. Mitigated by the runtime-analysis
  switch in the golden flow ([[PRD]] §11.2 step 10) and by FR-012 mode
  disclosure, which makes the replay honest rather than hidden.

**Accepted trade-off**
- Early hours go to producing fixtures instead of features. That is the premium
  paid for a demo that cannot be taken down by someone else's outage.

## Alternatives considered

| Alternative | Why not |
|---|---|
| Live camera feed as the demo path | Two High-impact risks at once — the feed may be unavailable, and no near-miss may occur during the judging window |
| Runtime inference on an uploaded clip as P0 | Still depends on Roboflow being reachable and on completing inside 60 s over venue wifi |
| Pre-recorded video of the demo as the primary | Judges discount a recording. [[PRD]] §22.5 keeps one as backup, not as the submission |

---
Related: [[PRD]] · [[07-Demo-Story]] · [[05-Demo-Reliability]] · [[07-Provider-Adapters]] · [[ADR-010-JSON-Fixture-Fallbacks]] · [[00-ADR-Index]]
