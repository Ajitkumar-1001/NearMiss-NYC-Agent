---
title: Specify Prompt
tags:
  - speckit
status: active
---

# Specify Prompt

**Purpose:** Turn intent into an unambiguous spec — what, for whom, and how we'll know it works.

> [!warning] Stage complete — do not re-run `/specify`
> [[00-Source-of-Truth-PRD|PRD]] §1 makes the PRD the canonical spec: when any
> other note, prompt, README, or implementation decision conflicts with it, the
> PRD wins. Re-running `/specify` produces a second spec, and a second spec
> means there is no single source of truth any more.
>
> Everything this stage would generate is already written: problem (§4), users
> (§6), jobs (§7), goals (§8), non-goals (§9), scope ladder (§11),
> capabilities with acceptance criteria (§14 FR-001–FR-022, §15
> NFR-001–NFR-012), and definition of done (§26).
>
> Changing the spec is a §31 change-control action with a version increment —
> not a re-run of this prompt. The entry point for build work is
> [[03-Plan-Prompt]].

## Prompt

Kept for reference. If this vault structure is reused on a project with no
frozen spec, this is the shape that worked.

```text
CONTEXT
The spec for NearMiss NYC is [[00-Source-of-Truth-PRD|PRD]], already written and
frozen under §31. Do not regenerate it. If you were invoked to change the spec,
stop and follow the eight-item §31 change-control protocol instead, read from
the PRD — including item 8's organizer-evidence requirement, which is the
only sanctioned trigger for a new PRD version under the §31 pre-event freeze.

1. Restate the problem without naming a solution
2. Define the user and their job
3. List capabilities with acceptance criteria
4. List explicit non-goals
5. Flag every assumption as an open question

Constraints: follow [[01-Constitution]]. Do not invent facts — mark unknowns
as {{UPPER_SNAKE}} placeholders and list them as open questions.
```

---
Related: [[04-MVP-Scope]] · [[05-Non-Goals]] · [[02-Problem-Statement]] · [[02-Workflow]]
