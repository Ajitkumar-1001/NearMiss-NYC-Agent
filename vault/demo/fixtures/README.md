---
title: Demo Fixtures
tags:
  - code
status: draft
---

# Demo Fixtures

Recorded inputs and expected outputs that make the demo deterministic.

> [!important] These are committed on purpose
> [[PRD]] §29 makes the demo run from this directory
> with the network disabled. `.gitignore` deliberately does not exclude it.

## Contents

| Fixture | Source | Used by |
|---|---|---|
| {{FIXTURE}} | {{SOURCE}} | |

## Rules

- Shapes must match [[06-Data-Model]] exactly, or fixture and live behaviour drift
- Every adapter in [[07-Provider-Adapters]] has a fixture here
- Keep them small enough to commit comfortably

## Provenance

Licensing for anything derived from a public dataset: [[01-Datasets]].

> [!todo] Record each fixture's source before the demo.
