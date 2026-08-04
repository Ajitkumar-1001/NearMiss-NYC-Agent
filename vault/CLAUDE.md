---
title: CLAUDE
tags:
  - meta
status: draft
---

# Working in this vault

This is an Obsidian vault, not a source tree. Notes are the product here.

## Where things go

| Content | Folder |
|---|---|
| Hackathon rules, sponsor info, organizer Q&A | `01-Event/` |
| Problem, users, scope, metrics, demo narrative | `02-Product/` |
| Datasets, feeds, prior art, CV and safety notes | `03-Research/` |
| System design, contracts, data model, deployment | `04-Architecture/` |
| SpecKit constitution, workflow, prompts | `05-SpecKit/` |
| gstack workflow and review checklists | `06-gstack/` |
| Architecture decision records | `07-Decisions/` |
| Runbook, time-box, task board, risks, blockers | `08-Execution/` |
| Test strategy, cases, agent/vision eval | `09-Evaluation/` |
| Pitch copy, judging map, demo script | `10-Pitch/` |
| Reusable note templates | `11-Templates/` |
| Running logs and changelog | `12-Logs/` |

Unsorted capture goes to `00-Inbox/` and gets triaged, not left there.

## Note rules

1. **Frontmatter on every note** — `title`, `tags` (one domain tag), `status`
   (`draft` / `active` / `done`). Nothing else unless there's a reason.
2. **Unknown facts use `{{UPPER_SNAKE}}`** — never invent an event name, date,
   sponsor, metric, or benchmark number. Uppercase avoids colliding with
   Obsidian's lowercase template variables (`{{title}}`, `{{date}}`, `{{time}}`),
   which are live substitutions inside `11-Templates/` only.
3. **Wikilinks by basename** — `[[04-MVP-Scope]]`, including the number prefix.
4. **Never link `[[README]]` except to the root one.** There are five
   `README.md` files (root, `app/backend/`, `app/frontend/`, `demo/fixtures/`,
   `tests/`); the four sub-READMEs link outward but are never link targets.
5. **A decision that constrains the build becomes an ADR** in `07-Decisions/`
   from [[ADR-Template]], and gets a row in [[00-ADR-Index]].

## Don't

- Don't add a `created:` date to frontmatter — file ctime already has it.
- Don't renumber folders; the prefixes are baked into every wikilink.
- Don't commit `.env`. Use [[README]] setup steps.
