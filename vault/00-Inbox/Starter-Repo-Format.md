---
title: Starter repo or mandatory output format?
tags:
  - inbox
status: draft
---

# Does the event mandate a starter repository or output format?

> [!info] Source
> [[PRD]] §29, open question 6.

- **Captured:** 2026-08-03
- **Source:** [[PRD]] §29

## Why it matters

**Answer this one first.** It is the only open question that can invalidate an
already-accepted decision. A mandatory starter repo or submission format could
override the FastAPI backend and Next.js dashboard decisions locked in
[[PRD]] §29 — the latter is already qualified there as "preferred but not
allowed to endanger the Cloud Run agent".

Every hour spent building on the wrong scaffold before this is answered is an
hour spent twice.

## How to resolve

- [ ] Read the event brief and submission rules end to end
- [ ] Ask the organizers directly — log the question in [[04-Organizer-Questions]]
- [ ] Confirm the required submission artifacts: repo, demo URL, video, slides
- [ ] Confirm whether a specific output schema is imposed on the event record

## Triage to

[[01-Event-Brief]] and [[02-Rules-and-Constraints]]. Any event-specific rule that
overrides this vault's decisions goes in [[05-Decision-Log]] and into the next
PRD version, per [[PRD]] §29. If it changes the stack, supersede the affected ADR
rather than editing it.

---
Nothing stays in the inbox — see [[00-Triage]].
