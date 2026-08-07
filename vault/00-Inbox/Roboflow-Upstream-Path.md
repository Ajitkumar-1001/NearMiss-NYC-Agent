---
title: How does Roboflow want the interaction primitive contributed?
tags:
  - inbox
status: draft
---

# Community plugin, core block proposal, or standalone OSS package?

> [!info] Source
> [[00-Source-of-Truth-PRD|PRD]] §30 — "Does Roboflow prefer the interaction
> primitive as a community plugin, core block proposal, or standalone OSS
> package?" New in v2.1 — no capture existed for it.

- **Captured:** 2026-08-04
- **Source:** [[00-Source-of-Truth-PRD|PRD]] §30 (v2.1.0-FINAL), "Does Roboflow
  prefer the interaction primitive as a community plugin, core block proposal,
  or standalone OSS package?"
- **Decision deadline:** mentor conversation, **after P0 is stable**
- **Default if unresolved:** keep the standalone package; ask for the preferred
  upstream path **without attempting an onsite refactor**

## Why it matters

[[11-Vision-Conflict-Analytics-Package]] is a P0 artifact and its shape is
already locked: a public, permissively licensed Python package that NearMiss
consumes through a pinned release ([[00-Source-of-Truth-PRD|PRD]] §29).

This question is only about the **upstream contribution path** — whether
Roboflow would rather see it as a Workflow block, a community plugin, or exactly
what it already is. §2.4 and §29 both place that wrapper **post-P0**.

> [!warning] The real risk here is scope, not the answer
> The deadline is deliberately *after P0 is stable*, and the default explicitly
> forbids an onsite refactor. A mentor saying "a Workflow block would be great"
> is an invitation to rebuild the package during the build window — which is how
> a submission gets lost. Note the answer, ship the library, do the wrapper after
> Friday.

## When to ask

During the Roboflow mentor conversation — questions 6 and 7 in
[[06-Roboflow-Mentor-Conversation]] are this question. Ask them **after** the
package is released and pinned, not before.

## How to resolve

- [ ] Confirm P0 is stable first — deployment baseline and captured evidence green
- [ ] Ask which shape is most useful to the Roboflow community and why
- [ ] Ask what the actual submission/review path is for that shape
- [ ] Write the answer down. Do **not** start the refactor.

## Triage to

[[06-Roboflow-Mentor-Conversation]] for the answer as given;
[[11-Vision-Conflict-Analytics-Package]] for the post-P0 contribution plan; the
call itself to [[05-Decision-Log]].

Changing the package's shape *before* the submission would touch a §29 locked
decision and need the §31 protocol — which the pre-event freeze makes
deliberately expensive. That is the point.

---
Nothing stays in the inbox — see [[00-Triage]].
