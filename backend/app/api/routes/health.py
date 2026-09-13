from fastapi import APIRouter
from app.schemas.api import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def get_health():
    """Health check endpoint."""
    return HealthResponse(status="ok", version="1.0.0")
