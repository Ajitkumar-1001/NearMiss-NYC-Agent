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

> [!success] Rewritten Friday 5:15 PM against the deployed service
> Every number, label, and button name below was read off
> `https://nearmiss-nyc-711121860771.us-east1.run.app` (revision
> `nearmiss-nyc-00002-7xb`, git `f128a2d`). No placeholders remain and no beat
> requires anything unbuilt.
>
> **There is no live-inference beat, because there is no source adapter.** The
> "Analyze live source" button returns the fixture pipeline and says so. FR-016
> forbids presenting fallback operation as live inference, so the script below
> makes the fallback the point rather than hiding it — which is also the direct
> answer to the organizers' own warning that cameras go offline.

## Pre-flight

- [ ] Deployed URL open in a **logged-out** browser profile — proves NFR-002
      without saying a word about it
- [ ] Page loaded once already, this hour, from the venue wifi
- [ ] Browser zoom and resolution set for the projector; the canvas should fill
      the screen without scrolling
- [ ] Notifications silenced; second screen mirrored, not extended
- [ ] Backup recording open in a background tab ([[05-Demo-Reliability]] mode E)
- [ ] Phone hotspot ready — venue wifi is the single point of failure for a
      demo that lives on a public URL

## Steps

Target is under two minutes (§12.2). Times are cumulative.

| # | Time | Action | Say | Expected on screen | Fallback if it breaks |
|---|---|---|---|---|---|
| 1 | 0:00 | Open the deployed dashboard, logged out | "This is on Cloud Run, public URL, no login. Revision `f128a2d`." | Header badges: `SERVICE OK` · `REVISION F128A2D` · `V0.1.0` · `SOURCES 1` | Second device already loaded on the same URL; last resort, the recording |
| 2 | 0:10 | Point at the four amber notices | "Before anything else — the system is telling you what it could not do. No Roboflow key, so detection fell back to committed fixtures. It labels that itself." | Four amber notice bars, `MODE DEMONSTRATION FIXTURE` | These always render; they are part of the response contract, not debug output |
| 3 | 0:20 | Click **Analyze live source** | "Same honesty on the live path. It does not pretend a fixture is a camera." | Same four notices, mode badge unchanged | If it errors, say so and click **Replay evidence case** — step 4 onward is unaffected |
| 4 | 0:30 | Say the fallback line | "Your slide said don't hardcode one camera and pray. This is what handling it looks like: four independent fallbacks, each one labelled in the payload and on screen." | — | None. This beat is words, not software |
| 5 | 0:45 | Point at the vision canvas | "A car and a pedestrian, tracked across twelve seconds. The bold trails are the pair the engine flagged; the thin boxes are per-frame detections." | Blue horizontal trail (car #1), red vertical trail (person #2), crossing | If the canvas is blank, describe the numbers instead and move to step 6 — do not debug on stage |
| 6 | 1:00 | Point at the risk panel | "84.3 out of 100 — and every part of it is on screen. Proximity 0.78, path overlap 0.99, closing motion 0.62, vulnerable user 1.0. It is a visual conflict proxy, not a crash probability." | Score `84.3`, `HIGH` badge, four factor bars | Score without factors is not a demo — skip to step 8 rather than show an opaque number |
| 7 | 1:20 | Point at the context card | "Fourteen reported collisions within 150 metres. Beside the score, never inside it — correlation, not cause. And it is labelled `synthetic_placeholder`, because it is." | Source, count, radius, retrieval timestamp | The run survives its absence; just say the card is missing |
| 8 | 1:35 | Point at the explanation and limitations | "Observations, a human-review recommendation, and three limitations it volunteered — including that the camera is not calibrated and the demo sequence is synthetic." | Observations list, recommended action, limitations card | The template **is** the P0 path; it cannot be unavailable |
| 9 | 1:50 | Close on privacy | "No face recognition, no plate recognition, no identity inference, no automated enforcement. Track IDs are local to this clip and never correlated across cameras. It hands a human the evidence and the uncertainty." | Privacy card | None needed — say it even if everything else broke |

## The question you will be asked

**"Is this running on a real NYC camera?"** — No. Answer it directly, in one
breath, without flinching:

> "No. The perception pipeline is real, the risk engine is real, and it is
> deployed and public. The sequence is synthetic, and the service says so in
> four places before you ask. What is missing is a source adapter — one provider
> class. Everything downstream of it is built and running."

Do not soften it, do not bury it, and do not let it be discovered. A volunteered
limitation reads as engineering judgement; the same fact extracted under
questioning reads as a cover-up. §21.6 and [[01-Constitution]] principle 7 both
say the quiet part out loud is the product.

Related questions worth one sentence each:

- *"Why no live feed?"* — "Three hours of build time. We spent it on the
  eligibility gate, the evidence pipeline, and the disclosure layer."
- *"So the score is meaningless?"* — "The score describes the sequence it was
  computed on. It is an image-space proxy, and the frame geometry is fixed at
  1280×720 — a different camera needs the calibration knobs retuned before its
  numbers mean anything. That is in the README."
- *"What would you do next?"* — "Wire one 511NY still through the Roboflow
  adapter. The registry in `sources.py` is a list of literals precisely so that
  is a configuration change, not an architecture change."

## If the whole thing fails

Descend the ladder out loud, never silently ([[05-Demo-Reliability]] modes A–E):

1. Deployed service dies → same page on localhost, say it is local
2. Venue wifi dies → phone hotspot, keep talking while it reconnects
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
