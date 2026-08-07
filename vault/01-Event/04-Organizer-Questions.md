---
title: Organizer Questions
tags:
  - event
status: active
---

# Organizer Questions

Open questions for organizers, and the answers once we get them.

> [!info] Filled from the PRD
> Seeded from [[00-Source-of-Truth-PRD|PRD]] §2.1's unverified list, §2.4's Veris questions, and the
> §30 rows whose deadline is *kickoff*. Every question carries the §30 default —
> **if it goes unanswered, the default is the answer.** Nothing here blocks the
> build.

## Ask at kickoff — in this order

The window is 4:00 PM to ~5:15 PM. Three of these have deadlines inside it.

### 1. Camera source — by 4:45 PM

> Is there an organizer starter-pack live camera feed, and what are its
> endpoint, auth, and usage terms?

Highest priority: it is the critical-path unknown for P0 ([[Camera-Source]]).
**Default:** use the already tested approved source.

### 2. Veris — by 5:15 PM

Verbatim from [[00-Source-of-Truth-PRD|PRD]] §2.4:

> 1. Is there a Veris-specific prize, judging dimension, or required artifact?
> 2. Can Veris run scenario tests against a public HTTP agent within the
>    remaining time?
> 3. Is there an SDK, starter project, account, or credit requirement that must
>    be prepared?

**Default:** skip Veris and claim nothing ([[Veris-Integration]]).

### 3. Starter repo or output format — at kickoff

> Is a starter repository mandatory? Is a specific submission or output schema
> imposed on the event record?

The only question that can invalidate an accepted decision
([[Starter-Repo-Format]]). **Default:** preserve the current repo, adapt
metadata only.

### 4. Submission mechanism

> Where exactly does the submission go, and what fields does it require?

Listed as unverified in §2.1. **Default:** none stated — this one genuinely
needs an answer before 8:30 PM.

### 5. Demo duration

> How long does each team get to present?

**Default:** prepare both [[01-30-Second-Pitch]] and [[02-2-Minute-Pitch]] and
deliver whichever fits.

### 6. Pre-existing code policy — reconfirm

> Are prepared scaffolding, reusable packages, and fixtures permitted, and how
> should they be disclosed?

§30's "What is the policy for pre-existing code, scaffolding, reusable packages,
and prepared fixtures?" says reconfirm at kickoff even though we have a working
answer.
**Default:** disclose everything, separating pre-event from event-day commits
([[09-Preexisting-Code-Disclosure]]).

### 7. Lower priority

- Final judge list — §2.1 unverified
- Attendee-specific sponsor credits — §2.1 unverified
- Video and slide-deck requirements, if any

## Answered

| Question | Answer | Asked | Source |
|---|---|---|---|
| | | | |

> [!warning] Record answers as they land
> [[00-Source-of-Truth-PRD|PRD]] §32.3: an organizer update received during the event goes into
> [[05-Decision-Log]] with **timestamp and impact**. Because the PRD is frozen,
> §30 requires no PRD revision onsite unless the answer invalidates the product
> thesis, the safety boundary, or the Cloud Run eligibility contract. Only a
> mandated starter repo plausibly reaches that bar.

> [!tip] Escalate blockers
> If an unanswered question is blocking work, mirror it into [[07-Blocker-Log]]
> so it's visible on the board rather than buried here.

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[01-Event-Brief]] · [[02-Rules-and-Constraints]] · [[06-Hackathon-Compliance-Checklist]] · [[00-Triage]] · [[05-Decision-Log]] · [[07-Blocker-Log]]
