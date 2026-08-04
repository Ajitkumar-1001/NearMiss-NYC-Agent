---
title: Scope Ladder
tags:
  - execution
status: active
---

# Scope Ladder

Decided in advance: what gets cut, in what order, when time runs short.

> [!info] Source
> [[PRD]] §10 (P0/P1/P2) and §25 (priority order and scope-freeze rule).

## Rungs — cut from the bottom up

| Rung | Capability | Cut cost | Cut by |
|---|---|---|---|
| 1 (never cut) | Fixture demo path end-to-end — P0 | Demo dies; nothing else scores | — |
| 2 (never cut) | Deployed P0 dashboard and `GET /health` | No public URL; submission incomplete | — |
| 3 | Runtime detection, tracking, and risk scoring — P1 | Demo becomes replay-only; loses the "not a static mock" proof | hour-3 checkpoint |
| 4 | Runtime NYC context and Gemini explanation — P1 | Falls back to cached context and template explanation, disclosed in the UI | hour-3 checkpoint |
| 5 | Visual polish | Cosmetic | final hour |
| 6 (cut first) | Live or sampled camera feed — P2 | None — P2 is optional by design | any time |

Rungs 3–6 map to [[PRD]] §25's priority order read backwards. P2 failing must not
affect P0 or P1.

## Scope-freeze rule

At the end of the third implementation hour ([[PRD]] §25):

- If P0 works, **freeze P0**.
- If P1 works, preserve a known-good deployed revision.
- If P0 does **not** work, stop all live-feed and advanced-feature work.
- During the final hour, add no new core features.

## Rule

Cutting is a decision, not a failure — log it in [[05-Decision-Log]] so the
reason survives. What must never be cut is rung 1: without a working demo path
nothing else scores.

---
Related: [[PRD]] · [[04-MVP-Scope]] · [[02-Time-Box-Plan]] · [[05-Decision-Log]] · [[05-Non-Goals]]
