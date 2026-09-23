from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import auth, imagery, query
from app.core.config import settings
from fastapi.responses import JSONResponse

app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(imagery.router)
app.include_router(query.router)


@app.exception_handler(SatQueryError)
async def satquery_error_handler(_request: Request, exc: SatQueryError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.to_response())
