# Local Development Setup

This guide explains how to spin up the SatQuery AI environment locally.

## Repository Structure
```text
.
├── backend/          # Python FastAPI application
├── frontend/         # React/Vite application
├── docs/             # Technical documentation
├── docker-compose.yml
├── .env.example
└── .gitignore
```

## Prerequisites
*   Docker & Docker Compose
*   Node.js (for local frontend dev, optional)
*   Python 3.10+ (for local backend dev, optional)

## Getting Started

1.  **Configure Environment Variables**
    Copy the example configuration to your active `.env` file:
    ```bash
    cp .env.example .env
    ```
    *Note: The `.env` file is excluded from Git via `.gitignore`. You can edit the values inside it to match your local setup.*

2.  **Start the Stack**
    Run the entire stack (Frontend, Backend, PostGIS) via Docker:
    ```bash
    docker-compose up --build
    ```

3.  **Access the Application**
    *   Frontend: `http://localhost:3000`
    *   Backend API: `http://localhost:8000`
    *   Database: `localhost:5432`

## Development Workflows
The Docker environment mounts your local `./frontend` and `./backend` directories directly into the containers. This means hot-reloading (for Vite and Uvicorn) will work out-of-the-box when you edit files locally.
