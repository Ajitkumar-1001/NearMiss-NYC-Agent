---
title: Specify Prompt
tags:
  - speckit
status: draft
---

# Specify Prompt

**Purpose:** Turn intent into an unambiguous spec — what, for whom, and how we'll know it works.

## Prompt

```text
{{PASTE_CONTEXT}}

1. Restate the problem without naming a solution
2. Define the user and their job
3. List capabilities with acceptance criteria
4. List explicit non-goals
5. Flag every assumption as an open question

Constraints: follow [[01-Constitution]]. Do not invent facts — mark unknowns
as {{UPPER_SNAKE}} placeholders and list them as open questions.
```

> [!todo] Not filled in yet
> Tune the prompt after first use; record what worked in [[Experiment-Log]].

---
Related: [[04-MVP-Scope]] · [[05-Non-Goals]] · [[02-Problem-Statement]] · [[02-Workflow]]
