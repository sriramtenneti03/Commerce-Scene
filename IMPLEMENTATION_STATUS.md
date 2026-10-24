# Implementation status

Updated 2026-10-24. This file describes observed code in this repository, not the full target in `spec.md`.

## Implemented in this local build

- React + TypeScript + Vite workspace shell and responsive dashboard/navigation.
- FastAPI API with generated OpenAPI documentation and health/readiness endpoints.
- SQLite persistence with first-run sample catalogue and brand profile.
- Product list/search, create, detail, duplicate, and archive API operations.
- Product detail editing in the UI and CSV catalogue import with required header checks, per-row errors, and duplicate SKU handling.
- JPEG/PNG/WebP upload with MIME/signature checks, a 20 MB cap, image dimension checks, and local file persistence.
- Version-incrementing brand profile updates and immutable settings copied into generation batch configuration.
- Asynchronous-in-process mock batch processing with persisted batch/output records and explicitly labeled, non-AI output.
- Job list with polling, asset review/approval, private API file delivery, and approved-only ZIP export with CSV manifest.
- Frontend production build: passed with Node.js 24.19.0 (`npm run build`), including after catalogue updates.
- API syntax and startup on Python 3.13: passed.
- Local API workflow smoke check: passed. Confirmed dashboard response, product creation, persisted mock batch completion, asset approval, successful ZIP export with manifest, and CSV import. Temporary smoke-test records and files were removed afterward.

## Not implemented yet

- Authentication, email flows, user profiles, workspace membership, roles, and tenant isolation.
- PostgreSQL/Alembic, Supabase Auth/Storage or S3, Redis and a durable independent worker.
- Real provider adapter, credentials validation, usage accounting, provider retries/idempotency, SSE, job cancellation, and recovery after process restart.
- Column-mapping wizard for CSV import, bulk catalogue operations, variants, marketplace profile management, configurable validation rules.
- Rich image editor/version history, side-by-side comparison, favorite/reject actions, marketplace dimension/format transforms, export queue, expiring signed URLs.
- Comprehensive automated unit, integration, component, and E2E tests and production deployment hardening.

## Current limitations

The local API is intentionally single-user and has no authentication or workspace isolation. Do not expose it to untrusted networks. The local mock is the only generation mode; it creates labeled preview artwork and never claims an AI generation occurred. Batch processing is a background thread in the API process and is not durable across a restart while work is in progress. Exports are synchronous local ZIP creation. These gaps prevent this build from meeting the production definition of done in `spec.md`.
