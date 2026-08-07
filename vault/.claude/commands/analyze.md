---
description: SpecKit Analyze — adversarial review of plan and tasks, report only
---

Read `05-SpecKit/Prompts/05-Analyze-Prompt.md` and execute the prompt inside its
fenced `text` block exactly as written. That note is the prompt; this file only
routes to it.

Inputs are the `## Plan` section of `04-Architecture/02-High-Level-Design.md`
and the task list in `08-Execution/04-Task-Board.md`.

Before starting:

- `05-SpecKit/01-Constitution.md` overrides anything this stage produces.
- The three KNOWN RISK blocks in the prompt are already verified. **Do not spend
  the run rediscovering them** — assume them, confirm the plan and tasks cover
  each, then go find what they still miss.
- Note paths are relative to this vault. **Code paths are repo-root relative.**

Output lands in `08-Execution/06-Risk-Register.md`.

**This is report-only.** Propose no fixes and change no code. Report only what
you can point at in a file or a PRD section — a finding without a `file:line` or
a `§` reference is not a finding.

$ARGUMENTS
