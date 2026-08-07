"""The pipeline, the fallback ladder, and the one place that decides which
processing mode is active. PRD §16.8, §17, FR-011, FR-012. ADR-004.

The ladder degrades per PRD §17:

    runtime inference      -> precomputed detections/tracks
    runtime public data    -> cached public-data context
    Gemini explanation     -> deterministic template explanation

A failure at any level must not corrupt the level below, which is why every
step-down is a caught ProviderUnavailable and never a partially-built Event.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from .config import Settings, settings as default_settings
from .models import (
    DependencyStatus,
    Detection,
    Event,
    EvidenceOverlay,
    HistoricalContext,
    Location,
    NoConflictFound,
    Participant,
    ProcessingMode,
    ProviderMetadata,
    Severity,
    TimeWindow,
    Track,
)
from .providers.base import ProviderUnavailable
from .providers.context import CachedContext, NycOpenDataContext
from .providers.explanation import (
    Explanation,
    GeminiExplanation,
    TemplateExplanation,
)
from .providers.tracking import ByteTrackTracker, FixtureTracker
from .providers.vision import FixtureVision, RoboflowVision
from .risk import Candidate, RiskEngine

# The demo clip's geometry. These become real values when Camera-Source
# resolves; until then they describe the synthetic scene in demo/fixtures/.
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS = 5.0

DEMO_LOCATION = Location(
    label="Demo intersection (synthetic fixture)",
    latitude=None,
    longitude=None,
)


@dataclass
class PipelineResult:
    event: Event | None
    no_conflict: NoConflictFound | None
    notices: list[str] = field(default_factory=list)


class Orchestrator:
    def __init__(self, settings: Settings | None = None):
        self.s = settings or default_settings
        fx = self.s.fixture_dir

        self.vision_runtime = RoboflowVision(
            os.getenv("ROBOFLOW_API_KEY"), os.getenv("ROBOFLOW_MODEL_ID")
        )
        self.vision_fixture = FixtureVision(fx)
        self.tracker_runtime = ByteTrackTracker()
        self.tracker_fixture = FixtureTracker(fx)
        self.context_runtime = NycOpenDataContext(
            os.getenv("NYC_OPEN_DATA_APP_TOKEN"), radius_meters=150
        )
        self.context_fixture = CachedContext(fx)
        self.explanation_runtime = GeminiExplanation(os.getenv("GEMINI_API_KEY"))
        self.explanation_fixture = TemplateExplanation()

    # -- readiness --------------------------------------------------------

    def readiness(self) -> list[DependencyStatus]:
        """FR-019 provider readiness.

        Reports, per stage, whether *anything* can serve it and which
        implementation will. Never a key, a token, or a URL (NFR-010) — only a
        name, a boolean, and prose.

        A stage is `ready` when either rung can serve. The fixture rung is what
        makes P0 guaranteed, so a missing fixture is what turns health
        `degraded` even with every runtime credential present.
        """

        def stage(name: str, runtime: str, configured: bool, fixture_ok: bool) -> DependencyStatus:
            return DependencyStatus(
                name=name,
                ready=configured or fixture_ok,
                detail=(
                    f"{runtime} {'configured' if configured else 'unconfigured'}; "
                    f"fixture {'present' if fixture_ok else 'MISSING'}"
                ),
            )

        return [
            stage(
                "vision",
                "roboflow",
                bool(self.vision_runtime.api_key and self.vision_runtime.model_id),
                self.vision_fixture.path.exists(),
            ),
            stage("tracking", "bytetrack", False, self.tracker_fixture.path.exists()),
            stage(
                "context",
                "nyc_open_data",
                bool(self.context_runtime.app_token),
                self.context_fixture.path.exists(),
            ),
            # The template needs no file and cannot be unavailable, which is the
            # whole point of it sitting at the bottom of the ladder.
            DependencyStatus(
                name="explanation",
                ready=True,
                detail=(
                    f"gemini {'configured' if self.explanation_runtime.api_key else 'unconfigured'}; "
                    "deterministic template always available"
                ),
            ),
        ]

    # -- ladder rungs -----------------------------------------------------

    def _detect(self, notices: list[str]) -> tuple[list[Detection], str, bool]:
        try:
            return self.vision_runtime.detect(), self.vision_runtime.name, True
        except ProviderUnavailable as exc:
            notices.append(f"Detection fell back to fixtures — {exc.reason}.")
            return self.vision_fixture.detect(), self.vision_fixture.name, False

    def _track(
        self, detections: list[Detection], notices: list[str]
    ) -> tuple[list[Track], str, bool]:
        try:
            return (
                self.tracker_runtime.track(detections),
                self.tracker_runtime.name,
                True,
            )
        except ProviderUnavailable as exc:
            notices.append(f"Tracking fell back to fixtures — {exc.reason}.")
            return (
                self.tracker_fixture.track(detections),
                self.tracker_fixture.name,
                False,
            )

    def _context(
        self, location: Location, notices: list[str]
    ) -> tuple[HistoricalContext | None, str]:
        try:
            return (
                self.context_runtime.lookup(location.latitude, location.longitude),
                self.context_runtime.name,
            )
        except ProviderUnavailable as exc:
            notices.append(f"Historical context is cached — {exc.reason}.")
            try:
                return self.context_fixture.lookup(
                    location.latitude, location.longitude
                ), self.context_fixture.name
            except FileNotFoundError:
                # Context is genuinely optional (FR-009 "when available"); the
                # event is still valid without it.
                notices.append("No historical context available.")
                return None, "none"

    def _explain(
        self,
        candidate: Candidate,
        context: HistoricalContext | None,
        severity: Severity,
        notices: list[str],
    ) -> tuple[Explanation, str]:
        try:
            return (
                self.explanation_runtime.explain(candidate, context, severity),
                self.explanation_runtime.name,
            )
        except ProviderUnavailable as exc:
            notices.append(f"Explanation is a deterministic template — {exc.reason}.")
            return (
                self.explanation_fixture.explain(candidate, context, severity),
                self.explanation_fixture.name,
            )

    # -- assembly ---------------------------------------------------------

    def _severity(self, score: float) -> Severity:
        return "high" if score >= self.s.high_severity_at else "medium"

    def _event_type(self, candidate: Candidate):
        classes = {candidate.a.class_name, candidate.b.class_name}
        if "person" in classes:
            return "vehicle_pedestrian_conflict"
        return "vehicle_cyclist_conflict"

    def run(self, event_id: str = "nmyc_demo_001") -> PipelineResult:
        notices: list[str] = []

        detections, vision_name, vision_live = self._detect(notices)
        tracks, tracker_name, tracker_live = self._track(detections, notices)

        engine = RiskEngine(self.s, FRAME_WIDTH, FRAME_HEIGHT)
        candidates = engine.evaluate(tracks)
        over = [c for c in candidates if c.score >= self.s.alert_threshold]

        # FR-016. Runtime mode requires the runtime providers to have actually
        # served — a fixture-fed pipeline is a replay however it is invoked.
        #
        # The fixture rung is `demonstration_fixture`, NOT `captured_feed_replay`.
        # Both detections and tracks come from committed JSON, so vision is
        # bypassed entirely and no feed was ever captured — sources.py describes
        # the sequence as "Not camera footage and not attributed to any NYC
        # source." §23 item 11 requires fixture assets labelled accurately, and
        # calling this a captured feed would put a false provenance claim on the
        # §2.2 eligibility gate. `captured_feed_replay` becomes correct when a
        # real recorded sequence replaces the synthetic one (W-14).
        mode: ProcessingMode = (
            "runtime_sequence_analysis"
            if (vision_live and tracker_live)
            else "demonstration_fixture"
        )

        if not over:
            # PRD §20. Say so; do not manufacture an event for presentation.
            return PipelineResult(
                event=None,
                no_conflict=NoConflictFound(
                    processing_mode=mode,
                    message=(
                        "No candidate conflict crossed the configured "
                        "visual-risk threshold in this clip."
                    ),
                    threshold=self.s.alert_threshold,
                    pairs_evaluated=len(candidates),
                    highest_score=candidates[0].score if candidates else None,
                ),
                notices=notices,
            )

        best = over[0]
        severity = self._severity(best.score)
        context, context_name = self._context(DEMO_LOCATION, notices)
        explanation, explanation_name = self._explain(best, context, severity, notices)

        event = Event(
            event_id=event_id,
            event_type=self._event_type(best),
            severity=severity,
            risk_score=best.score,
            risk_factors=best.factors,
            participants=[
                Participant(track_id=best.a.track_id, class_name=best.a.class_name),
                Participant(track_id=best.b.track_id, class_name=best.b.class_name),
            ],
            time_window=TimeWindow(
                start_seconds=best.start_seconds, end_seconds=best.end_seconds
            ),
            location=DEMO_LOCATION,
            processing_mode=mode,
            observations=explanation.observations,
            historical_context=context,
            limitations=explanation.limitations,
            recommended_action=explanation.recommended_action,
            representative_frame=None,
            overlay=EvidenceOverlay(
                clip_path=None,
                frame_width=FRAME_WIDTH,
                frame_height=FRAME_HEIGHT,
                fps=FPS,
                detections=detections,
                tracks=tracks,
            ),
            providers=ProviderMetadata(
                vision=vision_name,
                tracker=tracker_name,
                context=context_name,
                explanation=explanation_name,
            ),
            explanation_confidence=explanation.confidence,
        )
        return PipelineResult(event=event, no_conflict=None, notices=notices)
