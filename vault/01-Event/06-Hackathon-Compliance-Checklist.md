---
title: Hackathon Compliance Checklist
tags:
  - event
status: active
---

# Hackathon Compliance Checklist

> [!info] Role
> Named in [[00-Source-of-Truth-PRD|PRD]] §32.1 for the eligibility gate, Cloud Run constraints,
> data-access lead times, and the submission checklist. §2.1 cites it for the
> eligibility and judging facts.

Each item below is tagged with its claim class per [[00-Source-of-Truth-PRD|PRD]] §32.2:
**[O]** organizer-stated · **[P]** platform constraint · **[R]** research
finding · **[E]** execution inference · **[U]** unverified.

## The gate

**[O]** The only stated eligibility gate is deployment on Google Cloud Run.

Per [[00-Source-of-Truth-PRD|PRD]] §2.2, missing this means the submission is not hackathon-complete
**even if everything runs locally**.

- [ ] Deployed on Cloud Run before the 8:30 PM lock
- [ ] Publicly reachable with no judge authentication
- [ ] `GET /health` returns HTTP 200
- [ ] At least one working real-source analysis endpoint exposed
- [ ] Deployed revision and active processing mode identified in the response
- [ ] Available for the whole demo window

## Cloud Run constraints

**[P]** Platform behaviour, not organizer rules — these fail silently in
development and loudly on stage:

- [ ] Container listens on `0.0.0.0:$PORT`, not a hardcoded port
- [ ] Service is stateless — no reliance on local disk between requests
- [ ] Public invoker access granted (`allUsers`), verified from a logged-out browser
- [ ] Concurrency and memory sized for the demo, not for scale
- [ ] Billing enabled on the personal-Gmail project **[E]**
- [ ] Cloud Run, Cloud Build, and Artifact Registry APIs enabled
- [ ] Known-good revision recorded with its rollback command

Full pre-event baseline: [[00-Source-of-Truth-PRD|PRD]] §11.1 → [[08-Deployment]].

## Data-access lead times

**[R]** The reason [[00-Source-of-Truth-PRD|PRD]] §18 bans dependence on signed bulk-feed agreements:
approval cycles outlast the event.

| Source | Lead time | Usable Friday? |
|---|---|---|
| Organizer starter feeds | Handed out at kickoff | Yes, if provided |
| Accessible NYC camera still endpoints | None | Yes |
| 511NY REST cameras | {{511NY_KEY_LEAD_TIME}} | Verify before Friday |
| NYC Open Data Socrata | Anonymous, throttled; app token raises limits | Yes |
| MTA GTFS-realtime | {{MTA_KEY_LEAD_TIME}} | P2 only |
| Signed bulk feed agreements | Weeks | **No — excluded by §18** |

- [ ] Every credential needed on Friday obtained and tested **before** Friday
- [ ] Every source recorded in the source registry with attribution and retrieval time

## Submission checklist

- [ ] Public repository
- [ ] README with setup, architecture, demo, data provenance, and limitations
- [ ] Permissive license (Apache-2.0 or MIT)
- [ ] Privacy statement — no identity recognition, no biometric processing
- [ ] Source policy and attribution
- [ ] Prepared-code disclosure → [[09-Preexisting-Code-Disclosure]]
- [ ] Fallback recording captured as a backup artifact, not the primary demo
- [ ] Live Cloud Run URL in the submission
- [ ] `vision-conflict-analytics` public repo, licensed, released, and pinned

P0 definition of done: [[00-Source-of-Truth-PRD|PRD]] §26 · [[08-Definition-of-Done]].

## Unverified — ask at kickoff

**[U]** Do not treat any of these as a rule or a benefit until confirmed:

- Exact submission mechanism — {{SUBMISSION_MECHANISM}}
- Per-team demo duration
- Final judge list
- Veris prize track and any required Veris tooling
- Attendee-specific sponsor credits

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[05-Roboflow-and-Event-Preparation-Brief]] · [[02-Rules-and-Constraints]] · [[08-Definition-of-Done]] · [[08-Deployment]] · [[ADR-007-Cloud-Run-Eligibility-Gate]]
