---
title: ADR-004 Single Orchestrated Pipeline
tags:
  - adr
status: active
---

# ADR-004 — Single Orchestrated Pipeline

## Status

Accepted — [[PRD]] §29, approved for v2.0.

## Context

Two separate pressures point at the same shape, and this ADR covers both.

**Against distributed services.** A hackathon has no operational team. Every
network hop between stages is another failure mode to debug at 3am and another
thing that can be misconfigured at deploy time. [[PRD]] §25 no longer carries a
prohibited-time-sinks list in v2.0 — that section is now the event-day
execution timeline; the standing constraints are §9's non-goal against
production-grade streaming infrastructure and §11.1's single-service P0 scope.
§21 states outright that a queue is not required — synchronous processing is
acceptable (NFR-004, §15), which fits inside the 60 s P1 short-sequence budget
(NFR-006, §15).

**Against a multi-agent council.** The fashionable alternative is a set of LLM
agents that debate the event. [[PRD]] §9 makes building one an explicit
non-goal ('Build a multi-agent council'); v2.0 no longer carries the separate
before-P0 prohibition list that used to sit at §25 (see above). It also
inverts §10 principle 3 — evidence before explanation, no longer principle 1
as in v1.0. The risk engine is no longer described by a standalone '§16.5'
subsection — it is the Conflict Risk Engine node in the §16 architecture
diagram — and is specifically required to avoid language-model dependence: §8
(G5) states the LLM/VLM must not originate the risk score; agents deciding
severity would put a nondeterministic component on the guaranteed path.

§16.1's Mandatory agent service list now names the shape that satisfies
both — the standalone '§16.8' component-responsibilities subsection no longer
exists in v2.0: one FastAPI/Cloud Run service that owns the source,
perception, risk, context, and explanation adapters, applies the FR-015
fallback ladder and FR-016 processing-mode disclosure (§14), and returns one
normalized event report (§20).

## Decision

One orchestrated pipeline process rather than independent services communicating over a network.

The orchestrator is also the single owner of the FR-015 provider-fallback
ladder ([[PRD]] §14 — the standalone §17 fallback ladder section no longer
exists in v2.0) and of the `processing_mode` value the UI displays (FR-016,
§14). Language models explain evidence the pipeline has already produced; they
never produce it.

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
| A service per pipeline stage | No distinct prohibited-time-sinks list remains at §25 in v2.0 (see Context); re-anchored to §9 non-goals and §11.1's single-service P0 scope. Network hops inside a 60 s budget with no ops team. |
| Multi-agent LLM council | Explicit non-goal (§9); nondeterministic, and inverts evidence-before-explanation (§10 principle 3) |
| Background job queue with polling | §21 says a queue is not required; adds infrastructure the demo does not need |

---
Related: [[PRD]] · [[02-High-Level-Design]] · [[03-Data-Flow]] · [[08-Deployment]] · [[09-Observability]] · [[ADR-009-Cloud-Run-Deployment]] · [[00-ADR-Index]]
