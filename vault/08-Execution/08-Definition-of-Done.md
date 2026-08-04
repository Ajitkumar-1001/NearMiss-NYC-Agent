---
title: Definition of Done
tags:
  - execution
status: active
---

# Definition of Done

A task is done when **every** box is ticked. No partial credit.

- [ ] Behaviour matches its acceptance criterion in [[04-MVP-Scope]]
- [ ] Works on the fixture path with the network off
- [ ] Has a case in [[02-Test-Cases]] and it passes
- [ ] No new console errors on the demo path
- [ ] Provider failures degrade gracefully → [[07-Provider-Adapters]]
- [ ] Committed, pushed, and running on a teammate's machine
- [ ] [[04-Task-Board]] updated

## P0 — hackathon-complete

> [!info] Source
> [[PRD]] §26, verbatim. P1 and P2 are enhancements and do not change this list.

- [ ] Agent is deployed on Google Cloud Run
- [ ] Agent is publicly reachable without authentication
- [ ] `GET /health` returns HTTP 200
- [ ] Service binds to `0.0.0.0:$PORT`
- [ ] A real NYC source is configured and attributed
- [ ] The deployed service has fetched and analyzed the real source successfully
- [ ] Live-source result shows source, retrieval time, freshness, provider, and processing mode
- [ ] A valid no-conflict or insufficient-evidence state is implemented
- [ ] Captured evidence sequence plays correctly
- [ ] Bounding boxes and trajectory trails are visible in the evidence case
- [ ] One supported candidate conflict is highlighted
- [ ] Risk score and factor breakdown are displayed
- [ ] Cached or runtime historical context is displayed and sourced
- [ ] Structured explanation and limitations are displayed
- [ ] Every fallback is labeled
- [ ] Core captured-replay demo works without runtime external APIs
- [ ] Public repo includes README, architecture, deployment instructions, source policy, privacy boundaries, and demo instructions
- [ ] A permissive license is present
- [ ] Backup recording and screenshots exist locally
- [ ] Presenter can complete the golden demo in under two minutes
- [ ] Submission artifacts are ready before 8:15 PM, leaving buffer before the 8:30 PM lock

## For the project

- [ ] [[05-QA-Checklist]] fully passed
- [ ] [[04-Demo-Script]] rehearsed twice end-to-end
- [ ] Every claim in [[02-2-Minute-Pitch]] traces to a measured row in [[06-Success-Metrics]]
- [ ] Reliability gates in [[05-Demo-Reliability]] met — 10/10 local, 5/5 deployed
- [ ] Submission requirements met → [[01-Event-Brief]]

---
Related: [[PRD]] · [[04-MVP-Scope]] · [[05-QA-Checklist]] · [[02-Test-Cases]] · [[04-Task-Board]]
