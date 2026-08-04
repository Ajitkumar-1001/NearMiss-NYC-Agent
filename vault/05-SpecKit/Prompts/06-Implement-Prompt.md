---
title: Implement Prompt
tags:
  - speckit
status: draft
---

# Implement Prompt

**Purpose:** Execute one task, verify it, and stop.

## Prompt

```text
{{PASTE_CONTEXT}}

1. Make the smallest change that satisfies the task
2. Do not refactor adjacent code
3. Add or update the test case in [[02-Test-Cases]]
4. Run the verification and report the actual output
5. Update [[04-Task-Board]] and stop — do not start the next task

Constraints: follow [[01-Constitution]]. Do not invent facts — mark unknowns
as {{UPPER_SNAKE}} placeholders and list them as open questions.
```

> [!todo] Not filled in yet
> Tune the prompt after first use; record what worked in [[Experiment-Log]].

---
Related: [[08-Definition-of-Done]] · [[02-Test-Cases]] · [[04-Task-Board]] · [[02-Workflow]]
