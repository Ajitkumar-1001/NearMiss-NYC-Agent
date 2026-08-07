---
description: SpecKit Implement — execute exactly one task, verify it, and stop
---

Read `05-SpecKit/Prompts/06-Implement-Prompt.md` and execute the prompt inside
its fenced `text` block exactly as written. That note is the prompt; this file
only routes to it.

Input is **one** task from `08-Execution/04-Task-Board.md`, selected by the
ordering that `05-SpecKit/Prompts/04-Tasks-Prompt.md` produced. One. Not a
phase, not a baseline.

Before starting:

- `05-SpecKit/01-Constitution.md` overrides anything this stage produces.
- Read the files you are about to change, before changing them.
- Fixtures must match `app/backend/nearmiss/models.py` field for field — the
  models are Pydantic v2 with `extra="forbid"`, so a drifted key fails at load
  time rather than being tolerated.
- The captured replay must be verified with **networking disabled**, not merely
  with the live provider unselected.
- Note paths are relative to this vault. **Code paths are repo-root relative** —
  write code to `app/`, `demo/`, and `tests/` one level above this vault, never
  inside it.

The evidence rule, restated because it is the one that gets faked: every claim
of completion must be backed by the **actual output of a command, pasted
verbatim**. Not a description of the output. Not "verified". If you did not run
the command, the task is not done.

When the task is done: update `08-Execution/04-Task-Board.md` and **stop**. Do
not start the next task.

If finishing the task would require changing a PRD §29 locked decision, stop and
raise it through §31 rather than deciding it in code.

$ARGUMENTS
