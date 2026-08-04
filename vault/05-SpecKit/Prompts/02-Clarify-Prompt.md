---
title: Clarify Prompt
tags:
  - speckit
status: draft
---

# Clarify Prompt

**Purpose:** Find ambiguity in the spec before it becomes rework.

## Prompt

```text
{{PASTE_CONTEXT}}

1. List every underspecified term
2. For each, give the competing readings
3. Say which reading changes the build and how
4. Rank by cost of getting it wrong
5. Do not resolve them by guessing

Constraints: follow [[01-Constitution]]. Do not invent facts — mark unknowns
as {{UPPER_SNAKE}} placeholders and list them as open questions.
```

> [!todo] Not filled in yet
> Tune the prompt after first use; record what worked in [[Experiment-Log]].

---
Related: [[04-Organizer-Questions]] · [[07-Blocker-Log]] · [[04-MVP-Scope]] · [[02-Workflow]]
