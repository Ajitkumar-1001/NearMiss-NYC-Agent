---
title: QA Checklist
tags:
  - gstack
status: active
---

# QA Checklist

Run before the demo. Every item is pass/fail, no "mostly".

Run with `/qa` on Thursday before the 8:00 PM readiness gate and again Friday
before submission. After the 7:00 PM Friday freeze, use `/qa-only`.

## Blocking today

These are not aspirational items awaiting a run. They were checked on Tuesday
4 August and they **fail right now**. Nothing below this section can be trusted
until these two pass.

- [ ] **FAIL — Cold start from a clean clone succeeds.** There is no server to
  start. No tracked `.py` file references FastAPI, uvicorn, or `APIRouter`, and
  no Dockerfile exists. Blocks [[00-Source-of-Truth-PRD|PRD]] §2.2, the only
  stated eligibility gate. → [[03-Engineering-Review]] findings 1–3
- [ ] **FAIL — Demo path runs end-to-end on fixtures with the network off.**
  `demo/fixtures/` contains only `README.md`; `FixtureVision`, `FixtureTracker`,
  and `CachedContext` all raise `FileNotFoundError`. The guaranteed fallback
  cannot complete a single run. Blocks the §11.1 captured evidence baseline.
  → [[03-Engineering-Review]] finding 4

Everything in **Core paths** below is a re-check of the same ground once these
two are green. Do not tick a box in this file that has not actually been run.

## Core paths

- [ ] Cold start from a clean clone succeeds
- [ ] Demo path runs end-to-end on fixtures with the network **off**
- [ ] Every case in [[02-Test-Cases]] passes
- [ ] No console errors on the demo path

> [!warning] `tests/` contains only `README.md`
> There are no test files, so "every case in [[02-Test-Cases]] passes" is
> currently unrunnable rather than failing. It cannot be ticked until tests
> exist.

## Failure handling

- [ ] Provider outage degrades to fixtures with no visible error
- [ ] Empty and malformed input handled
- [ ] Slow network doesn't hang the UI

## Demo readiness

- [ ] Runs on the actual demo machine
- [ ] Runs on the actual demo screen resolution
- [ ] Reset-to-start takes under {{RESET_SECONDS}} seconds

> [!note] `{{RESET_SECONDS}}` stays unresolved
> There is nothing to reset yet, so no honest number exists. Measure it the
> first time the demo runs end-to-end, then fill it in.

## Deployed checks — Friday, against the Cloud Run URL

Not localhost. [[00-Source-of-Truth-PRD|PRD]] §26.2 is the authority; these are
the ones worth re-running by hand at the machine.

- [ ] `GET /health` returns HTTP 200 from a logged-out browser
- [ ] The response identifies the deployed revision and the active processing mode
- [ ] Every fallback is visibly labelled as a fallback
- [ ] Golden demo succeeds three consecutive times from the deployed URL

---
Related: [[05-Demo-Reliability]] · [[02-Test-Cases]] · [[01-Workflow]] · [[08-Definition-of-Done]]
