# cicd-pipeline-demo

[![CI](https://github.com/hermes-93/cicd-pipeline-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/hermes-93/cicd-pipeline-demo/actions/workflows/ci.yml)
[![Docker](https://ghcr.io/hermes-93/cicd-pipeline-demo)](https://github.com/hermes-93/cicd-pipeline-demo/pkgs/container/cicd-pipeline-demo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-ready FastAPI service that demonstrates a complete CI/CD pipeline:
automated linting, matrix testing, multi-stage Docker builds, and container
publishing to GitHub Container Registry — all on every push.

> Part of the [DevOps portfolio](https://github.com/hermes-93) series.

---

## Architecture

```
Developer
   │ git push
   ▼
GitHub Actions ──► lint (ruff)
                       │ pass
                       ▼
                   test (Python 3.11 & 3.12)
                       │ pass
                       ▼
                   build & push → ghcr.io/hermes-93/cicd-pipeline-demo:sha-xxxxx
                                                                        :latest
```

### Pipeline stages

| Stage | Tool | Triggers |
|-------|------|----------|
| Lint | ruff check + format | push / PR to main |
| Test | pytest (matrix 3.11/3.12) | after lint |
| Build & Push | Docker Buildx → GHCR | push to main only |
| Release | semver tags → GitHub Release | `v*.*.*` tags |

---

## Project structure

```
cicd-pipeline-demo/
├── app/
│   ├── main.py          # FastAPI app factory, middleware
│   ├── config.py        # Settings from environment variables
│   └── routers/
│       ├── health.py    # /health (readiness) + /health/live (liveness)
│       └── items.py     # Full CRUD: GET/POST/PATCH/DELETE /items
├── tests/
│   ├── conftest.py      # TestClient fixture, DB isolation
│   ├── test_health.py   # Health endpoint tests
│   └── test_items.py    # CRUD + validation tests (26 total)
├── .github/
│   ├── workflows/
│   │   ├── ci.yml       # Lint → Test → Build pipeline
│   │   └── release.yml  # Semver release + GHCR publish
│   └── pull_request_template.md
├── Dockerfile           # Multi-stage: builder + runtime (non-root)
├── docker-compose.yml   # Local development
├── requirements.txt
└── requirements-dev.txt
```

---

## Quick start

### Run locally with Docker

```bash
# Build and start
docker compose up --build

# Verify
curl http://localhost:8000/health
curl http://localhost:8000/items/
```

### Run locally without Docker

```bash
# Create virtual environment
python3 -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Start the server
uvicorn app.main:app --reload

# Run tests
pytest tests/ -v
```

### Pull from GHCR

```bash
docker pull ghcr.io/hermes-93/cicd-pipeline-demo:latest
docker run -p 8000:8000 ghcr.io/hermes-93/cicd-pipeline-demo:latest
```

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Service info |
| GET | `/health` | Readiness probe (full status) |
| GET | `/health/live` | Liveness probe (fast) |
| GET | `/docs` | Swagger UI (non-production only) |
| GET | `/items/` | List all items |
| POST | `/items/` | Create an item |
| GET | `/items/{id}` | Get item by ID |
| PATCH | `/items/{id}` | Partially update an item |
| DELETE | `/items/{id}` | Delete an item |

---

## Configuration

All settings are environment variables. Copy `.env.example` to `.env` for local dev:

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | `development` or `production` |
| `APP_PORT` | `8000` | Server port |
| `LOG_LEVEL` | `INFO` | Logging level |
| `SERVICE_NAME` | `cicd-pipeline-demo` | Reported in /health |
| `SERVICE_VERSION` | `0.1.0` | Reported in /health |

> In `production` mode the `/docs` and `/redoc` endpoints are disabled.

---

## CI/CD details

### Layer caching strategy

The workflow uses **registry-based cache** (`type=registry`) so Docker layer
cache persists across GitHub Actions runners — significantly faster rebuilds
when only application code changes (the heavy `pip install` layer is reused).

### Image tagging

- **On push to main:** `sha-<short>` + `latest`
- **On semver tag** (`v1.2.3`): `1.2.3`, `1.2`, `1`

### Security

- Docker image runs as non-root user `app`
- `GITHUB_TOKEN` is scoped to `packages: write` only in the build job
- Secrets are never printed in logs

---

## Running the linter

```bash
# Check code style
ruff check .

# Auto-fix where possible
ruff check --fix .

# Check formatting
ruff format --check .
```
