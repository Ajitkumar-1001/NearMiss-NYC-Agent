"""The conflict-risk engine. FR-005, FR-006, FR-007.

This is the only place a risk number is produced. It takes tracks and returns
candidate events. It does not call a language model — PRD §16.5 requires the
risk engine to avoid language-model dependence, because a nondeterministic
component must not sit on the guaranteed path (ADR-004).

Everything here is image-space. Nothing here may be presented as real-world
metric distance (FR-004, ADR-002).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .config import Settings
from .models import Point, RiskFactors, Track


@dataclass(frozen=True)
class Candidate:
    """A scored pair, before it becomes an Event."""

    a: Track
    b: Track
    score: float
    factors: RiskFactors
    start_seconds: float
    end_seconds: float
    closest_at: float
    min_separation_px: float


def _distance(p: Point, q: Point) -> float:
    return math.hypot(p.x - q.x, p.y - q.y)


def _paired_by_time(a: Track, b: Track) -> list[tuple[float, float]]:
    """(timestamp, separation) for frames where both tracks have a sample.

    Matching on frame_number rather than timestamp avoids float-equality
    problems when the sampler emits fractional timestamps.
    """
    by_frame = {p.frame_number: p for p in b.centroid_history}
    return [
        (p.timestamp, _distance(p, by_frame[p.frame_number]))
        for p in a.centroid_history
        if p.frame_number in by_frame
    ]


def _min_path_separation(a: Track, b: Track) -> float:
    """Closest approach of the two paths ignoring time.

    This is what distinguishes path_overlap from proximity: two road users can
    trace crossing paths minutes apart. That is geometric overlap without a
    conflict, and the time-aware factors are what tell them apart.
    """
    return min(
        _distance(p, q) for p in a.centroid_history for q in b.centroid_history
    )


def _closing_motion(
    paired: list[tuple[float, float]], closest_at: float, window: float
) -> float:
    """How much separation collapsed in the `window` seconds before closest
    approach, as a fraction of where it started.

    Parallel movement holds separation constant and scores ~0. Measuring over
    the whole track instead would make anything approaching from off-frame look
    severe, which is why the window exists.
    """
    before = [(t, d) for t, d in paired if closest_at - window <= t <= closest_at]
    if len(before) < 2:
        return 0.0
    d_start = before[0][1]
    d_end = min(d for _, d in before)
    if d_start <= 0:
        return 0.0
    return max(0.0, min(1.0, (d_start - d_end) / d_start))


class RiskEngine:
    def __init__(self, settings: Settings, frame_width: int, frame_height: int):
        self.s = settings
        self.diagonal = math.hypot(frame_width, frame_height)

    # -- FR-005 -----------------------------------------------------------
    def _is_supported_pair(self, a: Track, b: Track) -> bool:
        """Only vehicle-to-vulnerable-road-user pairs are evaluated."""
        va, vb = a.class_name in self.s.vulnerable_classes, b.class_name in self.s.vulnerable_classes
        ha, hb = a.class_name in self.s.vehicle_classes, b.class_name in self.s.vehicle_classes
        return (va and hb) or (vb and ha)

    def _has_enough_evidence(self, a: Track, b: Track) -> bool:
        """PRD §22.2 cases 5 and 6: detection jitter and unstable tracks must
        not produce events."""
        if len(a.centroid_history) < self.s.min_track_points:
            return False
        if len(b.centroid_history) < self.s.min_track_points:
            return False
        paired = _paired_by_time(a, b)
        if len(paired) < 2:
            return False
        span = paired[-1][0] - paired[0][0]
        return span >= self.s.min_overlap_seconds

    def _normalise(self, separation_px: float, scale: float) -> float:
        """Separation -> 0..1 closeness, against a fraction of the diagonal."""
        limit = self.diagonal * scale
        return max(0.0, min(1.0, 1.0 - separation_px / limit))

    def score_pair(self, a: Track, b: Track) -> Candidate | None:
        if not self._is_supported_pair(a, b):
            return None
        if not self._has_enough_evidence(a, b):
            return None

        paired = _paired_by_time(a, b)
        closest_at, min_sep = min(paired, key=lambda td: td[1])

        factors = RiskFactors(
            proximity=self._normalise(min_sep, self.s.proximity_scale),
            path_overlap=self._normalise(
                _min_path_separation(a, b), self.s.path_scale
            ),
            closing_motion=_closing_motion(
                paired, closest_at, self.s.closing_window_seconds
            ),
            # FR-006. Constant 1.0 for every evaluated pair, because FR-005
            # already restricts evaluation to VRU pairs. It is a deliberate
            # floor on the score of any VRU conflict, not a discriminator.
            vulnerable_user=1.0,
        )

        w = self.s.weights
        score = 100.0 * (
            w.proximity * factors.proximity
            + w.path_overlap * factors.path_overlap
            + w.closing_motion * factors.closing_motion
            + w.vulnerable_user * factors.vulnerable_user
        )

        return Candidate(
            a=a,
            b=b,
            score=round(score, 1),
            factors=factors,
            start_seconds=paired[0][0],
            end_seconds=paired[-1][0],
            closest_at=closest_at,
            min_separation_px=min_sep,
        )

    def evaluate(self, tracks: list[Track]) -> list[Candidate]:
        """Every supported pair, scored, highest first. Filtering by threshold
        is the caller's job — the orchestrator needs the near-misses that did
        not clear it in order to report `highest_score` when nothing fires."""
        out: list[Candidate] = []
        for i, a in enumerate(tracks):
            for b in tracks[i + 1 :]:
                candidate = self.score_pair(a, b)
                if candidate is not None:
                    out.append(candidate)
        return sorted(out, key=lambda c: c.score, reverse=True)
