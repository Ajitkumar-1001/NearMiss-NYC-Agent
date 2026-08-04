---
title: Deploy frontend and backend together or separately?
tags:
  - inbox
status: draft
---

# Should the frontend and backend be deployed together or separately?

> [!info] Source
> [[PRD]] §29, open question 5. [[ADR-009-Cloud-Run-Deployment]] deliberately
> left this open rather than guessing.

- **Captured:** 2026-08-03
- **Source:** [[PRD]] §29

## Why it matters

Blocks the first line of [[08-Definition-of-Done]]'s P0 list — a deployed
dashboard that loads without authentication. A working public URL is a
submission requirement, and deployment failure is a High-impact risk
([[06-Risk-Register]] row 9).

The decision is reversible, which is why it is a question and not an ADR. What is
**not** reversible is losing hours to it: the mitigation is to deploy a health
skeleton early and keep a known-good revision, whichever topology wins.

## How to resolve

- [ ] Time-box a spike on each: one container serving both, versus two targets
- [ ] Prefer whichever produces a public URL soonest — polish is rung 5 of
      [[03-Scope-Ladder]], deployment is rung 2
- [ ] Confirm CORS and API base URL handling for the separate case
- [ ] Confirm the Cloud Run request timeout clears the 60 s P1 budget
- [ ] Deploy the `GET /health` skeleton before any of this is settled

## Triage to

[[08-Deployment]], with the choice logged in [[05-Decision-Log]].

> [!warning] This may need more than a log entry
> [[PRD]] §1 lists deployment architecture among the changes requiring an **ADR
> and a PRD version bump**. A same-container-versus-two-targets call is an
> implementation detail; abandoning Cloud Run is not — that supersedes
> [[ADR-009-Cloud-Run-Deployment]].

---
Nothing stays in the inbox — see [[00-Triage]].
