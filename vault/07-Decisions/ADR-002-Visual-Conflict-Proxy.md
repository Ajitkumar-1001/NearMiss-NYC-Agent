---
title: ADR-002 Visual Conflict Proxy
tags:
  - adr
status: active
---

# ADR-002 — Visual Conflict Proxy

## Status

Accepted — [[00-Source-of-Truth-PRD|PRD]] §27, approved for v1.0.

## Context

The camera is fixed, monocular, and uncalibrated. There is no depth, no metric
scale, and no ground truth. Recovering real-world distance would require camera
calibration, which [[00-Source-of-Truth-PRD|PRD]] §25 lists as a prohibited time sink before P0, and
§8 explicitly rules out calculating scientifically validated time-to-collision
from an uncalibrated camera.

Two High-impact risks in [[06-Risk-Register]] pull in the same direction:
perspective invalidating any metric claim, and judges interpreting the output as
a crash prediction. §21.5 forbids claiming the score equals collision
probability, and G3 (§7) requires every score to decompose into visible factors.

So the question is not "proxy or measurement" — measurement is unavailable. It
is whether to ship an honest proxy or nothing.

## Decision

Conflict severity is scored with a **visual conflict-risk proxy** computed from
monocular video in image space, not a physically calibrated measurement and not
a collision probability.

The proxy is a normalized 0–100 score from four transparent factors (FR-006):

```text
risk =
  0.35 × proximity
+ 0.35 × path_overlap
+ 0.20 × closing_motion
+ 0.10 × vulnerable_user
```

Weights may be tuned against the selected demo clip; every change is recorded in
[[05-Decision-Log]]. Severity (`low` / `medium` / `high`) derives from the proxy
and evidence quality. The UI must never present image-space motion as real-world
metric distance (FR-004), and every report states this limitation.

## Consequences

**Positive**
- Computable with no calibration, so it ships inside the time box.
- Fully decomposable into four named factors, satisfying G3 and §9 principle 1.
- Honest under direct questioning — the limitation is stated rather than
  discovered by a judge.

**Negative**
- Scores are not comparable across cameras, angles, or focal lengths.
- Precision and recall are unmeasured; a high score may not be a real near-miss,
  which [[00-Source-of-Truth-PRD|PRD]] §8 concedes explicitly.
- The weights are a reasoned starting point, not a validated model.

**Accepted trade-off**
- Metric rigour is given up for something that ships, explains itself, and does
  not overclaim. Calibrated geometry is R1 work ([[00-Source-of-Truth-PRD|PRD]] §28).

## Alternatives considered

| Alternative | Why not |
|---|---|
| True time-to-collision from calibrated geometry | Calibration is a prohibited time sink (§25) and there is no ground truth to validate against |
| Homography onto an assumed ground plane | Needs per-camera reference measurements we do not have, and would still produce an unvalidated metric claim |
| Learned severity classifier | No labelled data; training a model is an explicit non-goal (§8) |
| Report raw detections and let the human judge | Fails the job to be done in §6 — the analyst wants to know *why* it was flagged |

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[05-Safety-Methodology]] · [[04-Computer-Vision-Notes]] · [[04-Vision-Evaluation]] · [[10-Responsible-AI]] · [[00-ADR-Index]]
