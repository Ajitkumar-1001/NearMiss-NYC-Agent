---
title: Analyze Prompt
tags:
  - speckit
status: draft
---

# Analyze Prompt

**Purpose:** Adversarial review of the plan and tasks before writing code.

## Prompt

```text
{{PASTE_CONTEXT}}

1. Where does this plan fail under time pressure?
2. Which task is on the critical path and what happens if it slips?
3. What breaks if a provider is down mid-demo?
4. Which assumption, if wrong, invalidates the most work?
5. What is missing that no task covers?

Constraints: follow [[01-Constitution]]. Do not invent facts — mark unknowns
as {{UPPER_SNAKE}} placeholders and list them as open questions.
```

> [!todo] Not filled in yet
> Tune the prompt after first use; record what worked in [[Experiment-Log]].

---
Related: [[06-Risk-Register]] · [[05-Demo-Reliability]] · [[03-Scope-Ladder]] · [[02-Workflow]]
