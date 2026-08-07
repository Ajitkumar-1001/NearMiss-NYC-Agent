---
title: Observability
tags:
  - architecture
status: active
---

# Observability

Enough to debug under time pressure, no more.

[[00-Source-of-Truth-PRD|PRD]] §17 puts structured JSON logging in the backend
stack, and NFR-008 requires provider failures to produce structured logs plus a
user-readable fallback notice, without exposing secrets or stack traces. The
notice half exists in code; the log half does not.

## Logging

- [ ] **No logging exists in the backend today.** Nothing under
  `app/backend/nearmiss/` imports `logging`, constructs a logger, or prints.
  Wiring it up is this note's entire build item.
- [ ] One structured line per ladder rung: rung name, provider name, whether the
  runtime provider served or the fixture did, and the step-down reason. Only
  part of that exists as a value today. In `nearmiss/orchestrator.py`, `_detect`
  and `_track` return the provider `name` plus a live/fallback boolean;
  `_context` and `_explain` return only the name, so on those two rungs the
  fallback fact survives nowhere but inside the notice prose. The rung name is
  never a value at all — it is only the private method identity (`_detect`,
  `_track`, `_context`, `_explain`). And `exc.reason` is interpolated into the
  notice string inside the `except` block, after which the exception is
  discarded, so the raw reason is not retained either. Wiring the log line means
  adding the rung name and the discrete reason, not just calling a logger.
- [ ] Errors carry the input id so a failure is reproducible from fixtures.
  `Orchestrator.run()` takes `event_id` (default `"nmyc_demo_001"`) but does not
  thread it anywhere except the assembled `Event`.
- [ ] Log the `reason` field, never the caught exception.
  `nearmiss/providers/base.py` defines `ProviderUnavailable(provider, reason)`,
  which carries a short user-readable reason and nothing else — that is the
  NFR-008-safe payload. Its docstring cites NFR-005 for that rule; in v2.1.0
  NFR-005 is the reliability run-count requirement and the no-secrets/no-traces
  rule is NFR-008.

## What we need to see live during the demo

| Signal | Why | Where shown |
|---|---|---|
| Processing mode | FR-016 requires exactly one mode active and forbids presenting fallback as live inference — it is the observability surface a judge actually reads | `SourceAndModeHeader`, one of PRD §22's required judge-facing surfaces. Set in `nearmiss/orchestrator.py` and carried on `Event.processing_mode` and `NoConflictFound.processing_mode` |
| Which rung of the fallback ladder served | Know if we're on fallback | `PipelineResult.notices` in `nearmiss/orchestrator.py` — one string appended per step-down, plus one extra on the context rung when the cached fixture is also missing (`_context` appends "No historical context available." and returns `None, "none"`), so notices are not a one-to-one count of step-downs. PRD §22 also requires a "Completed with fallback" UI state. No log line yet |
| Provider readiness and version | FR-019 requires a `GET /health` payload; its fields are documented in [[05-API-Contracts]] | Not yet built. `nearmiss/models.py` defines a `Health` model with status, version, environment, and a `dependencies` list — no git revision, no configured source count — and no HTTP layer exists in `app/backend/` to serve it. Its docstring cites FR-015, which in v2.1.0 is provider fallbacks, not health |
| Pipeline stage timings | Spot the stall; NFR-006 sets the targets these would be judged against | Not yet built. Nothing in `nearmiss/` measures elapsed time |

> [!warning] The mode literal does not match FR-016
> The `ProcessingMode` literal in `nearmiss/models.py` still carries the v1
> three-value set; the FR-016 five-value set and its wire spellings are in
> [[06-Data-Model]]. Until they are reconciled the header cannot truthfully name
> the active mode, and reconciling them is a code change, not a note change.

> [!tip] Debuggability beats dashboards
> At a hackathon the win condition is "reproduce the failure from a fixture in
> under a minute". Build for that, not for graphs.

No observability dashboard, metrics backend, or tracing system is planned. The
PRD names no metrics or tracing tooling anywhere — the dashboard it does name
repeatedly (§12.1's default dashboard, FR-015's primary dashboard) is the
judge-facing product surface of §22, not an operations view.
§9's non-goals rule out production-grade streaming infrastructure, and NFR-012
requires scale-to-zero with no minimum instances, which leaves nothing running
to scrape. Structured lines on the way past are the whole budget.

The exercise that these signals have to survive is PRD §24.6's reliability test
list. Most of its rows are single-provider or single-input failures — live
source, Roboflow, Gemini, NYC Open Data, internet-after-load, corrupt upload,
unsupported format — plus the no-conflict and insufficient-temporal-evidence
outcomes. NFR-005 then demands repeated clean runs (10 local, 5 deployed) before
submission, so a failure has to be diagnosable from its log line rather than by
rerunning it.

---
Related: [[00-Source-of-Truth-PRD|PRD]] §17 · [[03-Data-Flow]] · [[05-API-Contracts]] · [[06-Data-Model]] · [[05-Demo-Reliability]] · [[07-Blocker-Log]] · [[08-Deployment]]
