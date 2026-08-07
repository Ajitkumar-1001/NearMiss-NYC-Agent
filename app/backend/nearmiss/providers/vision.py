"""Detection. FR-002, FR-011 (Roboflow -> fixture detections)."""

from __future__ import annotations

from pathlib import Path

from ..models import Detection
from .base import ProviderUnavailable, load_fixture


class RoboflowVision:
    """Runtime detection via Roboflow.

    Not implemented at P0 and deliberately so: there is no API key and no clip
    to run it against (see 00-Inbox/Roboflow-Model.md and Camera-Source.md).
    It declines cleanly so the ladder steps down, rather than pretending.
    """

    name = "roboflow"

    def __init__(self, api_key: str | None, model_id: str | None):
        self.api_key = api_key
        self.model_id = model_id

    def detect(self) -> list[Detection]:
        if not self.api_key or not self.model_id:
            raise ProviderUnavailable(
                self.name, "no API key or model configured"
            )
        # The model choice is still an open question; implementing against a
        # guess would be the wrong kind of progress.
        raise ProviderUnavailable(
            self.name, "runtime detection not implemented at P0"
        )


class FixtureVision:
    """Precomputed detections. The P0 path."""

    name = "fixture"

    def __init__(self, fixture_dir: Path):
        self.path = fixture_dir / "detections.json"

    def detect(self) -> list[Detection]:
        raw = load_fixture(self.path)
        return [Detection.model_validate(d) for d in raw]  # type: ignore[union-attr]
