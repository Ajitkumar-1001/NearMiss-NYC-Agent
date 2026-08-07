---
title: Sponsor Resources
tags:
  - event
status: active
---

# Sponsor Resources

> [!info] Filled from the PRD
> Integration *policy* is [[00-Source-of-Truth-PRD|PRD]] §2.4 and is locked. What each sponsor
> actually hands out on the day is not — those rows stay `{{PLACEHOLDER}}`
> until kickoff.

## The three named parties

Each has a different status in the build. Confusing them is how a runtime
dependency gets created by accident.

| Sponsor | Status in P0 | Policy |
|---|---|---|
| **Google Cloud** | **Mandatory infrastructure.** Cloud Run is the eligibility gate | §2.2, §2.4 |
| **Roboflow** | **Preferred perception provider.** P0 demonstrates inference on ≥1 real NYC frame where credentials and availability permit | §2.4, §29 |
| **Veris AI** | **Conditional evaluation-plane integration.** Co-host. Not a runtime dependency | §2.4, §29 |

### Google Cloud

Cloud Run is P0 and non-negotiable — see [[ADR-007-Cloud-Run-Eligibility-Gate]].
**Gemini is optional P1** and §2.4 states it shall never replace the
deterministic P0 explanation.

Account is a personal-Gmail project with billing enabled ([[00-Source-of-Truth-PRD|PRD]] §11.1) —
an execution inference, not a sponsor offer. Any attendee credit is
{{GCP_ATTENDEE_CREDIT}}.

### Roboflow

RF-DETR via Workflow or hosted inference (§17 preference order). Stored
normalized detections remain the fallback for the captured evidence case.

**Roboflow MCP and Computer Vision Skills are development-plane accelerators
only** (§29, FR-020) — never runtime infrastructure. Mixing that up would put a
dev tool on the demo's critical path.

Account creation and API-key validation were due **Tuesday 4 August** because
Wednesday's evidence work depended on them ([[00-Source-of-Truth-PRD|PRD]] §1.3 item 5).
Today is Thursday 6 August and they are **two days overdue** — the runtime
detection rung is still unconfigured, which is why the replay path runs on a
synthetic fixture rather than a Roboflow-derived capture.

Open question on the upstream contribution path:
[[Roboflow-Upstream-Path]]. Mentor questions: [[06-Roboflow-Mentor-Conversation]].

### Veris AI

Co-host — source-supported. **A dedicated Veris prize track or mandatory
integration is unverified, and §2.1 says do not claim it.**

§2.4 sets a 30-minute gate: integrate only if support is confirmed *and* the
work fits without consuming contingency time. Otherwise skip it and say nothing.
Full reasoning and the three kickoff questions: [[Veris-Integration]].

## Sponsor prize tracks

- [ ] Which tracks are we eligible for? — {{PRIZE_TRACKS}}, unverified
- [ ] Does any track require a specific integration?

Only one integration is *required* by anything we know: Cloud Run, and that is
an eligibility gate rather than a prize track. Everything else stays behind
[[07-Provider-Adapters]] so a late requirement swaps an adapter rather than
reshaping the pipeline — that is what
[[ADR-003-Provider-Adapter-Architecture]] bought.

## Keys and access

Credentials go in `.env`, never committed — template in `.env.example`.

| Key | Adapter | Needed by | Obtained? |
|---|---|---|---|
| Google Cloud / `gcloud` auth | deployment | pre-event (§11.1) | [ ] |
| Roboflow API key | vision | **Tuesday 4 Aug** (§1.3) | [ ] |
| NYC Open Data app token | context | optional; raises throttle | [ ] |
| 511NY developer key | source | pre-event if used (§18.1) | [ ] |
| Gemini API key | explanation | P1 only | [ ] |
| Veris — {{VERIS_CREDENTIAL}} | evaluation | only if confirmed | [ ] |

> [!warning] §18.3 excludes untestable sources
> Any credential that cannot be obtained and **tested before Friday** puts its
> source in the prohibited-at-P0 list. Getting a key at the venue is not a plan.

Which key belongs to which adapter is recorded in [[07-Provider-Adapters]].

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[01-Event-Brief]] · [[07-Provider-Adapters]] · [[03-Judging-Criteria-Map]] · [[Veris-Integration]] · [[Roboflow-Upstream-Path]] · [[06-Hackathon-Compliance-Checklist]]
