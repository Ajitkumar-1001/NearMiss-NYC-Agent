"""Explanation. FR-010, FR-011 (Gemini -> deterministic template).

The template implementation is real and is the P0 path. It is deliberately
mechanical: it restates the evidence it was given and nothing else, which is
the same constraint FR-010 puts on the language model ("shall not invent
measurements, identities, legal conclusions, or infrastructure facts not
present in supplied evidence"). A template cannot violate that constraint.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..models import HistoricalContext, Severity
from ..risk import Candidate
from .base import ProviderUnavailable


@dataclass(frozen=True)
class Explanation:
    observations: list[str]
    limitations: list[str]
    recommended_action: str
    confidence: float


# PRD §21.6 requires every report to expose limitations, and ADR-002 requires
# the proxy never to be read as a collision probability. These two are
# unconditional; situational ones get appended.
BASELINE_LIMITATIONS = [
    "The camera is not geometrically calibrated, so all motion is image-space "
    "and no measurement here is a real-world distance.",
    "The score is a visual conflict-risk proxy, not a crash probability.",
]


class GeminiExplanation:
    """Runtime structured explanation via Gemini.

    Unimplemented at P0. When wired, it must be schema-constrained — an
    unconstrained model is the "Gemini fails or hallucinates" row in the risk
    register, and the mitigation is the schema plus this template fallback.
    """

    name = "gemini"

    def __init__(self, api_key: str | None):
        self.api_key = api_key

    def explain(
        self, candidate: Candidate, context: HistoricalContext | None, severity: Severity
    ) -> Explanation:
        if not self.api_key:
            raise ProviderUnavailable(self.name, "no API key configured")
        raise ProviderUnavailable(
            self.name, "runtime explanation not implemented at P0"
        )


class TemplateExplanation:
    """Deterministic explanation. The P0 path."""

    name = "template"

    def explain(
        self, candidate: Candidate, context: HistoricalContext | None, severity: Severity
    ) -> Explanation:
        a, b = candidate.a.class_name, candidate.b.class_name
        f = candidate.factors

        observations = [
            f"A {a} (track {candidate.a.track_id}) and a {b} "
            f"(track {candidate.b.track_id}) were tracked over the same "
            f"{candidate.end_seconds - candidate.start_seconds:.1f} s window.",
            f"Their closest image-space approach was "
            f"{candidate.min_separation_px:.0f} px at "
            f"{candidate.closest_at:.1f} s.",
        ]
        if f.path_overlap >= 0.9:
            observations.append(
                "The two image-space paths converge to the point of crossing."
            )
        elif f.path_overlap >= 0.5:
            observations.append("The two image-space paths converge.")
        if f.closing_motion >= 0.5:
            observations.append(
                "Visual separation decreases across consecutive frames "
                "approaching the closest point."
            )
        else:
            observations.append(
                "Visual separation stays broadly constant, so the pair were "
                "close but not closing."
            )

        limitations = list(BASELINE_LIMITATIONS)
        if context is not None:
            observations.append(
                f"{context.nearby_collision_count} collisions are recorded "
                f"within {context.radius_meters} m of this location "
                f"({context.source})."
            )
            limitations.append(
                "Historical collisions are context for the location, not "
                "evidence about this event, and correlation is not cause."
            )
        else:
            limitations.append(
                "No historical context was available for this location."
            )

        # PRD §21.7: every high-severity event must recommend human review.
        if severity == "high":
            action = (
                "Review this event and examine whether conflicts recur at this "
                "location."
            )
        else:
            action = (
                "Optional review. Consider batching with other events at this "
                "location before acting."
            )

        return Explanation(
            observations=observations,
            limitations=limitations,
            recommended_action=action,
            # A template restates its input, so it is exactly as confident as
            # the evidence — but it has done no reasoning, and saying 1.0 would
            # overclaim. This is a fixed, honest mid value.
            confidence=0.6,
        )
