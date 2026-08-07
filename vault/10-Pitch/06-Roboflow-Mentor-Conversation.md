---
title: Roboflow Mentor Conversation
tags:
  - pitch
status: draft
---

# Roboflow Mentor Conversation

> [!todo] Not held yet
> Nothing below is a record of anything said. `{{PLACEHOLDER}}` marks what a
> Roboflow mentor still has to answer. Do not present these as guidance
> received.

- **When:** {{MENTOR_SESSION_TIME}}
- **Who:** {{MENTOR_NAME}}
- **Format:** {{MENTOR_SESSION_FORMAT}}

## What we want out of it

Three decisions in [[00-Source-of-Truth-PRD|PRD]] §29 rest on Roboflow assumptions that only a mentor
can confirm quickly. Ask about those, not about generic advice.

## Questions

**Perception path** — §17 preference order is Workflow → hosted/serverless
RF-DETR → local RF-DETR → stored detections.

1. For a 10–20 s NYC street sequence at demo latency, is a Workflow or direct
   hosted inference the better path?
2. Which RF-DETR size holds up on CPU-only Cloud Run? §29 locks CPU-first.
3. Do the Apache-2.0 N/S/M/L weights cover our submission, and is anything about
   the Plus weights' license negotiable for a hackathon?

**Tracking** — §17 names ByteTrack or Roboflow `trackers`.

4. Which associates more stably on short sequences with occlusion?
5. Any known failure mode for pedestrian–vehicle pairs specifically?

**The package** — [[11-Vision-Conflict-Analytics-Package]].

6. Is a Workflow block the right contribution shape for pairwise conflict
   scoring, or is a plain library more useful to the community?
7. What would make it worth featuring, and what is the actual submission path?

**Operational**

8. Rate limits or throttling we should expect on hackathon day?
9. Anything in the starter feeds that behaves unlike a normal camera endpoint?

## What they said

{{MENTOR_ANSWERS}}

## What changed as a result

Nothing yet. Anything that changes a locked decision goes through [[00-Source-of-Truth-PRD|PRD]] §31;
anything smaller goes to [[05-Decision-Log]] with a timestamp.

| Answer | Impact | Recorded in |
|---|---|---|
| | | |

---
Related: [[00-Source-of-Truth-PRD|PRD]] · [[05-Roboflow-and-Event-Preparation-Brief]] · [[04-Computer-Vision-Notes]] · [[11-Vision-Conflict-Analytics-Package]] · [[03-Sponsor-Resources]] · [[05-Decision-Log]]
