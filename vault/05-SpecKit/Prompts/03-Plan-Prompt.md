---
title: Plan Prompt
tags:
  - speckit
status: active
---

# Plan Prompt

**Purpose:** Turn the frozen spec into a technical approach that closes the eligibility gate and the fixture gap before Thursday 8:00 PM.

> [!important] This is the entry point
> `/specify` and `/clarify` are complete ([[01-Specify-Prompt]],
> [[02-Clarify-Prompt]]). Start here. Output feeds [[04-Tasks-Prompt]], then
> [[05-Analyze-Prompt]], then [[06-Implement-Prompt]].

## Prompt

```text
CONTEXT

Read first, in this order:
- [[00-Source-of-Truth-PRD|PRD]] §2.2 (eligibility gate), §11.1 (readiness
  baseline + readiness rule), §27.1 (critical path), §29 (locked decisions)
- [[01-Constitution]] and [[02-Workflow]]
- [[07-Provider-Adapters]], [[05-API-Contracts]], [[06-Data-Model]],
  [[08-Deployment]]
- `app/backend/nearmiss/` — every file. It is 1,169 lines and reads quickly:
  `models.py` 221, `orchestrator.py` 284, `risk.py` 167, `config.py` 86,
  `sources.py` 55, `providers/` 348, `__init__.py` 8.

LAYOUT CHANGED 6 AUGUST — verify before trusting any path here
`app/`, `demo/`, and `tests/` moved out of `vault/` to the repository root; the
vault is notes only. Every path in this prompt is relative to the repo root.
The move is only partly staged: `demo/` and `tests/` renames are staged, `app/`
is not. Confirm the tree with `ls` before planning against it.

Governing sections: §2.2 is the only stated disqualifier. §11.1's readiness
rule sets Thursday 6 August 8:00 PM America/New_York — if the deployment
baseline or the captured evidence baseline is incomplete by then, all optional
product work stops until both are finished. §29 decisions are locked; changing
one requires the §31 protocol, not a plan.

STATE RIGHT NOW (verified against the tree, not asserted from notes)

Built — verify against the contradiction list before treating as done:
- `nearmiss/risk.py` RiskEngine. FR-010 weights 0.35/0.35/0.20/0.10 and the
  FR-011 threshold of 70.0 match the PRD. FR-009 pair filtering and the FR-005
  class list match. But FR-010's `risk = base_risk × evidence_quality`
  multiplier is never applied (contradiction 1), and `config.py:72`
  min_track_points = 8 is stricter than FR-008's three usable observations
  while track continuity is never computed at all (contradiction 5).
- `nearmiss/models.py` Pydantic v2 with extra='forbid', satisfying NFR-007 at
  the Python boundary. ProcessingMode and the Event field set contradict §20
  (contradictions 2 and 3).
- `nearmiss/orchestrator.py` — the FR-015 provider fallback ladder is
  implemented and steps down on ProviderUnavailable. (Its own docstring cites
  "§17", which is now Recommended stack — more of contradiction 8.)
- `nearmiss/config.py` — resolves FIXTURE_DIR = REPO_ROOT / "demo" / "fixtures".
- `nearmiss/providers/base.py` — three Protocols (VisionProvider,
  TrackerProvider, ContextProvider; explanation has no Protocol) plus
  ProviderUnavailable and `load_fixture`.
- The fixture rung: FixtureVision, FixtureTracker, CachedContext, and
  TemplateExplanation. These have real behaviour.

Not built — the runtime rung of every boundary is a declining stub.
`providers/vision.py:32` RoboflowVision.detect, `providers/tracking.py:21`
ByteTrackTracker.track, `providers/context.py:33` NycOpenDataContext.lookup and
`providers/explanation.py:55` GeminiExplanation.explain each raise
ProviderUnavailable("… not implemented at P0") unconditionally. Plan the real
work; do not read "adapter exists" as "adapter works".

There is no HTTP surface and no network I/O anywhere in this package. There is
local filesystem I/O — `base.py:60` opens fixture files — and env-var reads:
`orchestrator.py:71-80` pulls ROBOFLOW_API_KEY, ROBOFLOW_MODEL_ID,
NYC_OPEN_DATA_APP_TOKEN and GEMINI_API_KEY via `os.getenv`. Nothing serves this
package and nothing feeds it.

Blocking the §2.2 eligibility gate — not yet built:
- No FastAPI application exists. No tracked .py file references FastAPI,
  uvicorn, or APIRouter. `app/backend/pyproject.toml` pins fastapi>=0.115 and
  uvicorn[standard]>=0.32; nothing imports them.
- No endpoint exists, including GET /health (FR-019). `models.py` defines
  Health, DependencyStatus, and AnalysisResponse, and `orchestrator.readiness()`
  returns the four DependencyStatus rows FR-019 needs — but nothing serves any
  of it. The gap is the HTTP layer alone, not the data behind it.
- No Dockerfile exists anywhere in the repo. Nothing is deployed to Cloud Run.

The guaranteed fallback now runs — on synthetic data (§11.1 captured evidence
baseline, §29 "captured-feed evidence replay is the guaranteed conflict
demonstration"):
- `demo/fixtures/` holds detections.json, tracks.json, and context.json.
  FixtureVision, FixtureTracker, and CachedContext all load. The pipeline
  completes end-to-end: score 84.3, severity high, mode demonstration_replay,
  120 detections across 2 tracks.
- The sequence is **synthetic** — a generated car/pedestrian convergence, not
  the §11.1 "10–20 second source-attributed NYC sequence". `context.json` reads
  `source: synthetic_placeholder` and its `nearby_collision_count` is not a real
  NYC Open Data figure. Plan the real capture, or record the substitution as a
  deviation; do not read "replay runs" as "captured evidence baseline complete".

Other P0 gaps — not yet built:
- FR-001 source registry: `sources.py` exists with a `Source` model, a
  one-entry `SOURCES` list, `by_id`, and `enabled_count`. Nothing serves it.
- FR-002/FR-004 source adapter. See the interface problem below.
- FR-003 provenance and freshness — not captured and not modelled.
- FR-022 `vision-conflict-analytics` package — does not exist, not pinned.
- §22 six judge-facing surfaces. `app/frontend/` holds only README.md; zero of
  the six exist.
- `tests/` holds only README.md. There are no test files.
- No logging anywhere (NFR-008).

THE FR-002/FR-004 INTERFACE PROBLEM — plan this explicitly

`nearmiss/providers/base.py:31` declares:

    def detect(self) -> list[Detection]: ...

`VisionProvider.detect()` takes no arguments. A fetched live frame has nowhere
to go. FR-002 real-source retrieval and FR-004 sequence input cannot be added
as new code alongside the existing provider — they require changing this
signature. That is a blast-radius change: the Protocol in `base.py`, both
implementations in `providers/vision.py`, and every call site in
`orchestrator.py` move together. Treat it as its own planned step with a stated
migration order, not as a line item inside "build the source adapter".

CODE THAT CONTRADICTS THE PRD

Eight known contradictions are listed in [[05-Analyze-Prompt]]. The plan must
say, for each, whether it is fixed before Friday or recorded as a deviation.
Silently leaving one is not an option. Note that two of them
(`models.py` ProcessingMode, the §20 Event field set) interact with
extra='forbid': today the PRD's own §20 example payload fails validation
against `models.py`.

WHAT THIS PLAN MUST PRODUCE

A plan to close the §2.2 eligibility gate and the §11.1 captured evidence
baseline before Thursday 6 August 8:00 PM. Everything else is sequenced after
those two, per the §11.1 readiness rule and the §27.3 kill order.

1. Propose the component breakdown — name only what does not exist yet
2. Name the interfaces between components, including the changed
   VisionProvider signature and who moves with it
3. Identify the riskiest assumption and how to test it first
4. Call out where a §29 locked decision is being touched, and route it through
   §31 rather than deciding it here
5. State what you are deliberately not building before Friday

Constraints: follow [[01-Constitution]]. Do not invent facts — mark unknowns
as {{UPPER_SNAKE}} placeholders and list them as open questions. Distinguish
"the PRD requires", "the code does", and "not yet built" in every sentence;
never state a requirement as an accomplished fact.
```

## After the plan

Run the gstack plan reviews before decomposing into tasks. `/autoplan` runs
`/plan-ceo-review`, `/plan-design-review`, `/plan-eng-review`, and
`/plan-devex-review` sequentially with auto-decisions; run them individually
when a specific angle matters more than throughput. Verify a skill resolves
before relying on it in a time-boxed run.

---
Related: [[02-High-Level-Design]] · [[04-Component-Design]] · [[00-Source-of-Truth-PRD|PRD]] §29 · [[02-Workflow]]
