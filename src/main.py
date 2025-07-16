from fastapi import FastAPI
from core.config import settings
from api.v1.health import router as health_router
from api.v1.index import router as index_router

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(health_router, prefix=settings.API_V1_PREFIX)
app.include_router(index_router, prefix=settings.API_V1_PREFIX)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
