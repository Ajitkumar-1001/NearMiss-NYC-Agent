# Demo Fixtures

Recorded inputs and expected outputs that make the demo deterministic.

> **These are committed on purpose.** PRD §29 makes the demo run from this
> directory without runtime external APIs. `.gitignore` deliberately does not
> exclude it.

## Contents

| Fixture | Source | Used by |
|---|---|---|
| `detections.json` | Synthetic — 120 rows, 2 objects × 60 frames | `FixtureVision` |
| `tracks.json` | Synthetic — 2 converging tracks | `FixtureTracker` |
| `context.json` | **Placeholder — not real NYC Open Data** | `CachedContext` |

## The synthetic scene

A 1280×720 frame at 5 fps for 12 s. A car crosses left-to-right along `y=380`
at 89 px/s; a pedestrian crosses bottom-to-top along `x=884` at 48 px/s. The
car passes behind the pedestrian — closest image-space approach **82 px at
8.2 s**.

Scored by the real `RiskEngine` in `app/backend/nearmiss/risk.py` against the
`app/backend/nearmiss/config.py` defaults:

| Factor | Value |
|---|---|
| `proximity` | 0.777 |
| `path_overlap` | 0.991 |
| `closing_motion` | 0.619 |
| `vulnerable_user` | 1.000 |
| **Score** | **84.3** → `high` |

That clears `alert_threshold` (70) and `high_severity_at` (80), and lands on
the worked example of 84.0 in PRD §20 — the core data contract.

Regenerate by editing the scene constants and re-scoring; the geometry is
described above precisely enough to reproduce.

## `context.json` is a labelled placeholder

`nearby_collision_count` is **not** a real NYC Open Data figure. `source` reads
`synthetic_placeholder` precisely so it cannot be mistaken for one — the
deterministic explanation surfaces that string verbatim in its observations.
Replace it with a real Motor Vehicle Collisions query once the demo
intersection is chosen and the event carries coordinates to query on.

It is also missing PRD §20's `dataset_id` field, which lands with the §20
contract refactor.

## Replace all three with the real capture

These exist so the API, the deployment check, the dashboard, and the tests can
be built and verified now. When the camera source and Roboflow model are
settled, regenerate from the real 10–20 second sequence. The schema does not
change — only the numbers.

Until then PRD §11.1's captured-evidence baseline is **runnable but not
satisfied**: it requires a source-attributed NYC sequence, and this is neither
attributed nor NYC.

## Rules

- Shapes must match `app/backend/nearmiss/models.py` exactly — the models are
  Pydantic v2 with `extra="forbid"`, so a drifted key fails at load time
- Every fixture-rung adapter in `app/backend/nearmiss/providers/` has a file here
- Keep them small enough to commit comfortably

Open questions on sourcing and licensing are tracked in the vault:
`vault/00-Inbox/Camera-Source.md`, `vault/00-Inbox/Demo-Intersection.md`,
`vault/00-Inbox/Roboflow-Model.md`, `vault/03-Research/01-Datasets.md`.
