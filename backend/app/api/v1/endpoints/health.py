from fastapi import APIRouter

router = APIRouter()

@router.get("/healthz", status_code=200)
def health_check() -> dict[str, str]:
    """
    Health check endpoint for k8s/docker probes.
    """
    return {"status": "ok"}
