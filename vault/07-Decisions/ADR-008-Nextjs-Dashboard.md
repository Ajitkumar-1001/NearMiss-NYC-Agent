---
title: ADR-008 Nextjs Dashboard
tags:
  - adr
status: active
---

# ADR-008 — Next.js Dashboard

## Status

Accepted **with a stated escape hatch** — [[PRD]] §27, approved for v1.0.

## Context

[[PRD]] §20 requires ten components on a single dashboard — replay, trajectory
overlay, risk score, factor breakdown, evidence, historical context,
explanation, limitations, processing-mode badge, and system status — across six
states including *completed with fallback* and *no candidate conflict found*.

The hard part is the overlay: bounding boxes, track labels, trajectory trails,
pair highlighting, and a conflict marker drawn in sync with video playback
(FR-013). That is Canvas or SVG work over a `<video>` element.

NFR-004 requires TypeScript strict mode and typed API responses; NFR-006
requires that critical state never be conveyed by colour alone. [[PRD]] §25
warns against unnecessary design-system work, so the framework has to be one
that ships a single page fast.

## Decision

The dashboard is **Next.js with TypeScript in strict mode and Tailwind CSS**,
with Canvas or SVG overlays for the replay annotations.

> [!warning] The escape hatch is part of the decision
> [[PRD]] §27 locks this as "Next.js dashboard **unless event constraints
> strongly favor a faster UI**." If a mandatory starter repository, a required
> output format, or a time crisis makes a simpler UI the right call, switching is
> pre-approved — record it in [[05-Decision-Log]] and supersede this ADR. What is
> *not* negotiable is [[PRD]] §20's component list and NFR-006.

## Consequences

**Positive**
- One framework for routing, build, and deploy of a single-page dashboard.
- TypeScript strict satisfies NFR-004 on the frontend side.
- Tailwind avoids building a design system, per §25.
- Large ecosystem for video and Canvas overlay work.

**Negative**
- Heavier than the one page it serves; the server/client boundary is a real
  source of subtle bugs under time pressure.
- Deployment is a second target alongside the backend — [[PRD]] §15.1 leaves
  bundled-vs-separate open, and it stays open in [[08-Deployment]].

**Accepted trade-off**
- Framework weight is accepted for a familiar path to a polished single page.
  The escape hatch above is the release valve if that stops being true.

## Alternatives considered

| Alternative | Why not |
|---|---|
| Static HTML + vanilla JS | Fastest to ship, but state handling across six UI states gets messy quickly |
| Vite + React SPA | Genuinely viable and lighter; Next.js chosen for the single deploy path and familiarity |
| Server-rendered templates from FastAPI | One less deploy target, but frame-synced Canvas overlays fight the model |
| Streamlit or similar | Fast to build, but cannot meet FR-013's frame-synced overlay requirement |

---
Related: [[PRD]] · [[04-Design-Review]] · [[04-Component-Design]] · [[08-Deployment]] · [[05-Decision-Log]] · [[00-ADR-Index]]
