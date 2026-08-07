---
title: Rules and Constraints
tags:
  - event
status: active
---

# Rules and Constraints

> [!info] Filled from the PRD
> Anything that can disqualify us. Claim classes per [[00-Source-of-Truth-PRD|PRD]] §32.2:
> **[O]** organizer-stated · **[P]** platform constraint · **[R]** research
> finding · **[E]** our own execution rule · **[U]** unverified.
>
> §32.2 classifies *event* claims. A rule that comes from the PRD's own product
> requirements is not one of those classes, so it carries **[PRD]** and the
> section that mandates it.
>
> The operational checklist form of this note is
> [[06-Hackathon-Compliance-Checklist]]. This note states the rules; that one
> tracks compliance.

## Hard rules

| Rule | Class | Source | Consequence if broken |
|---|---|---|---|
| Deploy a publicly reachable agent on Google Cloud Run | [O] | §2.2 | **Submission is not hackathon-complete**, even if everything works locally |
| Cloud Run service reachable with no judge authentication | [O] | §2.2 | Judge cannot see it; treated as not deployed |
| Submission locked by 8:30 PM ET | [O] | §2.1 | Not submitted |
| Team of at most four | [O] | §2.1 | Ineligible |
| P0 shall not depend on a signed bulk-feed agreement | [R] | §18.3 | Approval outlasts the event; no working data path |
| Never represent fallback output as live analysis | [PRD] | §14 FR-016 | Truthfulness failure in front of judges |
| Never present the risk score as collision probability | [PRD] | §19, §23 | Overclaim; breaks the stated safety boundary |
| No identity recognition or biometric processing | [PRD] | §29, §23 | Breaks the privacy commitment |

## Code provenance

Answered by [[00-Source-of-Truth-PRD|PRD]] §11.1 and §1.3 item 4, not by an organizer statement.

- **Can we use pre-existing code?** Yes — §11.1 *requires* it. The deployment
  baseline, captured evidence, and `vision-conflict-analytics` package are
  explicitly pre-event artifacts, not event-day build tasks.
- **When may work begin?** Already begun. The build period starting ~5:15 PM is
  the *event* window, not a restriction on prior work.
- **The obligation that comes with it:** §1.3 item 4 requires the public README
  to separate pre-event scaffolding, reusable components, fixtures, and
  event-day work. Draft: [[09-Preexisting-Code-Disclosure]]. Tag the boundary
  commit **before** the window opens.
- **Open-source license requirements?** Apache-2.0 or MIT, per §26. §17 excludes
  AGPL-3.0 Ultralytics YOLO from the default implementation for exactly this
  reason, and excludes restricted RF-DETR Plus weights without a license review.

> [!warning] §30 reconfirms the pre-existing-code policy at kickoff
> The pre-existing-code policy has a Thursday 6 August deadline **and** a
> reconfirm-at-kickoff instruction. Default if unresolved: disclose everything,
> and separate pre-event from event-day commits.

## Data and API constraints

[[00-Source-of-Truth-PRD|PRD]] §18 is the approved data-source policy. Candidate sources go in
[[02-Live-Feeds]]; chosen datasets in [[01-Datasets]].

**Permitted primary sources**, in priority order (§18.1): organizer starter-pack
live camera → publicly reachable NYC DOT still-image endpoint with polite
caching → 511NY REST camera with a self-service developer key → phone/USB webcam
physically in NYC as an emergency fallback.

**Permitted enrichment** (§18.2): NYC Open Data Socrata collision and 311
datasets; 511NY REST incidents/roadwork; MTA GTFS-realtime at P2.

**Prohibited at P0** (§18.3):

- NYC DOT bulk feeds requiring a signed data-sharing agreement
- 511NY bulk feeds requiring a Developer Access Agreement
- Third-party commercial webcam scraping
- Any undocumented endpoint without a source/usage note
- Any source whose availability cannot be tested before the demo

**Recorded vs live** — both are required, and both must be labelled.
[[ADR-006-Real-Source-P0-with-Captured-Fallback]] makes real-source analysis P0
*and* keeps the captured replay mandatory. §14 FR-016 requires the active
processing mode to be visible. A repeated still frame must never be treated as
new temporal evidence (§18.4) — see [[Source-Temporal-Sufficiency]].

**Attribution** (§18.5): README and dashboard must state source name, category,
retrieval method, whether content is current/cached/captured/fixture,
attribution, known limitation, and retrieval timestamp.

## Privacy

[[00-Source-of-Truth-PRD|PRD]] §23 governs; methodology in [[05-Safety-Methodology]], implementation
in [[10-Responsible-AI]].

- No identity recognition, no biometric processing
- Historical correlation must never be presented as causal proof
- Uncertainty and evidence sufficiency stated explicitly, not implied
- Output is a human-review recommendation, not automated enforcement

## Practical limits

- **Presentation length:** {{PITCH_MINUTES}} min — per-team demo duration is
  **unverified** (§2.1). [[01-30-Second-Pitch]] and [[02-2-Minute-Pitch]] both
  exist so either can be delivered.
- **Demo hardware / network:** {{DEMO_ENV}} — assume hostile venue wifi. That
  assumption is why the captured path must run with the network disabled
  ([[05-Demo-Reliability]]).

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[01-Event-Brief]] · [[06-Hackathon-Compliance-Checklist]] · [[04-Organizer-Questions]] · [[08-Definition-of-Done]] · [[09-Preexisting-Code-Disclosure]]
