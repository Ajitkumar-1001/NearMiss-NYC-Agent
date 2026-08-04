---
title: Risk Register
tags:
  - execution
status: active
---

# Risk Register

> [!info] Source
> [[PRD]] §28. Impact and mitigation are the PRD's; **Likelihood is deliberately
> blank** — §28 does not estimate it, and a guessed likelihood would drive real
> cut decisions. Fill it from observation, not intuition.

| # | Risk | Likelihood | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| 1 | Not deployed on Cloud Run | | Disqualification | Deploy health skeleton first and preserve revision ([[PRD]] §29) | Ajit | open |
| 2 | Public access blocked by organization policy | | Disqualification | Use personal Gmail or `--no-invoker-iam-check` | Ajit | open |
| 3 | Container binds to localhost/wrong port | | High | Bind to `0.0.0.0:$PORT`; test locally and deployed | Ajit | open |
| 4 | Venue network unusable | | High | Offline demo path; P0 works after the app has loaded ([[PRD]] G6, §8) | Ajit | open |
| 5 | Live feed unavailable | | High | Uploaded and bundled clips | Ajit | open |
| 6 | Official feed requires signed agreement | | High | Do not depend on bulk feed; use approved accessible REST/still source ([[PRD]] §18) | Ajit | open |
| 7 | No near-miss occurs live | | High | Reproducible demonstration clip | Ajit | open |
| 8 | Duplicate camera stills create false motion | | High | Content hashing and temporal-evidence gate | Ajit | open |
| 9 | Detection misses cyclist or pedestrian | | High | Validate the clip early; fixture detections | Ajit | open |
| 10 | Tracking identity switches | | Medium | Short clip; smoothing; precomputed tracks | Ajit | open |
| 11 | Perspective invalidates metric claims | | High | Image-space visual conflict-risk proxy ([[PRD]] §29) | Ajit | open |
| 12 | Gemini fails or hallucinates | | High | Schema constraints and template fallback | Ajit | open |
| 13 | NYC Open Data API fails | | Medium | Cached normalized context | Ajit | open |
| 14 | UI consumes excessive time | | Medium | Single dashboard; no auth; fixture-first development | Ajit | open |
| 15 | Judges interpret output as crash prediction | | High | Explicit terminology and visible limitations ([[PRD]] §19.1) | Ajit | open |
| 16 | License conflict | | Medium | RF-DETR + MIT/Apache defaults; avoid AGPL default ([[PRD]] §17) | Ajit | open |

Rows 1–3, 6, 8, and 16 are new for v2.0 — [[PRD]] §26 (v1) had no equivalent for
the Cloud Run disqualification risks (rows 1–2) or wrong-port binding (row 3);
their Risk/Impact/Mitigation cells are [[PRD]] §28 verbatim. Rows 5, 7, 9–10,
12–13 restate the same risks that were in v1's §26, but §28 reworded most of
the PRD-side mitigation text since then (e.g. "fixture detections" is now
"stored detections fallback") — treat those cells as this note's paraphrase,
not a current quotation; reread §28 before citing them as a direct source. Row
4 is the venue-internet case named in [[PRD]] G6 (§8; this was G4 in v1) and is
the reason [[PRD]] §29 exists. Row 11 (perspective) still matches §29's
framing. Row 15 (judges reading the score as crash prediction) is no longer
its own row in §28 — v2 defines that safeguard in [[PRD]] §19.1 (Risk
semantics) instead.

## Review

Re-read at each checkpoint in [[02-Time-Box-Plan]]. A risk that materialises
becomes an entry in [[07-Blocker-Log]]. Add any further risks surfaced by
[[05-Analyze-Prompt]].

---
Related: [[PRD]] · [[05-Analyze-Prompt]] · [[07-Blocker-Log]] · [[05-Demo-Reliability]] · [[02-Time-Box-Plan]]
