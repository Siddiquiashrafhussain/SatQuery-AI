# Frontend Architecture

The frontend is a Single Page Application (SPA) built with React and bundled via Vite for rapid development and optimized production builds.

## Key Components

*   **Upload Component:** Handles drag-and-drop dataset uploads. It performs client-side validation (checking extensions like `.tif`) before interacting with the Backend API to save bandwidth.
*   **Query Input:** The main user interface for submitting natural language or structured search queries against the uploaded datasets.
*   **Map/Visualizer (Planned):** Will render bounding boxes, geospatial results, and the actual satellite imagery layers.

## State and API Integration
The frontend strictly adheres to the API contracts. It is responsible for parsing standardized JSON success responses and securely handling structured error responses (e.g., displaying `INVALID_FILE` gracefully to the user).

## Key Directories
*   `src/components/`: Reusable UI elements (Upload, QueryInput).
*   `src/tests/`: Client-side unit testing using Vitest and React Testing Library.
