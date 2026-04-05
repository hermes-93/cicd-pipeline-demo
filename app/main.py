"""
FastAPI application entry point.

Wires up routers, middleware, and startup/shutdown lifecycle hooks.
Designed to be imported by uvicorn and by the test suite alike.
"""

import logging
import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import health, items

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="CI/CD Pipeline Demo",
        description=(
            "A production-ready FastAPI service that demonstrates a complete "
            "CI/CD pipeline with GitHub Actions, Docker multi-stage builds, "
            "automated testing, and container registry publishing."
        ),
        version=settings.service_version,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
    )

    # Allow all origins in dev; tighten this in production via env var
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next) -> Response:
        """Log every request with method, path, status code, and latency."""
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info(
            "%s %s → %d  (%.2fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response

    app.include_router(health.router)
    app.include_router(items.router)

    @app.get("/", include_in_schema=False)
    def root() -> dict:
        return {
            "service": settings.service_name,
            "version": settings.service_version,
            "docs": "/docs",
        }

    return app


app = create_app()
