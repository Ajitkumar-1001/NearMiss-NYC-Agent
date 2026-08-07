---
title: Analyze Prompt
tags:
  - speckit
status: active
---

# Analyze Prompt

**Purpose:** Adversarial review of the plan and tasks before writing code — find what they still miss.

## Prompt

```text
CONTEXT

Input: the plan from [[03-Plan-Prompt]] and the task list from
[[04-Tasks-Prompt]].

Read first: [[06-Risk-Register]], [[05-Demo-Reliability]], [[03-Scope-Ladder]],
[[00-Source-of-Truth-PRD|PRD]] §11.1 readiness rule, §27.3 kill order, §28
major risks.

The risks below are already known and verified. Do not spend the run
rediscovering them — assume them, check the plan covers each one, and then go
find what the plan still misses.

KNOWN RISK 1 — the eligibility gate has no code behind it
§2.2 is the only stated disqualifier. Read its five conditions there; missing
any one means the submission is not hackathon-complete even if everything runs
locally. Nothing in the repo satisfies any of them: no FastAPI application
exists, no endpoint exists, no Dockerfile exists. `pyproject.toml` pins fastapi
and uvicorn; nothing imports either. `models.py` defines Health and
DependencyStatus, but nothing serves them. Nothing is deployed.

KNOWN RISK 2 — the guaranteed fallback runs, but on synthetic data
§29 locks captured-feed evidence replay as the guaranteed conflict
demonstration and fallback. `demo/fixtures/` now holds detections.json,
tracks.json, and context.json, and the pipeline completes on them: 84.3, high,
demonstration_replay. The FileNotFoundError risk is closed.

What replaced it: the sequence is synthetic, not the §11.1 "10–20 second
source-attributed NYC sequence", and context.json reads
`source: synthetic_placeholder` with a `nearby_collision_count` that is not a
real NYC Open Data figure. §11.1's captured-evidence baseline is therefore
runnable but unsatisfied. Check whether the plan schedules the real capture or
records the substitution as a deviation — and whether anything downstream
claims NYC attribution the fixture cannot support.

KNOWN RISK 3 — eight code-vs-PRD contradictions
1. FR-010 / §19.2 — `risk.py:139` computes the weighted sum and stops. The
   evidence_quality multiplier is never applied, and RiskFactors in `models.py`
   has only four fields with no evidence_quality.
2. FR-016 / §20 — `models.py:33` declares
   ProcessingMode = Literal["live_feed","runtime_analysis",
   "demonstration_replay"], three v1 values. The PRD requires five, none of
   which match. Because models use extra='forbid', the PRD's own §20 example
   payload fails validation against the current models.
3. §20 — Event uses `event_id`, not `analysis_id`, and has no outcome, source,
   temporal_evidence, or model fields.
4. §23.10 — `explanation.py:98` appends historical-collision text into the
   observations list. §23.10 requires observed evidence, derived metrics,
   public context, and generated explanation to remain separate.
5. FR-008 — `config.py:72` sets min_track_points = 8; the PRD gate specifies at
   least three usable observations. Track continuity is never computed at all.
6. §13 — `orchestrator.py:151` returns only 'high' or 'medium'; 'low' is
   unreachable.
7. FR-017 — the orchestrator emits "...in this clip." where the PRD mandates
   "...in the available evidence."
8. Module docstrings cite v1 numbering and one retired ADR id. `config.py:3`
   attributes the configurable threshold to FR-007, which is now Trajectory
   representation — the threshold is FR-011. `models.py:3` says it mirrors
   §18, which is now the data-source policy — the data contract is §20.
   ADR-010 is cited by `models.py:9`, `base.py:52`, `base.py:57` and
   `context.py:17` but does not exist: `07-Decisions/` holds ADR-001–ADR-007
   plus 00-ADR-Index.md, and 008–010 are retired. `models.py:69` cites ADR-006
   for a no-identity-recognition rule; since v2.1 ADR-006 is the P0-sequencing
   decision and that rule lives in §29.

YOUR JOB

Assume all of the above. Answer these against the plan and task list:

1. Where does this plan fail under time pressure? Check it against the §11.1
   Thursday 6 August 8:00 PM readiness rule specifically, not against Friday.
2. Which task is on the critical path and what happens if it slips? Compare
   against §27.1 — if the plan's critical path differs from the PRD's, say
   which is wrong.
3. What breaks if a provider is down mid-demo? The fallback is Known Risk 2;
   trace what actually happens today, not what the design intends.
4. Which assumption, if wrong, invalidates the most work?
5. What is missing that no task covers? Check at minimum: FR-001 source
   registry, FR-003 provenance and freshness, FR-022 package, the §22 six
   surfaces (`app/frontend/` has only README.md), the empty `tests/`, absent
   logging under NFR-008, and each of the eight contradictions above — does a
   task fix it, or is it recorded as a deviation?

Constraints: follow [[01-Constitution]]. Do not invent facts — mark unknowns
as {{UPPER_SNAKE}} placeholders and list them as open questions. Report only
what you can point at in a file or a PRD section. This is a report-only stage:
propose no fixes here, and change no code.
```

---
Related: [[06-Risk-Register]] · [[05-Demo-Reliability]] · [[03-Scope-Ladder]] · [[02-Workflow]]
