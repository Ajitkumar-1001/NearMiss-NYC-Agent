---
title: Time Box Plan
tags:
  - execution
status: active
---

# Time Box Plan

The calendar for what is left — tonight and Friday. [[01-Hackathon-Runbook]] says what to do at
the venue; this note says **how much time there is to do it in**, and what the numbers
already rule out.

> [!danger] Two days slipped — the readiness gate fires TODAY
> Today is **Thursday, 6 August**. [[00-Source-of-Truth-PRD|PRD]] §27.1 carries **three**
> dated lists and none of them is closed: **Tuesday items 1–8** (two days overdue),
> **Wednesday items 9–17** (one day overdue), **Thursday items 18–24** (due today).
> The §11.1 readiness rule fires **tonight, 8:00 PM America/New_York**.
>
> Twenty-four items, two baselines that both have to be green, and the rest of one day.
> That is not a schedule — it is a triage problem. Plan from [[03-Scope-Ladder]] and expect
> the §11.1 branch tonight to be "stop everything else and fix the baselines", not "freeze
> and prepare adapters". §27.3's kill order does not apply until Friday's build window opens.

> [!warning] The Friday build window is 105 minutes — about 60 of them are feature work
> Build opens **~5:15 PM** · hard feature freeze **7:00 PM** (§29). Inside that window §27.2
> spends the first 20 minutes on the eligibility gate and the last 25 on documentation and
> submission fields, so real feature integration is roughly **5:35–6:35**. Those other 45
> minutes cannot be borrowed. §11.2 is explicit that event-day P0 does not include building
> the pipeline, the fixtures, the dashboard, or the deployment scaffolding from scratch.
> Anything that misses Thursday does not get built on Friday — it gets cut.

## The whole remaining budget

| Block | Hours | Goal | Checkpoint |
|---|---|---|---|
| Wednesday (today) | {{HOURS_AVAILABLE_WEDNESDAY}} | Overdue §27.1 Tuesday chain **plus** today's items 9–17 | Deployment baseline and captured-replay baseline both runnable |
| Thursday | {{HOURS_AVAILABLE_THURSDAY}} | §27.1 items 18–24 | **8:00 PM readiness decision** (§11.1, §27.1) |
| Friday pre-event | {{TRAVEL_TIME_TO_VENUE}} travel; depart {{DEPART_FOR_VENUE}} | Nothing. Do not code in transit | Doors 4:00 PM at {{VENUE_ADDRESS}} |
| Friday build | **1:45** (5:15–7:00 PM) | §11.2 steps **2–6** only | Freeze 7:00 PM |
| Friday freeze | 1:15 (7:00–8:15 PM) | Prove reliability, assemble submission, submit | §26.2 submission gate |

No invented hour estimates for Wednesday and Thursday. The only honest budget is those two
unknown numbers; what this note fixes is **the order**, so nobody re-litigates priority late
tonight.

---

## Today — Wednesday 5 August

Carrying two days' work. Sequence below follows the §11.1 readiness rule, which gates only
**two** baselines — deployment and captured evidence. Everything else yields to them. If you
work a different order, that is a call to record in [[05-Decision-Log]].

### First: the overdue Tuesday chain (§27.1 items 1–8) — retire deployment risk

§2.2 makes public Cloud Run deployment a hard eligibility gate; §2.1 records it as the *only*
stated one, organizer-page-derived and to be reconfirmed at kickoff. Nothing outranks it.

| Order | Items | State right now |
|---|---|---|
| 1 | GCP project on personal Gmail, billing, Cloud Run / Cloud Build / Artifact Registry APIs (1–3) | **Unknown — needs human confirmation.** External console state; nothing in this repo can show it either way |
| 2 | Install and authenticate `gcloud` (4) | **Not done** — `command -v gcloud` fails |
| 3 | FastAPI health skeleton, deployed and reachable logged-out (5–6) | **Not done.** No FastAPI application exists: `pyproject.toml` pins FastAPI and uvicorn, no tracked module imports either; `nearmiss/models.py` defines `Health` and `DependencyStatus` and nothing serves them. **No Dockerfile anywhere** |
| 4 | Record deploy and rollback commands (7) | **Not done** — [[08-Deployment]] still carries `{{BE_URL}}` |
| 5 | Roboflow account, key, one inference smoke test (8) | **Unknown — needs human confirmation.** `.gitignore` ignores `.env` and `.env.*`, so an absent file proves nothing about whether the key exists |

### Then: today's own list (§27.1 items 9–17) — retire evidence risk

| Order | Items | State right now |
|---|---|---|
| 6 | Captured evidence sequence and committed fixtures (14–15) | `demo/fixtures/` holds only `README.md`; `demo/captured-sequence/`, `demo/recordings/`, `demo/screenshots/` are empty. `providers/vision.py:43` reads `detections.json`, `providers/tracking.py:37` reads `tracks.json`, `providers/context.py:48` reads `context.json` — all three raise `FileNotFoundError` today |
| 7 | Verify captured replay locally **and on the deployed service** (16) | Blocked on order 3 and order 6 together — there is no HTTP surface at all, so the deployed half cannot even be attempted |
| 8 | No-conflict, stale-frame, insufficient-evidence states (17) | **Not implemented** — grepping `app/backend/nearmiss/` for `no_candidate`, `insufficient`, and `stale` returns nothing, so the outcome states §11.1's real-source baseline and §26.2 require do not exist in the pipeline; `tests/` holds only `README.md`, so nothing covers them either |
| 9 | Validate one approved NYC source (13) | No source registry (FR-001) and no source adapter (FR-002) yet; of FR-004's input modes only the fixture path is stubbed |
| 10 | `vision-conflict-analytics` package, tests, pinned release (9–12) | NearMiss side not done — `nearmiss/risk.py` computes the score in-repo, which §29 requires to move behind the pinned package. Whether the public package repo itself exists is external state — unknown from here |

> [!caution] Order 6 is the guaranteed fallback, not a nice-to-have
> §29 locks captured-feed evidence replay as *the* guaranteed conflict demonstration, and
> with zero fixture files the three fixture-backed providers above cannot complete a single
> run. Fixtures alone do not finish it either: `providers/explanation.py:60`
> `TemplateExplanation` and `risk.py:85` `RiskEngine` are already implemented and need no
> fixture, while §27.1 item 16 also demands the replay verified **on the deployed service**,
> which does not exist. Order 6 comes first in sequence; that does not make items 9–13
> optional.

> [!note] Where the hours actually go today
> Orders 1–5 unblock the disqualifier. Orders 6–8 unblock the fallback. Orders 9–10 sit
> outside §11.1's two-baseline readiness rule but **inside §26.1's first-nine arrival gate**
> — check 5 (a source adapter has fetched a current image) and check 9 (public package repo,
> tests, license, immutable release). Neither can be shed quietly: cutting either is a §26.1
> breach and must be logged in [[05-Decision-Log]].

---

## Thursday 6 August

§27.1 items 18–24 close out submission risk. Load Thursday honestly: `app/frontend/` holds
only `README.md`, so **zero of the six §11.3 surfaces exist** and item 19 is a from-scratch
day of work sitting behind whatever slips out of today.

### The 8:00 PM readiness decision (§27.1, §11.1)

Stop at 8:00 PM sharp and take the branch §27.1's readiness decision assigns. Do not keep
building through it. Both baselines have to be green — the deployment branch and the
captured-evidence branch are **not** alternatives, which §27.1 leaves implicit. Record the
branch taken, with the time, in [[05-Decision-Log]].

This decision is not §27.3. §27.3 is the *event-day* kill order, scoped to Friday's timeline
when time is lost; a Thursday blocker is governed by the readiness decision above.

Green-lists: §26.1 in the PRD, not restated here. Read them there —
[[08-Definition-of-Done]] merges §26.1 and §26.2 into a single P0 list and drops items,
including "Golden demo succeeds three consecutive times from the deployed URL".

---

## Friday 7 August — the hour-by-hour

Condensed from §27.2 as a **budget**. The runbook's version of this table says what each
window is for; this one says how many minutes it has and what gets cut when it overruns.

| Block | Time | Mins | Goal | If it overruns |
|---|---|---|---|---|
| Check-in | 4:00–5:15 | 75 | §30 questions, source confirmation, workshop; revalidate the existing service. §11.2 step 1 is retired here | Never rebuild the platform here — carry the question, use its §30 default |
| Eligibility gate | 5:15–5:35 | 20 | Deploy known-good revision; `/health`, public access, revision metadata; save URL + rollback | Everything else waits. This is §2.2 |
| Real source | 5:35–6:05 | 30 | Configure the source through the **existing** adapter, run Roboflow, show provenance | Kill-order 5: drop to the one already-tested source |
| Verify both paths | 6:05–6:35 | 30 | Live path, captured replay, no-event and insufficient-evidence behaviour | Integration defects only — no architecture changes |
| Docs + optional | 6:35–7:00 | 25 | Final source names, screenshots, README, submission fields | Kill-order 4: drop Veris. It only runs if it finishes before 7:00 |
| **Freeze** | **7:00** | — | Tag and preserve the deployed revision | Nothing crosses this line (§29) |
| Reliability proof | 7:00–7:30 | 30 | Three deployed golden-path runs; source-outage → replay fallback; record backup; save screenshots locally | Backup recording is the last thing to lose, never the first |
| Submission assembly | 7:30–8:00 | 30 | Repo, license, README, architecture, source and privacy notes, URLs; rehearse two minutes | Rehearsal is cut before submission fields are |
| **Contingency** | **8:00–8:15** | **15** | Rollback, broken URL, submission metadata, re-record backup — **nothing else** (§29) | Protected. It is not spare build time |
| Submit | 8:15 | — | Fifteen minutes before the 8:30 PM lock | 8:15–8:30 is submission-system recovery only |
| Demos | 8:45 | — | Two-minute run of show ([[04-Demo-Script]]) | Our slot: {{DEMO_SLOT_TIME}} |

The build window is 105 minutes (5:15–7:00 PM), but only **60** of them — 5:35–6:35 — are
feature integration. The other 45 are the eligibility gate and the documentation block, and
neither can be borrowed from. Every minute borrowed from a later block comes out of
reliability proof, submission assembly, or contingency — the three things that make the demo
survivable.

## Checkpoint rule

At each checkpoint: if the goal isn't met, cut rather than borrow time from the next block.
Borrowed time always comes out of Freeze, and Freeze is what makes the demo work.

Two different instruments, split by phase — they are not one list and they do not match:

- **Before Friday** (today and Thursday): cut with [[03-Scope-Ladder]], bottom rung up.
- **From 5:15 PM Friday**: §27.3's kill order governs, reproduced in
  [[01-Hackathon-Runbook]]. Apply it top down; it is not a judgement call.

> [!caution] Freeze is not optional
> Features added after freeze are the single most common cause of a broken
> hackathon demo.

> [!warning] Open inconsistency to resolve — 8:00 PM vs 7:00 PM
> [[03-Scope-Ladder]]'s scope-freeze rule is anchored to **8:00 PM**, while §29 locks the
> hard feature freeze at **7:00 PM**. Both cannot be right, and this note does not pick one.
> Resolve it and record the resolution in [[05-Decision-Log]] before Friday.

> [!info] Placeholders
> `{{HOURS_AVAILABLE_WEDNESDAY}}`, `{{HOURS_AVAILABLE_THURSDAY}}`, `{{TRAVEL_TIME_TO_VENUE}}`,
> `{{DEPART_FOR_VENUE}}`, `{{VENUE_ADDRESS}}`, and `{{DEMO_SLOT_TIME}}` are genuinely
> unknown — personal availability, travel, and the venue/demo-order details unconfirmed per
> §2.1. Fill them in as they land; a time-box plan with an unknown departure time will make
> you late to your own 20-minute eligibility window.

---
Related: [[01-Hackathon-Runbook]] · [[03-Scope-Ladder]] · [[04-Task-Board]] · [[08-Definition-of-Done]] · [[05-Demo-Reliability]] · [[05-Decision-Log]] · [[00-Source-of-Truth-PRD|PRD]]
