---
title: Plan Prompt
tags:
  - speckit
status: draft
---

# Plan Prompt

**Purpose:** Turn the clarified spec into a technical approach.

## Prompt

```text
{{PASTE_CONTEXT}}

1. Propose the component breakdown
2. Name the interfaces between components
3. Identify the riskiest assumption and how to test it first
4. Call out where an ADR is needed
5. State what you are deliberately not building

Constraints: follow [[01-Constitution]]. Do not invent facts — mark unknowns
as {{UPPER_SNAKE}} placeholders and list them as open questions.
```

> [!todo] Not filled in yet
> Tune the prompt after first use; record what worked in [[Experiment-Log]].

---
Related: [[02-High-Level-Design]] · [[04-Component-Design]] · [[PRD]] §29 · [[02-Workflow]]
