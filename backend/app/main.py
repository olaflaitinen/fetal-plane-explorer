from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import uuid
import logging
import os

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model on startup
    if not os.path.exists(settings.MODEL_PATH):
        logger.warning(f"Model not found at {settings.MODEL_PATH}. Inference will fail until model is present.")
    yield
    logger.info("Shutting down")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request ID Middleware
@app.middleware("http")
async def request_id_middleware(request: Request, call_next): # type: ignore
    request_id = str(uuid.uuid4())
    # Inject request_id into log context could be done here with ContextVar
    # For simplicity, we just add it to response headers
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root(): # type: ignore
    return {"message": "Fetal Plane Explorer API. Go to /docs for API documentation."}
