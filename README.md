# SatQuery AI

SatQuery AI is a modern web application designed to query and process satellite imagery using AI models and GIS processing tools. The platform allows users to upload datasets (e.g. GeoTIFFs), run natural language or structured queries, and receive actionable intelligence backed by spatial and visual analysis.

## Core Features
*   **Satellite Image Processing:** Upload and validate high-resolution GIS files (.tif, .geojson).
*   **AI Integration (Planned):** Orchestrate advanced computer vision models to identify features from user queries.
*   **GIS Engine:** Spatial validations, coordinate reference system handling, and dataset parsing.

## Documentation
Please refer to the `docs/` directory for detailed information on the project:

### Architecture
*   [System Architecture](docs/architecture/system.md): High-level overview of services and communication.
*   [Backend Architecture](docs/architecture/backend.md): Details on the Python API, GIS engine, and AI model integration.
*   [Frontend Architecture](docs/architecture/frontend.md): Details on the React/Vite client interface.

### Development & API
*   [Local Development Setup](docs/development/setup.md): How to get the project running via Docker.
*   [API Contracts & Conventions](docs/api/api-contract.md): Standards for requests, responses, and error handling.
