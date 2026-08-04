---
title: Backend
tags:
  - code
status: draft
---

# Backend

Pipeline and API.

## Structure

Components and their responsibilities are specified in
[[04-Component-Design]]; endpoints in [[05-API-Contracts]].

## Rules

- External providers only through adapters — [[07-Provider-Adapters]]
- Must run end-to-end on `demo/fixtures/` with no network —
  [[ADR-001-Deterministic-Demo-First]]
- Payload shapes match [[06-Data-Model]] exactly

## Run

```bash
{{RUN_COMMAND}}
```

> [!todo] Fill in once the stack is chosen.
