# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-04-06

### Added
- **FastAPI application** with `/health`, `/health/live`, and `/items` CRUD endpoints
- **Multi-stage Docker build** — separate `builder` and `runtime` stages for minimal image size
- **docker-compose** stack for local development
- **pytest suite** — 26 tests covering health checks and full CRUD lifecycle (matrix: Python 3.11 & 3.12)
- **GitHub Actions CI pipeline**:
  - `lint` — ruff check + format validation
  - `test` — matrix test across Python 3.11 and 3.12 (needs lint)
  - `build` — multi-stage Docker build and push to GHCR (needs test, main only)
  - `release` — GitHub Release creation on `v*.*.*` tags
- **GitHub Actions Security workflow**:
  - Bandit — Python SAST scanning
  - pip-audit — dependency vulnerability audit
  - Trivy — container image CVE scan (HIGH/CRITICAL), results uploaded to GitHub Security tab as SARIF
- **Dependabot** — weekly auto-updates for pip, GitHub Actions, and Docker base images
- **CODEOWNERS** — mandatory review on all changes
- **Comprehensive README** with architecture diagram, pipeline stages table, API reference, and usage examples

[1.0.0]: https://github.com/hermes-93/cicd-pipeline-demo/releases/tag/v1.0.0
