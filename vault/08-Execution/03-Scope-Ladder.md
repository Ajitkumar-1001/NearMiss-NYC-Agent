---
title: Scope Ladder
tags:
  - execution
status: active
---

# Scope Ladder

Decided in advance: what gets cut, in what order, when time runs short.

> [!info] Source
> [[00-Source-of-Truth-PRD|PRD]] §11 (P0/P1/P2 scope ladder), §27.2 (event execution timeline;
> 7:00 PM hard code freeze, 8:00–8:15 PM protected contingency), and §27.3
> (event-day kill order). PRD v1's abstract priority-order list (old §25) is
> not restated in v2 — it is replaced by a concrete event-day timeline, so
> rung cut timing below is re-anchored to that timeline, not a numbered list.

## Rungs — cut from the bottom up

| Rung | Capability | Cut cost | Cut by |
|---|---|---|---|
| 1 (never cut) | Captured-evidence replay path end-to-end — P0 | Demo dies; nothing else scores | — |
| 2 (never cut) | Cloud Run public deployment and `GET /health` — hard eligibility gate ([[00-Source-of-Truth-PRD|PRD]] §2.2) | Submission is not hackathon-complete even if the app works locally | — |
| 3 (never cut) | Real-feed path: one configured NYC source retrieved and analyzed at least once — P0 | Real-feed proof is now required for P0, not optional ([[00-Source-of-Truth-PRD|PRD]] §11.1 "Real-source baseline"; §29 locks "Real NYC source analysis is part of P0") | — |
| 4 | Runtime detection, tracking, and risk scoring — P1 | Demo becomes replay-only; loses the "not a static mock" proof | 7:00 PM hard code freeze — the last point at which any runtime path may change ([[00-Source-of-Truth-PRD|PRD]] §27.2) |
| 5 | Runtime NYC context and Gemini explanation — P1 | Falls back to cached context and template explanation, disclosed in the UI | 6:35 PM, when demo-path verification ends and the documentation window opens ([[00-Source-of-Truth-PRD|PRD]] §27.2) |
| 6 | Visual polish | Cosmetic | First in the §27.3 kill order, so cut at the first sign of time pressure; hard-cut at the 7:00 PM freeze, and §27.2 forbids polish in the 8:00–8:15 PM contingency ([[00-Source-of-Truth-PRD|PRD]] §27.2, §27.3) |
| 7 (cut first) | Periodic or continuous live-camera sampling, multiple-camera selection — P2 | None — P2 is optional by design | any time |

Rungs 4–7 map to [[00-Source-of-Truth-PRD|PRD]] §11's P1/P2 boundaries, cut-first to never-cut.
Rungs 1–3 are the full P0 set: PRD v2 promoted the real-feed path from P2 to
P0, so it is now a never-cut rung alongside the captured-evidence path and
the Cloud Run gate, not the cut-first rung it was under v1. Failure to
complete P1 or P2 must not break P0 ([[00-Source-of-Truth-PRD|PRD]] §11.5).

## Scope-freeze rule

At 7:00 PM, the hard code freeze ([[00-Source-of-Truth-PRD|PRD]] §27.2; locked in §29 as
"7:00 PM is the hard feature freeze"):

- If P0 works, **freeze P0** — tag and preserve the deployed revision, add no
  new core feature, then spend 7:00–7:30 PM on the reliability and fallback
  proof and the backup recording that §27.2 puts in that window.
- If P1 works, preserve a known-good deployed revision and its rollback command.
- If P0 does **not** work, stop all P1 and P2 work and focus on rungs 1–3 —
  and this bites *before* 7:00 PM, while code changes are still permitted.

> [!warning] This rule changed meaning when it was re-anchored
> It previously read "at 8:00 PM ([[00-Source-of-Truth-PRD|PRD]] §27.2 scope freeze)". §27.2
> defines no scope freeze: 7:00 PM is the hard code freeze, 7:00–7:30 PM is
> reliability and fallback proof, 7:30–8:00 PM is submission assembly, and
> 8:00–8:15 PM is protected contingency limited to rollback, a broken public
> URL, submission metadata, and re-recording a failed backup clip. Re-anchoring
> to 7:00 PM narrows the rule: it removes an implied hour of post-freeze scope
> work the PRD does not allow, and it moves the "stop P1 and P2" trigger to
> before the freeze rather than at it. Record this correction in
> [[05-Decision-Log]].

## Rule

Cutting is a decision, not a failure — log it in [[05-Decision-Log]] so the
reason survives. What must never be cut is rung 1: without a working demo path
nothing else scores.

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[04-MVP-Scope]] · [[02-Time-Box-Plan]] · [[05-Decision-Log]] · [[05-Non-Goals]]
