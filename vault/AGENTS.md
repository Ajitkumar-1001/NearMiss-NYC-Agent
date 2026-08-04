---
title: AGENTS
tags:
  - meta
status: draft
---

# Agent instructions

Same rules as [[CLAUDE]] — read that first. This file exists so non-Claude
agents pick up the same conventions.

## Summary

- Vault root is this directory. Notes are the deliverable.
- Every note: `title` / `tags` / `status` frontmatter.
- Unknown facts: `{{UPPER_SNAKE}}` placeholders. Never fabricate event details,
  sponsor names, dates, metrics, or benchmark results.
- Wikilinks use the full basename including number prefix.
- `[[README]]` refers only to the root README; four other README files exist and
  must not be used as link targets.
- Decisions that constrain the build go in [[PRD]] §29; changing one follows the
  §31 change-control protocol. There is no ADR folder.

## Before finishing an edit

Check no wikilink points at a note that doesn't exist:

```bash
python3 - <<'PY'
import pathlib, re, sys
names = {p.stem for p in pathlib.Path('.').rglob('*.md') if '.obsidian' not in p.parts}
broken = {(str(p), m.strip()) for p in pathlib.Path('.').rglob('*.md')
          if '.obsidian' not in p.parts
          for m in re.findall(r'\[\[([^\]|#]+)', p.read_text())
          if m.strip() not in names}
print('BROKEN:', broken or 'none'); sys.exit(1 if broken else 0)
PY
```
