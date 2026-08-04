---
title: QA Checklist
tags:
  - gstack
status: draft
---

# QA Checklist

Run before the demo. Every item is pass/fail, no "mostly".

## Core paths

- [ ] Cold start from a clean clone succeeds
- [ ] Demo path runs end-to-end on fixtures with the network **off**
- [ ] Every case in [[02-Test-Cases]] passes
- [ ] No console errors on the demo path

## Failure handling

- [ ] Provider outage degrades to fixtures with no visible error
- [ ] Empty and malformed input handled
- [ ] Slow network doesn't hang the UI

## Demo readiness

- [ ] Runs on the actual demo machine
- [ ] Runs on the actual demo screen resolution
- [ ] Reset-to-start takes under {{RESET_SECONDS}} seconds

> [!todo] Not filled in yet


---
Related: [[05-Demo-Reliability]] · [[02-Test-Cases]] · [[01-Workflow]] · [[08-Definition-of-Done]]
