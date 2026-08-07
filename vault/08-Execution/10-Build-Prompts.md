---
title: Build Prompts
tags:
  - execution
status: active
---

# Build Prompts

Copy-paste arguments for the workflow commands, in run order.

> [!danger] Rewritten 6 August 4:45 PM after `/analyze` — the previous sequence was defective
> [[06-Risk-Register]] records seven verified defects in the first version of this
> note (unbuildable Dockerfile path, a done condition deleted by the next step,
> no redeploy after the endpoints landed, `GIT_REVISION` unreachable through
> `--source`, `/qa` gated behind the least achievable task, and a "smoke test
> first" step that was described but never written). It also found the
> `app/backend/.venv` console scripts dead and `nearmiss` not installed — both
> **now repaired and verified from outside `app/backend`**.
>
> **The eleven-block sequence does not fit in 3.3 hours.** This version is cut to
> what the §11.1 deployment baseline actually needs, with a drop-dead time on
> every block. Everything else is explicitly deferred below, not silently
> dropped — [[01-Constitution]] principle 7.

## The cut

| Time | Block | Status |
|---|---|---|
| **now** | gcloud install / auth / project / billing | human, running |
| 5:15 PM | `/implement` **D-0** — prove the deploy path | MUST |
| 6:15 PM | `/implement` **D-1** — the real service, verified under local Docker | MUST |
| 6:45 PM | `/implement` **D-2** — deploy, verify logged-out, record rollback | **MUST — this is the gate** |
| 7:15 PM | `/implement` **D-3** — C-5 + C-6 honesty fixes, redeploy | SHOULD |
| 7:35 PM | `/implement` **D-4** — LICENSE + root README | SHOULD |
| 7:50 PM | `/implement` **D-5** — log every deviation | MUST |
| 8:00 PM | **§27.1 readiness decision** | — |

**Cut outright, and logged as deviations in D-5:** T-19 (six surfaces), TEST-1
(the NearMiss test suite), W-9…W-12 (the `vision-conflict-analytics` package),
W-13/W-14 (real source and real capture), S-4 (real context query), T-21/T-22,
T-A (logging), and C-1/C-3/C-4/C-7/C-8/C-9/C-10.

If a block misses its drop-dead time, **skip to D-5 and log it**. An honest red
at 8:00 PM is a readiness decision; an unnoticed overrun is not.

---

## D-0 — prove the deploy path (drop-dead 5:15 PM)

The step the previous version described but never wrote. Fifteen lines of
throwaway code whose only job is to fail fast if the *external* path is broken.

```text
D-0 — prove the Cloud Run deploy path with a throwaway service. This is NOT the
real application. Do not import nearmiss. Do not touch app/backend/.

Prerequisite check first — if either fails, STOP and report, do not work around:
  gcloud auth list          → an active account
  gcloud config get-value project → a project id

Create exactly two throwaway files at the repo root:
  _smoke/main.py     — FastAPI, one route GET /health returning {"status":"ok"},
                       binding 0.0.0.0 and reading $PORT default 8080
  _smoke/Dockerfile  — python:3.12-slim, pip install fastapi uvicorn, CMD uvicorn

Deploy:
  gcloud run deploy nearmiss-smoke --source _smoke --region us-central1 \
    --allow-unauthenticated --port 8080

If --allow-unauthenticated is refused by org policy, retry with
--no-invoker-iam-check (NFR-002 names both; PRD §28 pre-authorises the swap).
If billing is disabled, that is a hard blocker — record it in 07-Blocker-Log.md
and report immediately; there is no written workaround for it.

Done condition — paste every output verbatim:
  curl -s -o /dev/null -w '%{http_code}' $SMOKE_URL/health     → 200
  MANUAL: open $SMOKE_URL/health in a logged-out/incognito window. It must render
  the JSON with no Google sign-in interstitial. curl does NOT prove this — curl
  was never carrying your Google session.

Report the elapsed wall-clock time for the deploy. D-2 needs that estimate.

Leave nearmiss-smoke running; D-2 deploys a separate service. Do not delete
_smoke/ yet — if D-2 fails, this is the proof the account is not the cause.
```

---

## D-1 — the real service, verified locally (drop-dead 6:15 PM)

One block, not four. `/health` **and** all three endpoints **and** the C-2 mode
fix land together, so the artifact D-2 deploys is the one §2.2 describes.

```text
D-1 — the full NearMiss service and its container, verified under local Docker.
Deploy is D-2; do not deploy here.

--- part 1: app/backend/nearmiss/main.py ---

Endpoints per 04-Architecture/05-API-Contracts.md:
  GET  /health                            → models.Health
  GET  /api/v1/sources                    → sources.SOURCES verbatim
  GET  /api/v1/demo                       → Orchestrator().run()
  POST /api/v1/live/{source_id}/analyze   → same pipeline; 404 on unknown id

Reuse, do not redefine — all of this already exists:
  models.Health carries all six FR-019 fields
  models.AnalysisResponse is the envelope (event | no_conflict | notices)
  orchestrator.readiness() returns the four DependencyStatus rows
  sources.enabled_count(), sources.by_id()
  __init__.__version__

git_revision comes from the GIT_REVISION env var, None when unset. Do not shell
out to git — the container has no .git.

/health returns 200 even when degraded; report degradation in the body as
status:"degraded". A non-200 would make Cloud Run's health checking meaningless.
NFR-010: never a key, token, or URL in any response.

Add CORSMiddleware (ADR-005: no authentication, nothing to protect).

Do NOT implement a real source fetch — no source adapter exists. The live route
runs the same pipeline and degrades to the fixture rung, disclosed through
processing_mode and notices. A fallback is a SUCCESS with a changed mode.

--- part 2: the C-2 mode fix, in the same block ---

It lands here, not later, because the previous sequence had B-1d assert a mode
value that a later step renamed, invalidating its own done condition.

models.py:33 declares three v1 values. FR-016 names five: Live NYC snapshot,
Live sampled sequence, Runtime sequence analysis, Captured feed replay,
Demonstration fixture. Wire values snake_case.

USE demonstration_fixture, NOT captured_feed_replay, for the current path.
The pipeline reads precomputed detections from detections.json and precomputed
tracks from tracks.json — vision is bypassed entirely, and sources.py:37-42
states the sequence is synthetic and "Not camera footage and not attributed to
any NYC source." Labelling that a captured feed replay would be a false
provenance claim, and §2.2 puts "identify the active processing mode" on the
eligibility gate. §23 item 11 requires fixture assets labelled accurately.

Scope: the Literal in models.py and the mode selection in orchestrator.py
(around :222 — the board's :171 pointer is ~50 lines stale).

--- part 3: the Dockerfile, at the REPO ROOT ---

Path is ./Dockerfile, not app/backend/Dockerfile. demo/ is a sibling of app/, so
the build context must be the repo root, and `docker build .` resolves
./Dockerfile. The previous version put it under app/backend and built with `.`,
which cannot work.

  FROM python:3.12-slim
  COPY app/backend/ /app/app/backend/
  COPY demo/fixtures/ /app/demo/fixtures/
  RUN pip install --no-cache-dir /app/app/backend
  ENV NEARMISS_FIXTURE_DIR=/app/demo/fixtures
  ENV PORT=8080
  CMD exec uvicorn nearmiss.main:app --host 0.0.0.0 --port $PORT

NEARMISS_FIXTURE_DIR IS LOAD-BEARING — do not omit it. config.py:22 is
parents[3], correct only while the package sits at app/backend/nearmiss/. A
non-editable pip install moves it into site-packages, where parents[3] resolves
wrong, or at /app/nearmiss/ raises IndexError AT IMPORT — the container never
starts and Cloud Run reports a failed health check that names no fixture.
Verified: the override resolves correctly, and a bad value fails loudly with the
ADR-010 message rather than degrading silently.

--- done condition: paste every output ---

Local, before Docker:
  cd app/backend && .venv/bin/uvicorn nearmiss.main:app --port 8080 &
  curl -s localhost:8080/api/v1/demo | jq -e '.event.risk_score==84.3'      → exit 0
  curl -s localhost:8080/api/v1/demo | jq -r '.event.processing_mode'       → demonstration_fixture
  curl -s localhost:8080/api/v1/sources | jq -e 'length==1'                 → exit 0
  curl -s -o /dev/null -w '%{http_code}' -X POST localhost:8080/api/v1/live/nope/analyze  → 404

Container — this is the part the previous version could not catch:
  docker build -t nearmiss .
  docker run -d -p 8081:8080 nearmiss
  curl -s localhost:8081/health | jq -e '.status=="ok"'                     → exit 0
  curl -s localhost:8081/api/v1/demo | jq -e '.event.risk_score==84.3'      → exit 0

The .status=="ok" assertion is mandatory — readiness() calls .exists() on every
fixture path, so it is the only check that proves the container can actually
serve an analysis rather than merely return 200.
```

---

## D-2 — deploy and verify (drop-dead 6:45 PM) — **this is the gate**

```text
D-2 — deploy the real service. Closes W-5, W-6, W-7 and §26.1 checks 1-4, and is
the §11.1 deployment baseline in full.

Commit the fixtures FIRST. `git ls-files demo/fixtures` reports the INDEX, so it
is green on staged-but-uncommitted files — and `git log -- demo/fixtures/` shows
no commits. `gcloud run deploy --source` uploads the working tree, so without
this the image carries fixtures the public repository does not, and a fresh
clone cannot reproduce the demo (§26.1 check 8 says "committed").

  git add -A && git commit -m "P0 deployment baseline: service, container, fixtures"

Deploy from the repo root:
  gcloud run deploy nearmiss-api --source . --region us-central1 \
    --allow-unauthenticated --port 8080 --concurrency 1 \
    --set-env-vars GIT_REVISION=$(git rev-parse --short HEAD)

--set-env-vars is how GIT_REVISION reaches the service. A Docker --build-arg
cannot survive a Cloud Build --source deploy — that was a defect in the previous
version, which asserted git_revision non-null while providing no path for it.
--concurrency 1 is NFR-004's stated default; Cloud Run's own default is 80, and
this is a public unauthenticated endpoint doing synchronous CPU work.

Done condition — four parts, paste every output:
1. curl -s -o /dev/null -w '%{http_code}' $URL/health                   → 200
2. curl -s $URL/api/v1/demo | jq -e '.event.risk_score==84.3'           → exit 0
   (this is what proves the fixtures resolved inside the container)
3. curl -s $URL/health | jq -e '.git_revision != null'                  → exit 0
4. MANUAL: open $URL/health in a logged-out/incognito window, no sign-in
   interstitial. Screenshot to demo/screenshots/.

Then write into 04-Architecture/08-Deployment.md, replacing {{BE_URL}}: the
literal deploy command above, the resolved URL, the revision name from
  gcloud run services describe nearmiss-api --region us-central1 \
    --format='value(status.latestReadyRevisionName)'
and the rollback line
  gcloud run services update-traffic nearmiss-api --to-revisions=<REV>=100
pasted from a run that actually succeeded. §27.2's 7:00 PM freeze leaves no time
to reconstruct these on Friday.

Also delete the D-0 throwaway:
  gcloud run services delete nearmiss-smoke --region us-central1 --quiet
  git rm -r _smoke
```

---

## D-3 — the two honesty fixes (drop-dead 7:15 PM)

Both are minutes, both are Constitution principle 5, and both change what a judge
reads. Redeploy after, or they are not on the deployed artifact.

```text
D-3 — C-5 and C-6, then redeploy.

C-5 — §23.10 separation. providers/explanation.py appends the historical
collision sentence into the observations list. Verified live: observations ends
with "14 collisions are recorded within 150 m of this location
(synthetic_placeholder)." That is public context sitting inside observed visual
evidence. §23 item 10 requires observed evidence, derived metrics, public
context and generated explanation to stay separate. The Event already carries
historical_context as its own field, so removing the sentence de-duplicates
rather than loses.

C-6 — FR-017 mandates exactly: "No candidate conflict crossed the configured
visual-risk threshold in the available evidence." orchestrator.py emits
"...in this clip." (around :233 — the board's :183 pointer is ~50 lines stale).

Done condition:
  .venv/bin/python -c "from nearmiss.orchestrator import Orchestrator; e=Orchestrator().run().event; assert not any('collision' in o.lower() for o in e.observations), e.observations; assert e.historical_context.nearby_collision_count==14; print('ok')"
    → prints ok
  grep -rn "in this clip" app/backend/       → no output

Then redeploy with the same D-2 command and re-run D-2's done conditions 1 and 2.
A fix that is not on the deployed revision does not count — §2.2 is a deployed
gate.
```

---

## D-4 — submission baseline (drop-dead 7:35 PM)

Currently scheduled nowhere, and cheap. Verified absent: the repo root holds only
`.gitignore app demo tests vault`.

```text
D-4 — LICENSE and root README. §11.1 submission baseline; §26.1 check 14.

LICENSE at the repo root — MIT or Apache-2.0. PRD §11.1 requires a permissive
licence committed and the repository public.

README.md at the repo ROOT. GitHub's landing page is currently blank because
everything lived under vault/ until today. §11.1 requires eight headings:
problem, architecture, sources, setup, Cloud Run deployment, demo flow,
limitations, privacy handling.

Two things it must state plainly, because they are honesty obligations rather
than marketing:
- the risk score is an image-space visual conflict proxy, NOT a collision
  probability and NOT calibrated time-to-collision (§19.1, ADR-002)
- the demo runs on a SYNTHETIC fixture sequence, not a source-attributed NYC
  capture, and context.json is a labelled placeholder rather than real NYC Open
  Data

Link vault/08-Execution/09-Preexisting-Code-Disclosure.md and fill its
{{BOUNDARY_COMMIT_SHA}}, {{BOUNDARY_COMMIT_TIME}}, {{BOUNDARY_TAG}} from
  git rev-parse HEAD && git tag pre-event-baseline && git push --tags
A judge seeing a working system at 8:45 PM Friday is entitled to know what
existed at 4:00 PM. Reconstructing that boundary afterwards is not credible.

Done condition:
  ls /Users/ajit/dev/NYC-agent/LICENSE /Users/ajit/dev/NYC-agent/README.md   → both exist
  grep -c '^#' README.md    → at least 8 headings
  git tag | grep pre-event-baseline                                          → present
```

---

## D-5 — log every deviation (drop-dead 7:50 PM) — **MUST**

The block that makes the 8:00 PM decision honest rather than silent.

```text
D-5 — one entry in 08-Execution/05-Decision-Log.md recording everything cut
tonight, with its reason. Constitution principle 7: silently leaving a known gap
is the violation; a logged, reasoned cut is a decision.

Record, each with one line of reason:
- T-19, the six §11.3 surfaces — §26.1 check 13 stays RED. Three notes estimate
  it a day of work from an empty directory.
- TEST-1, the NearMiss test suite — tests/ still holds only README.md, so no
  "tests pass" claim is available tonight.
- W-9…W-12, vision-conflict-analytics — §26.1 checks 9 and 10 stay RED, and both
  sit inside §26.1's hard first-nine subset.
- W-13 / W-14, real source and real capture — §26.1 checks 5 and 7 stay RED. The
  captured-evidence baseline is therefore NOT green; the fixture is synthetic.
- S-4 real context query. Note that running S-4 before C-10 would CRASH the
  pipeline: adding dataset_id to context.json raises ValidationError
  (extra_forbidden), which orchestrator.py does not catch.
- T-20 architecture diagram, T-21 backup recording, T-22 three deployed golden
  runs, T-23/T-24 organizer questions, T-A logging (NFR-008).
- C-1, C-3, C-4, C-7, C-8, C-9, C-10 — the §20 contract refactor and the rest.
  Flag C-8 specifically: min_track_points=8 clears by 7.5x on the synthetic
  fixture, but a real 20-second still-image capture at 0.5 Hz yields ~10 points
  and at 0.25 Hz ~5, below the gate — so a real capture would emit
  NoConflictFound. FR-008 requires three. C-8 must be re-decided WITH W-14, not
  independently.
- S-2 cooldown and S-3 conflict-zone gate — 05-Decision-Log already requires
  these to be built-or-dropped before tonight's gate. Drop them explicitly.

Then record the §27.1 Thursday 8:00 PM readiness decision itself: which of the
two §11.1 baselines is green, which is red, and which branch you are taking.

Done condition: the entry exists and names every item above with a reason.
```

---

## If time remains — `/qa`

Ahead of any new feature work, never behind it. The previous version gated this
behind T-19, which made the sweep that decides the branch the step least likely
to be reached.

```text
Run 06-gstack/05-QA-Checklist.md against the DEPLOYED Cloud Run URL, not
localhost. Then walk PRD §26.1's fifteen arrival-gate boxes and report each
red/green, calling out specifically which of the FIRST NINE are red — §26.1
makes those nine the subset that stops all optional work.

Report only. Do not fix anything after 7:00 PM.
```

---

## Known-red at 8:00 PM, by design

Stated here so the readiness decision is made against reality:

- **§11.1 deployment baseline** — achievable tonight, and the target.
- **§11.1 captured-evidence baseline — RED.** The sequence is synthetic, not
  source-attributed NYC. No amount of tonight's work changes that; it needs
  W-14.
- **§26.1 first-nine — four red** (checks 5, 6, 7, 9). §26.1's consequence
  clause therefore fires against all optional work, which is the stated reason
  T-19 is cut rather than attempted.
- **§2.2 — partially met.** Public URL, `/health` 200 and revision identification
  land tonight. "At least one working **real-source** analysis endpoint" does
  not, and no source adapter exists to make it land Friday inside §11.2's
  configuration-only window. **This is the single largest open risk on the
  project** — see [[06-Risk-Register]].

---
Related: [[04-Task-Board]] · [[06-Risk-Register]] · [[02-High-Level-Design]] · [[06-Implement-Prompt]] · [[01-Workflow|gstack workflow]] · [[08-Definition-of-Done]]
