---
title: Non-Goals
tags:
  - product
status: active
---

# Non-Goals

Explicitly out of scope. Writing these down stops the same debate recurring.

> [!info] Source
> [[PRD]] §8 (non-goals) and §25 (prohibited time sinks). Roadmap horizons in the
> Revisit column refer to [[PRD]] §28.

| Not doing | Why | Revisit when |
|---|---|---|
| Authentication / user accounts | [[ADR-005-No-Authentication]] | Post-hackathon |
| Monitoring every NYC camera | One clip, one event, done properly beats breadth | R2 — multiple camera ingestion |
| Guaranteed real-time citywide operation | No operational team, no streaming infrastructure | R3 — city-scale batch analysis |
| Training a new foundation or detection model | Consumes the entire time box; off-the-shelf detection is sufficient | Post-hackathon |
| Scientifically validated time-to-collision | The camera is uncalibrated — [[ADR-002-Visual-Conflict-Proxy]] | R1 — calibrated camera geometry |
| Identifying people, plates, or drivers | [[ADR-006-No-Identity-Recognition]] | Never |
| Autonomous enforcement or emergency-response decisions | The output is a candidate event for human review, not a verdict | Never |
| A complex multi-agent council | [[ADR-004-Single-Orchestrated-Pipeline]] | Post-hackathon |
| Production-grade streaming infrastructure | P2 at most, and only after P0 is frozen | R2 |
| Guaranteeing every flagged event is a true near-miss | It is a visual proxy; precision is unmeasured | R1 — precision/recall against human labels |
| Recommending definitive civil-engineering changes | Requires human analysis we are not qualified to replace | R3 — formal validation with transportation experts |

## Tempting but out

These are the ones that will get suggested at hour 20. [[PRD]] §25 prohibits all
of them **before P0 is complete** — not because they are bad ideas, but because
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
