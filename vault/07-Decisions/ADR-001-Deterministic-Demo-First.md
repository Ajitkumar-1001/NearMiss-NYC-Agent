---
title: ADR-001 Deterministic Demo First
tags:
  - adr
status: done
---

# ADR-001 — Deterministic Demo First

## Status

**Superseded** as the P0 sequencing decision by
[[ADR-006-Real-Source-P0-with-Captured-Fallback]], per
[[00-Source-of-Truth-PRD|PRD]] §29 "Required superseding ADRs". §31 makes this
marking a condition of v2.1 ratification.

Accepted for version 2.0. What survives: the captured-evidence replay is still
mandatory, still runs from committed fixtures with the network disabled, and is
still the guaranteed fallback ([[00-Source-of-Truth-PRD|PRD]] §29). What is
superseded: its claim that the deterministic path is the *whole* of P0. Real NYC
source analysis is now P0 alongside it. Read the Context section below with that
correction in mind — it already describes the shift.

## Context

Goal G6 ([[00-Source-of-Truth-PRD|PRD]] §8) requires the core demo to survive the unavailability of
live feeds, Roboflow, Gemini, NYC Open Data, **or venue internet**. Every one of
those is a realistic failure on hackathon day, and three of them appear in
[[06-Risk-Register]] at High impact: live feed unavailable, no near-miss
occurring during a live window, and deployment failure.

A demo that depends solely on live external services is a demo that can be
destroyed by someone else's rate limit thirty seconds before judging. This
remains true, but the balance has shifted: PRD v1.0 defined P0 as excluding
all runtime external API dependencies and made "deterministic demo first" its
top principle. PRD v2.0 reprioritizes — principle 1 is now Cloud Run first and
principle 2 is Real feed plus reproducible evidence ([[00-Source-of-Truth-PRD|PRD]] §10) — and
promotes real-feed analysis of a live NYC source from P2 to P0 ([[00-Source-of-Truth-PRD|PRD]] §11.1,
"Real-feed path"). The captured-evidence replay is still mandatory, but it is
now the guaranteed evidence demonstration and network-failure fallback
underneath a live-first P0, rather than the sole guaranteed product.

## Decision

The captured-evidence-replay path runs from committed fixtures and must work
with the network disabled. This fixture path is a guaranteed fallback, not the
whole of P0 — see Context for how PRD v2.0 also makes real-feed analysis
mandatory at P0.

Concretely: the captured-evidence path must work offline once the web
application has loaded, and it is the fallback destination named in FR-015
([[00-Source-of-Truth-PRD|PRD]] §14, "Provider fallbacks") and shown as the dotted fallback edges in
the architecture diagram ([[00-Source-of-Truth-PRD|PRD]] §16) — a failure at any higher level (live
source, Roboflow, tracker, NYC Open Data, Gemini) degrades onto it without
corrupting it. PRD v1's standalone §17 "Fallback ladder" section no longer
exists as such in v2.0; its content now lives in FR-015 and the diagram.

## Consequences

**Positive**
- The captured-evidence portion of P0 is judgeable regardless of network,
  provider, or credential state, even though real-feed analysis is now also
  mandatory at P0 ([[00-Source-of-Truth-PRD|PRD]] §11.1) and does depend on those things.
- P1 and P2 are free to fail, because failing costs nothing that was guaranteed.
- Fixtures are the fallback path, so building them is not throwaway work.
- Development can start before any credential arrives.

**Negative**
- Fixtures must stay shape-identical to live output or the demo silently
  diverges from real behaviour — see fixture parity in [[06-Data-Model]].
- A fixture-driven demo can read as a mock. In PRD v2.0 this is addressed
  structurally rather than by a mid-demo switch: the golden flow ([[00-Source-of-Truth-PRD|PRD]]
  §12.2) now runs live analysis on a real NYC source first (steps 3-4), before
  the captured-evidence replay (steps 6-11), so the judge sees genuine runtime
  inference before the deterministic path is shown. FR-016 mode disclosure
  ([[00-Source-of-Truth-PRD|PRD]] §14) still requires the active processing mode to be labeled, which
  keeps the replay honest rather than hidden.

**Accepted trade-off**
- Early hours go to producing fixtures instead of features. That is the
  premium paid for a captured-evidence demo that cannot be taken down by
  someone else's outage — even though PRD v2.0 also requires a real-feed demo
  path at P0 that can be.

## Alternatives considered

| Alternative | Why not |
|---|---|
| Live camera feed as the demo path | Two High-impact risks at once — the feed may be unavailable, and no near-miss may occur during the judging window |
| Runtime inference on an uploaded clip as P0 | Still depends on Roboflow being reachable and on completing inside 60 s over venue wifi |
| Pre-recorded video of the demo as the primary | Judges discount a recording. [[00-Source-of-Truth-PRD|PRD]] §11.1 requires a fallback recording as a backup submission artifact, not the primary demo, and §15 NFR-005 sets the reliability run-count gates (10/10 successful local captured-replay runs, 5/5 successful deployed captured-replay runs, 3 successful real-source fetches, 3 successful real-source perception runs where credentials permit, 1 verified independent public-access test) that justify treating a live run as the default |

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[07-Demo-Story]] · [[05-Demo-Reliability]] · [[07-Provider-Adapters]] · [[00-ADR-Index]]
