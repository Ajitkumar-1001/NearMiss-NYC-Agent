---
title: Tasks Prompt
tags:
  - speckit
status: draft
---

# Tasks Prompt

**Purpose:** Decompose the plan into independently completable tasks.

## Prompt

```text
{{PASTE_CONTEXT}}

1. One task = one verifiable outcome
2. Mark dependencies explicitly
3. Flag which tasks can run in parallel
4. Estimate in hours against [[02-Time-Box-Plan]]
5. Every task states its done condition

Constraints: follow [[01-Constitution]]. Do not invent facts — mark unknowns
as {{UPPER_SNAKE}} placeholders and list them as open questions.
```

> [!todo] Not filled in yet
> Tune the prompt after first use; record what worked in [[Experiment-Log]].

---
Related: [[04-Task-Board]] · [[02-Time-Box-Plan]] · [[08-Definition-of-Done]] · [[02-Workflow]]
