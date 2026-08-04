---
title: ADR Index
tags:
  - adr
status: active
---

# ADR Index

Decisions that constrain the build. New ones start from [[ADR-Template]].

> [!info] Source
> These ten rows correspond to a subset of [[PRD]] §29's locked architectural
> decisions, approved for v2.0 (was §27, v1.0). §29 now lists 18 locked
> decisions in total — see the gap note below for the eight that don't have a
> row here yet.
> Changing any of them requires an ADR *and* a PRD version increment — see
> [[PRD]] §1 and §31.

| ID | Decision | Status | Note |
|---|---|---|---|
| 001 | Deterministic demo first | Accepted | [[ADR-001-Deterministic-Demo-First]] |
| 002 | Visual conflict-risk proxy, not collision probability | Accepted | [[ADR-002-Visual-Conflict-Proxy]] |
| 003 | Provider adapter architecture | Accepted | [[ADR-003-Provider-Adapter-Architecture]] |
| 004 | Single orchestrated pipeline, not a multi-agent council | Accepted | [[ADR-004-Single-Orchestrated-Pipeline]] |
| 005 | No authentication | Accepted | [[ADR-005-No-Authentication]] |
| 006 | No identity recognition | Accepted | [[ADR-006-No-Identity-Recognition]] |
| 007 | FastAPI backend | Accepted | [[ADR-007-FastAPI-Backend]] |
| 008 | Next.js dashboard (escape hatch stated) | Accepted | [[ADR-008-Nextjs-Dashboard]] |
| 009 | Google Cloud Run deployment target | Accepted | [[ADR-009-Cloud-Run-Deployment]] |
| 010 | JSON fixtures as operational fallbacks | Accepted | [[ADR-010-JSON-Fixture-Fallbacks]] |

> [!warning] Gap — v2.0 locked decisions with no ADR yet
> [[PRD]] §29 (v2.0) locks 18 architectural decisions, up from 10 in v1.0 §27.
> The following are new or newly-locked in v2.0 and have no corresponding row
> or ADR file in this folder yet. Per [[PRD]] §1 and this vault's CLAUDE.md
> rule 5, a decision that constrains the build gets an ADR — flagging here so
> the gap isn't silently dropped. Writing these ADRs is out of scope for this
> reconciliation pass.
>
> - Real NYC feed analysis is part of P0 (promoted from P2 in v1.0)
> - A live no-conflict result is a valid outcome
> - Roboflow RF-DETR/Workflow is the preferred perception provider; AGPL-licensed Ultralytics YOLO is excluded from the default implementation
> - `supervision` plus a lightweight tracker are the preferred post-processing tools
> - Roboflow MCP is a development-plane integration only, not runtime infrastructure
> - CPU-first Cloud Run strategy; GPU is optional
> - Approved accessible camera endpoints or organizer feeds only; no signed bulk-feed dependency
> - Public repo, README, source policy, privacy statement, and permissive license are P0

## When to write one

A decision earns an ADR when reversing it later would cost real work — anything
touching architecture, data shape, vendor choice, or demo strategy. Smaller calls
go in [[05-Decision-Log]].

[[PRD]] §1 additionally requires an ADR **and** a PRD version bump for changes to
the product problem or target user, the P0 definition of done, the core event
taxonomy, risk-scoring semantics, external provider boundaries, safety and
privacy requirements, the required demo flow, or the deployment architecture.

---
Related: [[PRD]] · [[ADR-Template]] · [[05-Decision-Log]] · [[01-Constitution]]
