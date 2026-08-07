---
title: Tasks Prompt
tags:
  - speckit
status: active
---

# Tasks Prompt

**Purpose:** Decompose the plan into independently completable tasks, ordered by the Thursday 8:00 PM readiness gate.

## Prompt

```text
CONTEXT

Input: the plan produced by [[03-Plan-Prompt]] and reviewed through the gstack
plan reviews.

Read first:
- [[00-Source-of-Truth-PRD|PRD]] §11.1 (the baseline item lists), §27.1 (the
  critical path), §26.1 (arrival gate checkboxes)
- [[02-Time-Box-Plan]], [[04-Task-Board]], [[08-Definition-of-Done]]

ORDERING RULE — non-negotiable

Order every task by the §11.1 readiness gate: Thursday 6 August, 8:00 PM
America/New_York. §11.1's readiness rule stops all optional product work if the
deployment baseline or the captured evidence baseline is incomplete at that
moment, so those two baselines come first and nothing may be scheduled ahead of
them. §27.1 already sequences the critical path across Tuesday, Wednesday, and
Thursday and gives the Thursday 8:00 PM readiness decision — mirror that
sequence, do not invent a different one. Today is Thursday 6 August: the
Tuesday and Wednesday legs of §27.1 did not happen, so treat their unfinished
items as due tonight, not as sequenced ahead. The readiness gate is hours away,
the event is Friday 7 August, 4:00–10:00 PM ET, and submission locks at 8:30 PM.

Derive one task per bullet in §11.1's five baseline lists — Deployment,
Captured evidence, Reusable conflict-analytics, Real-source, Submission —
reading each bullet from the PRD, not from this prompt. Do not work from a
summary; a dropped bullet is a dropped task. Then cross-check the resulting set
against the §26.1 arrival-gate checkboxes: every checkbox must map to at least
one task.

DONE CONDITIONS — the part that usually gets faked

Every task states its done condition as a command that can actually be run, plus
the output that counts as passing. Not "health endpoint works" — a curl of the
deployed URL and the HTTP status expected. Not "fixtures committed" — the
command that loads them through FixtureVision, FixtureTracker, and
CachedContext and completes without FileNotFoundError. Not "tests added" — the
pytest invocation and the count expected. `tests/` currently holds only
README.md, so the first test task is also the task that makes any later "tests
pass" claim meaningful.

If a task's done condition cannot be expressed as a runnable command, split the
task until it can, or mark it explicitly as a manual verification with the exact
steps and the observable result.

1. One task = one verifiable outcome
2. Mark dependencies explicitly — including the VisionProvider.detect()
   signature change, which blocks every FR-002/FR-004 task behind it
3. Flag which tasks can run in parallel
4. Estimate in hours against [[02-Time-Box-Plan]], and against the hours
   actually remaining before Thursday 8:00 PM
5. Every task states its done condition as a runnable command and its expected
   output

Constraints: follow [[01-Constitution]]. Do not invent facts — mark unknowns
as {{UPPER_SNAKE}} placeholders and list them as open questions. Anything not
required by §11.1 or §26.1 before Friday is P1 and goes below the line, in the
§27.3 kill order.
```

---
Related: [[04-Task-Board]] · [[02-Time-Box-Plan]] · [[08-Definition-of-Done]] · [[02-Workflow]]
