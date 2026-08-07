---
title: Roboflow and Event Preparation Brief
tags:
  - event
status: draft
---

# Roboflow and Event Preparation Brief

> [!info] Role
> Named in [[00-Source-of-Truth-PRD|PRD]] §32.1 as the source register entry for event schedule,
> judging synthesis, Roboflow research, and prior-winner patterns. §2.1 cites this
> brief for seven event facts.

> [!warning] Provenance
> Derived from retrieved public registration material, not from an organizer
> statement made directly to this team. **Every time-sensitive detail below must
> be re-verified at kickoff.** Anything unconfirmed stays a `{{PLACEHOLDER}}`.

## Event schedule

As carried in [[00-Source-of-Truth-PRD|PRD]] §2.1, all marked *organizer-page-derived*:

| Fact | Value |
|---|---|
| Event | NYC Vision Hack v.2 — Live Feeds, Open Data |
| Date | Friday, 7 August 2026 |
| Window | 4:00–10:00 PM ET |
| Build period begins | ~5:15 PM |
| Submission locks | 8:30 PM |
| Demos begin | 8:45 PM |
| Team size | Up to four; solo builders allowed |
| Venue | {{VENUE}} |
| Check-in procedure | {{CHECKIN_PROCEDURE}} |

## Judging dimensions

Six dimensions, mapped to our proof in [[00-Source-of-Truth-PRD|PRD]] §2.3 and to our work in
[[03-Judging-Criteria-Map]]:

Working Demo · NYC Relevance · Usefulness or Insight · Technical Execution ·
Data Craft + Responsibility · Open Source

Weighting between dimensions is {{JUDGING_WEIGHTS}} — not stated in retrieved
material. Per-team demo duration is {{DEMO_DURATION}}.

## Co-hosts and sponsors

- **Veris AI** — co-host. Source-supported.
- A dedicated Veris prize track or mandatory Veris integration is
  **unverified — do not claim.** [[00-Source-of-Truth-PRD|PRD]] §2.4 treats Veris as a conditional
  evaluation-plane integration only.
- Other sponsors: {{SPONSOR_LIST}}. Attendee-specific credits: {{SPONSOR_CREDITS}}.

## Roboflow research

Findings behind the perception decisions locked in [[00-Source-of-Truth-PRD|PRD]] §29 and the stack
in §17:

- **RF-DETR** N/S/M/L weights are Apache-2.0 — clean for a permissive submission.
  RF-DETR **Plus** weights are restricted and must not be used without a license
  review.
- **Ultralytics YOLO** is AGPL-3.0. Excluded as the default because its
  obligations complicate an open-source submission.
- **Roboflow Workflows** and hosted/serverless inference are both viable runtime
  paths; preferred order is in §17.
- **`supervision`** (annotation, zones, normalized detections) and **ByteTrack /
  Roboflow `trackers`** (temporal association) are the supporting libraries.
- **Roboflow MCP server** and **Computer Vision Skills** are development-plane
  accelerators. §29 locks them out of the runtime.

Account creation and API-key validation are scheduled for Tuesday 4 August
([[00-Source-of-Truth-PRD|PRD]] §1.3 item 5) because Wednesday's evidence work depends on them.

## Prior-winner patterns

{{PRIOR_WINNER_PATTERNS}} — no retrieved source in hand. Do not present pattern
claims as organizer guidance.

## Re-verify at kickoff

- [ ] Schedule, especially the 8:30 PM lock
- [ ] Submission mechanism — {{SUBMISSION_MECHANISM}}, still unverified
- [ ] Per-team demo duration
- [ ] Final judge list
- [ ] Veris prize terms and required tooling
- [ ] Starter feeds and credentials actually handed out

Answers go to [[04-Organizer-Questions]]; anything that changes a requirement
goes to [[05-Decision-Log]] with timestamp and impact per [[00-Source-of-Truth-PRD|PRD]] §32.3.

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[01-Event-Brief]] · [[06-Hackathon-Compliance-Checklist]] · [[03-Sponsor-Resources]] · [[04-Organizer-Questions]] · [[04-Computer-Vision-Notes]]
