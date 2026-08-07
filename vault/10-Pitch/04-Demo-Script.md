---
title: Demo Script
tags:
  - pitch
status: active
---

# Demo Script

Exact clicks and words. The story behind it is [[07-Demo-Story]].

> [!info] Source
> [[00-Source-of-Truth-PRD|PRD]] §12.2's golden demo flow, twelve beats, in
> order. The fallback column is FR-015's ladder — one rung per step. §26.1
> requires this script to exist before arrival; §27.1 item 20 finalizes it.

> [!warning] Steps 3–5 are written against the target state
> The live path needs a FastAPI surface and a source adapter, and neither exists
> yet ([[04-Task-Board]] B-1, W-13). Until they do, the honest run is steps 1–2
> then 6–12 with the mode badge reading captured, and the fallback column is what
> is actually reachable. Do not rehearse a live beat that cannot run — FR-016
> forbids presenting fallback operation as live inference.

## Pre-flight

- [ ] Deployed URL open in a logged-out browser profile — proves NFR-002 without
      saying a word about it
- [ ] Captured replay verified once on this machine, this hour
- [ ] Network off for the replay rehearsal (§11.1: the captured path runs without
      runtime external APIs)
- [ ] Browser zoom and resolution set for the projector
- [ ] Notifications silenced; second screen mirrored, not extended
- [ ] Backup recording open in a background tab ([[05-Demo-Reliability]] mode E)

## Steps

Target is under two minutes (§12.2). Times are cumulative.

| # | Time | Action | Say | Expected on screen | Fallback if it breaks |
|---|---|---|---|---|---|
| 1 | 0:00 | Open the deployed dashboard | "This is running on Cloud Run, public URL, no login." | Service status and deployed revision | Second browser/device already loaded on the same URL; last resort, the recording |
| 2 | 0:10 | Point at the Source and Mode header | "{{SOURCE_NAME}}, retrieved at the timestamp shown. The badge tells you which mode is active." | Source id, attribution, retrieval time, freshness, one mode badge | If freshness is stale, say so out loud — a stale label is a correct label |
| 3 | 0:20 | Click **Analyze live source** | "Fetching the current frame now." | Fetching state, then perception state | Live source → captured evidence sequence (FR-015 rung 1); badge changes, say it changed |
| 4 | 0:30 | Let detections render | "Roboflow detections on a frame that did not exist a minute ago." | Boxes and labels on the real frame | Roboflow → stored detections (rung 2); label it as stored |
| 5 | 0:40 | Read the outcome aloud, whatever it is | "One frame is not enough for trajectories, so it says insufficient temporal evidence rather than inventing an alert." | `insufficient_temporal_evidence` or `no_candidate_conflict` | **This step cannot fail.** Every §12.4 outcome is a valid result; a quiet answer is the point |
| 6 | 0:50 | Click **Replay evidence case** | "Now the reproducible case, so you can see the whole path." | Replay starts within 2 s (NFR-006) | Tracker runtime → precomputed tracks (rung 3); already the P0 path |
| 7 | 1:00 | Let the sequence play | "Two tracked road users, trails behind them, and the pair the engine picked out." | Boxes, trajectory trails, candidate pair marked | If trails misalign, name it as a known limit and move on — do not debug on stage |
| 8 | 1:15 | Point at the risk panel | "{{RISK_SCORE}} out of 100 — and every part of it is on screen: proximity, path overlap, closing motion, vulnerable-user weighting. It is a visual proxy, not a crash probability." | Score plus the four named factors | Score without factors is not a demo — cut to step 10 rather than show an opaque number |
| 9 | 1:30 | Point at the context card | "Reported collisions near this location, from NYC Open Data, cached and dated — beside the score, never inside it." | Dataset, radius, time window, retrieval time | NYC Open Data → cached context (rung 4); the run survives its absence, just say the card is missing |
| 10 | 1:40 | Point at the explanation | "Observations, limitations, and a human-review recommendation. It says what it does not know." | Explanation, ≥1 limitation, recommended action | Gemini → deterministic template explanation (rung 5); the template **is** the P0 path |
| 11 | 1:50 | Veris scenario result — **only if confirmed and already passing** | "One reliability scenario, ten seconds." | A pass/fail artifact | Skip silently. §2.4: never mention an unimplemented integration |
| 12 | 1:55 | Close | "No face recognition, no plate recognition, no identity inference, no automated enforcement. It hands a human the evidence and the uncertainty." | — | None needed — say it even if everything else broke |

## If the whole thing fails

Descend the ladder out loud, never silently ([[05-Demo-Reliability]] modes A–E):

1. Live path dies → captured replay, badge changes, say it changed
2. Deployed service dies → same replay on localhost, say it is local
3. Machine dies → backup recording, announced as a recording, never as a live run

The one sentence that recovers any of it: **"That is the fallback doing its job —
every one of them is labelled, which is the point."**

## Rehearsal log

§26.2 wants three consecutive successes from the deployed URL;
[[08-Definition-of-Done]] wants two clean end-to-end rehearsals.

| # | Date | Ran from | Full run? | Broke on | Time |
|---|---|---|---|---|---|
| | | | | | |

> [!caution] Do not backfill a row
> An invented rehearsal is worse than an empty table — it is the one thing here
> that would make every other claim suspect.

---
Related: [[07-Demo-Story]] · [[05-Demo-Reliability]] · [[02-2-Minute-Pitch]] · [[05-QA-Checklist]] · [[00-Source-of-Truth-PRD|PRD]] §12.2 · §12.4 · FR-015 · FR-016
