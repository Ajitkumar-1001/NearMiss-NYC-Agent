---
title: Deployment
tags:
  - architecture
status: active
---

# Deployment

## Targets

| Piece | Host | URL | Deployed by |
|---|---|---|---|
| Frontend | Either a separately deployed Next.js app or a lightweight frontend served by the Cloud Run service — [[00-Source-of-Truth-PRD\|PRD]] §16.1 leaves the choice open and states the dashboard's location is **not** the eligibility gate | {{FE_URL}} | {{FE_DEPLOY_MECHANISM}} |
| Backend | Google Cloud Run, public endpoint, FastAPI — [[00-Source-of-Truth-PRD\|PRD]] §16.1 "Mandatory agent service" | {{BE_URL}} | `gcloud` CLI; §27.1 requires the deploy and rollback commands to be recorded on Tuesday, August 4 |

The gate itself lives in [[00-Source-of-Truth-PRD|PRD]] §2.2 and is locked in §29
("Public Google Cloud Run agent is mandatory") — not restated here. See
[[06-Hackathon-Compliance-Checklist]].

- [ ] Deploy the `GET /health` skeleton **first, before choosing a topology** —
  §16.1 leaves the dashboard's location open, so one container or two is a free
  implementation call, made on whichever produces a public URL soonest. Nothing
  about the topology needs settling before the gate is cleared.

> [!todo] Both URLs are still unknown
> They exist only once the service is deployed. §11.1's deployment baseline
> requires the public URL to be verified from a logged-out browser before the
> event, so both cells should be filled the same day the deploy happens.

> [!warning] There is no HTTP layer in the backend yet
> `app/backend/pyproject.toml` declares `fastapi` and `uvicorn[standard]` as
> dependencies, but nothing under `app/backend/nearmiss/` imports either one —
> there is no app module, no route, and no `GET /health` handler. The pipeline
> in `nearmiss/orchestrator.py` is importable Python, not a service. No
> Dockerfile exists anywhere under `app/`. Everything below marked "PRD
> requires" is therefore a requirement against code that is not yet built.

## Environments

- **Local** — §11.1's captured-evidence baseline requires the captured replay to
  work *without runtime external APIs*; §29 locks captured-feed replay as the
  guaranteed conflict demonstration and fallback, and JSON fixtures and captured
  assets as operational fallbacks. That is the accurate constraint — neither §29
  nor §11.1 says "no network", they say the guaranteed path must not depend on
  runtime providers.
  The ladder is wired: `providers/vision.py`, `providers/tracking.py`,
  `providers/context.py`, and `providers/explanation.py` each pair a runtime class
  with a fixture class, and `nearmiss/orchestrator.py` catches `ProviderUnavailable`
  at each rung and steps down. What is missing is the data the ladder lands on.
  With no credentials set every rung steps down and then dies: `demo/fixtures/`
  holds only `README.md` — no `detections.json`, no `tracks.json`, no
  `context.json` — so `load_fixture()` raises `FileNotFoundError` and the pipeline
  does not complete a single run. §11.1's captured-evidence baseline is therefore
  red, and the wiring has never survived a real run. See [[07-Provider-Adapters]].
- **Deployed** — for judges to click after the pitch. §11.1 requires the public
  service, `GET /health` returning 200, and `0.0.0.0:$PORT` binding to be
  verified *before arriving at the venue*; §27.1 schedules that as the first
  thing on the critical path, ahead of all product work.

## Configuration

NFR-001 sets the container contract the ingress service must satisfy. None of it
is implemented — nothing under `nearmiss/` reads `$PORT` or binds a socket, and
the package contains no match for `fastapi`, `uvicorn`, `PORT`, or `0.0.0.0`.

What the code does configure today:

- `nearmiss/config.py` defines `Settings` on `pydantic-settings` with
  `env_prefix="NEARMISS_"` and `extra="ignore"`. It carries the environment name,
  the candidate threshold and severity cut, the risk-factor weights, the
  normalisation and evidence-quality knobs, the vulnerable/vehicle class sets, and
  `fixture_dir`. Every field has a default, so the pipeline starts with no
  environment at all.
- `nearmiss/orchestrator.py` reads four credentials directly with `os.getenv`,
  **unprefixed**: `ROBOFLOW_API_KEY`, `ROBOFLOW_MODEL_ID`,
  `NYC_OPEN_DATA_APP_TOKEN`, `GEMINI_API_KEY`. These bypass `Settings` and its
  `NEARMISS_` prefix. Two configuration mechanisms currently coexist; that is
  unresolved, not a design.
- The vault-root `.env.example` is still a commented scaffold and names none of
  those four variables. Aligning it with what `orchestrator.py` actually reads is
  outstanding work.

Statelessness holds so far by accident of scope: `config.py` resolves
`fixture_dir` to `demo/fixtures/`, which currently holds only its `README.md`
placeholder; `providers/base.py` `load_fixture()` opens read-only; and nothing in
the package writes to disk or opens a temporary file — the sole `open(` anywhere
in `nearmiss/` is `path.open()` at `providers/base.py:60`.

Deployment strategy is NFR-003; cost posture is NFR-012. Neither is exercised
yet, because nothing is deployed.

Two deploy-time settings need confirming against the PRD once a revision exists:

- [ ] CORS and API base-URL handling, **if** the dashboard deploys separately —
  moot if it is served by the same Cloud Run service
- [ ] Cloud Run request timeout clears the 60 s NFR-006 budget

> [!warning] No authentication
> NFR-002 requires the agent to be public — via `--allow-unauthenticated` or
> `--no-invoker-iam-check` — and prefers a personal-Gmail project to avoid
> organization-level domain-restricted-sharing blockers. §29 locks "no
> authentication" as an architectural decision. Anything deployed is therefore
> readable by anyone with the URL. Do not deploy anything with real personal data
> in it; NFR-011's privacy boundaries and NFR-010's secret handling are what keep
> that true.

## Rollback

- [ ] How do we get back to the last working build fast? → [[05-Demo-Reliability]]

§11.1's deployment baseline requires a **known-good revision and rollback command
recorded** as part of pre-event readiness, and §27.1 puts recording the deploy and
rollback commands on Tuesday, August 4. Neither the revision nor the command is
recorded anywhere in this vault yet, so the box stays unchecked. Fill it with the
literal command, not a description of one — under §27.2's 7:00 PM freeze there is
no time to reconstruct it.

Cloud Run's own revision history is the mechanism §2.2 leans on when it requires
the service to identify its deployed revision. The `Health` model in
`nearmiss/models.py` is short of FR-019 — no revision field, no source count — and
no handler exists to serve it either way. Shape: [[06-Data-Model]]. Endpoint
contract: [[05-API-Contracts]].

---
Related: [[00-Source-of-Truth-PRD|PRD]] §2.2 · §11.1 · §16.1 · §29 · FR-019 · NFR-001 · NFR-002 · NFR-003 · NFR-006 · NFR-012 · [[06-Hackathon-Compliance-Checklist]] · [[05-Demo-Reliability]] · [[07-Provider-Adapters]] · [[05-API-Contracts]] · [[06-Data-Model]] · [[09-Observability]]
