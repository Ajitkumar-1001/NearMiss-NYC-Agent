---
title: SpecKit Workflow
tags:
  - speckit
status: active
---

# SpecKit Workflow

Stock SpecKit is Specify → Clarify → Plan → Tasks → Analyze → Implement. On this
project the first two stages are already satisfied and must not be re-run.

## Where we actually are

Today is **Thursday 6 August 2026**. The event is Friday 7 August, 4:00–10:00 PM
ET and submission locks at 8:30 PM — organizer-page-derived per
[[00-Source-of-Truth-PRD|PRD]] §2.1, re-check after sign-in; a same-day organizer
update supersedes it and goes to [[05-Decision-Log]]. [[00-Source-of-Truth-PRD|PRD]]
§11.1 sets a readiness gate at **Thursday 6 August, 8:00 PM** — **tonight**: if the
deployment baseline or the captured evidence baseline is incomplete by then, all
optional product work stops until both are finished. Hours, not days.

**Entry point: `/plan`.** Not `/specify`, not `/clarify`.

> [!warning] The repo was restructured on 6 August — verify paths before trusting them
> `app/`, `demo/`, and `tests/` moved out of `vault/` to the repository root.
> The vault is now notes only. Paths below are relative to the repo root, not
> the vault. The move is only partly staged in git: the `demo/` and `tests/`
> renames are staged, `app/` is not.

What is actually built: 1,169 lines under `app/backend/nearmiss/` — `models.py`
221, `orchestrator.py` 284, `risk.py` 167, `config.py` 86, `sources.py` 55,
`providers/` 348, `__init__.py` 8. `orchestrator.py` already implements the
provider fallback ladder and exposes `readiness()` for FR-019; `config.py`
already resolves `FIXTURE_DIR = REPO_ROOT / "demo" / "fixtures"`; `sources.py`
is the FR-001 registry. Do not re-plan any of them. No network I/O and no HTTP
surface — but `providers/base.py:load_fixture` reads the filesystem,
`orchestrator.py` reads `ROBOFLOW_API_KEY`, `NYC_OPEN_DATA_APP_TOKEN`, and
`GEMINI_API_KEY` from the environment, and `config.py` resolves `REPO_ROOT` off
the filesystem.

The replay path now runs. `demo/fixtures/` holds `detections.json`,
`tracks.json`, and `context.json`; the pipeline completes end-to-end at score
84.3, severity `high`, mode `demonstration_replay`. The sequence is
**synthetic**, so principle 2 is satisfied mechanically but §11.1's
source-attributed capture is not.

What is not built, in the order it blocks: no FastAPI application and no endpoint
of any kind, so nothing serves `Health`, `readiness()`, or `sources.SOURCES`
(principle 1); no Dockerfile and nothing deployed; `app/frontend/` and `tests/`
hold only a README. Full gap list and the code-versus-PRD contradictions belong
in the plan, not here.

## Stages

| Stage | State | Command | Prompt | Output lands in |
|---|---|---|---|---|
| 1. Specify | **Satisfied — do not re-run.** [[00-Source-of-Truth-PRD\|PRD]] v2.1.0 (frozen, §31) is the spec. | *none, deliberately* | [[01-Specify-Prompt]] | — |
| 2. Clarify | **Satisfied — do not re-run.** §30 is the clarification register: every open question carries a decision deadline and a default when unresolved. | *none, deliberately* | [[02-Clarify-Prompt]] | §30; answers to [[05-Decision-Log]] |
| 3. Plan | **Done 6 Aug 12:50 PM.** Planned against the verified code state, not the notes. | `/plan` | [[03-Plan-Prompt]] | [[02-High-Level-Design]] |
| 4. Tasks | Ordered by principle 1 then principle 2. | `/tasks` | [[04-Tasks-Prompt]] | [[04-Task-Board]] |
| 5. Analyze | Cheap here, expensive on Friday. | `/analyze` | [[05-Analyze-Prompt]] | [[06-Risk-Register]] |
| 6. Implement | One task per invocation. | `/implement` | [[06-Implement-Prompt]] | `app/`, `demo/`, `tests/` |

Commands live in `.claude/commands/` in this vault and are **thin routers** —
each reads its prompt note and names its output note. The prompt notes remain
the single copy of the instruction; editing a command does not change a stage,
editing its prompt note does.

Specify and Clarify have **no command on purpose**. A command that cannot be
invoked is a stronger guard than a warning inside one.

Re-running Specify or Clarify would produce a second document claiming to be the
spec. [[00-Source-of-Truth-PRD|PRD]] §1 makes the PRD win over any conflicting
note, prompt, README, design, or implementation decision unless a newer approved
version explicitly supersedes it — so a second spec could never take effect. When
a clarification is needed, answer it against §30's default and record the answer
in [[05-Decision-Log]] — do not restate the spec.

## gstack skills

The registry is larger than this table — this is the subset that matters here.
Verify a skill resolves before relying on it in a time-boxed run.

| When | Skill |
|---|---|
| After the plan, before tasks | `/autoplan` (CEO + design + eng + DX, sequential, auto-decisions), or the individual `/plan-ceo-review`, `/plan-eng-review`, `/plan-design-review`, `/plan-devex-review` |
| Running `gcloud` and other destructive commands | `/careful` |
| A failure whose cause isn't obvious | `/investigate` |
| The six §11.3 surfaces, once they render | `/design-review`, then `/qa` (fixes) or `/qa-only` (report only), with `/browse` for the deployed URL |
| Before landing | `/review` |
| Landing and deploying | `/ship`, `/land-and-deploy`, then `/canary` |
| Scoping edits to one directory | `/freeze` / `/unfreeze` — note this is a tooling boundary, not the PRD's 7:00 PM feature freeze, which is a human rule |
| README and submission docs | `/document-release`, `/document-generate` |

## Rules

- Don't skip Clarify — but on this project it is already done. Ambiguity found at
  Implement still costs the most, so resolve it against §30 and the decision log
  rather than by guessing in code.
- Anything constraining later stages goes in [[00-Source-of-Truth-PRD|PRD]] §29
  (change control: §31). Pre-event freeze applies — see [[01-Constitution]].
- Principles in [[01-Constitution]] override the output of any stage.
- Verify before asserting. Every stage output states what the code does, what the
  PRD requires, or that something is not yet built — never blurs the three.

## Deviations from stock SpecKit

- Specify and Clarify are pre-satisfied by an external document. The stock
  assumption that SpecKit owns the spec does not hold here.
- Where the existing code contradicts the PRD, the plan must either fix the code
  or record the gap as a deviation in [[05-Decision-Log]]. Silently leaving it is
  a principle 7 violation.

---
Related: [[01-Constitution]] · [[00-Source-of-Truth-PRD|PRD]] · [[01-Workflow|gstack workflow]] · [[04-Task-Board]]
