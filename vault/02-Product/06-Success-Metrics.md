---
title: Success Metrics
tags:
  - product
status: active
---

# Success Metrics

> [!info] Source
> [[PRD]] §23, plus NFR-001 and NFR-003 (§14) and the demo gates in §22.5.
> Targets are set here in advance; nothing is measured yet.

## Product metrics

| Metric | Definition | Target | Actual | Measured by |
|---|---|---|---|---|
| End-to-end report | A full footage → evidence-backed report path completes for one event | 1 reproducible event | — | [[05-Demo-Reliability]] |
| Five-second comprehension | A judge understands the flagged conflict without narration | pass | — | [[04-Demo-Script]] rehearsal |
| Score decomposition | Risk score visibly broken into named factors | all 4 factors shown | — | [[05-QA-Checklist]] |
| Mode disclosure | Active processing mode labelled on screen, never disguised | 1 mode, always visible | — | [[05-QA-Checklist]] |
| Public-data correlation | One meaningful historical-context correlation displayed and sourced | 1 | — | [[05-QA-Checklist]] |
| P0 replay latency | Time from user action to replay starting (NFR-003) | < 2 s | — | [[05-Demo-Reliability]] |
| P1 processing time | Runtime analysis of the demo clip (NFR-003) | < 60 s | — | [[05-Demo-Reliability]] |

## Engineering metrics

| Metric | Target | Actual |
|---|---|---|
| P0 deployment success rate during pre-demo checks | 100% | — |
| Unhandled exceptions on the golden path | 0 | — |
| External providers without a fallback | 0 | — |
| Dead or misleading UI controls | 0 | — |
| Secrets committed | 0 | — |

## Model / pipeline metrics

Defined and measured in [[04-Vision-Evaluation]] and [[03-Agent-Evaluation]].
These are pass/fail gates, not scores — [[PRD]] §22 does not define numeric
accuracy targets, and none should be invented.

| Metric | Target | Actual |
|---|---|---|
| Required classes detected in key frames | pass | — |
| Track identity stable through the conflict window | pass | — |
| Trajectory trails visually aligned with objects | pass | — |
| Explanation cites only supplied evidence | pass | — |
| Explanation states ≥ 1 limitation and recommends human review | pass | — |
| Explanation returns valid schema-constrained output | pass | — |

## Demo metrics

Reliability targets live in [[05-Demo-Reliability]]. The submission gates from
[[PRD]] §22.5 and NFR-001:

| Gate | Target | Actual |
|---|---|---|
| Consecutive successful local P0 runs | 10/10 | — |
| Consecutive successful deployed P0 runs | 5/5 | — |
| Successful runtime P1 runs where credentials permit | 3/3 | — |
| Recorded backup demo saved locally | yes | — |
| Screenshots saved locally | yes | — |

> [!caution] Don't quote a number we haven't measured
> Any figure that reaches [[02-2-Minute-Pitch]] must trace to a row here with a
> real value in the Actual column.

---
Related: [[PRD]] · [[02-Problem-Statement]] · [[04-Vision-Evaluation]] · [[03-Agent-Evaluation]] · [[05-Demo-Reliability]]
