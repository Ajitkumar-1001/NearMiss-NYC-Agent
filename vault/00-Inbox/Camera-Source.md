---
title: Which camera source for the demo clip?
tags:
  - inbox
status: draft
---

# Which official camera source provides the most reliable clip or feed?

> [!info] Source
> [[00-Source-of-Truth-PRD|PRD]] §30 — "Which organizer or city camera source
> is most reliable?"

- **Captured:** 2026-08-03
- **Source:** [[00-Source-of-Truth-PRD|PRD]] §30 (v2.1.0-FINAL)
- **Decision deadline:** Kickoff, 4:45 PM — the earliest deadline in §30
- **Default if unresolved:** use the already tested approved source

> [!warning] This one has a 4:45 PM clock
> §30 sets the deadline at kickoff, which means the candidate list below has to
> be built and tested **before Friday**. Arriving with no tested source and
> discovering the organizer feed is unusable leaves no time to fall back.

## Why it matters

Blocks [[04-MVP-Scope]] capability 1 — the bundled clip — and therefore
capabilities 2 through 8, which all derive from it. This is the critical-path
unknown for P0.

It also decides whether P2 is possible at all: a source with no live or sampled
feed caps the project at runtime analysis of uploaded clips.

Two High-impact rows in [[06-Risk-Register]] hang on the answer: the feed being
unavailable, and no near-miss occurring in the footage.

## Narrowed by the approved-source policy

[[00-Source-of-Truth-PRD|PRD]] §18.1 sets an approved source order to try, in this priority: (1)
organizer starter-pack live camera, (2) public NYC DOT still-image endpoint,
(3) 511NY REST camera via a self-service developer key, (4) phone/USB webcam
as an emergency fallback. [[00-Source-of-Truth-PRD|PRD]] §9 and §18.3 confirm P0 must not depend on
a signed NYC DOT bulk-feed agreement or a 511NY Developer Access Agreement —
so those paths are ruled out for the candidate list below, not just deprioritized.

The exact source pick for the demo is still {{CAMERA_SOURCE_FOR_DEMO}} — this
remains the [[00-Source-of-Truth-PRD|PRD]] §30 open question "Which organizer or
city camera source is most reliable?"

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
