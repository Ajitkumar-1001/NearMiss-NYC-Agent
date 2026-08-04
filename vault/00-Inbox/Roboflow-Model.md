---
title: Which Roboflow model for detection?
tags:
  - inbox
status: draft
---

# Which Roboflow model or workflow best detects the required classes?

> [!info] Source
> [[PRD]] §29, open question 2.

- **Captured:** 2026-08-03
- **Source:** [[PRD]] §29
- **Depends on:** [[Camera-Source]] — evaluate against the actual clip, not a
  benchmark

## Why it matters

Blocks P1 runtime detection, which is rung 3 of [[03-Scope-Ladder]]. It is
**not** a P0 blocker: [[ADR-001-Deterministic-Demo-First]] puts precomputed
detections on the guaranteed path, so a bad answer here costs the runtime demo,
not the submission.

It does carry G5 weight — [[PRD]] §7 wants Roboflow used meaningfully, and
[[ADR-003-Provider-Adapter-Architecture]] requires the fallback regardless of
which model wins.

## How to resolve

- [ ] Shortlist models covering all six FR-002 classes: person, bicycle,
      motorcycle, car, bus, truck
- [ ] Run each against the chosen clip, not against a published benchmark
- [ ] **Weight the vulnerable-road-user cases hardest** — a model that nails cars
      and misses the cyclist is useless here ([[06-Risk-Register]] row 4)
- [ ] Check the confidence distribution at the frames that matter, not the mean
- [ ] Record latency against the 60 s NFR-003 budget for the whole clip

## Triage to

[[04-Computer-Vision-Notes]] for the evaluation; adapter and fallback details to
[[07-Provider-Adapters]]; the choice to [[05-Decision-Log]]. If the model shapes
the detection contract, update [[06-Data-Model]].

---
Nothing stays in the inbox — see [[00-Triage]].
