---
title: ADR-007 FastAPI Backend
tags:
  - adr
status: active
---

# ADR-007 — FastAPI Backend

## Status

Accepted — [[PRD]] §29, approved for v2.0.

## Context

The pipeline is Python-shaped whether or not the API is: OpenCV for frame
sampling, the Roboflow inference client for detection, and a
Supervision/ByteTrack-class tracker all live in Python. Rewriting any of them
elsewhere is not on the table inside the time box.

NFR-007 requires Pydantic models at Python boundaries, and [[05-API-Contracts]]
needs validation at the edge with shapes shared against [[06-Data-Model]].
[[ADR-009-Cloud-Run-Deployment]] requires a containerised HTTP service that
starts fast and answers `GET /health`.

In [[PRD]] v2.0, Google Cloud Run deployment is a hard eligibility gate rather
than just a locked architecture preference: public reachability, a passing
`GET /health`, `0.0.0.0:$PORT` binding, and revision/mode identification are
explicit P0 acceptance criteria ([[PRD]] §11.1; NFR-001/NFR-002 at §15), and
"Cloud Run first" is now product principle #1 ([[PRD]] §10). [[PRD]] §16.1
accordingly names FastAPI-on-Cloud-Run literally "the mandatory agent
service," not merely a locked technology preference.

## Decision

The backend is **FastAPI on Python 3.11+, with Pydantic models at every
boundary**, packaged as a single containerised service.

## Consequences

**Positive**
- Same language as the CV and tracking stack — no cross-process bridge.
- Pydantic satisfies NFR-007 directly, and its schema output can generate the
  TypeScript contract the frontend needs.
- Async request handling covers the synchronous 60 s analyse path without a
  queue, per [[ADR-004-Single-Orchestrated-Pipeline]].
- Trivial `GET /health` and a small container image — now doubling as direct
  proof for the P0 Cloud Run hard-gate criteria ([[PRD]] §11.1, §15
  NFR-001/NFR-002).

**Negative**
- Python's CPU-bound work blocks; a slow inference call occupies a worker.
- OpenCV and inference dependencies make the image heavier than a bare API
  container, which slows cold starts on Cloud Run.

**Accepted trade-off**
- Cold-start weight is accepted in exchange for keeping the pipeline and the API
  in one process and one language. Deploying the health skeleton early
  ([[06-Risk-Register]] row 9) surfaces image-size problems while there is still
  time to fix them.

## Alternatives considered

| Alternative | Why not |
|---|---|
| Node/TypeScript API calling a Python worker | Two processes and a bridge, contradicting [[ADR-004-Single-Orchestrated-Pipeline]] |
| Flask or Django | No first-class Pydantic validation or automatic schema output; NFR-007 becomes manual work |
| Serverless functions per endpoint | Cold starts with a heavy CV image, and no single orchestrator to own the fallback ladder |

---
Related: [[PRD]] · [[05-API-Contracts]] · [[06-Data-Model]] · [[04-Component-Design]] · [[ADR-004-Single-Orchestrated-Pipeline]] · [[ADR-009-Cloud-Run-Deployment]] · [[00-ADR-Index]]
