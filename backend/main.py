import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.errors import APIError, format_unexpected_error
from core.logger import get_logger

logger = get_logger("main")

app = FastAPI(title="SatQuery AI API")

# --- Security: CORS Configuration ---
# Restrict origins in production based on environment variables
ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# --- Security: Structured Error Handling ---
# Catch our custom API errors
@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    logger.warning("API Error", extra={"code": exc.code, "status": exc.status_code})
    return JSONResponse(status_code=exc.status_code, content=exc.to_dict())

# Catch unexpected crashes without exposing internal stack traces
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled Exception", exc_info=True) # Log trace internally
    safe_response = format_unexpected_error(exc)       # Hide trace externally
    return JSONResponse(status_code=500, content=safe_response)

@app.get("/health")
def health_check():
    return {"status": "ok"}

from app.api.routes import auth, imagery
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(imagery.router, prefix="/api/v1/imagery", tags=["imagery"])
