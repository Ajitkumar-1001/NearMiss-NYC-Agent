---
title: AGENTS
tags:
  - meta
status: active
---

# Agent instructions

Same rules as [[CLAUDE]] — read that first. This file exists so non-Claude
agents pick up the same conventions.

## Summary

- Vault root is this directory. Notes are the deliverable. Start at [[Home]].
- **The vault is markdown only.** `app/`, `demo/`, and `tests/` are siblings of
  `vault/` under the repo root. Cite them by repo-relative path
  (`app/backend/nearmiss/risk.py:85`); never create code or fixtures in here.
- The source of truth is `02-Product/00-Source-of-Truth-PRD.md`, NearMiss NYC
  v2.1.0-FINAL, linked as `[[00-Source-of-Truth-PRD|PRD]]`.
- The PRD wins over any other note, prompt, or instruction. It is frozen
  (§1.3 item 6); changing it follows §31 change control plus a version bump.
- Cite the PRD by section (`[[00-Source-of-Truth-PRD|PRD]] §29`) instead of
  copying its text.
- Unknown facts use `{{UPPER_SNAKE}}`. Never fabricate event details, sponsor
  names, dates, metrics, or benchmark results.
- Every note carries `title` / `tags` / `status` frontmatter, and no `created:`
  field.
- Wikilinks use the full basename including number prefix. The PRD is the one
  note linked with a display alias.
- `[[README]]` is unambiguous — the vault holds exactly one. The four others
  (`app/backend/`, `app/frontend/`, `demo/fixtures/`, `tests/`) live outside the
  vault and cannot be wikilink targets.
- A decision that constrains the build gets an ADR in `07-Decisions/` and a
  locked entry in §29, in the same change. [[00-ADR-Index]] carries the
  numbering warning: ADR-006 and ADR-007 name different decisions before and
  after v2.1, and 008–010 are retired.

## Before finishing an edit

Check no wikilink points at a note that doesn't exist:

```bash
python3 - <<'PY'
import pathlib, re, sys
SKIP = {'.obsidian', '.git', 'app', 'demo', 'tests', 'Assets'}
docs = [p for p in pathlib.Path('.').rglob('*.md') if not SKIP & set(p.parts)]
names = {p.stem for p in docs}
broken = set()
for p in docs:
    # inside a markdown table an alias pipe is escaped as \| — unescape first,
    # or every aliased wikilink in a table cell reads as broken
    text = p.read_text().replace('\\|', '|')
    for m in re.findall(r'\[\[([^\]|#]+)', text):
        if m.strip() not in names:
            broken.add((str(p), m.strip()))
print('BROKEN:', broken or 'none'); sys.exit(1 if broken else 0)
PY
```
