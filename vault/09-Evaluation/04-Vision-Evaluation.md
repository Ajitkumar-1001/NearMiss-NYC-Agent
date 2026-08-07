---
title: Vision Evaluation
tags:
  - evaluation
status: active
---

# Vision Evaluation

Quality of detection, tracking, and trajectory output for the selected evidence
sequence.

> [!danger] Blocked today — nothing here can be run yet
> [[00-Source-of-Truth-PRD|PRD]] §24.2 evaluates **the selected evidence
> sequence**. There is no such sequence: `demo/fixtures/` contains only
> `README.md`, so `FixtureVision.detect` (`providers/vision.py:45`) and
> `FixtureTracker.track` (`providers/tracking.py:39`) raise `FileNotFoundError`
> through `base.py:56`. The runtime path declines instead —
> `RoboflowVision.detect` raises `ProviderUnavailable` at
> `providers/vision.py:26-29`, "no API key or model configured", which is the
> branch actually taken while no key exists. The second raise at
> `providers/vision.py:32`, "runtime detection not implemented at P0", is
> unreachable until one is configured. Both declines are deliberate.
> Neither path produces a detection. Unblocking needs a captured clip plus
> `detections.json` and `tracks.json`, before the §11.1 readiness gate on
> **Thursday 6 August, 8:00 PM America/New_York**.

Contrast [[03-Agent-Evaluation]], which is runnable now because
`TemplateExplanation` reads no fixture. This one is not.

## Ground truth

- **Source:** {{GROUND_TRUTH_SOURCE}}
- **Size:** {{N_CLIPS}} clips / {{N_EVENTS}} labelled events
- **Labelled by:** {{LABELLER}}

> [!todo] Not filled in yet
> Without labelled ground truth, no accuracy claim can be made. If we don't
> have it, say so explicitly rather than implying numbers.

**No labelled set exists, and none is planned before the event.** The
placeholders above stay unfilled on purpose — they are the honest record of an
absence, not a task. This is exactly why §24.2 is scoped as five qualitative
checks and asks for no precision, recall, or agreement figure: those numbers
are unobtainable here, so the PRD does not request them.

## Metrics

§24.2's five checks, scored **pass/fail each**, judged by a human viewing the
overlay and reading the payload. There is no target number to hit and no
automated scorer.

The checks are already tabulated as cases 30–34 in [[02-Test-Cases]] §E; that
note's `Automated?` and `Status` columns are the single source for what is
blocked and on what. This table adds only how each check is judged and where it
lands in code.

| # | §24.2 check | Case | How it is judged | Where it lands in code | Result |
|---|---|---|---|---|---|
| V1 | Required classes detected in key frames | [[02-Test-Cases]] 30 | Reviewer names the road users visible in the key frames and confirms each appears in `detections.json` | `models.py:36` `RoadUserClass` — the six FR-005 classes exactly | |
| V2 | Track identities stable through the conflict window | [[02-Test-Cases]] 31 | One `track_id` per road user across `time_window`; no ID swap, no mid-window renumber | `models.py:65` `Track.track_id` + `centroid_history` | |
| V3 | Trajectory trails align visually with objects | [[02-Test-Cases]] 32 | Reviewer overlays `centroid_history` on the clip; trails sit on the objects, not beside them | `models.py:115` `EvidenceOverlay` feeds §11.3 surface 2, Vision Canvas | |
| V4 | Representative frame clearly shows the event | [[02-Test-Cases]] 33 | Reviewer confirms the frame shows both participants inside the conflict window | `models.py:166` `representative_frame` — **expected fail**, see below | |
| V5 | Stored and runtime outputs use the same normalized schema | [[02-Test-Cases]] 34 | Same `Detection`/`Track` models validate both fixture-loaded and runtime-produced output | `providers/vision.py:47` `Detection.model_validate` | |

Every Result cell is empty because nothing has been run. Do not fill one from a
code read.

> [!warning] Failures this evaluation should catch
> **V4 — no representative frame is ever produced.** `orchestrator.py:216`
> hardcodes `representative_frame=None`, and `models.py:166` declares it
> `str | None = None`, so the payload validates while carrying nothing to show.
> `orchestrator.py:218` hardcodes `clip_path=None` in the same way, which also
> leaves V3 with no image to align trails against.
>
> **V1 — detections carry no provider metadata.** FR-005 requires class,
> confidence, bounding box, frame index, timestamp, **and provider metadata**
> per detection. `models.py:55` `Detection` has the first five. Provider
> identity exists only once per event, at `models.py:134` `ProviderMetadata`,
> so a mixed-provider detection set could not be told apart.
>
> **V2 — track continuity is never computed.** FR-008's gate requires
> "acceptable track continuity" and at least three usable observations per
> track. `risk.py:97-108` `_has_enough_evidence` gates on `min_track_points`
> (`config.py:72`, set to 8), a minimum of two time-paired samples
> (`risk.py:105`), and `min_overlap_seconds` (`risk.py:107-108`,
> `config.py:73`). None of those is continuity, and 8 is not FR-008's three
> usable observations. Same defect as the track-continuity entry in
> [[02-Test-Cases]]'s open-gaps list and [[04-Task-Board]] C-8 — one defect, not
> three.
>
> **V5 — the schema is unverifiable while one side declines.** `models.py:8`
> claims `tests/test_fixture_parity.py` validates the fixtures. That file does
> not exist; `tests/` contains only `README.md`.

The runner command for `09-Evaluation/` lives in [[01-Test-Strategy]] and is
not repeated here. It collects **zero tests today** — `tests/` holds only
`README.md`.

## Known limits

The score is a proxy, not a measurement — [[00-Source-of-Truth-PRD|PRD]] §19.1
and §29, and [[05-Safety-Methodology]]. Report it as such in
[[02-2-Minute-Pitch]].

Two limits specific to this evaluation:

- **No accuracy claim is available in any form.** V1–V5 answer "does the
  pipeline show what it says it shows", not "how often is it right". Nothing
  here supports a percentage in the pitch.
- **FR-007 forbids presenting image-space motion as metric distance or
  calibrated speed.** V3 checks that trails *align*, never that they measure.
  Degraded input would be recorded in the evidence-quality factor, whose
  admissible inputs §19.2 enumerates. FR-010 requires an evidence-quality
  adjustment — its reference formula ends `× evidence_quality` — and §19.2
  requires low evidence quality to reduce the score or prevent scoring
  entirely. `models.py:77` `RiskFactors` has only four fields and `risk.py:139`
  applies no such multiplier, so a poor-quality sequence scores the same as a
  clean one. That defect belongs to FR-010 and §19.2 — [[01-Test-Strategy]] and
  [[04-Task-Board]] C-1 — not to §24.4, whose evidence-touching cases (jitter
  overlap, unstable track, duplicate frames, insufficient frame count) are
  already guarded by `risk.py:97-108` `_has_enough_evidence` and would pass.

## Results log

No runs yet. Record runs as [[Experiment-Log]] notes; summarise here once a
fixture exists.

| Run | Date | Sequence | V1 | V2 | V3 | V4 | V5 | Notes |
|---|---|---|---|---|---|---|---|---|

---
Related: [[00-Source-of-Truth-PRD|PRD]] §24.2 · [[05-Safety-Methodology]] · [[06-Success-Metrics]] · [[Model-Card]] · [[01-Test-Strategy]] · [[03-Agent-Evaluation]]
