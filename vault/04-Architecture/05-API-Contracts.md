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
> [[PRD]] §19, plus FR-014 and FR-015 (§13) and NFR-004/NFR-005 (§14).

## Endpoints

| Method | Path | Purpose | Contract |
|---|---|---|---|
| GET | `/health` | Status, version, active environment, optional provider readiness. Must return HTTP 200 (FR-015) | [[API-Contract]] |
| GET | `/api/v1/demo` | The deterministic demonstration event and its media references | [[API-Contract]] |
| POST | `/api/v1/analyze` | Accepts a short video upload or input reference; returns a processing job or the final event report | [[API-Contract]] |
| GET | `/api/v1/events/{event_id}` | The normalized event report | [[API-Contract]] |

Synchronous processing on `POST /api/v1/analyze` is acceptable for the hackathon
if it completes inside the NFR-003 target of 60 seconds. **A job queue is not
required** — [[PRD]] §19 says so explicitly, and §25 lists complex queues as a
prohibited time sink.

Every endpoint returns the event record as JSON (FR-014). A downloadable JSON
control in the UI is optional but preferred once the core is complete.

## Conventions

- **Error shape** — one envelope for every failure. Provider failures produce
  structured logs and a user-readable fallback notice; **never a stack trace and
  never a secret** (NFR-005). A degraded response is a success with a changed
  `processing_mode`, not an error.
- **Versioning** — decided: `/api/v1` path prefix on everything except
  `/health`, which stays unversioned so uptime checks never break on a bump.
- **Validation at the boundary** — Pydantic models on the Python side, TypeScript
  strict mode on the frontend, both generated from or checked against the shapes
  in [[06-Data-Model]] (NFR-004).
- **Upload constraints** — type and size limited on `POST /api/v1/analyze`;
  temporary files deleted after processing where practical (NFR-007).

> [!note] Contract before code
> Agreeing the shape first is what lets frontend and backend proceed in
> parallel — the main reason this note exists.

---
Related: [[PRD]] · [[API-Contract]] · [[06-Data-Model]] · [[04-Component-Design]] · [[02-Test-Cases]]
