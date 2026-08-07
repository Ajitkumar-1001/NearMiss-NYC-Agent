---
title: Responsible AI
tags:
  - architecture
status: active
---

# Responsible AI

Judges ask about this, and it matters independently of that.

[[05-Safety-Methodology]] owns the proxy's epistemic limits — what a monocular
score can and cannot know. This note owns the deployment-side posture: what
enters the system, what leaves it, and which of the
[[00-Source-of-Truth-PRD|PRD]] §23 requirements the code actually enforces
today.

## Data and privacy

- **Personal data in our inputs:** {{PII_ASSESSMENT}}. This is genuinely
  unknown, and it is unknown for a structural reason — the camera source is not
  chosen yet ([[Camera-Source]], the §30 open question "Which organizer or city
  camera source is most reliable?"). Whether faces and plates are legible in
  the frames we will actually process depends on that answer. What is settled
  is the *policy*, not the finding: §29 locks "No identity recognition",
  NFR-011 forbids face recognition, plate recognition, identity and demographic
  inference, and re-identification, and §23 opens with the same four as data
  requirements. G8 adds unnecessary retention of raw street imagery to that
  list, and §28 carries "Privacy sloppiness" as a High-impact risk.
- [ ] **Are faces / plates visible? If so, what do we do about it?** — Unknown
  until the source lands. The policy if they are: §23 requires public artifacts
  to avoid unnecessary exposure of faces and plates, and NFR-011 requires
  stored representative frames to be minimized, source-attributed, and blurred
  or discarded when retention is not required. No blurring, cropping, or
  redaction step exists anywhere in `app/backend/nearmiss/` — not yet built.
  The mechanism is {{FRAME_REDACTION_METHOD}}, and it cannot be chosen before
  [[Camera-Source]] resolves.
- [ ] **Retention: what do we keep after the demo, and for how long?** — No
  policy written; the window is {{MEDIA_RETENTION_WINDOW}}. What the code does
  today is narrower than a policy and should not be mistaken for one:
  `nearmiss/orchestrator.py` constructs every `Event` with
  `representative_frame=None` and `EvidenceOverlay.clip_path=None`, so the
  payload carries bounding boxes, centroid tracks, and timestamps and no pixels
  at all. That is a consequence of there being no clip yet, not a retention
  decision. NFR-010 requires temporary files to be deleted after processing
  where practical; there is no upload path or temp file to delete yet either.

The identity boundary is enforced in the type system rather than by convention.
`nearmiss/models.py` carries no appearance, attribute, or demographic field
anywhere in the contract, and its `Strict` base rejects unknown fields, so one
cannot be added by a drifting fixture — [[06-Data-Model]] owns the field list.
`RoadUserClass` is a closed `Literal` of six classes, and the `Track.track_id`
docstring states that the id is scoped to a single clip and is not an identity.

> [!todo] Owed before the demo
> - **README privacy handling.** §11.1's submission baseline requires the
>   README to cover limitations and privacy handling. No README in this repo
>   mentions either yet.
> - **`LimitationsAndPrivacyCard`.** One of §22's six required judge-facing
>   surfaces. `app/frontend/` currently contains only a README, so nothing
>   renders limitations to a viewer — they exist in the payload only.

## Known limitations

State plainly what the system cannot do. From [[05-Safety-Methodology]]:
the conflict score is a monocular proxy, not a measurement.

The first four rows are produced by real code. `BASELINE_LIMITATIONS` in
`nearmiss/providers/explanation.py` appends rows 1 and 2 unconditionally, rows
3 and 4 are the two branches of the historical-context case in the same file,
and `Event.limitations` in `nearmiss/models.py` is `Field(min_length=1)`, so a
report carrying no limitation fails validation outright (§23 requires every
report to expose limitations). Rows 5 onward are real limits of the code that
no report currently states.

| Limitation | Consequence | Mitigation |
|---|---|---|
| The camera is not geometrically calibrated, so all motion is image-space — *in every report* | Pixel separation is not metric distance, and a score is not comparable across cameras or framings | Stated in every report; `nearmiss/risk.py` normalises separations against the frame diagonal (`proximity_scale`, `path_scale` in `nearmiss/config.py`) so a resolution change does not silently move the number |
| The score is a visual conflict-risk proxy, not a crash probability — *in every report* | §19.1 rules it out as a legal finding, a traffic-violation determination, or a causal infrastructure diagnosis; enforcement and insurance adjudication are §6.3 excluded uses | Stated in every report; `nearmiss/risk.py` is the only place a score is produced and it calls no language model, so narration can never originate the number |
| Historical collisions are context for the location, not evidence about this event — *in every report that has context* | Correlation is not cause (§23.9) | Partial. `nearmiss/models.py` keeps `historical_context` a field separate from `observations`, but `TemplateExplanation` also appends the collision count as a sentence *inside* `observations` — §23.10 requires public context to stay separate from observed evidence, and at the text level the code does not do that |
| No historical context was available for this location — *in every report that lacks it* | The event carries only its location label | `nearmiss/orchestrator.py` treats context as genuinely optional and records its absence rather than dropping the field silently |
| Motorcyclists are treated as vehicles, not vulnerable road users — *not stated in any report* | `nearmiss/config.py` places `motorcycle` in `vehicle_classes`, so a car–motorcycle pair fails `RiskEngine._is_supported_pair` and is never scored at all | None in the product. The config comment flags it as the conservative reading of a PRD that does not classify motorcyclists, and asks for a [[05-Decision-Log]] entry rather than a silent edit |
| The vulnerable-user factor is a constant — *not stated in any report* | `nearmiss/risk.py` sets `vulnerable_user=1.0` for every evaluated pair; it is a deliberate score floor, not a discriminator, but `risk_factors` renders it beside three factors that do vary | None. The FR-010 factor breakdown is honest about the value and silent about its being fixed |
| Explanation confidence is fixed at 0.6 — *not stated in any report* | `TemplateExplanation` returns the same confidence regardless of evidence, so `explanation_confidence` does not track evidence quality | The code comment is explicit that this is a deliberate mid value for a template that has done no reasoning and would overclaim at 1.0 |
| A pair that fails the evidence gate disappears rather than being reported — *not stated in any report* | `RiskEngine._has_enough_evidence` drops a pair below `min_track_points` (8) or `min_overlap_seconds` (1.0) before scoring, and `NoConflictFound.pairs_evaluated` counts only pairs that were scored | Not yet built. §13 defines an `insufficient_temporal_evidence` outcome state and FR-008 requires it when the gate fails; `nearmiss/models.py` has no such outcome — `NoConflictFound` is the only non-event shape. The gate is also all-or-nothing because FR-010's evidence-quality adjustment is unimplemented: `RiskFactors` has four fields and no `evidence_quality`, and `risk.py` stops at the weighted sum, so a pair that clears the gate is scored as though its evidence were perfect |
| Nothing runs live yet — *not stated in any report* | `RoboflowVision`, `ByteTrackTracker`, `NycOpenDataContext`, and `GeminiExplanation` all raise `ProviderUnavailable`, so every run steps down to the fixture path and `processing_mode` is `demonstration_replay` | Each step-down is labelled: `ProviderMetadata` names the implementation that actually served each stage and the orchestrator appends one notice per fallback, which is what FR-016's "fallback operation shall never be represented as live inference" asks for. The labelling stops there — `ProcessingMode`'s three values are not FR-016's five named modes, and that mapping is unbuilt. `demo/fixtures/` holds only a README, so the fixture path cannot run today either |
| {{SOURCE_USAGE_LIMITATION}} | The known usage limitation of the chosen camera source, which §18.5 requires the README and dashboard to state alongside attribution and retrieval timestamp | Unresolvable until [[Camera-Source]] resolves |

> [!warning] The code's own citations point at an older PRD
> Not two stale pointers — the §, FR, and ADR references throughout `nearmiss/`
> predate the v2.1.0 renumber, so no citation in the package can be followed
> without checking it first.
>
> - **Renumbered.** `models.py` and `providers/explanation.py` both cite "PRD
>   §21.6" for the always-expose-limitations rule, and `explanation.py` cites
>   "PRD §21.7" for the human-review rule. Both are §23 items — §21 is now API
>   requirements.
> - **Nonexistent.** `risk.py` cites §16.5 (§16 has only 16.1 and 16.2);
>   `risk.py` and `config.py` cite "§22.2 cases 5 and 6" (§22 has no numbered
>   subsections); `models.py` cites §21.8 and `providers/context.py` cites
>   §21.10.
> - **Misattributed.** `config.py` credits §18 with "the worked example scores
>   84.0" — §18 is the data-source policy; the 84.0 example is §20's data
>   contract.
> - **Shifted FR numbers.** `config.py`'s "FR-007 threshold" is FR-011, its
>   "FR-006 weights" is FR-010, its "FR-005 vulnerable classes" is FR-009; the
>   providers' "FR-011 fallbacks" is FR-015; `explanation.py` attributes
>   FR-014's do-not-invent rule to FR-010.
> - **ADRs.** The files cite `ADR-002`, `ADR-003`, `ADR-004`, `ADR-006`, and
>   `ADR-010`. `07-Decisions/` has since been renumbered: 002, 003, and 004
>   still resolve, but its `ADR-006` is `Real-Source-P0-with-Captured-Fallback`
>   — a different decision from the No-identity-recognition one the code means
>   — and `ADR-010` no longer exists. The surviving statements are §29's "No
>   identity recognition" and "JSON fixtures and captured assets are
>   operational fallbacks".
>
> These are pointer errors rather than behaviour errors, but the two are easy to
> confuse: where the code genuinely diverges from v2.1.0 the rows above say so,
> and a comment can be stale in both ways at once. `models.py` claims fixture
> parity is enforced by `tests/test_fixture_parity.py`; `tests/` holds only a
> README. Whether the vault keeps ADRs at all is itself unsettled — §29 lists
> required superseding ADRs, while this vault's own note rules treat §29 as the
> single list of locked decisions. That conflict is owed to
> [[05-Decision-Log]].

## Bias

- [x] **Where could coverage be uneven — camera placement, lighting, time of
  day?** Placement first: `nearmiss/risk.py` normalises separations against the
  frame diagonal, using the `proximity_scale` and `path_scale` fractions
  declared in `nearmiss/config.py`, precisely because the same interaction seen
  from a pole and from a bridge is a different number of pixels; the config
  comment says those scales need tuning once a real clip exists. Until that
  tuning happens the score is a function of vantage point as much as of
  behaviour. Scope compounds it — §9
  rules out monitoring every NYC camera and §10 prefers one camera and one
  event, so coverage is a single vantage point and nothing generalises from it.
  Lighting and time of day are untested: §24.2's vision evaluation covers
  detection, track stability, trail alignment, and schema parity on the
  selected sequence, and names no lighting or time-of-day condition. The
  evidence gate then biases the whole system toward under-reporting rather than
  over-reporting — occlusion, short tracks, and dropped frames remove a pair
  from evaluation entirely instead of lowering its score, and the gate as
  configured (8 observations) is stricter than FR-008's initial gate of three.
- [x] **Who is affected if the system is wrong, and in which direction?** The
  dominant error is a false negative, and it lands on the road user whose
  conflict never reaches a reviewer. A false positive costs analyst time and
  nothing else, because §19.3 keeps a human between the score and any action.
  One class-level bias is structural rather than statistical: motorcyclists sit
  outside `vulnerable_classes`, so a motorcyclist struck by a car is never
  evaluated — a motorcycle is only ever scored as the vehicle half of a pair,
  never as the party at risk. §23 forbids demographic inference and the data
  contract has no field that could carry one, so the system cannot produce a
  demographic disparity directly — but where the camera
  points decides whose street is analysed, and that choice is made in
  [[Camera-Source]] on feed reliability, clip content, and redistribution
  terms, none of which is a measure of where the risk actually is.

## Misuse

- [x] **What would make this harmful — enforcement? individual tracking?**
  Both, and §6.3 names them. Its eight excluded uses split cleanly in two:
  acting on an event automatically, and resolving a road user into a person.
  Everything the design does below is aimed at one half or the other. §9's
  non-goals restate both halves as things the MVP will not do.
- [x] **What does the design do to make that harder?**
  - There is no identity to attach an action to. The six-class taxonomy and the
    clip-scoped `track_id` in `nearmiss/models.py` are the whole vocabulary,
    and correlating a track across clips has nothing to correlate on.
  - Nothing in `nearmiss/` opens a network connection. The three providers that
    would — `RoboflowVision`, `NycOpenDataContext`, and `GeminiExplanation` —
    raise `ProviderUnavailable` before any request. §19.3 forbids automatically
    contacting enforcement, dispatch, or filing a 311 report, and today no code
    path exists that could.
  - Every high-severity event carries a review recommendation.
    `TemplateExplanation` branches on `severity == "high"` and returns a review
    action, and `Event.recommended_action` is a required field, which is §23's
    human-review requirement and §19.3's.
  - Evidence, derived metrics, public context, and generated language have
    separate fields in the same record ([[06-Data-Model]]), so a reader can see
    which claim came from where — §23.10 requires exactly that separation. The
    separation holds in the schema but leaks in the text, because
    `TemplateExplanation` writes the historical collision count into
    `observations` as well.
- [ ] **Residual.** The service is public and unauthenticated by §29, and
  FR-018 makes the complete normalized record exportable as JSON, so anything
  we publish is reusable by a consumer bound by none of the above. §29 also
  requires a permissive licence, and a permissive licence carries no
  field-of-use restriction. Past the export boundary the constraint is
  documentary, not technical — which is why §23's "avoid unnecessary exposure
  of faces and plates in public artifacts" is the requirement that does the
  real work, and why it is still unbuilt.

## Framing

This surfaces patterns for safety review. It is not an enforcement tool and not
a measurement instrument. Keep that framing in [[05-Judge-Questions]].

---
Related: [[00-Source-of-Truth-PRD|PRD]] §23 · [[05-Safety-Methodology]] · [[05-Judge-Questions]] · [[06-Data-Model]] · [[01-Constitution]]
