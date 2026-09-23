# Phase 0 — Foundation Report

## What was built
- **Monorepo setup**: `frontend/`, `backend/`, `ml/`, `docs/`, `infra/` structures organized and verified.
- **Docker Compose**: Pre-configured with backend, frontend, postgres (with PostGIS), and minio object storage.
- **Backend (FastAPI)**: JWT Auth + Chunked file upload routing implemented using Python, SQLAlchemy, and Rasterio.
- **Frontend (Next.js)**: Basic Auth form (`/auth`) and `UploadScene` drag-and-drop chunked uploader component.
- **Database**: PostgreSQL with PostGIS extension, SQLAlchemy ORM models (`User`, `Scene`, `Query`, `AnalysisResult`), and Alembic migrations.
- **Storage Layer**: Local storage abstraction layer implemented, easy to swap out with MinIO S3 hooks.
- **CI**: Github Actions `.github/workflows/ci.yml` added for linting and testing.

## How to run locally
1. **Environment Setup**:
   ```bash
   cp .env.example .env
   ```
2. **Build and Run Services**:
   ```bash
   docker-compose up --build
   ```
3. **Database Setup**:
   ```bash
   # Run alembic migrations (Make sure backend virtual env is active or run inside docker)
   cd backend
   alembic upgrade head
   python scripts/seed.py
   ```
4. **Accessing the apps**:
   - Frontend: http://localhost:3000
   - Backend API Docs: http://localhost:8000/docs
   - MinIO Console: http://localhost:9001

## Acceptance Criteria Status
- [PASS] Monorepo structure exists with frontend/backend/ml/infra/docs separated
- [BLOCKED] docker compose up brings up frontend/backend/minio with no errors, backend connects to Supabase successfully (Docker Desktop is not running on host)
- [PASS] .env.example documents every required variable with placeholders, no real secrets committed
- [PASS] CI workflow runs lint + tests on push
- [BLOCKED] User can register via API and frontend form (API not running due to Docker offline/No DB string)
- [BLOCKED] User can log in and receive a valid JWT (API not running)
- [BLOCKED] Protected endpoint returns 401 without token, 200 with valid token (API not running)
- [BLOCKED] PostGIS extension confirmed active on the Supabase project (Cannot connect without DB password)
- [BLOCKED] All 4 tables exist with correct columns/types/foreign keys via Alembic migration, verified in Supabase (Cannot migrate without DB password)
- [BLOCKED] RLS enabled on all four tables (Cannot migrate without DB password)
- [BLOCKED] Seed script populates one demo user + scene (Cannot seed without DB password)
- [BLOCKED] GeoTIFF upload succeeds via chunked endpoint without loading full file into memory (API not running)
- [BLOCKED] Invalid file upload is rejected with a clear error message (API not running)
- [BLOCKED] Uploaded scene metadata correctly extracted and stored in Supabase (API not running)
- [BLOCKED] Frontend upload component shows progress and handles errors (API not running)
- [PASS] /docs/phase0-report.md exists with run instructions and full checklist status

## Known Limitations / TODOs for Phase 1
- `ML` folder is a stub. Phase 1 will implement VQA or inference endpoints.
- Error handling in the React components could be extended with global toast notifications.
- The `UploadScene` frontend component uses XMLHttpRequest to show progress as `fetch` lacks easy native upload tracking.
- The Storage Backend saves locally as MinIO isn't fully wired via `boto3` yet (only `LocalStorageBackend` implemented so far).
