---
title: Component Design
tags:
  - architecture
status: draft
---

# Component Design

One section per component. Keep interfaces here, implementation in `app/`.

## {{COMPONENT_NAME}}

- **Responsibility:** {{RESPONSIBILITY}}
- **Inputs:** {{INPUTS}}
- **Outputs:** {{OUTPUTS}}
- **Owns:** {{STATE}}
- **Depends on:** {{DEPENDENCIES}}
- **Failure behaviour:** {{FAILURE}}

> [!todo] Not filled in yet
> Duplicate the block above per component.

## Boundaries

A component may only be reached through its stated interface. Provider calls go
through adapters ([[07-Provider-Adapters]]), never direct SDK calls from
business logic.

---
Related: [[02-High-Level-Design]] · [[05-API-Contracts]] · [[07-Provider-Adapters]] · [[06-Data-Model]]
