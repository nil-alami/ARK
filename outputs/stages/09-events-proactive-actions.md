# Stage 09 — Event and proactive-action architecture

Status: `APPROVED`

## Purpose and scope

Define an implementable, fail-closed path from a configured evaluation trigger to an immutable ML insight, governed control decision, optional ARK job/workflow, and external platform notification. Specify event taxonomy, subscriptions and standing authorizations, routing, versioning, delivery, retry, dead-letter, deduplication, ordering, expiry, throttling, acknowledgement, replay, and audit without introducing an event backbone or granting a capability output authority to act.

This stage refines approved components `C05-04`, `C05-09`, `C05-12`, `C05-18`, `C05-21`, and `C05-22`; the Stage 07 callback boundary; and the Stage 08 scheduler, job, event-handler, and notification seams. It does not select a broker, streaming platform, workflow product, signature algorithm, identity provider, numeric retry/retention/rate policy, direct campaign sender, or named release workflow. Those remain conditional or belong to Stages 12, 13, 15, 17, and 20.

The sponsor explicitly approved Stage 08 and accepted ADR-005 on 2026-08-12 and authorized execution of Stage 09 only. Stage 09 stops after its completion gate for sponsor review before Stage 10.

The sponsor explicitly approved Stage 09 and ADR-006 as written on 2026-08-12 and authorized execution of Stage 10 only.

## Inputs read in full

- `AGENTS.md` — all sections
- `WORKFLOW.md` — all sections
- `STATUS.md` — all sections after recording Stage 08 approval
- `SOURCE_MANIFEST.md` — all sections
- `stages/STAGE-CONTRACT.md` — all sections
- `stages/09-events-proactive-actions.md` — all sections
- `templates/stage-output.md` — all sections
- `templates/adr.md` — all sections
- `sources/normalized/system-design-prompt.md` — **8. Event and proactive-action architecture** exactly
- `sources/normalized/ark-assumptions.md` — all sections, especially **Execution, orchestration, and proactive operation** and **Security, ownership, and operations**
- `outputs/stages/05-end-to-end-architecture.md` — all sections, especially `C05-04`, `C05-12`, `C05-18`, `C05-21`, and `C05-22`
- `outputs/stages/06-data-architecture.md` — all sections, especially four-layer acceptance, freshness, late/corrected data, lineage, and explicit recomputation
- `outputs/stages/07-api-integration.md` — all sections, especially subscriptions, callback registration, idempotency, correlation, and webhook contract
- `outputs/stages/08-execution-orchestration.md` — all sections after approval, especially schedules, event-triggered submission, notification identity, and component responsibilities
- `outputs/stages/01-discovery-and-questions.md` — active `A-01-BUS`, `A-01-SEC`, `A-01-SCALE`, `A-01-OPS`, `INT-04`, `SEC-03`, and `SEC-04`
- `outputs/stages/02-system-definition.md` — `ARK-FR-010`, `ARK-FR-011`, `ARK-NFR-001`, `ARK-NFR-004`, `ARK-NFR-006`, and proactive-action boundary
- `decisions/ADR-002-stage-03-capability-evidence-disposition.md` — `A-03-SYNAPSE`
- `decisions/ADR-003-architecture-style.md` through accepted `decisions/ADR-005-postgresql-job-state-machine.md` — all sections

The Stage 09-authorized `platform_architect` performed a bounded read-only delivery-semantics review. Its findings are reconciled into the two-phase authorization checks, resource identities, delivery state machine, replay semantics, conditional outbox rule, broker rejection, and completion-gate evidence below. The primary agent remains the sole writer.

## Source-instruction coverage

| Source requirement | Addressed in | Status/evidence |
|---|---|---|
| What causes evaluation to run | Evaluation-trigger contract | Addressed with schedule, explicit request, and conditional committed-fact triggers |
| Tenant schedules, permissions, thresholds, and channels | Proactive subscription, standing authorization, and policy records | Addressed; exact values/roles remain activation inputs |
| Output to domain event or actionable insight | Insight-to-decision conversion | Addressed without making output authoritative |
| Event schema | Versioned internal-domain-event example | Addressed |
| Event versioning | Schema/version compatibility rules | Addressed |
| Routing | Deterministic routing and subscription matching | Addressed |
| Subscription management | Capability versus proactive subscription contracts and APIs | Addressed |
| Webhook/other delivery | External notification contract | Webhook conditional; polling remains authoritative; SSE/public feed absent |
| Retry/exponential backoff | Delivery policy | Addressed with required policy values and no invented numbers |
| Dead-letter handling | Delivery state machine and administrative recovery | Addressed as PostgreSQL state, not a new queue product |
| Deduplication | Identity matrix and uniqueness rules | Addressed end to end |
| Ordering | Explicit default and optional ordering contract | Addressed; no global-order claim |
| Expiration | Grant/event/delivery expiry rules | Addressed |
| Throttling | Control quota, cooldown, delivery and runtime limits | Addressed; numeric values remain policy inputs |
| Acknowledgement | Transport and business acknowledgement distinction | Addressed |
| Replay | Authorized replay contract | Addressed without rerunning capability work |
| Audit history | Mandatory decision and delivery evidence | Addressed |
| Internal technical events | Event taxonomy | Distinguished |
| Business/domain events | Event taxonomy | Distinguished |
| Commands | Event taxonomy | Distinguished |
| Notifications | Event taxonomy | Distinguished |
| Actionable ML insights | Event taxonomy and action boundary | Distinguished |

## Facts

1. ARK supports permissioned proactive operation through a standing authorization that scopes capability/workflow, tenant/data, schedule/window, thresholds, configuration, quota, cooldown, validity, and notification destination. `sources/normalized/ark-assumptions.md — Execution, orchestration, and proactive operation`.
2. The governing flow requires ARK to validate permission, threshold, freshness, quota, and deduplication before creating an auditable task; outside the grant, ARK reports the finding without acting. `sources/normalized/ark-assumptions.md — Execution, orchestration, and proactive operation`.
3. ARK is an AI capability platform behind consumers, not the current customer master, campaign sender, or direct business-user UI. `outputs/stages/01-discovery-and-questions.md — A-01-BUS`; `outputs/stages/02-system-definition.md — System boundary`.
4. Tenant/control authority owns subscriptions, entitlements, quotas, grants, and policy; capabilities own scientific eligibility and results. The Synapse verifier is advisory and cannot authorize external action. `outputs/stages/05-end-to-end-architecture.md — C05-04`; `decisions/ADR-002-stage-03-capability-evidence-disposition.md — A-03-SYNAPSE`.
5. Dataset readiness/freshness, platform eligibility, and capability scientific eligibility are separate decisions. Corrected or late data produces a new immutable version; recomputation and redelivery are separate authorized operations. `outputs/stages/06-data-architecture.md — Four-layer acceptance model`; `— Incremental changes, duplicates, corrections, and late data`.
6. Polling is the universal result-recovery path. A registered signed webhook is optional and at least once; delivery failure never changes or reruns a job/result. `outputs/stages/07-api-integration.md — Callback/webhook contract`; `decisions/ADR-004-api-contract-boundary.md — Decision`.
7. The scheduler creates ordinary idempotent jobs. An event handler may map an approved versioned event to one typed job command, but cannot execute capability logic. No broker or internal event path is currently selected. `outputs/stages/08-execution-orchestration.md — Schedule contract and occurrence algorithm`; `— Conditional event-triggered execution`.
8. No named first-release proactive workflow, consumer delivery contract, numeric delivery policy, concrete authorization roles, or production trust protocol is evidenced. `outputs/stages/01-discovery-and-questions.md — INT-04, SEC-03, SEC-04`; `outputs/stages/07-api-integration.md — Open questions`; `outputs/stages/08-execution-orchestration.md — Open questions`.

## Assumptions

Stage 09 introduces no new temporary assumption and does not silently extend an expiry.

| ID | Assumption | Why needed | Architectural effect | Risk | Validation/expiry |
|---|---|---|---|---|---|
| `A-01-BUS` | ARK remains behind consuming platforms and does not own customer-channel delivery | Product boundary remains unanswered | ARK reports/notifies; it does not send campaigns or contact customers | Product boundary may expand | B-01 through B-05 |
| `A-01-SEC` | Least privilege, authenticated tenant binding, auditable grants, and deterministic policy-before-action are mandatory | Exact role/compliance policy is absent | All proactive paths fail closed; verifier remains advisory | Later duties may be stricter | SEC-01 through SEC-06 and authoritative policy evidence |
| `A-01-SCALE` | Rates, volumes, latency, retention, retry, cooldown, and quota values are unknown | Prevents fabricated delivery/capacity claims | Policy references are mandatory; missing concrete activation values block enablement | Production performance remains unproven | S-01 through S-04 / Stage 17 |
| `A-01-OPS` | Support, recovery, and observability targets are unknown; no broker/workflow product is assumed | Prevents premature operational commitments | PostgreSQL records/shared workers first; numeric recovery and placement remain later | Operational fit remains unproven | OPS-01 through OPS-05 |
| `A-03-SYNAPSE` | Synapse is interface-only, advisory, and non-production-eligible | Its policy, safety, state, and reliability internals are undocumented | No proactive Synapse execution, authorization, or external action is enabled | Capability may be scoped out or materially changed | Relevant Stage 10/12/14/15 or enablement decision |
| `A-04-OWNERSHIP` | Logical control, integration, capability, security, and operations roles suffice for design | Named accountable people are absent | Every resource has a logical owner; activation remains blocked without named authorities/runbooks | Staffing/segregation may differ | Existing expiry before Stage 20/extraction/production |
| `A-07-INTEGRATION` | Polling is universal; registered webhook is conditional; consumer adapters stay outside cores | Consumer/trust/delivery evidence remains incomplete | External notification is optional and reference-only; SSE/public feed absent | Consumer needs may differ | Existing per-portion expiry |

`INT-04` remains insight-only/no-unapproved-workflow because no concrete workflow and grant semantics have been approved. Stage 09 defines the required grant mechanism but does not activate a named workflow or direct external action.

## Analysis and recommendations

### Event and action taxonomy

| Type | Meaning | Authority and owner | May trigger work? | Example / prohibited confusion |
|---|---|---|---|---|
| Internal technical event | Operational fact about infrastructure or delivery, primarily for telemetry/recovery | Emitting technical component; never business truth | Only a specifically approved recovery handler | `WebhookDeliveryDeadLettered`; not a customer/business event |
| Business/domain event | Immutable committed domain fact useful to one or more internal consumers | Source domain module owns fact; publication owns delivery only | Yes, only through an approved handler and typed command | `InsightQualified`; not an instruction and not authorization |
| Command | Imperative request to one owner to attempt a state change | Authenticated caller/control/orchestrator; target owner decides | It is the work request | `SubmitProactiveEvaluation`; must be authorized/idempotent and may be rejected |
| External notification | Reference-oriented message telling a platform about an existing fact/resource | Integration owns delivery; source resource remains authoritative | Never by itself inside ARK | Signed webhook; not internal coordination and not campaign execution |
| Actionable ML insight | Immutable capability result that meets a declared scientific/trigger rule and is eligible for control review | Capability owns insight meaning; control plane owns action decision | No direct work until the control decision passes | A churn risk/recommendation; never a grant, command, policy decision, or proof an external action occurred |

An insight may be valuable and “actionable” in business language while still producing `REPORT_ONLY`. Actionability means it is eligible for a governed decision, not that ARK has authority to act.

### Resource and ownership contracts

#### Capability subscription versus proactive subscription

A capability subscription enables entitlement/discovery only; it does not ingest, schedule, evaluate, create a standing authorization, or run work. A separate proactive subscription configures a possible governed task.

```text
ProactiveSubscription {
  proactive_subscription_id, tenant_id, version, state,
  capability_or_named_workflow_ref,
  trigger_policy_ref, threshold_policy_ref,
  dataset_scope_ref, capability_config_ref,
  delivery_channel_ref?, standing_authorization_ref,
  active_from, active_until?, etag,
  created_by, created_at, updated_by, updated_at
}
```

States are `DRAFT | ACTIVE | SUSPENDED | REVOKED | EXPIRED`. `ACTIVE` means configuration is enabled; it does not prove the referenced grant is currently valid. A change creates a new version or uses compare-and-set/ETag; existing evaluations retain exact references.

#### Event subscription and endpoint registration

Endpoint registration establishes only a validated possible destination. It does not subscribe that destination to events and grants no evaluation or action authority. A separate event subscription authorizes routing of exact event types/versions to that endpoint.

```text
EventSubscription {
  event_subscription_id, tenant_id, version, state, etag,
  subscriber_principal_or_application_ref,
  allowed_event_types_and_schema_versions[], bounded_filter_policy_ref?,
  webhook_endpoint_id, webhook_endpoint_version,
  data_classification_ceiling, active_from, active_until?,
  created_by, updated_by, audit_ref
}
```

States are `DRAFT | ACTIVE | SUSPENDED | REVOKED | EXPIRED`. Wildcard event majors, arbitrary routing expressions, and caller-supplied destination URLs are prohibited. Capability subscription, proactive subscription, event subscription, endpoint registration, and standing authorization are five independent records; none creates another.

#### Standing authorization

```text
StandingAuthorization {
  authorization_id, tenant_id, authorization_version, state,
  authorized_principal_or_application_ref, permitted_evaluation,
  authorized_capability_or_workflow_ref,
  allowed_task_types[], allowed_action_scope,
  data_scope_ref, purpose_policy_ref,
  trigger_policy_ref, threshold_policy_ref,
  quota_policy_ref, cooldown_policy_ref,
  delivery_channel_refs[],
  valid_from, valid_until,
  requester_actor_ref, approver_actor_ref,
  approval_policy_ref, revoked_at?, revoked_by?, revocation_reason?,
  created_at, approved_at?, state_version
}
```

States are `DRAFT | PENDING_APPROVAL | ACTIVE | SUSPENDED | REVOKED | EXPIRED`. The grant is tenant-scoped, immutable once active except through a new version or explicit state transition, and can only narrow upstream authority. Exact requester/approver/revoker role bindings and any dual-control requirement are Stage 12 activation inputs; absence blocks activation rather than creating a default administrator.

#### Trigger and threshold policy

The versioned trigger policy declares one or more allowed trigger types, schedules/windows/time zone, dataset/source applicability, minimum data/readiness/freshness policy, misfire behavior, and occurrence identity. Threshold policy contains capability-owned supported metric semantics plus tenant-selected values within an approved capability definition. A tenant cannot redefine model meaning or bypass capability scientific eligibility.

#### Action decision

```text
ActionDecision {
  decision_id, tenant_id,
  proactive_subscription_id, subscription_version,
  event_subscription_id?, event_subscription_version?,
  authorization_id, authorization_version,
  trigger_id, trigger_type, trigger_policy_ref,
  insight_ref, capability/version/operation refs,
  dataset_version_ref, freshness_policy_ref, freshness_evidence_ref,
  threshold_policy_ref, threshold_evidence_ref,
  deterministic_policy_ref, policy_evidence_ref,
  quota_reservation_ref?, cooldown_key?, dedupe_key,
  disposition, reason_codes[],
  authorized_task_ref?, notification_intent_refs[],
  correlation_id, causation_id, evaluated_at, expires_at
}
```

Disposition is one of `REPORT_ONLY | SUPPRESSED | AUTHORIZED_TASK_SUBMITTED | NOTIFICATION_ONLY | EXPIRED`. It never records that a downstream customer-channel action occurred. `AUTHORIZED_TASK_SUBMITTED` is legal only for an exact ARK task or approved named workflow in the active grant; no named workflow is active now.

### Evaluation-trigger contract

| Trigger | Status now | Identity and behavior | Constraint |
|---|---|---|---|
| Versioned schedule occurrence | Supported | `{tenant, subscription version, schedule version, scheduled_for}`; scheduler submits an evaluation job | Recheck grant/window/freshness at execution; no hidden process-local schedule |
| Explicit authenticated evaluation request | Supported as ordinary command | Stage 07 idempotency scope plus exact subscription/grant refs | It is user-requested, not independent proactive discovery; same gate still applies |
| New ready dataset version | Conditional | Committed dataset fact + handler version + subscription version dedupe | Requires approved internal domain event/outbox path and source-specific freshness semantics |
| Capability insight/result commit | Conditional | Immutable insight/result identity + handler/subscription version | Does not fire merely because a job state changed; no recursive rerun |
| Approved external/domain input event | Conditional | Authenticated producer event ID + schema/handler version | Stage 12 trust and explicit source contract required |
| Continuous threshold polling/stream processing | Not justified | None selected | Requires approved latency/volume/window/watermark/checkpoint evidence and Stages 15/17 gate |

The first viable proactive mechanism is scheduled evaluation through the accepted scheduler/job manager. Internal-event triggers remain inactive until a named consumer needs temporal decoupling. A threshold is normally evaluated on an immutable result/insight; it is not itself an unbounded trigger loop.

### Two-phase fail-closed decision order

The checks occur at two boundaries so ARK cannot spend resources under an invalid configuration and cannot act on authority that expired during computation.

#### Phase A — evaluation admission

| Order | Mandatory check | Owner | Failure behavior |
|---:|---|---|---|
| 1 | Authenticated tenant and trigger provenance | Edge/control/event adapter | Reject/quarantine; no job |
| 2 | Active capability entitlement and proactive subscription/version | Control plane | Record `SUBSCRIPTION_INACTIVE`; no job |
| 3 | Active standing authorization permits evaluation task, scope, window, and configuration | Control/security policy | Record `AUTHORIZATION_MISSING/EXPIRED/REVOKED`; no job |
| 4 | Dataset/source scope, readiness, policy compliance, and freshness evidence | Data catalog/control | Record reportable not-ready/stale outcome if allowed; no action |
| 5 | Evaluation quota/rate and runtime admission | Control/job manager | Reject/defer according to versioned policy; no hidden queue |
| 6 | Trigger/occurrence dedupe and cooldown applicable before evaluation | Control/job manager | Return existing decision/job or suppress duplicate |
| 7 | Mandatory admission audit | Audit owner | Fail closed; no sensitive proactive job |
| 8 | Submit typed durable evaluation job | Job manager | Normal Stage 08 idempotency/state machine |

#### Phase B — post-insight task/notification decision

| Order | Mandatory check | Owner | Failure behavior |
|---:|---|---|---|
| 1 | Immutable insight/result exists with exact lineage and scientific outcome | Capability/data owner | No action; truthful failure/ineligible/degraded result |
| 2 | Capability/proactive subscription and standing authorization are still active and still cover exact task/data scope | Control/security policy | `REPORT_ONLY` or `SUPPRESSED`; never broaden scope |
| 3 | Dataset/result freshness and revocation/tombstone state still satisfy policy | Data catalog/control | `REPORT_ONLY`/`SUPPRESSED`; no stale action |
| 4 | Versioned scientific trigger threshold passes | Capability-owned semantics + control reference | `REPORT_ONLY`; threshold failure is not execution failure |
| 5 | Deterministic policy/purpose/channel/action rule passes | Control/security policy | `REPORT_ONLY`/`SUPPRESSED`; Synapse verifier output is advisory only |
| 6 | Action/delivery quota reservation, cooldown, and per-scope throttle pass atomically | Control plane | Suppress/defer with reason; no double consumption |
| 7 | Decision/action/event/delivery dedupe keys are unclaimed or replay-identical | Owning modules | Return existing logical resources; conflicting reuse fails |
| 8 | Mandatory action-decision audit commits with exact evidence/version refs | Audit/control owner | Fail closed; no task or external notification intent |
| 9 | For notification, require an active matching event subscription and registered endpoint/version | Integration/control | No notification intent if routing/destination authority is absent |
| 10 | Commit decision, quota/cooldown/dedupe reservation, mandatory audit evidence, and producer-owned typed command/notification intents without a crash gap | Control plus owner ports | Only grant-listed task; no direct cross-module table write |
| 11 | Idempotent intent handlers submit the exact Stage 08 job/workflow command and/or integration delivery record | Job manager/integration | Intent retry returns the same logical resource; delivery remains separate |

In the initial same-codebase/PostgreSQL placement, owner module ports may participate in one transaction while preserving one authoritative writer per table. If a later extraction removes that transaction boundary, the producer-owned outbox/intent is the durable handoff and requires a superseding reliability design. At execution/delivery time, the responsible worker rechecks time-sensitive subscription, authorization, destination, freshness/revocation, and policy evidence before any irreversible external effect. A stale or revoked decision is denied/reconciled, not executed. Revocation wins for future work and any not-yet-authorized task. A committed immutable insight remains evidence. A task already durably accepted follows explicit cancellation/reconciliation policy; ARK never claims revocation undid an external effect.

### Identity and deduplication matrix

| Layer | Stable logical identity | Duplicate behavior |
|---|---|---|
| Trigger occurrence | Tenant + subscription/trigger version + schedule/event/source occurrence | One evaluation admission decision |
| Evaluation job | Stage 08 submission key derived from trigger identity + exact operation versions | Same job returned; changed request conflicts |
| Insight | Capability-owned result/insight ID + immutable version lineage | Never recomputed solely for delivery replay |
| Action decision | Subscription version + authorization version + insight + policy versions | One logical decision; changed policy creates a new decision identity |
| Authorized ARK task | Decision ID + exact task/workflow/version | One logical job/workflow command |
| Domain event | Producer + event type/major + committed source fact + decision | One immutable logical `event_id` |
| Subscription routing | Event ID + event-subscription/endpoint versions | One consumer publication record |
| External notification | Event/notification ID + webhook endpoint version | One logical delivery with multiple attempt IDs |
| Replay | Original event/delivery identity + authorized replay request ID | New attempt, not a new fact/result/action |

### Insight-to-event conversion

1. The capability commits an immutable result/insight with exact dataset, model/artifact, feature, code, configuration, policy, and execution references.
2. The control evaluator creates an immutable `ActionDecision` after the Phase B checks. A capability cannot write this record or choose its disposition.
3. `REPORT_ONLY` remains a queryable result and may produce an authorized informational notification. It cannot create an action command.
4. `AUTHORIZED_TASK_SUBMITTED` creates one typed idempotent Stage 08 job or an approved named-workflow command. No named workflow is active in this stage.
5. A business/domain event is created only when an approved internal subscriber requires the committed fact. Event creation is not automatic for every result or state transition.
6. If internal publication is activated, the source owner commits the fact plus an outbox/publication record transactionally. A shared publisher provides at-least-once delivery to an idempotent handler. The source fact, not the outbox/broker, remains authority.
7. External notification uses a separate `NotificationIntent` and delivery records. When a webhook promise follows a control decision, the decision transaction also records a producer-owned notification/outbox intent so a crash cannot lose the promised publication. A webhook is never reused for internal coordination.

### Subscription management and APIs

The Stage 07 common HTTP rules apply: authenticated principal-derived tenant, required idempotency for mutations, ETag/`If-Match` concurrency, opaque IDs, bounded versioned schemas, no caller-supplied tenant authority, and no arbitrary callback URL.

| Endpoint | Responsibility | Activation/security constraint |
|---|---|---|
| `GET /v1/proactive-subscriptions` | List authorized tenant-scoped proactive configurations | Read scope; bounded pagination |
| `POST /v1/proactive-subscriptions` | Create idempotent draft configuration | Cannot activate or create authority |
| `PUT /v1/proactive-subscriptions/{id}` | Version/update configuration with `If-Match` | Active version must reference valid approved policies and registered endpoint |
| `POST /v1/proactive-subscriptions/{id}:activate` | Request activation | Requires active standing authorization and concrete activation policies |
| `POST /v1/proactive-subscriptions/{id}:suspend` | Prevent future occurrences | Does not silently cancel accepted jobs or erase insights |
| `GET /v1/event-subscriptions` | List tenant-scoped exact event routes | Separate from capability/proactive subscription and endpoint registration |
| `POST /v1/event-subscriptions` | Create an idempotent draft route to a registered endpoint/version | Exact event types/schema majors and bounded filters only; no wildcard/dynamic expression |
| `PUT /v1/event-subscriptions/{id}` | Version/update route with `If-Match` | Cannot activate evaluation/action or broaden standing authorization |
| `POST /v1/event-subscriptions/{id}:suspend` | Stop new notification routing | In-flight delivery follows explicit cancellation/reconciliation policy |
| `POST /v1/standing-authorizations` | Create a draft grant request | Privileged role mapping remains Stage 12 input |
| `POST /v1/standing-authorizations/{id}:approve` | Activate exact immutable grant version | Requires approved approver/segregation policy; no self-approval unless explicitly allowed |
| `POST /v1/standing-authorizations/{id}:revoke` | Revoke future authority with reason | Mandatory audit; pending work reconciled explicitly |
| `GET /v1/action-decisions/{id}` | Retrieve reasons/evidence/status | Tenant/resource authorization; sensitive details minimized |
| `POST /v1/webhook-deliveries/{id}:replay` | Authorized redelivery of the same logical notification | Does not rerun result, decision, or ARK task |

Exact role names, approval separation, signature controls, and numeric policies are required before endpoint activation and remain Stage 12/13 inputs.

### Versioned internal domain-event schema example

This example defines a contract, not an activated event stream or broker.

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

Internal payloads use trusted tenant scope but remain minimal and reference-oriented. Actionable-insight payloads carry capability/result/lineage/evidence references and validity, but never an `authorized=true` field. Secrets, prompts, raw PII, arbitrary URLs, and large results are prohibited.

### Versioned external webhook schema example

```http
POST <pre-registered authorized endpoint>
Content-Type: application/json
X-ARK-Event-ID: evt_opaque
X-ARK-Delivery-ID: delivery_attempt_opaque
X-ARK-Timestamp: 2026-08-12T12:00:02Z
X-ARK-Signature: <versioned-signature>
```

```json
{
  "event_version": "1.0",
  "event_id": "evt_opaque",
  "event_type": "ark.insight.available.v1",
  "occurred_at": "2026-08-12T12:00:00Z",
  "expires_at": "2026-08-13T12:00:00Z",
  "tenant_ref": "tenant_opaque",
  "subject": {"type": "insight", "id": "insight_opaque"},
  "correlation_id": "corr_opaque",
  "data": {
    "capability_id": "churn",
    "outcome": "ELIGIBLE",
    "disposition": "REPORT_ONLY",
    "insight_url": "/v1/insights/insight_opaque",
    "decision_url": "/v1/action-decisions/decision_opaque"
  }
}
```

External `tenant_ref` is informational and cannot establish authority. URLs are ARK-relative resource references, not raw object paths. A webhook saying `AUTHORIZED_TASK_SUBMITTED` reports an existing ARK task reference; it never instructs the receiving platform to contact a customer unless a separate external consumer contract and grant are later approved.

### Schema versioning and routing

- Event type carries a major version suffix; `schema_version` records exact schema. Additive optional fields may evolve within the major. Changed meaning, required fields, identity, ordering, or authority semantics requires a new major/event type.
- Producers store canonical payload or payload hash plus immutable source/version references. Consumers reject/quarantine unsupported major versions; they do not guess.
- Routing is a deterministic match over exact tenant, active event/proactive subscription version, event type/major, subject/capability/workflow, allowed data/action scope, and registered destination. No arbitrary expression language or dynamic code is accepted.
- One event may route to several explicitly registered subscribers, each with independent publication/delivery state. Fan-out count alone does not select a broker.
- Default ordering is none. If a contract requires order, it declares `ordering_key`, monotonic `sequence`, gap/late policy, and serialized consumer scope. Global or cross-tenant order is prohibited and unsupported.

### External delivery state and semantics

```text
NotificationIntent {
  notification_id, tenant_id, event_id, event_type/version,
  subject_ref, endpoint_id, endpoint_version,
  payload_or_ref, payload_hash,
  policy_ref, ordering_key?, sequence?,
  state, next_attempt_at?, expires_at,
  attempt_count, last_error_code?,
  correlation_id, created_at, acknowledged_at?
}
```

States are `PENDING | DELIVERING | RETRY_WAIT | ACKNOWLEDGED | DEAD_LETTERED | EXPIRED | CANCELLED`.

```text
DeliveryAttempt {
  delivery_id, notification_id, attempt_number, replay_generation,
  notification_job_id, job_attempt_id, fence_ref,
  endpoint_id, endpoint_version,
  signature_policy_ref, signing_key_version_ref,
  started_at, finished_at?, timeout_policy_ref,
  response_status_class?, bounded_response_metadata?,
  retry_class?, error_code?, next_attempt_at?, replay_parent_id?
}
```

1. A short fenced claim changes `PENDING/RETRY_WAIT → DELIVERING`; computation/network call holds no database lock.
2. A 2xx response is transport acknowledgement for that attempt and commits `ACKNOWLEDGED`. It does not prove the consumer performed a business action.
3. Timeout, connection failure, retryable 408/429/5xx, and policy-listed errors schedule bounded exponential backoff with jitter. Base, cap, maximum attempts, total delivery deadline, per-attempt timeout, and `Retry-After` treatment are mandatory versioned policy values; no values are invented here.
4. Permanent destination/payload/auth failures, unsupported schema, exhausted attempts, or expired delivery become `DEAD_LETTERED` or `EXPIRED` with a stable reason. This is PostgreSQL delivery state and an operator view, not a new queue/DLQ product.
5. The same logical `event_id`/notification is delivered at least once; every attempt has a new `delivery_id`. Consumers deduplicate by `event_id`; attempt diagnostics use `delivery_id`. The shared job manager may schedule notification work under the `notification` routing class, but delivery state remains owned by integration and never becomes job/result truth.
6. Endpoint disable/revocation stops new claims. Pending intents become `CANCELLED` or remain held according to explicit policy; an in-flight ambiguous response is reconciled, not declared undone.
7. Polling/result/insight APIs remain authoritative even after dead-letter or expiry. Delivery failure never reruns capability computation, changes the action decision, or consumes action quota twice.

### Throttling, cooldown, expiry, acknowledgement, and replay

- Control quota and cooldown apply before task/notification intent creation and use transactional reservation/unique keys. Delivery throttling is separate and scoped by tenant, subscription, endpoint, event type, and global destination safety policy.
- Runtime concurrency limits remain Stage 08 job/delivery worker controls; commercial quota, scientific threshold, cooldown, and transport rate limit are not collapsed.
- Grant, subscription, trigger occurrence, insight relevance, event, and delivery may each expire independently. No action or delivery may be created after the earliest applicable authority/freshness expiry. Expiry never mutates the underlying immutable insight.
- HTTP 2xx acknowledges receipt of a delivery attempt. If a future consumer requires business acknowledgement, it must be a separate authenticated, idempotent command/resource with its own deadline and semantics; silence is never approval.
- Replay requires an authorized operator/API command, reason, original event/delivery reference, destination still authorized, schema compatibility, and expiry/retention policy. Replay creates a new delivery generation/job and attempt under the same logical event/notification identity and preserves payload hash/schema/source fact. It never reruns the capability, reevaluates the grant, recreates an action, or changes the original occurred time.
- Re-evaluation after new data/policy is a new explicit evaluation/decision identity, not replay.

### Internal reliable publication and broker disposition

`C05-21` remains conditional, not a platform-wide required component. Direct module ports plus PostgreSQL jobs/schedules satisfy current approved flows. If a named internal domain-event subscriber is activated, reliable publication becomes mandatory for that path and uses a producer-owned transactional outbox plus a shared same-codebase publisher and idempotent handler with uniqueness on `{event_id, handler_version}`. A promised external webhook likewise requires its notification/outbox intent to commit without a crash gap from the source control decision. Each consumer has explicit publication state, retry/dead-letter/replay policy, compatible schema versions, and owner/runbook.

No broker is selected. A broker requires accepted ADR-005's measured fan-out/replay/ordering/independent-boundary or dispatch trigger, a named owner/on-call/runbook, security and tenant isolation, retention/recovery/cost evidence, and proof that direct calls, jobs, and PostgreSQL outbox cannot meet an approved need. Adding transport never moves source fact, job, grant, decision, or result authority into the broker.

### Audit history

Mandatory append/supersede audit evidence includes:

- capability/proactive/event subscription and endpoint-registration creation, version change, activation, suspension, revocation, and expiry;
- standing-authorization request, approval, rejection, suspension, revocation, expiry, actor, role/policy, and reason;
- trigger receipt/occurrence, provenance, duplicate/cooldown/quota decision, and evaluation job identity;
- exact dataset/freshness, capability/model/config, threshold, policy, grant, and subscription versions used;
- every Phase A and Phase B allow/deny/suppress/report-only reason;
- quota/cooldown reservation, release/consumption, authorized task command, and reconciliation;
- event creation, subscription routing, publication/delivery attempt, acknowledgement, retry, dead-letter, expiry, cancellation, replay, and replay actor/reason;
- correlation/causation from source data and insight through decision, job/workflow, event, notification, and consumer acknowledgement.

Mandatory audit failure prevents standing-authorization mutation, proactive task submission, and external notification-intent creation. Diagnostic telemetry failure remains separate and is resolved in Stage 14.

### Failure and recovery matrix

| Failure | Authoritative state | User/platform-visible outcome | Retry/recovery | Forbidden behavior |
|---|---|---|---|---|
| Capability/proactive/event subscription, endpoint, or grant absent, expired, revoked, or mismatched | Control/integration records | `REPORT_ONLY`/suppressed/no-delivery reason | New authority/version required | Infer permission from enablement, endpoint, or capability output |
| Dataset stale/not ready/revoked | Catalog evidence | No proactive task; explicit data reason | New dataset/evaluation | Act on old result silently |
| Threshold/policy fails or ambiguous | Decision record | Report-only/suppressed | Re-evaluate only under new input/policy | Treat verifier `accepted` as authority |
| Quota/cooldown/dedupe blocks | Control reservation/decision | Existing resource, deferred, or suppressed | Policy-defined later trigger | Double consume or bypass under retry |
| Audit commit unavailable | Audit/control transaction | No task/notification intent | Safe retry before effect | Perform sensitive action then backfill audit |
| Evaluation/job fails | Job/owner result | Truthful job failure/outcome | Stage 08 retry policy | Delivery retry reruns job |
| Webhook times out | Delivery attempt | Pending/retry/ambiguous; polling works | Bounded backoff or reconciliation | Assume not received and create new event |
| Permanent delivery failure/exhaustion | `DEAD_LETTERED` | Result/insight remains available | Authorized replay after correction | Change result/action decision |
| Unsupported internal event version | Consumer publication record | Quarantined/dead-letter with lag visible | Deploy compatible handler or authorized replay | Guess schema/meaning |
| Revocation races accepted task/delivery | Versioned control + CAS state | Future work stopped; in-flight reconciled | Cancellation where contract permits | Claim external effect was undone |

### R-09-01 — Separate configuration, authority, insight, decision, work, and delivery

**Requirement/where:** `ARK-FR-001/006/010/011`, `ARK-NFR-001/004/006`; proactive flows in Stages 09/12/13/22. **Why now:** collapsing these records lets enablement or an ML result become accidental authority. **Simplest implementation:** module-owned PostgreSQL records with exact version references and typed ports. **Alternative:** one “proactive event” object or capability-owned automation. **Why rejected:** hides owners, checks, failure truth, and revocation. **Burden:** more explicit state and reconciliation. **Reconsideration:** only a superseding requirement can merge records without weakening independent authority/audit.

### R-09-02 — Use a two-phase, fail-closed proactive gate

**Requirement/where:** `ARK-FR-010`, `A-01-SEC`, source assumption 24; schedule/event admission and post-insight action. **Why now:** authority, freshness, quota, and policy can change while an evaluation runs. **Simplest implementation:** Phase A admission plus Phase B action-decision transactions using immutable evidence refs and compare-and-set. **Alternative:** validate only at schedule or API admission. **Why rejected:** creates time-of-check/time-of-use bypass. **Burden:** extra reads, version checks, reservations, and explicit reasons. **Reconsideration:** never remove the Phase B recheck; optimize only with proven equivalent consistency.

### R-09-03 — Keep scheduled jobs as the first proactive trigger and internal events conditional

**Requirement/where:** `ARK-CON-005/007`, `ARK-FR-011`; Stages 09/13/15/17. **Why now:** schedules/jobs are approved and sufficient; no internal subscriber or throughput need is named. **Simplest implementation:** scheduler submits ordinary evaluation jobs; direct ports observe results. Activate a transactional outbox only for a concrete subscriber. **Alternative:** broker/event backbone/continuous processor now. **Why rejected:** unsupported ordering, replay, security, retention, and operations burden. **Burden:** PostgreSQL publisher/reconciliation if an event path activates. **Reconsideration:** ADR-005 broker triggers or an approved named independent subscriber that direct/job coordination cannot satisfy.

### R-09-04 — Make external delivery at least once and independent from result/action truth

**Requirement/where:** `ARK-FR-011`, `ARK-NFR-004/006`, accepted ADR-004; platform notification flows. **Why now:** retries, timeout ambiguity, dead-letter, and replay must not duplicate computation or authority. **Simplest implementation:** registered endpoint, immutable notification intent, PostgreSQL delivery attempts, bounded policy backoff, consumer dedupe by `event_id`, and polling recovery. **Alternative:** webhook-only result truth, capability-owned callbacks, SSE/public event feed, or broker. **Why rejected:** couples computation/delivery or lacks evidence. **Burden:** destination validation, secret rotation, retry/replay tooling, and runbooks. **Reconsideration:** approved consumer contract proves a different protocol is necessary while preserving authoritative polling/reconciliation.

## Decisions

- Propose `decisions/ADR-006-governed-proactive-action-and-delivery.md`: capability/proactive/event subscriptions, endpoint registration, authority, insight, control decision, ARK task, internal event, and external notification remain separate authoritative records and contracts.
- Scheduled durable evaluation is the first supported independent trigger. Explicit requests are ordinary commands. Dataset/result/external event triggers remain conditional on a named approved contract and reliable publication path.
- No named proactive workflow, direct customer-channel action, broker, event backbone, continuous processor, SSE/public event feed, or general workflow engine is activated.
- A capability output—including Synapse campaign-verifier `accepted`—never authorizes a task or delivery. Deterministic control policy and an active exact standing authorization remain authoritative.
- Internal reliable publication is required only for an activated internal event boundary and begins with a transactional outbox/shared publisher; it is not universal infrastructure.
- External webhooks remain optional at-least-once notifications over registered endpoints. Polling/resource APIs remain authoritative.
- Numeric retry/backoff/expiry/retention/quota/cooldown/throttle values, trust/signature controls, concrete authorization roles, and named workflows remain unresolved activation inputs.

These are Stage 09 recommendations and proposed ADR-006 pending sponsor review. No accepted ADR is superseded and no later-stage production activation is implied.

## Contradictions and dangerous assumptions

| ID | Tension/hazard | Treatment | Consequence |
|---|---|---|---|
| `C-09-01` | “Actionable insight” sounds like permission to act | It means eligible for control review only | Insight can remain `REPORT_ONLY` |
| `C-09-02` | Capability subscription can be confused with proactive authorization | Separate proactive subscription and standing authorization | Enabling a capability never schedules or runs it |
| `C-09-13` | Endpoint registration or event subscription can be confused with evaluation/action authority | Keep both separate from capability/proactive subscription and standing authorization | Routing/destination enablement never authorizes work |
| `C-09-03` | Synapse verifier returns `accepted` | Advisory evidence only; deterministic control policy wins | No LLM-only authorization or action |
| `C-09-04` | Baseline says proactive flow sends webhook, while no consumer delivery contract/security values exist | Webhook contract is conditional and activation-blocked; polling/reporting remains valid | No unsupported delivery promise |
| `C-09-05` | Baseline says reliable publication eventually uses outbox, but no internal subscriber is named | Outbox is mandatory only when a concrete internal event path activates | No unused event infrastructure |
| `C-09-06` | At-least-once delivery can duplicate downstream effects | Logical event ID stable; consumer dedupe and separate business command required | No exactly-once claim |
| `C-09-07` | Global ordering is often assumed from a queue | Default unordered; specific key/sequence/gap contract required | Consumers cannot infer order from timestamps |
| `C-09-08` | Retry/replay can be mistaken for recomputation or reauthorization | Delivery replay retains original event/decision; re-evaluation is a new command | No duplicate model work/action quota |
| `C-09-09` | Revocation can race an accepted task or ambiguous webhook | Stop future work and reconcile in-flight state; do not claim rollback | Accurate audit and cancellation semantics |
| `C-09-10` | DLQ terminology may imply a broker product | Dead-letter is explicit PostgreSQL publication/delivery state | No new queue authority/product |
| `C-09-11` | Tenant-selected thresholds could redefine scientific semantics | Capability defines supported metrics/ranges; tenant selects only within policy | Scientific ownership preserved |
| `C-09-12` | External notification can be mistaken for campaign sending | Notification reports ARK facts/resources only | Channel execution remains outside ARK under `A-01-BUS` |

## Open questions

| ID | Question | Blocking? | Options | Recommended temporary treatment | Effect |
|---|---:|---|---|---|---|
| `Q-09-01` | Which named proactive use case/workflow is first release scope? | Before workflow/event activation | Insight only; scheduled single capability; named deterministic workflow | Keep insight/reporting plus scheduled evaluation contract; no named workflow | Avoids speculative orchestration/action |
| `Q-09-02` | Who may request, approve, revoke, audit, and operate standing authorizations; is dual control required? | Before grant endpoint activation / Stage 12 | Tenant admin; platform admin; dual control; human approval | Require policy-bound distinct logical roles; no default binding | Mechanics implementable; production authority blocked |
| `Q-09-03` | Which exact ARK tasks/actions and external channels may each grant authorize? | Before action activation | Evaluate/report; notify platform; named workflow; later external command | Only evaluate/report/notify ARK resource references now | No direct channel action |
| `Q-09-04` | What schedules/windows/time zones, thresholds, freshness rules, quotas, cooldowns, throttle rates, and expiries apply? | Before subscription activation | Per use case/tenant policy | Require concrete versioned values; do not invent defaults | Activation blocked, design remains implementable |
| `Q-09-05` | Which consumers require webhook, their endpoint/security contract, and delivery SLO/retry/retention policy? | Before webhook activation / Stages 12/13/17 | Polling only; webhook per consumer; another protocol | Polling universal; webhook conditional | No unsupported delivery guarantee |
| `Q-09-06` | Is any internal dataset/result/domain event subscriber required now? | Before outbox activation | Direct/job observation; PostgreSQL outbox; broker | None until named; outbox first when approved | Keeps `C05-21` conditional |
| `Q-09-07` | Does any event type require per-key ordering or business acknowledgement? | Before ordered/acknowledged contract | Unordered; per-key sequence; separate ack command | Unordered and transport-ack only | Avoids hidden blocking semantics |
| `Q-09-08` | What event/delivery/audit/idempotency retention and replay window apply? | Before production / Stages 12/13 | Policy by class/tenant | Required policy refs; no guessed duration | Replay/expiry tooling cannot be numerically configured |
| `Q-09-09` | Who owns proactive control, event schemas, delivery endpoints/workers, dead-letter reconciliation, and on-call? | Before production / Stage 20 | Assign named roster | Logical roles under `A-04-OWNERSHIP` | Design proceeds; operation remains blocked |
| `Q-09-10` | Can authoritative Synapse policy/safety/reliability evidence be supplied, or should proactive Synapse uses be scoped out? | Before Stage 10/12/enablement | Supply evidence; scope out; remain unavailable | Continue `A-03-SYNAPSE` | No Synapse proactive path |

## Requirements-traceability updates

| Requirement | Stage 09 design response | Verification direction |
|---|---|---|
| `ARK-FR-001` | Capability subscription, proactive subscription, and execution remain separate | Enablement-never-executes negative tests |
| `ARK-FR-006` | Readiness, platform control, scientific outcome, and action decision remain separate | Outcome/decision matrix tests |
| `ARK-FR-007` | Evaluation/action tasks use accepted Stage 08 durable lifecycle | Schedule/event duplicate and restart tests |
| `ARK-FR-010` | Two-phase standing-authorization, freshness, threshold, policy, quota, cooldown, dedupe, audit gate plus execution-time recheck | Exhaustive no-action negative suite and race tests |
| `ARK-FR-011` | Internal events, commands, actionable insights, and external notifications have distinct contracts/owners | Schema/routing/authority boundary tests |
| `ARK-FR-012` | Audit/lineage from source through insight, decision, task, event, and delivery | LAB end-to-end evidence trace |
| `ARK-NFR-001` | Tenant/auth scope on grants, subscriptions, decisions, events, deliveries, quotas, and audit | Cross-tenant read/write/route/replay tests |
| `ARK-NFR-002/003` | Exact source/data/model/config/policy/grant/schema versions and bounded reference payloads | Reproduction and compatibility tests |
| `ARK-NFR-004` | At-least-once event/delivery with stable logical identities and idempotent handlers | Duplicate, timeout, crash, stale-claim, replay fault injection |
| `ARK-NFR-005` | Opaque references/minimal event payloads; no raw PII/secrets | Schema/log/payload privacy scans |
| `ARK-NFR-006` | Correlation/causation across every decision and attempt | Trace completeness/reconciliation tests |
| `ARK-NFR-007` | Missing numeric activation policies remain visible/blocking | Policy-completeness and Stage 17 measurement tests |
| `ARK-CON-001/002` | Same-codebase owner modules and one writer; no event service proliferation | Dependency/schema ownership tests |
| `ARK-CON-005` | PostgreSQL jobs/delivery/outbox first; broker only by accepted trigger | Recovery/load evidence and ADR gate |
| `ARK-CON-007` | No broker/workflow/streaming/action product without evidence | Anti-overengineering challenge |
| `SC-02-04/05/06/08/09/10/12` | Truthful failure, replay, isolation, no action, ownership, and target blocks | Named contract/security/recovery suites |

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Every governing event/proactive bullet addressed | PASS | Source-instruction coverage maps every item |
| Evaluation triggers and tenant configuration implementable | PASS | Trigger, subscription, authorization, and policy contracts |
| Insight/domain-event/action conversion explicit | PASS | Taxonomy, decision record, and conversion flow |
| Internal events, domain events, commands, notifications, and actionable insights distinct | PASS | Event and action taxonomy |
| Versioned event and webhook examples present | PASS | Two concrete schemas plus compatibility rules |
| Routing/subscription/delivery semantics implementable | PASS | Deterministic routing, APIs, delivery record/state machine |
| Retry/backoff/dead-letter/dedupe/ordering/expiry/throttle/ack/replay addressed | PASS WITH ACTIVATION VALUES OPEN | Semantics explicit; numeric/security policy values correctly remain required inputs |
| Proactive action cannot bypass subscription | PASS | Phase A step 2 and Phase B step 2 |
| Proactive action cannot bypass explicit authorization | PASS | Standing authorization and both-phase recheck |
| Proactive action cannot bypass data freshness | PASS | Phase A step 4 and Phase B step 3 |
| Proactive action cannot bypass thresholds | PASS | Phase B step 4 |
| Proactive action cannot bypass deterministic policy | PASS | Phase B step 5; verifier advisory only |
| Proactive action cannot bypass quota | PASS | Phase A step 5 and Phase B step 6 |
| Proactive action cannot bypass cooldown | PASS | Phase A step 6 and Phase B step 6 |
| Proactive action cannot bypass deduplication | PASS | Phase A/Phase B checks and identity matrix |
| Proactive action cannot bypass audit | PASS | Phase A step 7, Phase B step 8, fail-closed audit rule |
| Execution/delivery cannot rely on a stale earlier decision | PASS | Mandatory time-sensitive recheck before irreversible external effect |
| Report versus act boundary unambiguous | PASS | Dispositions and no direct campaign/channel action |
| Reliable publication is crash-safe and narrowly scoped | PASS | Outbox for a named internal subscriber or promised webhook intent; no platform-wide event backbone |
| Broker/stream/workflow products rejected without evidence | PASS | Internal publication/broker disposition and anti-overengineering recommendations |
| Authorized platform delivery review reconciled | PASS | Review findings incorporated into two-phase checks, identities, delivery states, replay/outbox rules, and open activation inputs |
| Proposed ADR-006 recorded | PASS | `decisions/ADR-006-governed-proactive-action-and-delivery.md` |
| Stage 10 not executed | PASS | No Stage 10 output or decision created |
| Sponsor-requested review before Stage 10 | **PASS** | Sponsor explicitly approved Stage 09 and ADR-006 on 2026-08-12 |

**Gate result: PASSED AND APPROVED.** The proactive path is fail-closed and cannot bypass subscription, authorization, freshness, threshold, deterministic policy, quota, cooldown, deduplication, or mandatory audit. Missing roles, trust controls, named workflows, and numeric policies block activation rather than stage-level logical design. The sponsor explicitly approved Stage 09 and ADR-006 on 2026-08-12; Stage 10 is authorized to begin.

## Downstream consequences

- Stage 10 must define per-capability insight/result semantics, approved scientific thresholds, evaluation evidence, model/artifact/config versions, and capability eligibility without granting control authority.
- Stage 11 must not infer agentic behavior from proactive workflows or Synapse names.
- Stage 12 must bind authentication/roles, grant approval/revocation/segregation, purpose/consent, webhook signatures, destination verification, replay protection, secrets, and provider/data-transfer policy.
- Stage 13 must set retry/backoff/deadline/retention, ambiguous acknowledgement, endpoint health, dead-letter/replay, database/outbox recovery, and runbook semantics.
- Stage 14 must instrument trigger lag, decision reasons, suppression, quotas/cooldowns, publication/delivery attempts, dead letters, replays, and trace completeness while keeping audit authoritative.
- Stage 15 must place control, scheduler, publisher, and delivery roles without treating logical records as services or selecting a broker without evidence.
- Stage 16 must test authorization/freshness/threshold/policy/quota/cooldown/dedupe/audit bypass, revocation races, event compatibility, delivery ambiguity, and replay.
- Stage 17 must supply measured rates, backlogs, fan-out, retention, delivery SLO, concurrency, and cost evidence for activation/broker decisions.
- Stage 20 must name grant/control/integration/schema/delivery/on-call owners and sequence only approved use cases.
- Stage 22 must trace scheduled and conditional event-driven proactive flows through concrete runtime/process/concurrency placement.

## Exact next-stage inputs

Approved inputs for Stage 10:

1. Approved `outputs/stages/03-capability-inventory.md` and its seven capability contracts
2. Approved `outputs/stages/05-end-to-end-architecture.md` through `outputs/stages/09-events-proactive-actions.md`
3. Accepted `decisions/ADR-002-stage-03-capability-evidence-disposition.md` through `decisions/ADR-006-governed-proactive-action-and-delivery.md`
4. Active `A-03-ML-MIGRATION`, `A-03-SYNAPSE`, `A-04-OWNERSHIP`, and all applicable `A-01-*`/`A-07-INTEGRATION` constraints
5. `sources/normalized/ark-assumptions.md`
6. All seven service cards under ADR-000/ADR-002 evidence restrictions
7. `stages/10-mlops.md`, `templates/stage-output.md`, and exact governing prompt section **9. ML and MLOps architecture**

Stage 09 and ADR-006 are approved; Stage 10 may consume them.
