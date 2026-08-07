---
title: Preexisting Code Disclosure
tags:
  - execution
status: active
---

# Preexisting Code Disclosure

> [!info] Role
> Named in [[00-Source-of-Truth-PRD|PRD]] §32.1 as the submission transparency artifact. Required
> by §1.3 item 4: the public README must separate pre-event scaffolding,
> reusable components, fixtures, and event-day integration work.

This note is the working draft. Its content ships in the public README before
the 8:30 PM lock.

## Why this exists

[[00-Source-of-Truth-PRD|PRD]] §11.1 deliberately front-loads work: deployment baseline, captured
evidence, and the `vision-conflict-analytics` package are all **pre-event
artifacts, not event-day build tasks**. That is a sound execution strategy and a
disclosure obligation — a judge seeing a polished system at 8:45 PM is entitled
to know what existed at 4:00 PM.

Disclosing it costs nothing. Not disclosing it and being asked is the risk.

## The commit boundary

The build window opens at approximately 5:15 PM ET on Friday 7 August 2026.

- **Boundary commit:** {{BOUNDARY_COMMIT_SHA}}
- **Timestamp:** {{BOUNDARY_COMMIT_TIME}}
- **Tag:** {{BOUNDARY_TAG}}

Everything reachable from that commit is pre-event. Everything after is
event-day work. Tag it before the window opens — reconstructing the boundary
afterwards is not credible.

## Existed before the event

### Scaffolding
- FastAPI service skeleton and Cloud Run deployment configuration
- Next.js dashboard shell
- Repository structure, license, CI configuration
- {{OTHER_SCAFFOLDING}}

### Reusable components
- `vision-conflict-analytics` — public package, separately licensed and
  released. See [[11-Vision-Conflict-Analytics-Package]].
- Provider adapter interfaces → [[07-Provider-Adapters]]
- {{OTHER_REUSABLE}}

### Fixtures and captured assets
- The 10–20 second source-attributed NYC sequence
- Normalized detections, tracks, and the verified candidate-conflict event
- Cached, source-attributed NYC historical context
- Deterministic explanation output

### Deployment
- Google Cloud project, billing, enabled APIs
- A public Cloud Run revision verified from a logged-out browser

## Built during the event

- {{EVENT_DAY_WORK}}

Expected shape per [[00-Source-of-Truth-PRD|PRD]] §11: real-source integration against whatever feed
is actually available, live-path validation, presentation, and submission. Fill
this in as it happens — it is the section a judge reads most closely.

## Claim discipline

- Do not describe pre-event artifacts as built at the hackathon.
- Do not describe the captured replay as live analysis ([[00-Source-of-Truth-PRD|PRD]] FR-016 mode
  disclosure, §14).
- If asked what was built today, answer with this note's second list.

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[01-Hackathon-Runbook]] · [[02-Time-Box-Plan]] · [[08-Definition-of-Done]] · [[06-Hackathon-Compliance-Checklist]] · [[11-Vision-Conflict-Analytics-Package]]
