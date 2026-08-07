---
title: Engineering Review
tags:
  - gstack
status: active
---

# Engineering Review

Run with `/plan-eng-review`, or as part of `/autoplan`. Findings below are the
drift audit of Tuesday 4 August, hand-verified against
`app/backend/nearmiss/`, `demo/fixtures/`, `tests/`, and `app/frontend/`.

Three registers are kept apart deliberately: what the
[[00-Source-of-Truth-PRD|PRD]] *requires*, what a named file *does*, and what is
*not yet built*.

## Checklist

- [ ] Is the critical path identified? → [[02-Time-Box-Plan]]
- [ ] Does anything block parallel work? → [[04-Task-Board]]
- [ ] Are provider failures handled at the adapter? → [[07-Provider-Adapters]]
- [ ] Does the whole thing run offline? → [[00-Source-of-Truth-PRD|PRD]] §11.1 ("Captured replay working without runtime external APIs"), re-checked at §26.1
- [ ] Are contracts agreed before implementation? → [[05-API-Contracts]]
- [ ] Is there a rollback path? → [[08-Deployment]]

## What works

1,039 lines: `models.py` 197, `orchestrator.py` 233, `risk.py` 167, `config.py`
86, `providers/` 348, `__init__.py` 8. No network I/O and no HTTP surface. The
I/O that does exist is local: `providers/base.py:48` `load_fixture` reads
committed JSON off disk, `orchestrator.py:71`–`80` reads `ROBOFLOW_API_KEY`,
`NYC_OPEN_DATA_APP_TOKEN`, and `GEMINI_API_KEY` from the environment, and
`config.py:22`–`23` resolves `REPO_ROOT` off the filesystem to set
`FIXTURE_DIR = REPO_ROOT / "demo" / "fixtures"`.

`risk.py` `RiskEngine` matches FR-010's weights exactly (0.35 / 0.35 / 0.20 /
0.10), FR-011's 70.0 threshold, FR-009 pair filtering, and FR-005's class list.
`models.py` is Pydantic v2 with `extra='forbid'`, satisfying NFR-007 at the
Python boundary. `orchestrator.py` already implements the FR-015 fallback
ladder, so that is built work — do not re-plan it.

The provider layer is half-built and should not be counted as done.
`providers/base.py` defines the three Protocols plus `ProviderUnavailable`, and
each boundary pairs a working fixture implementation with a runtime
implementation that declines unconditionally: `RoboflowVision.detect`
(`providers/vision.py:32`), `ByteTrackTracker.track` (`providers/tracking.py:21`),
and `NycOpenDataContext.lookup` (`providers/context.py:33`) all raise
`ProviderUnavailable(... "not implemented at P0")`. Only `FixtureVision`,
`FixtureTracker`, `CachedContext`, and `TemplateExplanation` have behaviour, and
`TemplateExplanation` is complete and evidence-grounded. The runtime side of
every boundary is not yet built.

## Findings

### Eligibility and fallback

| # | Finding | Severity | Action | Status |
|---|---|---|---|---|
| 1 | No FastAPI application exists. Zero tracked `.py` files reference FastAPI, uvicorn, or `APIRouter`. `pyproject.toml` pins `fastapi>=0.115` and `uvicorn[standard]>=0.32`; nothing imports them. | Blocker | Build the app module today. It is the single dependency of everything else. | open |
| 2 | No endpoint exists, including `GET /health`. `models.py` defines `Health` and `DependencyStatus`, but nothing serves them. [[00-Source-of-Truth-PRD\|PRD]] §2.2 requires HTTP 200 from `GET /health`; FR-019 specifies health and readiness. | Blocker | Wire `Health` to a route. The model already exists — this is routing, not design. | open |
| 3 | Not deployed to Cloud Run, and no Dockerfile is present in the tree. §2.2 makes deployment the only stated disqualifier. | Blocker | Dockerfile, deploy, verify from a logged-out browser, record the rollback revision ([[00-Source-of-Truth-PRD\|PRD]] §27.1 Tuesday, steps 5–7). | open |
| 4 | `demo/fixtures/` contains only `README.md`. The code reads `detections.json`, `tracks.json`, and `context.json`; `FixtureVision`, `FixtureTracker`, and `CachedContext` all raise `FileNotFoundError`. The captured-replay path cannot complete a single run today. | Blocker | Generate and commit the three fixture files. Until they exist the §11.1 captured evidence baseline is red and the guaranteed fallback is fiction. | open |

### P0 gaps — code that does not exist yet

| # | Finding | Severity | Action | Status |
|---|---|---|---|---|
| 5 | FR-001 source registry: does not exist. | Blocker | Wednesday, alongside §27.1 step 13 (validate one approved NYC source). Note that no §27.1 step explicitly covers FR-001 — the registry is unscheduled work hiding inside step 13. | open |
| 6 | FR-002 / FR-004 source adapter: does not exist, and `VisionProvider.detect()` in `providers/base.py:31` takes no arguments, so there is no signature through which a fetched live frame could be passed. This is an interface change, not just new code. | Blocker | Change the Protocol signature first, then both implementations, then add the adapter. Sequence it — it touches every vision call site. | open |
| 7 | FR-003 provenance and freshness: not captured and not modelled anywhere. §26.2 requires the live result to show source, retrieval time, freshness, provider, and mode. | Blocker | Add the fields to `models.py` at the same time as the adapter, not after. | open |
| 8 | FR-022 `vision-conflict-analytics` package: does not exist and is not pinned. §11.1 additionally requires NearMiss to consume it rather than duplicate internal scoring — today `risk.py` *is* the duplicate. | High | Ship-or-cut decision, logged in [[05-Decision-Log]]. Cutting it is survivable; drifting on it is not. | open |
| 9 | The six judge-facing surfaces of §11.3: `app/frontend/` has only `README.md`. Zero exist. | Blocker | One deliverable, six surfaces. See [[04-Design-Review]]. | open |
| 10 | `tests/` contains only `README.md`. No test files at all, so `/ship`'s test step has nothing to run and [[01-Test-Strategy]] is unexecuted. | High | Add tests with the HTTP layer. Start with `/health` and one fixture replay. | open |
| 11 | No logging anywhere in `nearmiss/`. NFR-008 covers failure visibility; a silent service on Cloud Run is undebuggable on Friday. | High | Minimal structured logging at the provider boundaries before deploy. | open |

### Code that contradicts the PRD

Fix, or record as a deliberate deviation in [[05-Decision-Log]]. Do not silently
ignore.

| # | Finding | Severity | Action | Status |
|---|---|---|---|---|
| 12 | FR-010 requires an evidence-quality multiplier. `risk.py:139` computes the weighted sum and stops; `RiskFactors` has only four fields and no `evidence_quality`. | High | Add the field and apply the multiplier, or record the deviation. | open |
| 13 | FR-016 defines five processing modes as display strings (`Live NYC snapshot` … `Demonstration fixture`); §20's example payload serialises one of them as `captured_feed_replay`. `models.py:33` defines three unrelated values — `Literal["live_feed","runtime_analysis","demonstration_replay"]`. With `extra="forbid"`, the §20 payload fails validation. | Blocker | The PRD does not state the wire encoding for the other four — settle that first, then replace the Literal. Do it before the API is written; every response shape depends on it. | open |
| 14 | §20's event contract does not match `models.py`. The model uses `event_id` rather than `analysis_id`, and has no `outcome`, no `source`, no `temporal_evidence`, and no `model` field. | Blocker | Reconcile with §20 before [[05-API-Contracts]] is implemented. A wrong contract shipped is worse than a late one. | open |
| 15 | §23 item 10 requires observed evidence, derived metrics, public context, and generated explanation to stay separate, and FR-013 closes with "Historical context shall never be presented as evidence observed in the current frame." `providers/explanation.py:98` appends historical-collision text into the `observations` list. | High | Move it to its own field. This is a responsible-AI requirement, and Data Craft + Responsibility is a judging dimension (§2.3). | open |
| 16 | FR-008's temporal-evidence gate specifies at least three usable observations. `config.py:72` sets `min_track_points: int = Field(default=8, ge=2)`, and track continuity is never computed at all. | High | Align the threshold and implement continuity, or record why 8 is the chosen operating point. | open |
| 17 | §13's taxonomy includes a low severity. `orchestrator.py:151` returns `"high" if score >= self.s.high_severity_at else "medium"` — `'low'` is unreachable. | Medium | Add the third band or narrow §13 by deviation note. | open |
| 18 | FR-017 mandates the phrase "...in the available evidence." `orchestrator.py:183` emits "...in this clip." | Low | One-line string fix. Judges read the no-event copy; "clip" implies we only ever look at video. | open |
| 19 | Module docstrings cite v1 FR numbering (`providers/vision.py:1` says FR-002/FR-011 for detection; v2.1 FR-011 is the candidate threshold), a `PRD.md §18` path that no longer exists (`__init__.py:5` — the PRD is now `02-Product/00-Source-of-Truth-PRD.md`), and ADR ids that have moved. `ADR-010` is cited four times and has no file — it was revoked, and JSON fixtures as operational fallbacks is now a §29 entry. `ADR-006` is cited in `models.py:69` meaning No Identity Recognition, but ADR-006 now denotes Real-Source-P0 ([[00-ADR-Index]] carries the warning). | Low | Sweep the docstrings once, late, in a single commit. Cosmetic but it misleads anyone reading the code cold. | open |

> [!warning] Ordering matters more than volume
> Findings 13 and 14 change `models.py`, which every route and every fixture
> depends on. Finding 6 changes a Protocol signature. Do those before writing
> the HTTP layer, or write the HTTP layer twice.

---
Related: [[01-Workflow]] · [[02-High-Level-Design]] · [[06-Risk-Register]] · [[05-API-Contracts]]
