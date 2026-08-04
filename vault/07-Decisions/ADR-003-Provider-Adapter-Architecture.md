---
title: ADR-003 Provider Adapter Architecture
tags:
  - adr
status: active
---

# ADR-003 — Provider Adapter Architecture

## Status

Accepted — [[PRD]] §27, approved for v1.0.

## Context

FR-011 mandates a fallback for every external provider — Roboflow to fixture
detections, the runtime tracker to precomputed tracks, NYC Open Data to cached
context, Gemini to a deterministic template, and the live feed to an uploaded or
bundled clip. [[PRD]] §17 orders those fallbacks into a ladder that must degrade
without corrupting the level below.

That is five boundaries, each needing two implementations and a switch between
them. Sponsor credentials may arrive late or rate-limit, and G5 (§7) still wants
each integration to be meaningful. [[ADR-001-Deterministic-Demo-First]] requires
the fixture side to be the guaranteed path rather than a test double.

Written ad hoc, that becomes five different try/except shapes and no single
place that knows which mode is active — which FR-012 requires the UI to state.

## Decision

Every external model or data provider is reached through an adapter with a fixture implementation. Business logic never imports a vendor SDK directly.

Each adapter exposes provider metadata, which flows into the evidence package
(FR-008), and reports which implementation served the request, which is what the
orchestrator turns into the single `processing_mode` value.

## Consequences

**Positive**
- FR-011's five fallbacks become one interface each, not five bespoke rescues.
- Fixture implementations *are* the P0 path, so they are load-bearing rather
  than throwaway.
- Swapping or dropping a provider is a local change late in the build.
- Provider readiness is reportable on `GET /health` ([[05-API-Contracts]]).

**Negative**
- One indirection layer must exist before any real provider works.
- Under time pressure there is a genuine risk of abstracting more than the five
  known boundaries need.

**Accepted trade-off**
- A small amount of upfront structure buys the graceful degradation that §9
  principle 6 requires. The abstraction is capped at the five boundaries FR-011
  names — no adapter without a fallback to justify it.

## Alternatives considered

| Alternative | Why not |
|---|---|
| Call vendor SDKs directly, wrap in try/except | Fallback logic scatters, and nothing owns the active-mode answer FR-012 needs |
| Environment flags per provider | Same indirection with less clear ownership, and no place for provider metadata |
| Fixtures only, no runtime providers at all | Fails G5 — sponsor integrations are part of the submission |

---
Related: [[PRD]] · [[07-Provider-Adapters]] · [[ADR-001-Deterministic-Demo-First]] · [[ADR-010-JSON-Fixture-Fallbacks]] · [[03-Sponsor-Resources]] · [[04-Component-Design]] · [[00-ADR-Index]]
