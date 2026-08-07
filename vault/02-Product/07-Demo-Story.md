---
title: Demo Story
tags:
  - product
status: active
---

# Demo Story

The narrative the demo tells. Beat-by-beat staging is in [[04-Demo-Script]];
this note is the story, not the stage directions.

> [!info] Source
> [[00-Source-of-Truth-PRD|PRD]] §12.2 (golden demo flow) and §12.3 (five-second comprehension).

## Setup

Who the viewer is watching, and what they care about: a transportation-safety
analyst reviewing a candidate conflict event, deciding whether this location
deserves further investigation. The judge is watching over that analyst's
shoulder.

## Beats

1. **Hook** — road-safety decisions are made from crash reports. Every one of
   them is evidence of harm that already happened.
2. **Problem made concrete** — the clip plays. Detected road users carry boxes
   and movement trails. A vehicle path and a vulnerable-road-user path converge.
3. **The turn** — the conflict marker appears, and the risk panel shows the
   visual conflict-risk proxy broken into proximity, path overlap, closing
   motion, and vulnerable-user weighting. The score is not a number from a black
   box; every part of it is on screen.
4. **Proof it generalises** — historical collision context for the location
   appears, sourced and visibly separated from what the clip showed. The
   presenter then runs live analysis against the configured NYC source — no
   longer an optional aside proving the pipeline isn't a mock, but a required P0
   step in its own right ([[00-Source-of-Truth-PRD|PRD]] §11.1), with an explicit `Insufficient
   temporal evidence` outcome shown when the source lacks enough evidence,
   rather than a forced alert.
5. **Close** — the explanation panel states the observations, the limitations,
   and the recommended human-review action. The system says what it does not
   know, and closes on the privacy boundary: no face recognition, plate
   recognition, identity inference, or automated enforcement ([[00-Source-of-Truth-PRD|PRD]] §12.2).

## What the audience should remember

One sentence: **see the risk before it becomes a crash statistic — with the
evidence, and the uncertainty, on screen.**

## The five-second test

Without narration, the UI must visibly answer:

- What objects are involved?
- Where is the possible conflict?
- How serious is the visual risk proxy?
- Why was it flagged?
- Is there enough temporal evidence to support a conflict result?
- Which NYC source is being analyzed, and when was it retrieved?
- Is this live/runtime output or a replay fixture?

> [!note] Real-feed analysis is now P0; captured replay is the guaranteed fallback
> [[00-Source-of-Truth-PRD|PRD]] §11.1 promotes real-feed analysis of a live NYC source from P2 to P0,
> superseding the v1.0 framing in [[00-Source-of-Truth-PRD|PRD]] §29 that live
> data is "a bonus beat, never a dependency." Per §10 principle 2, live analysis
> now proves the connection while captured replay proves the complete event
> workflow — captured replay stays the guaranteed evidence demonstration and the
> fallback if the live source or network fails (FR-015, §14; locked decision,
> §29). An `insufficient_temporal_evidence` live result is an explicit, valid
> outcome (§13, §29), not a beat allowed to fail.

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[04-Demo-Script]] · [[01-30-Second-Pitch]] · [[00-Source-of-Truth-PRD|PRD]] §29 · [[05-Demo-Reliability]]
