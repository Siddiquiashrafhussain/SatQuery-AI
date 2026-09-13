# System Architecture

SatQuery AI follows a microservices-based architecture orchestrated via Docker Compose.

## Service Overview

1.  **Frontend**: A modern web client (React/Vite) providing the user interface for uploading datasets and entering queries.
2.  **Backend**: A Python API (FastAPI) responsible for handling requests, routing GIS processing, and coordinating AI model inference.
3.  **Database**: PostgreSQL equipped with the PostGIS extension for spatial data storage and complex geographic queries.

*Future Architecture Additions:*
*   **GPU Worker Node:** For dedicated AI model inference without blocking web requests.
*   **Redis:** For job queues and caching.
*   **Object Storage (MinIO/S3):** For horizontally scalable raw dataset storage.

## How Services Communicate

1.  **Client to API**: The Frontend communicates with the Backend strictly via REST API over HTTP/JSON (routed to `API_BASE_URL`).
2.  **API to Database**: The Backend communicates with PostgreSQL/PostGIS over TCP (port 5432) using standard connection pooling.
3.  **Cross-Origin Resource Sharing (CORS)**: The Backend strictly whitelists the Frontend's URL to prevent unauthorized access.
