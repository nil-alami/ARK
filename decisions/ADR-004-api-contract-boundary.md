# ADR-004 — API contract and integration boundary

Status: `ACCEPTED`

Date: 2026-08-11

Decision owner: ARK design sponsor (user approval)

## Context and requirements

ARK needs one implementable external contract that keeps seven capability modules independently versioned without creating seven service lifecycles or a schema-free generic executor. It must support platform-neutral consumer adapters, principal-derived tenant scope, synchronous calls only for measured short operations, one durable job lifecycle, large inputs/results by reference, polling, optional external notification, and machine-readable capability definitions.

`A-01-INT` reaches its Stage 07 dispositions, but named adapter owners, the identity provider/token protocol, consumer delivery constraints, first-release workflows, and migration/cutover inventories remain unavailable. The design therefore needs a narrow temporary integration disposition rather than a silent extension.

Evidence: `sources/normalized/ark-assumptions.md — Integration and contracts`, `— Execution, orchestration, and proactive operation`, `— Security, ownership, and operations`; `outputs/stages/01-discovery-and-questions.md — A-01-INT`, `— INT-01 through INT-05`; `outputs/stages/02-system-definition.md — ARK-FR-004 through ARK-FR-008`, `— ARK-NFR-001 through ARK-NFR-004`; `outputs/stages/05-end-to-end-architecture.md — C05-01 through C05-05`, `— C05-12`, `— C05-22`; `outputs/stages/06-data-architecture.md — Data boundaries and invariants`.

## Decision

ARK will use this API/integration boundary:

1. One major-versioned platform REST/JSON namespace exposes shared capability discovery, ingestion, dataset, job, result, subscription/configuration, and callback conventions.
2. Capability execution uses typed capability/version/operation paths and schemas inside that namespace. There is no schema-free universal execute contract and no separate network API/service lifecycle per capability.
3. Durable operations return `202 Accepted` with a universal tenant-scoped job resource. Polling/status/result retrieval is the required recovery path. Synchronous invocation is enabled only for an operation whose definition contains an approved measured short/predictable profile; the API never silently changes sync to async.
4. A named versioned workflow submission path remains conditional until Stages 08/09 approve a concrete workflow and grant semantics. No caller-programmable DAG/DSL or workflow engine is introduced.
5. Tenant authority comes only from validated immutable `AuthContext`; no body/header/path business/customer/tenant identifier can establish or broaden tenant scope.
6. Every side-effecting external command requires a tenant/caller/route-scoped idempotency key. Same key and canonical request replays the same logical resource; same key with different request returns a conflict. Correlation remains distinct from request, job, execution, result, event, and delivery identities.
7. External notifications use only a registered tenant-scoped callback reference, versioned minimal event envelope, and later-approved signature controls. Polling remains authoritative; delivery failure never changes or reruns a capability result. SSE/public event feed and internal event infrastructure are not selected.
8. Consumer-specific translation remains outside capability cores. ARK owns platform-neutral schemas, conformance support, and technical/provider adapters; consumer-platform integration roles own consumer terminology/mapping by default. Any ARK-operated migration adapter remains isolated behind public contracts and creates no new cross-writes.
9. Large inputs/results/artifacts use opaque tenant-scoped references. Endpoint definitions must contain concrete request, collection, page, result, rate, and timeout policies before activation; no numeric production values are invented in Stage 07.
10. Synapse remains an unavailable/interface-only adapter target under `A-03-SYNAPSE`. Its legacy API keys, body IDs, `Agent` names, opaque settings, costs, verifier status, and undocumented internals do not become ARK trust, tenant, policy, workflow, or production contracts.

The sponsor approved the following temporary disposition with the Stage 07 outputs on 2026-08-11:

**`A-07-INTEGRATION` — Stage 07 integration disposition.** Consumer/platform-side adapters remain the default owners of consumer-specific translation; ARK owns the platform-neutral API, schemas, conformance support, and technical/provider adapters. External callers present `Authorization: Bearer <access-token>` and an edge authentication adapter produces immutable `AuthContext {subject_id, tenant_id, scopes, credential_id, auth_time}`. Token format, issuer, client flow, optional mTLS, and IdP remain unresolved. Polling is universal; registered signed webhook is conditional; SSE/public event feed is absent. Legacy coexistence uses bounded adapters and creates no new cross-writes.

Each portion expires on the first applicable event: named adapter ownership or authoritative consumer constraint; Stage 12 trust-protocol decision or external enablement; approved release delivery contract; or Stage 16 cutover plan. `INT-04` remains insight-only/no-unapproved-workflow until a concrete grant/workflow is approved. Named staffing remains blocked under `A-04-OWNERSHIP`.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| One schema-free execute API | Small route count | Hides operation schemas, authority, limits, compatibility, and eligibility | Rejected | Never without bounded registered operation schemas—in which case it becomes the selected typed strategy |
| Separate API/service per capability | Independent network evolution | Duplicates auth, lifecycle, errors, jobs, delivery, operations, and service ownership without evidence | Rejected now | ADR-003 extraction gate for a specific module |
| Common namespace + typed operation schemas + universal jobs | Common lifecycle with capability ownership and versioning | Requires shared contract governance | Selected | Reassess only on measured/extraction evidence |
| General workflow/DAG API | Flexible composition | Exposes private orchestration and adds safety/state/engine burden without a named need | Rejected | A concrete approved workflow cannot be expressed as named public jobs |
| Polling only | Simplest reliable retrieval | Less convenient for consumers | Required baseline | Registered webhook added per approved consumer delivery contract |
| Webhook/public event/SSE as universal completion | Push UX | Delivery failure, dedupe, signing, ordering, connection, and recovery burden | Rejected as baseline | Measured consumer requirement with polling retained as recovery |
| Select a concrete IdP/token/mTLS product now | Fully specific trust stack | No environment/provider evidence; premature vendor/protocol commitment | Rejected | Stage 12/15 authoritative evidence |
| `A-07-INTEGRATION` temporary disposition | Allows the API contract to be approved while preserving explicit blocks/expiries | Requires later replacement and prevents external production enablement today | Selected temporarily | Each stated expiry |

## Rationale

The selected combination is the smallest contract that satisfies the common operational envelope, independent capability schemas, durable jobs, data-reference rules, and tenant/security boundaries. It avoids both extremes: a generic router that erases capability contracts and a distributed API estate that duplicates lifecycle and operations.

`A-07-INTEGRATION` is deliberately narrower than carrying `A-01-INT` forward. It settles the logical boundary and default delivery behavior required by Stage 07 while keeping missing organization, trust, consumer, and cutover evidence visible and time-bounded.

## Consequences and trade-offs

- Consumers integrate once with common authentication, errors, idempotency, correlation, pagination, jobs, results, and callback conventions.
- Each capability still owns its operation schemas, scientific eligibility, and result meaning.
- Contract governance, schema compatibility tests, and definition-policy completeness become required engineering work.
- Async clients must poll; webhooks are optional delivery conveniences and require later security/reliability policy.
- No endpoint can be externally enabled until concrete limits/rates/timeouts and the authoritative trust protocol are approved.
- Consumer/platform teams carry translation by default; insufficient staffing remains an operating blocker rather than a reason to couple the core.
- Legacy/Synapse compatibility lives in bounded adapters and may create temporary maintenance burden, but not new core cross-writes.

## Implementation constraints

- API major in path; exact capability/operation/schema versions immutable and independently recorded.
- Public HTTP controllers call only typed module application ports; no shared-table/private-method integration.
- Bearer presentation under `A-07-INTEGRATION` is a temporary boundary, not a token-format/IdP choice.
- All non-health public endpoints authenticate; owner modules enforce semantic authorization again at their public ports.
- No public tenant-authority header/body field and no caller-selected object path/callback URL.
- Side-effecting POST/PUT/PATCH commands require idempotency; safe reads do not.
- Transport errors use the stable problem schema; job execution, dataset readiness, capability outcome, and delivery state remain separate.
- Large values use tenant-scoped opaque references. API errors/events/logs contain no raw PII, secrets, or hidden paths.
- Callback activation requires Stage 12/13 signature, replay, destination, timeout, and retry controls.
- Public job wire states remain coarse; Stage 08 owns internal state/transitions/leases/retries/cancellation.
- No gateway product, per-capability service, ESB, GraphQL/gRPC requirement, service registry, broker, SSE, or workflow engine follows from this ADR.

## Validation evidence

- `outputs/stages/07-api-integration.md` maps every governing prompt bullet.
- The endpoint matrix records authentication, authorization, tenant source, timeout/limits, idempotency/concurrency, and error behavior for every endpoint class.
- Concrete examples cover operation submission/result, ingestion/upload, jobs, errors, pagination, and callback events.
- Independent read-only `platform_architect` review found the design passable only with the explicit `A-01-INT` replacement; `A-07-INTEGRATION` incorporates that finding.
- Required tests include schema/compatibility, replay/conflict, cross-tenant concealment, timeout ambiguity, 413-to-upload, job/result truth, callback dedupe/signature, and adapter-boundary checks.

## Reconsideration trigger

- Any `A-07-INTEGRATION` expiry.
- Authoritative consumer ownership/delivery/trust/cutover evidence.
- A named workflow/grant approved in Stages 08/09.
- Measured need for SSE/public event delivery or a different protocol.
- A module satisfies ADR-003's service-extraction gate.
- New Synapse evidence conflicts with the adapter treatment.

## Supersedes / superseded by

This ADR replaces `A-01-INT` only for its Stage 07 integration-boundary disposition. It does not supersede ADR-000 through ADR-003 or the unrelated portions of ADR-001. Superseded by: none.
