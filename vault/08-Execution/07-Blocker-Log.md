---
title: Blocker Log
tags:
  - execution
status: active
---

# Blocker Log

Anything stopping work. Log it, switch tasks, come back.

> [!important] Scope boundary — read before adding a row
> This note owns **what is stopping work right now**, verified against the tree.
> [[06-Risk-Register]] owns **what might happen** ([[00-Source-of-Truth-PRD|PRD]] §28).
> A risk that materialises leaves the register and becomes a row here. Nothing
> hypothetical belongs in this note; nothing already true belongs in that one.
> If an entry needs a likelihood, it is a risk, not a blocker.

**Clock:** today is Thursday 6 August 2026. The [[00-Source-of-Truth-PRD|PRD]] §11.1 readiness gate
fires **tonight at 8:00 PM ET**. The event is tomorrow, Friday 7 August, 4:00–10:00 PM ET.

## Active

| # | Blocker | Blocking | Raised | Owner | Unblocked when |
|---|---|---|---|---|---|
| 1 | Eligibility gate has no code behind it | [[00-Source-of-Truth-PRD\|PRD]] §2.2 (failure means the submission is not hackathon-complete); §11.1 deployment baseline | 2026-08-05 | Ajit | All five §2.2 service requirements hold — public reachability and `GET /health` are only two; a working real-source analysis endpoint and an identifiable revision + processing mode are also required. The public URL replaces `{{BE_URL}}` in [[08-Deployment]]; the known-good revision and rollback command are recorded there (§27.1 item 7) |
| 2 | Guaranteed fallback cannot run — `demo/fixtures/` is empty | [[ADR-006-Real-Source-P0-with-Captured-Fallback]]; §11.1 captured evidence baseline; the §27.3 never-remove list | 2026-08-05 | Ajit | `detections.json`, `tracks.json` and `context.json` are committed under `demo/fixtures/` and one captured replay completes end to end, locally **and on the deployed service** (§27.1 items 15–16) |
| 3 | Schedule has slipped a full day against §27.1 | Every P0 item on the Tuesday, Wednesday and Thursday lists | 2026-08-05 | Ajit | All three §27.1 lists (items 1–24) reach zero outstanding, **or** [[03-Scope-Ladder]] is cut until the remaining scope fits the hours actually left |

### 1 — Eligibility gate has no code behind it

[[00-Source-of-Truth-PRD|PRD]] §2.2 requires a publicly reachable Cloud Run service answering
`GET /health` before the 8:30 PM submission lock, and states that failing it
means the submission is not hackathon-complete even when the local application
works. That service is **not yet built**.

Verified in the tree today:

- No tracked file under `app/backend/nearmiss/` mentions FastAPI, uvicorn, or
  `APIRouter`. `pyproject.toml` declares FastAPI and uvicorn as dependencies
  (`fastapi>=0.115`, `uvicorn[standard]>=0.32`); nothing imports them.
- `models.py` defines `Health` and `DependencyStatus`; nothing serves them.
- No `Dockerfile` exists anywhere in the repository.
- `command -v gcloud` fails — the CLI is not installed. §27.1 item 4 is
  therefore not started, and items 5–7 cannot begin until it is.

This is a blocker rather than a task because §2.2 is a gate, not a feature: no
amount of other progress substitutes for it. §2.1 records "The only stated
eligibility gate is deployment on Google Cloud Run" as organizer-page-derived
and to be reconfirmed at kickoff — treat the exclusivity as unverified, and the
gate itself as binding regardless.

### 2 — Guaranteed fallback cannot run

[[ADR-006-Real-Source-P0-with-Captured-Fallback]] makes captured replay the path
that always works, and §27.3 lists it among the things that may never be removed
or destabilised. It **cannot complete a single run today**.

Verified in the tree today:

- `demo/fixtures/` contains only `README.md`.
- The code resolves three fixture files that do not exist:
  `providers/vision.py:43` → `detections.json`, `providers/tracking.py:37` →
  `tracks.json`, `providers/context.py:48` → `context.json`.
  `providers/base.py:56` raises `FileNotFoundError` for a missing fixture, and
  its docstring is explicit that this is not a `ProviderUnavailable`.
- The rungs above the fixture rung are declining stubs by design at P0:
  `providers/vision.py:32`, `providers/tracking.py:21` and
  `providers/context.py:33` all raise `ProviderUnavailable`.

So for detection, tracking and context the fixture rung is not currently a
*fallback* — it is the only rung with behaviour, and it cannot load. The
explanation ladder is unaffected: `providers/explanation.py:60`
`TemplateExplanation` is fully implemented and reads no fixture, as is
`risk.py:85` `RiskEngine`.

Committing the fixtures is the cheaper of the two §11.1 baselines to close, but
it does not produce a demo on its own — §27.1 item 16 requires the replay to be
verified locally **and on the deployed service**, and there is no HTTP surface
yet. Blocker 1 still gates that half.

### 3 — Schedule has slipped a full day

§27.1 has **three** dated lists: eight deployment items on Tuesday 4 August
(1–8), nine evidence-and-package items on Wednesday 5 August (9–17), and seven
submission items on Thursday 6 August (18–24). No list has been closed.

- **Tuesday (1–8): overdue.** Items 4, 5, 6 and 7 are contradicted by the tree
  directly — no `gcloud`, no FastAPI app, no `Dockerfile`, `{{BE_URL}}` still
  unresolved in [[08-Deployment]]. Items 1, 2, 3 (Cloud account, billing, API
  enablement) and 8 (Roboflow account, key, smoke test) are external console
  state this repository cannot see: **unknown — needs human confirmation**, not
  "not done". `.env` and `.env.*` are gitignored, so an absent `.env` is not
  evidence either way.
- **Wednesday (9–17): due today, no repo-visible progress.**
  `app/backend/pyproject.toml` declares no `vision-conflict-analytics`
  dependency, so item 12's pin is not done; `demo/fixtures/` holds only
  `README.md` (item 15), which also blocks items 16–17. Items 9–11 live in a
  separate public repository — external state, unknown here.
- **Thursday (18–24): not started.** Item 19 alone — finalize the six §11.3
  dashboard surfaces — is a from-scratch day of work: `app/frontend/` holds only
  `README.md`. Items 18, 23 and 24 (keys, organizer questions) are external.

**Twenty-four §27.1 items are outstanding or unconfirmed across all three
lists.** Everything the tree can see is not done; the account, key, organizer
and external-repo items (1–3, 8, 9–11, 18, 23–24) are **unknown — needs human
confirmation**. The §11.1 readiness gate is Thursday 6 August, 8:00 PM ET: a day
and a half out. Blockers 1 and 2 are the two baselines §11.1 names, and its
readiness rule stops all optional work if either is incomplete by that time. The
response to blocker 3 is not more hours — it is [[03-Scope-Ladder]].

## Escalation

> [!danger] Thursday 6 August, 8:00 PM ET
> Two instruments apply here, and **neither is §27.3**.
>
> §11.1's readiness rule applies first and is the narrower one: if the
> deployment baseline (blocker 1) or the captured evidence baseline (blocker 2)
> is not complete by that time, all optional product work stops until they are.
>
> §27.1's "Thursday 8:00 PM readiness decision" then picks the branch — fix
> deployment, or finish fixtures, or freeze both and prepare only small
> event-day adapters.
>
> §27.3 is the **event-day** kill order, scoped to Friday from 5:15 PM when time
> is lost. Cut order there is §27.3's list; the never-remove list is its closing
> paragraph. Do not apply it at this gate.

Pre-event cuts (Wednesday and Thursday) are governed by [[03-Scope-Ladder]], not
by §27.3 — the two are different, non-matching lists and must not be treated as
one instrument.

> [!warning] Open inconsistency — for [[05-Decision-Log]]
> [[03-Scope-Ladder]]'s scope-freeze rule is anchored to 8:00 PM, while
> [[00-Source-of-Truth-PRD|PRD]] §29 locks 7:00 PM as the hard feature freeze
> (8:00–8:15 PM is protected contingency). Unresolved — do not silently pick
> one.

## Not blockers

Unstarted P0 work is not a blocker — it is scope, and it lives on
[[04-Task-Board]] and [[03-Scope-Ladder]]. Currently unstarted and **not yet
built**: the source registry (FR-001), the source adapter (FR-002 / FR-004),
provenance capture (FR-003), the reusable package (FR-022), the six judge-facing
surfaces of §11.3 (`app/frontend/` holds only `README.md`), and any test suite
(`tests/` holds only `README.md`).

One of these is worth flagging early because it changes shape under time
pressure: `VisionProvider.detect()` takes no arguments, so a live frame has
nowhere to go. Adding the real-source path is a Protocol signature change with
blast radius across `vision.py`, `tracking.py` and `orchestrator.py` — not a
drop-in. Start it before §29's 7:00 PM feature freeze or not at all. The item
itself is owned by [[04-Task-Board]]; this note only flags the shape.

## Resolved

| # | Blocker | Resolution | Cost (h) |
|---|---|---|---|
| | | | |

> [!warning] The {{BLOCK_MINUTES}}-minute rule
> Stuck longer than that on one thing? Log it here and move to another task on
> [[04-Task-Board]]. Sunk time is the most expensive thing at a hackathon.

Blockers needing an organizer answer also go to [[04-Organizer-Questions]].

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[04-Task-Board]] · [[06-Risk-Register]] · [[03-Scope-Ladder]] · [[08-Definition-of-Done]] · [[05-Decision-Log]] · [[04-Organizer-Questions]] · [[Progress-Log]]
