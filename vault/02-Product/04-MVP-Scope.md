---
title: MVP Scope
tags:
  - product
status: active
---

# MVP Scope

What ships. Anything not listed here is out — see [[05-Non-Goals]].

> [!info] Source
> [[PRD]] §10.1 (P0) and §13 (functional requirements). P1 and P2 are
> enhancements and do not change the P0 definition of done — see
> [[03-Scope-Ladder]].

## In scope

P0 is the guaranteed submission. It must work offline once the web application
has loaded, and excludes all runtime external API dependencies.

| # | Capability | Why it's essential | Owner | Status |
|---|---|---|---|---|
| 1 | One bundled 10–20 second traffic clip | Nothing downstream runs without a known-good input | Ajit | todo |
| 2 | One precomputed potential-conflict event | The single event the whole demo is built around | Ajit | todo |
| 3 | Precomputed detections and tracks | Removes the vision provider from the demo path | Ajit | todo |
| 4 | Annotated replay — boxes, trails, conflict marker (FR-013) | The five-second comprehension test in [[PRD]] §11.3 | Ajit | todo |
| 5 | Visual conflict-risk proxy with factor breakdown (FR-006) | Explainability; an opaque score fails [[PRD]] §9 principle 1 | Ajit | todo |
| 6 | Cached NYC collision context (FR-009) | The public-data correlation judges look for | Ajit | todo |
| 7 | Deterministic structured safety report (FR-010) | The deliverable the analyst actually reads | Ajit | todo |
| 8 | Processing-mode disclosure — `Demonstration replay` (FR-012) | Fallback must never be disguised as live inference | Ajit | todo |
| 9 | One deployed dashboard | Judges need a working public URL | Ajit | todo |
| 10 | Health endpoint — `GET /health` (FR-015) | Proves the deployment is alive before the demo starts | Ajit | todo |
| 11 | README, architecture diagram, demo script, limitations | Submission requirement and the responsible-AI record | Ajit | todo |

Alert threshold is 70/100 and configurable (FR-007). Supported event types are
listed in [[PRD]] §12; the first implementation prioritises one of them based on
the selected clip.

## Acceptance

A capability is done when it meets [[08-Definition-of-Done]] and has a case in
[[02-Test-Cases]].

## Cut order

If we run out of time, cut in the order given by [[03-Scope-Ladder]] — decided in
advance, on purpose, so the decision isn't made at 3am.

---
Related: [[PRD]] · [[05-Non-Goals]] · [[03-Scope-Ladder]] · [[08-Definition-of-Done]] · [[07-Demo-Story]]
