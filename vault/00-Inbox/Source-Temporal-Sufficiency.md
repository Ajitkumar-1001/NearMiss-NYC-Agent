---
title: Does the source update fast enough for trajectories?
tags:
  - inbox
status: draft
---

# Does the selected source update frequently enough for temporal analysis?

> [!info] Source
> [[00-Source-of-Truth-PRD|PRD]] §30 — "Does the selected source update
> frequently enough for temporal analysis?" New in v2.1 — no capture existed
> for it.

- **Captured:** 2026-08-04
- **Source:** [[00-Source-of-Truth-PRD|PRD]] §30 (v2.1.0-FINAL), "Does the
  selected source update frequently enough for temporal analysis?"
- **Decision deadline:** Before 5:35 PM on event day
- **Default if unresolved:** use the source for **live snapshot proof only**;
  use captured replay for trajectories
- **Depends on:** [[Camera-Source]] — cannot be measured until the source is picked

## Why it matters

This is the question that decides whether the live path can show *motion* or
only *presence*.

Trajectory and pairwise conflict scoring need several observations of the same
object over time. A still-image endpoint refreshing every 20 seconds gives
frames that cannot be associated into a track — every frame is a new scene.
[[11-Vision-Conflict-Analytics-Package]] would return insufficient evidence, and
correctly so.

The §30 default is the honest degradation: prove the system runs on real data
with a snapshot, and let the captured sequence carry the trajectory story. That
is precisely the split [[ADR-006-Real-Source-P0-with-Captured-Fallback]] designs
for, so hitting the default costs nothing at P0.

What it *would* cost is discovering it at 5:30 PM having assumed otherwise.

## The trap §18.4 names

[[00-Source-of-Truth-PRD|PRD]] §18.4 is explicit: **a repeated still frame must not be treated as new
temporal evidence**, and a content hash must be stored to detect duplicates.

A source that returns the same cached image on every poll looks like a working
feed and produces fabricated motion if unguarded. The duplicate-frame check is
not an optimization — it is what stops the system inventing a trajectory.

## How to resolve

- [ ] Poll the chosen source repeatedly and record the actual interval between
      **content changes**, not between requests
- [ ] Hash each frame; count how many polls return an unchanged image
- [ ] Decide the minimum observation count the conflict scorer needs, and whether
      the measured interval can supply it inside the NFR-006 budget
- [ ] Respect the source-specific polling policy and the 511NY throttle (§18.4)
- [ ] Confirm the insufficient-evidence path renders truthfully when the answer
      is no — see [[04-Vision-Evaluation]]

## Triage to

[[02-Live-Feeds]] for the measured refresh characteristics; the snapshot-versus-
trajectory call to [[05-Decision-Log]]. If it changes the sampler, update
[[04-Component-Design]]; the duplicate-frame guard belongs in
[[07-Provider-Adapters]].

---
Nothing stays in the inbox — see [[00-Triage]].
