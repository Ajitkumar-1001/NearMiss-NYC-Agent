---
title: ADR Index
tags:
  - adr
status: active
---

# ADR Index

Architectural decisions that constrain the build. Each is also carried as a
locked entry in [[00-Source-of-Truth-PRD|PRD]] §29 — **the PRD wins on conflict** ([[00-Source-of-Truth-PRD|PRD]] §1).
An ADR explains *why*; §29 states *what*.

Changing an accepted ADR follows the §31 change-control protocol and needs a PRD
version increment. Smaller calls that don't constrain the build go to
[[05-Decision-Log]].

## Active

| ADR | Decision | Approved for |
|---|---|---|
| [[ADR-001-Deterministic-Demo-First]] | Captured-evidence replay runs from committed fixtures with the network disabled | v2.0 — partly superseded by ADR-006 |
| [[ADR-002-Visual-Conflict-Proxy]] | An image-space conflict-risk proxy, decomposed into named factors — never a crash probability | v1.0 |
| [[ADR-003-Provider-Adapter-Architecture]] | Every external provider sits behind an adapter with a fallback | v1.0 |
| [[ADR-004-Single-Orchestrated-Pipeline]] | One orchestrated pipeline in one deployable unit, not a multi-agent council | v2.0 |
| [[ADR-005-No-Authentication]] | No auth, accounts, or roles — there is nothing to protect and a login blocks judges | v2.0 |
| [[ADR-006-Real-Source-P0-with-Captured-Fallback]] | Real NYC source analysis is P0; captured replay is the guaranteed fallback | v2.1 |
| [[ADR-007-Cloud-Run-Eligibility-Gate]] | A public Cloud Run agent is a pass/fail gate, not a deployment preference | v2.1 |

## Superseded

| ADR | Superseded by | Note |
|---|---|---|
| [[ADR-001-Deterministic-Demo-First]] | [[ADR-006-Real-Source-P0-with-Captured-Fallback]] | Only as the **P0 sequencing** decision. Its fallback guarantee still stands and the note is still live |

## Retired into PRD §29

Three v1 ADRs stated decisions that [[00-Source-of-Truth-PRD|PRD]] §29 now carries directly. They
were retired rather than renumbered, and their numbers reassigned:

| Retired ADR | Now stated as | Number now held by |
|---|---|---|
| ADR-006 No Identity Recognition | §29 — "No identity recognition." | [[ADR-006-Real-Source-P0-with-Captured-Fallback]] |
| ADR-007 FastAPI Backend | §29 — "FastAPI backend." | [[ADR-007-Cloud-Run-Eligibility-Gate]] |
| ADR-008 Nextjs Dashboard | §29 — "Next.js dashboard is preferred but not allowed to endanger the Cloud Run agent." | *unassigned* |

> [!warning] Numbering
> ADR-006 and ADR-007 refer to **different decisions** before and after v2.1.
> A pre-v2.1 document citing "ADR-006" means No Identity Recognition. Text in
> git history at commit `3fdf0cc` and earlier uses the old numbering.
> Do not reuse ADR-008, ADR-009, or ADR-010 for new decisions.

Two further v1 ADRs — ADR-009 Cloud Run Deployment and ADR-010 JSON Fixture
Fallbacks — were revoked outright. Cloud Run deployment is now
[[ADR-007-Cloud-Run-Eligibility-Gate]]; JSON fixtures as operational fallbacks
is a §29 entry.

## Writing a new one

Next free number is **ADR-011**. Copy [[ADR-Template]], and add the matching
§29 entry through the [[00-Source-of-Truth-PRD|PRD]] §31 protocol in the same change.

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[ADR-Template]] · [[05-Decision-Log]] · [[02-High-Level-Design]]
