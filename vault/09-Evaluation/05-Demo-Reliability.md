---
title: Demo Reliability
tags:
  - evaluation
status: active
---

# Demo Reliability

The demo working is the highest-value property this project has. Treat it as a
requirement, not a hope.

This note owns one question: **what counts as proof that the demo works?**
[[00-Source-of-Truth-PRD|PRD]] NFR-005 answers it with five run-count gates.
A checkbox here means the gate was met at its stated count — not that something
seemed fine once.

> [!warning] Zero of the five gates can be attempted today
> `demo/fixtures/` holds only `README.md`, and `providers/base.py:56` raises
> `FileNotFoundError` on a missing fixture rather than degrading — so not one
> local captured-replay run can complete. No FastAPI application exists in the
> tree (no tracked `.py` file references FastAPI, uvicorn, or `APIRouter`,
> though `app/backend/pyproject.toml` pins both), so there is no deployed
> service, no deployed run, and no public-access test. Every `[ ]` and every
> empty row below is empty because it is true, not because nobody filled it in.

## Verification standard

NFR-005, "before submission". These are counts, not impressions.

| # | Gate | Count | Attemptable today? | Blocked by |
|---|---|---|---|---|
| R1 | Local captured-replay runs | 10/10 | No | `demo/fixtures/` has only `README.md`, so `FixtureVision` / `FixtureTracker` raise `FileNotFoundError` (`base.py:56`) and `Orchestrator._detect` does not catch it. The `CachedContext` miss is the one exception — `orchestrator.py:123` catches that one |
| R2 | Deployed captured-replay runs | 5/5 | No | no FastAPI app, no Dockerfile, no deployed service — plus R1's blocker |
| R3 | Real-source fetches through the deployed service | 3 | No | no source registry (FR-001) and no real-source retrieval adapter (FR-002/FR-003); no deployed service |
| R4 | Real-source perception runs, where credentials permit | 3 | No | `providers/vision.py:32` `RoboflowVision.detect` raises `ProviderUnavailable`, and `VisionProvider.detect()` takes no arguments, so a live frame has nowhere to go |
| R5 | Public-access test from an independent browser/device | 1 verified | No | nothing is deployed to access |

Two adjacent gates are **not** substitutes for these:

- §26.2 requires the golden demo to succeed **three consecutive times from the
  deployed URL**. That is a §12.2 end-to-end flow, not R2's replay-path count.
  [[08-Definition-of-Done]] drops this item from its merged list — check §26.2
  directly, not that note.
- §24.3 requires a **live source fetch to succeed three consecutive times**.
  Consecutive is stricter than R3's three successes.

Deadlines: the §27.1 readiness decision falls on **Thursday 6 August, 8:00 PM
America/New_York** (§27.1 heads it "Thursday 8:00 PM readiness decision"; the
qualified timestamp is in the §11.1 readiness rule). If the captured evidence
package is not green there, all live, Gemini, Veris, and design work stops.
§27.2 gives the last window for the
deployed proofs: **Friday 7 August, 7:00–7:30 PM**, after the 7:00 PM freeze.
§29 locks that 7:00 PM hard feature freeze and the 8:00–8:15 PM protected
contingency together in one bullet, and §27.2 sequences them, so the reliability
window is pinned on both sides.

## Guarantees

Verified only when the named gate is met at its count.

| Property | How it's guaranteed | Proven by | Verified |
|---|---|---|---|
| Runs with network off | Fixture path; §26.1 requires captured replay to work without external APIs, §29 locks fixtures as operational fallbacks | R1 | [ ] |
| Provider outage degrades visibly, never breaks the run | Adapter fallback per FR-015 ([[07-Provider-Adapters]]); FR-016 forbids representing fallback as live inference and NFR-008 requires a user-readable notice, not a stack trace | D2–D5 below | [ ] |
| Same result every run | Fixed fixture inputs. There is nothing to seed: `nearmiss/risk.py:85` `RiskEngine` is pure arithmetic and `providers/explanation.py:60` `TemplateExplanation` is deterministic, so no random component exists | R1 at 10/10 — a flapping run is a failed gate, not a retry | [ ] |
| Reachable by a judge who is not us | NFR-002 public access | R5 | [ ] |
| Real source actually analyzed | FR-002 retrieval through the deployed service | R3 + R4 | [ ] |
| Resets in under {{RESET_SECONDS}}s | {{RESET_METHOD}} | not yet defined — nothing exists to reset | [ ] |
| Runs on the demo machine | Rehearsed on it | two clean rehearsals per [[08-Definition-of-Done]], table below | [ ] |

## Resilience modes A–E

**Proposed, not in the PRD.** The mode letters are a strategy addition and need a
[[05-Decision-Log]] entry. They add no new fallback: each mode names a position
on FR-015's existing ladder, paired with the FR-016 label that must be on screen
while that mode is active.

| Mode | What is running | FR-015 rung it sits on | FR-016 label that must show | Reachable today? |
|---|---|---|---|---|
| A | Live feed → live Roboflow → live or cached open data → deployed Cloud Run | None. Top of every ladder; no fallback engaged | A live label — `Live NYC snapshot` or `Live sampled sequence`, whichever matches the source shape ({{MODE_A_LABEL}}) | No — no FastAPI app and no Dockerfile in the tree, so nothing is deployed; no source registry (FR-001) or source adapter (FR-002/FR-004 — `providers/base.py:31` `VisionProvider.detect()` takes no arguments) |
| B | As A, but historical context served from cache | `NYC Open Data → cached context` — that rung only | Still A's live label. The context card itself must read as cached and source-attributed; `models.py:105` `HistoricalContext` carries `source` and `retrieved_at` | No — A's blockers, plus `CachedContext` (`context.py:48`) reads `demo/fixtures/context.json`, which does not exist — the run survives that miss but shows no context card |
| C | Recorded clip in place of the live feed; perception still runs on it | `Live source → captured evidence sequence` | `Captured feed replay` | No — this mode *is* gates R1 (local) and R2 (deployed); `demo/fixtures/` holds only `README.md` |
| D | Recorded event JSON replayed; vision bypassed entirely | `Roboflow hosted inference → stored detections`, plus `Tracker runtime → precomputed tracks` | `Demonstration fixture` | No — same empty fixture directory. There is no stored detection or track file to replay |
| E | Screen recording of an earlier working run | `Primary dashboard → backup recording and screenshots` — the last rung | None of FR-016's five. Nothing is processing, so no mode string is honest; the recording must be announced as a recording | No — E presupposes a run worth recording, and none has completed |

> [!important] Judges should see A. The project must stay presentable through D.
> A→D is the descent that is allowed to happen live without the demo stopping
> being a demo. E is an emergency exit, not a rung to plan around: it shows a
> recording of the agent, not the agent.

**Why this matrix is not a way to fake a demo.** FR-016 requires exactly one mode
to be active and forbids fallback operation being represented as live inference.
So each row above owes the audience a visible label, and the label descends with
the mode: C and D must not display A's live label, and E must not display any of
them. Read that way the matrix is a disclosure obligation, not a set of
substitutions — the descent buys presentability, never the appearance of a live
run. Below, drill D2 rehearses A→C, D3 rehearses A→D, and D5 rehearses A→B; they
inherit the blockers listed there. D4 (Gemini) sits on FR-015's explanation rung,
which no mode letter covers — the template explanation is a swap inside a mode,
not a step down it.

## Failure drill

§24.6 names eleven scenarios. Seven are rehearsals — a human breaks something
and watches what the audience sees. Four belong in [[02-Test-Cases]] as
automated cases. Rehearse, don't just plan.

| # | §24.6 scenario | How to trigger | Expected on screen | Rehearsal or test | Blocked by, or runnable today |
|---|---|---|---|---|---|
| D1 | All providers available | Normal golden run (§12.2) | Full flow, live badge honest | Rehearsal | R1–R4 blockers |
| D2 | Live source unavailable | Pull the source URL / disable the key | Falls to captured replay, mode badge changes per FR-016 | Rehearsal | no source adapter exists |
| D3 | Roboflow unavailable | `RoboflowVision.detect` (`vision.py:32`) already raises `ProviderUnavailable` unconditionally — the outage is free | Stored detections, labeled fallback | Rehearsal | The **fallback** rung, not the trigger: `FixtureVision.__init__` (`vision.py:43`) points at `demo/fixtures/detections.json` and that directory holds only `README.md`, so `Orchestrator._detect` (`orchestrator.py:85`) raises on the fallback |
| D4 | Gemini unavailable | `GeminiExplanation.explain` (`explanation.py:50`) raises `ProviderUnavailable` | Deterministic template explanation | Rehearsal | **Runs today.** `Orchestrator._explain` (`orchestrator.py:129`) catches it and returns `TemplateExplanation` (`explanation.py:60`) output from an in-memory `Candidate` — no fixture needed |
| D5 | NYC Open Data unavailable | `NycOpenDataContext.lookup` (`context.py:26`) declines | Cached context card, source-attributed | Rehearsal | **Not D3's shape.** `Orchestrator._context` (`orchestrator.py:123`) catches the `FileNotFoundError` that `CachedContext` (`context.py:48`, reading `demo/fixtures/context.json`) raises, appends "No historical context available." and returns no context — so the absent fixture degrades instead of killing the run, and the expected cached card is what is missing. The drill is still blocked by R1: `_detect` fails first, so the run never reaches this rung |
| D6 | Internet unavailable after initial load | Wi-Fi off mid-demo | Replay completes; no silent hang | Rehearsal | R1 blocker |
| D7 | Corrupt upload | Truncated file | Readable error, no stack trace (NFR-008) | Test | no API surface to upload to |
| D8 | Unsupported format | Wrong MIME/extension | Rejected with a reason | Test | same |
| D9 | No candidate conflict | Hand-built `Track` pair whose score falls below the `config.py:49` threshold | FR-017 wording verbatim; no manufactured event | Test | **Scoring half runs today** — `RiskEngine.evaluate` (`risk.py:157`) takes in-memory `Track` models and reads no files. The FR-017 string exists but is **not verbatim** — `orchestrator.py:181` emits "…visual-risk threshold in this clip." where FR-017 requires "…visual-risk threshold in the available evidence." The response surface is additionally blocked by the absent API layer |
| D10 | Insufficient temporal evidence | Single frame | `insufficient_temporal_evidence` state | Test — **expected to fail** | Unmet contract: §20 specifies `outcome`, `source`, and `temporal_evidence` as top-level record keys and §13 enumerates the four outcome states; `models.py:147` `Event` carries none of the three. §24.3 is the check that trips on the gap |
| D11 | Public access from a logged-out browser | Independent device, no session | Dashboard loads | Rehearsal = R5 | nothing deployed |

Non-§24.6 drills that still bite on the day:

- [ ] Restart from cold → how long to demo-ready? (feeds {{RESET_SECONDS}})
- [ ] Laptop switches / projector resolution changes
- [ ] Rooftop Wi-Fi fails → hotspot, then local replay, then the backup recording
      (FR-015's last rung)

## Rehearsals

| # | Date | Full run? | Broke on | Fixed |
|---|---|---|---|---|

No rehearsals yet. There is nothing end-to-end to rehearse.

> [!todo] Not filled in yet
> The rehearsal count is [[08-Definition-of-Done]]'s to set. Do not backfill a
> row from memory — a fabricated rehearsal is worse than an empty table.

---
Related: [[00-Source-of-Truth-PRD|PRD]] NFR-005 · §24.6 · §26.2 · §27.2 ·
FR-015 · FR-016 · [[01-Test-Strategy]] · [[02-Test-Cases]] · [[04-Demo-Script]] ·
[[06-Risk-Register]] · [[07-Provider-Adapters]] · [[05-Decision-Log]]
