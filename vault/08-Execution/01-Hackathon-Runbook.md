---
title: Hackathon Runbook
tags:
  - execution
status: draft
---

# Hackathon Runbook

The operational sequence. Follow it rather than improvising at hour 20.

## Before the clock starts

- [ ] Repo cloned and running on every machine
- [ ] `.env` populated from `.env.example`
- [ ] Sponsor credits claimed → [[03-Sponsor-Resources]]
- [ ] Fixtures recorded → [[ADR-001-Deterministic-Demo-First]]
- [ ] Roles agreed

## During

- [ ] Work only what's on [[04-Task-Board]]
- [ ] Blocked over {{BLOCK_MINUTES}} min → log it in [[07-Blocker-Log]] and switch tasks
- [ ] Check [[02-Time-Box-Plan]] at each checkpoint; cut per [[03-Scope-Ladder]]
- [ ] Commit working states often — a green commit is a rollback point

## Before submitting

- [ ] [[05-QA-Checklist]] fully passed
- [ ] [[04-Demo-Script]] rehearsed end-to-end at least twice
- [ ] Submission artifacts ready → [[01-Event-Brief]]

> [!todo] Not filled in yet
> Fill in venue-specific steps once logistics are known.

---
Related: [[02-Time-Box-Plan]] · [[04-Task-Board]] · [[03-Scope-Ladder]] · [[05-QA-Checklist]]
