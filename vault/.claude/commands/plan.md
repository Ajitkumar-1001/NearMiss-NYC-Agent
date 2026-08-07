---
description: SpecKit Plan — technical approach against the verified code state
---

Read `05-SpecKit/Prompts/03-Plan-Prompt.md` and execute the prompt inside its
fenced `text` block exactly as written. That note is the prompt; this file only
routes to it.

Before starting:

- `05-SpecKit/01-Constitution.md` overrides anything this stage produces.
- `05-SpecKit/02-Workflow.md` records that Specify and Clarify are already
  satisfied by the frozen PRD. Do not re-run them and do not restate the spec.
- Note paths are relative to this vault. **Code paths are repo-root relative**
  (`app/backend/nearmiss/risk.py`) — one level above this directory.

Output lands in `04-Architecture/02-High-Level-Design.md` under a dated
`## Plan` heading. **Append** — the verified state analysis already in that note
is the input to this stage, not something to overwrite.

Verify before claiming the stage is done: the plan answers all five numbered
outputs the prompt demands, and gives a fix-or-deviation disposition for every
contradiction listed in `05-SpecKit/Prompts/05-Analyze-Prompt.md`.

$ARGUMENTS
