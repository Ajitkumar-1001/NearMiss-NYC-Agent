---
title: Deploy frontend and backend together or separately?
tags:
  - inbox
status: draft
---

# Should the frontend and backend be deployed together or separately?

> [!info] Source
> [[PRD]] §30, open question 6. [[PRD]] §30 deliberately
> left this open rather than guessing.

- **Captured:** 2026-08-03
- **Source:** [[PRD]] §30

## Why it matters

Blocks the first line of [[08-Definition-of-Done]]'s P0 list — a deployed
dashboard that loads without authentication. A working public URL is a
submission requirement, and deployment failure is a High-impact risk
([[06-Risk-Register]] row 9).

The decision is reversible, which is why it is a question and not an ADR. What is
**not** reversible is losing hours to it: the mitigation is to deploy a health
skeleton early and keep a known-good revision, whichever topology wins.

Google Cloud Run deployment is no longer just a locked architecture preference —
[[PRD]] §2.2 makes it a hard eligibility gate: public reachability without judge
authentication, `GET /health` returning HTTP 200, listening on `0.0.0.0:$PORT`,
and identifying the deployed revision/processing mode are explicit P0 acceptance
criteria ([[PRD]] §11.1; [[PRD]] §15 NFR-001, NFR-002). "Cloud Run first" is now
product principle #1 ([[PRD]] §10).

[[PRD]] §16.1 resolves part of this question directly, even though the exact
choice is still open: the dashboard may be a separate Next.js application or a
lightweight frontend served by the Cloud Run service, and dashboard deployment
location is explicitly **not** the eligibility gate — only the FastAPI agent must
be visibly deployed on Cloud Run.

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
> [[PRD]] §1's list of changes requiring an **ADR and a PRD version bump** grew in
> v2.0: it now names the Cloud Run eligibility contract explicitly, alongside
> deployment architecture. A same-container-versus-two-targets call is an
> implementation detail; abandoning Cloud Run is not — that supersedes
> [[PRD]] §30.

---
Nothing stays in the inbox — see [[00-Triage]].
