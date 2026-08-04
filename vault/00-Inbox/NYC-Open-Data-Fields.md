---
title: Which NYC Open Data fields are stable?
tags:
  - inbox
status: draft
---

# Which NYC Open Data fields are stable enough for runtime enrichment?

> [!info] Source
> [[PRD]] §29, open question 4.

- **Captured:** 2026-08-03
- **Source:** [[PRD]] §29

## Why it matters

Determines the `HistoricalContext` shape in [[06-Data-Model]] — `source`,
`nearby_collision_count`, `radius_meters`, `retrieved_at` — and whether FR-009's
runtime lookup is worth attempting at all.

**Not a P0 blocker.** P0 serves cached context by design. But the cached fixture
has to be shaped like the real response, or [[ADR-010-JSON-Fixture-Fallbacks]]'s
fixture-parity rule is violated the moment the runtime path is switched on.

The answer also sets the radius, which is the one number a judge is most likely
to ask about.

## How to resolve

- [ ] Inspect the collisions dataset schema and confirm which fields are
      consistently populated, not merely present
- [ ] Confirm whether vulnerable-road-user involvement is reliably distinguishable
      ([[PRD]] FR-009 says "where available" — verify which it is)
- [ ] Decide the search radius and be able to justify it
- [ ] Check rate limits and whether an API token is needed
- [ ] Capture one real response as the cached fixture

## Triage to

[[01-Datasets]] for the field analysis; the cached response into `demo/fixtures/`;
the radius and any field decisions into [[05-Decision-Log]]. Confirm the final
shape against [[06-Data-Model]] before writing the adapter.

> [!warning] Correlation, not cause
> Whatever fields are used, [[PRD]] §21.8 forbids presenting historical
> correlation as causal proof, and FR-009 requires this context to render
> visibly separate from what the clip showed.

---
Nothing stays in the inbox — see [[00-Triage]].
