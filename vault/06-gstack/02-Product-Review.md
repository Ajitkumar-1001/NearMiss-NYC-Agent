---
title: Product Review
tags:
  - gstack
status: active
---

# Product Review

Founder-mode review of what we're building. Run with `/plan-ceo-review`, or as
part of `/autoplan`. Findings below come from the drift audit of Tuesday
4 August and are hand-verified against the tree, not from a prior review pass.

## Checklist

- [ ] Can a stranger understand it in one sentence? → [[01-Project-Overview]]
- [ ] Is the problem real and evidenced? → [[02-Problem-Statement]]
- [ ] Is the MVP genuinely minimal? → [[04-MVP-Scope]]
- [ ] Does the demo tell a story, or just show features? → [[07-Demo-Story]]
- [ ] Would we be embarrassed by any claim in the pitch? → [[06-Success-Metrics]]

## Findings

| # | Finding | Severity | Action | Status |
|---|---|---|---|---|
| 1 | The vault documents a system whose HTTP layer does not exist. No tracked `.py` file references FastAPI, uvicorn, or `APIRouter`; there is no endpoint of any kind, including `GET /health`. Everything written about the API in [[05-API-Contracts]] and [[00-Source-of-Truth-PRD\|PRD]] §21 describes intent, not behaviour. | Blocker | Build the FastAPI app and `GET /health` today, ahead of any further documentation. Read every product note as a plan until then. | open |
| 2 | [[00-Source-of-Truth-PRD\|PRD]] §2.2 names Cloud Run deployment as the only stated eligibility gate. It is not met: nothing is deployed and no Dockerfile exists in the tree. A perfect local product is not hackathon-complete. | Blocker | Deploy the health skeleton and verify from a logged-out browser. This is step 5–6 of §27.1's Tuesday list. | open |
| 3 | The guaranteed fallback cannot run. `demo/fixtures/` contains only `README.md`, while the code reads `detections.json`, `tracks.json`, and `context.json`. The captured-replay demo — the thing that is supposed to work when everything else fails — cannot complete a single run today. | Blocker | Produce the captured evidence baseline per [[00-Source-of-Truth-PRD\|PRD]] §11.1 before Thursday 8:00 PM. | open |
| 4 | Zero of the six judge-facing surfaces in [[00-Source-of-Truth-PRD\|PRD]] §11.3 exist. `app/frontend/` holds only `README.md`. The demo story in [[07-Demo-Story]] and the script in [[04-Demo-Script]] currently describe a screen nobody can open. | Blocker | Treat the six surfaces as one deliverable, not six. Do not polish subcomponents; §11.3 says separate polish is not an acceptance criterion. | open |
| 5 | `vision-conflict-analytics` ([[00-Source-of-Truth-PRD\|PRD]] FR-022, §11.1) does not exist and is not pinned. It is a §26.1 arrival-gate item and an explicit Roboflow-facing artifact under §2.4, and it is also the largest optional-looking item on the plan. | High | Decide explicitly whether it ships or is cut, and log the call in [[05-Decision-Log]]. Do not let it drift. | open |
| 6 | The real-source path — the reason §1.1 promoted real-feed analysis to P0 — is not started. FR-001 source registry, FR-002/FR-004 source adapter, and FR-003 provenance and freshness do not exist. "Working demo on a real NYC feed" is not currently a claim we can make. | Blocker | Land the source registry and one adapter Wednesday. Until then the pitch says captured evidence, honestly labelled. | open |
| 7 | Documentation volume is far ahead of implementation. Extensive architecture, evaluation, and pitch notes describe a system that is 1,039 lines with no network I/O and no HTTP surface — the only I/O is `load_fixture` reading committed JSON from disk (`providers/base.py:48`) plus env-var lookups. The risk is believing the vault instead of the tree. | High | Every claim in [[06-Success-Metrics]] and [[02-2-Minute-Pitch]] gets checked against a running deployment before Friday, not against a note. | open |
| 8 | No tests exist. `tests/` contains only `README.md`. [[01-Test-Strategy]] and [[02-Test-Cases]] describe coverage that has never run. | High | Do not claim tested behaviour in the pitch or README. Add tests alongside the HTTP layer, not after. | open |

> [!warning] The honest read
> The offline core is genuinely good — the risk engine, the models, the
> orchestrator's fallback ladder, the provider Protocols, and the deterministic
> explanation builder are in place and correct. The fixture side of every
> provider works; the runtime side is not built — Roboflow detection, ByteTrack
> tracking, and the NYC Open Data lookup all decline unconditionally today. On
> top of that, everything that turns the core into a product a judge can reach
> is missing: a server, a deployment, fixtures, and a UI. The product is not
> behind on thinking. It is behind on shipping.

---
Related: [[01-Workflow]] · [[01-Project-Overview]] · [[04-MVP-Scope]] · [[07-Demo-Story]]
