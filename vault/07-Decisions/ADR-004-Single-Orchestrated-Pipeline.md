---
title: ADR-004 Single Orchestrated Pipeline
tags:
  - adr
status: active
---

# ADR-004 — Single Orchestrated Pipeline

## Status

Accepted — [[PRD]] §27, approved for v1.0.

## Context

Two separate pressures point at the same shape, and this ADR covers both.

**Against distributed services.** A hackathon has no operational team. Every
network hop between stages is another failure mode to debug at 3am and another
thing that can be misconfigured at deploy time. [[PRD]] §25 lists complex queues
and microservices as prohibited time sinks, and §19 states outright that a job
queue is not required — synchronous processing is acceptable inside the 60 s
NFR-003 budget.

**Against a multi-agent council.** The fashionable alternative is a set of LLM
agents that debate the event. [[PRD]] §8 makes building one an explicit non-goal
and §25 prohibits multi-agent orchestration before P0. It also inverts §9
principle 1 — evidence before explanation. The risk engine (§16.5) is
specifically required to avoid language-model dependence; agents deciding
severity would put a nondeterministic component on the guaranteed path.

§16.8 already names the shape that satisfies both: one orchestrator that
executes the pipeline, applies the fallback ladder, records the active
processing mode, and returns one normalized event report.

## Decision

One orchestrated pipeline process rather than independent services communicating over a network.

The orchestrator is also the single owner of the [[PRD]] §17 fallback ladder and
of the `processing_mode` value the UI displays. Language models explain evidence
the pipeline has already produced; they never produce it.

## Consequences

**Positive**
- One deployable unit, matching the Cloud Run target in
  [[ADR-009-Cloud-Run-Deployment]].
- One place where the fallback ladder and mode disclosure live, rather than
  logic smeared across services.
- A synchronous request fits the 60 s budget with no queue, no worker, no broker.
- Deterministic and reproducible, which is what [[ADR-001-Deterministic-Demo-First]]
  needs from the guaranteed path.

**Negative**
- No independent scaling of the vision stage, which is the expensive one.
- A slow provider call blocks the whole request.
- Single process is a single failure domain.

**Accepted trade-off**
- Coupling is accepted in exchange for one thing to deploy and one place to
  debug. At this scale, that is the correct side of the trade.

## Alternatives considered

| Alternative | Why not |
|---|---|
| A service per pipeline stage | Prohibited by §25; network hops inside a 60 s budget with no ops team |
| Multi-agent LLM council | Explicit non-goal (§8); nondeterministic, and inverts evidence-before-explanation |
| Background job queue with polling | §19 says a queue is not required; adds infrastructure the demo does not need |

---
Related: [[PRD]] · [[02-High-Level-Design]] · [[03-Data-Flow]] · [[08-Deployment]] · [[09-Observability]] · [[ADR-009-Cloud-Run-Deployment]] · [[00-ADR-Index]]
