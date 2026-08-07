---
title: Design Review
tags:
  - gstack
status: active
---

# Design Review

> [!important] There is nothing to review yet
> `app/frontend/` contains only `README.md`. None of the six judge-facing
> surfaces required by [[00-Source-of-Truth-PRD|PRD]] §11.3 exist. `/design-review`
> operates on a built UI and has no target today, so this note is parked.
>
> Running it now would produce invented findings, which is worse than none.
> `/plan-design-review` is the skill that applies to a plan; run that instead if
> a design opinion is wanted before the UI exists.

## Status, 4 August

All six judge-facing surfaces named in [[00-Source-of-Truth-PRD|PRD]] §11.3 —
that section is authoritative for their names and contents — are **not built**.
`app/frontend/` holds only `README.md`. Zero of six.

The only design-adjacent finding available today is the absence itself, and it
is already recorded as finding 4 in [[02-Product-Review]] and finding 9 in
[[03-Engineering-Review]]. It is not duplicated here.

## Checklist — run once a UI renders

- [ ] Is the primary action obvious within three seconds?
- [ ] Does the hierarchy match what the demo needs to emphasise? → [[04-Demo-Script]]
- [ ] Is it legible from the back of a room / on a projector?
- [ ] Consistent spacing, type scale, and colour?
- [ ] Any interaction slow enough to break the demo's rhythm?
- [ ] Does it look generic? Specificity reads as care.
- [ ] Do all six §11.3 surfaces render, and is each one identifiable without narration?
- [ ] Is every fallback visibly labelled as a fallback? (§26.2)

## Findings

None yet. Populate after the first `/design-review` pass against a running UI.

| # | Finding | Severity | Action | Status |
|---|---|---|---|---|
| — | — | — | — | — |

> [!note] When this unparks
> Earliest realistic window is Thursday 6 August, after the deployment and
> captured evidence baselines are green. If they are not green at the 8:00 PM
> readiness gate, [[00-Source-of-Truth-PRD|PRD]] §11.1 stops visual redesign
> outright — this note stays parked and that is the correct outcome.
>
> Projector contrast is the one that bites — check it on the real screen if at
> all possible.

---
Related: [[01-Workflow]] · [[04-Demo-Script]] · [[05-QA-Checklist]]
