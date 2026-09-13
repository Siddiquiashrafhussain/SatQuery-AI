from fastapi import APIRouter
from app.api.routes import health, projects, datasets, upload, query, analysis, results

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(query.router, prefix="/query", tags=["query"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(results.router, prefix="/results", tags=["results"])
