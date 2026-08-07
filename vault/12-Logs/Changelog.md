---
title: Changelog
tags:
  - log
status: draft
---

# Changelog

User-visible changes. Internal churn belongs in [[Progress-Log]].

## Unreleased

### Added
- [[00-Source-of-Truth-PRD|PRD]] **v2.1.0-FINAL** installed, superseding v2.0.0 — the pre-event frozen
  revision (`pre_event_document_freeze: 2026-08-04`; no v2.2 planned). Change
  summary at [[00-Source-of-Truth-PRD|PRD]] §1.2 and §1.3: Veris gets a conditional, non-runtime
  integration (FR-021); the event-day plan is rebuilt around a pre-event
  readiness gate, a 7:00 PM code freeze, and 75+ minutes of reserve; P0 is split
  into pre-arrival artifacts vs the event-day integration delta; the mandatory UI
  surface drops from sixteen components to six judge-facing surfaces; runtime NYC
  enrichment and Gemini generation move to P1; and the conflict-scoring engine is
  extracted into a public `vision-conflict-analytics` package consumed as a
  pinned release (FR-022). Section numbering is unchanged from v2.0.0, so
  existing §29 and FR-0NN citations across the vault remain valid.
- [[00-Source-of-Truth-PRD|PRD]] **v2.0.0** installed, superseding v1.0.0. Adds the NYC Vision Hack v.2
  compliance contract (§2), promotes Cloud Run to the hard eligibility gate and
  real-feed analysis into P0, and carries the event schedule and judging rubric.
- [[00-Source-of-Truth-PRD|PRD]] v1.0.0 landed as the vault's canonical source of truth.
- `ADR-006-No-Identity-Recognition`, `ADR-007-FastAPI-Backend`,
  `ADR-008-Nextjs-Dashboard`, `ADR-009-Cloud-Run-Deployment`, and
  `ADR-010-JSON-Fixture-Fallbacks` — the five [[00-Source-of-Truth-PRD|PRD]] §27 locked decisions that
  had no ADR.
- [[00-Source-of-Truth-PRD|PRD]] **v2.0.0** import, full change summary at [[00-Source-of-Truth-PRD|PRD]] §1.1: Google Cloud
  Run is now the hard eligibility gate (not a deployment preference),
  real-feed analysis is promoted to P0, Roboflow RF-DETR/Workflow is the
  preferred perception provider (AGPL-licensed YOLO excluded), and the
  approved live-data policy uses organizer or accessible camera feeds only,
  with no signed bulk-feed dependency. Of the 18 locked decisions now in
  [[00-Source-of-Truth-PRD|PRD]] §29 (up from v1's 10), four are new and have no ADR yet:
  real-feed-in-P0, the RF-DETR preference, the data-source policy, and
  CPU-first Cloud Run — flagged here as an open gap per `00-ADR-Index` /
  CLAUDE.md rule 5, both since retired (see Removed).

### Changed
- Product notes, [[03-Scope-Ladder]], [[06-Risk-Register]],
  [[08-Definition-of-Done]], [[05-API-Contracts]], and [[06-Data-Model]] filled
  from the PRD; each cites the section it came from.
- `00-ADR-Index`: all ten ADRs moved from Draft to Accepted.

### Removed
- **`07-Decisions/` and all ten ADRs, revoked.** [[00-Source-of-Truth-PRD|PRD]] v2.0.0 §29 now holds
  every locked architectural decision (18, up from v1's 10), so the folder was
  redundant — and two entries actively contradicted v2: `ADR-001` asserted an
  offline-only P0 that v2 §1.1 change 2 reversed, and `ADR-009` framed Cloud Run
  as a deployment preference rather than v2 §2.2's hard eligibility gate.
  Inbound wikilinks across the vault were repointed to [[00-Source-of-Truth-PRD|PRD]] §29.
  [[ADR-Template]] survives in `11-Templates/`.

### Fixed
-

> [!note] Not yet user-visible
> Nothing here has shipped to a user. These entries track the knowledge base;
> product entries start when the dashboard exists.

---
Related: [[Progress-Log]] · [[Hackathon-Day-Log]] · [[08-Definition-of-Done]]
