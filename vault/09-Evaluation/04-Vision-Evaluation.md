---
title: Vision Evaluation
tags:
  - evaluation
status: draft
---

# Vision Evaluation

Quality of detection, tracking, and conflict scoring.

## Ground truth

- **Source:** {{GROUND_TRUTH_SOURCE}}
- **Size:** {{N_CLIPS}} clips / {{N_EVENTS}} labelled events
- **Labelled by:** {{LABELLER}}

> [!todo] Not filled in yet
> Without labelled ground truth, no accuracy claim can be made. If we don't
> have it, say so explicitly rather than implying numbers.

## Metrics

| Metric | Definition | Target | Actual |
|---|---|---|---|
| Detection precision | | {{TARGET}} | — |
| Detection recall | | {{TARGET}} | — |
| Conflict-score agreement with labels | | {{TARGET}} | — |

## Known limits

The score is a proxy, not a measurement — [[PRD]] §29 and
[[05-Safety-Methodology]]. Report it as such in [[02-2-Minute-Pitch]].

## Results log

Record runs as [[Experiment-Log]] notes; summarise here.

---
Related: [[PRD]] §29 · [[05-Safety-Methodology]] · [[06-Success-Metrics]] · [[Model-Card]]
