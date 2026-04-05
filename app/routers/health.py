"""Health check endpoints used by load balancers and Kubernetes probes."""

import time
from fastapi import APIRouter
from pydantic import BaseModel

from app.config import settings

router = APIRouter(tags=["health"])

# Record startup time to calculate uptime
_START_TIME = time.time()


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    uptime_seconds: float
    environment: str


class LivenessResponse(BaseModel):
    status: str


@router.get("/health", response_model=HealthResponse, summary="Full health check")
def health_check() -> HealthResponse:
    """
    Readiness probe — used by Kubernetes and load balancers.
    Returns 200 only when the service is fully ready to serve traffic.
    """
    return HealthResponse(
        status="healthy",
        service=settings.service_name,
        version=settings.service_version,
        uptime_seconds=round(time.time() - _START_TIME, 2),
        environment=settings.app_env,
    )


@router.get("/health/live", response_model=LivenessResponse, summary="Liveness probe")
def liveness_check() -> LivenessResponse:
    """
    Liveness probe — a fast check to confirm the process is alive.
    Kubernetes restarts the pod if this returns non-2xx.
    """
    return LivenessResponse(status="alive")
