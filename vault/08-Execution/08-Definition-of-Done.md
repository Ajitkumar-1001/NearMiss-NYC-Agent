---
title: Definition of Done
tags:
  - execution
status: active
---

# Definition of Done

A task is done when **every** box is ticked. No partial credit.

- [ ] Behaviour matches its acceptance criterion in [[04-MVP-Scope]]
- [ ] Works on the fixture path with the network off
- [ ] Has a case in [[02-Test-Cases]] and it passes
- [ ] No new console errors on the demo path
- [ ] Provider failures degrade gracefully → [[07-Provider-Adapters]]
- [ ] Committed, pushed, and running on a teammate's machine
- [ ] [[04-Task-Board]] updated

## P0 — the three §26 gates

> [!info] Source
> [[00-Source-of-Truth-PRD|PRD]] §26, which is **three separate gates with
> different deadlines**, not one list. This note previously merged them into 21
> items and dropped eleven — including both `vision-conflict-analytics` checks,
> the six judge-facing surfaces, the architecture diagram, the demo script, the
> three consecutive deployed golden runs, and §26.3 entirely.
> Restored below at full count: **15 + 12 + 5 = 32**.

### §26.1 — Arrival gate, green **before Friday**

- [ ] Public Cloud Run health skeleton is deployed
- [ ] Public URL works from a logged-out browser
- [ ] `GET /health` returns HTTP 200
- [ ] Service binds to `0.0.0.0:$PORT`
- [ ] At least one NYC source adapter has fetched a current image
- [ ] Roboflow perception has been tested on the selected source or a source-compatible sample
- [ ] Captured evidence sequence and source attribution are committed
- [ ] Normalized detections, tracks, trajectories, candidate pair, and risk fixtures are committed
- [ ] Public `vision-conflict-analytics` repository, tests, license, and immutable release/commit exist
- [ ] NearMiss imports a pinned package version and contains no duplicate private scoring implementation
- [ ] Captured replay works without external APIs
- [ ] Cached NYC context and deterministic explanation are committed
- [ ] Six required judge-facing surfaces render
- [ ] Public repo, README skeleton, architecture diagram, and permissive license exist
- [ ] Two-minute demo script exists

> [!danger] The first nine are the hard subset
> §26.1: "If any of the first nine checks is red, the project is not ready for
> optional sponsor integrations or design expansion." That is checks 1–9 above,
> and it is a stricter rule than the §11.1 two-baseline readiness gate — it
> reaches the package checks, which §11.1's two baselines do not.

**Verified so far** — Thursday 6 August, 12:10 ET:

| Check | State | Evidence |
|---|---|---|
| 11 — captured replay without external APIs | **green** | 10/10 identical runs, `nmyc_demo_001`, risk 84.3, severity high. Every runtime provider declines by construction, so no network path is exercised |
| 8 — fixtures committed | **staged, not committed** | `git ls-files demo/fixtures` lists all three; commit still owed |
| 7 — sequence *and source attribution* | **red** | The fixture is synthetic — `sources.py` attributes it "Not camera footage and not attributed to any NYC source". §11.1 wants a 10–20 s source-attributed NYC sequence |
| 15 — demo script exists | **green** | [[04-Demo-Script]] |

Everything not listed is untouched. Do not tick a box from this table — tick it
when you have run the check yourself.

### §26.2 — Submission gate, green **by 8:15 PM Friday**

- [ ] Public Cloud Run revision is reachable and identified
- [ ] Real NYC source is configured, attributed, and analyzed through the deployed service
- [ ] Live result shows source, retrieval time, freshness, provider, and processing mode
- [ ] No-conflict and insufficient-evidence states behave truthfully
- [ ] Captured evidence replay shows the supported candidate conflict and risk-factor breakdown
- [ ] Context, explanation, limitations, and privacy boundary are visible
- [ ] Every fallback is labeled
- [ ] README contains final source, deployment, run, demo, limitation, reusable-package, and pre-existing-code disclosure details
- [ ] Backup recording and screenshots exist locally
- [ ] Public repo and Cloud Run URL are placed in the submission form
- [ ] Golden demo succeeds three consecutive times from the deployed URL
- [ ] Submission is ready by 8:15 PM, leaving fifteen minutes before the 8:30 PM lock

### §26.3 — Conditional Veris completion

Complete only when **all five** are true. Failing this subsection does **not**
make NearMiss incomplete unless organizers announce a Veris eligibility
requirement (§26.3, [[Veris-Integration]]).

- [ ] Organizers or Veris staff confirm the integration or prize value
- [ ] Account/tool access already works
- [ ] The scenario pack runs without changing the production pipeline
- [ ] A result artifact is available
- [ ] The work did not consume protected contingency time

## For the project

- [ ] [[05-QA-Checklist]] fully passed
- [ ] [[04-Demo-Script]] rehearsed twice end-to-end
- [ ] Every claim in [[02-2-Minute-Pitch]] traces to a measured row in [[06-Success-Metrics]]
- [ ] Reliability gates in [[05-Demo-Reliability]] met — NFR-005's five counts, of
      which **R1 (10/10 local) passed at 12:10 ET Thursday**
- [ ] Submission requirements met → [[01-Event-Brief]]

---
Related: [[00-Source-of-Truth-PRD|PRD]] §26.1 · §26.2 · §26.3 · [[04-MVP-Scope]] · [[05-QA-Checklist]] · [[02-Test-Cases]] · [[04-Task-Board]] · [[05-Demo-Reliability]]
