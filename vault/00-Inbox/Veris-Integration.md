---
title: Is there a Veris prize, requirement, or scenario API?
tags:
  - inbox
status: draft
---

# Is there a Veris prize, requirement, starter tool, or useful scenario API?

> [!info] Source
> [[00-Source-of-Truth-PRD|PRD]] §30 — "Is there a Veris prize, requirement,
> starter tool, or useful scenario API?" New in v2.1 — no capture existed for it.

- **Captured:** 2026-08-04
- **Source:** [[00-Source-of-Truth-PRD|PRD]] §30 (v2.1.0-FINAL), "Is there a
  Veris prize, requirement, starter tool, or useful scenario API?"
- **Decision deadline:** Kickoff, **before 5:15 PM**
- **Default if unresolved:** skip Veris and **do not claim integration**

## Why it matters

Veris AI is a co-host — that much is source-supported ([[00-Source-of-Truth-PRD|PRD]] §2.1). A
dedicated Veris prize track or mandatory integration is **unverified, and §2.1
says do not claim it.**

The risk here runs both ways, which is why it has a deadline before the build
window opens:

- Assume a prize track that doesn't exist → hours spent on an integration
  nobody asked for, taken from contingency.
- Assume no requirement when one exists → a missed judging dimension found out
  at 8:45 PM.

Both are avoided by one question at kickoff.

## The three questions to ask

Verbatim from [[00-Source-of-Truth-PRD|PRD]] §2.4:

1. Is there a Veris-specific prize, judging dimension, or required artifact?
2. Can Veris run scenario tests against a public HTTP agent within the remaining
   time?
3. Is there an SDK, starter project, account, or credit requirement that must be
   prepared?

## The 30-minute rule

§2.4 sets the gate precisely. Integrate **only** if support is confirmed *and*
the work fits without consuming contingency time. If requirements are
unconfirmed, unavailable, or would take more than **30 minutes of untested
work**, skip it.

Veris must never endanger Cloud Run eligibility, the real-source path, the
captured evidence replay, or submission readiness. It is an evaluation-plane
integration, not a runtime dependency ([[00-Source-of-Truth-PRD|PRD]] §29).

## If it is confirmed

§2.4 pre-specifies the artifact — a scenario pack proving graceful degradation
across:

- Live source unavailable
- Duplicate or stale frames
- No candidate conflict
- Insufficient temporal evidence
- Roboflow or enrichment provider failure

Deliverable is a test result, screenshot, or machine-readable report. These are
the same failure modes [[05-Demo-Reliability]] already rehearses, so the pack is
mostly a matter of recording what should already work.

## How to resolve

- [ ] Ask the three §2.4 questions at kickoff, before 5:15 PM
- [ ] Log the answers in [[04-Organizer-Questions]]
- [ ] Time-box the go/no-go to the 30-minute rule — decide, don't drift
- [ ] If skipping, say nothing about Veris in the pitch or README

## Triage to

[[03-Sponsor-Resources]] for what Veris actually offers; the go/no-go to
[[05-Decision-Log]] with a timestamp. If confirmed, the scenario pack is
evaluation work — [[03-Agent-Evaluation]] and [[05-Demo-Reliability]].

---
Nothing stays in the inbox — see [[00-Triage]].
