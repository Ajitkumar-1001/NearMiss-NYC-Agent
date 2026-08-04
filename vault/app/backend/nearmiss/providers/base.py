"""Protocols shared by every adapter, and the one exception that drives the
fallback ladder."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol, runtime_checkable

from ..models import Detection, HistoricalContext, Track


class ProviderUnavailable(Exception):
    """A provider could not serve this request.

    Raising this is the *normal* way a runtime provider declines. The
    orchestrator catches it and steps down PRD §17's ladder. It carries a
    user-readable reason and never a stack trace or a secret (NFR-005).
    """

    def __init__(self, provider: str, reason: str):
        self.provider = provider
        self.reason = reason
        super().__init__(f"{provider}: {reason}")


@runtime_checkable
class VisionProvider(Protocol):
    name: str

    def detect(self) -> list[Detection]: ...


@runtime_checkable
class TrackerProvider(Protocol):
    name: str

    def track(self, detections: list[Detection]) -> list[Track]: ...


@runtime_checkable
class ContextProvider(Protocol):
    name: str

    def lookup(self, latitude: float | None, longitude: float | None) -> HistoricalContext: ...


def load_fixture(path: Path) -> object:
    """Read a committed fixture.

    A missing or malformed fixture is not a ProviderUnavailable — it is a
    broken P0, because ADR-010 makes these files load-bearing rather than test
    data. It fails loudly instead of degrading quietly.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Fixture missing: {path}. ADR-010 makes demo/fixtures/ the "
            f"guaranteed path; P0 cannot run without it."
        )
    with path.open() as fh:
        return json.load(fh)
