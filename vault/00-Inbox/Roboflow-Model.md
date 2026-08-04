---
title: Which Roboflow model for detection?
tags:
  - inbox
status: draft
---

# Which Roboflow model or workflow best detects the required classes?

> [!info] Source
> [[PRD]] §30, open question (RF-DETR size/Workflow latency-accuracy
> tradeoff). Model family and licensing are now locked — see [[PRD]] §29, §17.

- **Captured:** 2026-08-03
- **Source:** [[PRD]] §30
- **Depends on:** [[Camera-Source]] — evaluate against the actual clip, not a
  benchmark

## Why it matters

Blocks P1 runtime detection, which is rung 3 of [[03-Scope-Ladder]]. It is
**not** a P0 blocker: [[PRD]] §11.1 puts precomputed
detections on the guaranteed captured-evidence path, so a bad answer here costs
the runtime demo, not the submission.

It does carry G7 weight — [[PRD]] §8 wants Roboflow used meaningfully, and
[[PRD]] FR-015 (§14) requires the fallback regardless of
which model wins.

**PRD v2.0 update:** the model *family* and license policy are no longer open
— only the exact size/variant is. [[PRD]] §29 locks Roboflow RF-DETR (via a
Workflow or hosted inference) as the preferred perception provider; [[PRD]]
§17 prefers RF-DETR N/S/M/L (Apache-2.0) weights, excludes Ultralytics YOLO
from the default implementation (AGPL-3.0), and excludes restricted RF-DETR
Plus weights unless their license is reviewed and accepted. Roboflow MCP /
Computer Vision Skills stay a development-plane accelerator only, never a
runtime dependency ([[PRD]] FR-020, principle 10). Which RF-DETR size or
Workflow — {{RF_DETR_VARIANT}} — remains open ([[PRD]] §30).

## How to resolve

- [ ] Shortlist RF-DETR sizes/variants (N/S/M/L, Apache-2.0) and Roboflow
      Workflow options covering all six FR-005 classes: person, bicycle,
      motorcycle, car, bus, truck
- [ ] Run each against the chosen clip, not against a published benchmark
- [ ] **Weight the vulnerable-road-user cases hardest** — a model that nails cars
      and misses the cyclist is useless here ([[06-Risk-Register]] row 4)
- [ ] Check the confidence distribution at the frames that matter, not the mean
- [ ] Record latency against the 60 s NFR-006 (§15) budget for the whole clip

## Triage to

[[04-Computer-Vision-Notes]] for the evaluation; adapter and fallback details to
[[07-Provider-Adapters]]; the choice to [[05-Decision-Log]]. If the model shapes
the detection contract, update [[06-Data-Model]].

---
Nothing stays in the inbox — see [[00-Triage]].
