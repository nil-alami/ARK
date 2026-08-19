# Stage 07 — API and integration design

Governing source: `system-design-prompt.md` section **6. API and integration design**.

Inputs: Stages 02–06.

## Work

- Define external APIs, internal contracts, endpoint responsibilities, concrete request/response schemas, async job APIs, errors, versioning, limits, timeouts, callbacks, identity, and tenant propagation.
- Decide unified operational envelope versus capability-specific APIs versus workflow API.
- Define idempotency and correlation semantics precisely.
- Show how platform-owned adapters keep ARK platform-neutral.
- Ask `platform_architect` for contract-boundary review.

Output: `outputs/stages/07-api-integration.md`.

Gate: schemas are concrete enough to implement and every endpoint has authentication, authorization, tenant source, timeout, idempotency, and error behavior.
