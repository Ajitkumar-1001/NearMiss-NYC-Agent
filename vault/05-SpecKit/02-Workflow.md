---
title: SpecKit Workflow
tags:
  - speckit
status: draft
---

# SpecKit Workflow

Specify → Clarify → Plan → Tasks → Analyze → Implement. Each stage has a prompt.

| Stage | Prompt | Output lands in |
|---|---|---|
| 1. Specify | [[01-Specify-Prompt]] | [[04-MVP-Scope]] |
| 2. Clarify | [[02-Clarify-Prompt]] | [[04-Organizer-Questions]], spec updates |
| 3. Plan | [[03-Plan-Prompt]] | [[02-High-Level-Design]] |
| 4. Tasks | [[04-Tasks-Prompt]] | [[04-Task-Board]] |
| 5. Analyze | [[05-Analyze-Prompt]] | [[06-Risk-Register]] |
| 6. Implement | [[06-Implement-Prompt]] | `app/` |

## Rules

- Don't skip Clarify. Ambiguity found at Implement costs the most.
- Anything constraining later stages becomes an ADR ([[ADR-Template]]).
- Principles in [[01-Constitution]] override the output of any stage.

> [!todo] Not filled in yet
> Note any deviations from stock SpecKit here so the team isn't surprised.

---
Related: [[01-Constitution]] · [[01-Workflow]] · [[04-Task-Board]]
