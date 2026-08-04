---
title: Provider Adapters
tags:
  - architecture
status: draft
---

# Provider Adapters

Every external model or data provider sits behind an adapter — rationale in
[[ADR-003-Provider-Adapter-Architecture]].

## Adapter interface

- [ ] Define the common interface once here, before writing the second adapter

## Registered adapters

| Adapter | Provider | Env var | Fallback | Status |
|---|---|---|---|---|
| {{ADAPTER}} | {{PROVIDER}} | `{{ENV_VAR}}` | fixture | todo |

> [!todo] Not filled in yet


## Rules

1. Business logic never imports a vendor SDK directly.
2. Every adapter has a **fixture implementation** — this is what makes
   [[ADR-001-Deterministic-Demo-First]] achievable.
3. Provider selection is configuration, not code.
4. Failures are typed and handled at the adapter boundary, not leaked upward.

## Credentials

Declared in `.env.example`, supplied via `.env`, never committed. Sponsor-issued
keys tracked in [[03-Sponsor-Resources]].

---
Related: [[ADR-003-Provider-Adapter-Architecture]] · [[ADR-001-Deterministic-Demo-First]] · [[03-Sponsor-Resources]] · [[02-Live-Feeds]]
