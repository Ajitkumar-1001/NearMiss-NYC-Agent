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
> [[PRD]] §24, verbatim. P1 and P2 are enhancements and do not change this list.

- [ ] Deployed dashboard loads without authentication
- [ ] `GET /health` returns HTTP 200
- [ ] Bundled clip plays correctly
- [ ] Bounding boxes and trajectory trails are visible
- [ ] One supported potential-conflict event is highlighted
- [ ] Risk score and factor breakdown are displayed
- [ ] Cached historical context is displayed and sourced
- [ ] Structured explanation and limitations are displayed
- [ ] Processing mode is labelled `Demonstration replay`
- [ ] Core demo works without runtime external APIs
- [ ] README includes setup, architecture, limitations, and demo instructions
- [ ] Backup recording and screenshots exist locally
- [ ] Presenter can complete the golden demo in under two minutes

## For the project

- [ ] [[05-QA-Checklist]] fully passed
- [ ] [[04-Demo-Script]] rehearsed twice end-to-end
- [ ] Every claim in [[02-2-Minute-Pitch]] traces to a measured row in [[06-Success-Metrics]]
- [ ] Reliability gates in [[05-Demo-Reliability]] met — 10/10 local, 5/5 deployed
- [ ] Submission requirements met → [[01-Event-Brief]]

---
Related: [[PRD]] · [[04-MVP-Scope]] · [[05-QA-Checklist]] · [[02-Test-Cases]] · [[04-Task-Board]]
