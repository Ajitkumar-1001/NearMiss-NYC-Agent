---
title: Scope Ladder
tags:
  - execution
status: active
---

# Scope Ladder

Decided in advance: what gets cut, in what order, when time runs short.

> [!info] Source
> [[PRD]] §11 (P0/P1/P2 scope ladder) and §27 (execution plan; 8:00 PM
> scope-freeze at §27.2). PRD v1's abstract priority-order list (old §25) is
> not restated in v2 — it is replaced by a concrete event-day timeline, so
> rung cut timing below is re-anchored to that timeline, not a numbered list.

## Rungs — cut from the bottom up

| Rung | Capability | Cut cost | Cut by |
|---|---|---|---|
| 1 (never cut) | Captured-evidence replay path end-to-end — P0 | Demo dies; nothing else scores | — |
| 2 (never cut) | Cloud Run public deployment and `GET /health` — hard eligibility gate ([[PRD]] §2.2) | Submission is not hackathon-complete even if the app works locally | — |
| 3 (never cut) | Real-feed path: one configured NYC source retrieved and analyzed at least once — P0 | Real-feed proof is now required for P0, not optional ([[PRD]] §11.1 "Real-feed path") | — |
| 4 | Runtime detection, tracking, and risk scoring — P1 | Demo becomes replay-only; loses the "not a static mock" proof | ~7:00 PM, end of the evidence-replay window ([[PRD]] §27.2) |
| 5 | Runtime NYC context and Gemini explanation — P1 | Falls back to cached context and template explanation, disclosed in the UI | ~7:40 PM, end of the context/explanation window ([[PRD]] §27.2) |
| 6 | Visual polish | Cosmetic | 7:40–8:00 PM dashboard/README window ([[PRD]] §27.2) |
| 7 (cut first) | Periodic or continuous live-camera sampling, multiple-camera selection — P2 | None — P2 is optional by design | any time |

Rungs 4–7 map to [[PRD]] §11's P1/P2 boundaries, cut-first to never-cut.
Rungs 1–3 are the full P0 set: PRD v2 promoted the real-feed path from P2 to
P0, so it is now a never-cut rung alongside the captured-evidence path and
the Cloud Run gate, not the cut-first rung it was under v1. P2 failing must
not affect P0 or P1.

## Scope-freeze rule

At 8:00 PM ([[PRD]] §27.2 scope freeze):

- If P0 works, **freeze P0** — preserve the deployed revision, add no new
  core feature, run demo reliability checks, and record a fallback demo.
- If P1 works, preserve a known-good deployed revision.
- If P0 does **not** work, stop all P1 and P2 work and focus on rungs 1–3.

## Rule

Cutting is a decision, not a failure — log it in [[05-Decision-Log]] so the
reason survives. What must never be cut is rung 1: without a working demo path
nothing else scores.

---
Related: [[PRD]] · [[04-MVP-Scope]] · [[02-Time-Box-Plan]] · [[05-Decision-Log]] · [[05-Non-Goals]]
