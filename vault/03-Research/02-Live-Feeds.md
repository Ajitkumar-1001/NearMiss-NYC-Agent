---
title: Live Feeds
tags:
  - research
status: active
---

# Live Feeds

Real-time NYC sources. **Part of P0, not an enhancement.**

This note previously said live feeds were "treated as an enhancement, never a
demo dependency". That predates the v2.0 consolidation, which promoted real-feed
analysis from P2 to P0 ([[00-Source-of-Truth-PRD|PRD]] §1.1). Under v2.1,
[[00-Source-of-Truth-PRD|PRD]] §29 locks "Real NYC source analysis is part of
P0", and [[ADR-006-Real-Source-P0-with-Captured-Fallback]] supersedes
`ADR-001-Deterministic-Demo-First` as the P0 sequencing decision. §11.1 requires
at least one approved source adapter tested and one current source image fetched
successfully before the event.

What survived the change is the *fallback* half, not the optionality: FR-015
pairs the live source with a captured evidence sequence, and §29 keeps captured
replay as the guaranteed conflict demonstration.

> [!info] A quiet live result is a valid P0 outcome
> §12.4 enumerates the valid live-path outcomes, and a quiet one — no candidate
> conflict, or insufficient temporal evidence — is on that list. §29 locks the
> same rule and makes captured replay the guaranteed conflict demonstration. So a
> no-conflict live run is a pass, not a failure to explain away.

## Candidates

§18.1 fixes the order to try. Rows below are that order; the concrete endpoints
are still unresolved.

| Feed | Endpoint | Auth | Rate limit | Latency | Reliability |
|---|---|---|---|---|---|
| 1 — Organizer starter-pack live camera | {{ORGANIZER_FEED_ENDPOINT}} | {{ORGANIZER_FEED_AUTH}} | {{ORGANIZER_FEED_POLICY}} | {{ORGANIZER_FEED_REFRESH}} | {{ORGANIZER_FEED_RELIABILITY}} |
| 2 — Public NYC DOT traffic-camera still-image endpoint | {{NYC_DOT_STILL_ENDPOINT}} | {{NYC_DOT_STILL_AUTH}} — publicly reachable per §18.1, auth requirement unverified | Polite caching (§18.1) | Still images, refresh {{NYC_DOT_REFRESH}} | {{NYC_DOT_RELIABILITY}} |
| 3 — 511NY REST camera endpoint | {{NY511_CAMERA_ENDPOINT}} | Self-service developer key, held server-side (FR-002) | Documented request throttle (§18.4) | {{NY511_REFRESH}} | {{NY511_RELIABILITY}} |
| 4 — Phone or USB webcam physically operating in NYC | Local device | None | n/a | {{WEBCAM_REFRESH}} | Emergency live-input demonstration only |

> [!todo] Endpoints still open
> Which source we actually use is the §30 open question "Which organizer or city
> camera source is most reliable?" — deadline **kickoff, 4:45 PM**, default "use
> the already tested approved source". [[Camera-Source]] owns that decision and
> its blockers; the tested result lands back here.

FR-002 requires only that at least one current NYC source image is fetched
through a provider adapter, with credentials and any key-bearing URL kept
server-side — so row 3's key never reaches the browser.

§18.3 bars five classes of P0 dependency. The two that bite when filling this
table are an undocumented endpoint with no source/usage note, and any source
whose availability cannot be tested before the demo. A candidate that cannot be
exercised before Friday does not belong in the table.

**Polling.** §18.4 governs every candidate in the table: source-specific polling
policy, the 511NY documented throttle, cached metadata instead of refetched
unchanged images, and a stored content hash. The hash is what matters most here
— a repeated still frame must not count as new temporal evidence, so it is the
guard against a stalled feed producing invented motion. That guard belongs in
[[07-Provider-Adapters]], which does not yet define it. Whether any candidate
changes content fast enough for trajectory analysis is the §30 open question
"Does the selected source update frequently enough for temporal analysis?";
[[Source-Temporal-Sufficiency]] owns that measurement and the duplicate-frame
trap.

**Acceptance bar.** A candidate only counts as working once it clears §24.3 —
repeat-fetch stability, timestamp and duplicate-hash behaviour, a visible
fallback on outage, and `insufficient_temporal_evidence` on single-frame input
instead of a fabricated event.

NFR-006 sets a separate bar — live source fetch plus perception under 20 seconds.
That bounds our adapter round-trip, **not** the source's refresh cadence, which is
what the Latency column above records. A source refreshing every 20 s neither
fails nor passes NFR-006; whether its cadence supports trajectories is the §30
question "Does the selected source update frequently enough for temporal
analysis?" — see [[Source-Temporal-Sufficiency]].

## Failure behaviour

If a feed is down mid-demo the system must degrade without a visible error.
FR-015 names the specific fallback: live source → captured evidence sequence.
The degraded run stays labelled — §12.4 calls this "source unavailable with a
clearly labeled fallback", and FR-016 forbids representing fallback operation as
live inference. [[05-Demo-Reliability]] covers the drill; the adapter-boundary
half belongs in [[07-Provider-Adapters]], still to be written.

## Open questions

- [ ] Terms of use permit our access pattern? → [[02-Rules-and-Constraints]].
      §18.5 requires the README and dashboard to state attribution and the known
      usage limitation, so this has to be answerable in one line per source.
- [ ] Do we need to cache/replay to avoid rate limits? §18.4 already answers yes
      for caching; what remains is the per-source polling interval.
- [ ] Which candidate becomes the demo source? → [[Camera-Source]] (§30, kickoff
      4:45 PM).
- [ ] Does it update frequently enough for temporal analysis? →
      [[Source-Temporal-Sufficiency]] (§30, before 5:35 PM; default is live
      snapshot proof only, with captured replay carrying trajectories).

---
Related: [[01-Datasets]] · [[07-Provider-Adapters]] · [[05-Demo-Reliability]] · [[03-Data-Flow]] · [[Camera-Source]] · [[Source-Temporal-Sufficiency]] · [[ADR-006-Real-Source-P0-with-Captured-Fallback]]
