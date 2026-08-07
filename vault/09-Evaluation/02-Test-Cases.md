---
title: Test Cases
tags:
  - evaluation
status: active
---

# Test Cases

The concrete case list behind [[01-Test-Strategy]]. [[00-Source-of-Truth-PRD|PRD]]
§24 names the cases; this note adds the input, the expected result, whether it
can run today, and what it will catch.

> [!warning] Nothing here has ever been run
> `tests/` contains only `README.md` — zero test files, so every **Status** below
> is `todo`. Do not mark a row done without a passing test file behind it. The
> runner is already configured and belongs to [[01-Test-Strategy]]; it collects
> nothing today.

## How to read the Automated? column

| Value | Meaning |
|---|---|
| `unit` | Runnable **today** with hand-built objects. No fixtures, no service. |
| `blocked: fixtures` | `demo/fixtures/` holds only `README.md`; `FixtureVision` / `FixtureTracker` / `CachedContext` read `detections.json` / `tracks.json` / `context.json` and raise `FileNotFoundError`. |
| `blocked: no service` | No FastAPI application exists in the repo — no tracked `.py` file imports FastAPI, uvicorn, or `APIRouter`, and there is no Dockerfile. `pyproject.toml` pins both dependencies anyway. |
| `blocked: no source` | No source registry or source adapter exists, and `VisionProvider.detect()` in `providers/base.py:31` takes no arguments — a retrieved frame has nowhere to go. |
| `blocked: no UI` | `app/frontend/` holds only `README.md`; none of §22's six judge-facing surfaces exist. |

Cases marked **FAILS TODAY** are expected to fail against current code. That is
the point of writing them — they are the divergences evaluation should catch, not
tests to soften.

## A. Risk engine — PRD §24.4

Eight cases. All eight are runnable now: `risk.py:85` `RiskEngine` is fully
implemented and takes `Track` objects, so cases are built in memory. Thresholds
and weights come from `config.py`, not `risk.py` — `alert_threshold` 70.0
(`config.py:49`), weights 0.35 / 0.35 / 0.20 / 0.10 (`config.py:29-32`),
`min_track_points` 8 and `min_overlap_seconds` 1.0 (`config.py:72-73`).

| # | Case | Input | Expected | Automated? | Status |
|---|---|---|---|---|---|
| 1 | Converging vehicle–cyclist paths | Two `Track`s, `car` + `bicycle`, ≥8 centroid points each, ≥1.0 s of shared `frame_number`s, separation collapsing before closest approach | `score_pair` returns a `Candidate`; `closing_motion > 0`; score clears `alert_threshold`. Assert the threshold from settings, never a hardcoded score | `unit` | todo |
| 2 | Converging vehicle–pedestrian paths | Same geometry, `car` + `person` | `Candidate` returned; `orchestrator._event_type` maps to `vehicle_pedestrian_conflict` | `unit` | todo |
| 3 | Parallel movement without convergence | Two tracks holding constant separation across the window | `closing_motion == 0.0` (`risk.py:65` returns 0 when separation never collapses); pair must not clear threshold at realistic separation | `unit` | todo |
| 4 | Stationary pedestrian near a vehicle | `person` with identical x/y across ≥8 frames, `car` parked close by | PRD intent: no alert. **FAILS TODAY** — `closing_motion` is the only factor a static pair drives to 0; the other three weights still total 0.80 (`config.py:29-32`), so a close enough static pair can still clear `alert_threshold` (`config.py:49`). Assert `closing_motion == 0.0` and compare against the configured threshold — never write an expected score | `unit` | todo |
| 5 | Temporary overlap from detection jitter | Two tracks that touch for one or two frames, `<1.0 s` shared span | `score_pair` returns `None` via `_has_enough_evidence` (`risk.py:97`) | `unit` | todo |
| 6 | Missing or unstable track | One track with <8 points, or two tracks sharing no `frame_number` | `score_pair` returns `None` | `unit` | todo |
| 7 | Duplicate frames | A track whose `centroid_history` repeats the same `frame_number` / `timestamp` | `score_pair` returns `None`: `_paired_by_time` (`risk.py:39`) keys the second track by `frame_number`, so repeats collapse there, and a repeated-timestamp window fails the `min_overlap_seconds` span check in `_has_enough_evidence`. Note for the test writer: `min_track_points` counts `len(centroid_history)` raw, so duplicates do count toward it. Hash-level duplicate detection is §24.3's concern — case 27 | `unit` | todo |
| 8 | Insufficient frame count | Tracks with 3–7 centroid points | `score_pair` returns `None`. **Divergence to resolve, not a code bug:** FR-008's gate is *three* usable observations per track; `config.py:72` requires 8. Pick one and log it in [[05-Decision-Log]] | `unit` | todo |

> [!note] Stale citation
> `risk.py:98` attributes cases 5 and 6 to "PRD §22.2". §22 is user-interface
> requirements; the case list is §24.4. Harmless, but correct it when the file
> is next touched.

## B. Explanation — PRD §24.5

`providers/explanation.py:60` `TemplateExplanation` is fully implemented and
needs no fixture file. All five criteria are testable today against a hand-built
`Candidate`.

| # | Case | Input | Expected | Automated? | Status |
|---|---|---|---|---|---|
| 9 | References supplied evidence only | `Candidate` + a `HistoricalContext` | The §24.5 criterion itself holds: the historical-collision sentence is built from the `context` argument handed to `TemplateExplanation.explain` (`explanation.py:65`), so it *is* supplied evidence. The unmet requirement is PRD §23 item 10 — "Observed evidence, derived metrics, public context, and generated explanation remain separate." **FAILS TODAY** — `explanation.py:98` appends that sentence into `observations` | `unit` | todo |
| 10 | Avoids identity, legal, and metric claims | Any `Candidate` | No real-world unit describing the conflict itself (image-space `px` only); no legal or enforcement wording; only `track_id`, never an identity. Scope the assertion: the public-context radius in metres (`explanation.py:100`) is a supplied `HistoricalContext` field, not an invented measurement, so a blanket "no `m` anywhere" assertion fails on the context branch | `unit` | todo |
| 11 | Includes at least one limitation | `Candidate`, context present and absent | `limitations` never empty — `BASELINE_LIMITATIONS` supplies two unconditionally, plus one situational | `unit` | todo |
| 12 | Recommends human review when appropriate | `severity="high"` and `severity="medium"` | `explanation.py:113` returns the review action for `high` only, satisfying §23 item 8. Note `low` is unreachable: `orchestrator._severity` returns only `high` or `medium` | `unit` | todo |
| 13 | Produces valid schema-constrained output | Template output assembled into an `Event` | `Explanation` is a frozen dataclass, not a Pydantic model — the schema constraint only binds when `models.Event` validates it. Test must build the `Event`, not just the dataclass | `unit` | todo |

## C. Reliability — PRD §24.6

Eleven scenarios. The three cases previously seeded in this note fold in here:
old case 1 into #19, old case 2 into #16–#18, old case 3 into #22.

| # | Case | Input | Expected | Automated? | Status |
|---|---|---|---|---|---|
| 14 | All providers available | Real Roboflow + ByteTrack + NYC Open Data | Cannot be exercised: all three runtime providers are declining stubs that raise `ProviderUnavailable` (`providers/vision.py:32`, `tracking.py:21`, `context.py:33`) | `blocked: no service` | todo |
| 15 | Live source unavailable | Configured source returns an error | §12.4 allows "source unavailable with a clearly labeled fallback" as a valid outcome. Nothing to fail — no source adapter exists | `blocked: no source` | todo |
| 16 | Roboflow unavailable | No `ROBOFLOW_API_KEY` | `orchestrator._detect` catches `ProviderUnavailable`, appends a **visible** notice, and steps to `FixtureVision`. The stub's unconditional raise *is* the trigger and costs nothing; what blocks the case is the rung below — `FixtureVision.__init__` (`vision.py:43`) points at `demo/fixtures/detections.json` and that directory holds only `README.md`, so `_detect` raises on the fallback. Old seeded case 2 said "silent fixture fallback"; that is wrong twice over — FR-016 and §26.2 both require every fallback to be labeled | `blocked: fixtures` | todo |
| 17 | Gemini unavailable | No `GEMINI_API_KEY`, hand-built `Candidate` | `orchestrator._explain` appends a notice and returns `TemplateExplanation` output. Needs no fixture — call `_explain` directly | `unit` | todo |
| 18 | NYC Open Data unavailable | No app token, no `context.json` | `orchestrator._context` steps runtime → cached → `FileNotFoundError` caught at `orchestrator.py:123` → returns `(None, "none")` plus two notices. Runnable **because** the fixture is missing | `unit` | todo |
| 19 | Internet unavailable after initial load | Deployed URL loaded, then network disabled; replay invoked | Full replay result renders from committed fixtures with no external call. Needs both the deployed service and the fixture set | `blocked: no service` | todo |
| 20 | Corrupt upload | Truncated or non-decodable file | §22 required state `Failed input`; no crash, no fabricated event. No upload endpoint exists (uploaded MP4 is P1 per PRD §14) | `blocked: no service` | todo |
| 21 | Unsupported format | File of a type the pipeline does not accept | Rejected with the `Failed input` state before perception runs | `blocked: no service` | todo |
| 22 | No candidate conflict | Tracks that score below `alert_threshold`; also the empty-track case | Engine level: `evaluate([])` returns `[]` — runnable now. Pipeline level: `run()` returns `NoConflictFound` with `pairs_evaluated` and `highest_score` and no `Event`, which needs fixtures | `unit` (engine) / `blocked: fixtures` (pipeline) | todo |
| 23 | Insufficient temporal evidence | A single frame, or tracks under the FR-008 gate | §13 lists `insufficient_temporal_evidence` among the outcome states and §20's contract carries `outcome`, `source`, and `temporal_evidence` as top-level keys. **FAILS TODAY** — `models.Event` (`models.py:147`) has none of the three, and `NoConflictFound` only expresses "nothing crossed threshold". The state is not representable, so it is indistinguishable from #22 | `unit` | todo |
| 24 | Public Cloud Run access from logged-out browser | Deployed URL in a private window | HTTP 200, dashboard renders, `GET /health` returns 200 — §26.1's arrival gate. No application and no Dockerfile exist to deploy | `blocked: no service` | todo |

## D. Live source — PRD §24.3

All five blocked. Recorded so the gap is visible, not to imply they are close.

| # | Case | Input | Expected | Automated? | Status |
|---|---|---|---|---|---|
| 25 | Source fetch succeeds three consecutive times | Configured NYC source | Three successful retrievals, each with its own timestamp | `blocked: no source` | todo |
| 26 | Retrieval timestamp changes when content changes | Two fetches spanning a source update | Timestamps differ. **No field to assert against** — the only `retrieved_at` in `models.py` belongs to `HistoricalContext`, not to the frame or the report | `blocked: no source` | todo |
| 27 | Duplicate frames detected by hash | Two fetches returning identical bytes | Second is recognised as a duplicate. No hashing exists in `nearmiss/` — see case 7 | `blocked: no source` | todo |
| 28 | Source outage triggers a visible fallback | Source errors mid-run | Fallback labeled in the UI, not only in `notices` | `blocked: no UI` | todo |
| 29 | Single-frame input returns `insufficient_temporal_evidence` | One frame | Engine level: a one-point `Track` fails `_has_enough_evidence`, so `score_pair` returns `None` — runnable now. Report level: **FAILS TODAY** for the same reason as #23 — §20 and §13 define the `outcome` state, `models.Event` has no field to land it in. Fetch path needs a source adapter | `unit` (engine) / `blocked: no source` (fetch) | todo |

## E. Vision — PRD §24.2

| # | Case | Input | Expected | Automated? | Status |
|---|---|---|---|---|---|
| 30 | Required classes detected in key frames | Selected evidence sequence | Expected classes present in the key frames | `blocked: fixtures` | todo |
| 31 | Track identities stable through the conflict window | Same sequence | `track_id` does not switch across the window | `blocked: fixtures` | todo |
| 32 | Trajectory trails align with objects | Same sequence | Trails render on the objects they belong to | `blocked: no UI` | todo |
| 33 | Representative frame clearly shows the event | Assembled `Event` | A frame reference is present. `orchestrator.py:216` sets `representative_frame=None` unconditionally | `blocked: fixtures` | todo |
| 34 | Stored and runtime outputs use the same normalized schema | Committed fixtures + runtime output | Both validate against `models.py`. `models.py:8` cites `tests/test_fixture_parity.py` as the enforcement — **that file does not exist**, and neither do the fixtures it would validate | `blocked: fixtures` | todo |

## Results

No runs yet. Nothing in this note has been executed.

| Date | Cases run | Passed | Failed | Notes |
|---|---|---|---|---|
| | | | | |

## Edge cases to cover

- [ ] Malformed fixture — `models.py` uses `extra="forbid"`, a local design choice
      rather than an NFR-007 requirement. One consequence is worth a test: the
      PRD's own §20 example payload fails validation against these models.
- [ ] Very short / very long input — short is case 8; long is untested and
      unbounded.
- [ ] Weights that do not sum to 1.0 — `RiskWeights.total()` exists but nothing
      calls it.
- [ ] Track continuity — FR-008 requires it; nothing computes it.
- [ ] `ProcessingMode` coverage — `models.py:33` defines three values
      (`live_feed`, `runtime_analysis`, `demonstration_replay`); FR-016 lists
      five, none matching, and §20's example payload uses a sixth spelling,
      `captured_feed_replay`. Cases asserting mode strings will need rewriting
      once that is settled.

## Priority before the readiness gate

The §11.1 readiness decision is **Thursday 6 August, 8:00 PM America/New_York**,
governed by PRD §27.1 — not §27.3, which is the event-day kill order.

1. Cases 1–8 and 9–13 (`unit`) — the only real coverage obtainable without
   fixtures or a service, and they cover the scoring surface the demo rests on.
2. Cases 17, 18, 22, and the engine half of 29 (`unit`) — fallback and
   insufficient-evidence behaviour, testable today.
3. Everything else waits on a specific missing piece, not one blanket blocker:
   cases 30, 31, 33, 34 and the pipeline half of 22 need fixtures; 15, 25–27 and
   the fetch half of 29 need a source adapter; 28 and 32 need the frontend; 14,
   19–21 and 24 need a deployed service. Gate checks live in PRD §26.1 and
   §26.2 — see [[01-Test-Strategy]].

---
Related: [[01-Test-Strategy]] · [[04-MVP-Scope]] · [[08-Definition-of-Done]] · [[05-QA-Checklist]] · [[05-Demo-Reliability]]
