---
title: ADR-009 Cloud Run Deployment
tags:
  - adr
status: active
---

# ADR-009 — Cloud Run Deployment

## Status

Accepted — [[PRD]] §27, approved for v1.0.

## Context

[[PRD]] §24 requires a deployed dashboard reachable without authentication and a
`GET /health` returning 200 — a working public URL is a submission requirement,
not a nice-to-have. G5 (§7) additionally wants the service deployable to Google
Cloud Run as a meaningful sponsor integration.

Deployment failure is a High-impact risk ([[06-Risk-Register]] row 9), and its
mitigation is specific: deploy the health skeleton early and preserve a
known-good revision. That mitigation only works on a platform with immutable
revisions and instant rollback.

[[ADR-004-Single-Orchestrated-Pipeline]] and [[ADR-007-FastAPI-Backend]] already
produce exactly what Cloud Run wants — one container, one HTTP port.

## Decision

The backend deploys as a **containerised service on Google Cloud Run**,
unauthenticated, with revisions retained so a known-good one can be restored
instantly.

Frontend hosting is deliberately left open — [[PRD]] §15.1 permits serving it
separately or bundling it depending on time. That call belongs in
[[08-Deployment]] and [[05-Decision-Log]], not here.

## Consequences

**Positive**
- Immutable revisions with one-command rollback, which is the actual mitigation
  for the deployment risk.
- Scale-to-zero costs nothing between demo runs.
- Container is the same artifact locally and deployed, so "works on my machine"
  fails earlier.
- Counts as a meaningful sponsor integration under G5.

**Negative**
- Cold starts, made worse by the CV dependencies noted in
  [[ADR-007-FastAPI-Backend]] — the first request after idle may miss the
  NFR-003 targets.
- Request-timeout ceilings must be checked against the 60 s P1 budget.
- Ties the deployment story to one cloud vendor.

**Accepted trade-off**
- Cold-start latency is accepted because the demo can be warmed with a `/health`
  call immediately before presenting — a step that belongs in
  [[01-Hackathon-Runbook]].

## Alternatives considered

| Alternative | Why not |
|---|---|
| Local laptop + tunnel | Depends on venue network — the exact failure [[ADR-001-Deterministic-Demo-First]] exists to avoid |
| A long-running VM | No instant rollback, and it costs money while idle |
| Vercel or similar for both tiers | Poor fit for a heavy Python CV container, and forfeits the G5 sponsor integration |
| Kubernetes | Prohibited-time-sink territory (§25) for a single container |

---
Related: [[PRD]] · [[08-Deployment]] · [[09-Observability]] · [[01-Hackathon-Runbook]] · [[ADR-004-Single-Orchestrated-Pipeline]] · [[ADR-007-FastAPI-Backend]] · [[00-ADR-Index]]
