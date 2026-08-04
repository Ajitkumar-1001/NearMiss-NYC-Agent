---
title: ADR-005 No Authentication
tags:
  - adr
status: active
---

# ADR-005 — No Authentication

## Status

Accepted — [[PRD]] §29, approved for v2.0.

## Context

[[PRD]] §9 rules out authentication, accounts, roles, billing, and subscriptions
as non-goals. PRD v2.0 no longer carries the v1 §25 prohibited-time-sinks list —
that list was restructured into the §27 event-day execution-plan timeline — but
the same exclusion holds: authentication appears nowhere in §11.1's P0 scope.
More decisively, §26's definition of done requires the deployed agent to **be
publicly reachable without authentication** — a judge who has to be handed
credentials is a judge who may not reach the demo at all.

There is also nothing to protect. The system holds no personal data by
construction ([[ADR-006-No-Identity-Recognition]]), keeps no per-user state, and
persists no database ([[06-Data-Model]]). A login would guard an empty room.

## Decision

No user accounts, sessions, or authentication. Anything deployed is public.

## Consequences

**Positive**
- Judges open a URL and it works. No credential is a thing that can fail live.
- No session store, no user table, no password reset, no role model.
- Removes an entire category of hackathon time sink before it starts.

**Negative**
- Everything deployed is public, **including `POST /api/v1/analyze`**. Uploads
  must therefore be constrained by type and size (NFR-010), because there is no
  identity to rate-limit against.
- Nothing that must stay private can be deployed on this stack.
- Secrets must remain strictly server-side — the public surface makes any
  client-side key immediately public.

**Accepted trade-off**
- A public endpoint is accepted for the duration of the hackathon. It is
  survivable only because there is no personal data and no persistence behind
  it; if either changes, this ADR must be revisited before deployment.

## Alternatives considered

| Alternative | Why not |
|---|---|
| Basic auth or a shared password | One more thing to fail on stage, and judges must be told it |
| IP allowlist for the venue | Venue networks are unpredictable; a NAT change locks everyone out |
| Full authentication | Ruled out as a non-goal (§9) and guards data that does not exist |

---
Related: [[PRD]] · [[05-Non-Goals]] · [[08-Deployment]] · [[01-System-Context]] · [[10-Responsible-AI]] · [[ADR-006-No-Identity-Recognition]] · [[00-ADR-Index]]
