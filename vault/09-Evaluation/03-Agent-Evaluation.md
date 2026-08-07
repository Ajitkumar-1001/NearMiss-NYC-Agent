---
title: Agent Evaluation
tags:
  - evaluation
status: active
---

# Agent Evaluation

How we judge the agent/orchestration layer's output quality.

"Agent" here means the orchestrated pipeline's **output**, and in practice that
means the structured explanation. There is no autonomous LLM agent at P0:
`GeminiExplanation.explain` (`nearmiss/providers/explanation.py:50`) raises
`ProviderUnavailable` unconditionally (`:54-57`), and the live path is
`TemplateExplanation` (`explanation.py:60`), which is deterministic and fully
implemented.

> [!important] This evaluation is runnable today
> `TemplateExplanation.explain` takes a `Candidate`, an optional
> `HistoricalContext`, and a `Severity` — all constructible in memory. It reads
> no fixture file and needs no HTTP service, so unlike [[00-Source-of-Truth-PRD|PRD]]
> §24.2 and §24.3 it is not blocked by the empty `demo/fixtures/` or by the
> absent FastAPI app.
>
> It is not the only one. §24.4 against `RiskEngine` (`risk.py:85`) is equally
> runnable — all eight cases, since `score_pair`/`evaluate` take hand-built
> `Track` objects and read no files — and parts of §24.6 run too. See
> [[01-Test-Strategy]] for the map and [[02-Test-Cases]] for the cases.
>
> Run it before the **Thursday 6 August, 8:00 PM America/New_York** readiness
> decision in §27.1, which governs the §11.1 baseline.

## What "good" means

[[00-Source-of-Truth-PRD|PRD]] §24.5 already defines it, in five criteria. That
list **is** the definition — there is no second rubric to invent.

| # | §24.5 criterion | What it means for this code | Where it lands |
|---|---|---|---|
| 1 | Reference supplied evidence only | Every observation traces to an argument passed into `explain` — the `Candidate` or the `HistoricalContext` | `explanation.py:71-102` |
| 2 | Avoid identity, legal, and metric claims | Track IDs and class names only; separation stated as image-space px | `explanation.py:72-77` |
| 3 | Include at least one limitation | `BASELINE_LIMITATIONS` is unconditional | `explanation.py:30`, `models.py:162` `limitations: Field(min_length=1)` |
| 4 | Recommend human review when appropriate | §19.3: every high-severity candidate recommends review, and nothing auto-contacts enforcement | `explanation.py:113` |
| 5 | Produce valid schema-constrained output | The `Explanation` must populate a `models.Event` that validates | `models.py:147` `Event` |

§14 FR-014 names the eight elements the provider must return; §23 (items 6-10)
is the responsibility floor those criteria enforce. Cite them; don't restate
them here.

## Method

- [ ] Fixed evaluation set of hand-built `Candidate` objects, committed
      alongside the cases
- [ ] Rubric: §24.5's five criteria, scored **pass/fail each**. An explanation
      passes only when all five pass.
- [ ] Scored by: **a human reading the output against the five criteria.**
      There is no automated judge, and building one is out of scope — the
      criteria are short, the template is deterministic, so one careful read
      per case is the whole method.
- [ ] Same inputs every run, so scores are comparable

The `Candidate` inputs are hand-built, not drawn from `demo/fixtures/` — that
directory holds only `README.md`, so a fixture-drawn set is not available yet.
Determinism comes from the template being deterministic and the inputs being
fixed, not from seeding — there is no stochastic component to seed.

The runner lives in [[01-Test-Strategy]]. Don't restate it here.

### Cases

[[02-Test-Cases]] §B owns the case list: cases 9-13, one per §24.5 criterion,
with input, expected result, `Automated?`, and status columns. Score against
those rows. Nothing there has been executed either, so every "expected" in that
note is what §24.5 requires, not what was observed.

What this rubric adds on top of the case list:

| Scoring note | Applies to |
|---|---|
| Score `context=None` and context-present as two separate reads of criterion 3 — the situational limitation differs between them (`explanation.py:96-110`) | case 11 |
| Criterion 3's two unconditional limitations answer two different requirements: the "not a crash probability" caveat is §23.6 and FR-010's closing line; the uncalibrated / image-space caveat is §19.1's "not a calibrated time-to-collision metric". Score them separately | case 11 |
| Criterion 2 is a negative check — read for names, plates, fault, speed, and real-world distance, and confirm the only units in the text are image-space `px` | case 10 |
| Severity `low` is unreachable through the orchestrator (`orchestrator.py:150` `_severity` returns only `high` or `medium`), so case 12's two rows cover the whole reachable range. A low-severity explanation can still be scored by calling `TemplateExplanation.explain` directly | case 12 |

> [!warning] One divergence this rubric adds
> **FR-017 wording drift.** FR-017 fixes the no-event sentence as ending
> "…in the available evidence." `orchestrator.py:183` returns "…in this clip."
> Same meaning, different string; a literal check fails. Not a §24.5 criterion —
> it belongs to whoever writes [[02-Test-Cases]] case 22 — but it is agent output
> text, so score it here when reading no-event output.

> [!note] How to attribute the `explanation.py:98` defect
> [[02-Test-Cases]] case 9 is expected to fail. Attribute it to §23.10 only —
> "Observed evidence, derived metrics, public context, and generated explanation
> remain separate" — not to §24.5's "reference supplied evidence only". The
> historical-collision sentence is built from the `context` argument passed into
> `TemplateExplanation.explain` (`explanation.py:66`), so it **is** supplied
> evidence; the defect is the merge into `observations`, not the source. The
> `Event` also carries a separate `historical_context` field, so the text lands
> in the wrong bucket and is duplicated. Related gap: FR-014 lists a
> "historical-context summary" element the `Explanation` dataclass
> (`explanation.py:19`) has no field for.

## Results

No runs yet. Do not fill a row from a read-through — only from an executed case.

| Run | Date | Eval set | Score | Notes |
|---|---|---|---|---|

## Failure modes seen

No runs yet, so nothing has been *seen*. The entries in the callouts above are
code-read predictions and belong there, not here.

| Mode | Frequency | Mitigation |
|---|---|---|

## Notes

- Code comments in `explanation.py` and `models.py` cite `§21.6`, `§21.7`,
  `§21.8`, `FR-010`, and `FR-011` for explanation rules. In the current PRD,
  §21 is API requirements, limitations are §23.7, human review is §19.3 /
  §23.8, and the explanation requirement is FR-014. Stale citations, not a
  behaviour defect — worth a pass if there is time after the gate.
- Stale-docstring claims across the backend are inventoried in
  [[01-Test-Strategy]]. Don't re-list them here.

---
Related: [[06-Success-Metrics]] · [[04-Vision-Evaluation]] · [[01-Test-Strategy]] · [[02-Test-Cases]]
