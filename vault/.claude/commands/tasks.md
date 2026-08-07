---
description: SpecKit Tasks — decompose the plan, ordered by the readiness gate
---

Read `05-SpecKit/Prompts/04-Tasks-Prompt.md` and execute the prompt inside its
fenced `text` block exactly as written. That note is the prompt; this file only
routes to it.

Input is the `## Plan` section of `04-Architecture/02-High-Level-Design.md`.

Before starting:

- `05-SpecKit/01-Constitution.md` overrides anything this stage produces.
- The ordering rule in the prompt is non-negotiable: PRD §11.1's readiness gate
  comes first and nothing may be scheduled ahead of the deployment and
  captured-evidence baselines.
- Derive one task per bullet in §11.1's five baseline lists by reading the PRD
  directly. A dropped bullet is a dropped task.
- Note paths are relative to this vault. **Code paths are repo-root relative.**

Output lands in `08-Execution/04-Task-Board.md`.

Verify before claiming the stage is done: every task's done condition is a
**runnable command plus its expected output**, not a description. Split any
task whose done condition cannot be written that way, or mark it explicitly as
manual verification with the exact steps and the observable result.

$ARGUMENTS
