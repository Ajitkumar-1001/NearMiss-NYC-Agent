---
title: ADR-006 Real Source P0 with Captured Fallback
tags:
  - adr
status: active
---

# ADR-006 — Real Source P0 with Captured Fallback

## Status

Accepted — [[00-Source-of-Truth-PRD|PRD]] §29, approved for version 2.1.

**Supersedes [[ADR-001-Deterministic-Demo-First]]** as the P0 sequencing
decision. ADR-001's fallback guarantee survives; its claim to be the *whole* of
P0 does not.

## Context

PRD v1.0 defined P0 as excluding all runtime external API dependencies, and made
"deterministic demo first" its top principle. Real-feed analysis sat at P2.

That ordering optimizes for the wrong failure. The judging rubric's first
dimension is **Working Demo** ([[00-Source-of-Truth-PRD|PRD]] §2.3), and the event is titled *Live
Feeds, Open Data*. A system that only ever replays a recording answers a
question the judges did not ask, however reliably it answers it.

The opposing force is real and unchanged: [[06-Risk-Register]] carries three
High-impact risks that a live-only demo cannot survive — the feed is
unavailable, no near-miss occurs inside the judging window, or deployment fails.
A live-only demo can be destroyed by someone else's rate limit thirty seconds
before judging.

Both paths are therefore mandatory, and they answer different questions:
*does it work on real data* and *can you show me the interesting case on demand*.

## Decision

**Real NYC source analysis is part of P0.** The deployed agent must analyze at
least one real NYC feed or organizer-provided live-feed source.

**Captured-feed replay remains mandatory** as the guaranteed conflict
demonstration and network-failure fallback, running from committed fixtures with
the network disabled ([[00-Source-of-Truth-PRD|PRD]] §11.1, captured evidence baseline).

**A live no-conflict or insufficient-evidence result is a valid P0 outcome**
(§29). The live path proves the system runs on real data; it is not required to
produce a conflict on demand. Truthfully reporting "not enough evidence" is a
feature of the risk semantics in §19, not a failed demo.

The demo order follows from this: golden flow §12.2 runs live analysis on a real
source first (steps 3–4), then the captured replay (steps 6–11). The judge sees
genuine runtime inference before the deterministic path.

## Consequences

**Positive**
- Answers the rubric's first dimension directly, on the event's own theme.
- The interesting case is still shown on demand, from fixtures that cannot be
  taken down.
- "Insufficient evidence" becomes a demonstrable behaviour rather than an
  embarrassment.

**Negative**
- P0 now depends on external services that can fail. ADR-001's clean offline
  guarantee no longer covers all of P0.
- Two paths to build, validate, and rehearse instead of one.
- FR-016 processing-mode disclosure ([[00-Source-of-Truth-PRD|PRD]] §14) becomes load-bearing: with
  both paths live, an unlabeled screen is a truthfulness failure.

**Accepted trade-off**
- More pre-event work, front-loaded into [[00-Source-of-Truth-PRD|PRD]] §11.1's readiness baseline so
  that Friday is integration rather than construction. This is what
  [[09-Preexisting-Code-Disclosure]] then has to disclose.

## Alternatives considered

| Alternative | Why not |
|---|---|
| Keep deterministic-only P0, real feed at P2 | Fails the Working Demo dimension on a live-feeds-themed event; the demo answers an unasked question |
| Live-only P0, drop the captured path | Three High-impact risks in [[06-Risk-Register]] land on the demo with no floor underneath |
| Live path, but require it to produce a conflict | Not controllable. Forcing it invites staging the result, which breaks the §19 claim boundary |
| Switch modes mid-demo to disguise the fallback | Directly violates FR-016 mode disclosure |

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[ADR-001-Deterministic-Demo-First]] · [[ADR-007-Cloud-Run-Eligibility-Gate]] · [[03-Scope-Ladder]] · [[07-Demo-Story]] · [[05-Demo-Reliability]] · [[06-Risk-Register]] · [[00-ADR-Index]]
