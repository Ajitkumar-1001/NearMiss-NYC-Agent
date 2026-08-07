---
title: Computer Vision Notes
tags:
  - research
status: active
---

# Computer Vision Notes

Working notes on the vision side. This note holds the reasoning, not the ruling —
anything here that ends up constraining the build gets promoted into
[[00-Source-of-Truth-PRD|PRD]] §29, and smaller calls go to [[05-Decision-Log]].

## Pipeline stages

- [ ] Ingest / decode — FR-004 (four accepted input shapes; uploaded MP4 is P1,
      sampled live frames P2). Only the captured sequence is guaranteed to carry
      enough frames for the stages below — §29 locks captured-feed evidence
      replay as the guaranteed demonstration, and §24.3 requires single-frame
      input to return `insufficient_temporal_evidence`.
- [ ] Detection — FR-005 (six road-user classes; the per-detection fields are
      specified there).
- [ ] Annotation — `supervision` for annotation, zones, and normalized detection
      utilities (§17 supporting libraries), locked as a preferred post-processing
      tool by §29. In the §16 architecture diagram it hangs off the vision
      provider in parallel with the tracker, so it is a rendering and
      normalization branch rather than an input to the gate.
- [ ] Tracking — FR-006. Track identifiers plus centroid history, multi-frame
      only; explicitly not required for a single live snapshot. Association is a
      post-processing step (§17 lists ByteTrack or Roboflow `trackers`).
- [ ] Trajectory extraction — FR-007. Image-space trails plus direction and
      closing-motion proxies, derived only for stable tracks.
- [ ] Conflict scoring — FR-008 (temporal-evidence gate), FR-009 (candidate-pair
      filtering, vehicle-to-vulnerable-road-user only), FR-010 (normalized 0–100
      proxy). Not owned by this note: the engine lives in
      [[11-Vision-Conflict-Analytics-Package]], locked in
      [[00-Source-of-Truth-PRD|PRD]] §29.

> [!note] A detected class is not a scored class
> FR-005 requires the detector to handle motorcycle, but §13 names only three
> supported event types — pedestrian, cyclist, and turning-vehicle-vs-vulnerable-user
> conflicts — and FR-009 restricts the engine to supported
> vehicle-to-vulnerable-road-user pairs. So detection coverage is wider than
> scoring coverage, and the detector must not be tuned as though every class it
> emits will be scored. Which pairs count is the taxonomy question owned by
> [[05-Safety-Methodology]], not this note.

What "working" means for the detection, tracking, and trajectory stages on the
evidence sequence is defined in [[00-Source-of-Truth-PRD|PRD]] §24.2, and ingest
behaviour falls under §24.3 live-source evaluation. Both tracked in
[[04-Vision-Evaluation]].

> [!warning] Image space only
> §19.1 states the output is not a crash probability or a calibrated
> time-to-collision metric. Nothing in this pipeline is calibrated for
> perspective, so per FR-007 the UI must not present image-space motion as metric
> distance or calibrated speed, and per FR-022 the package must not claim
> calibrated metric distance or true time-to-collision.

## Model candidates

Preference order and the licensing constraints below are set by
[[00-Source-of-Truth-PRD|PRD]] §17. Speed and accuracy columns stay empty until
we measure them ourselves — no vendor numbers.

| Model | Task | Speed | Accuracy | Runs where | Notes |
|---|---|---|---|---|---|
| Roboflow Workflow, RF-DETR-compatible detection path | Detection (FR-005) | {{LATENCY}} | {{ACCURACY}} | Roboflow-hosted workflow | §17 preference 1. Preferred perception provider per §29. |
| RF-DETR via Roboflow hosted / serverless inference | Detection (FR-005) | {{LATENCY}} | {{ACCURACY}} | Roboflow hosted / serverless | §17 preference 2. |
| Local RF-DETR small / nano-compatible path | Detection (FR-005) | {{LATENCY}} | {{ACCURACY}} | Local, CPU-first Cloud Run (§29) | §17 preference 3, "where runtime permits" — CPU-first is the constraint to test against. |
| Stored detections | Replay, no inference (FR-015 provider fallback) | n/a | n/a | Bundled with the captured evidence sequence | §17 preference 4; the FR-015 fallback for Roboflow hosted inference. §29 locks captured-feed evidence replay itself as the guaranteed demonstration and fallback. |
| ByteTrack or Roboflow `trackers` | Temporal association (FR-006) | {{LATENCY}} | {{ACCURACY}} | Post-processing, alongside whichever detector wins | §17 supporting libraries; §29 locks only "a lightweight tracker", so either satisfies the PRD. Selection status: {{TRACKER_CHOICE}}. |
| Ultralytics YOLO | Detection | n/a | n/a | — | §17: shall not be the default implementation — AGPL-3.0 obligations complicate a clean permissive submission. |
| RF-DETR Plus (restricted weights) | Detection | excluded | excluded | — | Excluded by §17 unless the license is reviewed and accepted. |

Licensing rule from §17, in short: prefer RF-DETR N/S/M/L weights covered by
Apache-2.0, and prefer MIT or Apache-2.0 supporting libraries.

Which exact RF-DETR size or Workflow wins is the [[00-Source-of-Truth-PRD|PRD]]
§30 open question "Which RF-DETR size or Workflow gives the best tradeoff?" —
decision deadline Thursday 6 August, and the default if it is still open is the
smallest already validated option. Working notes go in [[Roboflow-Model]].

## Known hard cases

Each of these degrades evidence rather than producing a wrong answer directly:
each one lands on the §19.2 evidence-quality factor, which is owned by
[[05-Safety-Methodology]].

- Occlusion — named in §19.2 outright, and it breaks the "acceptable track
  continuity" condition in FR-008's gate.
- Camera motion / shake — the camera-stability input in §19.2.
- Night and weather — pushes detection confidence down, one of the §19.2
  evidence-quality inputs, which reduces or suppresses the FR-010 score rather
  than tripping the FR-008 gate; the classes in FR-005 do not get easier in the
  dark.
- Perspective — no depth from a single uncalibrated monocular source. This is why
  FR-007 stays in image space and why FR-022 bars the package from claiming
  metric distance or true time-to-collision without perspective calibration.
- Duplicate / repeated frames — a static or stalled feed can look like a long
  sequence while carrying one observation. §19.2 counts this against evidence
  quality; §24.3 requires duplicates be caught by hash.
- {{HARD_CASE}}

> [!info] The honest answer is usually "not enough evidence"
> FR-008 gates on track count, per-track usable-observation count, track
> continuity, and timestamp ordering — see the PRD for the exact conditions. When
> the gate fails the result is `insufficient_temporal_evidence`. §19.2 goes
> further: low evidence quality shall reduce the score or prevent scoring
> entirely. So a hard case is not a modelling problem to paper over with a lower
> threshold — the correct output is the refusal, and §29 makes an
> insufficient-evidence result a valid one.

> [!info] Experiments live elsewhere
> Record experiments as [[Experiment-Log]] notes rather than editing this
> file in place — we want the failures preserved. Per-model results belong in a
> [[Model-Card]].

---
Related: [[00-Source-of-Truth-PRD|PRD]] §17 · §19.2 · §24.2 · §29 · [[04-Vision-Evaluation]] · [[05-Safety-Methodology]] · [[11-Vision-Conflict-Analytics-Package]] · [[Roboflow-Model]] · [[Model-Card]] · [[Experiment-Log]]
