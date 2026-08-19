# Stage 07 — API and integration design

Status: `APPROVED`

## Purpose and scope

Define implementable external HTTP contracts and internal module ports for capability discovery/invocation, ingestion, durable jobs, datasets/results, control administration, optional callbacks, and named workflows. The design preserves the approved platform-neutral modular-monolith boundaries, the Stage 06 data/reference contracts, and the separation between transport acceptance, dataset readiness, platform eligibility, capability outcome, job execution, and notification delivery.

This stage defines logical HTTP behavior and schemas. It does not select an identity provider, token format, gateway product, network topology, signing algorithm, numeric workload/SLO target, job lease/retry state machine, event broker, or named workflow. Those decisions remain with Stages 08, 09, 12, 13, 15, and 17.

The sponsor explicitly approved Stage 06 and its outputs on 2026-08-11. Per the sponsor's instruction, Stage 07 stops after its completion gate for approval before Stage 08.

## Inputs read in full

- `AGENTS.md` — all sections
- `WORKFLOW.md` — all sections
- `STATUS.md` — all sections after recording Stage 06 approval
- `SOURCE_MANIFEST.md` — all sections
- `stages/STAGE-CONTRACT.md` — all sections
- `stages/07-api-integration.md` — all sections
- `templates/stage-output.md` — all sections
- `templates/adr.md` — all sections
- `templates/service-contract.md` — all sections
- `sources/normalized/system-design-prompt.md` — **6. API and integration design** exactly
- `sources/normalized/ark-assumptions.md` — all sections
- `outputs/stages/02-system-definition.md` through `outputs/stages/06-data-architecture.md` — all sections after their approvals were recorded
- `outputs/stages/01-discovery-and-questions.md` — `A-01-INT` and `INT-01` through `INT-05`
- `decisions/ADR-000-temporary-source-evidence-disposition.md` through `decisions/ADR-003-architecture-style.md` — all sections

The Stage 07-authorized `platform_architect` completed a bounded, read-only contract-boundary review of endpoint coverage, the combined consumer surface, schemas, cross-cutting semantics, adapter boundaries, Synapse restrictions, anti-overengineering, and the gate. The primary agent reconciled its findings, especially the complete `A-01-INT` disposition, and remains the sole writer.

## Source-instruction coverage

| Governing requirement | Addressed in | Status/evidence |
|---|---|---|
| External APIs | External resource/operation surface; endpoint contract matrix | Addressed |
| Internal module/service contracts | Internal application-port contracts | Addressed without introducing network services |
| Endpoint responsibilities | Endpoint contract matrix | Addressed with owner/non-responsibility |
| Request/response examples | Concrete JSON examples | Capability, ingestion, job, result, error, and callback examples supplied |
| Synchronous vs asynchronous patterns | Invocation mode policy | Addressed; sync is opt-in by definition/measurement |
| Job submission and status APIs | Job contract | Addressed with 202, polling, cancellation, result retrieval |
| Pagination | Cursor-pagination contract | Addressed |
| Idempotency keys | Idempotency contract | Precise scope, replay, conflict, and timeout-ambiguity behavior |
| Correlation IDs | Request/correlation contract | Precise generation, propagation, and response behavior |
| Error model | Problem schema and code mapping | Addressed; transport/execution/capability outcomes remain separate |
| API versioning | Version and compatibility policy | Addressed for API, operation, dataset, capability, and event versions |
| Rate limiting | Admission/rate-limit contract | Addressed without inventing numeric rates |
| Timeout behavior | Timeout contract | Addressed for sync, submission, polling, dependencies, and callbacks |
| Webhook/event contracts | Callback registration and event envelope | External webhook concrete; internal event publication remains Stage 09-conditional |
| Authentication/authorization | Trust contract and endpoint matrix | Auth scheme presentation concrete; provider/token validation deferred under accepted `A-07-INTEGRATION` |
| Tenant propagation | Principal-derived tenant contract | Request body/header tenant authority prohibited |
| Unified vs separate vs workflow API | API strategy decision | Combination selected and bounded |
| Example schemas, not names only | Schema and examples sections | Addressed |

## Facts

1. Every capability request shares an operational envelope/lifecycle while inputs, options, and outputs remain capability-specific. `sources/normalized/ark-assumptions.md — Integration and contracts`.
2. Every capability publishes a machine-readable definition of operations, inputs, outputs, modes, dependencies, thresholds, and fallbacks. `sources/normalized/ark-assumptions.md — Integration and contracts`; `outputs/stages/02-system-definition.md — ARK-FR-004`.
3. The edge handles authentication, routing, throttling, API versions, request-size limits, and request IDs, but not normalization, scientific eligibility, or workflow logic. `sources/normalized/ark-assumptions.md — Integration and contracts`.
4. Tenant identity comes from the authenticated principal and cannot be supplied authoritatively in a body/query/header field. `sources/normalized/ark-assumptions.md — Security, ownership, and operations`; `outputs/stages/06-data-architecture.md — Tenant and access-isolation rules`.
5. Synchronous execution is limited to short, predictable operations. Ingestion, training, backfills, large/batch inference, scheduled work, and retryable work use the shared durable job lifecycle. `sources/normalized/ark-assumptions.md — Execution, orchestration, and proactive operation`.
6. Polling is the required universal async result path; signed webhook is useful soon; SSE and a broker/event backbone are not justified. `outputs/stages/05-end-to-end-architecture.md — C05-12`, `— Conditional and rejected expected components`.
7. Large request inputs/results/artifacts move through tenant-scoped opaque references; PostgreSQL stores bounded operational metadata. `outputs/stages/06-data-architecture.md — Data boundaries and invariants`, `— Zone and authoritative-writer matrix`.
8. Churn, RFM, NPT, and REC target durable typed operations but retain unresolved exact scientific schemas; Synapse exposes only documented legacy HTTP interface facts and remains non-production-eligible. `outputs/stages/03-capability-inventory.md — Capability contracts`; `decisions/ADR-002-stage-03-capability-evidence-disposition.md — Decision`.

## Assumptions

| ID | Assumption | Why needed | Architectural effect | Risk | Validation/expiry |
|---|---|---|---|---|---|
| `A-07-INTEGRATION` (accepted) | Consumer/platform-side adapters remain the default owners of consumer-specific translation; ARK owns the platform-neutral API, schemas, conformance support, and technical/provider adapters. External callers present `Authorization: Bearer <access-token>` and the edge produces immutable `AuthContext {subject_id, tenant_id, scopes, credential_id, auth_time}`, while token format, issuer, client flow, optional mTLS, and IdP remain unresolved. Polling is universal; registered signed webhook is conditional; SSE/public event feed is absent. Legacy coexistence uses bounded adapters and creates no new cross-writes. | `A-01-INT` reaches its Stage 07 dispositions while named owners, consumer delivery constraints, trust protocol, and cutover inventory are absent | Resolves the logical adapter/API/delivery boundary and makes HTTP trust behavior implementable without inventing teams, a vendor, or migration schedule | Consumer environments may require different ownership, credentials, delivery, or coexistence | Sponsor approved Stage 07 and its outputs on 2026-08-11; each portion expires on named ownership/consumer constraint, Stage 12 trust decision, approved release delivery contract, or Stage 16 cutover plan—whichever applies first |
| `A-01-SCALE` | Numeric throughput, latency, request size, page size, rate, and availability targets remain unknown | Controller prohibits invented targets | Every active operation must publish concrete limit/timeout/rate policy values before enablement; Stage 07 defines behavior, not numbers | Production profiles cannot be activated yet | Measured S-01 through S-04 |
| `A-01-SEC` | Least privilege, authenticated tenant binding, minimal PII, auditable grants, and policy-before-action remain mandatory | Exact security/policy regime is absent | Fail closed; verifier output never authorizes action; callback destinations are registered | Later policy may be stricter | SEC-01 through SEC-06 / Stage 12 |
| `A-03-ML-MIGRATION` | Prototype APIs are migration evidence, not target contracts | Prevents defective schemas/lifecycle from becoming public compatibility obligations | Typed target operations use neutral schemas; legacy translation stays in adapters | Compatibility/cutover work remains | Per capability Stage 10/16 |
| `A-03-SYNAPSE` | Synapse is interface-only and non-production-eligible | Provider/state/security internals are absent | Legacy paths are adapter targets only; ARK exposes no production Synapse operation until evidence arrives | Capability may be scoped out or redesigned | Relevant Stage 10/12/14/15 or enablement decision |
| `A-04-OWNERSHIP` | Logical integration/platform/capability owner roles suffice; named people remain TBD | Allows contract ownership without inventing teams | Every schema/endpoint has a logical owner; production/extraction remains blocked | Operating capacity unknown | Existing expiry |

`A-07-INTEGRATION` replaces `A-01-INT` only for its Stage 07 integration-boundary treatment. It resolves `INT-01` and `INT-03` architecturally, dispositions `INT-02` until Stage 12, retains `INT-04`'s no-unapproved-workflow rule, and carries `INT-05` only to its Stage 16 cutover decision. Named staffing remains blocked under `A-04-OWNERSHIP`.

## Analysis and recommendations

### R-07-01 — Use a combined API strategy

Consumers use one platform API namespace and lifecycle, typed capability operations inside that namespace, one common ingestion/job/dataset/result surface, and a workflow API only for a named approved workflow.

| Option | Disposition | Reason |
|---|---|---|
| One unbounded generic `execute` endpoint | Rejected | Hides capability schemas, eligibility, limits, ownership, and evolution |
| Separate network API/service per capability | Rejected now | Capability count does not justify distributed endpoints/operations |
| Shared namespace with typed capability/version/operation resources | Selected | Preserves a common envelope/lifecycle and capability-owned schemas |
| Universal job/status/result API | Selected | One durable lifecycle is authoritative across ingestion/capabilities/workflows |
| Caller-programmable workflow/DAG API | Rejected | No named complexity or safe arbitrary-composition requirement |
| Named versioned workflow submit API | Conditional/useful soon | Activate only after Stage 08/09 defines an approved workflow/grant |

**Requirement/where:** `ARK-FR-004`–`008`, `ARK-NFR-003/004`, `ARK-CON-001/002/007`; consumer invocation and Stages 07–09. **Why now:** capability independence must not fragment lifecycle or create a schema-less router. **Simplest implementation:** controllers in the modular monolith route validated operation DTOs to public module ports. **Trade-off:** shared HTTP conventions require governance, but capability schemas remain independently versioned. **Reconsideration:** independent API deployment only through ADR-003 extraction evidence; workflow API only on a named release workflow.

### External resource and operation surface

All paths use an API major version. Resource IDs are opaque and tenant-scoped. Path IDs never establish authorization.

| Surface | Endpoint | Responsibility / non-responsibility |
|---|---|---|
| Discovery | `GET /v1/capabilities` | List caller-entitled capability summaries; not a dynamic network service registry |
| Definition | `GET /v1/capabilities/{capability_id}/versions/{capability_version}` | Return immutable operation/schema/mode/dependency/limit metadata |
| Sync operation | `POST /v1/capabilities/{capability_id}/versions/{capability_version}/operations/{operation_id}:invoke` | Execute only a definition-declared synchronous operation; never promote an unqualified operation to sync |
| Async operation | `POST /v1/capabilities/{capability_id}/versions/{capability_version}/operations/{operation_id}:submit` | Admit one durable job using capability-specific input and common references |
| Inline ingestion | `POST /v1/data/ingestions` | Register bounded small push/micro-batch data and create/replay an ingestion job |
| Bulk upload registration | `POST /v1/data/uploads` | Issue a scoped upload authority/reference; bytes do not pass through the operational API |
| Bulk upload commit | `POST /v1/data/uploads/{upload_id}:commit` | Verify uploaded object metadata/checksum and create/replay ingestion job |
| Ingestion status | `GET /v1/data/ingestions/{ingestion_id}` | Return ingestion resource and job/dataset references; not raw content |
| Dataset version | `GET /v1/datasets/{dataset_id}/versions/{dataset_version}` | Return readiness, reasons, schema/quality/lineage references |
| Job status | `GET /v1/jobs/{job_id}` | Return stable public lifecycle and progress/result/error references |
| Job cancel | `POST /v1/jobs/{job_id}:cancel` | Record an idempotent cancellation request; does not promise immediate termination |
| Job result | `GET /v1/jobs/{job_id}/result` | Return bounded result or tenant-scoped object reference after result commit |
| Subscription/config | `GET /v1/subscriptions`, `PUT /v1/subscriptions/{capability_id}` | Read/update tenant capability enablement only; never ingest or execute |
| Callback registration | `POST /v1/webhook-endpoints`, `PATCH /v1/webhook-endpoints/{endpoint_id}` | Register/disable an authorized destination; submissions reference ID, never arbitrary URL |
| Named workflow | `POST /v1/workflows/{workflow_id}/versions/{workflow_version}:submit` | Conditional named composition of public operations/jobs; no generic DAG/private calls |

Administrative evidence/export surfaces use the same conventions but remain release-scoped. Grant/policy APIs and event-subscription detail belong to Stage 09/12; their absence does not authorize proactive action.

### Common headers and operational envelope

#### Request headers

| Header | Rule |
|---|---|
| `Authorization` | Required on every non-health public endpoint; `Bearer` presentation under accepted `A-07-INTEGRATION`; failure is 401, insufficient permission is 403 |
| `Idempotency-Key` | Required on every mutation, durable submission, upload registration/commit, cancellation, and callback/subscription change; forbidden as a substitute for resource/version preconditions |
| `X-Correlation-ID` | Optional caller-supplied opaque trace token satisfying the published bound; ARK generates one when absent and echoes it |
| `If-Match` | Required for replace/update of versioned mutable control resources such as subscription or callback configuration; value is prior ETag |
| `Content-Type` | `application/json` for JSON contracts; object bytes use the scoped upload mechanism |
| `traceparent` | Optional standards-compatible technical trace context; never tenant authority |

ARK returns `X-Request-ID` for the individual HTTP attempt and `X-Correlation-ID` for the logical trace. Request ID changes on a retry; correlation ID may be retained; idempotency controls logical side effects. No public `X-Tenant-ID` header exists. Any body `businessId`, `tenantId`, phone, or customer ID is capability/source data only and must match authorized scope where retained for legacy compatibility.

#### Operation request schema

```json
{
  "request_version": "1.0",
  "dataset_refs": [
    {
      "dataset_id": "ds_opaque",
      "dataset_version": "dv_immutable",
      "purpose": "inference"
    }
  ],
  "configuration_ref": {
    "configuration_id": "cfg_opaque",
    "configuration_version": "cv_immutable"
  },
  "callback": {
    "webhook_endpoint_id": "wh_opaque",
    "event_types": ["ark.job.completed.v1"]
  },
  "input": {}
}
```

`input` is validated by the exact capability/version/operation schema. Fields not used by an operation are omitted, not accepted as generic extension bags. `dataset_refs`, `configuration_ref`, and `callback` are present only where the operation definition permits them. Tenant/caller/idempotency/correlation are server context, not body authority.

#### Standard synchronous response

```json
{
  "request_id": "req_opaque",
  "correlation_id": "corr_opaque",
  "capability_id": "CAP-EXAMPLE",
  "capability_version": "1.0",
  "operation_id": "example-operation",
  "outcome": {
    "status": "ELIGIBLE",
    "reason_code": "COMPLETED",
    "message": "Operation completed"
  },
  "result": {},
  "lineage_ref": "lin_opaque",
  "usage_ref": "usage_opaque"
}
```

`outcome.status` is one of `ELIGIBLE | DEGRADED | FALLBACK | INELIGIBLE`; transport/execution failure uses the problem schema. A verifier's advisory `accepted` may appear only inside a capability result and never in platform authorization.

### Concrete capability example — recommendation batch submission

```http
POST /v1/capabilities/CAP-REC/versions/1.0/operations/recommendation-generate-batch:submit
Authorization: Bearer <access-token>
Idempotency-Key: rec-run-2026-08-11-a
X-Correlation-ID: consumer-trace-opaque
Content-Type: application/json
```

```json
{
  "request_version": "1.0",
  "dataset_refs": [
    {"dataset_id": "transactions", "dataset_version": "dv_tx_opaque", "purpose": "inference"},
    {"dataset_id": "catalog", "dataset_version": "dv_cat_opaque", "purpose": "inference"},
    {"dataset_id": "inventory", "dataset_version": "dv_inv_opaque", "purpose": "inference"}
  ],
  "configuration_ref": {
    "configuration_id": "rec-policy",
    "configuration_version": "cv_rec_opaque"
  },
  "input": {
    "as_of": "2026-08-11T00:00:00Z",
    "audience_ref": "aud_opaque",
    "requested_result_schema": "rec-ranked-items/1.0"
  }
}
```

```http
HTTP/1.1 202 Accepted
Location: /v1/jobs/job_opaque
X-Request-ID: req_opaque
X-Correlation-ID: consumer-trace-opaque
```

```json
{
  "job_id": "job_opaque",
  "job_type": "capability-operation",
  "state": "ACCEPTED",
  "capability": {"id": "CAP-REC", "version": "1.0", "operation_id": "recommendation-generate-batch"},
  "submitted_at": "2026-08-11T00:00:01Z",
  "status_url": "/v1/jobs/job_opaque",
  "result_url": "/v1/jobs/job_opaque/result",
  "correlation_id": "consumer-trace-opaque"
}
```

Exact REC feature/ranking schemas and numeric `top_k` bounds remain capability-owned/unresolved under `A-03-ML-MIGRATION`; the example is concrete at the approved contract/reference boundary and does not approve a scientific schema.

### Job contract

The public job state vocabulary is deliberately coarser than the internal Stage 08 state machine:

`ACCEPTED | RUNNING | SUCCEEDED | FAILED | CANCELLATION_REQUESTED | CANCELLED`

Stage 08 may add internal claim/wait/retry phases but must map them without breaking these meanings. `SUCCEEDED` means the authoritative result/outcome commit exists; it does not mean capability outcome `ELIGIBLE`. A job may succeed with a truthful `INELIGIBLE`, `DEGRADED`, or `FALLBACK` capability outcome. `FAILED` is execution/lifecycle failure. Notification delivery has a separate state.

```json
{
  "job_id": "job_opaque",
  "job_type": "capability-operation",
  "state": "RUNNING",
  "phase": "capability-defined-public-phase",
  "progress": {"completed_units": null, "total_units": null, "message": "Progress estimate unavailable"},
  "attempt_summary": {"attempts_started": 1},
  "submitted_at": "2026-08-11T00:00:01Z",
  "started_at": "2026-08-11T00:00:03Z",
  "finished_at": null,
  "outcome": null,
  "result_ref": null,
  "error": null,
  "links": {
    "self": "/v1/jobs/job_opaque",
    "result": "/v1/jobs/job_opaque/result",
    "cancel": "/v1/jobs/job_opaque:cancel"
  },
  "correlation_id": "consumer-trace-opaque"
}
```

Unknown progress remains `null`; it is never fabricated. `POST :cancel` returns `202` with `CANCELLATION_REQUESTED`, `200` with the existing terminal resource on idempotent replay, or `409 JOB_NOT_CANCELLABLE` when the operation has no safe cancellation contract. Client disconnect never means cancellation.

### Ingestion/upload example

```json
{
  "source_id": "src_opaque",
  "source_contract": {"id": "transactions", "version": "1.0"},
  "content": {
    "media_type": "application/x-ndjson",
    "content_length": 12345,
    "checksum": {"algorithm": "SHA-256", "value": "checksum-value"}
  },
  "purpose": "initial-load"
}
```

`POST /v1/data/uploads` returns `201` with `upload_id`, an opaque scoped `upload_ref`, upload instructions, expiry metadata supplied by the configured policy, and `commit_url`. `POST /v1/data/uploads/{id}:commit` repeats the declared checksum/length, requires the same logical idempotency key family, verifies ownership/object integrity, and returns `202` with `ingestion_id` and `job_id`. It never accepts a caller-chosen arbitrary object path as authority.

### Endpoint contract matrix

`Auth` below means valid `AuthContext` under `A-07-INTEGRATION`. All tenant resources derive tenant from that context and conceal cross-tenant existence. Every endpoint enforces its machine-readable `limit_policy_ref`, `rate_policy_ref`, and, where applicable, `timeout_policy_ref`; an operation cannot be enabled until those policies contain concrete values.

| Endpoint class | Authentication / authorization | Tenant source | Timeout and limit behavior | Idempotency/concurrency | Principal errors |
|---|---|---|---|---|---|
| Capability list/definition `GET` | Auth; discovery/read entitlement | AuthContext | Bounded page/definition policy; ordinary read timeout | Safe GET; ETag/If-None-Match supported | 401/403; 404 concealed; 429; 503 |
| Sync `:invoke` | Auth; subscribed operation scope, quota, active versions | AuthContext | Definition must declare sync and concrete server timeout/size/rate policy; otherwise 409 `OPERATION_REQUIRES_ASYNC`; timeout never becomes an implicit job | Idempotency required if any metered/result side effect; same key/hash replays result | 400/401/403/404/409/413/415/422/429/504 |
| Async `:submit` / workflow submit | Auth; operation/workflow scope, quota/grant where applicable | AuthContext | Short admission timeout only; computation is outside HTTP lifetime; large input by ref | Required key; atomic create/replay; same key different canonical hash → 409 | 400/401/403/404/409/413/415/422/429/503 |
| Inline ingestion `POST` | Auth; source/contract/write entitlement | AuthContext | Inline size bound from source-contract policy; exceeding it → 413 plus upload-registration link | Required; same source/key/hash returns same ingestion/job | 400/401/403/404/409/413/415/422/429/503 |
| Upload register/commit `POST` | Auth; source/object write scope | AuthContext | Registration/commit timeout; bytes uploaded separately; expiry policy explicit | Required; commit verifies ETag/checksum/length; conflicting replay 409 | 400/401/403/404/409/410/413/422/429/503 |
| Ingestion/dataset/job/result `GET` | Auth; resource read scope and entitlement | AuthContext + resource binding | Bounded metadata/result read; large result returns reference; object-access expiry explicit | Safe GET; ETag supported | 401/403/404/409(result not ready)/410/429/503 |
| Job `:cancel` | Auth; submitter or cancellation scope; operation supports cancel | AuthContext + job binding | Short command timeout; cancellation is cooperative | Required; repeated request returns same logical state | 401/403/404/409/429/503 |
| Subscription/config `PUT` | Auth; tenant administration scope | AuthContext | Bounded admin timeout/body policy | Required plus `If-Match`; stale ETag → 412 | 400/401/403/404/409/412/422/429/503 |
| Webhook endpoint `POST/PATCH` | Auth; integration administration scope | AuthContext | Destination validation/secret provisioning policy; no per-job raw URL | Required; PATCH requires `If-Match` | 400/401/403/404/409/412/422/429/503 |

`422` means the JSON is structurally valid but violates declared semantic/admission constraints. Dataset `NOT_READY/STALE/REVOKED`, platform ineligibility, and scientific outcomes use explicit codes/objects; the same fact must not appear sometimes as transport success and sometimes as an unrelated HTTP error. The operation definition declares whether admission rejects before a job or the capability returns an outcome during execution.

### Idempotency contract

1. Scope is `{tenant_id, authenticated caller/application, API major, endpoint operation, logical target, Idempotency-Key}`.
2. ARK stores the key, canonical request hash excluding transport-only headers, created resource/result reference, outcome/status, and retention expiry under the authoritative owner.
3. First accepted request performs one logical mutation. An identical replay returns the same resource identity and semantically equivalent response; it does not consume quota/cost twice.
4. Same key with a different canonical hash returns `409 IDEMPOTENCY_KEY_REUSED` and performs no new work.
5. A request that fails before durable acceptance may be retried with the same key. If the client times out ambiguously, it must retry the same key; the server resolves accepted versus not accepted.
6. Idempotency retention durations are policy values and cannot be shorter than the published client retry/reconciliation window. Exact durations remain Stage 13/production inputs.
7. Source record/event IDs, object checksums, callback `event_id`, and job attempt IDs are separate dedupe identities; none replaces request idempotency.

### Correlation and propagation contract

- `X-Request-ID` identifies one HTTP attempt and is always server-generated.
- `X-Correlation-ID` identifies the consumer-visible logical trace. ARK validates a caller value against the published character/length bound or generates one.
- Job, ingestion, dataset publication, capability execution, result, webhook delivery, audit, lineage, usage, and technical trace records carry the correlation value plus their own authoritative IDs.
- Internal ports receive a trusted `OperationContext`, never raw headers. Child jobs inherit correlation and add parent/child causation IDs. They inherit or narrow tenant/authorization scope, never broaden it.
- Correlation/idempotency keys contain no PII, secrets, or tenant authority.

### Cursor-pagination contract

List endpoints accept `page_size`, opaque `cursor`, stable documented filters, and one documented sort. The server applies the endpoint's configured default/maximum page size; invalid sizes or cursors return 400. Response:

```json
{
  "items": [],
  "page": {
    "next_cursor": "opaque-or-null",
    "has_more": false
  },
  "links": {"self": "/v1/capabilities", "next": null}
}
```

The signed/opaque cursor binds tenant, caller authorization view, API/schema version, filters, sort, and snapshot/position. Clients cannot edit it or use it cross-tenant. Offset pagination is not used for mutable large collections. Cursor lifetime is published per endpoint; expiry yields `400 CURSOR_EXPIRED`, allowing restart from the first page.

### Error model

Errors use `application/problem+json`:

```json
{
  "type": "urn:ark:problem:idempotency-key-reused",
  "title": "Idempotency key conflict",
  "status": 409,
  "code": "IDEMPOTENCY_KEY_REUSED",
  "detail": "The key was previously used for a different request.",
  "instance": "/v1/jobs/job_opaque",
  "request_id": "req_opaque",
  "correlation_id": "corr_opaque",
  "retryable": false,
  "field_errors": []
}
```

| HTTP | Stable use |
|---:|---|
| 400 | Malformed JSON, unknown field where schema forbids it, invalid cursor/header syntax |
| 401 | Missing/invalid/expired authentication |
| 403 | Authenticated principal lacks permitted action; no cross-tenant metadata leaked |
| 404 | Resource/operation/version absent or concealed from caller |
| 409 | Idempotency conflict, illegal resource/job state, result not yet committed, operation requires async |
| 410 | Expired/revoked upload or result reference where disclosure is safe |
| 412 | Failed ETag/version precondition |
| 413 | Request exceeds declared inline policy; use referenced upload where applicable |
| 415 | Unsupported media type |
| 422 | Structurally valid request violates declared semantic/admission constraint |
| 429 | Edge rate policy exceeded; `Retry-After` when known; no job/side effect created |
| 500 | Unexpected ARK failure with no sensitive detail |
| 503 | Required control/job/storage dependency unavailable; acceptance not fabricated |
| 504 | Declared synchronous/dependency deadline exceeded; never silently converted to async |

`detail` and `field_errors` never expose secrets, raw payloads, hidden Synapse internals, other tenants, stack traces, or sensitive object paths. Error codes are additive within API major only when clients treat unknown codes as the documented category; changed meaning requires a new major.

### Versioning and compatibility

- API major is in the path (`/v1`). Incompatible resource/envelope/error behavior requires `/v2`; supported majors may coexist during an approved migration window.
- Capability ID, capability contract version, and operation ID are explicit in the path. A capability version never changes schema/meaning in place.
- Request/response schemas are registered immutable references. Additive optional fields may be introduced only when existing clients are required to ignore unknown response fields; new required fields or semantic changes require a new capability/API version.
- Dataset/config/model/code/execution versions remain independent references; the API does not collapse them into an API version.
- Deprecation is machine-readable in capability definitions with status, replacement, and sunset policy. No sunset date is invented before a release/cutover plan.
- Mutable control resources use ETag/`If-Match`. Immutable datasets/results/artifacts use exact IDs/versions and do not accept updates.
- Internal ports version DTO/schema packages and preserve the same ownership/compatibility rules even when invoked in process.

### Rate limits, quotas, and timeouts

- Edge rate limiting protects infrastructure and is keyed by authenticated application/tenant/operation; entitlement/business quota remains authoritative in the control module. A rate limiter cannot grant entitlement or consume/reconcile business quota by itself.
- Every enabled endpoint/operation definition must supply concrete `max_request_bytes`, inline collection/string bounds, result mode/inline-result bound, page-size policy, rate policy, and timeout policy. Missing values block activation. Stage 17 supplies measured targets rather than Stage 07 inventing them.
- Rate rejection occurs before job creation and returns 429. Quota/entitlement rejection returns a distinct stable control code, normally 403 or 422 according to disclosure/admission contract.
- Synchronous server deadline is operation-defined and measurable; client disconnect never starts a durable job or changes a committed result. Long/retryable work must use 202 jobs.
- Async submission timeout covers admission only. After 202, work has its own durable deadlines/retries in Stage 08/13. An ambiguous submit timeout is resolved by repeating the same idempotency key.
- Polling GET has ordinary read deadlines and may return `Retry-After`/recommended poll metadata. Webhook connect/response deadlines and retry schedule are delivery-policy values for Stages 09/13.

### Callback/webhook contract

Submissions reference a pre-registered, authorized `webhook_endpoint_id`. ARK never accepts an arbitrary callback URL in a capability request. External notifications are at-least-once delivery conveniences; polling remains authoritative recovery.

```http
POST <registered consumer endpoint>
Content-Type: application/json
X-ARK-Event-ID: evt_opaque
X-ARK-Delivery-ID: delivery_opaque
X-ARK-Timestamp: 2026-08-11T00:05:00Z
X-ARK-Signature: <versioned-signature>
```

```json
{
  "event_version": "1.0",
  "event_id": "evt_opaque",
  "event_type": "ark.job.completed.v1",
  "occurred_at": "2026-08-11T00:04:59Z",
  "tenant_ref": "tenant_opaque",
  "subject": {"type": "job", "id": "job_opaque"},
  "correlation_id": "corr_opaque",
  "data": {
    "job_state": "SUCCEEDED",
    "capability_outcome": "ELIGIBLE",
    "status_url": "/v1/jobs/job_opaque",
    "result_url": "/v1/jobs/job_opaque/result"
  }
}
```

- A 2xx response acknowledges that delivery attempt; non-2xx/timeout follows bounded Stage 09/13 retry policy. The capability job/result is never rerun or changed by delivery failure.
- Consumers deduplicate by `event_id`; `delivery_id` distinguishes attempts. Ordering is not guaranteed unless an event type explicitly adds an ordering contract.
- Signature algorithm, secret rotation, replay window, destination verification, SSRF/network rules, and retry schedule remain Stage 12/13 decisions, but absence blocks callback activation.
- Event schemas are immutable/versioned and minimal. External payloads carry references rather than large results/PII.
- Internal event publication is not selected here. If Stage 09 justifies it, the internal event uses a separate contract and reliable publication; a webhook is never reused as internal coordination.

### Internal application-port contracts

Internal interactions are typed in-process module ports in the approved modular monolith unless later extraction passes ADR-003. They are not shared-table calls and do not require internal HTTP.

| Port | Request → response | Authority / forbidden behavior |
|---|---|---|
| `AuthenticateCredential` | Raw credential metadata → `AuthContext` or denial | Security adapter validates; body tenant cannot influence result |
| `EvaluateControl` | `OperationContext + capability/operation + refs + requested units` → allow/deny/reservation + policy/config versions | Control module authoritative; edge cannot substitute |
| `ResolveDatasetReadiness` | Tenant + exact dataset/version/purpose → readiness/reasons/lineage | Dataset catalog authoritative; no scientific decision |
| `EvaluateCapabilityEligibility` | Trusted context + exact input/dataset/artifact/config refs → eligible/degraded/fallback/ineligible | Capability authoritative; cannot grant platform permission |
| `InvokeCapability` | Trusted context + typed operation DTO → bounded outcome/result/ref | Public capability port only; no private cross-capability import |
| `SubmitJob` | Trusted context + typed job command + idempotency identity → job resource | Job manager authoritative for lifecycle; capability owns computation |
| `GetJob/RequestCancellation` | Tenant-bound job query/command → public job representation | Job manager; cancellation remains cooperative |
| `RegisterRaw/PublishDataset` | Source/object evidence → ingestion/job; validated candidate → immutable catalog version | Ingestion/catalog writers only; no raw capability bypass |
| `CommitCapabilityResult` | Job/execution + exact lineage + outcome + bounded result/ref → immutable result identity | Capability result owner; no terminal success before commit |
| `AppendAudit/Usage` | Actor/action/target/versions/reason/correlation → evidence ID | Audit/usage writer; does not become business authority |
| `CreateNotificationIntent` | Committed subject/result + registered endpoint/event type → delivery ID | Integration delivery owner; failure does not change subject |

Every port receives trusted `OperationContext`:

```text
OperationContext {
  request_id, correlation_id,
  auth: {subject_id, tenant_id, scopes, credential_id, auth_time},
  api_major, capability_id?, capability_version?, operation_id?,
  idempotency_identity?, deadline?, causation_id?, parent_job_id?
}
```

Modules may narrow this context for child work; they may not replace tenant/caller authority or query another module's private store.

### Adapter placement and platform neutrality

1. Direct, Whatson, POS, LAB, and future consumer-specific anti-corruption adapters sit outside capability cores. Their logical owner is the consuming-platform integration role; exact named team remains unresolved under `A-04-OWNERSHIP`.
2. An adapter maps consumer credentials/protocols/terminology and legacy identifiers into the canonical ARK API, bounded source/capability schemas, opaque IDs, and registered references. It maps ARK outcomes/errors back to consumer presentation without changing their meaning.
3. ARK owns the canonical OpenAPI/schema packages, compatibility rules, conformance suite, and optional generated SDKs. A consumer owns platform-specific mapping/configuration and its source-of-record semantics.
4. If ARK temporarily operates a consumer adapter during migration, it remains a separate integration module with a one-way dependency on public ARK contracts, no capability-private imports, no cross-writes, and its own decommission trigger. This does not move consumer schema into the core.
5. Legacy Synapse paths and current BCDP/Whatson shapes terminate in such adapters. Synapse response enums are mapped to advisory capability results only; body business/customer IDs are checked against trusted scope and never create tenant authority.

This resolves `INT-01` at the logical boundary and `INT-03` by selecting sync-or-job/polling/registered-webhook rules. `INT-05` cutover sequence remains for Stage 16/20 because consumer inventories and ownership are absent.

### Anti-overengineering findings

- No separate API gateway product is selected; the logical edge can be ordinary middleware/controllers.
- No API/service per capability; typed operation paths preserve ownership within one deployment/release.
- No unbounded generic execute endpoint, GraphQL layer, gRPC requirement, service registry, ESB, or shared canonical consumer object.
- Polling is the universal async contract; SSE/WebSocket is not included without an evidenced interactive requirement.
- Named workflow API is conditional; no general DAG/DSL/workflow product.
- Webhook delivery does not require an event broker. Internal events remain Stage 09 conditional.
- No external object URL, raw callback URL, hidden Synapse provider API, agent/MCP/A2A protocol, or API-key body tenant path is promoted into the ARK core.

## Decisions

- Accepted `ADR-004-api-contract-boundary.md`: one `/v1` platform namespace, typed capability/version/operation contracts, universal ingestion/job/dataset/result resources, conditional named workflow API, and consumer-platform adapters outside capability cores.
- Tenant is always derived from trusted `AuthContext`; there is no public tenant-authority header/body field.
- Polling is mandatory for durable work; registered signed webhook is optional; SSE and internal event publication are not baseline API dependencies.
- Public job states are stable coarse wire states; Stage 08 owns the complete internal state machine.
- Every operation must publish concrete bounds/rate/timeout policy before activation; this stage does not invent numeric production values.
- `A-07-INTEGRATION` was explicitly approved with the Stage 07 outputs because `A-01-INT` reached its Stage 07 disposition while named ownership, trust-protocol, delivery, and cutover evidence remain incomplete.
- No decision makes Synapse production-eligible or validates its undocumented internals.

## Contradictions and dangerous assumptions

| ID | Tension/hazard | Treatment | Consequence |
|---|---|---|---|
| `C-07-01` | A “unified API” can become an untyped generic execute router | Common namespace/lifecycle plus exact capability/version/operation schemas | Capability contracts/ownership remain visible |
| `C-07-02` | Separate capability modules can be misread as separate APIs/services | Typed paths route to in-process public ports; no independent deployment claim | Preserves ADR-003 |
| `C-07-03` | Current bodies contain `businessId`, phone, and customer IDs | AuthContext tenant is authoritative; legacy fields are data/compatibility only | Payload cannot cross tenant boundaries |
| `C-07-04` | Synapse uses API keys and `Agent` paths | Target trust/envelope wraps only documented interface facts; non-production eligibility retained | No hidden provider/agent/security inference |
| `C-07-05` | HTTP success, job success, dataset readiness, capability outcome, and webhook delivery can collapse into one status | Separate problem, job state, readiness, outcome, and delivery resources | Truthful failures/fallbacks and retries |
| `C-07-06` | Client timeout after submit can create duplicate work | Atomic idempotency record; retry same key to resolve ambiguity | Exactly one logical job/side effect |
| `C-07-07` | Arbitrary callback URL permits confused-deputy/SSRF behavior | Pre-registered authorized endpoint ID only | Stage 12 can harden validation/signing without changing submissions |
| `C-07-08` | Concrete API limits are required but scale/latency evidence is absent | Schema requires named concrete activation policies; missing values block enablement | No invented production numbers; not yet enablement-ready |
| `C-07-09` | `A-01-INT` reaches Stage 07 without named ownership, trust, delivery, or cutover evidence | Accepted `A-07-INTEGRATION` resolves the logical boundary/delivery defaults while deferring only the evidence-dependent portions to their named stages | Sponsor approval explicitly authorizes the temporary disposition until its stated expiries |
| `C-07-10` | Workflow endpoint could smuggle orchestration before Stage 08/09 | Marked conditional; only named versioned workflow/public child jobs allowed | No generic workflow engine or proactive authority |

## Open questions

| ID | Question | Blocking? | Options | Recommended temporary assumption | Effect |
|---|---:|---|---|---|---|
| `Q-07-01` | Which IdP, token format/issuer/client flow, scopes/roles, optional mTLS, and tenant-claim binding are authoritative? | Yes before external production; disposition needed for Stage 07 approval | OAuth/OIDC; opaque tokens; signed platform token; mTLS combination | Approve `A-07-INTEGRATION`; resolve trust portion in Stage 12 | HTTP boundary implementable; provider/security acceptance remains blocked |
| `Q-07-02` | Which consumers and capability operations are first release, and what exact schemas/limits apply? | Before endpoint activation | One vertical slice; subset; all | Activate only release-scoped definitions with filled policies | No unsupported API surface or numbers |
| `Q-07-03` | Which operations have measured short/predictable sync fitness? | Before enabling `:invoke` | Measured sync; async-only | Async-only unless definition evidence approves sync | Prevents request-lifetime durable work |
| `Q-07-04` | Which consumer needs registered webhooks and what delivery/signing/retry policy? | Before webhook activation | Polling only; webhook per consumer | Polling universal; callback conditional | No arbitrary callback or unsupported delivery promise |
| `Q-07-05` | Is there a named first-release workflow and grant semantics? | Before workflow endpoint activation | None; named deterministic workflow | Keep endpoint conditional and insight-only by default | Stage 08/09 avoids generic orchestration |
| `Q-07-06` | What legacy schemas/paths and cutover windows must adapters preserve? | Stage 16/20 | Strangler; big bang; governed dual read/project | Adapter-based incremental migration; no new cross-write | Compatibility burden remains measurable |
| `Q-07-07` | What idempotency/cursor/result-reference retention and expiry periods apply? | Before production | Per operation/data policy | Require published policy, no guessed duration | Reconciliation/410 behavior not numerically configured |
| `Q-07-08` | Who operates each consumer adapter, canonical API, callback delivery, and contract conformance suite? | Before production/Stage 20 | Consumer team; ARK integration; shared | Logical roles above under `A-04-OWNERSHIP` | Contract design valid; operating readiness blocked |

## Requirements-traceability updates

| Requirement | Stage 07 design response | Verification direction |
|---|---|---|
| `ARK-FR-001` | Subscription/config resources separate from ingestion/invocation | Enabling capability produces no ingestion/job side effect |
| `ARK-FR-002/003` | Inline push and scoped upload register/commit APIs; dataset version/readiness resource | Contract/checksum/raw-first/publication tests |
| `ARK-FR-004` | Entitled capability list and immutable machine-readable definition | OpenAPI/schema/definition conformance tests |
| `ARK-FR-005` | Common headers/envelope/outcome/problem contracts plus typed operation input/result | Schema and consumer-adapter tests |
| `ARK-FR-006` | Readiness, platform control, capability outcome, job failure remain separate | Scenario/status-mapping suite |
| `ARK-FR-007/008` | `:submit`, universal job/status/cancel/result; `:invoke` opt-in only | Idempotency, timeout, replay, polling, sync-classification tests |
| `ARK-FR-009` | No inference lifecycle operation can train/promote implicitly; exact version refs | Negative side-effect and lineage tests |
| `ARK-FR-010` | Workflow conditional; grant/policy authoritative; verifier advisory | No-action and endpoint-authorization tests |
| `ARK-FR-011` | Registered webhook external contract distinct from conditional internal events | Delivery dedupe/signature/failure-isolation tests |
| `ARK-FR-012` | Machine-readable definitions, errors, IDs, versions, and trace evidence | LAB contract/conformance suite |
| `ARK-NFR-001` | AuthContext tenant; no tenant header/body authority; concealed cross-tenant lookup | Cross-tenant negative endpoint suite |
| `ARK-NFR-002/003` | Independent exact versions, immutable schemas, major compatibility, ETags | Compatibility/replay/lineage tests |
| `ARK-NFR-004` | Precise idempotency, async ambiguity resolution, callback dedupe | Duplicate/fault/timeout tests |
| `ARK-NFR-005` | Opaque IDs/refs, bounded errors/events, no arbitrary callback/PII trace keys | Schema/privacy/logging/SSRF tests |
| `ARK-NFR-006` | Request/correlation/causation propagation across job/result/audit/delivery | Trace completeness test |
| `ARK-NFR-007` | Activation requires explicit policies; no numeric targets invented | Definition-policy completeness gate and Stage 17 measurements |
| `ARK-CON-001/002` | HTTP façade routes to typed public module ports; no per-capability service/private call | Dependency and contract-boundary tests |
| `ARK-CON-003` | Consumer-platform adapters outside cores; canonical ARK schema/SDK owned centrally | No consumer term/type dependency in capability modules |
| `ARK-CON-004` | Inline bound and upload/result references | 413-to-upload and large-result reference tests |
| `ARK-CON-005` | Universal job API over PostgreSQL truth; no broker/workflow product | Job acceptance/recovery tests in Stage 08/13 |
| `ARK-CON-006` | Source/identity registration and trusted tenant boundary | Reject body tenant/unregistered source/direct DB |
| `ARK-CON-007` | SSE, generic workflow, service API split, broker, GraphQL/gRPC products excluded without trigger | Anti-overengineering review |
| `SC-02-03/04/05/06/07/08/09/10/12` | Concrete contract and test mappings above | Release conformance suite |

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Every governing API/integration bullet addressed | PASS | Source-instruction coverage maps all bullets |
| Unified vs capability-specific vs workflow strategy decided | PASS | Combined API strategy with conditional named workflow |
| External endpoint responsibilities concrete | PASS | Resource surface and endpoint matrix |
| Internal contracts preserve module boundaries | PASS | Typed application-port matrix; no shared tables/private imports |
| Request/response/event/error schemas concrete enough to implement | PASS | JSON/HTTP examples and stable schema rules |
| Every endpoint class has authentication, authorization, tenant source, timeout/limits, idempotency/concurrency, and errors | PASS | Endpoint contract matrix plus common contracts |
| Idempotency and correlation semantics precise | PASS | Dedicated scope/replay/conflict/propagation contracts |
| Sync/async/job/polling/cancellation/result behavior explicit | PASS | Invocation policy, 202/job schemas, public state vocabulary |
| Pagination/versioning/rate/timeout behavior explicit | PASS | Dedicated sections; numeric activation policies remain evidence-bound |
| Webhook/event boundary concrete and safe | PASS WITH LATER SECURITY/RELIABILITY INPUTS | Registered endpoint, signed versioned reference-only event; activation blocked until Stage 12/13 policy |
| Platform neutrality and adapter ownership visible | PASS | Adapter placement and conformance responsibilities |
| Synapse restrictions preserved | PASS | Legacy adapter only, advisory verifier, no production/internal inference |
| Anti-overengineering applied | PASS | No per-capability service, generic execute/workflow, broker, SSE, ESB, or new product |
| Authorized platform review reconciled | PASS | `platform_architect` confirmed the design is passable with the endpoint/schema matrix, precise cross-cutting rules, interface-only Synapse treatment, and explicit `A-01-INT` replacement; findings incorporated |
| `A-01-INT` Stage 07 disposition | PASS | Accepted `A-07-INTEGRATION` resolves adapter/delivery defaults and temporarily dispositions missing ownership, trust, and cutover evidence to named expiries |
| Stage 08 not executed | PASS | No Stage 08 artifact or decision created |
| Sponsor-requested approval | **PASS** | Sponsor explicitly approved Stage 07 and its outputs, including `A-07-INTEGRATION` and ADR-004, on 2026-08-11 |

**Gate result: PASSED AND APPROVED.** The platform review is reconciled, the endpoint/schema gate is satisfied, and the sponsor explicitly approved Stage 07 and its outputs, including `A-07-INTEGRATION` and ADR-004, on 2026-08-11. Stage 08 is authorized to begin.

## Downstream consequences

- Stage 08 must define the internal job state machine, claims/leases, retries, deadlines, cancellation safe points, progress, parent/child jobs, and mapping to the stable public job states.
- Stage 09 must decide whether any named workflow/internal event/outbox is activated and complete proactive grant plus callback delivery semantics without changing the API authority boundaries.
- Stage 10 must fill capability-specific input/output/feature/model definitions and operation eligibility without changing the common envelope or enabling Synapse without evidence.
- Stage 12 must replace the trust portion of `A-07-INTEGRATION` with authoritative IdP/token/mTLS/scope/tenant-claim policy and select webhook signing/destination/replay controls.
- Stage 13 must define idempotency retention, timeout/retry/circuit behavior, callback retry/dead-letter policy, result/reference expiry, and ambiguous failure recovery.
- Stage 14 must instrument request/correlation/job/delivery/schema-version evidence while preserving privacy/cardinality.
- Stage 15 selects gateway/identity/network/runtime placement only from environment evidence.
- Stage 16 must test schema compatibility and define strangler/cutover behavior for BCDP/Whatson/Synapse legacy adapters.
- Stage 17 supplies measured request/page/rate/timeout/payload/result policies before endpoint activation.
- Stage 20 must assign named API/adapter/delivery/runbook owners under `A-04-OWNERSHIP`.

## Exact next-stage inputs

Approved inputs for Stage 08:

1. Approved `outputs/stages/02-system-definition.md` through `outputs/stages/07-api-integration.md`
2. Accepted `decisions/ADR-000-temporary-source-evidence-disposition.md` through `decisions/ADR-003-architecture-style.md`
3. Accepted `decisions/ADR-004-api-contract-boundary.md`
4. Active `A-07-INTEGRATION` until each portion's named ownership/Stage 12/release-delivery/Stage 16 expiry
5. `sources/normalized/ark-assumptions.md`
6. All seven service cards under ADR-000/ADR-002 restrictions
7. `stages/08-execution-orchestration.md`, `templates/stage-output.md`, and exact governing prompt section **7. Execution and orchestration**

Stage 07, `A-07-INTEGRATION`, and ADR-004 are approved; Stage 08 may consume them.
