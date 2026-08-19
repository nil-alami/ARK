# ARK Reference MVP execution-trace contract

Status: `PLANNED`

> **ADR-017/018 notice:** this trace contract predates both revisions. It must add safe organization/membership/business/pattern references plus billing-account, credit-policy, reservation, usage-event and pricing-version references while excluding full name, phone, payment data and raw inputs. See both ADR impact documents.

Contract identifier: `ark.reference-mvp.trace-event/1.0`

## Purpose and authority

The execution trace is an append-only, tenant-scoped account of the demonstration. It lets the Gradio client display stored runtime progress, attempts, quarantine, results, delivery simulation, and replay.

For the Reference MVP, PostgreSQL trace rows are durable demonstration evidence. They do not replace owner state:

- job and attempt tables remain execution truth;
- catalog/dataset rows remain readiness truth;
- quarantine rows remain invalid-input truth;
- capability result rows/object refs remain result truth;
- simulated delivery rows remain delivery truth.

A trace event must reference those owner resources and must never be used to authorize work or fabricate a terminal state. Diagnostic timing fields are informative; owner state and required evidence decide completion.

## Event envelope

```json
{
  "schema_version": "1.0",
  "event_id": "evt_opaque",
  "run_id": "run_opaque",
  "sequence_no": 17,
  "event_type": "job.attempt.failed",
  "stage": "JOB_EXECUTION",
  "status": "FAILED",
  "implementation_class": "REAL_IMPLEMENTATION",
  "occurred_at": "2026-08-15T12:00:00.000Z",
  "recorded_at": "2026-08-15T12:00:00.010Z",
  "tenant_id": "tenant_opaque_internal",
  "correlation_id": "corr_opaque",
  "request_id": "req_opaque",
  "causation_id": "evt_opaque_or_resource",
  "component": "job-manager",
  "runtime_role": "worker-general",
  "resource_refs": {
    "dataset_version_id": "dv_opaque",
    "job_id": "job_opaque",
    "attempt_id": "attempt_opaque",
    "result_id": null,
    "delivery_id": null
  },
  "versions": {
    "release_id": "release_opaque",
    "configuration_version": "demo-rec-policy/1.0",
    "contract_version": "demo-transactions/1.0",
    "handler_version": "poa_fixture_recommendation/1.0"
  },
  "detail": {
    "reason_code": "DEMO_TRANSIENT_EXECUTION_FAILURE",
    "retryable": true,
    "attempt_number": 1,
    "counts": {},
    "duration_ms": 4,
    "shortcut_flags": ["POA_FIXTURE_ONLY", "INJECTED_FAULT"]
  },
  "classification": "SYNTHETIC_INTERNAL",
  "production_decision": false,
  "payload_hash": "sha256_opaque"
}
```

## Field rules

| Field | Rule |
|---|---|
| `schema_version` | Required semantic contract version. Incompatible field/meaning changes require a new major version. |
| `event_id` | Server-generated opaque immutable identity. |
| `run_id` | Required for every Reference MVP event. |
| `sequence_no` | Positive, gap-tolerant, strictly increasing per run; allocated in the same transaction as event insertion. Consumers order by this field, not timestamps. |
| `event_type` | Registered dot-separated type from the taxonomy below. Unknown types are displayable as generic supporting events but cannot change UI terminal truth. |
| `stage` | One stable stage enum for UI grouping. |
| `status` | One status enum; event status does not substitute for owner resource state. |
| `implementation_class` | `REAL_IMPLEMENTATION`, `SIMPLIFIED_IMPLEMENTATION`, `SIMULATED_BEHAVIOR`, `POSTPONED`, or `NOT_APPLICABLE`. Runtime events use the first three; plan/absence assertions may use the latter two. |
| `occurred_at` / `recorded_at` | UTC timestamps. `recorded_at` is database time; ordering still uses `sequence_no`. |
| `tenant_id` | Internal trusted context only. API may return an opaque safe tenant label, never accept this field as caller authority. |
| `correlation_id` | Stable across the entire run. |
| `request_id` | HTTP-attempt identity when applicable; null for pure background/replay materialization events. |
| `causation_id` | Immediate triggering event/resource identity; null only for `run.initialized`. |
| `component` | Registered logical owner/module, not a deployment/service claim. |
| `runtime_role` | `gradio-client`, `api`, `worker-general`, `maintenance`, or `delivery-simulator`. |
| `resource_refs` | Opaque tenant-scoped refs only. Missing/not-applicable refs are null. |
| `versions` | Exact release/config/contract/handler versions applicable at the event boundary. |
| `detail.reason_code` | Stable machine code. Human display text is client-owned and not persisted as authority. |
| `detail.retryable` | Boundary-specific retry classification; never inferred solely from HTTP/status. |
| `detail.counts` | Non-sensitive bounded aggregates only. |
| `detail.duration_ms` | Diagnostic non-authoritative duration; null if unavailable. |
| `detail.shortcut_flags` | Explicit demonstration shortcuts such as `POA_FIXTURE_ONLY`, `TEST_TRUST`, `LOCAL_OBJECT_ADAPTER`, `DELIVERY_SIMULATOR`, `INJECTED_FAULT`. |
| `classification` | Always `SYNTHETIC_INTERNAL` for this MVP. |
| `production_decision` | Always `false`; schema validation rejects `true`. |
| `payload_hash` | Hash of the canonical event body excluding `payload_hash`; verified during replay. |

Unknown request fields are rejected. Additive response fields within schema major 1 may be ignored by clients. No event contains arbitrary extensions without a declared bounded extension object in a later version.

## Stage vocabulary

| Stage | Meaning |
|---|---|
| `RUN_INITIALIZATION` | Run identity and fixture scenario selection |
| `TENANT_CONTEXT` | Test trust and immutable tenant/caller context |
| `DATA_RECEIPT` | Raw immutable receipt/reference |
| `SCHEMA_VALIDATION` | Envelope/row structural results |
| `QUARANTINE` | Invalid-row dispositions |
| `NORMALIZATION` | Semantic normalization and dataset publication |
| `CAPABILITY_ELIGIBILITY` | Fixture-only sufficiency decision |
| `JOB_ADMISSION` | Logical job/idempotency creation |
| `JOB_EXECUTION` | Claim, attempt, fence, retry, cancel, failure |
| `FEATURE_GENERATION` | Fixture feature set creation |
| `CANDIDATE_GENERATION` | Fixture candidate set creation |
| `RANKING_RULES` | Fixture scoring, tie-break, filtering, top-k |
| `RESULT_PERSISTENCE` | Owner result commit |
| `FINALIZATION` | Evidence linkage and terminal job transition |
| `RESULT_DELIVERY` | Polling and local delivery simulation, kept separate |
| `REPLAY` | Stored event/resource reconstruction only |

## Status vocabulary

`STARTED | ACCEPTED | SUCCEEDED | FAILED | QUARANTINED | INELIGIBLE | RETRY_SCHEDULED | SKIPPED | REPLAYED | DEGRADED`

`DEGRADED` is limited to diagnostic/export or demo display state. It must not hide a failed mandatory owner operation.

## Required event taxonomy and order

Events marked conditional appear only when their condition occurs. No UI may synthesize a missing required event.

| Order | Event type | Stage | Class | Required / condition | Owner resource effect |
|---:|---|---|---|---|---|
| 1 | `run.initialized` | RUN_INITIALIZATION | real | required | durable run row |
| 2 | `tenant.context.derived` | TENANT_CONTEXT | simplified | required | trusted run context bound |
| 3 | `data.received` | DATA_RECEIPT | real | required | immutable raw ref/digest |
| 4 | `schema.validation.started` | SCHEMA_VALIDATION | real | required | validation run starts |
| 5 | `schema.validation.completed` | SCHEMA_VALIDATION | real | required | validation report committed |
| 6 | `row.quarantined` | QUARANTINE | real | conditional per invalid row or bounded batch summary | quarantine record(s) |
| 7 | `quarantine.completed` | QUARANTINE | real | required, including zero count | quarantine report complete |
| 8 | `normalization.completed` | NORMALIZATION | simplified | if accepted rows exist | normalized object/ref |
| 9 | `dataset.readiness.published` | NORMALIZATION | simplified | required before eligibility | immutable dataset state |
| 10 | `capability.eligibility.evaluated` | CAPABILITY_ELIGIBILITY | simplified | required after READY | eligible/ineligible decision |
| 11 | `run.ineligible` | CAPABILITY_ELIGIBILITY | simplified | conditional when ineligible | terminal run, no job |
| 12 | `job.created` | JOB_ADMISSION | real | required when eligible | one logical job |
| 13 | `job.attempt.claimed` | JOB_EXECUTION | real | per attempt | lease/fence/attempt |
| 14 | `job.execution_recheck.passed` | JOB_EXECUTION | real | per executable attempt | current fixture admission confirmed |
| 15 | `job.attempt.failed` | JOB_EXECUTION | real | conditional | attempt failure truth |
| 16 | `job.retry.scheduled` | JOB_EXECUTION | real | conditional retryable failure | job `RETRY_WAIT` |
| 17 | `feature.generation.completed` | FEATURE_GENERATION | simplified | successful execution | immutable feature-set ref |
| 18 | `candidate.generation.completed` | CANDIDATE_GENERATION | simplified | successful execution | candidate-set ref/count |
| 19 | `ranking.completed` | RANKING_RULES | simplified | successful execution | ranked-set ref/count |
| 20 | `business_rules.applied` | RANKING_RULES | simplified | successful execution | filtered top-k/empty truth |
| 21 | `result.persisted` | RESULT_PERSISTENCE | real | successful allowed outcome | immutable result ref/digest |
| 22 | `job.finalizing` | FINALIZATION | real | after result commit | job `FINALIZING` |
| 23 | `completion_evidence.linked` | FINALIZATION | simplified | required for success | lineage/audit/usage refs |
| 24 | `job.succeeded` | FINALIZATION | real | after evidence | terminal job |
| 25 | `result.polled` | RESULT_DELIVERY | real | at least once in UI demo | authorized read only |
| 26 | `delivery.intent.created` | RESULT_DELIVERY | simulated | S-05 only | simulated intent row |
| 27 | `delivery.attempt.failed` | RESULT_DELIVERY | simulated | S-05 only | simulated delivery failure |
| 28 | `run.replay.accessed` | REPLAY | real | S-06; appended after snapshot | replay-access evidence only |

Additional required failure events are `run.failed`, `job.failed`, and `dataset.readiness.rejected` when their owner states occur. They must use stable reason codes and truthful zero-effect assertions.

## Causation and identity rules

- `run.initialized` has no causation.
- Tenant and data events are caused by the run or preceding owner event.
- The dataset version is caused by the validation/normalization evidence, not by eligibility.
- The job is caused by an eligible decision and pins the dataset/config/handler versions.
- Attempts are caused by the job claim or retry schedule. A new attempt has a new identity and fence but the same job/result identity.
- Feature, candidate, ranking, and result events are caused by the current live attempt.
- Finalization is caused by the committed result, never the reverse.
- Simulated delivery is caused by the committed result and has separate intent/attempt identities.
- Replay uses a snapshot sequence and cannot be the causation of compute or delivery events.

## Storage and transaction rules

- `trace_events` has unique `(tenant_id, run_id, sequence_no)` and unique `event_id` constraints.
- The trace owner allocates sequence numbers with a run-scoped database lock or atomic counter; no process-local counter is authoritative.
- An owner state change and its required trace event commit in one database transaction when they share the accepted local database boundary. Cross-object events reference only a durably committed object/digest.
- Trace insertion is idempotent by stable `event_id` or owner transition/effect key. A retry cannot create a second logical transition event.
- Required trace insertion failure fails/holds the owner transition for this MVP. Optional diagnostic timing enrichment may be omitted.
- Events are immutable. Corrections append a new event referencing the corrected event; no update/delete API exists.
- Demo reset may delete only resources bearing the exact `reference_mvp` profile and fixture namespace, after resolved-target checks.

## API resources

| Route | Purpose | Contract notes |
|---|---|---|
| `GET /demo/v1/runs/{run_id}/events?after_sequence=N` | Incremental polling | Returns ascending events after N and `next_after_sequence`; tenant authorization required |
| `GET /demo/v1/runs/{run_id}` | Run/owner-state summary | UI terminal state derives from owner states, not last event |
| `GET /demo/v1/runs/{run_id}/replay?through_sequence=N` | Stored snapshot replay | Defaults to highest sequence at request start; no compute/effect |
| `GET /v1/jobs/{job_id}` | Authoritative job state | Mirrors final job contract subset |
| `GET /v1/jobs/{job_id}/result` | Authoritative result | Returns bounded result or object ref with fixture warnings |
| `GET /demo/v1/runs/{run_id}/quarantine` | Quarantine summary | Safe reason/count/ref projection only |

Polling is periodic, bounded, and stops when the run and any selected simulated delivery reach terminal state. The server may return `Retry-After`; no SSE/WebSocket requirement is introduced.

## Replay contract

1. Authenticate and derive tenant before resolving the run.
2. Determine `snapshot_sequence = min(requested_sequence, current_max_sequence)`.
3. Read event rows `1..snapshot_sequence` in one consistent snapshot.
4. Validate continuous monotonic ordering, canonical payload hashes, resource ownership, and supported schema major.
5. Return stored events plus authorized run/job/result/quarantine/delivery summaries.
6. Append a separate `run.replay.accessed` event after the snapshot transaction. It is visible only to later polling/replay.

Replay never invokes ingestion, normalization, eligibility, job submission, worker, capability, result commit, or delivery ports. Hash/resource mismatch returns a truthful integrity problem and no partial “successful replay.”

## Privacy, safety, and UI rendering

Allowed detail fields are bounded codes, versions, counts, durations, booleans, opaque refs, and shortcut flags. Prohibited fields include:

- raw transaction/catalog/inventory rows;
- names, phone numbers, emails, addresses, or direct customer identifiers;
- credentials, tokens, connection strings, or filesystem paths;
- arbitrary exceptions, SQL, or stack traces;
- recommendation text presented as scientific/business advice;
- URLs or webhook payloads.

The Gradio timeline groups by `stage`, orders by `sequence_no`, renders stable reason-code descriptions, and visually distinguishes real, simplified, and simulated events. It must show gaps/integrity failures rather than interpolate them.

## Contract tests

- strict schema valid/invalid/unknown-field cases;
- per-run monotonic order under API/worker concurrency;
- duplicate transition insertion/idempotency;
- owner transition plus event atomicity;
- complete required-taxonomy checks per scenario;
- causation/resource/tenant consistency;
- event hash verification and tamper detection;
- no-sensitive-field property/redaction tests;
- polling cursor behavior and terminal stop;
- replay snapshot stability and zero-new-effect assertions;
- cross-tenant event/poll/replay concealment;
- additive response compatibility within major 1 and rejection of unsupported major.

## Production boundary

This contract is a Reference MVP evidence/view contract. It may inform a later observability design, but it is not by itself the production event taxonomy, audit ledger, telemetry schema, event backbone, or external delivery contract. Promoting it requires a separate evidence-backed decision and reconciliation with the full final interface/event contracts.
