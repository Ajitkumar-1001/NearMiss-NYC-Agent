---
title: README
tags:
  - meta
status: draft
---

# NearMiss NYC — Repo & Vault

This directory is both a git repo and an Obsidian vault. Open **this folder**
(`vault/`) as the vault root in Obsidian.

## Layout

| Path | Holds |
|---|---|
| `PRD.md` | Canonical product + implementation source of truth. Conflicts resolve in its favour. |
| `00-Inbox/` | Unsorted capture. Triage into a numbered folder. |
| `01-Event/` … `12-Logs/` | The knowledge base. See [[Home]]. |
| `11-Templates/` | Obsidian Templates plugin source folder. |
| `Assets/` | Attachments (images, PDFs). Obsidian files drops here automatically. |
| `app/` | Application source — backend and frontend. |
| `demo/fixtures/` | Recorded fixtures for the deterministic demo. Committed on purpose. |
| `tests/` | Test suites. |

## Setup

```bash
cp .env.example .env   # then fill in
```

Numbered prefixes control sort order in the file explorer; they are part of the
filename and therefore part of every wikilink.

## Conventions

Notes carry `title`, `tags`, and `status` frontmatter. `{{UPPER_SNAKE}}` is an
unresolved fact — grep for `{{` to list them. Full rules in [[CLAUDE]].
