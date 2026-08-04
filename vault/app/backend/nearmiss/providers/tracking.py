"""Multi-object tracking. FR-003, FR-011 (tracker runtime -> precomputed tracks)."""

from __future__ import annotations

from pathlib import Path

from ..models import Detection, Track
from .base import ProviderUnavailable, load_fixture


class ByteTrackTracker:
    """Runtime tracking (Supervision/ByteTrack or equivalent).

    Unimplemented at P0 for the same reason as RoboflowVision: without runtime
    detections there is nothing to associate across frames.
    """

    name = "bytetrack"

    def track(self, detections: list[Detection]) -> list[Track]:
        raise ProviderUnavailable(
            self.name, "runtime tracking not implemented at P0"
        )


class FixtureTracker:
    """Precomputed tracks. The P0 path.

    Ignores the detections it is handed — the fixture tracks were derived from
    the fixture detections when they were generated, so re-deriving them would
    only add a way for the two to disagree.
    """

    name = "fixture"

    def __init__(self, fixture_dir: Path):
        self.path = fixture_dir / "tracks.json"

    def track(self, detections: list[Detection]) -> list[Track]:
        raw = load_fixture(self.path)
        return [Track.model_validate(t) for t in raw]  # type: ignore[union-attr]
