---
title: ADR-006 No Identity Recognition
tags:
  - adr
status: active
---

# ADR-006 — No Identity Recognition

## Status

Accepted — [[PRD]] §27, approved for v1.0.

## Context

The system points cameras at public streets and analyses the people in them.
That capability is one small step from surveillance, and the step is easy to
take by accident — a detector that finds "person" is a short distance from a
model that recognises *which* person.

[[PRD]] §21 draws the line explicitly in its first three requirements: no face
recognition, no plate recognition, no demographic inference. §8 restates it as a
non-goal, §5.3 excludes law-enforcement identification and automated enforcement
from the target users, and NFR-008 forbids identity inference and long-term
storage of unnecessary raw video.

This is the decision that makes the product defensible rather than merely legal,
and it is the one most likely to be eroded by a well-meaning feature request.

## Decision

The system analyses road-user **classes and movement**, never individual
identities. Specifically it will not perform face recognition, licence-plate
recognition, demographic inference, individual behaviour scoring, or any form of
personal identification — and will not store raw video longer than processing
requires.

Detections carry a class name from the FR-002 set and a track identifier that is
scoped to a single clip. Track identifiers are not identities and must never be
correlated across clips.

## Consequences

**Positive**
- Removes the entire privacy-risk surface rather than managing it.
- Makes [[ADR-005-No-Authentication]] safe — there is no personal data behind
  the public endpoint.
- Simplifies retention to "delete after processing" ([[06-Data-Model]]).
- Answers the sharpest question a judge can ask about a street-camera product.

**Negative**
- Rules out per-vehicle behaviour history and repeat-offender analysis, which
  some transport-safety workflows genuinely want.
- Cross-clip re-identification is unavailable, so recurring-conflict analysis
  must work at the *location* level, not the *road-user* level.

**Accepted trade-off**
- Analytical power at the individual level is given up permanently, not
  deferred. The Revisit column for this row in [[05-Non-Goals]] reads *Never*.

## Alternatives considered

| Alternative | Why not |
|---|---|
| Blur faces and plates, keep recognition internally | Still builds the capability; the boundary would exist only in the UI layer |
| Anonymised persistent road-user IDs | Pseudonymous identity is still identity, and re-identification risk is real |
| Defer the decision until post-hackathon | Capabilities are far harder to remove than to never build |

---
Related: [[PRD]] · [[10-Responsible-AI]] · [[05-Safety-Methodology]] · [[03-Users-and-Jobs]] · [[05-Non-Goals]] · [[ADR-005-No-Authentication]] · [[00-ADR-Index]]
