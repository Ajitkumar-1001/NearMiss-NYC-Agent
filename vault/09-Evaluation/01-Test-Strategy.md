---
title: Test Strategy
tags:
  - evaluation
status: draft
---

# Test Strategy

Minimum testing that keeps the demo safe. Not comprehensive coverage — there
isn't time, and that's a deliberate trade.

## What we test

| Layer | What | Why |
|---|---|---|
| Pipeline stages | Fixture in → expected out | Regressions here kill the demo |
| Adapters | Fixture fallback fires on failure | [[ADR-003-Provider-Adapter-Architecture]] |
| API | Contract shape matches [[05-API-Contracts]] | Frontend/backend drift |
| Demo path | Full end-to-end, network off | The thing judges see |

## What we don't test

- Exhaustive unit coverage
- Load / performance beyond the demo's needs
- {{NOT_TESTED}}

> [!todo] Not filled in yet


## Running

```bash
{{TEST_COMMAND}}
```

---
Related: [[02-Test-Cases]] · [[05-Demo-Reliability]] · [[08-Definition-of-Done]] · [[05-API-Contracts]]
