from pydantic import BaseModel, Field

from typing import Literal
from datetime import datetime

from schemas.health_checks import HealthChecks

class HealthResponse(BaseModel):
    status: Literal["healthy", "unhealthy"] = Field(..., example="healthy")
    timestamp: datetime = Field(..., example="2025-07-15T06:25:05.577Z")
    uptime: int = Field(..., example=3600)
    version: str = Field(..., example="1.0.0")
    environment: str = Field(..., example="production")
    checks: HealthChecks
