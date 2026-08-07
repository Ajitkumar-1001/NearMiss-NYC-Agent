---
title: Hackathon Runbook
tags:
  - execution
status: active
---

# Hackathon Runbook

The operational sequence for Friday, August 7, 2026. Held open at the venue. Follow it
instead of improvising at 6:30 PM.

> [!danger] 24 items outstanding — the readiness gate fires tonight
> Today is **Thursday, August 6**. The §11.1 readiness gate is **tonight at 8:00 PM ET** and
> the event is **tomorrow**. [[00-Source-of-Truth-PRD|PRD]] §27.1 carries three dated lists —
> Tuesday (items 1–8), Wednesday (9–17), Thursday (18–24) — and none has been worked. The
> first two are now overdue; the third is due today.
>
> Of the overdue Tuesday list only four items are checkable from this repo, and all four are
> red: item 4 (`command -v gcloud` fails), item 5 (no FastAPI application, no Dockerfile),
> item 6 (nothing exists to verify from a logged-out browser — follows from 5), item 7
> ([[08-Deployment]] still carries `{{BE_URL}}`, so no deploy or rollback command is recorded).
>
> Items 1–3 (Google Cloud account, billing, API enablement) and item 8 (Roboflow account, API
> key, smoke test) are external console state this vault cannot see — **unknown, needs human
> confirmation**, not "not done". `.gitignore` excludes `.env` and `.env.*`, so a missing
> `.env` is not evidence either way.
>
> The §11.1 readiness gate is **Thursday, August 6, 8:00 PM America/New_York** — one and a
> half days. Item 19 alone ("Finalize the six dashboard surfaces") is a from-scratch day of
> work: `app/frontend/` holds only `README.md`.

> [!warning] The build window is 105 minutes — roughly 60 of them for feature work
> Doors 4:00 PM · build opens ~5:15 PM · **hard feature freeze 7:00 PM** (§29) ·
> protected contingency 8:00–8:15 PM · submit 8:15 PM · lock 8:30 PM · demos 8:45 PM.
>
> Per §27.2 the first ~20 minutes go to the eligibility-gate deploy and the last ~25 to
> documentation and submission prep. Actual feature integration is roughly **5:35–6:35 PM**;
> the other 45 minutes are the gate and the paperwork and cannot be borrowed. Nothing on
> §27.1 that slips gets built at the venue — §11.2 is explicit that event-day P0 does not
> include building the pipeline, the fixtures, the dashboard, or the deployment scaffolding
> from scratch.

---

## Kill order — read this first when time is lost

[[00-Source-of-Truth-PRD|PRD]] §27.3 holds the seven-rung order and the item names. Read them
there; they are not restated here so the two cannot fork. Remove work from rung 1 downward.
Do not renegotiate the order at the venue — it was fixed so nobody has to think at 6:40 PM.
What this table adds is why each rung is cheap to lose:

| §27.3 rung | Why it is cheap to lose |
|---|---|
| 1 | Judges score the six §11.3 surfaces, not their finish |
| 2 | §29 makes it P1; the deterministic explanation is the P0 path |
| 3 | §29 makes it P1; cached source-attributed context already covers it |
| 4 | §2.4 makes it conditional — skip it and do not claim it |
| 5 | One configured source satisfies §2.2 and §11.1 |
| 6 | §11.4 lists it as P1 |
| 7 | §29 marks it post-P0 explicitly |

> [!danger] §27.3's never-remove list
> §27.3 closes with six things that are never removed or destabilized. If a change threatens
> any of them, revert the change — §27.3 states no exception. The first of them is Cloud Run
> public access: §2.2 makes a reachable public service the condition for being
> hackathon-complete, and §2.1's fact table records it as *the only stated eligibility gate* —
> organizer-page-derived, to be reconfirmed at kickoff.

> [!warning] [[03-Scope-Ladder]] is a different instrument, and it contradicts §29
> The ladder governs **pre-event** cuts (Wednesday and Thursday). §27.3 governs **Friday from
> 5:15 PM**. They are separate, non-matching lists and do not map rung for rung — do not treat
> one as a restatement of the other. The ladder also anchors its scope freeze at 8:00 PM while
> §29 locks the hard feature freeze at **7:00 PM**. That contradiction is unresolved: take it
> to [[05-Decision-Log]] before Friday rather than picking one at the venue.

---

## Before the venue — the Thursday 8:00 PM readiness gate

§11.1's readiness rule: if the **deployment baseline** or the **captured evidence baseline** is
incomplete by **Thursday 8:00 PM America/New_York**, stop all optional product work.

The arrival-gate checklist is [[00-Source-of-Truth-PRD|PRD]] §26.1 — go there directly.
[[08-Definition-of-Done]] carries one merged P0 list that does not reproduce §26.1's split or
all of its checks, so it is not a substitute for the gate.

**Red, and triggers the §11.1 stop-work rule:**

| Baseline | Blocker | Verified state in this repo |
|---|---|---|
| Deployment | Eligibility gate (§2.2) needs a deployed FastAPI service | No FastAPI application exists. `app/backend/pyproject.toml` declares `fastapi>=0.115` and `uvicorn[standard]>=0.32` as dependency floors, not pins; no module under `nearmiss/` imports either. `nearmiss/models.py` defines `Health` and `DependencyStatus`; nothing serves them. **No Dockerfile anywhere.** |
| Deployment | `gcloud` (§27.1 item 4) | Not installed — `command -v gcloud` fails |
| Deployment | Deploy/rollback commands (§27.1 item 7) | Not recorded — [[08-Deployment]] still carries `{{BE_URL}}` |
| Captured evidence | Replay fallback (§11.1, §29) | `demo/fixtures/` holds only `README.md`. `providers/vision.py:43` reads `detections.json`, `providers/tracking.py:37` reads `tracks.json`, `providers/context.py:48` reads `context.json` — all three raise `FileNotFoundError` today. `demo/captured-sequence/`, `demo/recordings/`, and `demo/screenshots/` are empty. |

**Red, but outside the §11.1 rule — still §26.1 arrival-gate items, so still due Thursday:**

| Blocker | Verified state in this repo |
|---|---|
| Reusable package (§11.1 reusable conflict-analytics baseline, FR-022) | `vision-conflict-analytics` not yet created |
| Six judge-facing surfaces (§11.3, §26.1) | `app/frontend/` holds only `README.md` — zero of six exist |
| Tests (§27.1 item 11) | Those tests belong to the not-yet-created `vision-conflict-analytics` repo, not to this vault. This vault's `tests/` is separately empty — only `README.md` — and `app/backend/pyproject.toml` points `testpaths` at it. |

> [!question] Not checkable from this repo
> §27.1 items 1–3 (Google Cloud account, billing, API enablement) and item 8 (Roboflow account,
> API key, smoke test) live in external consoles. Confirm with a human before treating them as
> either done or outstanding. The vault holds only `.env.example`; `.gitignore` excludes `.env`
> and `.env.*`.

> [!note] The runtime providers decline; the P0 rungs are coded but have no data
> `RoboflowVision.detect` (`providers/vision.py:25`), `ByteTrackTracker.track`
> (`providers/tracking.py:20`), and `NycOpenDataContext.lookup` (`providers/context.py:26`)
> each raise `ProviderUnavailable`. `RiskEngine` (`risk.py:85`) and `TemplateExplanation`
> (`providers/explanation.py:60`) are fully implemented and need no fixture file. The fixture
> rungs are implemented too — they just read files that do not exist. Both demo paths are
> unrunnable today because the fixtures and the HTTP surface are missing, not because the
> scoring code is.

**Thursday 8:00 PM decision, per §27.1's readiness decision (three branches):** Cloud Run
public access red → stop everything else and fix deployment. Captured evidence red → stop all
live, Gemini, Veris, and design work and finish the fixtures. Both green → freeze them and
prepare only small event-day adapters. Record whichever branch is taken in [[05-Decision-Log]].
This is a different instrument from §27.3, which is the event-day kill order and applies only
on Friday.

---

## First 15 minutes at the venue — 4:00 to 4:15 PM

Arrive, sit down, and ask these before touching a keyboard. Each has a
[[00-Source-of-Truth-PRD|PRD]] §30 deadline that falls at or before kickoff, and each has a
stated default so an unanswered question never blocks the build.

| Ask (§30, by question text) | Deadline | Default if unanswered |
|---|---|---|
| "Which organizer or city camera source is most reliable?" | Kickoff, 4:45 PM | Use the already tested approved source |
| "Is there a mandatory starter repo or submission format?" | Kickoff | Preserve the current repo; adapt metadata only |
| "Is there a Veris prize, requirement, starter tool, or useful scenario API?" | Kickoff, before 5:15 PM | Skip Veris and do not claim integration |
| "What is the policy for pre-existing code, scaffolding, reusable packages, and prepared fixtures?" | Thursday, **reconfirm at kickoff** | Disclose all prepared work in README and submission notes; separate pre-event from event-day commits |

Routing, no exceptions:

- Question text and the answer received → [[04-Organizer-Questions]].
- Any answer that changes what gets built → [[05-Decision-Log]], with the time it landed.
- §2.1: a same-day organizer update **supersedes** the PRD's event-facts table and must be
  recorded in the decision log. §30 adds that no PRD revision is required onsite unless an
  organizer change invalidates the product thesis, the safety boundary, or the Cloud Run
  eligibility contract.
- Also confirm in this window (§27.2): final rules, the submission mechanism, and that the
  chosen source is both permitted and technically reachable. Then revalidate the existing
  Cloud Run service — **do not rebuild the platform**.

Write the answers down as they arrive. Nobody remembers them at 7:50 PM.

---

## The build window — the only six things

[[00-Source-of-Truth-PRD|PRD]] §11.2 lists the complete event-day integration delta as six
numbered steps; read the steps there. If a task is not one of those six it is not P0 work, and
after 7:00 PM it is not work at all. What this runbook adds is the acceptance test for each:

| §11.2 step | Done when |
|---|---|
| 1 | Answers logged to [[04-Organizer-Questions]] |
| 2 | Source id, attribution, retrieval timestamp, freshness, and content hash all present (FR-003) |
| 3 | One annotated real NYC frame on screen |
| 4 | Live path and captured replay both complete from the public URL, not localhost |
| 5 | README carries final source names, screenshots, and the pre-existing-code disclosure ([[09-Preexisting-Code-Disclosure]]) |
| 6 | Backup clip and screenshots saved **locally**, not only in the cloud |

Anything else proposed during the window is a kill-order candidate, not a task. Blocked more
than **10 minutes** on one of the six → log it in [[07-Blocker-Log]], apply the kill order, and
move to the next numbered step. (Ten minutes is this runbook's own call, not a PRD figure —
change it here if it proves wrong.)

---

## Timeline — Friday, August 7

Condensed from §27.2. Each window has one job; do not carry work forward into the next one.

| Window | The one job |
|---|---|
| 4:00–5:15 PM | Check-in, §30 questions, source confirmation, workshop. Revalidate the existing service. |
| 5:15–5:35 PM | **Clear the eligibility gate.** Deploy the known-good revision; verify `/health`, public access, revision metadata; save the URL and rollback revision. |
| 5:35–6:05 PM | Integrate the final real source through the existing adapter; run Roboflow; show provenance, freshness, annotated result. |
| 6:05–6:35 PM | Verify both demo paths plus the no-event and insufficient-evidence behaviour. **Integration defects only — no architecture changes.** |
| 6:35–7:00 PM | Final source names, screenshots, README, submission fields. Veris scenario pack only if confirmed *and* it finishes before 7:00 PM. |
| **7:00 PM** | **Hard code freeze.** Tag and preserve the deployed revision. No new feature, provider, framework, model, camera, page, or refactor after this line. |
| 7:00–7:30 PM | Three deployed golden-path runs. Test primary-source outage → captured replay fallback. Record the backup demo. Save screenshots locally. |
| 7:30–8:00 PM | Submission assembly: repo, license, README, architecture, source notes, privacy notes, URLs. Rehearse the two-minute demo. Populate the form. |
| 8:00–8:15 PM | **Protected contingency.** Rollback, broken URL, submission metadata, or a re-recorded backup clip only. Never features or polish. |
| 8:15 PM | **Submit** — fifteen minutes before the 8:30 PM lock. 8:15–8:30 is for submission-system recovery only. |
| 8:45 PM | Demos begin. |

The two-minute run of show is [[04-Demo-Script]], built on §12.2's golden flow. The pass/fail
gates at 8:15 PM are [[00-Source-of-Truth-PRD|PRD]] §26.2 — cite it directly, including
"Golden demo succeeds three consecutive times from the deployed URL", which the merged list in
[[08-Definition-of-Done]] does not carry. Neither is restated here.

---

## When something breaks

| Symptom | First move |
|---|---|
| Public URL down or 5xx | Roll back to the known-good revision `{{KNOWN_GOOD_REVISION}}` using `{{ROLLBACK_COMMAND}}`. This outranks every other task: §2.2 makes a reachable public service the condition for being hackathon-complete, and §2.1 records it as the only stated eligibility gate (organizer-derived, reconfirm at kickoff). |
| Live source unreachable or stale | Do not fake it. Show the truthful outcome state and run the captured replay; §12.4 and §29 both make a live no-conflict or insufficient-evidence result **valid**. |
| Roboflow failing | Fall back down the FR-015 provider ladder in `nearmiss/orchestrator.py` — four step-downs are coded (`_detect`, `_track`, `_context`, `_explain`), but they land on fixtures that do not exist yet, and FR-015's live-source → captured-sequence rung has no implementation at all. Label the fallback in the UI (§26.2). |
| Behind schedule at any checkpoint | Apply the §27.3 kill order, rung 1 downward. Do not reprioritize by argument. |
| Anything at all after 7:00 PM | Freeze holds. Use the backup recording. |

Keep a green commit as a rollback point — commit each working state during the window and
note the time in [[Hackathon-Day-Log]].

> [!info] Placeholders
> `{{KNOWN_GOOD_REVISION}}` and `{{ROLLBACK_COMMAND}}` are unfilled because nothing is
> deployed. Fill them the moment they are known — a runbook with a blank rollback command is
> not a runbook.

---
Related: [[03-Scope-Ladder]] · [[08-Definition-of-Done]] · [[02-Time-Box-Plan]] · [[04-Task-Board]] · [[07-Blocker-Log]] · [[04-Organizer-Questions]] · [[05-Decision-Log]] · [[04-Demo-Script]] · [[00-Source-of-Truth-PRD|PRD]]
