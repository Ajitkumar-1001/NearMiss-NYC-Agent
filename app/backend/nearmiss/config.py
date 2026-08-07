"""Settings and the risk-engine calibration knobs.

FR-007 requires the alert threshold to be configurable through environment or
application settings. The factor weights are FR-006's reference weighting and
may be tuned against the selected demo clip — but every change must be recorded
in 08-Execution/05-Decision-Log.md.

The normalisation scales below are the knobs that actually need tuning once a
real clip exists. A near-miss at 1280x720 from a pole-mounted camera is a
different number of pixels than the same near-miss from a bridge. They are
fractions of the frame diagonal so they at least survive a resolution change.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Repo root: app/backend/nearmiss/config.py -> up 3 -> repo root
REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_DIR = REPO_ROOT / "demo" / "fixtures"


class RiskWeights(BaseModel):
    """FR-006 reference weighting. Must sum to 1.0."""

    proximity: float = 0.35
    path_overlap: float = 0.35
    closing_motion: float = 0.20
    vulnerable_user: float = 0.10

    def total(self) -> float:
        return (
            self.proximity
            + self.path_overlap
            + self.closing_motion
            + self.vulnerable_user
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NEARMISS_", extra="ignore")

    environment: str = "local"

    # FR-007. Candidate-event threshold, 0-100.
    alert_threshold: float = Field(default=70.0, ge=0, le=100)

    # Severity mapping. PRD §18's worked example scores 84.0 and is "high", so
    # the high cut sits below that. `low` is defined by PRD §12 but the engine
    # does not currently emit it: sub-threshold pairs produce no event at all.
    high_severity_at: float = Field(default=80.0, ge=0, le=100)

    weights: RiskWeights = RiskWeights()

    # --- calibration knobs -------------------------------------------------
    # Separation at which proximity decays to 0, as a fraction of the frame
    # diagonal. Smaller = stricter about what counts as "close".
    proximity_scale: float = Field(default=0.25, gt=0, le=1)
    # Same, for the distance between the two paths ignoring time.
    path_scale: float = Field(default=0.25, gt=0, le=1)
    # How far back from the closest approach to measure closure. Measuring over
    # the whole track makes anything approaching from off-frame look severe.
    closing_window_seconds: float = Field(default=2.0, gt=0)

    # --- evidence-quality guards (FR-006 "optional evidence-quality
    # adjustment"; PRD §22.2 cases 5 and 6) ---------------------------------
    # A pair is not evaluated at all unless both tracks clear these. This is
    # what stops detection jitter and dropped tracks from producing events.
    min_track_points: int = Field(default=8, ge=2)
    min_overlap_seconds: float = Field(default=1.0, gt=0)

    # FR-005. Which classes count as vulnerable road users.
    # Motorcyclists are vulnerable road users in most transport-safety
    # taxonomies, but the PRD does not say so; treated as a vehicle here, which
    # is the conservative reading. Revisit with a decision-log entry, not a
    # silent edit.
    vulnerable_classes: frozenset[str] = frozenset({"person", "bicycle"})
    vehicle_classes: frozenset[str] = frozenset({"car", "bus", "truck", "motorcycle"})

    fixture_dir: Path = FIXTURE_DIR


settings = Settings()
