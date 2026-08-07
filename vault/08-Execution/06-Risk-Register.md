---
title: Risk Register
tags:
  - execution
status: active
---

# Risk Register

> [!info] Source
> [[00-Source-of-Truth-PRD|PRD]] §28. Impact and mitigation are the PRD's; **Likelihood is deliberately
> blank** — §28 does not estimate it, and a guessed likelihood would drive real
> cut decisions. Fill it from observation, not intuition.

| # | Risk | Likelihood | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| 1 | Not deployed on Cloud Run | | Disqualification | Deploy health skeleton first and preserve revision ([[00-Source-of-Truth-PRD|PRD]] §29) | Ajit | open |
| 2 | Public access blocked by organization policy | | Disqualification | Use personal Gmail or `--no-invoker-iam-check` | Ajit | open |
| 3 | Container binds to localhost/wrong port | | High | Bind to `0.0.0.0:$PORT`; test locally and deployed | Ajit | open |
| 4 | Venue network unusable | | High | Offline demo path; P0 works after the app has loaded ([[00-Source-of-Truth-PRD|PRD]] G6, §8) | Ajit | open |
| 5 | Live feed unavailable | | High | Uploaded and bundled clips | Ajit | open |
| 6 | Official feed requires signed agreement | | High | Do not depend on bulk feed; use approved accessible REST/still source ([[00-Source-of-Truth-PRD|PRD]] §18) | Ajit | open |
| 7 | No near-miss occurs live | | High | Reproducible demonstration clip | Ajit | open |
| 8 | Duplicate camera stills create false motion | | High | Content hashing and temporal-evidence gate | Ajit | open |
| 9 | Detection misses cyclist or pedestrian | | High | Validate the clip early; fixture detections | Ajit | open |
| 10 | Tracking identity switches | | Medium | Short clip; smoothing; precomputed tracks | Ajit | open |
| 11 | Perspective invalidates metric claims | | High | Image-space visual conflict-risk proxy ([[00-Source-of-Truth-PRD|PRD]] §29) | Ajit | open |
| 12 | Gemini fails or hallucinates | | High | Schema constraints and template fallback | Ajit | open |
| 13 | NYC Open Data API fails | | Medium | Cached normalized context | Ajit | open |
| 14 | UI consumes excessive time | | Medium | Single dashboard; no auth; fixture-first development | Ajit | open |
| 15 | Judges interpret output as crash prediction | | High | Explicit terminology and visible limitations ([[00-Source-of-Truth-PRD|PRD]] §19.1) | Ajit | open |
| 16 | License conflict | | Medium | RF-DETR + MIT/Apache defaults; avoid AGPL default ([[00-Source-of-Truth-PRD|PRD]] §17) | Ajit | open |

Rows 1–3, 6, 8, and 16 are new for v2.0 — [[00-Source-of-Truth-PRD|PRD]] §26 (v1) had no equivalent for
the Cloud Run disqualification risks (rows 1–2) or wrong-port binding (row 3);
their Risk/Impact/Mitigation cells are [[00-Source-of-Truth-PRD|PRD]] §28 verbatim. Rows 5, 7, 9–10,
12–13 restate the same risks that were in v1's §26, but §28 reworded most of
the PRD-side mitigation text since then (e.g. "fixture detections" is now
"stored detections fallback") — treat those cells as this note's paraphrase,
not a current quotation; reread §28 before citing them as a direct source. Row
4 is the venue-internet case named in [[00-Source-of-Truth-PRD|PRD]] G6 (§8; this was G4 in v1) and is
the reason [[00-Source-of-Truth-PRD|PRD]] §29 exists. Row 11 (perspective) still matches §29's
framing. Row 15 (judges reading the score as crash prediction) is no longer
its own row in §28 — v2 defines that safeguard in [[00-Source-of-Truth-PRD|PRD]] §19.1 (Risk
semantics) instead.

## Analyze findings — Thursday 6 August, 2:00 PM

Output of [[05-Analyze-Prompt]] against [[02-High-Level-Design]]'s `## Plan` and
[[04-Task-Board]]. Twelve agents, six independent lenses, every finding
adversarially verified against `file:line` or a PRD `§`; anything that merely
restated the ten known contradictions was discarded. **84 findings survived.**

> [!warning] Question 6 was not verified
> The gcloud-blast-radius finder died on a connection error. Section 6 below was
> synthesized from other lenses' findings and did **not** pass the verification
> stage. Treat it as unconfirmed.

### Likelihood, filled from observation

Rows 1–3 above are no longer hypothetical, so the deliberately-blank column can
be filled honestly for them: `gcloud` is **not installed** with six hours to the
gate (`command -v gcloud` fails), and W-1/W-2/W-3 are unconfirmed console state
([[04-Task-Board]] W-1…W-4). Row 2's likelihood remains genuinely unknown —
billing has **no written workaround**, unlike org policy, which PRD §28 and
NFR-002 already pre-authorise two flags for.

### The two conclusions everything else follows from

1. **The eleven-invocation sequence in [[10-Build-Prompts]] does not fit in the
   remaining hours, and was never sized against a number.** `02-Time-Box-Plan`
   still carries `{{HOURS_AVAILABLE_THURSDAY}}` unfilled. No block carries a
   drop-dead time, so an overrun cannot be noticed until 8:00 PM arrives
   mid-block.
2. **The captured-evidence baseline is red by construction, so the 8:00 PM
   branch is already determined.** W-14 (real capture) and S-4 (real context
   query) appear in neither the run order nor the "Not tonight" exclusion list —
   which by that note's own closing rule is a principle 7 violation. PRD §27.1's
   branch then forbids design work, and the plan schedules T-19 (six UI
   surfaces) inside it.

### Defects in the build prompts — verified, and mine

| # | Defect | Pointer |
|---|---|---|
| A | **Dockerfile path cannot work.** `:113` puts it at `app/backend/Dockerfile`; `:130` builds `docker build … .` with no `-f`, so Docker looks for `./Dockerfile` at the repo root and errors. `gcloud run deploy --source .` then falls through to buildpacks, which need `requirements.txt` or a root `pyproject.toml` — the repo root has neither. | [[10-Build-Prompts]] `:113` vs `:130`, `:171` |
| B | **Step 7's done condition is deleted by step 8.** B-1d asserts `processing_mode=="demonstration_replay"`; C-2 one step later renames that exact value. Nothing re-runs step 7. | `:252` vs `:289` |
| C | **Nothing re-deploys after step 6.** The recorded known-good revision is the `/health`-only build, with no `/api/v1/demo`. PRD §2.2 requires the *deployed* service to expose a working analysis endpoint and identify its active mode. | `:33`–`:37`, PRD §2.2 |
| D | **B-1b drops the one assertion that catches a broken container.** B-1a checks `.status=="ok"` (which reaches `readiness()`'s `.exists()` calls); B-1b checks only HTTP 200 and `git_revision != null`. | `:104` vs `:132`–`:135` |
| E | **`/qa` is gated behind T-19**, the least achievable task — so the sweep that determines the 8:00 PM branch is the step most likely never reached. | `:38`, `:418` |
| F | **`GIT_REVISION` cannot reach a `--source` deploy.** Passed as a Docker `--build-arg`, but Cloud Build has no forwarding path and no `--set-env-vars` is set — while `:179` asserts it is non-null. | `:125`, `:171`, `:179` |
| G | **The "deploy a ten-line smoke test first" step does not exist.** [[02-High-Level-Design]] `:164` prescribes it and [[10-Build-Prompts]] `:21` claims to follow it. B-1a is the full FR-019 `/health`; the human gcloud gate sits at row 4, after two serial `/implement` cycles — un-inverting the plan's own stated principle. | `:21`, `:144` |

### Environment — the pre-flight was wrong

**`app/backend/.venv` is broken and `nearmiss` is not installed in it.**

- Every console script's shebang points at the pre-restructure path:
  `#!/Users/ajit/dev/NYC-agent/vault/app/backend/.venv/bin/python3.12`.
  `.venv/bin/pytest` and `.venv/bin/uvicorn` both fail with `bad interpreter`.
- No `nearmiss` dist-info in `site-packages`. `import nearmiss` from any
  directory other than `app/backend` raises `ModuleNotFoundError` — it only
  appeared installed because `cwd` is on `sys.path`.
- B-1a (`.venv/bin/uvicorn`) and TEST-1 (`.venv/bin/pytest`) therefore fail
  before touching any code.

**Consequence for the container:** `config.py:22` is
`REPO_ROOT = Path(__file__).resolve().parents[3]`, correct only while the package
sits at `app/backend/nearmiss/`. A plain (non-editable) `pip install` moves it to
`site-packages`, where `parents[3]` resolves wrong — or, at `/app/nearmiss/`,
raises `IndexError` **at import**, so the container never starts and Cloud Run
reports a failed health check naming no fixture.

**Verified fix:** `NEARMISS_FIXTURE_DIR` is a working override
(`config.py:44` `env_prefix="NEARMISS_"`, `:83` `fixture_dir`). Confirmed:
setting it resolves correctly and the pipeline returns 84.3; setting it to a bad
path fails loudly with the ADR-010 message rather than degrading silently. It
appears in no note, task, or prompt.

### Critical findings beyond the prompts

- **§26.1's first-nine subset cannot go green tonight — four of nine red by
  design.** Checks 5, 6, 7 and 9 have no scheduled step or are explicitly
  deferred. §26.1 says a red first-nine stops all optional work, and `/qa` is
  scheduled after the work it would stop. ([[08-Definition-of-Done]] `:48`)
- **The never-cut real-source path has no legal build window.** `SourceProvider`
  is listed as tonight's component 5 but has no run-order step, and B-1d
  forbids a real fetch; §11.2 permits only *configuration* on Friday, through
  "the **existing** source adapter" — none exists. [[03-Scope-Ladder]] marks it
  rung 3, never-cut. **This, not gcloud, is the assumption that invalidates the
  most work** — gcloud is *blocking*, not *invalidating*: nothing already built
  becomes wrong if the deploy fails, and the same image deploys later from
  another account or Cloud Shell.
- **Only a missing `context.json` is survivable.** Missing `tracks.json` →
  `FileNotFoundError` out of `run()`; truncated JSON → `JSONDecodeError`;
  unknown `class_name` → `ValidationError`. `base.py:55-59` guards `path.exists()`
  then calls `json.load` unguarded at `:60`. With no HTTP layer these surface as
  a bare 500 — no mode badge, no notices, no evidence package.
- **S-4's own output would crash the pipeline.** Adding `dataset_id` to
  `context.json` raises `ValidationError … extra_forbidden` — not
  `FileNotFoundError` — so `orchestrator.py:174` does not catch it and `run()`
  dies. Running S-4 before C-10 is total pipeline failure, not an incomplete card.
- **`insufficient_temporal_evidence` does not exist** (`grep insufficient
  app/backend/nearmiss/` → nothing), yet PRD §26.2 check 4 requires it and
  [[04-Demo-Script]] `:45` scripts a beat against it marked *"This step cannot
  fail."*
- **No LICENSE, no root README, no architecture diagram**, and T-20 appears
  nowhere in the run order. The submission baseline gets zero scheduled minutes
  before the gate. T-20's done condition omits the diagram, so it can pass with
  §26.1 check 14 red.
- **`/health` reports readiness from env-var presence alone.**
  `orchestrator.py:100` sets `ready = configured or fixture_ok`, but `vision.py`
  raises on *both* branches. The moment Friday credentials land, `/health` reads
  `roboflow configured, ready=true` for a stub that has never returned a
  detection — and the 5:15 PM gate check reads that payload.
- **The degraded path emits two contradictory notices** — both "Historical
  context is cached…" and "No historical context available." The append at
  `orchestrator.py:169` fires before the cached rung is attempted. B-1d pins
  `notices | length == 4`, and T-19 renders notices as the visible fallback
  disclosure, so this pair is what a judge reads.
- **Friday's planned state blends live detections with synthetic tracks in one
  overlay.** With vision live and tracking still a stub, `RiskEngine` scores only
  the synthetic tracks — risk stays 84.3 regardless of the real frame — while
  the overlay carries live boxes over a different scene's trails.
- **Frame geometry is hardcoded to the synthetic clip.** `orchestrator.py:46-50`
  fixes 1280×720 @ 5 fps; `risk.py:88` normalises by that diagonal. The planned
  `SourceFrame` carries no width, height, or sampling rate, so nothing lets the
  engine learn a real frame's geometry — against a smaller real frame, proximity
  and path_overlap saturate and inflate every score toward the 70 threshold.
- **C-8's deferral is sequenced backwards against W-14.** `min_track_points = 8`
  clears by 7.5× on the synthetic fixture, but a 20 s still-image capture at
  0.5 Hz yields ~10 points and at 0.25 Hz ~5 — below the gate, so a real capture
  emits `NoConflictFound`. FR-008 requires **three**. C-8 must be re-evaluated
  jointly with W-14, not independently.
- **NFR-004 / NFR-012 exposure:** the pinned deploy command sets no
  `--concurrency` (Cloud Run defaults to 80, NFR-004 specifies 1) and no budget
  alert exists — a public unauthenticated endpoint running synchronous CPU work
  at 80-way concurrency with no spend ceiling, at an open venue.

### Medium and low

Recorded in full at
`scratchpad/synth.md`; the load-bearing ones: FR-001 is 6 of 11 fields and
`Source` is `extra="forbid"`, so completing it Friday is *construction*, which
§11.2 excludes; `orchestrator.py` line pointers in the board and prompts are
stale by ~50 lines (C-2 and C-6 both edit that file); `git ls-files` in W-15's
done condition reports the *index*, so it is green on a staged-but-uncommitted
fixture set — and `git log -- demo/fixtures/detections.json` returns no commits;
`.env` is read by nothing (`config.py:44` has no `env_file`, credentials are bare
`os.getenv`), so W-8's done condition cannot affect the process; two §21
endpoints (`/api/v1/events/{analysis_id}`, `/api/v1/artifacts/{analysis_id}`) are
covered by no task and no deferral; NFR-011 privacy review of the captured
sequence has no task, and the repo is required to be public; T-A's logging
condition passes on a `print()` or on a stack-trace leak, which NFR-008 forbids.

## Review

Re-read at each checkpoint in [[02-Time-Box-Plan]]. A risk that materialises
becomes an entry in [[07-Blocker-Log]]. Add any further risks surfaced by
[[05-Analyze-Prompt]].

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[05-Analyze-Prompt]] · [[07-Blocker-Log]] · [[05-Demo-Reliability]] · [[02-Time-Box-Plan]]
