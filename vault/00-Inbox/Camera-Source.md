---
title: Which camera source for the demo clip?
tags:
  - inbox
status: draft
---

# Which official camera source provides the most reliable clip or feed?

> [!info] Source
> [[PRD]] §29, open question 1.

- **Captured:** 2026-08-03
- **Source:** [[PRD]] §29

## Why it matters

Blocks [[04-MVP-Scope]] capability 1 — the bundled clip — and therefore
capabilities 2 through 8, which all derive from it. This is the critical-path
unknown for P0.

It also decides whether P2 is possible at all: a source with no live or sampled
feed caps the project at runtime analysis of uploaded clips.

Two High-impact rows in [[06-Risk-Register]] hang on the answer: the feed being
unavailable, and no near-miss occurring in the footage.

## How to resolve

- [ ] List candidate official NYC sources with endpoint, auth, and licence
- [ ] Establish whether each serves video or periodic stills — stills change the
      frame-sampler design in [[04-Component-Design]]
- [ ] Pull one candidate 10–20 second clip
- [ ] **Verify it actually contains a usable vehicle–VRU interaction** before
      building anything on it ([[06-Risk-Register]] row 4 mitigation: validate the
      clip early)
- [ ] Confirm redistribution is permitted, since the clip gets committed to
      `demo/fixtures/`

## Triage to

[[02-Live-Feeds]] for the candidate source table. The chosen clip is recorded in
[[01-Datasets]], and the choice itself in [[05-Decision-Log]].

Blocks [[Demo-Intersection]], which cannot be answered until the source is known.

---
Nothing stays in the inbox — see [[00-Triage]].
