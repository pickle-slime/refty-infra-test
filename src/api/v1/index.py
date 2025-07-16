from schemas.requests.index import UpdateImageRequest
from schemas.responses.index import UpdateImageResponse
from services.index import update_image_service

from fastapi import APIRouter

router = APIRouter()

@router.post(path="/update_image", response_model=UpdateImageResponse, tags=["Core Logic"], summary="Handles updating images")
async def update_image(request: UpdateImageRequest):
    status, msg, updated_ymls = await update_image_service(request)
    return UpdateImageResponse(
            status=status, 
            message=msg, 
            updated_ymls=updated_ymls
        )
