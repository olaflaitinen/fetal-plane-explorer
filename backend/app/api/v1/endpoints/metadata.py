from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/metadata", status_code=200)
def get_metadata() -> dict[str, str]:
    """
    Returns metadata about the service and currently loaded model.
    """
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "model_mode": "synthetic" if settings.USE_SYNTHETIC_MODE else "onnx",
        "description": "Fetal Plane Classification Demo (Research Only)"
    }
