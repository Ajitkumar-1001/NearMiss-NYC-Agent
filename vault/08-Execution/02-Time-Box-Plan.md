---
title: Time Box Plan
tags:
  - execution
status: draft
---

# Time Box Plan

Total available: {{TOTAL_HOURS}} hours.

| Block | Hours | Goal | Checkpoint |
|---|---|---|---|
| Setup | {{H}} | Everyone running, fixtures recorded | Pipeline runs on a fixture |
| Core build | {{H}} | MVP capability working | [[04-MVP-Scope]] item 1 passes |
| Integration | {{H}} | End-to-end path | [[05-QA-Checklist]] core paths |
| Polish | {{H}} | Demo-grade | [[04-Design-Review]] |
| Freeze | {{H}} | No new features, rehearse only | [[04-Demo-Script]] rehearsed |

> [!todo] Not filled in yet
> Set real hours once the schedule is known.

## Checkpoint rule

At each checkpoint: if the goal isn't met, cut from [[03-Scope-Ladder]] rather
than borrowing time from the next block. Borrowed time always comes out of
Freeze, and Freeze is what makes the demo work.

> [!caution] Freeze is not optional
> Features added after freeze are the single most common cause of a broken
> hackathon demo.

---
Related: [[01-Hackathon-Runbook]] · [[03-Scope-Ladder]] · [[04-Task-Board]] · [[05-Demo-Reliability]]
