---
title: MVP Scope
tags:
  - product
status: active
---

# MVP Scope

What ships. Anything not listed here is out — see [[05-Non-Goals]].

> [!info] Source
> [[PRD]] §11.1 (P0) and §14 (functional requirements). P1 and P2 are
> enhancements and do not change the P0 definition of done — see
> [[03-Scope-Ladder]].

## In scope

P0 is the guaranteed submission, now built from four mandatory parts
([[PRD]] §11.1): Cloud Run and public access, the real-feed path, the
captured-evidence path, and submission artifacts. Real-feed analysis of a live
NYC source is P0, not an enhancement — but the captured-evidence path must
still work fully offline once the web application has loaded and excludes
runtime external API dependencies. It is the guaranteed evidence
demonstration and network-failure fallback, not the sole guaranteed product
([[PRD]] §3, §10 principle 2).

### Cloud Run and public access

| # | Capability | Why it's essential | Owner | Status |
|---|---|---|---|---|
| 1 | Public FastAPI agent deployed on Google Cloud Run, listening on `0.0.0.0:$PORT` | Hard eligibility gate — the submission is not hackathon-complete without it ([[PRD]] §2.2, NFR-001) | Ajit | todo |
| 2 | Health endpoint — `GET /health` returns HTTP 200 (FR-019) | Proves the deployment is alive before the demo starts | Ajit | todo |
| 3 | Public access verified from a logged-out browser or independent device; known-good deployed revision preserved and identifiable | Judges need a working public URL with no auth barrier ([[PRD]] §2.2, NFR-002) | Ajit | todo |

### Real-feed path

| # | Capability | Why it's essential | Owner | Status |
|---|---|---|---|---|
| 4 | One configured NYC source from the approved source policy, retrieved through a source adapter (FR-001, FR-002; [[PRD]] §18) | Real-feed analysis is now P0, not an enhancement | Ajit | todo |
| 5 | Source name, jurisdiction, source URL identifier, retrieval timestamp, and freshness displayed (FR-003) | Judges must see what's live vs. cached vs. fixture | Ajit | todo |
| 6 | Roboflow perception executed on at least one real source image (FR-005) | Proves the vision path runs against a real frame, not only fixtures | Ajit | todo |
| 7 | Annotated result returned through the Cloud Run service (FR-012) | The five-second comprehension test in [[PRD]] §12.3 applies to the live path too | Ajit | todo |
| 8 | Valid `no_candidate_conflict` / `insufficient_temporal_evidence` outcome supported (FR-008, FR-017) | A live no-conflict or insufficient-evidence result is a valid, locked outcome — never a fabricated alert ([[PRD]] §29) | Ajit | todo |

### Captured evidence path

| # | Capability | Why it's essential | Owner | Status |
|---|---|---|---|---|
| 9 | One bundled 10–20 second traffic clip | Nothing downstream runs without a known-good input | Ajit | todo |
| 10 | One precomputed potential-conflict event | The single event the whole demo is built around | Ajit | todo |
| 11 | Precomputed detections and tracks | Removes the vision provider from the demo path | Ajit | todo |
| 12 | Annotated replay — boxes, trails, conflict marker (FR-012) | The five-second comprehension test in [[PRD]] §12.3 | Ajit | todo |
| 13 | Visual conflict-risk proxy with factor breakdown (FR-010) | Explainability; an opaque score fails the evidence-before-narration principle in [[PRD]] §10 (principle 3) | Ajit | todo |
| 14 | Cached NYC collision context (FR-013) | The public-data correlation judges look for | Ajit | todo |
| 15 | Deterministic structured safety report (FR-014) | The deliverable the analyst actually reads | Ajit | todo |
| 16 | Processing-mode disclosure — `Captured feed replay` or `Demonstration fixture`, as applicable (FR-016) | Fallback must never be disguised as live inference | Ajit | todo |

### Submission artifacts

| # | Capability | Why it's essential | Owner | Status |
|---|---|---|---|---|
| 17 | Public repository with a permissive license | Open Source is a judging dimension ([[PRD]] §2.3) | Ajit | todo |
| 18 | README — problem, architecture, data sources, setup, Cloud Run deployment, demo flow, limitations, privacy | Submission requirement and the responsible-AI record | Ajit | todo |
| 19 | Architecture diagram and two-minute demo script | Submission requirement | Ajit | todo |
| 20 | Fallback recording and screenshots stored locally | Network-failure fallback for the demo itself | Ajit | todo |

Alert threshold is 70/100 and configurable (FR-011). Supported event types are
listed in [[PRD]] §13; the first implementation prioritises one of them based on
the selected clip.

## Acceptance

A capability is done when it meets [[08-Definition-of-Done]] and has a case in
[[02-Test-Cases]].

## Cut order

If we run out of time, cut in the order given by [[03-Scope-Ladder]] — decided in
advance, on purpose, so the decision isn't made at 3am.

---
Related: [[PRD]] · [[05-Non-Goals]] · [[03-Scope-Ladder]] · [[08-Definition-of-Done]] · [[07-Demo-Story]]
