---
title: Computer Vision Notes
tags:
  - research
status: draft
---

# Computer Vision Notes

Working notes on the vision side. Decisions that stick get promoted to an ADR.

## Pipeline stages

- [ ] Ingest / decode
- [ ] Detection
- [ ] Tracking
- [ ] Trajectory extraction
- [ ] Conflict scoring → see [[ADR-002-Visual-Conflict-Proxy]]

## Model candidates

| Model | Task | Speed | Accuracy | Runs where | Notes |
|---|---|---|---|---|---|
| {{MODEL}} | | | | | |

## Known hard cases

- Occlusion
- Camera motion / shake
- Night and weather
- Perspective — no depth from a single fixed camera
- {{HARD_CASE}}

> [!todo] Not filled in yet
> Record experiments as [[Experiment-Log]] notes rather than editing this
> file in place — we want the failures preserved.

---
Related: [[ADR-002-Visual-Conflict-Proxy]] · [[04-Vision-Evaluation]] · [[Model-Card]] · [[Experiment-Log]]
