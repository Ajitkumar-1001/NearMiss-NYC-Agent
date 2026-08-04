---
title: Risk Register
tags:
  - execution
status: active
---

# Risk Register

> [!info] Source
> [[PRD]] §26. Impact and mitigation are the PRD's; **Likelihood is deliberately
> blank** — §26 does not estimate it, and a guessed likelihood would drive real
> cut decisions. Fill it from observation, not intuition.

| # | Risk | Likelihood | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| 1 | Venue network unusable | | High | Offline demo path; P0 works after the app has loaded ([[PRD]] §7 G4) | Ajit | open |
| 2 | Live feed unavailable | | High | Uploaded and bundled clips | Ajit | open |
| 3 | No near-miss occurs live | | High | Reproducible demonstration clip | Ajit | open |
| 4 | Detection misses cyclist or pedestrian | | High | Validate the clip early; fixture detections | Ajit | open |
| 5 | Tracking identity switches | | Medium | Short clip; smoothing; precomputed tracks | Ajit | open |
| 6 | Perspective invalidates metric claims | | High | Image-space visual conflict-risk proxy ([[ADR-002-Visual-Conflict-Proxy]]) | Ajit | open |
| 7 | Gemini fails or hallucinates | | High | Schema constraints and template fallback | Ajit | open |
| 8 | NYC Open Data API fails | | Medium | Cached normalized context | Ajit | open |
| 9 | Deployment failure | | High | Deploy the health skeleton early; preserve a known-good revision ([[ADR-009-Cloud-Run-Deployment]]) | Ajit | open |
| 10 | UI consumes excessive time | | Medium | Single dashboard; no auth; fixture-first development | Ajit | open |
| 11 | Judges interpret output as crash prediction | | High | Explicit terminology and visible limitations ([[ADR-002-Visual-Conflict-Proxy]]) | Ajit | open |

Risks 2–11 are [[PRD]] §26 verbatim. Risk 1 is the venue-internet case named in
[[PRD]] §7 G4 and is the reason [[ADR-001-Deterministic-Demo-First]] exists.

## Review

Re-read at each checkpoint in [[02-Time-Box-Plan]]. A risk that materialises
becomes an entry in [[07-Blocker-Log]]. Add any further risks surfaced by
[[05-Analyze-Prompt]].

---
Related: [[PRD]] · [[05-Analyze-Prompt]] · [[07-Blocker-Log]] · [[05-Demo-Reliability]] · [[02-Time-Box-Plan]]
