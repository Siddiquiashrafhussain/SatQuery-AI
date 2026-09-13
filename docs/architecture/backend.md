# Backend Architecture

The backend is built in Python, leveraging FastAPI for high-performance async routing.

## Core Responsibilities
*   Serve as the primary REST API.
*   Validate and securely handle dataset uploads.
*   Maintain the single source of truth for the Database (PostgreSQL).

## GIS Processing Integration
GIS processing logic (e.g., raster parsing, boundary extraction, CRS validation) is intended to be encapsulated in `backend/services/gis`. 
When a user uploads a `.tif`, the `core/file_handling.py` utility safely streams it to disk, and the GIS service then parses the metadata to validate the spatial extent before registering it in PostGIS.

## AI Model Integration (Future)
Future AI models (like object detection on satellite imagery) will be integrated in `backend/services/ai`. 
*   **Synchronous:** Fast models may run directly in the API thread.
*   **Asynchronous:** Heavy models will be offloaded to a Redis-backed GPU worker pool, with the backend API acting as the job orchestrator, returning a `job_id` to the frontend.

## Key Directories
*   `core/`: Core utilities (logger, error handlers, file security).
*   `services/`: Business logic, GIS processing, and AI integrations.
*   `tests/`: Unit and integration testing using `pytest`.
