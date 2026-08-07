---
title: Project Overview
tags:
  - product
status: active
---

# Project Overview

> [!info] Source
> [[00-Source-of-Truth-PRD|PRD]] §3 and §5. The PRD is authoritative — if this note and the PRD
> disagree, the PRD wins.

## One-liner

NearMiss NYC is an explainable computer-vision decision-support system that
analyzes NYC street-camera footage to identify potential conflicts between
vehicles and vulnerable road users, including pedestrians and cyclists.

> **See the risk before it becomes a crash statistic.**

## What it does

- Tracks road users across the frames of a short street-camera clip.
- Estimates image-space motion and flags converging trajectories or rapidly
  decreasing separation between a vehicle and a vulnerable road user.
- Calculates a **visual conflict-risk proxy** from 0–100, decomposed into named
  factors — proximity, path overlap, closing motion, vulnerable-user weighting.
- Enriches the candidate event with NYC public-data collision context for the
  location, kept visibly separate from what was observed in the clip.
- Produces a structured, uncertainty-aware report for human review, with the
  active processing mode disclosed on screen.

> [!warning] What it is not
> The system does not claim to predict crashes with scientific certainty. It
> surfaces potentially dangerous visual interactions and the evidence behind
> them, so a human can decide whether a location deserves further
> investigation — see [[00-Source-of-Truth-PRD|PRD]] §29.

## Why it matters

See [[02-Problem-Statement]].

## How it works (one level deep)

See [[02-High-Level-Design]]. The pipeline in [[00-Source-of-Truth-PRD|PRD]] §16 runs: source adapter →
provenance and freshness record → frame sampler → vision provider → object
tracker → trajectory extractor → temporal-evidence gate → conflict-risk engine →
evidence package → context and explanation providers → event report.

## What's deliberately not in it

See [[05-Non-Goals]].

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[02-Problem-Statement]] · [[04-MVP-Scope]] · [[07-Demo-Story]] · [[01-System-Context]]
