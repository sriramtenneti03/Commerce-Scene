# Local run and deployment notes

## Local development

Run the API and frontend separately as described in the root README. API data is persisted in `commerce-data`. Back up that directory if you need to retain local content.

## Deployment status

There is no supported production deployment configuration yet. Before deploying, implement Supabase/JWT authentication and workspace authorization on every lookup, use PostgreSQL migrations, private object storage and short-lived authorized downloads, move generation/export work to a durable queue, configure rate limits and request limits, add secrets through the server environment, and run the automated isolation and workflow test suites. The current API is intentionally unauthenticated and local-only.

## Environment

`COMMERCE_DATA_DIR` sets the local directory for SQLite and files. `.env.example` reserves names for future services; blank variables do not enable those services. Provider keys must never be placed in frontend environment variables.
