# API overview

All application routes use `/api/v1`. Interactive OpenAPI docs are exposed at `/docs` by FastAPI.

| Method | Route | Purpose |
|---|---|---|
| GET | `/dashboard` | Counts and recent products/batches |
| GET, POST | `/products` | Search catalogue; create a product |
| GET | `/products/{product_id}` | Product with source images and assets |
| PATCH | `/products/{product_id}` | Update a product |
| POST | `/products/{product_id}/duplicate` | Duplicate a product |
| POST | `/products/{product_id}/archive` | Archive a product |
| POST | `/products/import-csv` | Import CSV rows (`name` and `sku` required; category, description, and semicolon-delimited tags optional) |
| POST | `/uploads/{product_id}` | Validate and persist one source image |
| GET | `/images/{image_id}/file` | Retrieve registered source image |
| GET, POST | `/brands` | List or create brand profiles |
| PUT | `/brands/{brand_id}` | Update profile and increment version |
| POST | `/generation/batches` | Queue a mock generation batch |
| GET | `/generation/batches` | List persisted batches |
| GET | `/generation/batches/{batch_id}` | Batch settings and outputs |
| GET | `/assets` | Search/filter generated assets |
| POST | `/assets/{asset_id}/approve` | Approve an asset |
| GET | `/assets/{asset_id}/file` | Retrieve registered generated output |
| POST | `/exports` | Validate approved assets and create ZIP + manifest |
| GET | `/exports` | List export history |
| GET | `/exports/{export_id}/download` | Download a completed export |

The local API is unauthenticated and all data belongs to one local workspace. Never expose it as a shared service. Errors use FastAPI HTTP error responses; duplicate SKUs return 409 and unapproved assets return 422 on export.
