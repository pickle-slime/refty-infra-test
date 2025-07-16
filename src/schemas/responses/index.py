from pydantic import BaseModel, Field

class UpdateImageResponse(BaseModel):
    status: int = Field(..., example=200)
    message: str | None = Field(default=None, example="some error")
    updated_ymls: list[str] | None = Field(default=None, description="list of updated yaml files")
