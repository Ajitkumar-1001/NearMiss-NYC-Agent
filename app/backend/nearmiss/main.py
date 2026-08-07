"""The HTTP surface. FR-018, FR-019, NFR-001, NFR-002, NFR-008.

Thin on purpose. Every endpoint translates `Orchestrator` output into JSON — no
risk logic, no provider knowledge, no branching on which rung served. The
pipeline already decided that and said so in `processing_mode` and `notices`.

NFR-001: binds 0.0.0.0, reads $PORT (default 8080), holds no request state, and
writes nothing to local disk.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from . import __version__, sources
from .config import settings
from .models import AnalysisResponse, Health
from .orchestrator import Orchestrator, PipelineResult

logging.basicConfig(
    level=logging.INFO, format='{"level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}'
)
log = logging.getLogger("nearmiss")

app = FastAPI(
    title="NearMiss NYC",
    version=__version__,
    description=(
        "Explainable street-conflict decision support. The risk score is an "
        "image-space visual conflict proxy, not a crash probability."
    ),
)

# ADR-005: no authentication and no user data, so there is no origin to protect.
# The dashboard is a separate service and therefore a separate origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Built once. Holds provider configuration, not request state.
_orchestrator = Orchestrator(settings)


def _envelope(result: PipelineResult) -> AnalysisResponse:
    return AnalysisResponse(
        event=result.event, no_conflict=result.no_conflict, notices=result.notices
    )


@app.exception_handler(Exception)
async def _unhandled(request: Request, exc: Exception) -> JSONResponse:
    """NFR-008: a failure produces a structured log and a user-readable notice —
    never a stack trace and never a secret over the wire."""
    log.exception("unhandled error on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "The service failed to complete this request."},
    )


_INDEX = Path(__file__).parent / "static" / "index.html"


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    """PRD §11.3's six judge-facing surfaces, in one static page.

    Served from this service rather than a separate frontend deployment: §16.1
    leaves the dashboard's location open and §2.2 puts only this service on the
    eligibility gate. One origin means one deploy to verify before the freeze.
    """
    return FileResponse(_INDEX)


@app.get("/health", response_model=Health)
def health() -> Health:
    """FR-019. Always HTTP 200 — a degraded pipeline is reported in the body, not
    as a failure status, so Cloud Run's health checking stays meaningful."""
    dependencies = _orchestrator.readiness()
    return Health(
        status="ok" if all(d.ready for d in dependencies) else "degraded",
        version=__version__,
        environment=settings.environment,
        git_revision=os.getenv("GIT_REVISION"),
        source_count=sources.enabled_count(),
        dependencies=dependencies,
    )


@app.get("/api/v1/sources", response_model=list[sources.Source])
def list_sources() -> list[sources.Source]:
    """FR-001. `Source` carries no credential by construction, so the registry
    serves verbatim (NFR-010)."""
    return sources.SOURCES


@app.get("/api/v1/demo", response_model=AnalysisResponse)
def demo() -> AnalysisResponse:
    """The deterministic captured-evidence case — ADR-001's guaranteed path.
    Runs without any runtime external API and returns the same result each time."""
    return _envelope(_orchestrator.run())


@app.post("/api/v1/live/{source_id}/analyze", response_model=AnalysisResponse)
def analyze_live(source_id: str) -> AnalysisResponse:
    """FR-002. Analyses the named source.

    At P0 every runtime provider declines and the ladder degrades to the
    committed fixtures. The response discloses that through `processing_mode`
    and `notices` rather than pretending otherwise (FR-016). Wiring a real feed
    is a change to `providers/`, not to this function.
    """
    source = sources.by_id(source_id)
    if source is None:
        raise HTTPException(status_code=404, detail=f"Unknown source: {source_id}")
    if not source.enabled:
        raise HTTPException(status_code=409, detail=f"Source is disabled: {source_id}")
    return _envelope(_orchestrator.run(event_id=f"nmyc_{source_id}"))
