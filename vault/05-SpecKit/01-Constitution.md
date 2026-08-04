---
title: Constitution
tags:
  - speckit
status: draft
---

# Constitution

Non-negotiable principles for this build. When a decision is contested, this
note wins.

## Principles

1. **The demo works offline.** Fixtures first — [[PRD]] §29.
2. **Vendors are replaceable.** All external calls behind adapters —
   [[PRD]] §29.
3. **Honest claims only.** No number in the pitch that isn't measured in
   [[06-Success-Metrics]].
4. **State the limits.** The conflict score is a proxy —
   [[05-Safety-Methodology]].
5. **Cut scope, not quality.** When time runs out, drop features via
   [[03-Scope-Ladder]]; don't ship a broken version of everything.
6. {{PRINCIPLE}}

> [!todo] Not filled in yet
> Add anything the team agrees is genuinely non-negotiable. Keep it short —
> a list of twenty principles is a list of none.

## Amending

Changing a principle requires an entry in [[05-Decision-Log]] and, if it
constrains the build, an ADR.

---
Related: [[02-Workflow]] · [[PRD]] §29 · [[05-Decision-Log]] · [[08-Definition-of-Done]]
