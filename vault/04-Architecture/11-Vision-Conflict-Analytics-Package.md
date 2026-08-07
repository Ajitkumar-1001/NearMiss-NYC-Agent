---
title: Vision Conflict Analytics Package
tags:
  - architecture
status: active
---

# `vision-conflict-analytics`

> [!info] Role
> Named in [[00-Source-of-Truth-PRD|PRD]] §32.1 as the final implementation design note for the
> reusable package boundary, API, tests, release, and Roboflow contribution path.
> Locked in §29; scope set in §1.3 items 1–3; pre-event baseline in §11.1.

## Why it exists as a package

Pairwise trajectory and conflict scoring is the reusable primitive in this
project. [[00-Source-of-Truth-PRD|PRD]] §29 removes it from NearMiss's private application logic and
makes it a public, permissively licensed library that NearMiss consumes through a
**pinned release**.

The API is deliberately domain-neutral. Traffic conflict is one case; the same
asymmetric class-pair analysis covers forklift–worker proximity, construction
safety, and robotics (§1.3 item 2).

## Boundary

The package owns pairwise interaction analysis and nothing else.

**In:** normalized tracked detections.
**Out:** candidate interacting pairs, decomposed factor scores, evidence
sufficiency, and an optional predicted image-space intersection ([[00-Source-of-Truth-PRD|PRD]] §2.4).

Everything else stays in NearMiss: source acquisition, detection, tracking,
NYC context enrichment, explanation, mode disclosure, and the API surface. See
[[04-Component-Design]] and [[07-Provider-Adapters]] for what sits on either side.

> [!warning] The honesty constraint
> The package README must state that the metric is an **image-space interaction
> proxy, not calibrated time-to-collision** ([[00-Source-of-Truth-PRD|PRD]] §11.1). This is the same
> claim boundary as [[ADR-002-Visual-Conflict-Proxy]] and §19 risk semantics —
> shipping it as a library does not soften it.

## API shape

Typed configuration and result schemas, mirroring the contracts in
[[06-Data-Model]]. Concrete signatures: {{PACKAGE_API_SIGNATURES}}.

Consumption rule from [[00-Source-of-Truth-PRD|PRD]] §11.1: **NearMiss fixtures and the runtime
pipeline both call the package API.** Duplicating scoring logic inside NearMiss
breaks fixture parity — the fixtures would stop proving anything about runtime.

## Tests

§11.1 requires unit coverage of:

- Converging paths
- Parallel motion
- Asymmetric class pairs
- Insufficient observations
- Unstable evidence

The last two matter most for the demo: they are what makes an
"insufficient evidence" verdict a real result rather than a failure. See
[[04-Vision-Evaluation]].

## Release and licensing

- [ ] Public repository created
- [ ] Apache-2.0 or MIT license committed
- [ ] Typed config and result schemas committed
- [ ] Unit tests above passing
- [ ] Versioned release or immutable commit published
- [ ] NearMiss dependency pinned to that release or commit
- [ ] README states the image-space-proxy limitation

Release identifier: {{PACKAGE_RELEASE_VERSION}}. Repository URL:
{{PACKAGE_REPO_URL}}.

## Roboflow contribution path

A Roboflow Workflow block or community-plugin wrapper is **post-P0**
([[00-Source-of-Truth-PRD|PRD]] §2.4, §29). The Friday artifact is the standalone tested library and
its use inside NearMiss. The wrapper must not delay the submission.

## Changes before the event

Per [[00-Source-of-Truth-PRD|PRD]] §32.1 this note is *logged rather than versioned* before the
event — record changes here inline, not through a PRD version bump.

| When | Change | Why |
|---|---|---|
| | | |

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[04-Component-Design]] · [[06-Data-Model]] · [[07-Provider-Adapters]] · [[04-Vision-Evaluation]] · [[ADR-002-Visual-Conflict-Proxy]] · [[ADR-003-Provider-Adapter-Architecture]]
