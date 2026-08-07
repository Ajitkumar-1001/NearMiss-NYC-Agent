---
title: Implement Prompt
tags:
  - speckit
status: active
---

# Implement Prompt

**Purpose:** Execute one task, verify it, and stop.

## Prompt

```text
CONTEXT

Input: one task from [[04-Task-Board]], selected by the [[04-Tasks-Prompt]]
ordering. One. Not a phase, not a baseline — one task with one runnable done
condition.

Read first: [[08-Definition-of-Done]], [[02-Test-Cases]], and
[[00-Source-of-Truth-PRD|PRD]] §26.1 for the arrival-gate checkbox this task
turns green. Read the files you are about to change before changing them.

EVIDENCE RULE

As of now `app/backend/nearmiss/` has no FastAPI application and `tests/` holds
only README.md — so there is no passing suite standing behind any claim you
make, and nothing about this repo can be confirmed by reading its layout.
`demo/fixtures/` does now hold the three JSON files and the replay does
complete, but that is the *only* verified thing here and it was verified by
running it. Every claim of completion must be backed by the actual output of a
command, pasted verbatim. Not a description of the output.
Not "verified". Not a summary. If you did not run the command, the task is not
done, and saying it is done is the worst failure mode available here.

TWO CONSTRAINTS SPECIFIC TO THIS CODEBASE

1. Deterministic replay runs with the network OFF. §11.1's captured evidence
   baseline requires "captured replay working without runtime external APIs".
   Verify it with networking disabled, not merely with the live provider
   unselected. A replay that silently reaches a network is not the fallback the
   §29 locked decision guarantees.
2. Fixtures must match `nearmiss/models.py` shapes exactly. The models are
   Pydantic v2 with extra='forbid' (NFR-007), so any extra key, renamed field,
   or drifted enum value is rejected at load time rather than tolerated. When
   writing detections.json, tracks.json, or context.json, read the model
   definition first and match it field for field.

1. Make the smallest change that satisfies the task
2. Do not refactor adjacent code. The one deliberate exception is the
   VisionProvider.detect() signature change, if that is your task — it moves
   `providers/base.py`, both implementations in `providers/vision.py`, and the
   `orchestrator.py` call sites together, because it cannot be done in pieces
3. Add or update the test case in [[02-Test-Cases]] and the corresponding file
   under `tests/`
4. Run the verification and paste the actual output — command, exit status, and
   what it printed
5. Update [[04-Task-Board]] and stop — do not start the next task

Constraints: follow [[01-Constitution]]. Do not invent facts — mark unknowns
as {{UPPER_SNAKE}} placeholders and list them as open questions. Distinguish
"the PRD requires", "the code does", and "not yet built" in every status
sentence. If a §29 locked decision would have to change to finish the task,
stop and raise it through §31 instead of deciding it in code.
```

## After implementing

`/review` before landing, `/ship` to land. Once a UI surface exists, `/qa` for
functional bugs and `/design-review` for the visual pass; `/investigate` when
something fails and the cause is not obvious. Verify a skill resolves before
relying on it in a time-boxed run.

---
Related: [[08-Definition-of-Done]] · [[02-Test-Cases]] · [[04-Task-Board]] · [[02-Workflow]]
