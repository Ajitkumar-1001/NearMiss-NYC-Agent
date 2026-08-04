---
title: Responsible AI
tags:
  - architecture
status: draft
---

# Responsible AI

Judges ask about this, and it matters independently of that.

## Data and privacy

- **Personal data in our inputs:** {{PII_ASSESSMENT}}
- [ ] Are faces / plates visible? If so, what do we do about it?
- [ ] Retention: what do we keep after the demo, and for how long?

> [!todo] Not filled in yet


## Known limitations

State plainly what the system cannot do. From [[05-Safety-Methodology]]:
the conflict score is a monocular proxy, not a measurement.

| Limitation | Consequence | Mitigation |
|---|---|---|
| {{LIMITATION}} | | |

## Bias

- [ ] Where could coverage be uneven — camera placement, lighting, time of day?
- [ ] Who is affected if the system is wrong, and in which direction?

## Misuse

- [ ] What would make this harmful — enforcement? individual tracking?
- [ ] What does the design do to make that harder?

## Framing

This surfaces patterns for safety review. It is not an enforcement tool and not
a measurement instrument. Keep that framing in [[05-Judge-Questions]].

---
Related: [[05-Safety-Methodology]] · [[05-Judge-Questions]] · [[06-Data-Model]] · [[01-Constitution]]
