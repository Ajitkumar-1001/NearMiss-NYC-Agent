# NearMiss NYC

**See the risk before it becomes a crash statistic.**

An explainable vision agent for NYC street-safety review. NearMiss NYC turns
camera frames into source-attributed, reviewable candidate-conflict events —
detecting road users, deriving temporal evidence, scoring vehicle-to-vulnerable-
road-user conflicts against a transparent visual proxy, enriching with NYC public
data, and producing a structured report for human review.

Built for **NYC Vision Hack v.2**, 7 August 2026.

> **The risk score is an image-space visual conflict proxy, not a crash
> probability.** It measures how close two tracked objects came in the image
> plane and how their paths converged. It does not model intent, right of way,
> occlusion, or real-world distance, and it must not be read as a prediction that
> a collision would have occurred.

---

## The problem

Road-safety decisions lean on lagging indicators — reported crashes, injuries,
complaints. Those records matter, but they describe harm after it has happened.

Street-camera footage often contains earlier signals: vehicles and cyclists
repeatedly converging at a turn, pedestrians entering a conflict zone while
traffic keeps moving, rapidly decreasing image-space separation. Reviewing that
footage by hand is slow and inconsistent, and conventional detection dashboards
count objects without producing event-level evidence, disclosing uncertainty, or
explaining why an interaction deserves review.

NearMiss NYC produces the evidence, and says plainly how confident it is.

---

## Architecture

One orchestrated pipeline — not a multi-agent council. `Orchestrator.run()` is a
single linear sequence:

```
detect → track → score → threshold → context → explain
```

```
app/backend/nearmiss/
├── main.py           FastAPI surface — translates pipeline output to JSON, no risk logic
├── orchestrator.py   The pipeline and the fallback ladder; decides the processing mode
├── risk.py           RiskEngine — pairwise trajectory analysis and factor scoring
├── models.py         Pydantic v2 schemas (extra="forbid" — payloads are exact)
├── sources.py        The approved-source registry; carries no credentials
├── config.py         Settings, risk weights, calibration knobs
└── providers/
    ├── base.py       ProviderUnavailable — the contract every adapter degrades through
    ├── vision.py     Roboflow (runtime) → committed fixture detections
    ├── tracking.py   ByteTrack (runtime) → committed fixture tracks
    ├── context.py    NYC Open Data (runtime) → cached context
    └── explanation.py Gemini (runtime) → deterministic template
```

### The fallback ladder

Every external dependency has a rung beneath it. A failure at any level steps
down rather than corrupting the level below — each step-down is a caught
`ProviderUnavailable`, never a partially-built event:

| Stage | Runtime | Fallback |
|---|---|---|
| Detection | Roboflow RF-DETR | precomputed detections |
| Tracking | ByteTrack | precomputed tracks |
| Context | NYC Open Data | cached public-data context |
| Explanation | Gemini | deterministic template |

The bottom rung needs no network at all, which is what makes the demo path
guaranteed. Whichever rung served is disclosed in the response's
`processing_mode` and `notices` — the system never presents a replay as a live
analysis.

### Risk scoring

A transparent weighted sum, not a learned model. Weights are FR-006's reference
weighting and sum to 1.0:

| Factor | Weight |
|---|---|
| Proximity | 0.35 |
| Path overlap | 0.35 |
| Closing motion | 0.20 |
| Vulnerable user involved | 0.10 |

Candidate threshold 70; `high` severity at 80. All configurable via
`NEARMISS_`-prefixed environment variables. A pair is not evaluated at all unless
both tracks clear the evidence-quality guards (`min_track_points`,
`min_overlap_seconds`) — this is what stops detection jitter from manufacturing
events.

---

## API

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Liveness, version, deployed revision, per-provider readiness |
| `GET` | `/api/v1/sources` | The approved-source registry |
| `GET` | `/api/v1/demo` | Deterministic captured-evidence replay — no network required |
| `POST` | `/api/v1/live/{source_id}/analyze` | Analyse a registered source |

`/health` returns HTTP 200 even when degraded — the degradation is reported in
the body so Cloud Run's health checking stays meaningful.

---

## Data sources

The registry in `app/backend/nearmiss/sources.py` is the single list of approved
inputs. Nothing in it carries a credential; `/api/v1/sources` serves those objects
verbatim to unauthenticated callers.

| Source | Kind | Attribution |
|---|---|---|
| `demo_fixture` | fixture | **Synthetic sequence generated for the deterministic demo path. Not camera footage and not attributed to any NYC source.** |

The approved live-data strategy is organizer starter feeds, accessible NYC camera
still endpoints, or 511NY REST cameras. The system does not depend on any signed
bulk-feed agreement.

---

## Setup

Requires Python ≥ 3.11.

```bash
pip install -e "app/backend[dev]"
uvicorn nearmiss.main:app --host 0.0.0.0 --port 8080
```

Then `curl localhost:8080/api/v1/demo`.

No credentials are needed to run the demo path — every runtime provider declines
cleanly and the pipeline degrades to the committed fixtures.

### Environment variables

All optional. Absent credentials degrade the corresponding stage rather than
failing the request.

| Variable | Effect when set |
|---|---|
| `ROBOFLOW_API_KEY`, `ROBOFLOW_MODEL_ID` | Enables runtime detection |
| `NYC_OPEN_DATA_APP_TOKEN` | Enables runtime NYC Open Data context lookup |
| `GEMINI_API_KEY` | Enables generated explanation |
| `NEARMISS_ALERT_THRESHOLD` | Candidate threshold, 0–100 (default 70) |
| `NEARMISS_HIGH_SEVERITY_AT` | `high` severity cut (default 80) |
| `NEARMISS_FIXTURE_DIR` | Fixture location — set explicitly in the container |
| `GIT_REVISION` | Reported by `/health` to identify the running revision |

Copy `app/.env.example` to `app/.env` and fill in. `.env` is gitignored; never
commit it.

---

## Cloud Run deployment

The `Dockerfile` at the repo root builds from the **repo root** as context —
`demo/fixtures/` is a sibling of `app/` and is load-bearing runtime data, not test
data. An image without it starts cleanly and then fails on the first analysis
request.

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

gcloud run deploy nearmiss-nyc \
  --source . \
  --region us-east1 \
  --allow-unauthenticated \
  --concurrency 1 \
  --min-instances 1 \
  --max-instances 10 \
  --set-env-vars GIT_REVISION=$(git rev-parse --short HEAD)
```

`--concurrency 1` because analysis is synchronous CPU work. `--max-instances`
caps cost. `GIT_REVISION` must be an env var, not a build arg — a `--build-arg`
cannot survive a `--source` build.

Rollback:

```bash
gcloud run revisions list --service nearmiss-nyc --region us-east1
gcloud run services update-traffic nearmiss-nyc --region us-east1 --to-revisions REVISION=100
```

The container binds `0.0.0.0`, reads `$PORT`, holds no request state, and writes
nothing to local disk.

---

## Demo flow

1. **`GET /health`** — service is up, shows the deployed revision and which
   providers are live versus degraded.
2. **`GET /api/v1/demo`** — the captured-evidence replay. Returns a scored
   candidate conflict with its factor breakdown, participants, time window,
   historical context, plain-language observations, stated limitations, and a
   recommended action. Deterministic: identical output on every call, with no
   external API.
3. **`POST /api/v1/live/{source_id}/analyze`** — the live path, with
   `processing_mode` and `notices` disclosing exactly which rung served.

A no-conflict result is a valid outcome. When nothing crosses the threshold the
service returns `NoConflictFound` with the threshold, the number of pairs
evaluated, and the highest score seen — it does not manufacture an event for
presentation.

---

## Limitations

Read this section before judging the output.

- **The demo sequence is synthetic.** It was generated to exercise the pipeline
  deterministically. It is not camera footage and is not attributed to any NYC
  source. The source-attributed NYC capture specified for this milestone was not
  completed, and nothing here should be read as claiming otherwise.
- **The live endpoint does not yet analyse a live frame.** `POST
  /api/v1/live/{source_id}/analyze` responds and is honest about what it did, but
  at this milestone every runtime provider declines and the ladder degrades to
  the committed fixtures. The response discloses this through `processing_mode`
  (`demonstration_fixture`, not `captured_feed_replay`) and through `notices`.
  Wiring a real feed is a change to `providers/`, not to the endpoint.
- **The risk score is an image-space proxy.** See the note at the top. Frame
  geometry is currently fixed at 1280×720 @ 5 fps to match the synthetic scene;
  a real capture at a different resolution needs the calibration knobs in
  `config.py` retuned before its scores mean anything.
- **Motorcyclists are scored as vehicles, not vulnerable road users.** Most
  transport-safety taxonomies disagree. This is the conservative reading of the
  specification and is a known structural bias, not an oversight.
- **Evidence-quality guards can suppress real events.** A pair needs 8 track
  points and 1 second of overlap to be evaluated at all. A sparse real capture
  may legitimately return no conflict.
- **No test suite ships with this milestone.**
- **The judge-facing dashboard is not built.** The system is exercised through
  the JSON API.

---

## Privacy and responsible use

- **No identity recognition and no biometric processing.** No face recognition,
  no gait analysis, no re-identification across cameras, no attempt to determine
  who anyone is.
- Road users are tracked only as anonymous class-labelled boxes (`person`,
  `bicycle`, `car`, …) within a single short sequence. Track IDs are local to
  that sequence and carry no identity.
- No footage, frames, or personal data are persisted. The service is stateless
  and writes nothing to disk.
- Output is **decision support for human review**, not enforcement. Events are
  candidate conflicts flagged for a person to look at — never automated citation,
  penalty, or dispatch.
- The service holds no user data and requires no authentication, so it collects
  nothing to protect.

---

## Prepared-code disclosure

In the interest of an honest submission:

- **Written before the event** — the entire pipeline core (`orchestrator.py`,
  `risk.py`, `models.py`, `config.py`, `providers/`), the FastAPI surface
  (`main.py`), the source registry (`sources.py`), the `Dockerfile`, the
  synthetic fixtures in `demo/fixtures/`, this README, and the planning vault in
  `vault/`.
- **Done during the event** — organizer-source configuration, deployment
  verification, and submission metadata.
- The two are separable in git history: everything committed before the 7 August
  16:00 ET kickoff is pre-event work.
- The `vault/` directory is the project's planning and decision record —
  requirements, architecture, ADRs, risk register, and execution log — kept in the
  repo so the reasoning behind the build is auditable.

---

## License

Apache License 2.0 — see [LICENSE](LICENSE).
