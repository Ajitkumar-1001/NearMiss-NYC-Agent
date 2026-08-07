"""The source registry. FR-001, FR-003.

Deliberately a list of data, not a class hierarchy. PRD §11.2 step 2 makes
"swap or configure the selected organizer/NYC source" an event-day task, and
the cheapest thing to swap is a literal.

Nothing here may carry a credential or a secret-bearing URL — `/api/v1/sources`
serves these objects verbatim to an unauthenticated caller (FR-001, NFR-010).
"""

from __future__ import annotations

from typing import Literal

from .models import Strict

SourceKind = Literal["fixture", "still_image", "video_clip"]


class Source(Strict):
    """One approved input. `url` is a public, human-visitable page — never the
    credentialed endpoint the adapter actually fetches."""

    source_id: str
    label: str
    kind: SourceKind
    attribution: str
    url: str | None = None
    enabled: bool = True


# The P0 registry. The captured-evidence source is the guaranteed path (ADR-001)
# and is the only entry that can serve without network access.
SOURCES: list[Source] = [
    Source(
        source_id="demo_fixture",
        label="Captured evidence case (synthetic)",
        kind="fixture",
        attribution=(
            "Synthetic sequence generated for the deterministic demo path. "
            "Not camera footage and not attributed to any NYC source."
        ),
        url=None,
        enabled=True,
    ),
]


def by_id(source_id: str) -> Source | None:
    return next((s for s in SOURCES if s.source_id == source_id), None)


def enabled_count() -> int:
    """FR-019's "configured source count"."""
    return sum(1 for s in SOURCES if s.enabled)
