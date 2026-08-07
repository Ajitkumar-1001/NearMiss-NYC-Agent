---
title: Tests
tags:
  - code
status: draft
---

# Tests

Scope and rationale: [[01-Test-Strategy]]. The case list is [[02-Test-Cases]].

## Run

```bash
{{TEST_COMMAND}}
```

## What lives here

- Pipeline stage tests against `demo/fixtures/`
- Adapter fallback tests — [[07-Provider-Adapters]]
- Contract tests against [[05-API-Contracts]]
- End-to-end demo path, network off

A task isn't done until its case here passes — [[08-Definition-of-Done]].

> [!todo] Fill in the runner once the stack is chosen.
