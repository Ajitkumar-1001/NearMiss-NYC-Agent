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
  [[00-Source-of-Truth-PRD|PRD]] §29
- Payload shapes match [[06-Data-Model]] exactly

## Run

```bash
cd app/backend
pip install -e .
uvicorn nearmiss.main:app --reload --port 8080
```

## Deploy

Built and deployed as a container on Google Cloud Run; see the root
`Dockerfile` (build context is the repo root, not this directory) and root
`README.md`.
