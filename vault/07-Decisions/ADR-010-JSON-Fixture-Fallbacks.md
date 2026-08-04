---
title: ADR-010 JSON Fixture Fallbacks
tags:
  - adr
status: active
---

# ADR-010 — JSON Fixtures As Operational Fallbacks

## Status

Accepted — [[PRD]] §27, approved for v1.0.

## Context

[[ADR-001-Deterministic-Demo-First]] makes the fixture path the guaranteed
product, and [[ADR-003-Provider-Adapter-Architecture]] gives every provider a
fixture implementation. What remains is a status question that decides how the
fixtures are treated day to day.

Fixtures are usually test data: approximate, allowed to drift, excluded from the
build. Here they are the opposite. [[PRD]] §17 puts precomputed
detections/tracks, cached public-data context, and the template explanation
directly on the fallback ladder — they are what production serves when a
provider fails. §10.1 makes them the substance of P0, and §21.10 requires them
to be labelled as fixtures in the UI.

Treating a load-bearing artifact as test data is how the demo diverges from real
behaviour without anyone noticing.

## Decision

JSON fixtures in `demo/fixtures/` are **operational fallbacks, not test data**.
They are committed on purpose, they must match the shapes in [[06-Data-Model]]
exactly, and serving them is a labelled success — never a silent substitution.

Three rules follow:

1. **Fixture parity.** A fixture whose shape drifts from the live contract is a
   bug of the same severity as a broken endpoint.
2. **Always labelled.** Serving a fixture sets `processing_mode` accordingly and
   the UI states it (FR-012, §21.10). Fallback is never disguised as inference.
3. **Verified before submission.** [[PRD]] §22.5 requires the JSON fixture and
   annotated media to be verified as a release gate — see
   [[05-Demo-Reliability]].

## Consequences

**Positive**
- The fallback path gets the same care as the live path, because it *is* a
  live path.
- Frontend development proceeds against real payload shapes with no backend.
- Makes the honesty requirement in §9 principle 6 concrete and checkable.

**Negative**
- Every contract change means updating fixtures in lockstep, or P0 breaks.
- Committed media makes the repository larger.

**Accepted trade-off**
- Fixture maintenance is accepted as ongoing cost rather than one-time setup.
  That cost is the price of [[ADR-001-Deterministic-Demo-First]].

## Alternatives considered

| Alternative | Why not |
|---|---|
| Fixtures as test data only, live path for the demo | Contradicts [[ADR-001-Deterministic-Demo-First]] outright |
| Generate fixtures at build time from a live call | Requires a working provider at build time — the dependency being removed |
| Silently fall back without labelling | Violates FR-012 and §21.10; the disclosure *is* the responsible-AI story |

---
Related: [[PRD]] · [[06-Data-Model]] · [[07-Provider-Adapters]] · [[05-Demo-Reliability]] · [[ADR-001-Deterministic-Demo-First]] · [[ADR-003-Provider-Adapter-Architecture]] · [[00-ADR-Index]]
