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
> [[PRD]] §11.2 (golden demo flow) and §11.3 (five-second comprehension).

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
   presenter can then switch to runtime analysis to prove the pipeline is not a
   static mock.
5. **Close** — the explanation panel states the observations, the limitations,
   and the recommended human-review action. The system says what it does not
   know.

## What the audience should remember

One sentence: **see the risk before it becomes a crash statistic — with the
evidence, and the uncertainty, on screen.**

## The five-second test

Without narration, the UI must visibly answer:

- What objects are involved?
- Where is the possible conflict?
- How serious is the visual risk proxy?
- Why was it flagged?
- Is this live/runtime output or a replay fixture?

> [!note] The demo runs on fixtures
> Per [[ADR-001-Deterministic-Demo-First]], the story must hold with recorded
> data. Live data is a bonus beat, never a dependency. Beat 4's runtime switch is
> the only beat allowed to fail without breaking the story.

---
Related: [[PRD]] · [[04-Demo-Script]] · [[01-30-Second-Pitch]] · [[ADR-001-Deterministic-Demo-First]] · [[05-Demo-Reliability]]
