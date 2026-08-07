---
title: gstack Workflow
tags:
  - gstack
status: active
---

# gstack Workflow

How review skills are used during the build. Today is **Thursday 6 August** and
the §11.1 readiness gate is **tonight at 8:00 PM**; the event is Friday 7 August
4:00–10:00 PM ET, submission locks 8:30 PM. Every skill below was checked as
real and invokable — do not
substitute a name that sounds plausible. The registry is larger than this table,
so this is not the full set; verify a skill resolves before relying on it inside
a time-boxed run.

| Stage | Skill | Note |
|---|---|---|
| Product sanity | `/plan-ceo-review` | [[02-Product-Review]] |
| Engineering sanity | `/plan-eng-review` | [[03-Engineering-Review]] |
| Design pass | `/design-review` | [[04-Design-Review]] |
| QA sweep | `/qa` | [[05-QA-Checklist]] |
| Pre-landing diff review | `/review` | Runs before anything lands on `main` |
| Land the change | `/ship` | Merges base, runs tests, bumps VERSION, opens PR |
| Deploy it | `/land-and-deploy` | The Cloud Run push — see [[08-Deployment]] |
| Watch the deploy | `/canary` | Post-deploy monitoring of the live revision |
| Debug under pressure | `/investigate` | Root cause first; no guess-patching on Friday |

Two more worth knowing:

- `/autoplan` runs the CEO, design, eng, and DX plan reviews sequentially with
  auto-decisions. That was the three-days-out answer; with the readiness gate
  hours away, four sequential reviews likely cost more than they return.
- `/qa-only` reports without fixing. Use it after the 7:00 PM Friday code freeze
  in [[00-Source-of-Truth-PRD|PRD]] §27.2, when finding a bug is allowed but
  changing code is not.

SpecKit stages (`/specify`, `/clarify`, `/plan`, `/tasks`, `/analyze`,
`/implement`) drive the build itself; see [[02-Workflow]]. The gstack reviews
wrap them.

## When to run each

**Plan reviews — now compressed.** `/autoplan` runs four reviews sequentially;
with the readiness gate hours away that is likely more process than the window
affords. Prefer `/plan-eng-review` alone, or skip to `/review` on the first
landing diff.
The plan under review is [[00-Source-of-Truth-PRD|PRD]] §27.1 against the state
recorded in [[03-Engineering-Review]]: no FastAPI application, no endpoint, and
`demo/fixtures/` holding only `README.md`. These reviews exist to force the
question of whether the Tuesday and Wednesday critical path is achievable — not
to bless it.

**Cadence decided 6 August: batched per baseline, not per task.** With the
readiness gate hours away, `/review` → `/ship` → `/land-and-deploy` → `/canary`
on every one of ~10 tasks is 2.5–3 hours of pure ceremony. Every gate still
runs; they batch:

| Gate | Frequency tonight |
|---|---|
| `/review` | Once per baseline — deployment, then captured evidence |
| `/land-and-deploy` + `/canary` | Once per actual deploy (~2–3) |
| `/qa` | Once, before the 8:00 PM readiness gate |
| `/design-review` | Only once the six surfaces render |
| Plan reviews (`/autoplan` et al.) | Cut — see the compression note above |

Batching is a scope cut and therefore a decision: log it in [[05-Decision-Log]]
per [[03-Scope-Ladder]]'s rule that cutting is a decision, not a failure.

[[00-Source-of-Truth-PRD|PRD]] §2.2 is a *deployed* gate; code that is merged
but not deployed clears nothing — so `/land-and-deploy` never batches away.

**Design review — not yet.** `app/frontend/` contains only `README.md`. None of
the six judge-facing surfaces in [[00-Source-of-Truth-PRD|PRD]] §11.3 exist, so
`/design-review` has nothing to look at. Run `/plan-design-review` now against
the surface list if a review is wanted this early; run `/design-review` only
once a UI renders. [[04-Design-Review]] is parked until then.

**Thursday 6 August — QA sweep before the 8:00 PM readiness gate.** Run `/qa`
against [[05-QA-Checklist]] and [[05-Demo-Reliability]] with enough time left to
act on the result. [[00-Source-of-Truth-PRD|PRD]] §11.1's readiness rule is
hard: if the deployment baseline or the captured evidence baseline is incomplete
at 8:00 PM Thursday, all optional product work stops until both are finished.
The sweep is what tells you which side of that rule you are on.

**Friday 7 August — QA sweep again before submission.** Re-run the checklist
against the deployed Cloud Run URL, not localhost, and check it against the
§26.2 submission gate. After the 7:00 PM freeze, switch to `/qa-only`.
`/investigate` is the only debugging path that should be used inside the
4:00–8:30 PM window.

> [!note] Record what the reviews caught
> Findings land in [[02-Product-Review]], [[03-Engineering-Review]], and
> [[04-Design-Review]]. Which reviews actually ran, and when, goes in
> [[Progress-Log]]. Decisions coming out of them go to [[05-Decision-Log]], not
> into the PRD — [[00-Source-of-Truth-PRD|PRD]] §31 freezes that document after
> today.

---
Related: [[02-Product-Review]] · [[03-Engineering-Review]] · [[04-Design-Review]] · [[05-QA-Checklist]]
