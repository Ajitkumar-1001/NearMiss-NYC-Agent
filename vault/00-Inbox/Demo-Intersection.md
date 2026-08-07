---
title: Which intersection is the demo clip?
tags:
  - inbox
status: draft
---

# Which exact intersection or coordinates correspond to the demonstration clip?

> [!info] Source
> [[00-Source-of-Truth-PRD|PRD]] §30 — "Which exact intersection corresponds to
> the evidence sequence?"

- **Captured:** 2026-08-03
- **Source:** [[00-Source-of-Truth-PRD|PRD]] §30 (v2.1.0-FINAL), "Which exact
  intersection corresponds to the evidence sequence?"
- **Decision deadline:** Thursday, 6 August
- **Default if unresolved:** label only, from verified source metadata —
  **do not invent coordinates**
- **Depends on:** [[Camera-Source]] — the source determines the location

## Why it matters

Fills `location.label`, `location.latitude`, and `location.longitude` in
[[06-Data-Model]], and is the key that FR-013 uses to look up historical
collision context. Without it there is no public-data correlation, which
[[06-Success-Metrics]] lists as a product metric and the pitch leans on.

**Not a P0 blocker.** `latitude` and `longitude` are nullable by design, so P0
can ship with a `label` only and cached context keyed to that label. Getting real
coordinates upgrades the demo from plausible to verifiable.

## How to resolve

- [ ] Read the location from the camera's published metadata
- [ ] Confirm lat/long against a map, not just the camera name
- [ ] Sanity-check that the collision history for those coordinates is non-empty —
      an intersection with no reported collisions makes a weak demo
- [ ] Record the values in the fixture so the cached context matches

## Triage to

[[01-Datasets]] for the location record; fixture values into `demo/fixtures/`
under the captured-evidence baseline ([[00-Source-of-Truth-PRD|PRD]] §11.1).
Field names are already fixed in [[06-Data-Model]] — do not invent new ones.

The §30 default is not a formality. Shipping a fabricated lat/long would breach
the source-attribution requirement in §18.5 and the responsible-data rules in
§23 — a label with no coordinates is the honest P0 outcome.

---
Nothing stays in the inbox — see [[00-Triage]].
