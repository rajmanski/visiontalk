# Build context must be the project root so that the shared `model` and
# `data` packages are available, e.g.:
#   docker build -f app/backend/Dockerfile -t visiontalk-backend .
FROM ghcr.io/astral-sh/uv:0.7.13 AS uv
FROM python:3.9-slim

WORKDIR /app

COPY --from=uv /uv /uvx /bin/

# Install dependencies first to leverage Docker layer caching.
# We reuse the project-wide requirements.txt (single source of truth).
COPY requirements.txt ./requirements.txt
RUN uv pip install --system --no-cache -r requirements.txt

# Copy the code the backend depends on.
COPY model/ ./model/
COPY data/ ./data/
COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
