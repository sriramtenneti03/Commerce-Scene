# Architecture

## Current local implementation

- `apps/web`: React, TypeScript, Vite, React Router, Lucide icons, and a small custom responsive component system. The API is accessed via same-origin `/api` proxy in development.
- `apps/api/app/main.py`: FastAPI routes and local application services.
- SQLite: `commerce-data/commercescene.db`, initialized on API startup. Tables persist products, images, brand profiles, generation batches, assets, and exports.
- Local files: source uploads and mock PNG assets live under `commerce-data/uploads`; ZIPs live under `commerce-data/exports`. API routes serve files only through database records.
- Mock jobs: batch creation persists a settings snapshot, starts an API-process worker thread, writes labeled preview PNGs and updates persisted counters.

## Production target versus current build

The target architecture from `spec.md` is FastAPI + SQLAlchemy/Alembic + PostgreSQL, Supabase JWT authentication, private Supabase/S3 storage, and Redis with a durable worker. Those services are not configured here. The current code is suitable for a local single-user demo only. A production migration should first add identity and workspace scoping, then move persistence/storage/queue behind adapters, then implement provider adapters and durable job reconciliation.

## Data and history

Products own source image records and generated asset records. Each batch stores the selected brand row copied at submission time, plus scene, selected products, and variation count. Brand edits increment a version, while batch settings remain unchanged. Asset approval is persisted and required before export.
