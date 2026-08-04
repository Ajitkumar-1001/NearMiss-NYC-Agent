---
title: Problem Statement
tags:
  - product
status: active
---

# Problem Statement

> [!info] Source
> [[PRD]] §4.

## The problem

Road-safety decisions are frequently based on lagging indicators — reported
crashes, injuries, fatalities, and complaints. Those records are valuable, but
every one of them describes harm that has already occurred.

Public street-camera footage may contain earlier indicators of unsafe
conditions:

- Vehicles and cyclists repeatedly converging at the same turn
- Pedestrians entering conflict zones while vehicles continue moving
- Turning vehicles crossing vulnerable-road-user paths
- Rapidly decreasing road-user separation
- Occlusions or street geometry that repeatedly create dangerous interactions

That footage is not being read at scale.

## Who has it

Detailed in [[03-Users-and-Jobs]].

## Evidence

Claims here need a source. Unsourced numbers are worse than no numbers — a judge
will ask.

| Claim | Source | Confidence |
|---|---|---|
| {{CLAIM}} | {{SOURCE}} | low |

> [!caution] This table is deliberately still empty
> [[PRD]] §4 states the problem qualitatively and cites nothing. Rather than
> invent a citation, the placeholder stays until a real source is found. Nothing
> in [[02-2-Minute-Pitch]] may quote a number that does not trace to a filled row
> here with a value in the Actual column of [[06-Success-Metrics]].

## Why it's unsolved today

Manually reviewing large amounts of footage is slow, expensive, inconsistent,
and difficult to scale. Standard object-detection dashboards count objects, but
they do not provide event-level reasoning, historical context, transparent risk
factors, or actionable evidence.

Prior art and its gaps: [[03-Prior-Art]].

## Why now

- [ ] What changed — data availability, model capability, cost?

> [!todo] The PRD does not answer this
> [[PRD]] §4 establishes the gap but not the timing. Fill this before the pitch —
> it is the question that follows "why hasn't someone done this already".

---
Related: [[PRD]] · [[01-Project-Overview]] · [[03-Users-and-Jobs]] · [[03-Prior-Art]] · [[06-Success-Metrics]]
