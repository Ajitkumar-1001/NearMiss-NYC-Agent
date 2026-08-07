---
title: Starter repo or mandatory output format?
tags:
  - inbox
status: draft
---

# Does the event mandate a starter repository or output format?

> [!info] Source
> [[00-Source-of-Truth-PRD|PRD]] §30 — "Is there a mandatory starter repo or
> submission format?" (Captured against v2.0 as a §29 item — §29 holds *locked
> decisions*, §30 holds open questions. Corrected against v2.1.0-FINAL.)

- **Captured:** 2026-08-03
- **Source:** [[00-Source-of-Truth-PRD|PRD]] §30 (v2.1.0-FINAL), "Is there a
  mandatory starter repo or submission format?"
- **Decision deadline:** Kickoff
- **Default if unresolved:** preserve the current repo; adapt metadata only

## Why it matters

**Answer this one first.** It is the only open question that can invalidate an
already-accepted decision. A mandatory starter repo or submission format could
override the FastAPI backend and Next.js dashboard decisions locked in
[[00-Source-of-Truth-PRD|PRD]] §29 — the latter is already qualified there as "preferred but not
allowed to endanger the Cloud Run agent".

Every hour spent building on the wrong scaffold before this is answered is an
hour spent twice.

## How to resolve

- [ ] Read the event brief and submission rules end to end
- [ ] Ask the organizers directly — log the question in [[04-Organizer-Questions]]
- [ ] Confirm the required submission artifacts: repo, demo URL, video, slides
- [ ] Confirm whether a specific output schema is imposed on the event record

## Triage to

[[01-Event-Brief]] and [[02-Rules-and-Constraints]]; also
[[06-Hackathon-Compliance-Checklist]], which now owns the submission-artifact
list. Any event-specific rule that overrides this vault's decisions goes in
[[05-Decision-Log]]. If it changes the stack, supersede the affected ADR rather
than editing it, and add the matching §29 entry.

> [!info] The freeze changes the escalation path
> v2.1 §30 states that because the PRD is frozen, **no PRD revision is required
> onsite** unless an organizer change invalidates the product thesis, safety
> boundary, or Cloud Run eligibility contract. A mandated starter repo would hit
> that bar — it is the one answer here that could force a §31 change. A mandated
> *output format* almost certainly would not; that is a decision-log entry.

---
Nothing stays in the inbox — see [[00-Triage]].
