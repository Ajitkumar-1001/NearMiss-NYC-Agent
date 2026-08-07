---
title: Safety Methodology
tags:
  - research
status: active
---

# Safety Methodology

How a "near miss" is defined and justified. This is the intellectual core — a
judge will push on it.

## Definition

A near miss is, **for our purposes**, an operational definition only. The
[[00-Source-of-Truth-PRD|PRD]] never defines "near miss" — the nearest object it
defines is the *candidate conflict* (§13 outcome `candidate_conflict_detected`):
a pairwise interaction between a vehicle and a vulnerable road user that the risk
engine scores above the candidate threshold using image-space evidence alone.

Treating the two as equivalent is our shorthand, not the PRD's, and it runs one
way only. §9 forbids the converse — claiming every candidate event is a true near
miss.

§13 fixes the taxonomy and this note does not restate it: three supported event
types, four outcome states of which `candidate_conflict_detected` is one, and
three severity levels derived from the visual conflict-risk proxy and evidence
quality and explicitly not a crash probability. Two of those outcome states —
no-event and insufficient-evidence — are acceptable results rather than
failures (§23 item 15). A run that finds nothing has still run.

The word *candidate* carries the whole claim. §9 forbids claiming that every
candidate event is a true near miss. The system prioritizes footage for a
human; it does not adjudicate it.

> [!todo] Literature grounding still owed
> The definition above is our own, taken from our own PRD. It is not grounded
> in published road-safety research — neither this vault nor the PRD cites any.
> A judge asking "whose definition is that?" has a real question, and the
> honest answer today is "ours". The literature definition and its source go
> here: {{NEARMISS_LITERATURE_CITATION}}. Until that lands, do not present the
> operational definition as an accepted standard, and do not import a number
> from memory to fill the gap.

## Established measures

| Measure | What it captures | Needs | Applicable to us? |
|---|---|---|---|
| Time to collision (TTC) | {{TTC_DEFINITION}} | {{TTC_REQUIREMENTS}} | No. §9 rules out calculating scientifically validated time-to-collision from an uncalibrated camera, and §19.1 lists a calibrated time-to-collision metric among the things the proxy is not |
| Post-encroachment time (PET) | {{PET_DEFINITION}} | {{PET_REQUIREMENTS}} | Undetermined. The [[00-Source-of-Truth-PRD|PRD]] never names PET, so the source of truth neither adopts nor excludes it |
| {{MEASURE}} | {{MEASURE_CAPTURES}} | {{MEASURE_NEEDS}} | Unknown until the literature review names it |

> [!warning] No thresholds, no definitions, on purpose
> The first two columns are placeholders because the PRD defines neither
> measure. It names time-to-collision only to exclude it, and it does not
> mention post-encroachment time at all. What TTC and PET measure, and what
> inputs they require, is general road-safety domain knowledge that this note
> owes a source for — it lands with {{NEARMISS_LITERATURE_CITATION}}, not from
> memory. No row carries a threshold value for the same reason, and §8 G8 rules
> out unsupported metric claims.

The nearest thing the system itself produces to a time-based measure is in §14
FR-022: the `vision-conflict-analytics` package output may include an optional
predicted image-space intersection and a frames-to-intersection proxy. Both are
expressed in image space and frame counts, and FR-022 forbids the package from
claiming calibrated metric distance or true time-to-collision without
perspective calibration. It resembles TTC in shape only.

## Our proxy and its limits

We approximate the above from monocular video — see
[[00-Source-of-Truth-PRD|PRD]] §29, which locks "visual conflict-risk proxy,
not true collision probability". §14 FR-010 defines it as a normalized 0–100
score over five transparent image-space factors: proximity, path overlap or
convergence, closing motion, vulnerable-road-user weighting, and an
evidence-quality adjustment. The initial reference formula weights proximity
and path overlap at 0.35 each, closing motion at 0.20, and vulnerable-user
weighting at 0.10, then multiplies that base by evidence quality. §14 FR-011
sets the initial candidate threshold at 70/100, configurable server-side.

Those weights are the operational definition of the proxy, and they are a
starting point rather than a validated calibration — FR-010 calls the result an
image-space prioritization proxy, not a crash probability.

What the proxy cannot know:

- **True distance.** Every factor is measured in image space. Pixel separation
  is not metric separation, and without calibration the engine cannot tell a
  genuinely close pair from a well-separated pair compressed along the camera's
  depth axis.
- **Intent.** Whether the driver saw the cyclist, or the pedestrian had already
  decided to stop, is not observable in a bounding box.
- **Driver reaction.** Braking or steering that prevented contact appears only
  as motion already baked into the track — the proxy sees the outcome, never
  the decision.
- **Whether anything was actually avoided.** §19.1 lists what the proxy is not,
  and the item this section turns on is first on that list: it is not a crash
  probability. It ranks image-space evidence for human review, and nothing
  more.

Two guards keep the proxy from overclaiming. §14 FR-008 refuses to score at all
below a minimum temporal-evidence bar, returning `insufficient_temporal_evidence`
instead of a guess. §19.2 then lets the evidence-quality adjustment consider
usable frames, track continuity, detection confidence, occlusion, duplicate
frames, and camera stability, and requires low quality to reduce the score or
prevent scoring entirely. The proxy is designed to decline to speak when the
video is too thin.

§24.4 requires testing at least eight risk-engine cases. Two of them are
converging vehicle–cyclist and vehicle–pedestrian paths, which the proxy is
supposed to catch. The other six cover non-converging movement, a static
pedestrian, detection jitter, unstable tracking, and evidence too thin to
score. §24.4 lists all eight neutrally; reading the latter six as the places a
proxy without depth is most exposed is our interpretation, not the PRD's.

Finally, the number stays ours: §8 G5 requires every risk score to decompose
into visible factors and forbids the LLM/VLM from originating it. Language
narrates the evidence; it never produces the score.

## Ethical framing

Surveillance, bias, and misuse considerations: [[10-Responsible-AI]].

The constraints that bind this note specifically: §19.3 requires every
high-severity candidate to recommend human review and forbids the application
from automatically contacting enforcement, dispatch, or issuing a 311 report.
§8 G8 rules out identity inference, biometric analysis, automated enforcement,
unsupported metric claims, and unnecessary retention of raw street imagery. §23
requires every report to expose its limitations, and requires that observed
evidence, derived metrics, public context, and generated explanation remain
separate.

Two more apply the moment a report sits next to public context data: §23
records that historical correlation is not causal proof, and §9 forbids
recommending definitive civil-engineering changes without expert review.

---
Related: [[00-Source-of-Truth-PRD|PRD]] §29 · [[10-Responsible-AI]] · [[04-Vision-Evaluation]] · [[03-Prior-Art]]
