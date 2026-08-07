---
title: Decision Log
tags:
  - execution
status: active
---

# Decision Log

The event-day landing zone. [[00-Source-of-Truth-PRD|PRD]] §31's pre-event freeze routes every
implementation choice, package pin, source selection, organizer answer, and bounded scope cut here
instead of into a PRD revision. §32.3 additionally requires that organizer updates received during
the event be captured here **with timestamp and impact**.

> [!warning] Add the row first, argue later
> One line, five cells, ten seconds. An unrecorded organizer answer is the thing that breaks the
> submission at 8:15 PM. `Time` is 12-hour, America/New_York — the zone §11.1's readiness rule
> states and §27.2's timeline assumes. `Source` is a person, channel, or named measurement — never
> "the team", and never a document that is not stored in this vault (§32.3 source custody).

## Log

| Time | Decision / organizer update | Source | Impact | What it changed |
|---|---|---|---|---|
| Wed 5 Aug, 7:56 PM | **Historical-context dataset selected: the NYC Open Data collision dataset, four-by-four `h9gi-nx95`.** Both the id and its published title (`{{SOCRATA_DATASET_TITLE}}`) are **selected-but-unverified** — the id came from user direction, not from a portal lookup, and nobody has queried it. | User direction, 5 Aug | Answers the §30 question *"Which NYC Open Data fields are stable?"* **at the dataset level only**. The field-stability half stays open to its Thu 6 Aug deadline, default "use cached, source-attributed context". Carry that qualifier anywhere this answer is cited. **No PRD change and no version bump** — §18.2 already approves "NYC Open Data Socrata datasets, including collision and 311 datasets where relevant", so this is a selection under an existing approval, not a §31 matter. | The proposed field set and its unverified status live in [[01-Datasets]] — not restated here. Nothing has been queried, so whether the columns are *present* is as untested as whether they are *populated*; [[NYC-Open-Data-Fields]] tracks the open half. Separately, `nearmiss/models.py:105` `HistoricalContext` carries `source`, `nearby_collision_count`, `radius_meters` and `retrieved_at` — no dataset identifier and no time window, both of which FR-013 requires and which §20's core data contract shows as a `dataset_id` field distinct from `source`. Its docstring also cites FR-009, which is candidate-pair filtering; the enrichment requirement is FR-013. A code task, not a doc change. |
| Wed 5 Aug, 7:56 PM | **Blended risk formula PROPOSED and REJECTED.** The proposal was `0.35 proximity + 0.25 zone_overlap + 0.20 closing_motion + 0.10 vulnerable_user + 0.10 historical_context`, with no `evidence_quality` multiplier. **FR-010 stands exactly as written** — approved, closed, not reopened. | User direction, 5 Aug | Rejected because §19.1 defines the proxy as ranking **image-space** evidence, so a location prior would make identical geometry score differently by neighbourhood — which §23 item 9 ("historical correlation is not causal proof") and item 10 (observed evidence, derived metrics, public context and explanation stay separate) both forbid, and because §1 lists risk-scoring semantics as an ADR-**plus**-version-bump change on a frozen [[00-Source-of-Truth-PRD\|PRD]]. §20's core data contract already places `historical_context` as a **sibling** of `risk_score` and `risk_factors` rather than an input to them; the contract is right and the formula was wrong. | What was rejected is the conflict zone as a **scoring factor** — `path_overlap` remains the FR-010 factor and is unchanged. Whether a conflict-zone **gate** is added at all is undecided: it is **proposed, not in the PRD**, and is carried in the PENDING row below, not adopted here. Historical context stays **displayed beside** the score, never inside it — which is what §20's contract and §23 item 10 already require. The absent `evidence_quality` multiplier is a **code task, not a doc change**: `nearmiss/risk.py:139` stops at the weighted sum and `nearmiss/models.py:77` `RiskFactors` has only four fields. `vulnerable_user` is already a hardcoded `1.0` in `risk.py:135` — a floor on any VRU conflict, not a discriminator, because FR-009 pre-filters to vehicle–VRU pairs. Cooldown, the Mode A–E resilience matrix and the mock-event generator are recorded as **proposals, not requirements, and not adopted** — Mode A–E would have to map onto FR-015's existing fallback ladder rather than duplicate it. See the PENDING row. |
| Wed 5 Aug, 7:56 PM — **PENDING** | **Cooldown / event deduplication** and the **conflict-zone polygon gate**. Both are **proposed additions, not in the PRD**. Needs a decision before either is built. | User direction, 5 Aug | Neither concept appears anywhere in the PRD. §24.4 covers duplicate frames and temporary overlap caused by detection jitter, but has **no** notion of suppressing repeated *events* arising from one interaction, and no polygon or zone geometry is specified anywhere. Writing either as a requirement would be a §29/§31 move, not a log entry. | Nothing yet — neither is built: no cooldown and no zone polygon exists under `app/backend/nearmiss/`. Decide (build or drop) before the **Thu 6 Aug 8:00 PM** readiness decision that grades the §11.1 baselines; an undecided proposal must not reach Friday as half-built behaviour. |
| Wed 5 Aug, 8:12 PM | **[[03-Scope-Ladder]]'s scope-freeze rule re-anchored from 8:00 PM to §27.2's 7:00 PM hard code freeze.** §27.2 defines no scope freeze at all. | [[00-Source-of-Truth-PRD\|PRD]] §27.2 read against [[03-Scope-Ladder]] | Narrows the rule: it removes an implied hour of post-freeze scope work §27.2 does not permit, and moves the "stop P1 and P2" trigger to *before* the freeze rather than at it. **No PRD change** — §29 already locks "7:00 PM is the hard feature freeze"; this aligns a vault note to the frozen document. | [[03-Scope-Ladder]] now reads 7:00 PM throughout, with §27.2's 7:00–7:30 PM reliability and fallback proof, 7:30–8:00 PM submission assembly, and 8:00–8:15 PM protected contingency intact behind it. The correction is applied; nothing here is open. |

The open questions, their decision deadlines, and their unresolved defaults live in
[[00-Source-of-Truth-PRD|PRD]] §30 (unnumbered — cite a question by its text). Do not restate them
here; a second copy drifts the moment either side moves. Add a row the moment an answer lands,
naming the §30 question it answers.

Until an answer lands, §30's unresolved default is what the build runs on. Once a row is written,
never delete it — the answer and the time it landed are the audit trail.

## Escalation boundary

Three tiers. Almost everything is tier 1.

1. **Lands here.** Implementation choices, package release hashes and pins, source selections,
   organizer answers, and bounded scope cuts. §31 pre-event freeze. No PRD version increment, no
   ADR. This is the default and should stay the default through Friday.
2. **Needs a §29 entry.** A decision that *constrains the build* — one that other work then has to
   obey. It goes into §29's locked list through the full §31 protocol, all eight steps, proposed
   change through organizer evidence, including an ADR reference when the change is architectural.
   Read §31 before starting; it is not a 6:40 PM activity.
3. **Needs a new PRD version.** Only when an organizer change invalidates the product thesis, the
   safety boundary, or the Cloud Run eligibility contract (§30; §31 adds architecture to that list).
   §30 states plainly that **no PRD revision is required onsite** otherwise.

> [!danger] Scope cuts are tier 1, and they follow a fixed order
> Cutting work is not an architectural decision — log it here and move. Two instruments, not one,
> and their orders do not match. [[03-Scope-Ladder]] is rung-ordered — bottom-up, cut-first rung
> before never-cut rung — and anchored to §27.2's timeline. §27.3 is a fixed seven-item removal
> order with its own never-cut list, and it carries no clock reference: it applies whenever time is
> lost. Both are event-day instruments. At the venue, §27.3 wins and is not negotiable.
>
> Dropping the public `vision-conflict-analytics` package work is not a bounded cut — it is a §26.1
> arrival-gate breach, and [[03-Scope-Ladder]] rung 3 marks the real-source path never-cut. If
> either is cut anyway, log it here and name the breach.

## Where this log is worth nothing

If the entry belongs somewhere else, put it there instead:

- A thing that is **broken and blocking** → [[07-Blocker-Log]], not here.
- A **risk that has not fired yet** → [[06-Risk-Register]].
- A **command or URL that turned out to be real** → the runbook ([[01-Hackathon-Runbook]]); §31
  explicitly permits updating actual commands and URLs without a PRD change.

## Open inconsistencies — decide here, do not silently pick

- **ADR folder status.** The vault `CLAUDE.md` states there is no ADR folder and routes every
  constraining decision to §29 alone. §31's governance state for v2.1 still requires ADR-006 and
  ADR-007 to be accepted and `07-Decisions/00-ADR-Index.md` to point at the active decisions, and
  the folder exists on disk with eight files ([[00-ADR-Index]] plus seven ADRs). Unresolved — tier 2
  above cites §31, which is the frozen document.

## Standing note on the schedule (as of Wed 5 Aug)

The build schedule has slipped. §27.1 carries **three** dated lists, not one: Tuesday items 1–8
(overdue), Wednesday items 9–17 (due today), Thursday items 18–24 (due tomorrow). That is 24 items,
and none of the three lists has produced a completed, verifiable artifact.

One item has partial work and should be named rather than counted as unstarted. Item 10 — "typed
asymmetric class-pair configuration and decomposed interaction scoring" — exists in substance:
`app/backend/nearmiss/config.py:80-81` carries the typed asymmetric class-pair configuration and
`app/backend/nearmiss/risk.py` implements decomposed per-factor scoring. But it lives privately
inside NearMiss, not in the public `vision-conflict-analytics` package item 9 was to create, and
§26.1's arrival gate requires "no duplicate private scoring implementation" — so the current
placement counts against the gate, not for it, until it moves behind a pinned dependency.

What this repo can actually confirm:

- **Verifiably not done.** `gcloud` is not installed (item 4). No FastAPI application and no
  Dockerfile exist anywhere under `app/backend/nearmiss/`, so there is nothing deployed and nothing
  to verify logged-out (items 5–6). [[08-Deployment]] still carries an unresolved `{{BE_URL}}`, so
  the deploy and rollback commands are unrecorded (item 7).
- **Unknown — needs human confirmation.** The GCP account, billing, and API enablement (items 1–3),
  the Roboflow account, key and smoke test (item 8), and whether the public
  `vision-conflict-analytics` repository exists (item 9) are console and GitHub state this vault
  cannot see. `.gitignore` excludes `.env` and `.env.*`, so an absent `.env` proves nothing either
  way. Do not count these as done or as not done — ask.

`demo/fixtures/` holds only a README and `demo/captured-sequence/` only a `.gitkeep`, so the
guaranteed fallback has no evidence to replay. Fixtures alone would not finish it: item 16 requires
the replay verified locally **and** on the deployed service, and there is no HTTP surface yet.
`app/frontend/` holds only `README.md`, so item 19 — the six dashboard surfaces — is a from-scratch
day of work on its own.

The gate these 24 items run at is §27.1's **Thursday 8:00 PM readiness decision** on
**Thursday 6 August**, which grades the two §11.1 baselines and branches three ways. It is not
§27.3 — §27.3 is Friday's kill order and cannot be triggered by a Thursday blocker.

Practical consequence for this log: from here, most entries will be **scope cuts**, not preferences.
Record each cut with the time it was taken and the kill-order rung it came from, so the submission
notes can state honestly what was dropped and why.

## Friday 7 August — event day

### 5:05 PM — D-5 deviation log (overdue; D-5 was due Thursday 7:50 PM)

The §27.1 Thursday 8:00 PM readiness decision **passed without being taken**. No
entry was written at the time. Recording it now, late, rather than leaving the
gate silently unresolved.

What actually happened against the two §11.1 baselines:

- **Deployment baseline — MISSED Thursday, cleared Friday 5:02 PM.** No GCP
  project, no billing, no `gcloud`, nothing deployed as of Friday morning. The
  service is now live at
  `https://nearmiss-nyc-711121860771.us-east1.run.app`, revision
  `nearmiss-nyc-00001-cr7`. §2.2 is satisfied: public without authentication
  (`allUsers`), `/health` 200, revision identified in the payload.
- **Captured-evidence baseline — RED, and cut.** The sequence is synthetic, not a
  source-attributed NYC capture. W-14 was never done and cannot be done inside
  §11.2's configuration-only window. Disclosed in the root `README.md`
  Limitations section rather than papered over.

Deviations from the plan, each deliberate:

| Deviation | Reason |
|---|---|
| D-0 through D-4 never ran as separate `/implement` invocations | The work they described was already done; running the ceremony would have consumed the gate window |
| LICENSE is Apache-2.0, replacing the stub repo's auto-generated MIT | Both satisfy §11.1 baseline 5; Apache-2.0's patent grant suits the reusable analytics package |
| `.specify/` gitignored, not committed | Stock SpecKit scaffolding appeared 11:42 AM carrying an unfilled template constitution that would compete with [[01-Constitution]] |
| Remote merged with `--allow-unrelated-histories` rather than force-pushed | `origin/main` was a GitHub stub; merging discarded nothing |
| Six §11.3 judge surfaces not built | `app/frontend/src/` is empty. Kill-order rung 1 (visual polish). See the organizer note below — a feed dashboard is actively discouraged |

### 5:10 PM — organizer slides close three §30 questions

From the kickoff slides ("Today's event" and "Do not (suggestions)"):

1. **Cloud Run exclusivity — CONFIRMED.** The slide reads "The only requirement:
   your agent must be deployed on Google Cloud Run." §2.1 previously classed this
   as organizer-stated but the *exclusivity* as unverified. It is now verified.
2. **Starter repo not mandatory.** "Starter packs include a working example" —
   offered, not required. The §30 default holds: keep this repo, adapt metadata.
3. **Build time is ~3 hours**, not the 105 minutes [[02-Time-Box-Plan]] assumed.

Two organizer instructions bear directly on scope:

- *"Don't hardcode one camera ID and pray. Cameras go offline, so handle it or
  have a fallback feed."* The §17 fallback ladder answers this literally, and
  discloses which rung served via `processing_mode` and `notices`. This is a
  pitch point, not just an implementation detail.
- *"Don't make a dashboard that just displays a camera feed."* This lowers the
  cost of the cut above — the missing dashboard is less damaging than it looked.

Against the slides' framing, the remaining gap is that "live NYC feeds" is the
spine of the event and our live path degrades to a synthetic fixture. That is now
the highest-value remaining work, not the UI.

---
Related: [[00-Source-of-Truth-PRD|PRD]] §29 · §30 · §31 · §32.3 · [[03-Scope-Ladder]] · [[07-Blocker-Log]] · [[01-Datasets]] · [[01-Constitution]]
