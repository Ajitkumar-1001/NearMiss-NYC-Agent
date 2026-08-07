---
title: Test Strategy
tags:
  - evaluation
status: active
---

# Test Strategy

Minimum testing that keeps the demo safe. Not comprehensive coverage — there
isn't time, and that's a deliberate trade.

This note is the frame for the other four in `09-Evaluation/`. It owns the
runner, the exclusions, and the map from rubric row to owning note. It owns no
cases of its own.

> [!warning] Nothing has been run yet
> `tests/` contains only `README.md` — zero test files. Every "Verified" box and
> every results row across this folder is empty because it is, not because
> nobody filled it in. Do not put a number in one without a run behind it.

## What we test

| Layer | What | Why | Runnable today? |
|---|---|---|---|
| Risk engine | Hand-built `Track` pairs in → `Candidate` out | `nearmiss/risk.py` is implemented; needs no fixture | Yes |
| Explanation | `Candidate` + context in → `Explanation` out | `providers/explanation.py` is implemented | Yes |
| Pipeline stages | Fixture in → expected out | Regressions here kill the demo | No — `demo/fixtures/` has only `README.md` |
| Adapters | Fixture fallback fires on failure | [[00-Source-of-Truth-PRD\|PRD]] §29 locks JSON fixtures as the operational fallback | Partly — the explanation rung falls back today; the detection and tracking rungs read `demo/fixtures/` files that do not exist |
| API | Contract shape matches [[05-API-Contracts]] | Frontend/backend drift | No — no FastAPI app exists |
| Demo path | Full end-to-end, network off | The thing judges see | No — needs fixtures and the service |

## Rubric coverage

[[00-Source-of-Truth-PRD\|PRD]] §24.1 maps each judging dimension to one test.
This is who owns each row.

| Rubric row | PRD evaluation subsection | Owning note |
|---|---|---|
| Working Demo | §24.6 + NFR-005 run counts | [[05-Demo-Reliability]] |
| NYC Relevance | §24.3 live-source | [[02-Test-Cases]] |
| Usefulness | §24.5 explanation | [[03-Agent-Evaluation]] |
| Technical Execution | §24.2 perception \| §24.4 risk engine | [[04-Vision-Evaluation]] \| [[02-Test-Cases]] |
| Data Responsibility | §23 obligations, surfaced \| §24.5 limitation criteria | [[02-Test-Cases]] \| [[03-Agent-Evaluation]] |
| Open Source | no §24 subsection — checked against §26.1/§26.2 directly | none; verify against the PRD gate lists |

Nothing in `09-Evaluation/` restates the §26 gates. Check them in the PRD —
[[08-Definition-of-Done]] carries a merged list that drops items, including
"Golden demo succeeds three consecutive times from the deployed URL."

## What is testable today

Two surfaces are fully implemented and take in-memory objects, so they need no
fixture file and no running service:

- **`nearmiss/risk.py` → `RiskEngine`** (`score_pair`, `evaluate`,
  `_closing_motion`, `_min_path_separation`). All eight §24.4 cases can be
  written now against hand-built `Track` objects — including duplicate frames
  and insufficient frame count, which `_has_enough_evidence` (`risk.py:97–108`)
  decides from `min_track_points` (`config.py:72`), `min_overlap_seconds`
  (`config.py:73`), and the `len(paired) < 2` guard, with `_paired_by_time`
  collapsing duplicate `frame_number` samples in memory. No file is read.
  Highest-value testable surface that exists.
- **`providers/explanation.py` → `TemplateExplanation`.** Takes a `Candidate`,
  an optional `HistoricalContext`, and a `Severity` — no fixture, no service —
  so all five §24.5 criteria are checkable now.

One §24.6 row also runs today: **"Gemini unavailable."** `orchestrator.py:129–146`
`_explain` catches `ProviderUnavailable` from `GeminiExplanation` and returns
`TemplateExplanation` output from an in-memory `Candidate`.

Two assertions will fail on first run, and that is the point of writing them:

- **Evidence-quality multiplier** — FR-010's reference formula ends
  `risk = base_risk × evidence_quality`, and §19.2 makes low evidence quality
  reduce the score or prevent scoring. Any test asserting the score is
  multiplied by an evidence-quality term fails: `risk.py:139` computes the
  weighted sum and stops, and `RiskFactors` has only four fields. Note this is
  not one of §24.4's eight cases — the four that touch evidence (jitter,
  missing/unstable track, duplicate frames, insufficient frame count) are
  already guarded by `RiskEngine._has_enough_evidence` (`risk.py:97–108`) and
  should pass.
- **§23.10 separation** — "Observed evidence, derived metrics, public context,
  and generated explanation remain separate." `explanation.py:98` appends
  historical-collision text into the `observations` list. The text itself comes
  from the `context` argument passed into `explain` (`explanation.py:66`), so
  §24.5's "reference supplied evidence only" is satisfied; the defect is the
  merge, not the source. Expected failure.

Note when writing assertions: the FR-010 weights and FR-011 threshold live in
`config.py:29–32` (0.35 / 0.35 / 0.20 / 0.10) and `config.py:49`
(`alert_threshold` 70.0), not in `risk.py`. The code's own comments label these
FR-006 and FR-007, which are Tracking and Trajectory representation in the PRD.

## What is blocked

| Blocked by | Tests it holds up |
|---|---|
| `demo/fixtures/` holds only `README.md`, while `FixtureVision.__init__` (`vision.py:43`) points at `demo/fixtures/detections.json` — so `Orchestrator._detect` (`orchestrator.py:85–90`) raises on the **fallback** rung, not the primary | §24.2 all, the captured-replay path, and every §24.6 outage row that runs through `_detect` — "Gemini unavailable" is the exception and runs today |
| No FastAPI app anywhere | §24.3 all, every contract test, and the deployment items in §26.1–§26.2: `GET /health` returns 200, service binds `0.0.0.0:$PORT`, public URL from a logged-out browser, analysis through the deployed service, golden demo three times from the deployed URL |
| `Event` (`models.py:147–169`) has no `outcome`, `source`, or `temporal_evidence` field, which §20's core data contract specifies as top-level keys and §13 enumerates the outcome states for | §24.3's `insufficient_temporal_evidence` expectation has nowhere to land |

The runtime providers raising `ProviderUnavailable` unconditionally
(`providers/vision.py:32`, `tracking.py:21`, `context.py:33`) is not a blocker —
that unconditional raise **is** the outage §24.6 asks for, and it is free. What
blocks those rows is the rung below it having no file to fall back to.

`models.py:8` cites `tests/test_fixture_parity.py` as enforcing fixture parity.
That file does not exist, and neither do the fixtures. Treat the docstring as a
stale claim, not evidence.

## What we don't test

- Exhaustive unit coverage
- Load / performance beyond the demo's needs
- Precision/recall against labelled ground truth. §24.2 asks for qualitative
  checks, not accuracy metrics: there is no labelled data, and §9 rules out
  calculating scientifically validated time-to-collision from an uncalibrated
  camera — which is what a defensible metric claim would require. Any accuracy
  number in this folder is a fabrication.

## Running

This is the one runner command for `09-Evaluation/`. Other notes in the folder
link here rather than carrying their own copy.

pytest is already configured. `app/backend/pyproject.toml` sets
`testpaths = ["../../tests"]` (`pyproject.toml:23–24`), and the `dev` extra pins
`pytest>=8.3` and `httpx>=0.27` (`pyproject.toml:14`). From `app/backend/`:

```bash
pytest
```

This collects **zero tests today** — `tests/` holds only `README.md`. The
runner is not the blocker; the absence of test files is.

Determinism here comes from fixed fixture inputs, not from seeding. There is no
stochastic component to seed: `RiskEngine` is pure arithmetic and
`TemplateExplanation` is deterministic.

---
Related: [[02-Test-Cases]] · [[05-Demo-Reliability]] · [[08-Definition-of-Done]] · [[05-API-Contracts]]
