---
title: README
tags:
  - meta
status: draft
---

# NearMiss NYC — Vault

This directory is the Obsidian vault and holds **markdown only**. Open **this
folder** (`vault/`) as the vault root in Obsidian. The git repo root is one level
up, at `NYC-agent/`.

## Layout

Inside the vault:

| Path | Holds |
|---|---|
| `02-Product/00-Source-of-Truth-PRD.md` | Canonical product + implementation source of truth. Conflicts resolve in its favour. Linked everywhere with a `PRD` display alias. |
| `00-Inbox/` | Unsorted capture. Triage into a numbered folder. |
| `01-Event/` … `12-Logs/` | The knowledge base. See [[Home]]. |
| `11-Templates/` | Obsidian Templates plugin source folder. |
| `Assets/` | Attachments (images, PDFs). Obsidian drops files here automatically. |

Outside the vault, as siblings of it under the repo root — notes cite these by
repo-relative path, never by wikilink:

| Path | Holds |
|---|---|
| `app/` | Application source — backend and frontend. |
| `demo/fixtures/` | Recorded fixtures for the deterministic demo. Committed on purpose. |
| `demo/captured-sequence/` | The source-attributed NYC sequence behind the evidence demo. |
| `tests/` | Test suites. |

## Setup

Run from the repo root, not from here:

```bash
cp app/.env.example .env   # then fill in
```

Numbered prefixes control sort order in the file explorer; they are part of the
filename and therefore part of every wikilink.

## Conventions

Notes carry `title`, `tags`, and `status` frontmatter. `{{UPPER_SNAKE}}` is an
unresolved fact — grep for `{{` to list them. Full rules in [[CLAUDE]].
