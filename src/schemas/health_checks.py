from pydantic import BaseModel, Field

class HealthChecks(BaseModel):
    github: str = Field(..., example="ok")
    database: str | None = Field(default=None, example="ok")
