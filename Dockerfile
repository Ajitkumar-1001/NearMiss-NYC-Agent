# NFR-001 Cloud Run container contract: binds 0.0.0.0, reads $PORT (default
# 8080), stateless, no reliance on local persistent storage.
#
# Build context is the REPO ROOT, not app/backend — demo/fixtures/ is a sibling
# of app/ and ADR-010 makes those files load-bearing runtime data rather than
# test data. An image without them starts cleanly and then fails on the first
# analysis request.
FROM python:3.12-slim

WORKDIR /app

COPY app/backend/ /app/app/backend/
COPY demo/fixtures/ /app/demo/fixtures/

RUN pip install --no-cache-dir /app/app/backend

# Load-bearing. config.py resolves FIXTURE_DIR from Path(__file__).parents[3],
# which is only correct while the package sits at app/backend/nearmiss/. pip
# installs it into site-packages, where that walk lands somewhere else entirely
# — so the fixture directory is pinned explicitly here instead of inferred.
ENV NEARMISS_FIXTURE_DIR=/app/demo/fixtures

# Overridden by Cloud Run at runtime; 8080 is the local default (NFR-001).
ENV PORT=8080

# GIT_REVISION is supplied at deploy time via --set-env-vars so FR-019's
# /health can identify the running revision (§2.2). A --build-arg cannot
# survive a `gcloud run deploy --source` build.

CMD exec uvicorn nearmiss.main:app --host 0.0.0.0 --port $PORT
