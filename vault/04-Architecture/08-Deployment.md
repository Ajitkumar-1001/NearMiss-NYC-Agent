---
title: Deployment
tags:
  - architecture
status: draft
---

# Deployment

## Targets

| Piece | Host | URL | Deployed by |
|---|---|---|---|
| Frontend | {{FE_HOST}} | {{FE_URL}} | |
| Backend | {{BE_HOST}} | {{BE_URL}} | |

> [!todo] Not filled in yet


## Environments

- **Local** — the demo must work here with no network. Non-negotiable per
  [[ADR-001-Deterministic-Demo-First]].
- **Deployed** — for judges to click after the pitch.

## Configuration

Environment variables only; see `.env.example` and [[07-Provider-Adapters]].

> [!warning] No authentication
> Per [[ADR-005-No-Authentication]] anything deployed is public. Do not deploy
> anything with real personal data in it.

## Rollback

- [ ] How do we get back to the last working build fast? → [[05-Demo-Reliability]]

---
Related: [[ADR-005-No-Authentication]] · [[05-Demo-Reliability]] · [[07-Provider-Adapters]] · [[09-Observability]]
