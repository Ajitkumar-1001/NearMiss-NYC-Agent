"""Public-data enrichment. FR-009, FR-011 (NYC Open Data -> cached context)."""

from __future__ import annotations

from pathlib import Path

from ..models import HistoricalContext
from .base import ProviderUnavailable, load_fixture


class NycOpenDataContext:
    """Runtime lookup against NYC Open Data.

    Unimplemented at P0. Which fields are stable enough to depend on is still
    open — see 00-Inbox/NYC-Open-Data-Fields.md. Guessing a schema here would
    produce a fixture that cannot be swapped for a real response later, which
    is precisely the drift ADR-010 exists to prevent.
    """

    name = "nyc_open_data"

    def __init__(self, app_token: str | None, radius_meters: int):
        self.app_token = app_token
        self.radius_meters = radius_meters

    def lookup(
        self, latitude: float | None, longitude: float | None
    ) -> HistoricalContext:
        if latitude is None or longitude is None:
            raise ProviderUnavailable(
                self.name, "event has no coordinates to query on"
            )
        raise ProviderUnavailable(
            self.name, "runtime public-data lookup not implemented at P0"
        )


class CachedContext:
    """Cached collision context. The P0 path.

    `source` in the payload says `cached_nyc_open_data` so the UI can label it
    as cached — PRD §21.10 requires fixtures to be labelled as fixtures.
    """

    name = "cached"

    def __init__(self, fixture_dir: Path):
        self.path = fixture_dir / "context.json"

    def lookup(
        self, latitude: float | None, longitude: float | None
    ) -> HistoricalContext:
        return HistoricalContext.model_validate(load_fixture(self.path))
