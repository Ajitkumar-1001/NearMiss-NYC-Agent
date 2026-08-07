---
title: Clarify Prompt
tags:
  - speckit
status: active
---

# Clarify Prompt

**Purpose:** Find ambiguity in the spec before it becomes rework.

> [!warning] Stage complete — do not re-run `/clarify`
> [[00-Source-of-Truth-PRD|PRD]] §30 is the clarification register. It is an
> unnumbered table where every remaining open question already carries a
> decision deadline and a default to apply when unresolved — so an unanswered
> question no longer blocks the build, it just selects the default.
>
> Eight of the nine §30 rows are captured as their own note in `00-Inbox/`,
> each restating the question text, deadline, default, what it blocks, and how
> to resolve it: [[Camera-Source]], [[Source-Temporal-Sufficiency]],
> [[Roboflow-Model]], [[Demo-Intersection]], [[NYC-Open-Data-Fields]],
> [[Starter-Repo-Format]], [[Roboflow-Upstream-Path]], [[Veris-Integration]].
> The remaining row — the pre-existing-code policy question — has no inbox
> note. Its §30 deadline is Thursday 6 August, reconfirmed at kickoff, and its
> default is to disclose all prepared work in the README and submission notes
> and separate pre-event from event-day commits;
> [[09-Preexisting-Code-Disclosure]] is where that disclosure gets drafted, but
> it does not itself carry the question, the deadline, or the default. Resolve
> these in their owning notes and record the answer per [[00-Triage]]; do not
> file answers back into §30.
>
> Generating a fresh ambiguity list now competes with a register that already
> has deadlines attached. The entry point for build work is [[03-Plan-Prompt]].

## Prompt

Kept for reference, and for one live use: when an organizer statement at kickoff
contradicts a §30 default, run this against that statement alone.

```text
CONTEXT
The clarification register for NearMiss NYC is [[00-Source-of-Truth-PRD|PRD]]
§30 — an unnumbered table of open questions, each with a decision deadline and
a default. Per-question detail lives in `00-Inbox/`. Do not regenerate the
register.

Scope this run to NEW ambiguity only: an organizer statement, a starter asset,
or a source behaviour that contradicts a §30 default or a §2.1 event fact.
Cite §30 rows by their question text, never by number.

1. List every underspecified term
2. For each, give the competing readings
3. Say which reading changes the build and how
4. Rank by cost of getting it wrong
5. Do not resolve them by guessing — name the §30 default that applies until
   it is resolved

Constraints: follow [[01-Constitution]]. Do not invent facts — mark unknowns
as {{UPPER_SNAKE}} placeholders and list them as open questions. A same-day
organizer override goes in [[05-Decision-Log]], not in the PRD.
```

---
Related: [[04-Organizer-Questions]] · [[07-Blocker-Log]] · [[04-MVP-Scope]] · [[02-Workflow]]
