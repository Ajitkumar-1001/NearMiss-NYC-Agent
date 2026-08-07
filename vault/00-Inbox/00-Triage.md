---
title: Triage
tags:
  - inbox
status: active
---

# Triage

This folder is a queue, not a home. Anything here is waiting to be routed.

## The rule

**Nothing stays.** A capture is done when its content lives in the note that owns
it and the capture file is deleted. An inbox that accumulates is an inbox nobody
reads.

## Procedure

1. **Read the capture.** If it's still a question, it stays until answered.
2. **Find the owner** — routing table is in [[CLAUDE]]. One note owns each fact.
3. **Move the content there**, in that note's own structure. Don't paste a capture
   verbatim into a section that wants a table row.
4. **Record the decision if there was one** — [[05-Decision-Log]] for almost
   everything. A decision that *constrains the build* needs an ADR in
   `07-Decisions/` **and** a locked entry in [[00-Source-of-Truth-PRD|PRD]] §29,
   through the §31 protocol. §30 is the open-questions table, not a place to
   file answers.
5. **Delete the capture.**

> [!warning] The PRD is frozen — escalate sparingly
> v2.1.0-FINAL is frozen before the event (§1.3 item 6). §30 says no PRD
> revision is required onsite **unless** an organizer change invalidates the
> product thesis, the safety boundary, or the Cloud Run eligibility contract.
> Below that bar, the answer goes in [[05-Decision-Log]] with a timestamp and
> impact — not into a version bump.

## What belongs here

Something you don't want to lose and can't file in ten seconds: an unanswered
question, a link to chase, an organizer's offhand remark, a fact you have no
source for yet.

## What doesn't

- Anything with an obvious owner — file it directly, skip the queue.
- Work items. Those go on [[04-Task-Board]].
- Blockers. Those go on [[07-Blocker-Log]] immediately.
- Anything contradicting [[00-Source-of-Truth-PRD|PRD]] — the PRD wins, so raise it as a PRD change per
  [[00-Source-of-Truth-PRD|PRD]] §31 rather than parking a contradiction here.

## Current queue

Seeded from [[00-Source-of-Truth-PRD|PRD]] §30 (v2.1.0-FINAL), which lists **nine** open questions.
Every capture carries its §30 decision deadline and its default-when-unresolved,
because on a six-hour event the default *is* the answer for anything not settled
in time.

Ordered by deadline — the top three are event-day clocks:

| Capture | Deadline | Default if unresolved |
|---|---|---|
| [[Camera-Source]] | Kickoff, 4:45 PM | Use the already tested approved source |
| [[Veris-Integration]] | Kickoff, before 5:15 PM | Skip Veris; claim nothing |
| [[Source-Temporal-Sufficiency]] | Before 5:35 PM | Live snapshot proof only; replay for trajectories |
| [[Starter-Repo-Format]] | Kickoff | Preserve the repo; adapt metadata only |
| [[Roboflow-Model]] | Thursday 6 Aug | Smallest already validated option |
| [[Demo-Intersection]] | Thursday 6 Aug | Label only; do not invent coordinates |
| [[NYC-Open-Data-Fields]] | Thursday 6 Aug | Cached, source-attributed context |
| [[Roboflow-Upstream-Path]] | Mentor talk, after P0 is stable | Keep the standalone package; no onsite refactor |

The §30 table is unnumbered, so a capture is identified by its question text,
not by a row number. The §30 question "What is the policy for pre-existing code,
scaffolding, reusable packages, and prepared fixtures?" has no capture on
purpose. It already has an owner: [[09-Preexisting-Code-Disclosure]].

Narrowed but not closed: [[Camera-Source]] and [[Roboflow-Model]] are both
bounded by §18's approved data-source policy and §17's model/license policy.

New captures start from [[Capture]].

---
Related: [[CLAUDE]] · [[Capture]] · [[00-Source-of-Truth-PRD|PRD]] · [[05-Decision-Log]] · [[04-Task-Board]]
