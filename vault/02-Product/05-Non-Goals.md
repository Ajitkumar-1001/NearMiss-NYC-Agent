---
title: Non-Goals
tags:
  - product
status: active
---

# Non-Goals

Explicitly out of scope. Writing these down stops the same debate recurring.

> [!info] Source
> [[PRD]] §9 (non-goals). PRD v2.0 no longer restates a prohibited-time-sinks list
> at old §25 — see the "Tempting but out" note below — and v1 §28 (future roadmap)
> is removed and not restated anywhere in v2.0.0, so the R1/R2/R3 horizons in the
> Revisit column below are vault-internal labels only, not currently sourced from
> the PRD.

| Not doing | Why | Revisit when |
|---|---|---|
| Authentication / user accounts | [[PRD]] §29 | Post-hackathon |
| Monitoring every NYC camera | One clip, one event, done properly beats breadth | R2 — multiple camera ingestion |
| Depending on a signed NYC DOT or 511NY bulk-feed agreement | Approved sources are self-service or organizer-provided — [[PRD]] §18.3 | Post-hackathon |
| Scraping commercial webcam sources without clear permission | Usage terms must clearly permit the use — [[PRD]] §9 | Never |
| Guaranteed real-time citywide operation | No operational team, no streaming infrastructure | R3 — city-scale batch analysis |
| Training a new foundation or detection model | Consumes the entire time box; off-the-shelf detection is sufficient | Post-hackathon |
| Training a custom detector before P0 is complete | Off-the-shelf Roboflow RF-DETR is sufficient for P0 — [[PRD]] §17 | Post-hackathon |
| Scientifically validated time-to-collision | The camera is uncalibrated — [[PRD]] §29 | R1 — calibrated camera geometry |
| Identifying people, plates, or drivers | [[PRD]] §29 | Never |
| Autonomous enforcement or emergency-response decisions | The output is a candidate event for human review, not a verdict | Never |
| A complex multi-agent council | [[PRD]] §29 | Post-hackathon |
| Production-grade streaming infrastructure | P2 at most, and only after P0 is frozen | R2 |
| Guaranteeing every flagged event is a true near-miss | It is a visual proxy; precision is unmeasured | R1 — precision/recall against human labels |
| Recommending definitive civil-engineering changes | Requires human analysis we are not qualified to replace | R3 — formal validation with transportation experts |

## Tempting but out

These are the ones that will get suggested at hour 20. PRD v2.0 replaced the old
§25 prohibited-time-sinks list with a concrete event-day schedule at [[PRD]] §27.2
(whose 8:00 PM scope-freeze step adds no new core feature); the durable
prohibition on these items **before P0 is complete** is re-anchored to [[PRD]] §9
(non-goals) and §11.1 (P0 scope) — not because they are bad ideas, but because
each one has eaten a hackathon before:

- Authentication
- Persistent user database
- Multi-agent orchestration
- Model training
- Camera calibration research
- Multi-camera dashboards
- Mobile application
- Complex queues or microservices
- Unnecessary design-system work

> [!warning] Scope creep shows up as "it's only a small change"
> If a new capability is genuinely worth it, it goes through [[05-Decision-Log]]
> and comes out of [[03-Scope-Ladder]] — something else gets cut.

---
Related: [[PRD]] · [[04-MVP-Scope]] · [[03-Scope-Ladder]] · [[05-Decision-Log]]
