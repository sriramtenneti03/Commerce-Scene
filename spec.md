# CommerceScene — AI Product Content Studio
## Master Coding Specification

## 1. ROLE AND OBJECTIVE

Act as a senior full-stack software engineer, frontend architect, backend engineer, AI integration specialist, database designer, QA engineer, and UI/UX designer.

Build a complete, production-oriented web application called **CommerceScene — AI Product Content Studio**.

CommerceScene enables e-commerce sellers to upload ordinary product photographs, establish reusable brand guidelines, generate multiple AI-powered product image variations, maintain consistent branding across their catalogue, review and edit generated images, monitor background jobs, and export validated marketplace-ready image packages.

The application must be fully functional across its frontend, backend, database, storage, image-generation integration, background workers, and export workflows.

**Do not deliver only a design, static website, frontend mockup, or proof of concept. Build the actual application.**

Work directly inside the existing repository. Inspect its current structure before making changes. Preserve useful existing code and configuration. If the repository is empty, initialize the project with the architecture specified below.

Do not stop after creating a plan, scaffolding, database schemas, or frontend pages. Implement the working features, execute commands and tests where possible, fix errors, and continue until the acceptance criteria are met or a genuine external dependency blocks progress.

Never claim a feature works unless you have implemented and verified it.

---

## 2. PRODUCT VISION

### Core proposition

"Transform a product catalogue into a consistent collection of professional, marketplace-ready images using AI, reusable brand rules, and efficient bulk workflows."

### Primary differentiator

CommerceScene is not merely an AI image generator. Its core capability is catalogue-wide visual consistency.

The application must preserve and reuse:
- Brand colors and approved visual styles.
- Background and lighting preferences.
- Product framing and placement rules.
- Scene templates and marketplace presets.
- Reference photographs and product identity constraints.
- Approved image versions and brand configuration history.

When users change a brand template, existing assets and historical jobs must remain associated with their original configuration versions.

AI-generated imagery is not guaranteed to preserve every product detail perfectly. Provide reference-image conditioning when the selected provider supports it and let users inspect and approve results.

### Target audience

- E-commerce sellers.
- Direct-to-consumer brands.
- Marketplace merchants.
- Product photography and marketing agencies.
- Businesses managing large product catalogues.

---

## 3. REQUIRED TECHNOLOGY STACK

### Frontend

- React.
- TypeScript with strict type checking.
- Vite.
- Tailwind CSS.
- shadcn/ui.
- Lucide icons.
- React Router.
- TanStack Query.
- Zustand.
- React Hook Form.
- Zod.
- Vitest.
- React Testing Library.
- Playwright for end-to-end testing.

### Backend

- Python 3.11 or a currently supported compatible Python version.
- FastAPI.
- Pydantic.
- SQLAlchemy 2.
- Alembic migrations.
- PostgreSQL.
- Supabase Auth for user authentication.
- Supabase Storage or S3-compatible private object storage.
- Redis.
- Celery or another persistent background-job system.
- Pillow for image processing.
- Pytest.

### Infrastructure

- Docker and Docker Compose for reproducible local development.
- PostgreSQL and Redis services for local execution.
- Separate API and background-worker processes.
- Environment-based configuration.
- Structured logging and health checks.

### Architecture decision

Use Supabase for authentication, PostgreSQL, and object storage when configured. Keep the FastAPI backend as the authoritative application API for business operations, authorization, image processing, AI calls, job management, and exports.

Verify Supabase JWTs on the backend. Never trust client-supplied user or workspace identifiers without authorization checks.

All AI provider credentials must remain on the server.

If credentials or external services are unavailable, implement a clearly identified development mode with a mock provider. Do not fabricate successful real AI generations.

---

## 4. FIRST ACTION: INSPECT THE REPOSITORY

Before implementation:

1. Inspect all repository files, package manifests, source folders, environment examples, Git status, and existing configuration.
2. Identify the current frontend and backend setup.
3. Identify what already works and what is missing.
4. Preserve existing user work and avoid destructive resets.
5. Establish a concise implementation plan.
6. Begin implementing the highest-priority functional workflow immediately.

Create and maintain:
- `README.md`
- `.env.example`
- `IMPLEMENTATION_STATUS.md`
- `docs/ARCHITECTURE.md`
- `docs/API.md`
- `docs/DEPLOYMENT.md`

Keep `IMPLEMENTATION_STATUS.md` updated as real features are completed and tested.

Do not paste all files into the chat instead of creating them in the repository. Use the coding tools to create, edit, and validate the project files directly.

---

## 5. PROJECT STRUCTURE

Use a clean monorepo structure similar to:

```text
commercescene/
├── apps/
│   └── web/
│       ├── public/
│       ├── src/
│       │   ├── app/
│       │   │   ├── router.tsx
│       │   │   └── providers.tsx
│       │   ├── components/
│       │   │   ├── ui/
│       │   │   ├── layout/
│       │   │   ├── upload/
│       │   │   ├── products/
│       │   │   ├── branding/
│       │   │   ├── generation/
│       │   │   ├── assets/
│       │   │   └── exports/
│       │   ├── features/
│       │   ├── hooks/
│       │   ├── lib/
│       │   │   ├── api.ts
│       │   │   ├── auth.ts
│       │   │   └── utils.ts
│       │   ├── pages/
│       │   ├── stores/
│       │   ├── schemas/
│       │   ├── types/
│       │   ├── App.tsx
│       │   └── main.tsx
│       ├── tests/
│       ├── package.json
│       └── vite.config.ts
├── apps/
│   └── api/
│       ├── app/
│       │   ├── api/
│       │   │   └── v1/
│       │   ├── core/
│       │   ├── db/
│       │   ├── models/
│       │   ├── schemas/
│       │   ├── repositories/
│       │   ├── services/
│       │   ├── providers/
│       │   ├── workers/
│       │   ├── storage/
│       │   └── main.py
│       ├── migrations/
│       ├── tests/
│       └── requirements.txt
├── infra/
│   └── docker-compose.yml
├── docs/
├── .env.example
├── .gitignore
├── IMPLEMENTATION_STATUS.md
└── README.md
```

Adapt the folder structure if the existing repository already has a good organization. Do not create redundant nested applications or duplicate package manifests.

Keep the code modular, typed, testable, and understandable.

---

## 6. APPLICATION ROUTES AND NAVIGATION

Implement the following routes.

### Public routes

- `/login`
- `/signup`
- `/forgot-password`
- `/reset-password`

### Protected application routes

- `/onboarding`
- `/dashboard`
- `/products`
- `/products/new`
- `/products/:productId`
- `/brands`
- `/brands/:brandId`
- `/scenes`
- `/studio`
- `/jobs`
- `/jobs/:jobId`
- `/assets`
- `/assets/:assetId`
- `/exports`
- `/settings`

Add appropriate redirects, route guards, loading states, page titles, error boundaries, and a not-found page.

Use a consistent application shell with:
- Responsive sidebar.
- Workspace switcher.
- Breadcrumbs.
- Page heading and contextual actions.
- User profile menu.
- Notifications or activity indicator.
- Main content region.
- Responsive mobile navigation.

Do not implement all routes as copies of the same placeholder page.

---

## 7. AUTHENTICATION AND WORKSPACE MANAGEMENT

Implement:

- Email/password registration.
- Login and logout.
- Email verification flow.
- Password reset flow.
- Session restoration after refresh.
- Protected frontend routes.
- Backend JWT verification.
- User profile management.
- Workspace creation and switching.
- Workspace membership.
- Owner, admin, editor, and viewer roles.

Enforce roles on the backend.

A viewer must not be able to modify products or generate images. An editor should be able to perform permitted production operations without managing workspace membership. Administrative actions must require the appropriate role.

Enforce workspace isolation on all database queries, storage operations, job requests, asset lookups, and download links.

Use Supabase Auth when configured. Provide documented local-development instructions and test authentication setup.

Do not include default production passwords, hard-coded privileged users, or bypasses that grant access to arbitrary workspace data.

---

## 8. DASHBOARD

Build a real, data-driven dashboard containing:

- Total products.
- Uploaded source images.
- Generated assets.
- Active generation jobs.
- Failed jobs.
- Approved assets ready for export.
- Recently modified products.
- Recently generated images.
- Recent activity.
- Quick actions.
- Recent export jobs.

Every statistic must be calculated from actual authorized data.

Include:
- Initial loading skeletons.
- Useful empty states.
- Error states with retry options.
- Search and navigation actions.
- Responsive layout.
- Relative timestamps based on persisted dates.

Seeded demo records may be provided for a demonstration workspace. Label seeded data as sample data and do not misrepresent it as live provider output.

Avoid meaningless charts and decorative metrics that do not help the workflow.

---

## 9. PRODUCT CATALOGUE

Implement full product CRUD.

Each product must support:
- Name.
- SKU.
- Description.
- Category.
- Tags.
- Brand/workspace association.
- Product attributes.
- Optional variants.
- Original source photographs.
- Primary reference image.
- Brand template assignment.
- Marketplace targets.
- Generation history.
- Approved assets.
- Creation and modification timestamps.
- Archive status.

Required operations:
- Create.
- Read.
- Update.
- Duplicate.
- Archive.
- Search.
- Filter.
- Sort.
- Paginate.
- Select multiple products.
- Apply a template to selected products.
- Start a generation batch for selected products.

Add CSV import with:
- Column mapping.
- Required-field validation.
- Duplicate SKU detection.
- Per-row error messages.
- Import summary.
- Successful record persistence.

Use database constraints to enforce appropriate uniqueness rules. Do not assume SKUs must be globally unique across unrelated workspaces.

Product deletion and archive behavior must be deliberate. Preserve associated assets and generation history according to the documented retention policy.

---

## 10. MULTI-IMAGE UPLOAD SYSTEM

Build an accessible, polished drag-and-drop upload component.

Requirements:
- Select multiple files.
- Drag and drop.
- Display previews.
- Remove individual files.
- Select the primary image.
- Reorder references when relevant.
- Validate formats and sizes.
- Display per-file progress.
- Cancel supported uploads.
- Retry failures.
- Show clear error messages.
- Prevent duplicate registrations.
- Recover from expired upload sessions.

Support JPEG, PNG, and WebP initially.

Validate uploaded file signatures, declared MIME types, file size, and image dimensions. Do not trust file extensions alone.

Use private object storage. Prefer signed uploads for large files.

Record upload metadata in the database and confirm the object exists before declaring upload success.

Distinguish these states:
- Selected locally.
- Uploading.
- Upload completed.
- Registration completed.
- Upload failed.
- Cancelled.

Use browser object URLs only for temporary previews, and revoke them when no longer needed.

Create thumbnail previews where practical to avoid loading full-resolution assets in grids.

---

## 11. BRAND PROFILE AND TEMPLATE SYSTEM

This is the application's defining capability.

Implement persistent brand profiles that include:

- Name and description.
- Logo.
- Brand color palette.
- Preferred backgrounds.
- Lighting preferences.
- Camera and composition preferences.
- Product framing.
- Padding and margins.
- Shadow preferences.
- Optional watermark.
- Typography configuration for supported overlays.
- Visual tone.
- Restricted or prohibited changes.
- Default image dimensions and ratios.
- Scene templates.
- Marketplace overrides.
- Version information.

Include useful templates:
- Clean White Studio.
- Premium Luxury.
- Neutral Minimalism.
- Lifestyle Photography.
- Outdoor Adventure.
- Seasonal Campaign.
- Custom Scene.

Allow users to create, edit, duplicate, archive, and reuse templates.

Each generation batch must store an immutable snapshot of relevant settings. Updating a template must not change previously created outputs or historical generation settings.

Create a centralized prompt/configuration builder. Do not distribute ad hoc brand prompts across UI components.

When supported by the provider, use reference images and structured generation parameters to improve consistency.

The app must not claim that prompts alone can guarantee pixel-identical branding or perfect preservation of product labels.

---

## 12. SCENE BUILDER

Implement a scene selection interface containing:

- White studio.
- Neutral gradient.
- Luxury studio.
- Lifestyle setting.
- Outdoor environment.
- Seasonal scene.
- Editorial composition.
- Custom prompt.

For every scene, support the appropriate configurable fields:
- Background.
- Lighting.
- Camera angle.
- Composition.
- Mood.
- Product position.
- Crop.
- Aspect ratio.
- Output dimensions.
- Number of variations.

Let users preview their selected scene configuration before starting a batch.

Persist reusable presets.

Allow custom scenes without permitting arbitrary frontend instructions to bypass system constraints or security restrictions.

Do not require a paid AI request merely to open the scene builder.

---

## 13. MARKETPLACE PROFILES AND VALIDATION

Create configurable marketplace profiles.

A profile should support:
- Marketplace name.
- Target image role.
- Required or permitted dimensions.
- Aspect ratio.
- Output formats.
- File-size limits.
- Background rules.
- Product-padding constraints.
- Applicable logo and text restrictions.
- Version and effective date.
- Validation rules.

Use configurable profiles for channels such as Amazon, Shopify, and other supported marketplaces.

Do not present unverified marketplace rules as guaranteed current requirements. Use documented defaults and allow authorized users to configure them.

Before export:
1. Check dimensions.
2. Check image format.
3. Check file size.
4. Check configured aspect ratio.
5. Check applicable padding or background conditions.
6. Return actionable validation errors or warnings.

Treat visual compliance as a separate concern. Automated technical checks cannot guarantee that every image complies with all marketplace policies.

---

## 14. AI IMAGE GENERATION

Build a real provider-adapter architecture.

Create a provider interface separating application logic from provider-specific SDK calls.

The adapter should support, as available:
- Reference-image editing or generation.
- Scene generation.
- Image dimensions or aspect ratio.
- Multiple variations.
- Provider request IDs.
- Usage metadata.
- Timeout handling.
- Provider errors.
- Rate-limit responses.

Choose an image-generation provider only after verifying its current API, model capabilities, supported inputs, output formats, and configuration requirements. Keep provider choice configurable rather than hard-coded throughout the application.

Credentials must be loaded from backend environment variables.

Support two modes:

### Real generation mode

Calls the configured provider and saves the actual generated image. Exposes accurate progress and errors. Records provider and generation metadata.

### Mock development mode

Uses a clearly identified mock provider to exercise job processing, job statuses, retries, storage, review, and exports without paid API calls.

Mock mode must never pretend that a real AI generation occurred. Keep mock outputs visibly identified in the UI and metadata.

For production mode, fail fast with an actionable configuration message if required provider credentials or capabilities are missing.

### Generation inputs

Support:
- Product ID.
- Selected reference images.
- Brand profile ID and snapshot.
- Scene template.
- Optional custom scene prompt.
- Marketplace profile.
- Target image size.
- Number of variations.
- Generation settings supported by the selected provider.

Use server-side validation to prevent invalid or unauthorized requests.

Construct prompts using reusable, tested services. Include explicit instructions to preserve the product identity and avoid unsupported modifications.

### Submission workflow

1. Validate workspace and user permissions.
2. Validate source images and configuration.
3. Calculate the planned work.
4. Estimate usage where the provider exposes reliable pricing information.
5. Create a generation batch.
6. Persist individual jobs.
7. Queue background processing.
8. Return the batch identifier immediately.
9. Process jobs asynchronously.
10. Save images to object storage.
11. Save image metadata to PostgreSQL.
12. Publish status updates.
13. Display results in the asset library.

Do not execute long-running image generation inside a blocking request/response cycle.

---

## 15. BACKGROUND JOB PROCESSING

Use Redis and Celery or a similarly reliable queue architecture.

Persist job state in PostgreSQL.

Job states:

- queued.
- processing.
- succeeded.
- partially_succeeded.
- failed.
- cancel_requested.
- cancelled.

Use valid state transitions and make job handling safe under worker restarts and duplicate task delivery.

Every individual image-generation job should record:
- Workspace.
- Product.
- Batch.
- Source image references.
- Brand configuration snapshot.
- Scene settings.
- Provider/model.
- Current status.
- Attempt count.
- Last error category.
- Created and updated timestamps.
- Start and completion times.
- Output asset IDs.
- Usage metadata when available.

Implement:
- Bounded retries.
- Exponential backoff with jitter.
- Provider-specific retry classification.
- Per-workspace concurrency limits.
- Provider rate-limit handling.
- Task timeouts.
- Idempotency keys.
- Recovery of interrupted processing.
- Cancellation where the provider and worker lifecycle permit it.
- Failed-job diagnostics.
- Successful output preservation.

Do not retry every error indiscriminately. Invalid inputs and permanent authorization failures should not be retried automatically.

Avoid double charging caused by duplicate submissions. Where possible, pass provider idempotency keys or persist request identifiers and recover existing work instead of resubmitting blindly.

A partially successful batch must retain its successful outputs.

Implement a documented reconciliation strategy for jobs left in an uncertain state after a worker or provider failure.

---

## 16. LIVE PROGRESS AND JOB DASHBOARD

Implement live job monitoring using Server-Sent Events with polling fallback, or another documented reliable approach.

Display:
- Queue status.
- Processing status.
- Number of completed images.
- Number of failed images.
- Number of pending images.
- Current stage where known.
- Elapsed time.
- Last update.
- Error summary.
- Results as they become available.

Calculate progress using real job counts or actual provider progress when available. Never invent progress percentages.

Allow:
- Open batch details.
- Inspect individual jobs.
- Retry eligible failed images.
- Cancel queued work where supported.
- Navigate away and return.
- Filter jobs by product, date, and status.
- View retry history.

Ensure the UI does not start duplicate work because of repeated clicks or network reconnections.

Use TanStack Query invalidation or appropriate cache updates when the batch or job state changes.

---

## 17. ASSET LIBRARY AND IMAGE COMPARISON

Create a library of generated assets.

Features:
- Grid and list views.
- Search.
- Filters.
- Sorting.
- Pagination.
- Product association.
- Scene and template filters.
- Approval status.
- Favorite status.
- Source-image metadata.
- Generation settings.
- Full-resolution preview.
- Download.
- Regeneration.
- Image version history.

Create a variation comparison interface with at least:
- Side-by-side comparison.
- Before/after comparison.
- Zoom.
- Fit-to-screen.
- Pan where appropriate.
- Keyboard-accessible selection.
- Approve, reject, and favorite actions.
- Regenerate actions.
- Rejection notes.

Ensure image dimensions, aspect ratios, and display surfaces do not cause accidental stretching or misleading comparisons.

Do not load every full-resolution image into the initial library grid.

---

## 18. IMAGE EDITOR

Implement real editing functionality.

Version one must include:
- Crop.
- Resize.
- Canvas padding.
- Supported background-color adjustment.
- Optional supported watermark overlay.
- Preview before saving.
- Undo and redo for supported operations.
- Save as a new asset version.
- Restore an earlier version.

Use Pillow or an appropriate image-processing service for deterministic operations.

Each edit must record:
- Parent asset/version.
- Editing parameters.
- Resulting dimensions.
- Resulting format.
- Timestamp.
- Editing user.
- Output storage key.

Preserve the original and previously approved versions.

If the editor includes advanced AI background replacement or inpainting, connect it to a real compatible endpoint. Otherwise, label the feature as unavailable instead of simulating success.

---

## 19. BATCH EXPORT

Build an asynchronous export system.

Users must be able to:
1. Select products.
2. Select approved assets.
3. Select target marketplace profiles.
4. Choose output formats and dimensions.
5. Validate selected assets.
6. Review validation failures.
7. Confirm export.
8. Track export progress.
9. Download the completed ZIP.
10. Revisit export history.

Generate a manifest CSV containing:
- Product ID.
- Product name.
- SKU.
- Marketplace.
- Scene.
- Asset ID.
- File path.
- Output width and height.
- Format.
- File size.
- Validation outcome.

Use an organized structure such as:

```text
commercescene-export.zip
├── product-001/
│   ├── amazon/
│   │   ├── hero.jpg
│   │   └── lifestyle-01.jpg
│   └── shopify/
│       ├── hero.webp
│       └── lifestyle-01.webp
├── product-002/
│   ├── amazon/
│   └── shopify/
└── manifest.csv
```

Sanitize archive paths and filenames.

Create export archives in background jobs and store them securely. Generate short-lived signed download URLs only after the export is complete and authorized.

Record export status, selected assets, validation results, archive metadata, and expiration.

Do not mark export jobs completed until the generated archive has been verified.

---

## 20. DATABASE MODELS

Create normalized SQLAlchemy models and Alembic migrations for:

- Workspace.
- WorkspaceMember.
- UserProfile where needed.
- Product.
- ProductVariant.
- SourceImage.
- BrandProfile.
- BrandProfileVersion.
- BrandTemplate.
- MarketplaceProfile.
- GenerationBatch.
- GenerationJob.
- GeneratedAsset.
- AssetVersion.
- ExportJob.
- ExportItem where required.
- ActivityEvent.
- UsageRecord.

Define relationships, foreign keys, database constraints, useful indexes, and UTC timestamps.

Use transactions for related writes.

Store image binaries in object storage, not directly in database rows.

Use soft deletion or archive semantics where appropriate.

Ensure workspace ownership is checked on every relevant lookup. Random identifiers or UUIDs do not replace authorization checks.

Add seed scripts for a clearly identified demo workspace and test dataset.

---

## 21. FASTAPI ENDPOINTS

Use `/api/v1` and consistent Pydantic response schemas.

Implement endpoints for:

### Workspace
- Create workspace.
- List accessible workspaces.
- Get workspace.
- Update workspace.
- Manage memberships and roles.

### Products
- Create product.
- List products with search, sorting, filters, and pagination.
- Retrieve product.
- Update product.
- Duplicate product.
- Archive product.
- Import CSV.

### Uploads
- Create secure upload authorization.
- Confirm and register an uploaded image.
- Retrieve image metadata.
- Remove an eligible uploaded asset.

### Branding and scenes
- Create, list, update, duplicate, and archive brand profiles.
- Retrieve brand versions.
- Create and manage templates.
- List and retrieve scene presets.
- Create and manage marketplace profiles.

### Generation
- Create a generation batch.
- Get batch status.
- List batches.
- Get individual job details.
- Stream job updates.
- Retry an eligible failed job.
- Cancel eligible work.

### Assets
- List assets with pagination and filters.
- Get asset details.
- Update approval and favorite status.
- Create an edited version.
- Restore a supported previous version.
- Generate an authorized download URL.

### Exports
- Create an export job.
- List export jobs.
- Get export status.
- Get validation results.
- Generate an authorized download URL.
- Cancel an eligible export.

Also implement:
- `/health/live`
- `/health/ready`

Use correct HTTP status codes, request validation, pagination, permission checks, and structured errors.

Document all API endpoints through FastAPI's OpenAPI documentation.

---

## 22. FRONTEND ENGINEERING RULES

### Server state

Use TanStack Query for:
- API queries.
- Mutations.
- Caching.
- Loading and error states.
- Pagination.
- Invalidation.
- Refetching job status.

### UI state

Use Zustand only for suitable shared client-side state, such as:
- Active generation selections.
- Temporary scene configuration.
- Editor interaction state.
- Cross-component UI preferences.

Keep form state in React Hook Form.

Do not mirror the full database into Zustand.

### Validation

Use shared or aligned Zod and Pydantic schemas where practical.

Validate forms at the client for usability and independently validate all inputs at the backend.

### Performance

- Lazy-load routes.
- Lazy-load heavy editor modules.
- Use thumbnails.
- Limit concurrent uploads.
- Cancel obsolete queries.
- Avoid unnecessary re-renders.
- Use list virtualization when justified.
- Paginate large asset collections.
- Avoid loading large image binaries before they are required.
- Avoid retaining unused object URLs.
- Keep polling intervals reasonable and back off when tabs are inactive.

### UX and accessibility

Every page needs meaningful:
- Loading states.
- Empty states.
- Error states.
- Success feedback.
- Form errors.
- Disabled states.
- Confirmation dialogs.

Implement accessible dialogs, keyboard focus management, labels, visible focus indicators, responsive layouts, and appropriate status announcements.

Never place decorative controls that do nothing.

---

## 23. VISUAL DESIGN DIRECTION

Design a polished, contemporary B2B SaaS application.

Use:
- A neutral background.
- Consistent typography.
- Restrained brand accents.
- Clear spacing.
- Clean cards and data tables.
- Professional image previews.
- A restrained status-color system.
- Accessible contrast.
- Consistent borders and corner radii.
- Subtle transitions.
- Responsive desktop-first production workflows.

Use shadcn/ui consistently and customize its theme rather than mixing multiple unrelated component systems.

Make CommerceScene feel like an actual commercial product.

Avoid:
- Excessive gradients.
- Excessive glassmorphism.
- Oversized empty hero areas inside the production dashboard.
- Too many nested cards.
- Unnecessary charts.
- Fake activity.
- Placeholder buttons.
- Hard-coded success messages.
- Sample numbers displayed as real metrics.

Prioritize the image studio, catalogue, brand editor, live jobs, asset comparison, and export workflow.

Do not let visual polish delay implementation of persistent backend behavior.

---

## 24. SECURITY AND DATA INTEGRITY

Implement:

- JWT verification.
- Backend authorization.
- Workspace isolation.
- Private object storage.
- Short-lived signed download URLs.
- Upload file-signature checks.
- Safe filename handling.
- File-size and dimension limits.
- Request rate limits.
- Generation quotas.
- Idempotent mutations.
- Input validation.
- SQL transaction boundaries.
- Database constraints.
- Structured logging.
- Timeouts.
- Retry policies.
- Health checks.
- Appropriate data-retention procedures.

Never expose credentials in browser bundles or committed files.

Never use unrestricted storage URLs for confidential user content.

Never use user-supplied image paths to access arbitrary local files or remote network resources.

Protect against unsafe archive filenames and malicious content.

Log request IDs, batch IDs, and job IDs where useful. Never log credentials.

Do not claim enterprise security certification or regulatory compliance without actual verification.

---

## 25. TESTING REQUIREMENTS

Write meaningful automated tests.

### Backend unit tests

Test:
- Input validation.
- Authorization rules.
- Workspace isolation.
- Brand configuration snapshots.
- Job state transitions.
- Retry classification.
- Idempotency.
- Image resizing and cropping.
- Export filename sanitization.
- Marketplace validation.

### Backend integration tests

Test:
- Product CRUD.
- Upload registration.
- Batch creation.
- Mock provider processing.
- Database persistence.
- Failed-job retry.
- Partial batch completion.
- ZIP generation.
- Download authorization.

Use disposable test data and a test database. Never let tests modify production data.

### Frontend component tests

Test:
- Product forms.
- Upload file validation.
- Multi-selection.
- Scene configuration.
- Brand template forms.
- Job status display.
- Failed-job retry.
- Asset approval.
- Export confirmation.

### End-to-end tests

Build Playwright tests for:

1. Open the application.
2. Log in through a supported test setup.
3. Create a product.
4. Upload sample images.
5. Choose a reference image.
6. Create a brand template.
7. Configure a scene.
8. Submit generation through the mock provider.
9. Observe job status updates.
10. Review generated outputs.
11. Approve an asset.
12. Edit an image.
13. Inspect version history.
14. Create a batch export.
15. Download the ZIP.
16. Inspect the ZIP manifest and file structure.

Add a production-provider integration test that can be enabled explicitly when real credentials are available. Do not require paid API requests for ordinary CI.

Run the available tests after each implementation stage and fix regressions.

---

## 26. ENVIRONMENT AND LOCAL DEVELOPMENT

Create a complete `.env.example` with descriptive variable names and no real credentials.

Include relevant variables for:

- Frontend application URL.
- Backend API base URL.
- Supabase project URL and public authentication key.
- Backend-only Supabase service credentials when needed.
- PostgreSQL connection.
- Redis connection.
- Object storage.
- AI provider.
- Image-generation model.
- Upload size limits.
- Generation concurrency limits.
- Worker retry configuration.
- Mock provider mode.
- CORS origins.
- Logging level.

Do not use frontend-prefixed environment variables for secrets.

Validate required backend settings at startup and display actionable configuration errors.

Create a Docker Compose setup where practical, including PostgreSQL, Redis, API, and worker services.

Document:
- Prerequisites.
- Environment configuration.
- Dependency installation.
- Migrations.
- Seed data.
- Frontend startup.
- Backend startup.
- Worker startup.
- Tests.
- Production builds.
- Deployment.
- Supabase setup.
- AI provider setup.

Make development mode usable without real generation credentials by using the mock provider.

---

## 27. IMPLEMENTATION ORDER

Work through the following stages in order. Continue autonomously wherever the environment permits.

### Stage 1: Repository and project foundation
- Inspect repository.
- Configure frontend and backend.
- Install dependencies.
- Establish TypeScript and linting settings.
- Configure route structure and design system.
- Verify the frontend starts and builds.

### Stage 2: Authentication and database
- Configure environment settings.
- Implement database models.
- Create migrations.
- Implement workspace access checks.
- Integrate authentication.
- Seed demo data.
- Write persistence tests.

### Stage 3: Products and uploads
- Implement product CRUD.
- Implement product search and filtering.
- Implement drag-and-drop uploads.
- Integrate storage.
- Persist upload metadata.
- Verify the full upload workflow.

### Stage 4: Brands and scenes
- Implement brand profiles.
- Implement versioned templates.
- Implement scene configuration.
- Implement marketplace presets.
- Verify that configuration snapshots remain stable.

### Stage 5: AI generation
- Implement provider interface.
- Implement mock provider.
- Implement real configurable provider adapter.
- Build persistent batches and jobs.
- Integrate background workers.
- Implement retries and progress updates.
- Verify success, partial success, and failure behavior.

### Stage 6: Asset library and editor
- Implement image search and filters.
- Implement comparison and approval.
- Implement real image operations.
- Implement immutable asset version history.
- Verify restore and download behavior.

### Stage 7: Exports
- Implement marketplace validation.
- Implement background ZIP creation.
- Generate CSV manifest.
- Implement secure download links.
- Verify archive structure and file contents.

### Stage 8: Production readiness
- Run tests.
- Fix TypeScript errors.
- Fix frontend build errors.
- Run backend tests.
- Test migrations.
- Verify authorization.
- Verify real provider setup where credentials exist.
- Verify mock-provider workflow end to end.
- Update documentation.
- Produce a final implementation report.

Do not declare a stage completed merely because files were created. Run the relevant checks and record the result.

---

## 28. DEFINITION OF DONE

The application can be considered functionally complete when all of the following are true:

1. Frontend builds successfully.
2. Backend starts successfully.
3. Database migrations run successfully.
4. Authentication works with the configured provider.
5. Workspace access is enforced.
6. Products persist across reloads.
7. Multi-image uploads work with real storage.
8. Brand profiles and templates persist.
9. Generation requests create persistent background jobs.
10. The mock provider exercises the actual job pipeline without external API credentials.
11. A configured real provider generates actual output images.
12. Job updates reflect persisted backend state.
13. Retry logic preserves successful outputs.
14. Asset comparison and approval work.
15. Supported editing operations create new versions.
16. Version history and restore work.
17. Marketplace validation runs against configured rules.
18. ZIP exports contain actual selected assets.
19. CSV manifests accurately describe exported content.
20. Downloads are authorized.
21. Workspace isolation tests pass.
22. Critical end-to-end workflows pass.
23. Documentation explains how to run and deploy the application.
24. Unimplemented functionality is documented honestly.

---

## 29. CODING AGENT EXECUTION RULES

- Build features, not just plans.
- Inspect before modifying.
- Work in small, coherent implementation stages.
- Prefer complete vertical slices over disconnected components.
- Reuse existing working code.
- Use strict TypeScript and typed API contracts.
- Avoid giant monolithic files.
- Avoid duplicated business logic.
- Avoid hard-coded production data.
- Avoid fake API responses in production mode.
- Avoid swallowed exceptions.
- Avoid broad untyped error handling.
- Do not hard-code provider credentials.
- Do not disable security checks to make tests pass.
- Do not remove tests simply because they fail.
- Do not replace persistent data with frontend-only local state.
- Do not leave essential controls as TODO placeholders.
- Do not claim to have run commands that were not run.
- Do not stop to request confirmation for ordinary implementation decisions; make sensible documented defaults.
- When a missing credential genuinely blocks an external integration, finish everything possible locally and document the exact credential/configuration needed.
- If a tool or dependency is unavailable, select a compatible alternative and document the decision.
- If an implementation fails, inspect the error, fix the actual cause, and rerun the relevant checks.
- Keep `IMPLEMENTATION_STATUS.md` accurate.
- Do not make destructive Git changes or discard user changes.
- Keep the repository in a buildable state throughout development when practical.

---

## 30. FINAL REPORT

After implementation, provide a concise but precise report containing:

- Completed features.
- Architecture and key design decisions.
- Important files created or modified.
- Database migrations and seed commands.
- Environment variables that must be configured.
- Commands to start the frontend, API, Redis, and worker.
- Commands to run tests.
- Build and test results actually observed.
- Whether real AI generation was verified.
- Known limitations and remaining blockers.
- Exact next steps needed to run the application in the user's environment.

Begin by inspecting the repository, then implement CommerceScene directly in the project. Do not stop after writing the plan or creating the initial interface.
