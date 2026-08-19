# ARK interface contracts — ADR-017/018 publication revision

Status: `POST-PUBLICATION REVISION — ADR-017/018 ACCEPTED; INDEPENDENT RE-ASSURANCE PENDING`

## Contract laws

- External baseline: REST/JSON with API-major paths and independently versioned typed schemas.
- Internal baseline: typed in-process public module ports; network protocols do not define ownership.
- Organization authority comes only from an authenticated principal plus a stored active organization membership. A business tenant is derived only after ARK verifies the stored business belongs to that authorized organization. No public organization/business/tenant header establishes authority.
- Resource IDs are opaque and organization/business scoped; possessing an ID never authorizes it.
- Large payloads use scoped object references; PostgreSQL holds bounded operational truth.
- Mutation/submission contracts require idempotency identity; optimistic updates require version/ETag preconditions.
- Polling is universal for durable work. Webhook delivery is conditional and separate from result truth.
- Request fields are rejected when unknown unless the request schema explicitly permits a bounded extension point. Clients must ignore additive unknown response fields declared compatible within the API major; new required request fields or semantic changes require a new contract/API version.

## Public resource and operation surface

| Surface | Contract | Responsibility |
|---|---|---|
| Account registration | `POST /v1/accounts:register` | Create the minimum profile under an admitted enrollment/trust contract; credentials and production enrollment remain blocked |
| Organization list/create | `GET /v1/organizations`; `POST /v1/organizations` | List authorized memberships or create an owned organization |
| Business list/create | `GET /v1/organizations/{organization_id}/businesses`; `POST /v1/organizations/{organization_id}/businesses` | Organization-scoped administration; every created business receives an opaque business tenant ID |
| Capability pattern read/update | `GET /v1/organizations/{organization_id}/capability-pattern`; `PUT /v1/organizations/{organization_id}/capability-pattern` | Read or replace the uniform organization allowlist; owner/admin may update under ETag/idempotency/audit |
| Organization memberships | `GET /v1/organizations/{organization_id}/memberships`; `POST /v1/organizations/{organization_id}/memberships` | Owner-controlled admin membership initially; viewer/tester remain inactive |
| Owner credit summary | `GET /v1/billing-account/credit-summary` | Authorized payer view of shared balance, active reservations and organization-policy consumption; no funding/mutation contract implied |
| Organization credit policy | `GET /v1/organizations/{organization_id}/credit-policy`; `PUT /v1/organizations/{organization_id}/credit-policy` | Owner/customer billing administrator reads or versions limits; organization admin receives no mutation authority by implication |
| Credit usage/charge read | `GET /v1/credit-usage/{usage_event_id}` | Authorized immutable payer→organization→business→capability→job attribution and settlement state |
| Discovery | `GET /v1/capabilities` | Entitled release-scoped summaries, not service discovery |
| Definition | `GET /v1/capabilities/{capability_id}/versions/{version}` | Immutable operations, schemas, modes, dependencies, limits and fallbacks |
| Sync invoke | `POST /v1/capabilities/{capability_id}/versions/{version}/operations/{operation_id}:invoke` | Only definition-declared, admitted, bounded synchronous work |
| Async submit | `POST /v1/capabilities/{capability_id}/versions/{version}/operations/{operation_id}:submit` | One durable job under canonical idempotency |
| Inline ingestion | `POST /v1/data/ingestions` | Bounded push/micro-batch and ingestion job |
| Upload registration | `POST /v1/data/uploads` | Scoped bulk-upload authority/reference |
| Upload commit | `POST /v1/data/uploads/{upload_id}:commit` | Verify checksum/metadata and create/replay ingestion job |
| Ingestion status | `GET /v1/data/ingestions/{id}` | Ingestion/job/dataset refs, not raw content |
| Dataset version | `GET /v1/datasets/{id}/versions/{version}` | Readiness, reason, schema, quality and lineage refs |
| Job status | `GET /v1/jobs/{id}` | Stable lifecycle, progress, result/error refs |
| Cancel | `POST /v1/jobs/{id}:cancel` | Idempotent request; no promise of immediate stop |
| Result | `GET /v1/jobs/{id}/result` | Bounded body or tenant-scoped immutable object ref |
| Subscription read | `GET /v1/subscriptions` | Read tenant-scoped enablement/config only |
| Subscription update | `PUT /v1/subscriptions/{capability_id}` | Versioned enablement/config mutation; never ingestion or execution |
| Webhook register | `POST /v1/webhook-endpoints` | Register authorized destination and return opaque endpoint ID |
| Webhook update | `PATCH /v1/webhook-endpoints/{endpoint_id}` | Versioned enable/disable/update under ETag; arbitrary submission URL prohibited |
| Named workflow | `POST /v1/workflows/{id}/versions/{version}:submit` | Conditional immutable named graph only; no generic DAG |

## Required headers and context

| Field | Rule |
|---|---|
| `Authorization` | Required on protected endpoints; exact production trust remains `EXTERNAL_TRUST_BLOCKED` |
| `Idempotency-Key` | Required on mutations, submissions, upload commit, cancel and configuration changes |
| `X-Correlation-ID` | Optional bounded caller token; ARK generates when absent and echoes it |
| `X-Request-ID` | Generated per HTTP attempt |
| `If-Match` | Required for versioned mutable control resources |
| `traceparent` | Optional technical context; never tenant authority |

Server context is immutable:

```json
{
  "subject_id": "sub_opaque",
  "actor_type": "HUMAN_OR_APPLICATION",
  "organization_id": "org_opaque",
  "membership_id": "membership_opaque",
  "organization_roles": ["admin"],
  "business_id": "business_opaque_or_null_for_org_control",
  "tenant_id": "business_opaque_or_null_for_org_control",
  "permissions": ["capability:submit"],
  "roles_or_attributes": [],
  "credential_id": "cred_opaque",
  "trust_profile_id": "trust_profile_opaque",
  "issuer_id": "issuer_opaque",
  "audience": "ark-api",
  "authenticated_at": "2026-08-14T00:00:00Z",
  "expires_at": "2026-08-14T00:15:00Z",
  "delegation_chain": null,
  "assurance_level": "profile_defined",
  "correlation_id": "corr_opaque"
}
```

This is the provider-neutral logical `AuthContext`, not a token schema. `organization_id`, membership, roles, and business scope are validated server-side rather than copied from caller-controlled fields. Organization-control operations may have no `business_id`; every business data/capability/job operation requires `business_id == tenant_id`. Background execution additionally requires a distinct workload identity and a non-forgeable delegated context bound to subject origin, organization, business tenant, membership and capability-pattern versions, job, attempt, fence, handler/version, purpose, and exact input/data/model/configuration references; neither identity alone is sufficient.

## Account, organization, business, and capability-pattern contracts

Minimum records are:

| Record | Required identity and state | Authority and invariant |
|---|---|---|
| `AccountProfile` | `account_id`, `subject_id`, `full_name`, `phone_number`, `status`, version/timestamps | Self/enrollment and authorized profile administration; additional fields and verification rules remain unresolved |
| `Organization` | `organization_id`, display metadata, status, version/timestamps | Created by an authenticated account; product ownership is not ARK architecture or production authority |
| `OrganizationMembership` | `membership_id`, `organization_id`, `account_id`, active role bindings, status, version/timestamps | Stored membership plus authenticated subject derives organization authority; admin is active, viewer/tester inactive |
| `Business` | `business_id`, `organization_id`, optional source-platform external reference, status, version/timestamps | One active parent organization; `business_id` is the effective tenant ID for business-bearing assets |
| `OrganizationCapabilityPattern` | `organization_id`, immutable `pattern_version`, canonical enabled capability IDs, effective time, actor/audit refs | One effective allowlist applies uniformly to all current/future businesses; owner/admin may replace it |

An organization admin may list and administer all businesses in that organization and may update the pattern. That scope does not authorize an operation without a specific derived business tenant and does not authorize a combined cross-business dataset, query, result, export, or job. Such behavior requires a future typed contract with explicit purpose, minimization, audit, and admission.

Capability-pattern replacement requires `Idempotency-Key` and `If-Match`. ARK validates canonical capability IDs, commits a new immutable pattern version plus mandatory old/new audit, and returns the new ETag. A per-business override field is rejected. Capability discovery returns the intersection of the effective organization pattern and capabilities visible in the current release; invocation additionally checks every existing entitlement, data, science/model, policy, quota, environment, and production block.

Example pattern response:

```json
{
  "organization_id": "org_direct",
  "pattern_version": "pattern_v3_immutable",
  "enabled_capability_ids": ["CAP-RFM", "CAP-CHURN", "CAP-REC"],
  "effective_at": "2026-08-15T00:00:00Z",
  "etag": "pattern_v3_immutable"
}
```

Pattern inclusion is configuration eligibility, not execution admission. For example, `CAP-RFM` remains unavailable while its `MIGRATION_BLOCKED` profile or any other required gate is active.

## Owner billing, organization policy, and credit contracts

`OwnerBillingAccount` is the shared payer/credit boundary for several organizations. An organization references the account but never owns a balance or wallet. Minimum records are:

| Record | Required identity/state | Invariant |
|---|---|---|
| `OwnerCustomerAccount` | stable commercial customer ID, status, authorized billing-administrator refs | Commercial payer boundary; not a human credential or ARK approval authority |
| `OwnerBillingAccount` | `billing_account_id`, owner-customer ID, status, ledger/projection version | One active shared account initially; balance derives from append-only ledger minus active reservations |
| `OrganizationCreditPolicy` | `policy_id/version`, `organization_id`, `billing_account_id`, daily/monthly/per-job limits, `hard_limit`, warning threshold, effective interval, audit refs | Policy/ceiling only; never a wallet or earmarked balance; one effective version per organization/time |
| `CreditReservation` | `reservation_id`, billing/organization/business IDs, job/idempotency refs, policy/pricing versions, reserved amount, state/expiry | Counts against shared available balance and organization headroom; atomically paired with durable job acceptance |
| `CreditUsageEvent` / settlement | stable `usage_event_id`, reservation/job/capability refs, pricing version, amount, outcome/timestamps | Exactly one logical settlement per priced usage identity; retries cannot duplicate it |
| `CreditLedgerEntry` | immutable entry ID/type/amount, billing account, source usage/reservation/adjustment refs, actor/audit/correlation | Append-only credit, debit, release/reversal/adjustment evidence; settled entries are never edited |

Canonical organization policy shape:

```json
{
  "organization_id": "org_A",
  "billing_account_id": "billing_owner_opaque",
  "policy_version": "credit_policy_v4_immutable",
  "monthly_limit": 100000,
  "daily_limit": null,
  "per_job_limit": 5000,
  "hard_limit": true,
  "warning_threshold": 80000,
  "effective_from": "2026-08-15T00:00:00Z",
  "effective_to": null,
  "etag": "credit_policy_v4_immutable"
}
```

An explicit null limit means no organization-specific ceiling for that dimension. A missing/expired policy, unresolved policy window, billing-account mismatch, or absent pricing version fails closed. Exact amount units, window time zone and non-hard behavior remain `CREDIT_BILLING_ADMISSION_BLOCKED`; the numeric values above illustrate shape only and are not ARK defaults.

Canonical settled usage/debit attribution:

```json
{
  "billing_account_id": "billing_owner_opaque",
  "organization_id": "org_A",
  "business_id": "business_A1",
  "capability": {
    "capability_id": "CAP-REC",
    "capability_version": "1.0",
    "operation_id": "recommendation-generate-batch"
  },
  "job_id": "job_opaque",
  "usage_event_id": "usage_immutable",
  "pricing_version": "pricing_immutable",
  "amount": 1200,
  "reservation_id": "reservation_opaque",
  "organization_credit_policy_version": "credit_policy_v4_immutable",
  "state": "SETTLED"
}
```

Credit amounts are non-negative in usage/reservation contracts; the signed ledger entry type determines debit, credit, release, refund or adjustment. Caller-controlled input cannot select these IDs, the payer, price, or amount.

Every credit-consuming execution has a durable logical `job_id`. Priced work therefore uses durable submission unless a later synchronous contract proves the same reservation, timeout/cancellation, settlement and job/result truth. Existing `:invoke` is limited to unpriced/zero-credit operations while production credit charging remains blocked.

### Dual financial admission and reservation

After authorization, capability-pattern, data-readiness and capability-eligibility gates pass, the control owner resolves stored `business → organization → billing account`, then atomically checks:

1. organization policy headroom, counting settled usage plus active reservations in every applicable window; and
2. owner available balance, counting settled debits plus all active reservations across its organizations.

Both checks must pass. The initial PostgreSQL placement commits one credit reservation and one durable job acceptance in a coordinated transaction through owner ports. Settlement/release is idempotent under stable reservation and `usage_event_id`. If actual usage can exceed the reservation, an atomic incremental reservation must pass before the extra usage; otherwise execution stops/fails according to the admitted pricing contract. Negative balances and silent hard-limit overrun are prohibited.

## Common operation request

```json
{
  "request_version": "1.0",
  "dataset_refs": [
    {"dataset_id": "ds_opaque", "dataset_version": "dv_immutable", "purpose": "inference"}
  ],
  "configuration_ref": {"configuration_id": "cfg_opaque", "configuration_version": "cv_immutable"},
  "input": {}
}
```

Organization, business tenant, caller, membership/pattern versions, idempotency and correlation are server/header context, not body authority. Capability-specific `input` is validated against the exact definition.

## Synchronous outcome

```json
{
  "request_id": "req_opaque",
  "correlation_id": "corr_opaque",
  "capability_id": "CAP-EXAMPLE",
  "capability_version": "1.0",
  "operation_id": "example-operation",
  "outcome": {"status": "ELIGIBLE", "reason_code": "COMPLETED", "message": "Operation completed"},
  "result": {},
  "lineage_ref": "lin_opaque",
  "usage_ref": "usage_opaque"
}
```

Outcome status is `ELIGIBLE | DEGRADED | FALLBACK | INELIGIBLE`. Transport/execution failure uses the problem contract. No current profile is production-admitted for this path.

## Durable submission and job resource

Successful submission returns `202 Accepted`, `Location: /v1/jobs/{job_id}`, and:

```json
{
  "job_id": "job_opaque",
  "job_type": "capability-operation",
  "state": "ACCEPTED",
  "capability": {"id": "CAP-REC", "version": "1.0", "operation_id": "recommendation-generate-batch"},
  "submitted_at": "2026-08-11T00:00:01Z",
  "status_url": "/v1/jobs/job_opaque",
  "result_url": "/v1/jobs/job_opaque/result",
  "correlation_id": "corr_opaque"
}
```

Public states map from the internal lifecycle without hiding truth. Internal states include `ACCEPTED`, `WAITING`, `READY`, `RUNNING`, `RETRY_WAIT`, `FINALIZING`, `CANCELLATION_REQUESTED`, `SUCCEEDED`, `FAILED`, `CANCELLED`; attempts separately record lease/run/terminal status. A retry creates a new attempt under the same logical job.

## Data contracts

Every source registration binds one derived business tenant, its organization, source owner, contract/schema version, integration mode, stable identity fields, classification/purpose, correction/deletion semantics, validation policy and object constraints. Every dataset version includes immutable object/checksum refs, structural report, semantic report, readiness decision, lineage and correction/tombstone state. An organization-wide admin must still select and authorize one business tenant for these operations.

`DATA_CONTRACT_ADMISSION_BLOCKED` means no Phase 1 fixture schema is a production contract.

## Internal public ports

| Owner port | Core commands/queries | Non-responsibility |
|---|---|---|
| Trust/context | authenticate, resolve active organization membership, derive/delegate organization and business `AuthContext` | Business/scientific eligibility |
| Control/billing | own accounts/organizations/memberships/business registry/pattern, owner billing accounts, organization credit policies, reservations and balance projections; decide entitlement/grant/quota/policy/credit admission | Data readiness, science, effect execution, payment processing or untyped cross-business aggregation |
| Catalog | register raw/candidate, publish/query readiness and lineage | Capability eligibility |
| Job manager | submit, claim, heartbeat, report, cancel, finalize, reconcile | Capability compute/result content |
| Capability | definition, eligibility, execute exact operation, commit result | Job lifecycle, tenant grant, external action |
| Registry | register identity/evidence, record promotion, assign/revoke exact deployment | Training or implicit activation |
| Evidence/usage ledger | append/verify/query audit, lineage, usage, metering, settlements/releases and charge attribution | Business/result truth, caller-selected price, or mutable organization wallet |
| Delivery | register endpoint, create/claim/finalize delivery record | Capability result or action authority |
| Workflow | submit/observe parent and public child jobs | Private capability calls or arbitrary DAG |

Every mutating port carries trusted organization/business/workload context, exact membership/pattern/contract/handler/policy versions, correlation/causation, idempotency/effect identity and expected state version where applicable.

## Error/problem contract

```json
{
  "type": "urn:ark:problem:capability-unavailable",
  "title": "Capability unavailable",
  "status": 409,
  "code": "CAPABILITY_UNAVAILABLE",
  "detail": "The requested operation is not admitted for this environment",
  "request_id": "req_opaque",
  "correlation_id": "corr_opaque",
  "retryable": false
}
```

Failures distinguish authentication, organization membership/authorization, business scope required or concealed, capability not enabled by pattern, credit policy missing/expired/exceeded, insufficient shared balance, reservation/pricing/version conflict, credit ledger unavailable, contract/version/ETag, idempotency conflict, not ready, ineligible, unavailable, rate/quota, dependency, deadline, cancellation, ambiguous external effect and internal fault. A retryable flag is operation/failure-class policy, not a blanket HTTP-status rule. Financial denial creates no executable job.

## Event envelope and webhook delivery

Internal events exist only for a named committed-fact subscriber:

```json
{
  "schema_version": "1.0.0",
  "event_type": "ark.insight.qualified.v1",
  "event_id": "evt_opaque",
  "data_schema_ref": "ark.insight.qualified.payload/1.0.0",
  "producer": {"module": "proactive-control", "version": "code_opaque"},
  "occurred_at": "2026-08-12T12:00:00Z",
  "recorded_at": "2026-08-12T12:00:01Z",
  "expires_at": "2026-08-13T12:00:00Z",
  "tenant_id": "tenant_opaque_internal",
  "subject": {"type": "action_decision", "id": "decision_opaque"},
  "source_fact_ref": "insight_opaque",
  "correlation_id": "corr_opaque",
  "causation_id": "insight_opaque",
  "payload_hash": "sha256_opaque",
  "classification": "INTERNAL_CONFIDENTIAL",
  "purpose": "PROACTIVE_INSIGHT_ROUTING",
  "ordering": null,
  "data": {
    "insight_ref": "insight_opaque",
    "capability_ref": "churn/version_opaque",
    "dataset_version_ref": "dataset_version_opaque",
    "authorization_ref": "authorization_opaque/version_opaque",
    "threshold_policy_ref": "threshold_policy_opaque",
    "disposition": "REPORT_ONLY"
  }
}
```

External webhook envelopes carry resource references and a stable delivery/event identity, use a registered endpoint version, are signed under an admitted mechanism, and are delivered at least once. Destination, subscription, policy, egress and secret authority are rechecked before every send. The path remains `EXTERNAL_DELIVERY_BLOCKED`.

## Compatibility and versioning

- API major version is explicit in path.
- Operation, dataset, source, configuration, policy, handler, event, workflow, artifact and assignment versions are independent.
- Additive compatible evolution is allowed only under declared schema rules; incompatible change creates a new version.
- Admitted jobs pin exact versions; deployment retains a compatible handler or applies an explicit migration/failure policy.
- No mutable `latest`, directory convention or unversioned `active` selection is authoritative.

## Canonical contract conformance tests

- Account/organization/business tests cover one account owning multiple organizations, one organization containing many businesses, one active parent per business, opaque IDs, and the unresolved-field prohibition.
- Organization authorization tests prove an admin can access all businesses and update the pattern within its organization, but cannot access another organization, create an unscoped business-data request, combine/export business data, or grant admin membership unless separately authorized.
- Capability-pattern tests cover uniform current/future-business inheritance, rejected per-business overrides, canonical IDs, idempotency, ETag races, immutable old/new audit, pattern-version pinning/recheck, capability removal, and the rule that pattern inclusion never clears an admission block.
- Credit tests cover one shared owner balance across multiple organizations, policy-not-wallet semantics, explicit null versus zero/missing policy, daily/monthly/per-job windows, policy and balance pass/fail combinations, concurrent reservations, atomic job acceptance, settlement/release/reconciliation, duplicate retry/replay, complete debit attribution, and owner-only billing-policy mutation.
- Block-preservation tests prove a funded account and permissive organization policy cannot run a blocked capability or bypass organization/business authorization, pattern, data, science, model, security, environment, or capacity gates.
- The provider-neutral `AuthContext` schema is checked field-for-field against accepted ADR-008/Stage 12 as refined by ADR-017's organization-membership and business-tenant fields; forged body/header authority, expired/revoked credentials, inactive membership, organization/business mismatch, audience mismatch, delegation broadening, and workload-only or context-only background execution must fail closed.
- The `202 Accepted` capability submission example is checked field-for-field against the Stage 07 concrete recommendation-batch contract, including `capability`, `submitted_at`, polling URLs, request and correlation identities.
- The internal event example is checked field-for-field against the Stage 09 `schema_version` envelope, including producer identity, schema reference, occurrence/record/expiry times, subject/source fact, integrity, classification, purpose and minimal typed `data`.
- Compatibility tests reject unknown request fields unless a bounded extension point is declared, require clients to ignore compatible additive response fields, and require a new version for new required request fields or changed meaning.
- These publication examples are canonical for the fields shown. Capability-specific schemas and later compatible additions remain the immutable registered contracts cited below; a summary cannot supersede an accepted owner schema.

## Security and production status

All external trust, production data governance, secrets/crypto, privileged action, external delivery, LLM provider, supply chain and model-cache paths remain blocked under ADR-008. Production credit charging is additionally `CREDIT_BILLING_ADMISSION_BLOCKED` under ADR-018. Contract existence is not activation, payment/accounting authority, or evidence of provider behavior.

## Exact contract provenance

| Contract family | Authoritative concrete evidence |
|---|---|
| Public routes and responsibilities | `outputs/stages/07-api-integration.md — External resource and operation surface`; `— Endpoint contract matrix` |
| Headers, trusted envelope and sync response | `outputs/stages/07-api-integration.md — Common headers and operational envelope`; `— Operation request schema`; `— Standard synchronous response` |
| Capability submit body and `202` response | `outputs/stages/07-api-integration.md — Concrete capability example — recommendation batch submission` |
| Job/status/cancel/result fields and status mapping | `outputs/stages/07-api-integration.md — Job contract`; `outputs/stages/08-execution-orchestration.md — Internal job state machine` |
| Ingestion, upload commit and dataset references | `outputs/stages/07-api-integration.md — Ingestion/upload example`; `outputs/stages/06-data-architecture.md — Source-registration and canonical contract envelope`; `— Four-layer acceptance model` |
| Idempotency/correlation/pagination/errors/timeouts | `outputs/stages/07-api-integration.md — Idempotency contract`; `— Correlation and propagation contract`; `— Cursor-pagination contract`; `— Error model`; `— Rate limits, quotas, and timeouts` |
| Subscription, endpoint and webhook envelope/delivery | `outputs/stages/07-api-integration.md — Callback/webhook contract`; `outputs/stages/09-events-proactive-actions.md — Subscription management and APIs`; `— Versioned external webhook schema example`; `— External delivery state and semantics` |
| Internal event schema/publication | `outputs/stages/09-events-proactive-actions.md — Versioned internal domain-event schema example`; `— Internal reliable publication and broker disposition` |
| Named workflow definition/parent/child state | `outputs/stages/08-execution-orchestration.md — Conditional named-workflow contract`; `outputs/stages/07-api-integration.md — External resource and operation surface` |
| Internal owner commands and non-responsibilities | `outputs/stages/07-api-integration.md — Internal application-port contracts`; `outputs/stages/08-execution-orchestration.md — Component responsibility matrix` |
| Tenant/security rules for every asset | `outputs/stages/12-security-governance.md — Tenant-bearing asset control matrix`; `— Workload identity and delegated execution` |
| Account/organization/business hierarchy, pattern, and admin scope | `sources/sponsor-decisions/2026-08-15-owner-organization-business.md`; accepted ADR-017 |
| Owner billing account, organization credit policy, reservation and charge attribution | `sources/sponsor-decisions/2026-08-15-owner-billing-credit-management.md`; accepted ADR-018 |

The publication deliberately does not repeat every large example field from those approved sections. Implementers must consume the exact cited contract family and its Stage 16 contract/negative tests together; a summary row here cannot override an approved schema.
