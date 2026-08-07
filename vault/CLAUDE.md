---
title: CLAUDE
tags:
  - meta
status: active
---

# Working in this vault

This is an Obsidian vault, not a source tree. Notes are the product here.
Start at [[Home]].

**Markdown only.** The vault holds notes and nothing else. Application code,
fixtures, and tests live one level up, as siblings of `vault/`:

```
NYC-agent/          ← git repo root
├── app/            ← backend + frontend source
├── demo/           ← fixtures, captured sequence, recordings, screenshots
├── tests/          ← test suites
└── vault/          ← this directory: markdown, plus .obsidian/ and Assets/
```

Notes cite code by **repo-relative** path — `app/backend/nearmiss/risk.py:85` —
which resolves from the repo root, not from here. Never create a `.py`, config,
or fixture file inside the vault.

## The PRD wins, and it is frozen

`02-Product/00-Source-of-Truth-PRD.md` — linked everywhere as
`[[00-Source-of-Truth-PRD|PRD]]` — is v2.1.0-FINAL. When anything conflicts with
it (a note, a prompt, an implementation choice, this file), the PRD wins.
§1.3 item 6 freezes it before the event; no v2.2 is planned.

Changing it means following §31 change control: proposed change, reason,
P0/P1/P2 impact, new risks, acceptance-criteria update, ADR reference when
architectural, version increment.

Cite it by section — `[[00-Source-of-Truth-PRD|PRD]] §29` — rather than copying
its text. One copy of a fact, and it lives in the PRD.

## Event facts

From the PRD frontmatter and §2:

- **NYC Vision Hack v.2** — Friday, 7 August 2026, 4:00–10:00 PM ET
- Submission locks **8:30 PM**; demos 8:45 PM
- Hard eligibility gate (§2.2): a publicly reachable Google Cloud Run agent.
  Missing it means the submission is incomplete even if everything runs locally.

## Where things go

| Content | Folder |
|---|---|
| Hackathon rules, sponsor info, organizer Q&A, compliance | `01-Event/` |
| Problem, users, scope, metrics, demo narrative, **the PRD** | `02-Product/` |
| Datasets, feeds, prior art, CV and safety notes | `03-Research/` |
| System design, contracts, data model, deployment, packages | `04-Architecture/` |
| SpecKit constitution, workflow, prompts | `05-SpecKit/` |
| gstack workflow and review checklists | `06-gstack/` |
| ADRs and the ADR index | `07-Decisions/` |
| Runbook, time-box, task board, risks, blockers, disclosure | `08-Execution/` |
| Test strategy, cases, agent/vision eval | `09-Evaluation/` |
| Pitch copy, judging map, demo script, mentor notes | `10-Pitch/` |
| Reusable note templates | `11-Templates/` |
| Running logs and changelog | `12-Logs/` |

Unsorted capture goes to `00-Inbox/` and gets triaged, not left there —
[[00-Triage]] has the procedure.

## Note rules

1. **Frontmatter on every note** — `title`, `tags` (one domain tag), `status`
   (`draft` / `active` / `done`). Nothing else unless there's a reason.
2. **Unknown facts use `{{UPPER_SNAKE}}`** — never invent an event name, date,
   sponsor, metric, or benchmark number. Uppercase avoids colliding with
   Obsidian's lowercase template variables (`{{title}}`, `{{date}}`, `{{time}}`),
   which are live substitutions inside `11-Templates/` only.
3. **Wikilinks by basename** — `[[04-MVP-Scope]]`, including the number prefix.
   The PRD is the one note linked with a display alias, because
   `[[00-Source-of-Truth-PRD]]` reads badly mid-sentence.
4. **`[[README]]` is unambiguous now** — the vault holds exactly one `README.md`.
   The other four (`app/backend/`, `app/frontend/`, `demo/fixtures/`, `tests/`)
   moved out with the code and are no longer in the vault, so they cannot be
   wikilink targets at all. Refer to them by path, never as a wikilink.
5. **A decision that constrains the build gets an ADR in `07-Decisions/` *and* a
   locked entry in [[00-Source-of-Truth-PRD|PRD]] §29**, added in the same change
   through the §31 protocol. [[00-ADR-Index]] tracks all of them and carries the
   numbering warning — ADR-006 and ADR-007 name *different decisions* before and
   after v2.1. Smaller calls that don't constrain the build go in
   [[05-Decision-Log]].

## Don't

- Don't add a `created:` date to frontmatter — file ctime already has it.
- Don't renumber folders; the prefixes are baked into every wikilink.
- Don't reuse ADR numbers 008, 009, or 010 — retired, see [[00-ADR-Index]].
  Next free number is ADR-011.
- Don't commit `.env`. Use [[README]] setup steps.
