---
title: Prior Art
tags:
  - research
status: active
---

# Prior Art

What already exists, and the specific gap we're filling.

## Existing work

| Work | What it does | Gap for our use | Link |
|---|---|---|---|
| {{WORK}} | {{WHAT_IT_DOES}} | {{GAP_FOR_OUR_USE}} | {{LINK}} |

> [!todo] Not filled in yet
> No prior-art search has been run. The vault holds no researched prior art, and the
> [[00-Source-of-Truth-PRD|PRD]] names no competing product, paper, or prior system — it
> names sponsor and stack vendors only, and it establishes what NearMiss does and what it
> refuses to claim, never what anyone else has already built. Nothing goes in the table
> until it has actually been looked up and
> read. Do not populate it from memory.

> [!warning] This blocks a judge answer
> [[05-Judge-Questions]] routes "Why doesn't X already solve this?" straight back to this
> note. Right now that row cannot be answered with a named X, only with the differentiator
> below. Naming a wrong or invented X in front of judges is worse than saying the search
> is outstanding.

Categories that need checking, and what a hit in each would change:

- **Surrogate-safety / traffic-conflict literature.** [[00-Source-of-Truth-PRD|PRD]] §4
  states that road-safety decisions frequently rely on lagging indicators such as reported
  crashes, and that street-camera footage *may contain* earlier visual indicators. A hit
  here does not threaten the product — it strengthens that hedge, and it also belongs in
  [[05-Safety-Methodology]].
- **Commercial intersection video-analytics products.** A hit tells us whether the gap is
  capability or access, and forces a sharper answer than "nobody does this."
- **Open-source detection/tracking repos that score pairwise road-user interaction.** A
  hit directly tests whether `vision-conflict-analytics` (§2.4, FR-022) is a new primitive
  or a re-implementation, and whether we should consume rather than publish.
- **Roboflow-ecosystem workflows or community blocks doing interaction analysis.** §2.4
  names a Roboflow Workflow block as a post-P0 contribution path; if one already exists,
  that path changes shape.
- **City, DOT, and Vision Zero camera-based near-miss programs.** §6.2 lists Vision Zero
  researchers as secondary users, so an existing municipal program is a reference customer
  and a comparison point at once.
- **Public NYC work built on the same camera and open-data sources.** A hit constrains the
  demo narrative and may supply source-attribution precedent.

## Our differentiator

NearMiss NYC does not count objects — it turns one real NYC camera source into a
source-attributed, event-level candidate conflict carrying an explainable visual
conflict-risk proxy that is stated up front to be a human-review prioritization signal
rather than a crash probability.

That sentence rests on four things the [[00-Source-of-Truth-PRD|PRD]] already fixes:

- **Not a counting dashboard.** §4 identifies exactly what conventional object-detection
  dashboards leave out: event-level evidence, disclosed uncertainty, connection to public
  context, and a stated reason the interaction deserves review. Those four are the product.
- **The honesty boundary is the claim, not a caveat.** §19.1 defines the proxy by what it
  is not, §19.3 keeps a human in the loop on every high-severity candidate, and §9 rules
  out both validated time-to-collision from an uncalibrated camera and any claim that every
  candidate event is a true near-miss. Anything that markets a calibrated crash probability
  off an uncalibrated street camera is making a claim this product deliberately refuses to
  make — and that refusal is defensible in a way the claim is not.
- **The primitive is separable and public — once it ships.** §2.4 and FR-022 *require* the
  pairwise track-interaction engine to be a standalone permissively licensed package with a
  domain-neutral API, consumed by NearMiss at a pinned release. §11.1 lists the repository,
  license, schemas, tests, and published release as pre-event baseline items, all still
  unchecked. Stated as a commitment the PRD makes, it is a real differentiator; stated as an
  accomplished fact before the release exists, it is an overclaim.
- **Bounded on purpose.** §5 scopes the hackathon build to one narrow vertical slice of a
  city-scale safety-intelligence layer, and §6.3 excludes enforcement, dispatch, insurance
  adjudication, individual behavior scoring, and any identification use. The honest
  comparison set is human-review tooling, not enforcement systems.

> [!question] A judge will ask "why doesn't X already solve this?"
> The answer needs to be one sentence and specific. Draft it here, use it in
> [[05-Judge-Questions]].

---
Related: [[02-Problem-Statement]] · [[05-Judge-Questions]] · [[04-Computer-Vision-Notes]] · [[05-Safety-Methodology]] · [[00-Source-of-Truth-PRD|PRD]]
