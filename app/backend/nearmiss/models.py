"""The shape contract.

Mirrors PRD §18 exactly for the fields it defines, plus the three FR-008 fields
the §18 example omits (`representative_frame`, `overlay`, `providers`) and
FR-010's explanation confidence.

Nothing here may drift from 04-Architecture/06-Data-Model.md. Fixtures in
demo/fixtures/ are validated against these models by tests/test_fixture_parity.py
— that test is the enforcement of ADR-010's fixture-parity rule.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# PRD §12. Only these three are supported; the risk engine currently produces
# the first two — deriving `turning_...` needs turn detection, which PRD §12
# explicitly defers ("prioritize one event type based on the selected clip").
EventType = Literal[
    "vehicle_pedestrian_conflict",
    "vehicle_cyclist_conflict",
    "turning_vehicle_vulnerable_user_conflict",
]

# PRD §12. Severity is derived from the risk proxy and evidence quality. It is
# NOT a crash probability — see ADR-002.
Severity = Literal["low", "medium", "high"]

# FR-016. Exactly one is active per report. Wire values are snake_case; the UI
# renders them title-case ("Demonstration fixture").
#
# These are FR-016's five names, not the three v1 values they replaced
# (`live_feed`, `runtime_analysis`, `demonstration_replay`) — none of which
# matched any of the five. §2.2 puts "identify the active processing mode" on
# the eligibility gate, so the label a judge reads has to be one the PRD names.
ProcessingMode = Literal[
    "live_nyc_snapshot",
    "live_sampled_sequence",
    "runtime_sequence_analysis",
    "captured_feed_replay",
    "demonstration_fixture",
]

# FR-002. The classes the pipeline recognises.
RoadUserClass = Literal["person", "bicycle", "motorcycle", "car", "bus", "truck"]


class Strict(BaseModel):
    """Reject unknown fields, so a drifting fixture fails loudly rather than
    silently losing data."""

    model_config = ConfigDict(extra="forbid")


class Point(Strict):
    """One centroid sample. Image-space — never metric distance (FR-004)."""

    frame_number: int = Field(ge=0)
    timestamp: float = Field(ge=0)
    x: float
    y: float


class Detection(Strict):
    """FR-002. One detected object in one frame."""

    class_name: RoadUserClass
    confidence: float = Field(ge=0, le=1)
    bbox: tuple[float, float, float, float]  # x1, y1, x2, y2 in image space
    frame_number: int = Field(ge=0)
    timestamp: float = Field(ge=0)


class Track(Strict):
    """FR-003. One object followed across frames.

    `track_id` is scoped to a single clip and is NOT an identity — correlating
    it across clips is forbidden by ADR-006.
    """

    track_id: int
    class_name: RoadUserClass
    centroid_history: list[Point]


class RiskFactors(Strict):
    """FR-006. Each factor is 0–1; weights live in config.RiskWeights."""

    proximity: float = Field(ge=0, le=1)
    path_overlap: float = Field(ge=0, le=1)
    closing_motion: float = Field(ge=0, le=1)
    vulnerable_user: float = Field(ge=0, le=1)


class Participant(Strict):
    track_id: int
    class_name: RoadUserClass


class TimeWindow(Strict):
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(ge=0)


class Location(Strict):
    """lat/long are nullable, not optional — P0 ships with `label` only until
    the Demo-Intersection question is answered."""

    label: str
    latitude: float | None = None
    longitude: float | None = None


class HistoricalContext(Strict):
    """FR-009. External correlation, never causal proof (PRD §21.8). Renders
    visibly separate from evidence observed in the clip."""

    source: str
    nearby_collision_count: int = Field(ge=0)
    radius_meters: int = Field(gt=0)
    retrieved_at: str


class EvidenceOverlay(Strict):
    """FR-008's "annotated clip or overlay data".

    Carries what the frontend needs to draw FR-013's overlay: the clip, its
    pixel dimensions (to scale image-space coords to the canvas), and the
    detections and tracks to render.

    `clip_path` is None until the real clip lands — see 00-Inbox/Camera-Source.
    The overlay still renders without it, against a placeholder.
    """

    clip_path: str | None
    frame_width: int = Field(gt=0)
    frame_height: int = Field(gt=0)
    fps: float = Field(gt=0)
    detections: list[Detection]
    tracks: list[Track]


class ProviderMetadata(Strict):
    """FR-008's "model/provider metadata".

    Each value names the implementation that actually served the request, so a
    fallback is visible in the payload and not just in the mode badge (FR-012).
    """

    vision: str
    tracker: str
    context: str
    explanation: str


class Event(Strict):
    """The normalized event report. PRD §18 is the source of truth for every
    field that appears there; see the module docstring for the additions."""

    event_id: str
    event_type: EventType
    severity: Severity
    risk_score: float = Field(ge=0, le=100)
    risk_factors: RiskFactors
    participants: list[Participant] = Field(min_length=2)
    time_window: TimeWindow
    location: Location
    processing_mode: ProcessingMode
    observations: list[str] = Field(min_length=1)
    historical_context: HistoricalContext | None = None
    limitations: list[str] = Field(min_length=1)  # PRD §21.6: always at least one
    recommended_action: str

    # FR-008 / FR-010 additions, absent from the §18 example.
    representative_frame: str | None = None
    overlay: EvidenceOverlay
    providers: ProviderMetadata
    explanation_confidence: float | None = Field(default=None, ge=0, le=1)


class DependencyStatus(Strict):
    name: str
    ready: bool
    detail: str


class Health(Strict):
    """FR-019. `GET /health` must return 200 with version and dependency state.

    `git_revision` and `source_count` complete FR-019's six required fields;
    04-Architecture/06-Data-Model.md does not specify this shape, so there is
    nothing to drift from. Provider readiness is reported as a name and a
    boolean — never a key, a token, or a URL (NFR-010).
    """

    status: Literal["ok", "degraded"]
    version: str
    environment: str
    git_revision: str | None = None
    source_count: int = Field(ge=0)
    dependencies: list[DependencyStatus]


class NoConflictFound(Strict):
    """PRD §20. Returned when runtime analysis finds nothing over threshold.

    The system must say so rather than manufacture an event for presentation.
    """

    processing_mode: ProcessingMode
    message: str
    threshold: float
    pairs_evaluated: int
    highest_score: float | None = None


class AnalysisResponse(Strict):
    """The one envelope every analysis endpoint returns. FR-018.

    Mirrors orchestrator.PipelineResult exactly. Exactly one of `event` and
    `no_conflict` is populated — a clip with no qualifying conflict is a
    successful analysis, not an error (PRD §20).

    `notices` carries the FR-016 disclosure of which fallbacks actually fired.
    It is part of the contract, not debug output: the UI is required to show it.
    """

    event: Event | None = None
    no_conflict: NoConflictFound | None = None
    notices: list[str] = Field(default_factory=list)
