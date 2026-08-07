---
title: Datasets
tags:
  - research
status: active
---

# Datasets

Candidate and chosen datasets. One [[Dataset-Card]] per dataset we actually use.

Camera and image sources are not listed here — those are primary sources and
belong to [[02-Live-Feeds]]. This note covers enrichment only: the tabular and
feed datasets that add context around an event after it has been detected.

## Candidates

The rows below cover the three enrichment source families approved in
[[00-Source-of-Truth-PRD|PRD]] §18.2, with the Socrata bullet split into its
collision and 311 datasets. Sources outside §18.2 are not approved enrichment
sources, and §18.3 separately names prohibited P0 dependencies. Changing either
list requires the §31 change-control protocol, which is under a pre-event
document freeze.

| Dataset | Source | License | Size | Fits our need? | Card |
|---|---|---|---|---|---|
| **NYC Open Data — NYPD Motor Vehicle Collisions** (proposed id `h9gi-nx95`; id and published title unverified) | Socrata, {{SOCRATA_COLLISIONS_URL}} | {{LICENSE}} | {{ROW_COUNT}} | **Selected** — nearby reported collisions and vulnerable-road-user involvement (FR-013), surfaced as `nearby_collision_count` in the §20 contract | pending |
| NYC Open Data — 311 | Socrata, {{SOCRATA_311_URL}} | {{LICENSE}} | {{ROW_COUNT}} | Approved "where relevant" (§18.2); no P0 or P1 use identified yet | pending |
| 511NY — incidents/roadwork | REST, {{NY511_INCIDENTS_URL}} | {{LICENSE}} | {{ROW_COUNT}} | Approved "when relevant" (§18.2); note the REST throttle in §18.4 | pending |
| MTA GTFS-realtime | {{MTA_GTFS_RT_URL}} | {{LICENSE}} | n/a — feed | P2 contextual source only (§18.2) | pending |

511NY appears in this table as an enrichment source and in [[02-Live-Feeds]] as
an approved primary camera source (§18.1). Both fall under the same §18.4
request throttle. Whether the incidents endpoint takes the same self-service
developer key as the camera endpoint is **unverified** — §18.1 attaches that key
to the REST camera endpoint only, and §18.2's incidents/roadwork bullet says
nothing about auth: {{NY511_INCIDENTS_AUTH}}, to be confirmed with the §27.1
Thursday task "Obtain the selected 511NY key and/or Socrata token only when
used". [[02-Live-Feeds]] owns the polling policy.

Which fields inside these datasets are stable enough to depend on is the
[[00-Source-of-Truth-PRD|PRD]] §30 open question "Which NYC Open Data fields are
stable?" — deadline Thursday, 6 August. Tracked in [[NYC-Open-Data-Fields]]. The
§30 default if it stays unresolved is cached, source-attributed context — which
is what P0 ships anyway, since runtime NYC Open Data lookup is P1 (§29).

> [!todo] Endpoints, licenses, and sizes still unfilled
> The datasets are settled; their retrieval details are not. Confirm licensing
> before anything ships — see [[02-Rules-and-Constraints]].

[[00-Source-of-Truth-PRD|PRD]] §18.5 fixes a seven-item per-source disclosure set
the README and dashboard must show. Vault convention: a card that cannot supply
all seven is not enough to back that disclosure surface.

The [[Dataset-Card]] template already covers provider, license, retrieval
timestamp, and the attribution requirement. It is missing source category,
retrieval method, freshness class, and usage limitation — add those four when
filling a card. The freshness class is the same current/cached/captured/fixture
distinction FR-003 requires the UI to display.

Vault convention: treat a shipped enrichment dataset as a registry source and give
it an FR-001 record too, so the §18.5 disclosure has a runtime backing. The two
overlap rather than nest — FR-001 carries retrieval-oriented fields the card does
not (jurisdiction, fetch method, polling/cache policy, enabled status), and the
card carries license and retrieval timestamp, which FR-001 does not list. Keep
them consistent where they meet.

## Selected

**NYPD Motor Vehicle Collisions — proposed NYC Open Data Socrata dataset id
`h9gi-nx95`**, selected by user direction 5 Aug. Neither the id nor the dataset's
published title on the portal has been looked up; both are selected-but-unverified.

This is not a new approval. [[00-Source-of-Truth-PRD|PRD]] §18.2 already approves
"NYC Open Data Socrata datasets, including collision and 311 datasets where
relevant", so naming the specific dataset answers the §30 open question "Which
NYC Open Data fields are stable?" **at the dataset level only**. The
field-stability half — which columns are consistently populated — stays open to
its Thursday, 6 August deadline, default "use cached, source-attributed context".
The selection is recorded in [[05-Decision-Log]] (Wed 5 Aug, 7:56 PM); the
rejected alternatives are not yet logged. It is **not** a §31 change-control item
and **not** a PRD version increment.

Still no runtime dependency. P0 does not need one: the captured-evidence baseline
in §11.1 requires cached, source-attributed NYC historical context committed
before the event, and the runtime lookup is P1 (§29).

- [ ] Pick the collisions dataset query — radius, time window, fields — and
      capture one real response as the cached fixture. **Overdue** — §27.1 placed
      this in the Wednesday 5 August block that commits the context fixture. It
      now falls inside the §11.1 readiness gate closing tonight at 8:00 PM.
- [ ] Confirm the published dataset title and the id `h9gi-nx95` against the
      portal, and verify the field set below against the live schema
- [ ] Record the rejected alternatives in [[05-Decision-Log]]

The backstop is the §11.1 readiness rule: if the captured evidence baseline is
incomplete by Thursday, 6 August at 8:00 PM America/New_York, all optional
product work stops until it is finished.

## Field set

> [!warning] Proposed and unverified — nobody has queried the API
> The columns below are the field set the strategy proposes, pending
> verification against the live `h9gi-nx95` schema. Do not treat them as
> confirmed. Verification is due with the §30 question "Which NYC Open Data
> fields are stable?" on Thursday, 6 August; if it slips, the §30 default —
> cached, source-attributed context — is what ships, which is the P0 path
> anyway.

| Group | Proposed columns |
|---|---|
| Location and time | `crash_date`, `crash_time`, `borough`, `latitude`, `longitude`, `on_street_name`, `cross_street_name`, `off_street_name` |
| Harm counts | `number_of_persons_injured`, `number_of_persons_killed`, `number_of_pedestrians_injured`, `number_of_pedestrians_killed`, `number_of_cyclist_injured`, `number_of_cyclist_killed`, `number_of_motorist_injured`, `number_of_motorist_killed` |
| Cause and record identity | `contributing_factor_vehicle_1`, `vehicle_type_code1`, `collision_id` |

Both halves are open. Nobody has queried `h9gi-nx95`, so whether these columns
*exist* in the live schema is simply untested; the §30 question covers whether
the fields are stable enough to depend on, and neither presence nor population
has been checked. That is what [[NYC-Open-Data-Fields]] tracks. A column that is
absent, or present but blank on most rows, cannot back a §18.5 disclosure or an
FR-013 context payload.

## Data modes

Three ways to get the context, in the order we should reach for them. The
three-mode split is **this note's proposal**, not PRD structure: FR-015 lists a
single NYC Open Data rung, "NYC Open Data → cached context". The Status column
says where each mode stands; it is not a claim that the PRD defines three tiers.

| Mode | When it runs | What it produces | Status |
|---|---|---|---|
| API mode | Once per camera location, at query time — pass the camera coordinates, aggregate the returned rows | An aggregate held in memory and cached | P1 (§29 runtime lookup) |
| Cached camera mode | Once, as soon as the feed location is known — query, aggregate, save `demo/fixtures/context.json`, reuse it from then on | A committed per-camera context file | The P0 path (§11.1); this is the FR-015 "NYC Open Data → cached context" rung |
| Fallback dataset mode | Never at runtime — a small local sample committed before the event | A fixture the demo can run from with no network | **Proposed extra backstop — not in the PRD.** FR-015 recognises one cached-context rung, which "Cached camera mode" already occupies |

> [!important] The rule that matters
> Do **not** call the API per frame or per event. One query per camera location,
> then reuse. §18.4 requires respecting the source polling policy and caching
> source metadata; per-frame lookup violates that and puts a network call on the
> demo's critical path.

## Aggregate shape

What the enrichment layer should hand back after aggregating the returned rows.
This is a **shape**, not data — no count is asserted *here* until a real response
is captured. (§20's core data contract carries an illustrative
`nearby_collision_count`; that is a schema example, not measured data.)

| Aggregate | Derived from |
|---|---|
| Total crashes in radius and window | Row count |
| Persons injured | Sum of the person-injury column |
| Pedestrians injured | Sum of the pedestrian-injury column |
| Cyclists injured | Sum of the cyclist-injury column |
| Fatal crashes | Rows with any non-zero killed column |
| Top contributing factors | Frequency ranking of the contributing-factor column |

This aggregate is **displayed beside** the conflict-risk score, never inside it.
§19.1 defines the proxy as ranking image-space evidence, and §23 keeps observed
evidence, derived metrics, and public context separate — a location prior would
make identical geometry score differently by neighbourhood. FR-013 says the same
thing from the other side: historical context is never presented as evidence
observed in the current frame.

> [!bug] Gap: the context model cannot carry what FR-013 requires
> Tracked as **C-10** in [[04-Task-Board]] — do not restate it here. The drift in
> one line: §20's core data contract already specifies `dataset_id` inside
> `historical_context`; `nearmiss/models.py:105` `HistoricalContext` does not.
> Flagged here, not fixed — this note does not own the model.

## Local copies

[[00-Source-of-Truth-PRD|PRD]] §29 makes JSON fixtures and captured assets
operational fallbacks, and §11.1 requires them committed before the event. This
vault keeps them in `demo/fixtures/` — a repo convention, not a PRD requirement.

The cached context fixture is itself a §11.1 deliverable, alongside the
normalized fixture schema. FR-013 requires the dataset identifier, query radius,
time window, and retrieval timestamp to travel with the context, so the fixture
has to carry them too — otherwise the README and dashboard cannot state what
§18.5 requires.

Neither fixture exists yet. `demo/fixtures/` holds only `README.md`.
`nearmiss/providers/context.py` `CachedContext` reads
`demo/fixtures/context.json`, and `NycOpenDataContext.lookup` raises
`ProviderUnavailable` unconditionally — so the P0 path has a reader and no file.
That file is the overdue capture task above.

---
Related: [[02-Live-Feeds]] · [[Dataset-Card]] · [[NYC-Open-Data-Fields]] · [[04-Computer-Vision-Notes]] · [[04-Task-Board]] · [[05-Decision-Log]] · [[00-Source-of-Truth-PRD|PRD]] §18.2 · §18.5 · §29 · FR-013
