from schemas.responses.health import HealthResponse
from schemas.health_checks import HealthChecks
from core.config import settings

from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()

@router.get(path="/health_check", response_model=HealthResponse, tags=["Health"], summary="Health check endpoint")
def health_check():
    current_time = datetime.now()
    up_time = int((current_time - settings.START_TIME).total_seconds())

    checks = HealthChecks(
            github="ok",
            database="ok",
        )

    status = "healthy" if all([check == "ok" for check in checks]) else "unhealthy"

    return HealthResponse(
            status=status,
            timestamp=datetime.now(tz=timezone.utc),
            uptime=up_time,
            version="1.0.0",
            environment="production",
            checks=checks
        )
