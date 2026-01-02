from fastapi import APIRouter
from app.api.v1.endpoints import health, metadata, predict

api_router = APIRouter()
api_router.include_router(health.router, tags=["system"])
api_router.include_router(metadata.router, tags=["system"])
api_router.include_router(predict.router, tags=["inference"])
