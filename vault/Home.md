---
title: Home
tags:
  - moc
status: draft
---

# NearMiss NYC

Vault hub. Every section's entry note is linked below — start here.

> [!info] Status
> [[00-Source-of-Truth-PRD|PRD]] v2.1.0-FINAL is landed, authoritative, and frozen before the
> event (§1.3 item 6). Product, Decisions, and the API/data contracts are filled
> from it. Event, Research, Evaluation, and Pitch are still structured stubs;
> `{{UPPER_SNAKE}}` marks a fact that still needs a real source. Search the vault
> for `{{` to find them all.

## Source of truth

[[00-Source-of-Truth-PRD|PRD]] lives at `02-Product/00-Source-of-Truth-PRD.md` and is the canonical
product and implementation authority. When any note in this vault conflicts with
it, the PRD wins — see [[00-Source-of-Truth-PRD|PRD]] §1. Changing the product thesis, P0, the event
taxonomy, risk semantics, provider boundaries, safety requirements, the demo
flow, or the deployment architecture requires an ADR *and* a PRD version bump.

## Sections

| # | Section | Entry note |
|---|---|---|
| 00 | Inbox | [[00-Triage]] |
| 01 | Event | [[01-Event-Brief]] |
| 02 | Product | [[01-Project-Overview]] |
| 03 | Research | [[01-Datasets]] |
| 04 | Architecture | [[01-System-Context]] |
| 05 | SpecKit | [[01-Constitution]] |
| 06 | gstack | [[01-Workflow]] |
| 07 | Decisions | [[00-ADR-Index]] |
| 08 | Execution | [[01-Hackathon-Runbook]] |
| 09 | Evaluation | [[01-Test-Strategy]] |
| 10 | Pitch | [[01-30-Second-Pitch]] |
| 11 | Templates | [[Capture]] |
| 12 | Logs | [[Progress-Log]] |

## Working set

The notes that change most during the build:

- [[04-Task-Board]] — what's in flight
- [[07-Blocker-Log]] — what's stuck
- [[03-Scope-Ladder]] — what to cut when time runs short
- [[05-Demo-Reliability]] — what must not break on stage
- [[06-Hackathon-Compliance-Checklist]] — the one thing that disqualifies us
- [[09-Preexisting-Code-Disclosure]] — what we say we built today

## Conventions

Repo orientation is in [[README]]. Agent-facing rules for editing this vault
live in [[CLAUDE]] and [[AGENTS]].
