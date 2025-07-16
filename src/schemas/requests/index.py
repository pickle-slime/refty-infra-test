from pydantic import BaseModel, Field

class UpdateImageRequest(BaseModel):
    image: str = Field(..., example="ghcr.io/refty-yapi/refty-node/refty-node",)
    version: str = Field(..., example="05-06-42a252")
