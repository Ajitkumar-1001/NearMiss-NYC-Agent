---
title: Event Brief
tags:
  - event
status: active
---

# Event Brief

> [!info] Filled from the PRD
> Everything below is carried from [[00-Source-of-Truth-PRD|PRD]] frontmatter and §2.1, where it is
> marked **organizer-page-derived** — retrieved from public registration
> material, not stated to us directly. **Re-check the time-sensitive rows at
> kickoff.** Research provenance is in [[05-Roboflow-and-Event-Preparation-Brief]].

## At a glance

- **Event:** NYC Vision Hack v.2 — Live Feeds, Open Data
- **Date:** Friday, 7 August 2026, 4:00–10:00 PM ET
- **Venue:** {{VENUE}} — not stated in any retrieved source
- **Track / theme:** Live feeds and open data. Co-hosted with Veris AI.
- **Team size limit:** up to four; solo builders allowed
- **Submission locks:** 8:30 PM ET
- **Demos begin:** 8:45 PM ET

### Timeline

| Time | What |
|---|---|
| 4:00 PM | Doors / kickoff |
| ~5:15 PM | Build period begins |
| 7:00 PM | **Our** hard feature freeze ([[00-Source-of-Truth-PRD|PRD]] §29 — self-imposed, not an organizer time) |
| 8:00–8:15 PM | **Our** protected contingency window |
| 8:30 PM | Submission locks |
| 8:45 PM | Demos begin |

Our own hour-by-hour plan is [[02-Time-Box-Plan]]; the runbook is
[[01-Hackathon-Runbook]].

## What they're asking for

A working system on **live feeds and NYC open data**, deployed publicly. The
theme is in the event's own title; [[00-Source-of-Truth-PRD|PRD]] §2.3 maps it to what we build.

Our answer: [[01-Project-Overview]].

## Deliverables

The one that disqualifies:

> **A publicly reachable Google Cloud Run agent.** [[00-Source-of-Truth-PRD|PRD]] §2.2 — the only
> stated eligibility gate. Missing it means the submission is not
> hackathon-complete even if everything runs locally.

Everything else, from [[00-Source-of-Truth-PRD|PRD]] §26. Full checklist lives in
[[06-Hackathon-Compliance-Checklist]] — don't duplicate it here.

- [x] Public repository — required
- [x] Deployed Cloud Run URL — required, and the gate
- [x] README with setup, architecture, demo, provenance, limitations
- [x] Permissive license (Apache-2.0 or MIT)
- [x] Privacy statement and source policy
- [x] Prepared-code disclosure → [[09-Preexisting-Code-Disclosure]]
- [x] Fallback recording as a backup artifact — not the primary demo
- [ ] Video? Length limit? — **{{VIDEO_REQUIREMENT}}, unverified**
- [ ] Slide deck? Format? — **{{DECK_REQUIREMENT}}, unverified**

## Judging

Six dimensions ([[00-Source-of-Truth-PRD|PRD]] §2.3), mapped to our proof in
[[03-Judging-Criteria-Map]]:

Working Demo · NYC Relevance · Usefulness or Insight · Technical Execution ·
Data Craft + Responsibility · Open Source

Relative weighting is {{JUDGING_WEIGHTS}} — not stated in retrieved material.

## Still unverified

[[00-Source-of-Truth-PRD|PRD]] §2.1 flags these explicitly. **Do not present any of them as a rule or
a benefit.** They are the kickoff questions in [[04-Organizer-Questions]].

- Exact submission mechanism
- Per-team demo duration
- Final judge list
- Veris prize terms — a Veris prize track is **unverified; do not claim**
- Attendee-specific sponsor credits

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[02-Rules-and-Constraints]] · [[03-Sponsor-Resources]] · [[04-Organizer-Questions]] · [[05-Roboflow-and-Event-Preparation-Brief]] · [[06-Hackathon-Compliance-Checklist]] · [[01-Project-Overview]]
