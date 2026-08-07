---
title: Component Design
tags:
  - architecture
status: active
---

# Component Design

One section per component. Keep interfaces here, implementation in `app/`.

> [!info] Three registers, kept apart
> **PRD §X requires …** is a requirement and may be unbuilt. **`nearmiss/foo.py`
> does …** was read in the source under `app/backend/nearmiss/`. **Not yet
> built** is neither. Field shapes are not restated here — [[06-Data-Model]] owns
> them, and [[05-API-Contracts]] owns the wire surface.

> [!warning] The code predates PRD v2.1.0
> Module docstrings under `app/backend/nearmiss/` cite FR numbers from an earlier
> PRD revision — `nearmiss/providers/vision.py` credits provider fallback to
> FR-011, which in [[00-Source-of-Truth-PRD|PRD]] v2.1 is the candidate threshold
> (fallbacks are FR-015). They also cite `ADR-00x` identifiers. Treat the
> docstring citations as stale and the numbers in this note as current;
> [[06-Data-Model]] records the same remapping for the shape contract.

## `nearmiss/orchestrator.py` — `Orchestrator`

- **Responsibility:** run the single pipeline and own the fallback ladder.
  [[00-Source-of-Truth-PRD|PRD]] §29 locks "one orchestrated pipeline, not a
  multi-agent council". `Orchestrator.run()` detects, tracks, scores, filters by
  threshold, then enriches and assembles one `Event` — or one `NoConflictFound`.
- **Inputs:** an `event_id` string (default `"nmyc_demo_001"` in code) and a
  `Settings` instance. Everything else it obtains from its providers.
- **Outputs:** `PipelineResult` — a dataclass carrying `event`, `no_conflict`,
  and `notices`. Exactly one of the first two is non-`None`. `notices` is the
  human-readable degradation trail, one line per rung stepped down.
- **Owns:** the ladder order; the mode decision; the severity cut
  (`_severity`, high at or above `Settings.high_severity_at`); the event-type
  choice (`_event_type` returns `vehicle_pedestrian_conflict` when either class
  is `person`, otherwise `vehicle_cyclist_conflict`); and the demo scene
  constants `FRAME_WIDTH = 1280`, `FRAME_HEIGHT = 720`, `FPS = 5.0`,
  `DEMO_LOCATION` (label only, `latitude`/`longitude` `None`).
- **Depends on:** `nearmiss/risk.py`, `nearmiss/models.py`, `nearmiss/config.py`,
  and all four provider pairs. It reads `ROBOFLOW_API_KEY`,
  `ROBOFLOW_MODEL_ID`, `NYC_OPEN_DATA_APP_TOKEN`, and `GEMINI_API_KEY` directly
  via `os.getenv` in `__init__` — those four are *not* routed through `Settings`,
  so they do not carry the `NEARMISS_` prefix the rest of the configuration uses.
- **Failure behaviour:** each rung is a `try`/`except ProviderUnavailable` that
  steps down and appends a notice. The context rung declines on absent
  coordinates — FR-013 conditions enrichment on location metadata being
  available — and then has a second level: if the cached fixture is also missing
  it catches `FileNotFoundError`, records "No historical context available." and
  continues with `None`. That second level is a local call about a missing
  fixture file, not an FR-013 requirement. No other exception is caught.

Two facts about the mode decision, both verified in `run()`. It sets
`runtime_analysis` only when the vision *and* tracker runtime providers both
served; anything else is `demonstration_replay`. And when nothing clears
`Settings.alert_threshold` it returns `NoConflictFound` rather than a
best-effort event — FR-017's "shall not manufacture an event", implemented. The
message string does not match FR-017's mandated wording: the code says "in this
clip", FR-017 requires "in the available evidence".

> [!warning] Mode vocabulary is behind the PRD
> FR-016 names five modes. `ProcessingMode` in `nearmiss/models.py` is a
> three-value `Literal`: `live_feed`, `runtime_analysis`, `demonstration_replay`.
> §20's contract JSON uses `captured_feed_replay`. The wire values do not yet
> line up with either — reconcile against [[06-Data-Model]] before the API layer
> is written, not after.

## `nearmiss/risk.py` — `RiskEngine`, `Candidate`

- **Responsibility:** turn tracks into scored candidate pairs. It is the only
  place in the codebase that produces a risk number, and it makes no
  language-model call — a nondeterministic component must not sit on the
  guaranteed path.
- **Inputs:** `list[Track]` and a `Settings`, plus frame width and height at
  construction (used only to derive `self.diagonal`).
- **Outputs:** `list[Candidate]` from `evaluate()`, sorted by score descending
  and **unfiltered** by threshold — the orchestrator applies the cut, because it
  needs the losing candidates to report `highest_score` and `pairs_evaluated`.
  `Candidate` carries `a`, `b`, `score`, `factors`, `start_seconds`,
  `end_seconds`, `closest_at`, `min_separation_px`.
- **Owns:** three scoring primitives. `_min_path_separation` is the closest
  approach of the two paths *ignoring time* — this is what separates
  `path_overlap` from `proximity`, since two road users can trace crossing paths
  minutes apart. `_closing_motion` measures the fraction of separation lost in
  the `closing_window_seconds` before closest approach, so parallel travel scores
  ~0 and something entering from off-frame does not look severe. `_normalise`
  converts pixel separation to 0–1 closeness against a fraction of the frame
  diagonal.
- **Depends on:** `nearmiss/models.py` (`Track`, `Point`, `RiskFactors`) and
  `nearmiss/config.py`. Nothing else — no I/O, no providers.
- **Failure behaviour:** `score_pair` returns `None` rather than raising, for
  both the unsupported-pair case and the insufficient-evidence case. A pair that
  fails is silently absent from the result.

FR-009 pair filtering is `_is_supported_pair`, which requires one side in
`Settings.vulnerable_classes` and the other in `Settings.vehicle_classes`.
FR-010's weighted sum is implemented and scaled to 0–100.

> [!warning] Two FR-010 / FR-008 gaps
> FR-010's formula is `risk = base_risk × evidence_quality`. `risk.py` computes
> `base_risk` only — there is no evidence-quality multiplier, and `RiskFactors`
> in `nearmiss/models.py` has no `evidence_quality` field, which §20's contract
> JSON does carry. Evidence quality is instead a **binary gate**:
> `_has_enough_evidence` drops the pair or lets it through at full weight.
>
> That gate is also not FR-008's gate. FR-008 requires an
> `insufficient_temporal_evidence` outcome; `risk.py` returns `None` and the pair
> vanishes. It checks per-track sample count and shared-window duration
> (`min_track_points`, `min_overlap_seconds`) but not track continuity or
> timestamp ordering as separate conditions. `vulnerable_user` is hard-coded to
> `1.0` for every evaluated pair — a floor on any VRU conflict, not a
> discriminator, since FR-009 already restricted the population.

## `nearmiss/config.py` — `Settings`, `RiskWeights`

- **Responsibility:** hold every tunable in one place. FR-011 requires the
  threshold to be configurable server-side.
- **Inputs:** environment variables with prefix `NEARMISS_`, via
  `pydantic_settings.BaseSettings` with `extra="ignore"`.
- **Outputs:** a module-level `settings` singleton, the default the
  `Orchestrator` uses when constructed with no argument.
- **Owns:** `alert_threshold` (70.0, matching FR-011's initial value, bounded
  0–100); `high_severity_at` (80.0); `RiskWeights` (0.35 / 0.35 / 0.20 / 0.10,
  FR-010's reference weighting, with a `total()` helper — nothing calls it, so
  the "must sum to 1.0" rule is documented but unenforced); the calibration
  knobs `proximity_scale` and `path_scale` (0.25 of the frame diagonal each) and
  `closing_window_seconds` (2.0); the evidence guards `min_track_points` (8) and
  `min_overlap_seconds` (1.0); the class sets `vulnerable_classes`
  (`person`, `bicycle`) and `vehicle_classes` (`car`, `bus`, `truck`,
  `motorcycle`); and `fixture_dir`, resolved to `demo/fixtures/` relative to the
  repo root.
- **Depends on:** `pydantic` and `pydantic-settings`. Nothing internal.
- **Failure behaviour:** an out-of-range value fails at import time via the
  Pydantic `Field` constraints, before any request is served.

Two calls recorded in the source, both of which belong in
[[05-Decision-Log]] if they change: `motorcycle` is classed as a **vehicle**,
not a vulnerable road user, on the grounds that the PRD does not say otherwise;
and `min_track_points = 8` is stricter than FR-008's "at least three usable
observations per involved track".

## `nearmiss/models.py` — the shape contract

- **Responsibility:** define every payload shape as a Pydantic model, so a
  drifting fixture fails loudly instead of quietly losing data.
- **Inputs:** JSON from fixtures, dicts from providers.
- **Outputs:** validated model instances. The full field list belongs to
  [[06-Data-Model]] and is not repeated here.
- **Owns:** the `Strict` base with `extra="forbid"`; the four `Literal` alias
  types (`EventType`, `Severity`, `ProcessingMode`, `RoadUserClass`); and the
  models `Point`, `Detection`, `Track`, `RiskFactors`, `Participant`,
  `TimeWindow`, `Location`, `HistoricalContext`, `EvidenceOverlay`,
  `ProviderMetadata`, `Event`, `DependencyStatus`, `Health`, `NoConflictFound`.
- **Depends on:** `pydantic` only. Every module that carries a payload depends
  on this one — `orchestrator.py`, `risk.py`, and all five modules under
  `nearmiss/providers/`, `base.py` included. `config.py` does not import it.
- **Failure behaviour:** `model_validate` raises `ValidationError`. Nothing
  catches it — an invalid fixture is a broken build, not a degradation.

Its docstring names `tests/test_fixture_parity.py` as the enforcement of
fixture parity. **That test does not exist**: `tests/` currently holds only
`README.md`. The parity rule is asserted, not enforced.

> [!warning] `Event` is the v1 field set
> `Event` mirrors the earlier PRD's example payload and has not been reconciled
> against §20 — [[06-Data-Model]] holds the field-level diff and is the
> authority on the target shape. FR-012's evidence package is not yet
> satisfiable from this model.

## `nearmiss/providers/base.py` — protocols and `ProviderUnavailable`

- **Responsibility:** define the adapter boundary. [[00-Source-of-Truth-PRD|PRD]]
  §29 locks the provider-adapter architecture; this file is where it is
  expressed.
- **Inputs:** none — it is definitions plus one helper.
- **Outputs:** three `@runtime_checkable` `Protocol` classes, one per provider
  family, each carrying a `name: str` and one method. [[07-Provider-Adapters]]
  tabulates the signatures; two things about them belong here.
  `VisionProvider.detect()` takes no frame argument, and explanation has no
  protocol in this file — its
  providers are duck-typed against the `Explanation` dataclass in
  `nearmiss/providers/explanation.py`.
- **Owns:** `ProviderUnavailable(provider, reason)`, the exception that *is* the
  ladder. Raising it is the normal way a runtime provider declines. It carries a
  user-readable reason and no stack trace or secret. Also `load_fixture(path)`.
- **Depends on:** `nearmiss/models.py`.
- **Failure behaviour:** `load_fixture` raises `FileNotFoundError` — deliberately
  *not* `ProviderUnavailable` — when a fixture is absent, because a missing
  fixture is a broken guaranteed path rather than a reason to degrade further.

## `nearmiss/providers/vision.py` — `RoboflowVision`, `FixtureVision`

- **Responsibility:** FR-005 detection, and the FR-015 rung "Roboflow hosted
  inference → stored detections or local inference where available". Only the
  stored-detections half is built; local inference is not.
- **Inputs:** `RoboflowVision(api_key, model_id)`; `FixtureVision(fixture_dir)`.
  `detect()` takes no arguments — there is no frame parameter yet, because
  there is no frame sampler.
- **Outputs:** `list[Detection]`.
- **Owns:** `name` — `"roboflow"` and `"fixture"` — which is what reaches the
  payload's provider metadata, so a fallback is visible in the response and not
  only in the mode badge.
- **Depends on:** `providers/base.py`, `nearmiss/models.py`. No vendor SDK is
  imported anywhere in the package.
- **Failure behaviour:** `RoboflowVision.detect()` **always raises
  `ProviderUnavailable`** — "no API key or model configured" when either the key
  or the model id is missing, otherwise "runtime detection not implemented at
  P0".
  Runtime detection is not built. `FixtureVision.detect()` reads
  `detections.json` from the fixture directory and validates every row.

## `nearmiss/providers/tracking.py` — `ByteTrackTracker`, `FixtureTracker`

- **Responsibility:** FR-006 tracking, and the FR-015 rung
  "tracker runtime → precomputed tracks".
- **Inputs:** `track(detections)`.
- **Outputs:** `list[Track]`.
- **Owns:** `name` — `"bytetrack"` and `"fixture"`.
- **Depends on:** `providers/base.py`, `nearmiss/models.py`.
- **Failure behaviour:** `ByteTrackTracker.track()` always raises
  `ProviderUnavailable("runtime tracking not implemented at P0")` — not built.
  `FixtureTracker` reads `tracks.json` and **ignores the detections it is
  handed**, on the reasoning that the fixture tracks were derived from the
  fixture detections when generated, so re-deriving them would only create a way
  for the two to disagree.

## `nearmiss/providers/context.py` — `NycOpenDataContext`, `CachedContext`

- **Responsibility:** FR-013 public-data enrichment, and the FR-015 rung
  "NYC Open Data → cached context".
- **Inputs:** `lookup(latitude, longitude)`. `NycOpenDataContext` also takes an
  app token and `radius_meters`, which the `Orchestrator` passes as `150`.
- **Outputs:** `HistoricalContext`.
- **Owns:** `name` — `"nyc_open_data"` and `"cached"`. `CachedContext`'s
  docstring requires the fixture's `source` to read `cached_nyc_open_data` so
  the UI can label it as cached — unverifiable today, since `context.json` does
  not exist. §23.11 requires captured and fixture assets to be labelled
  accurately, which is the rule that value is meant to satisfy.
- **Depends on:** `providers/base.py`, `nearmiss/models.py`.
- **Failure behaviour:** `NycOpenDataContext.lookup()` raises
  `ProviderUnavailable` — "event has no coordinates to query on" when either
  coordinate is `None` (which is the current state, since `DEMO_LOCATION` has
  none), otherwise "runtime public-data lookup not implemented at P0". Not
  built, and deliberately so while the §30 open question "Which NYC Open Data
  fields are stable?" is unresolved. `CachedContext.lookup()` reads
  `context.json`; a missing file surfaces as `FileNotFoundError` and the
  orchestrator degrades to no context at all.

**Enrichment boundary — historical context is displayed beside the risk score,
never an input to it.** `HistoricalContext` is a sibling of the score, not a
factor in it. §23 item 9 ("historical correlation is not causal proof") and item
10 (observed evidence, derived metrics, public context, and generated
explanation remain separate) are the two rules that fix this; FR-013's "shall
never be presented as evidence observed in the current frame" is the same
boundary at the presentation layer. Concretely: no context field may reach
`RiskFactors`, and `risk.py` must keep taking `Track` objects and reading no
files. The dataset behind this adapter and the modes it can run in are owned by
[[01-Datasets]] and are not restated here.

That boundary is currently broken on the display side — see the callout under
`providers/explanation.py` below. `explanation.py:98` merges the
historical-collision sentence into `observations`, the list that otherwise holds
only frame-derived evidence, which is exactly the mixing §23 item 10 forbids.
The score itself is clean: nothing in `risk.py` reads `HistoricalContext`.

## `nearmiss/providers/explanation.py` — `GeminiExplanation`, `TemplateExplanation`

- **Responsibility:** FR-014 structured explanation, and the FR-015 rung
  "Gemini → deterministic template explanation".
- **Inputs:** `explain(candidate, context, severity)`.
- **Outputs:** the `Explanation` dataclass — `observations`, `limitations`,
  `recommended_action`, `confidence`.
- **Owns:** `BASELINE_LIMITATIONS`, two unconditional entries covering the
  uncalibrated camera and the proxy-not-probability rule, appended to
  situationally. Also `name` — `"gemini"` and `"template"`.
- **Depends on:** `providers/base.py`, `nearmiss/models.py`, and
  `nearmiss/risk.py` for `Candidate`. This is the only adapter that imports the
  risk engine.
- **Failure behaviour:** `GeminiExplanation.explain()` always raises
  `ProviderUnavailable` — not built. `TemplateExplanation` cannot fail: it
  restates its input and branches on thresholds.

`TemplateExplanation` is real and is the P0 path. It states the two track ids,
class names, window length, closest image-space separation in pixels and when it
occurred; adds a path-convergence line at or above `path_overlap` 0.5 and a
stronger one at or above 0.9; adds a closing-motion line either way, branching
at `closing_motion` 0.5; appends the historical-context sentence and its
correlation-is-not-cause limitation when context exists, and a
"no historical context" limitation when it does not; and recommends human review
for high severity, optional batched review otherwise. `confidence` is a fixed
`0.6` — the code's reasoning is that a template has done no reasoning, so `1.0`
would overclaim.

A template cannot violate FR-014's non-invention clause — no identities,
measurements, legal conclusions, street-design facts, or causal claims can be
invented where there is no generative step. That is one clause, not the whole
requirement. FR-014
also requires the output to carry an outcome summary, an event classification
and a severity; the `Explanation` dataclass carries only `observations`,
`limitations`, `recommended_action`, and `confidence`, so the field list is
unmet. The Gemini path, when built, needs schema constraint to get even the
non-invention guarantee.

> [!warning] Context is mixed into the observations list
> `TemplateExplanation.explain()` appends the historical-collision sentence to
> `observations` at `explanation.py:98`, the same list that holds the
> frame-derived evidence. §23.10
> requires observed evidence, derived metrics, public context, and generated
> explanation to remain separate, and FR-013 says historical context shall never
> be presented as evidence observed in the current frame. Separating them means
> a second field, so it lands on [[06-Data-Model]] as well as here.

## Source adapter and source registry — not yet built

- **Responsibility:** FR-001 requires a server-side registry of approved sources;
  FR-002 requires fetching at least one current NYC source image through a
  provider adapter with credentials kept server-side; FR-003 requires a
  provenance and freshness record per frame; FR-004 requires accepting a live
  image and a bundled captured sequence. §16.1 lists "Source adapters" in the
  mandatory agent service.
- **Inputs:** a `source_id`, per §16.2's "Cloud Run validates source ID".
- **Outputs:** a frame plus the provenance record that §20 carries as `source`.
- **Owns:** nothing yet.
- **Depends on:** the §30 open question "Which organizer or city camera source
  is most reliable?" — unresolved, so the source is `{{SOURCE_ID}}`.
- **Failure behaviour:** FR-015 requires "live source → captured evidence
  sequence". **No source adapter exists** under `app/backend/nearmiss/`, so
  neither the live rung nor its fallback is implemented, and no provenance is
  produced. `Orchestrator` starts at detection with a hard-coded
  `DEMO_LOCATION`.

## Frame sampler — not yet built

- **Responsibility:** §16's architecture diagram places a frame sampler between
  the source adapter and the vision provider.
- **Inputs:** a clip or sampled live frames.
- **Outputs:** timestamped frames for detection.
- **Owns:** nothing yet.
- **Depends on:** the source adapter above.
- **Failure behaviour:** not built. `VisionProvider.detect()` in
  `providers/base.py` takes no frame argument, which is the signature-level
  evidence that nothing upstream of detection has been designed yet — adding a
  sampler changes that protocol.

## `vision-conflict-analytics` (pinned dependency) — not yet built

- **Responsibility:** [[00-Source-of-Truth-PRD|PRD]] §29 locks pairwise
  trajectory and conflict analysis to the public `vision-conflict-analytics`
  package, consumed through a pinned dependency; §16.1 lists that pin in the
  mandatory agent service and §16.2 puts it on the request path. The package
  boundary is specified in [[11-Vision-Conflict-Analytics-Package]].
- **Inputs:** normalized tracked detections.
- **Outputs:** candidate interacting pairs with decomposed factor scores and
  evidence sufficiency.
- **Owns:** what `nearmiss/risk.py` currently owns in-application.
- **Depends on:** a released version — `{{VCA_PINNED_VERSION}}`.
- **Failure behaviour:** not built. `app/backend/pyproject.toml` declares four
  runtime dependencies — `fastapi`, `uvicorn`, `pydantic`, `pydantic-settings` —
  plus a `dev` extra of `pytest` and `httpx`; there is no
  `vision-conflict-analytics` pin.
  `RiskEngine` is the in-app implementation the package is meant to replace, so
  the extraction is a move, not a rewrite — but until it happens the §29 lock is
  unmet.

## Temporal-evidence gate as an outcome — not yet built

- **Responsibility:** FR-008 requires the gate to produce an
  `insufficient_temporal_evidence` result, and §16.2 places it before conflict
  scoring is allowed. §20's contract carries a `temporal_evidence` block.
- **Inputs:** tracks and their observation counts, continuity, and ordering.
- **Outputs:** a third pipeline outcome alongside event and no-event.
- **Owns:** nothing yet.
- **Depends on:** `risk.py`'s existing `_has_enough_evidence` checks, which are
  the raw material.
- **Failure behaviour:** not built as an outcome, and insufficiency is currently
  *invisible* rather than merely conflated with a low score. A low-scoring pair
  still becomes a `Candidate`: `score_pair` returns it, `evaluate()` keeps it,
  and only `orchestrator.run()`'s
  `over = [c for c in candidates if c.score >= self.s.alert_threshold]` drops it
  from emission — it is still counted in `pairs_evaluated`, which
  `NoConflictFound` sets to `len(candidates)`. A pair that fails
  `_has_enough_evidence` returns `None` from `score_pair`, never enters
  `candidates`, and is therefore absent from `pairs_evaluated` altogether.
  `NoConflictFound` cannot distinguish the two because it never sees the second.
  `Event` has no `temporal_evidence` field.

## Conflict-zone gate — proposed, not in the PRD

> [!note] Proposed addition, not a requirement
> No conflict-zone polygon appears anywhere in
> [[00-Source-of-Truth-PRD|PRD]] v2.1 — §4's problem statement uses the phrase
> "conflict zone" descriptively and §17 lists `supervision` as a library with
> zone utilities, but no geometry is specified. This is a strategy proposal
> pending a recorded decision, and the routing of that decision is itself open
> (see below). Do not read it as an FR, and do not read it as adopted.

- **Responsibility:** admit a pair to scoring only when **both** participants
  occupy the marked conflict zone. It sits *before* FR-009's supported-pair
  filter, so `_is_supported_pair` sees a smaller population.
- **Inputs:** tracks, plus a per-camera image-space polygon —
  `{{CONFLICT_ZONE_POLYGON}}`, undefined until the §30 open question "Which
  exact intersection corresponds to the evidence sequence?" resolves.
- **Outputs:** a filtered track set. Pass or fail only. **No score, no factor,
  no weight.**
- **Owns:** nothing yet.
- **Depends on:** `nearmiss/risk.py`, which would call it ahead of
  `_is_supported_pair`. Nothing implements it today.

**Why it is a gate and not a scoring factor.** The obvious alternative — give
zone overlap a weight and take it out of `path_overlap` — was considered and
rejected. §19.1 defines the proxy as ranking **image-space** evidence, and the
two quantities are not interchangeable: zone occupancy says *where* two road
users were, `path_overlap` says *whether their paths converged*. Swapping one in
for the other drops the convergence signal entirely, and
`RiskEngine._min_path_separation` — the time-ignoring closest approach of the two
paths — is the only thing in the codebase that measures it. FR-010's weighting
stands unchanged: `0.35 proximity + 0.35 path_overlap + 0.20 closing_motion +
0.10 vulnerable_user`, times `evidence_quality`.

**How the decision gets routed is itself unresolved.** §1 lists "Risk-scoring
semantics" among the changes requiring an ADR and a PRD version update, and §31
carries both the change-control protocol and the post-4-August freeze that sends
implementation choices to [[05-Decision-Log]]. Which of the two covers a
pre-scoring gate is not settled here: the gate leaves FR-010's weighting
untouched, but it inserts a stage ahead of FR-009's supported-pair filter and
ahead of the §29-pinned `vision-conflict-analytics` package on §16.2's request
flow, which is a pipeline-shape change rather than a tuning call. Route it
through §31 and get the routing answered before anything is built.

## Cooldown / deduplication — proposed, not in the PRD

> [!note] Proposed addition, not a requirement
> [[00-Source-of-Truth-PRD|PRD]] v2.1 has no cooldown, dedup, or event-
> suppression concept. §24.4 covers duplicate *frames* and temporary overlap
> from detection jitter — neither is the same as suppressing repeated *events*
> from one continuing interaction. Needs a [[05-Decision-Log]] entry.

- **Responsibility:** suppress repeat emissions of the same interaction, so one
  encounter produces one event rather than one per scoring pass.
- **Inputs:** scored candidates that have already cleared
  `Settings.alert_threshold`. It sits **after** candidate scoring and **before**
  event emission, so it never changes a score.
- **Outputs:** the same candidates, minus those already emitted inside the
  window.
- **Owns:** nothing today — no state store, no timer, no module. The key would be
  `camera_id` + `vehicle_track_id` + `vru_track_id`; the window is proposed at
  roughly 5–10 seconds and is not calibrated.
- **Depends on:** `nearmiss/orchestrator.py`, which is where the threshold cut is
  applied today. Nothing implements it.
- **Failure behaviour:** not built. Single-shot fixture runs cannot exhibit the
  duplicate it prevents, so it is unexercised by the current guaranteed path.

## FastAPI service and HTTP surface — not yet built

- **Responsibility:** §16.1 makes a public FastAPI service on Google Cloud Run
  the mandatory agent service; §21 specifies the HTTP surface — seven
  endpoints, one of which (`POST /api/v1/analyze`) §21 itself marks P1. The
  contracts are owned by [[05-API-Contracts]], which tabulates all seven.
- **Inputs:** HTTP requests.
- **Outputs:** the normalized analysis record; FR-018 also requires the complete
  record as exportable JSON.
- **Owns:** nothing yet.
- **Depends on:** `Orchestrator.run()`, which is the handler body for the demo
  and analyze routes.
- **Failure behaviour:** **no FastAPI application module exists** — the tracked
  contents of `app/backend/` are `README.md`, `pyproject.toml`, and the
  `nearmiss` package, and `nearmiss/` has no app, router, or entrypoint module.
  No module under `app/backend/nearmiss/` imports `fastapi` or `uvicorn`, so
  `fastapi`
  and `uvicorn` are declared dependencies with nothing importing them.
  `models.Health` and `models.DependencyStatus` exist as shapes but no route
  serves them, and `Health` does not carry FR-019's git revision or configured
  source count.

## Fixture assets — declared, absent

- **Responsibility:** §16.1 lists "Fixture/captured-replay assets" in the
  mandatory agent service; §29 makes JSON fixtures and captured assets
  operational fallbacks. `Settings.fixture_dir` points at `demo/fixtures/`.
- **Inputs:** none.
- **Outputs:** `detections.json`, `tracks.json`, `context.json` — the three
  filenames the adapters read.
- **Owns:** the guaranteed demonstration path.
- **Depends on:** the §30 open question "Which exact intersection corresponds to
  the evidence sequence?" — unresolved, so the scene is `{{DEMO_INTERSECTION}}`
  and `EvidenceOverlay.clip_path` is `None`.
- **Failure behaviour:** **`demo/fixtures/` currently contains only
  `README.md`.** None of the three JSON files exist, so `load_fixture` raises
  `FileNotFoundError` on the first rung the orchestrator steps down to, and the
  pipeline cannot complete a run today. Every runtime provider declines and the
  fallback they decline into is missing. This is the single blocking gap in the
  backend.

## Boundaries

A component may only be reached through its stated interface. Provider calls go
through adapters, never direct SDK calls from business logic — verified: no
module under `app/backend/nearmiss/` imports a vendor SDK, and the runtime
adapters hold only credentials and identifiers.

The interface is defined in code, in `nearmiss/providers/base.py`, and
documented in [[07-Provider-Adapters]] — that note owns the protocol table and
the per-adapter status, and both notes follow the source rather than the reverse.

Three further boundaries hold in the current code:

1. `nearmiss/risk.py` makes no language-model call. Explanation reads the
   `Candidate`; the `Candidate` never depends on explanation.
2. `nearmiss/models.py` imports nothing from the package. Every module that
   carries a payload depends on it — `orchestrator.py`, `risk.py`, and all five
   modules under `nearmiss/providers/`, `base.py` included; `config.py` does not
   import it. That one-way dependency is
   what keeps the shape contract single-sourced against [[06-Data-Model]].
3. `ProviderUnavailable` is the only exception that crosses the adapter
   boundary as control flow. `FileNotFoundError` and `ValidationError` cross it
   as failures, and the orchestrator catches the former in exactly one place.

---
Related: [[02-High-Level-Design]] · [[05-API-Contracts]] · [[07-Provider-Adapters]] · [[06-Data-Model]] · [[11-Vision-Conflict-Analytics-Package]]
