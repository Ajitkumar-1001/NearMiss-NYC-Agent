---
title: Constitution
tags:
  - speckit
status: active
---

# Constitution

Non-negotiable principles for this build. When a decision is contested, this
note wins.

## Principles

1. **Eligibility before everything.** [[00-Source-of-Truth-PRD|PRD]] §2.2 is the
   only stated disqualifier — it lists five conditions on the deployed Cloud Run
   service, all of which must hold. Read them there; don't copy them here. It is
   pass/fail — nothing else scores if it fails, so it outranks every principle
   below it. Today no FastAPI application exists, no endpoint exists, and nothing is
   deployed. Until that is false, work that is not on this path is out of order.
2. **The demo works offline.** Captured-feed replay is the guaranteed conflict
   demonstration and the network-failure fallback — [[00-Source-of-Truth-PRD|PRD]]
   §29. `demo/fixtures/` now holds `detections.json`, `tracks.json`, and
   `context.json`, and the pipeline completes end-to-end on them: score 84.3,
   severity `high`, mode `demonstration_replay`, all four providers stepped down
   to their fixture rung. The sequence is **synthetic**, not a source-attributed
   NYC capture, so §11.1's captured-evidence baseline is *runnable* but not yet
   *satisfied* — and `context.json` carries `source: synthetic_placeholder`
   rather than a real NYC Open Data figure.
3. **Vendors are replaceable.** All external calls behind adapters —
   [[00-Source-of-Truth-PRD|PRD]] §29. `nearmiss/providers/base.py` defines the
   three Protocols and `ProviderUnavailable`; `vision.py`, `tracking.py`, and
   `context.py` each pair a fixture implementation that works with a runtime
   implementation that declines — `RoboflowVision.detect`,
   `ByteTrackTracker.track`, and `NycOpenDataContext.lookup` all raise
   `ProviderUnavailable(..., "… not implemented at P0")`. The runtime side of
   every boundary is not yet built. Changing a Protocol signature is an
   architecture change, not a chore.
4. **Honest claims only.** No number in the pitch that isn't measured in
   [[06-Success-Metrics]].
5. **State the limits.** The conflict score is an image-space proxy, not
   collision probability — [[00-Source-of-Truth-PRD|PRD]] §29 and
   [[05-Safety-Methodology]]. §23 item 10 additionally requires observed
   evidence, derived metrics, public context, and generated explanation to stay
   separate from one another.
6. **Cut scope, not quality.** When time runs out, drop features via
   [[03-Scope-Ladder]] and [[00-Source-of-Truth-PRD|PRD]] §11; don't ship a
   broken version of everything.
7. **Never claim something is built that is not.** A plan written against an
   overstated status is worse than no plan: it silently drops the unbuilt work
   from the schedule and nobody notices until the demo. Three registers, never
   blurred: *the PRD requires X* / *`file.py` does Y* / *not yet built*. Before writing
   any status, open the file. A checkbox is ticked by a command that ran, not by
   intent.

## Amending

Changing a principle requires an entry in [[05-Decision-Log]]. If it constrains
the build it needs two things in the same change: an ADR in `07-Decisions/` and a
locked entry in [[00-Source-of-Truth-PRD|PRD]] §29, filed through the §31
change-control protocol with a version increment — §31 item 6 requires the ADR
reference, and §31's governance state requires [[00-ADR-Index]] to point at the
active decisions. ADR-008 through ADR-010 are retired; next free number is
ADR-011.

The PRD is frozen at v2.1.0 before the event (§31). Onsite, organizer answers,
source selections, and bounded scope cuts go to [[05-Decision-Log]] — not into a
new PRD version.

---
Related: [[02-Workflow]] · [[00-Source-of-Truth-PRD|PRD]] §29 · [[05-Decision-Log]] · [[08-Definition-of-Done]]
