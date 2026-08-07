---
title: API Contracts
tags:
  - architecture
status: active
---

# API Contracts

Contracts between frontend, backend, and pipeline. Use [[API-Contract]] for each
endpoint.

> [!info] Source
> [[00-Source-of-Truth-PRD|PRD]] §21, plus FR-018 and FR-019 (§14) and NFR-007/NFR-008 (§15).

## Endpoints

| Method | Path | Purpose | Contract |
|---|---|---|---|
| GET | `/health` | Status, version, active environment, optional provider readiness. Must return HTTP 200 (FR-019) | [[API-Contract]] |
| GET | `/api/v1/sources` | Public source metadata, without credentials or secret-bearing URLs | [[API-Contract]] |
| POST | `/api/v1/live/{source_id}/analyze` | Fetches the latest approved source image, records provenance, runs perception, applies the temporal-evidence gate, and returns a normalized analysis | [[API-Contract]] |
| GET | `/api/v1/demo` | The deterministic demonstration event and its media references | [[API-Contract]] |
| POST | `/api/v1/analyze` | P1 endpoint. Accepts a short video upload or trusted input reference; returns a processing job or the final analysis record | [[API-Contract]] |
| GET | `/api/v1/events/{analysis_id}` | The normalized analysis record | [[API-Contract]] |
| GET | `/api/v1/artifacts/{analysis_id}` | Returns or redirects to approved annotated artifacts; raw source media is not exposed by default | [[API-Contract]] |

Synchronous processing on `POST /api/v1/analyze` is acceptable for the hackathon
if it completes inside the NFR-006 target of 60 seconds. **A job queue is not
required** — [[00-Source-of-Truth-PRD|PRD]] §21 says so explicitly, and now scopes the exclusion wider:
a persistent database, user accounts, and authentication are also not required
for P0. PRD v2.0 no longer carries a "prohibited time sinks" list (the v1 §25
material is now a time-boxed event-day schedule at §27.2); this claim is
anchored to §21 directly instead.

Every endpoint returns the analysis record as JSON (FR-018). A downloadable
JSON control in the UI is optional but preferred once the core is complete.

## Conventions

- **Error shape** — one envelope for every failure. Provider failures produce
  structured logs and a user-readable fallback notice; **never a stack trace and
  never a secret** (NFR-008). A degraded response is a success with a changed
  `processing_mode`, not an error.
- **Versioning** — decided: `/api/v1` path prefix on everything except
  `/health`, which stays unversioned so uptime checks never break on a bump.
- **Validation at the boundary** — Pydantic models on the Python side, TypeScript
  strict mode on the frontend, both generated from or checked against the shapes
  in [[06-Data-Model]] (NFR-007).
- **Upload constraints** — type and size limited on `POST /api/v1/analyze`;
  temporary files deleted after processing where practical (NFR-010).

> [!note] Contract before code
> Agreeing the shape first is what lets frontend and backend proceed in
> parallel — the main reason this note exists.

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[API-Contract]] · [[06-Data-Model]] · [[04-Component-Design]] · [[02-Test-Cases]]
