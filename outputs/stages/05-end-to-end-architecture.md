# Stage 05 — End-to-end architecture

Status: `APPROVED`

## Purpose and scope

Define the complete logical path from a consuming application or data source to an ARK result, including control, integration, ingestion/data, capability, execution, delivery, and operational boundaries. Evaluate every component named by the governing prompt, include only requirement-backed logical components, reject or defer unnecessary infrastructure, and specify every included component against the required component contract.

This stage defines logical components and interactions inside the approved modular-monolith style. It does not select physical topology, cloud/vendor products, concrete API schemas, detailed data schemas, workflow/event technology, capacity, SLOs, retention, or deployment placement; those remain with their named later stages.

The Stage 05 component-completeness gate passes. Per the user's instruction, the workflow is paused for explicit approval before Stage 06.

## Inputs read in full

- `AGENTS.md` — all sections
- `WORKFLOW.md` — all sections
- `STATUS.md` — all sections after recording Stage 04 approval
- `SOURCE_MANIFEST.md` — all sections
- `stages/STAGE-CONTRACT.md` — all sections
- `stages/05-end-to-end-architecture.md` — all sections
- `templates/stage-output.md` — all sections
- `templates/component-spec.md` — all sections
- `templates/execution-flow.md` — all sections
- `templates/requirements-traceability.md` — all sections
- `sources/normalized/system-design-prompt.md` — **4. End-to-end architecture** exactly
- `sources/normalized/ark-assumptions.md` — all sections
- `outputs/stages/02-system-definition.md` — all sections
- `outputs/stages/03-capability-inventory.md` — all sections
- `outputs/stages/04-architecture-style.md` — all sections after approval
- `decisions/ADR-000-temporary-source-evidence-disposition.md` through `decisions/ADR-003-architecture-style.md` — all sections

The authorized `platform_architect` performed a bounded read-only review of control, API, lifecycle, delivery, operational, and conditional infrastructure components. A separate authorized `data_mlops_architect` review was requested but could not be created because the collaboration runtime had reached its agent-thread limit, including two stale pending threads that could not be removed. The primary agent therefore performed the data/ML component analysis directly from the approved Stage 03 contracts and records this process limitation rather than claiming specialist coverage that did not occur.

## Source-instruction coverage

| Governing item | Disposition | Component/evidence |
|---|---|---|
| Consumer applications | Required external actor, not ARK-owned | `C05-01` |
| Consumer-specific adapters / anti-corruption layers | Required at integration boundary; exact consumer-vs-ARK placement deferred | `C05-01`; `A-01-INT` |
| Load balancer | Scale/deployment-triggered; no distinct first-version component | `X05-01`; unknown replicas/topology |
| API gateway | Required logical edge role; no separate gateway product selected | `C05-02` |
| Authentication and authorization | Required | `C05-03` |
| Tenant identification | Required; derived from authenticated principal | `C05-03`; `ARK-NFR-001` |
| Plans, entitlements, quotas, rate limits | Required control responsibility | `C05-04` |
| Versioned capability APIs | Required | `C05-05` |
| Workflow/orchestration API | Useful soon for named multi-job workflows; ordinary durable operations use the required job API | `C05-22` |
| Data ingestion | Required | `C05-06` |
| Schema and semantic validation | Required inside ingestion/readiness boundary | `C05-06` |
| Dataset catalog | Required logical registry | `C05-07` |
| Data eligibility/capability readiness | Required and deliberately separated | `C05-07`, `C05-11` |
| Job manager | Required, one shared lifecycle | `C05-08` |
| Task queue and workers | Required semantics; PostgreSQL claims plus worker roles, no broker queue | `C05-08`, `C05-10` |
| Scheduler | Required for scheduled work; creates jobs only | `C05-09` |
| Workflow orchestration | Useful soon for named multi-job workflows; no workflow-engine product | `C05-22` |
| Event producer/consumer handling | Useful soon as a reliable-publication adapter when Stage 09/13 justifies it | `C05-21` |
| Event broker | Scale/reliability-triggered, not justified now | `X05-02` |
| Notification delivery | Required as result-delivery boundary | `C05-12` |
| Webhooks, polling, SSE, other delivery | Polling required; signed webhook useful soon; SSE optional/unjustified now | `C05-12`, `X05-03` |
| Configuration and policy management | Required | `C05-04`, `C05-17` |
| Service registry | Unjustified for modular monolith/static roles | `X05-04` |
| Caching | Scale-triggered; no first-version cache tier | `X05-05` |
| Operational databases | Required; initially shared PostgreSQL cluster with owned schemas/writers | `C05-13` |
| Object storage/data lake | Required | `C05-14` |
| Feature/state storage | Required logical capability-owned namespaces; no separate feature-store product | `C05-15` |
| Model registry | Required logical registry; no separate registry product selected | `C05-16` |
| Secrets management | Required interface/control; product deferred | `C05-17` |
| Audit logging | Required authoritative ledger | `C05-18` |
| Observability | Required operational telemetry | `C05-19` |
| Administration/operational interfaces | Required narrow APIs/CLI; no business-user UI | `C05-20` |

Every included `C05-*` component has a full specification below. Every excluded/conditional `X05-*` item has an explicit trigger and removal rationale.

## Facts

- ARK is a multi-tenant capability platform behind consumer applications; consumer-specific terminology does not enter capability cores. `sources/normalized/ark-assumptions.md — Product and architecture`; `— Integration and contracts`.
- Control-plane authority, execution/data work, capability science, external integration, and operational evidence are distinct logical boundaries within the approved modular monolith. `ADR-003 — Decision`; `Stage 04 — Logical module and ownership boundaries`.
- The shared durable job manager owns asynchronous lifecycle; PostgreSQL is initially its durable truth. Capability workers own computation. `ark-assumptions.md — Execution, orchestration, and proactive operation`.
- The data lake preserves raw input, immutable curated datasets, service-owned derived data/results/artifacts, and lineage; PostgreSQL holds operational metadata/state rather than large histories. `ark-assumptions.md — Ingestion and the ARK data lake`.
- Dataset readiness, platform eligibility, and capability scientific eligibility are separate decisions and must return explicit outcomes. `ark-assumptions.md — Integration and contracts`; `ARK-FR-006`.
- Churn, RFM, NPT, and REC remain non-production migration evidence; Synapse remains interface-only and non-production-eligible. `ADR-002 — Decision`; `Stage 03 — Capability inventory`.
- Numeric workload, availability, recovery, retention, cost, and deployment constraints remain unknown. No component below is a production-sizing claim. `Stage 02 — A-01-SCALE, A-01-OPS`; `ARK-NFR-007`.

## Assumptions

No new temporary assumption is introduced.

| Active assumption | Stage 05 effect | Expiry preserved |
|---|---|---|
| `A-01-BUS` | Consumer apps/systems of record and channel delivery remain outside ARK | Stage 01 conditions |
| `A-01-DATA` | Upstreams provide authoritative opaque IDs; no probabilistic identity merge | Stage 01 conditions |
| `A-01-INT` | Adapter placement remains provisional; capability cores remain neutral | Stage 07/recorded conditions |
| `A-01-SCALE` | No load-balancer, cache, broker, replica, capacity, or SLO commitment without measurements | Measured S-01–S-04 evidence |
| `A-01-SEC` | Principal-derived tenant, least privilege, fail-closed proactive action | Security/policy evidence |
| `A-01-OPS` | Deployment/support/recovery and concrete observability targets remain open | OPS-01–OPS-05 |
| `A-03-ML-MIGRATION` | Target component boundaries do not preserve prototype cross-writes/implicit training | Per-capability Stage 10/16 decisions |
| `A-03-SYNAPSE` | Only documented Synapse interfaces enter the path; no hidden internals | Recorded evidence/production gates |
| `A-04-OWNERSHIP` | Logical owner roles are used; production/extraction remains blocked without named authorities | Stage 20/extraction/production or assignments |

## End-to-end logical architecture

### Boundary map

| Boundary | Components | Owns | Must not own |
|---|---|---|---|
| External consumer/source | `C05-01` consumer app and adapter | Consumer UX, source/master data, consumer schema translation, credentials/notification endpoint | ARK tenant/job/dataset/capability state |
| Integration/edge | `C05-02`, `C05-03`, `C05-05`, `C05-12` | Protocol/API boundary, request identity, tenant binding, public operations, result delivery | Scientific eligibility, normalization, capability business logic |
| Control plane | `C05-04`, `C05-17`, `C05-20` | Subscription/entitlement/quota/grants/configuration, technical secret/config delivery, administrative commands | Dataset transformation or capability computation |
| Data plane | `C05-06`–`C05-10`, `C05-13`–`C05-15` | Raw-to-ready datasets, durable jobs, schedules, worker claims, operational/data/artifact locations | Capability-specific scientific rules or consumer presentation |
| Capability plane | `C05-11`, `C05-16` | Seven public capability ports, scientific eligibility, private pipelines, model/artifact selection, results/evaluations | Another capability's state, platform lifecycle, external-action authority |
| Operational/evidence plane | `C05-18`–`C05-21` | Audit, telemetry, administrative visibility, conditional reliable publication | Business/scientific authority or tenant identity |

### Consumer-to-result flow: synchronous eligible operation

| Step | Component | Action/output | Failure boundary |
|---:|---|---|---|
| 1 | `C05-01` | Adapter translates consumer request into common envelope plus capability payload | Invalid translation fails outside capability core |
| 2 | `C05-02`/`C05-03` | Bound request, authenticate caller, derive tenant/request context, enforce edge limits | Reject without side effect; body tenant cannot override principal |
| 3 | `C05-04` | Check subscription, entitlement, quota, configuration, and grant where relevant | Explicit unauthorized/ineligible; no capability execution |
| 4 | `C05-05` | Validate API/definition versions and confirm operation is approved for synchronous mode | Long/unqualified work is rejected or submitted as a job |
| 5 | `C05-07`/`C05-11` | Resolve immutable dataset/context and active versions; distinguish dataset, platform, and scientific eligibility | Explicit not-ready/degraded/fallback/ineligible; no invented data |
| 6 | `C05-11`/`C05-16` | Execute through the capability public port with fixed artifact/config versions | Capability error is bounded; no implicit training/activation |
| 7 | `C05-13`–`C05-19` | Persist owned result/lineage/usage/audit; emit non-authoritative telemetry | Authoritative result/audit failure is explicit; telemetry degradation is separately visible |
| 8 | `C05-05`/`C05-12`/`C05-01` | Return bounded result/status to adapter and consumer | Delivery failure does not change the authoritative capability result |

### Consumer-to-result flow: durable asynchronous operation

| Step | Component | Action/output | Failure boundary |
|---:|---|---|---|
| 1 | `C05-01`–`C05-05` | Authenticate, authorize, validate envelope/operation/dataset references | Rejected before job creation |
| 2 | `C05-08`/`C05-13` | Atomically create/replay one tenant-scoped job by idempotency key; return job reference | Duplicate returns same logical job; DB failure means not accepted |
| 3 | `C05-09`/`C05-10` | Scheduler/coordinator releases eligible work; worker claims lease from PostgreSQL queue semantics | Lease expiry permits retry; process death does not lose job |
| 4 | `C05-07`/`C05-04` | Revalidate dataset readiness and execution-time entitlement/grant/config freshness | Job terminates or waits with explicit reason; no unauthorized work |
| 5 | `C05-11`/`C05-16` | Capability evaluates scientific eligibility and executes private pipeline | Retry/partial semantics are capability/job policy; no cross-write |
| 6 | `C05-14`/`C05-15`/`C05-13` | Store large results/artifacts by reference and bounded metadata/status in owned operational state | Result is not terminal-success until authoritative commit completes |
| 7 | `C05-08`/`C05-18`/`C05-19` | Commit terminal state, lineage, audit, usage/cost evidence | Audit/commit failures remain explicit/recoverable |
| 8 | `C05-12` | Consumer polls; signed webhook may be added when approved; delivery retried independently | Notification failure does not rerun capability or erase result |

### Source-to-ready-dataset flow

| Step | Component | Action/output | Failure boundary |
|---:|---|---|---|
| 1 | `C05-01`–`C05-04` | Source registers push/micro-batch or bulk object reference under authenticated tenant/entitlement | Invalid/unauthorized registration rejected |
| 2 | `C05-06`/`C05-14` | Persist immutable raw input before transformation; create ingestion job | Raw evidence retained; duplicate handled by idempotency/source identity |
| 3 | `C05-08`–`C05-10` | Worker validates technical schema then canonical semantics and policy | Failure publishes quality/error evidence, never ready dataset |
| 4 | `C05-06`/`C05-14` | Write validated/canonical immutable data and quality report | Partial objects remain unreferenced/unready |
| 5 | `C05-07`/`C05-13` | Atomically publish catalog metadata/readiness/lineage for one dataset version | Catalog failure means dataset is not ready even if objects exist |
| 6 | `C05-18`/`C05-19`/`C05-12` | Record audit/metrics and expose job/result status | Notification failure is independent of publication truth |

### Dependency and concurrency rules

- Control checks and contract validation may run concurrently only when neither can create side effects; all must join before job acceptance or synchronous execution.
- Independent capability jobs may run concurrently when tenant quota, resource pools, datasets, and owned state permit; they never call each other's private pipelines.
- Dataset publication is a single readiness commit after raw persistence, validation, normalization, quality, policy, and lineage succeed.
- Job/result/notification transitions use idempotency and compare-and-set/lease semantics; detailed state machines are deferred to Stage 08/13.
- Audit and authoritative usage records follow the business commit boundary; telemetry export is supporting-path and must expose loss/degradation without becoming business authority.
- Proactive action adds a mandatory deterministic grant/policy/freshness/quota/deduplication join; advisory verifier output alone never passes it.

## Component inventory

| ID | Component | Classification | First-version disposition | Logical owner |
|---|---|---|---|---|
| `C05-01` | Consumer application and anti-corruption adapter boundary | required now | External actor plus translation boundary; placement details deferred | Consumer/integration role |
| `C05-02` | Logical edge/API gateway | required now | Thin ingress inside/adjacent to modular monolith; no gateway product selected | Platform integration role |
| `C05-03` | Authentication, authorization, and tenant context | required now | Boundary enforcement plus principal-derived tenant context | Security/control role |
| `C05-04` | Tenant control, entitlement, quota, grant, configuration, and policy | required now | Module-owned control records/decisions | Platform control/security roles |
| `C05-05` | Versioned capability and job API | required now | Public façade over module ports and durable job lifecycle | Platform contract/integration role |
| `C05-06` | Ingestion, schema/semantic validation, and publication pipeline | required now | Durable pipeline; push/bulk reference; raw first | Data-platform role |
| `C05-07` | Dataset catalog and readiness | required now | PostgreSQL metadata plus object references; scientific eligibility remains capability-owned | Data-platform role |
| `C05-08` | Durable job manager and database task dispatch | required now | PostgreSQL state/claims; no external queue product | Platform execution role |
| `C05-09` | Scheduler | required now | Creates jobs only; never executes private pipelines | Platform execution role |
| `C05-10` | Worker runtime roles | required now | Same-codebase worker loops/pools by workload class | Platform + capability/data roles |
| `C05-11` | Seven capability modules | required now | Logical modules; release scope/readiness varies; Synapse not production-eligible | Per-capability role |
| `C05-12` | Result and notification delivery | required now | Polling required; signed webhook useful soon | Integration role |
| `C05-13` | Operational PostgreSQL | required now | Shared cluster, owned schemas/writers/RLS defense-in-depth | Platform/data roles by schema |
| `C05-14` | Object storage / ARK data lake | required now | Raw, curated, derived, result, artifact namespaces by tenant/version | Data-platform and capability roles |
| `C05-15` | Capability-owned feature/result/state storage | required now | Logical namespaces on PostgreSQL/object storage; no feature-store product | Per-capability role |
| `C05-16` | Model/artifact registry | required now | PostgreSQL metadata + object artifact references; no standalone product | Platform registry + capability roles |
| `C05-17` | Secrets and technical configuration delivery | required now | Narrow interface; concrete secret/config product deferred | Security/platform role |
| `C05-18` | Audit, lineage, usage, and metering ledger | required now | Tenant-scoped authoritative evidence in owned operational schemas/object references | Security/operations/platform role |
| `C05-19` | Observability | required now | Structured logs, metrics, traces and correlation interfaces; targets TBD | Operations + module roles |
| `C05-20` | Administration and operational interfaces | required now | Narrow authenticated APIs/CLI for control/jobs/datasets/artifacts/audit; no business UI | Platform/operations role |
| `C05-21` | Internal reliable-publication adapter | useful soon | Contract seam only until Stage 09/13 proves outbox/event need | Platform execution/integration role |
| `C05-22` | Named-workflow API and coordinator | useful soon | Explicit parent/child job state for an approved workflow; no generic DSL/engine | Platform orchestration role |

### Conditional and rejected expected components

| ID | Expected component | Classification | Why not included now | Trigger/reconsideration |
|---|---|---|---|---|
| `X05-01` | Distinct load balancer | scale-triggered | Replica/topology/environment needs are unknown; a single logical ingress suffices for architecture | Multiple ingress replicas or mandated environment needs distribution/health routing |
| `X05-02` | Event broker/streaming platform | scale-triggered | PostgreSQL job truth/direct module calls meet current evidence; broker operations are unjustified | Approved fan-out/throughput/latency/replay need cannot be met after simpler remedies |
| `X05-03` | Server-sent events | optional | No consumer requirement; polling covers durable results, webhook is the likely useful-soon push contract | Approved interactive progress requirement with measured connection feasibility |
| `X05-04` | Service registry/discovery | unjustified | One repository/coordinated roles and static configuration have no dynamic service estate | Extracted services create dynamic discovery need not met by deployment configuration |
| `X05-05` | Shared cache tier | scale-triggered | No measured hot path; caching risks tenant/version staleness and invalidation complexity | Measured bottleneck remains after query/index/code correction; tenant/version key and invalidation contract approved |
| `X05-06` | Separate API-gateway product | optional | Logical edge duties are required; vendor/product is not | Deployment/security constraint demonstrates need in Stage 15/17 |
| `X05-07` | Standalone feature-store product | unjustified now | Capability-owned versioned features plus lake/operational state satisfy current contracts | Proven online/offline consistency/reuse need cannot be met by existing ownership model |
| `X05-08` | Standalone model-registry product | optional | Logical registry metadata/object references are sufficient; no procurement/scale need | Stage 10 lifecycle evidence shows missing controls that a product uniquely satisfies |
| `X05-09` | General workflow engine | scale-triggered | Simple coordinator over durable jobs covers evidenced workflows | Workflow depth/duration/signals/compensation/operations exceed explicit Stage 08 criteria |

## Included component specifications

All version names and wire schemas below are responsibilities, not invented concrete formats; Stages 06–10 define them. All owners are logical roles under accepted `A-04-OWNERSHIP`.

### Component specification — C05-01 Consumer application and anti-corruption adapter boundary

- **Classification:** `required now` (external boundary).
- **Requirement(s):** `ARK-FR-002`, `ARK-FR-005`, `ARK-FR-011`; `ARK-NFR-003`; `ARK-CON-003`.
- **Responsibility and non-responsibilities:** Consumer owns source/business UX and maps its schemas/protocols to bounded ARK contracts; it does not derive ARK tenant authority, access ARK state, or contain scientific eligibility.
- **Stages/workflows where used:** Every ingestion, invocation, result, and notification path; detailed ownership/contract in Stage 07.
- **Trigger and prerequisites:** Registered consumer integration with authenticated credential and approved version mapping.
- **Inputs/outputs and contract versions:** Consumer-version payloads ↔ versioned ARK envelope/domain contracts; mapping failures explicit.
- **State and authoritative storage owner:** Consumer owns source/session/presentation state; adapter is preferably stateless, with any delivery/mapping state integration-owned and tenant/version scoped.
- **Upstream/downstream dependencies:** Consumer source/UI upstream; `C05-02` downstream.
- **Critical-path or supporting-path role:** Critical when translation is required; notifications are supporting after result commit.
- **Failure effect and user-visible status:** Unsupported/malformed mapping fails before ARK side effects; delivery failure does not invalidate committed result.
- **Timeout/retry/idempotency/cancellation:** Pass request/correlation/idempotency; consumer retries only safe/idempotent operations; job cancellation uses ARK API.
- **Security and tenant-isolation controls:** Credential-bound tenant; request fields cannot override; minimize PII.
- **Observability and audit:** Consumer/adapter version, correlation, mapping result/reason, delivery outcome; no raw sensitive payload by default.
- **Scaling/resource isolation:** Consumer-owned; isolate adapters only on measured traffic/runtime need.
- **Simplest viable implementation:** Consumer library or thin per-consumer mapping module at integration edge.
- **Alternative considered and rejection reason:** Universal customer DTO/ESB; creates shared business coupling.
- **Operational burden and owner:** Integration role plus consumer owner; compatibility tests/runbook required.
- **Reconsideration/extraction trigger:** Stage 07 placement decision or consumer natively adopts ARK contracts.
- **Effect if removed, moved, delayed, or replaced:** Removal is valid only for a native ARK-contract consumer; moving into capability core violates neutrality.

### Component specification — C05-02 Logical edge/API gateway

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-005`; `ARK-NFR-001`, `ARK-NFR-003`, `ARK-NFR-006`; approved edge baseline.
- **Responsibility and non-responsibilities:** Protocol termination, coarse authentication integration, routing, API version, request size/technical rate limits, request/correlation identity; no normalization, quota authority, readiness, workflow, or science.
- **Stages/workflows where used:** Every external API; refined Stage 07/12/15.
- **Trigger and prerequisites:** External request on a supported public version.
- **Inputs/outputs and contract versions:** HTTP request → bounded authenticated request context or standard edge error.
- **State and authoritative storage owner:** Minimal route/version/limit configuration; no business state.
- **Upstream/downstream dependencies:** `C05-01` and optional `X05-01` upstream; `C05-03`/`C05-05` downstream.
- **Critical-path or supporting-path role:** Critical external path.
- **Failure effect and user-visible status:** Reject before side effects with auth/version/size/rate/availability error.
- **Timeout/retry/idempotency/cancellation:** Short edge timeouts; no invisible retry of non-idempotent requests; pass identifiers.
- **Security and tenant-isolation controls:** Validate credentials/transport, but tenant is resolved by `C05-03`; no body tenant authority.
- **Observability and audit:** Request/rejection counts, route/version, latency, correlation; auth decisions go to audit owner.
- **Scaling/resource isolation:** Embed in API role first; `X05-01`/separate product only on replica/environment evidence.
- **Simplest viable implementation:** Thin middleware/router in the modular-monolith API role.
- **Alternative considered and rejection reason:** Enterprise gateway/ESB product; no environment/scale requirement.
- **Operational burden and owner:** Platform integration role; route/version/security runbook.
- **Reconsideration/extraction trigger:** Measured edge scale/security need or mandated deployment ingress.
- **Effect if removed, moved, delayed, or replaced:** Removing logical edge controls breaks public contract/security; replacing implementation does not change boundary.

### Component specification — C05-03 Authentication, authorization, and tenant context

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-001`, `ARK-FR-005`, `ARK-FR-006`, `ARK-FR-010`; `ARK-NFR-001`, `ARK-NFR-005`, `ARK-NFR-006`.
- **Responsibility and non-responsibilities:** Authenticate caller, derive immutable tenant/caller context, enforce operation/scope authorization; domain authorization/scientific eligibility remain owner-module duties.
- **Stages/workflows where used:** Every API, admin command, job, dataset/object access, and proactive action; Stage 12 details protocol/roles.
- **Trigger and prerequisites:** Credential or durable job principal/tenant reference.
- **Inputs/outputs and contract versions:** Credential/claims → authenticated subject, tenant, scopes/roles, correlation/audit context.
- **State and authoritative storage owner:** External identity provider owns identities/credentials; ARK control owns tenant bindings/grants.
- **Upstream/downstream dependencies:** `C05-02` upstream; every authoritative module downstream.
- **Critical-path or supporting-path role:** Critical, fail-closed.
- **Failure effect and user-visible status:** Unauthenticated/unauthorized/ambiguous context produces no ingestion, execution, result access, or outward action.
- **Timeout/retry/idempotency/cancellation:** No retry bypass; workers re-evaluate time-sensitive authority where policy requires.
- **Security and tenant-isolation controls:** Tenant never comes from phone/body/business ID; least privilege across all state classes.
- **Observability and audit:** Privacy-safe subject reference, decision/reason, tenant, operation, correlation; denied and privileged actions audited.
- **Scaling/resource isolation:** Optimize/cache only non-authoritative immutable mappings with safe invalidation after measurement.
- **Simplest viable implementation:** Common principal/tenant middleware plus module authorization ports.
- **Alternative considered and rejection reason:** Gateway-only authorization or per-capability identity parsing; creates bypass/inconsistency.
- **Operational burden and owner:** Security/control role with platform enforcement; named owner pending A-04.
- **Reconsideration/extraction trigger:** Protocol/provider changes in Stage 12/15; responsibility cannot be removed.
- **Effect if removed, moved, delayed, or replaced:** Removal invalidates multitenancy/security; provider replacement is boundary-neutral.

### Component specification — C05-04 Tenant control, entitlement, quota, grant, configuration, and policy

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-001`, `ARK-FR-006`, `ARK-FR-010`; `ARK-NFR-001`, `ARK-NFR-002`, `ARK-NFR-006`.
- **Responsibility and non-responsibilities:** Authoritative tenant subscription/entitlement/quota/grant/platform configuration and proactive policy; no scientific eligibility or capability-private configuration semantics.
- **Stages/workflows where used:** Admission, execution-time recheck, proactive authorization, admin; Stages 07/09/12 refine.
- **Trigger and prerequisites:** Authenticated tenant/caller plus operation/dataset/config context.
- **Inputs/outputs and contract versions:** Versioned control query/command → allow/deny, reason, reservation/grant/config/policy version references.
- **State and authoritative storage owner:** Control-plane-owned PostgreSQL schema; one writer.
- **Upstream/downstream dependencies:** `C05-03`, admin upstream; `C05-05`/`C05-08`/`C05-11` downstream.
- **Critical-path or supporting-path role:** Critical for admission/proactive action.
- **Failure effect and user-visible status:** Fail closed with not-entitled/quota/policy/control-unavailable; no action.
- **Timeout/retry/idempotency/cancellation:** Idempotent mutations; quota reservation/job acceptance coordinated; cancellation/completion reconciles usage by later policy.
- **Security and tenant-isolation controls:** Privileged writes, principal tenant, least privilege, verifier output never authority.
- **Observability and audit:** Decisions/reasons, version, reservations/consumption, changes, actor, correlation.
- **Scaling/resource isolation:** PostgreSQL indexes/transactions first; cache cannot be authority.
- **Simplest viable implementation:** Versioned module-owned relational records and transactionally consistent decision interface.
- **Alternative considered and rejection reason:** Gateway/cache/LLM as authority; stale or advisory state is unsafe.
- **Operational burden and owner:** Platform control/security roles; commercial semantics unresolved.
- **Reconsideration/extraction trigger:** Measured contention, compliance boundary, or dedicated accountable owner through ADR-003 gate.
- **Effect if removed, moved, delayed, or replaced:** Removal violates tenancy/governance; private capability configuration remains outside this module.

### Component specification — C05-05 Versioned capability and job API

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-004`–`ARK-FR-008`; `ARK-NFR-002`, `ARK-NFR-003`, `ARK-NFR-006`.
- **Responsibility and non-responsibilities:** Publish definitions, validate common envelope, expose bounded capability operations and job submit/status/cancel/result; no scientific logic or private workflow pipeline.
- **Stages/workflows where used:** Discovery and every invocation/result flow; exact schemas in Stage 07/08.
- **Trigger and prerequisites:** Authenticated/authorized request for supported capability/operation/version.
- **Inputs/outputs and contract versions:** Definition query; envelope + capability payload → sync outcome or job reference; job ID → status/result.
- **State and authoritative storage owner:** Definition index owned by platform contract module; content by capability; jobs by `C05-08`.
- **Upstream/downstream dependencies:** `C05-02`–`C05-04` upstream; `C05-07`, `C05-08`, `C05-11`, `C05-12` downstream.
- **Critical-path or supporting-path role:** Critical.
- **Failure effect and user-visible status:** Unsupported version/operation, invalid envelope, not-ready/ineligible, not-accepted, and execution failure remain distinct.
- **Timeout/retry/idempotency/cancellation:** Sync only classified short work; job submission idempotent; cancellation delegated to job manager.
- **Security and tenant-isolation controls:** Entitlement-filtered definitions where required; tenant-bound invocation/result lookup.
- **Observability and audit:** Per operation/version status/latency, job/correlation, no unnecessary PII.
- **Scaling/resource isolation:** API role scales only on measurements; large inputs/results by reference.
- **Simplest viable implementation:** Modular controllers/schema validation and static/code-generated definition documents.
- **Alternative considered and rejection reason:** Generic unbounded execute endpoint or dynamic network registry; erodes contracts.
- **Operational burden and owner:** Platform contract/integration plus each capability owner.
- **Reconsideration/extraction trigger:** Public contract stable plus ADR-003 measured boundary trigger.
- **Effect if removed, moved, delayed, or replaced:** Without it consumers cannot discover/invoke/retrieve consistently; implementation may move without contract change.

### Component specification — C05-06 Ingestion, validation, and dataset-publication pipeline

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-002`, `ARK-FR-003`, `ARK-FR-007`; `ARK-NFR-001`–`ARK-NFR-005`; `ARK-CON-004`, `ARK-CON-006`.
- **Responsibility and non-responsibilities:** Register push/bulk inputs, persist raw, validate technical schema then domain semantics/policy/quality/freshness, normalize, and publish candidate immutable data; no capability scientific eligibility or master-data ownership.
- **Stages/workflows where used:** Source-to-ready-dataset; detailed Stage 06.
- **Trigger and prerequisites:** Authenticated entitled tenant and versioned source contract; bulk object reference registered where applicable.
- **Inputs/outputs and contract versions:** Incremental/micro-batch payload or object reference → ingestion run, raw object, validation/quality report, canonical version candidate or explicit failure.
- **State and authoritative storage owner:** Data-platform owns ingestion runs/cursors/quality metadata; raw/canonical objects in `C05-14`; catalog publication by `C05-07`.
- **Upstream/downstream dependencies:** `C05-01`–`C05-04`, `C05-08`–`C05-10`, `C05-13`, `C05-14`; `C05-07` downstream.
- **Critical-path or supporting-path role:** Critical for dataset-dependent capabilities; async data path.
- **Failure effect and user-visible status:** Retain raw and publish no ready version; explicit structural/semantic/policy/quality failure.
- **Timeout/retry/idempotency/cancellation:** Durable job; source/ingestion idempotency; at-least-once safe; cancel before publication where possible; reprocessing creates new run/version.
- **Security and tenant-isolation controls:** Tenant-qualified source/run/object paths, opaque IDs, least privilege, quarantine untrusted input.
- **Observability and audit:** Counts/bytes, validation reason, quality/freshness, stage timing, retries, lineage, actor/source/run.
- **Scaling/resource isolation:** Partition workers by dataset/workload after measurement; object references for large data; push default, streaming conditional.
- **Simplest viable implementation:** Same-codebase durable ingestion workers, schema validators, modular normalizers, PostgreSQL metadata, object storage.
- **Alternative considered and rejection reason:** Direct shared DB, one universal customer object, streaming-first; violate baseline or lack evidence.
- **Operational burden and owner:** Data-platform role; contracts/quality/runbook required.
- **Reconsideration/extraction trigger:** Measured ingestion contention, incompatible runtime, or residency boundary through ADR-003.
- **Effect if removed, moved, delayed, or replaced:** Dataset-dependent capabilities cannot receive governed inputs; replacement must preserve raw-first/lineage/readiness.

### Component specification — C05-07 Dataset catalog and readiness

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-003`, `ARK-FR-006`; `ARK-NFR-001`–`ARK-NFR-003`, `ARK-NFR-006`; `SC-02-02`, `SC-02-04`, `SC-02-07`.
- **Responsibility and non-responsibilities:** Register immutable dataset/source/schema/version/run/object/quality/freshness/policy lineage and publish data-readiness status; not platform entitlement or capability scientific eligibility.
- **Stages/workflows where used:** Ingestion publication and every dataset-dependent invocation; Stage 06 details.
- **Trigger and prerequisites:** Completed validated ingestion outputs and quality/lineage evidence.
- **Inputs/outputs and contract versions:** Publication command → immutable dataset version/reference/readiness or rejection; query → version metadata/readiness reasons.
- **State and authoritative storage owner:** Data-platform-owned PostgreSQL catalog; objects remain in data lake.
- **Upstream/downstream dependencies:** `C05-06`, `C05-13`, `C05-14` upstream; `C05-05`, `C05-08`, `C05-11`, `C05-18` downstream.
- **Critical-path or supporting-path role:** Critical for publication/admission.
- **Failure effect and user-visible status:** Objects without successful catalog commit are not ready; capability gets not-ready, never fabricated input.
- **Timeout/retry/idempotency/cancellation:** Idempotent publication for same immutable identity; readiness transitions compare versions; published versions immutable.
- **Security and tenant-isolation controls:** Tenant-qualified keys/object references, authorized readers, no cross-tenant discovery.
- **Observability and audit:** Publication/readiness counts/reasons, stale versions, lineage gaps, query latency.
- **Scaling/resource isolation:** Relational metadata/indexes first; partition/archive only on measurement.
- **Simplest viable implementation:** Owned PostgreSQL tables referencing object-store paths and quality/lineage records.
- **Alternative considered and rejection reason:** Separate catalog product now or capability-private catalogs; adds product burden or inconsistent readiness.
- **Operational burden and owner:** Data-platform owner; schema/version/lineage governance.
- **Reconsideration/extraction trigger:** Metadata scale/federation/compliance evidence beyond relational implementation.
- **Effect if removed, moved, delayed, or replaced:** Reproducible readiness and safe invocation fail; registry implementation may change behind contract.

### Component specification — C05-08 Durable job manager and database task dispatch

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-007`, `ARK-FR-008`; `ARK-NFR-001`, `ARK-NFR-004`, `ARK-NFR-006`; `ARK-CON-005`.
- **Responsibility and non-responsibilities:** Authoritative job/attempt/idempotency/state/retry/progress/cancellation/result-reference lifecycle and claim semantics; never runs capability science.
- **Stages/workflows where used:** All ingestion, training, backfill, schedule, batch, long/retryable work; Stage 08/13 detail.
- **Trigger and prerequisites:** Authorized valid durable-operation submission or schedule/workflow occurrence.
- **Inputs/outputs and contract versions:** Submit/status/cancel/result and worker claim/transition commands → job/reference/state/error.
- **State and authoritative storage owner:** Job module in `C05-13`; one writer interface.
- **Upstream/downstream dependencies:** `C05-05`, `C05-09`, `C05-22` upstream; `C05-10`–`C05-12`, `C05-18` downstream.
- **Critical-path or supporting-path role:** Central asynchronous critical path.
- **Failure effect and user-visible status:** DB failure means not accepted/paused; committed jobs survive process failure; status remains truthful.
- **Timeout/retry/idempotency/cancellation:** Unique tenant/operation/idempotency, leases/CAS, policy-driven retry/timeout, cooperative cancellation.
- **Security and tenant-isolation controls:** Tenant-bound lookup/claim; scoped worker identity; body tenant cannot change job.
- **Observability and audit:** Queue age, transition/attempt/retry, stuck leases, completion, cancel, correlation.
- **Scaling/resource isolation:** Index/batch/worker pools first; broker only after ADR-003 coordination trigger.
- **Simplest viable implementation:** PostgreSQL job/attempt tables, transactional state machine, `SKIP LOCKED`-style claiming or equivalent.
- **Alternative considered and rejection reason:** Per-capability lifecycle, broker, workflow product; duplicate truth/unsupported burden.
- **Operational burden and owner:** Platform execution role; critical runbook.
- **Reconsideration/extraction trigger:** Proven PostgreSQL/workflow limit after simpler remedies.
- **Effect if removed, moved, delayed, or replaced:** Durable work violates requirements; replacement must migrate authoritative state safely.

### Component specification — C05-09 Scheduler

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-007`, `ARK-FR-010`; approved scheduler/job baseline.
- **Responsibility and non-responsibilities:** Evaluate schedules/grant windows and submit deterministic occurrence jobs; never execute capability pipelines.
- **Stages/workflows where used:** Scheduled/proactive execution; Stage 08/09.
- **Trigger and prerequisites:** Active tenant-scoped schedule, entitlement/grant/config, clock occurrence.
- **Inputs/outputs and contract versions:** Schedule/version/time → job submission with occurrence idempotency key or explicit rejection.
- **State and authoritative storage owner:** Scheduler/control owns schedules/occurrences in PostgreSQL; job manager owns jobs.
- **Upstream/downstream dependencies:** `C05-04`, `C05-13` upstream; `C05-08` downstream.
- **Critical-path or supporting-path role:** Supporting producer to async path.
- **Failure effect and user-visible status:** Miss/delay visible and recoverable; expired/revoked grant creates no work.
- **Timeout/retry/idempotency/cancellation:** Durable next-run/lease; deterministic occurrence; disable cancels future submissions, not existing jobs.
- **Security and tenant-isolation controls:** Tenant-scoped schedules, authorized mutations, execution-time recheck.
- **Observability and audit:** Scheduling lag, missed/duplicate occurrence, submission/rejection, actor/config/grant versions.
- **Scaling/resource isolation:** Single logical scheduler initially; role/partition only on measured contention.
- **Simplest viable implementation:** PostgreSQL schedule table and same-codebase scheduler loop.
- **Alternative considered and rejection reason:** Process-local capability timers/external scheduler product; nondurable or unsupported.
- **Operational burden and owner:** Platform execution/control roles.
- **Reconsideration/extraction trigger:** Measured schedule volume/reliability or environment mandate.
- **Effect if removed, moved, delayed, or replaced:** Scheduled/proactive use cases disappear; on-demand jobs unaffected.

### Component specification — C05-10 Worker runtime roles

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-007`–`ARK-FR-009`; `ARK-NFR-004`; `ARK-CON-002`, `ARK-CON-005`.
- **Responsibility and non-responsibilities:** Claim jobs and invoke one public ingestion/capability handler; no lifecycle authority, private cross-call, or implicit training/activation.
- **Stages/workflows where used:** Every durable pipeline; Stage 08/10/15/22.
- **Trigger and prerequisites:** Claimable authorized job with immutable references/versions.
- **Inputs/outputs and contract versions:** Job context → progress, result/reference, failure reason, attempt transition.
- **State and authoritative storage owner:** Job state owned by `C05-08`; capability/data module owns computation/output.
- **Upstream/downstream dependencies:** `C05-08`; `C05-06`, `C05-11`, storage/registry downstream.
- **Critical-path or supporting-path role:** Async critical execution path.
- **Failure effect and user-visible status:** Lease expiry/process death permits safe reclaim; duplicate attempt produces one logical effect.
- **Timeout/retry/idempotency/cancellation:** At-least-once, lease/heartbeat as needed, idempotent effects, safe-point cancellation.
- **Security and tenant-isolation controls:** Scoped worker identity, tenant-qualified references, schema least privilege.
- **Observability and audit:** Claim delay, active work, attempt/failure, progress, versions, resource use.
- **Scaling/resource isolation:** Same codebase with logical pools by workload/capability; split roles only from measurement.
- **Simplest viable implementation:** PostgreSQL-polling worker loops and modular handlers.
- **Alternative considered and rejection reason:** One undifferentiated pool or broker-first; interference/unsupported infrastructure.
- **Operational burden and owner:** Platform runtime plus data/capability handler owners.
- **Reconsideration/extraction trigger:** Resource/hardware/reliability trigger in ADR-003.
- **Effect if removed, moved, delayed, or replaced:** Durable jobs cannot execute; runtime movement must preserve handler contract/ownership.

### Component specification — C05-11 Seven capability modules

- **Classification:** `required now` as product modules; release/production eligibility remains per Stage 03.
- **Requirement(s):** `ARK-FR-004`–`ARK-FR-010`, `ARK-FR-012`; `ARK-NFR-001`–`ARK-NFR-007`; `ARK-CON-002`, `ARK-CON-003`.
- **Responsibility and non-responsibilities:** Own capability contracts/science/config/private pipelines/artifacts/evaluation/results/runbooks; not platform lifecycle, other capability state, tenant authority, or external-action authority.
- **Stages/workflows where used:** Eligible sync/durable invocation; Stage 10/14/16 refine.
- **Trigger and prerequisites:** Platform admission, ready dataset/context, active approved versions, capability scientific eligibility.
- **Inputs/outputs and contract versions:** Common envelope + capability schema/dataset refs/version context → explicit eligible/degraded/fallback/ineligible/result/error with lineage.
- **State and authoritative storage owner:** Each capability owns schema/object namespaces, feature/result/artifact/evaluation/config migrations; no cross-writes.
- **Upstream/downstream dependencies:** `C05-04`–`C05-10`, `C05-14`–`C05-17`; result/audit downstream.
- **Critical-path or supporting-path role:** Critical computation for its operation.
- **Failure effect and user-visible status:** Bounded capability failure/ineligibility; cannot corrupt another module or claim success on missing authoritative result.
- **Timeout/retry/idempotency/cancellation:** Operation-declared; durable jobs at-least-once safe; no inference-time training; safe cancellation points.
- **Security and tenant-isolation controls:** Principal/job tenant, opaque IDs, least-privilege datasets/artifacts, no consumer/private cross-access.
- **Observability and audit:** Operation/outcome, dataset/feature/model/config/code/execution versions, quality/fallback/drift/resource signals.
- **Scaling/resource isolation:** Worker pools/roles first; service extraction only through ADR-003 and owner gate.
- **Simplest viable implementation:** Seven enforced modules/public ports inside one codebase, owned schemas/namespaces.
- **Alternative considered and rejection reason:** Service per capability or shared generic ML module; no evidence or destroys ownership.
- **Operational burden and owner:** Per-capability logical role under A-04; named owner required before production.
- **Reconsideration/extraction trigger:** Per ADR-003 measured triggers and stable contract/owner/runbook.
- **Effect if removed, moved, delayed, or replaced:** Removes that product capability only; shared platform remains; Synapse cannot be enabled without evidence.

### Component specification — C05-12 Result and notification delivery

- **Classification:** `required now` (polling); signed webhook `useful soon`.
- **Requirement(s):** `ARK-FR-005`, `ARK-FR-007`, `ARK-FR-010`, `ARK-FR-011`; `ARK-NFR-003`, `ARK-NFR-004`, `ARK-NFR-006`.
- **Responsibility and non-responsibilities:** Expose authenticated status/result and deliver completion/finding notices; transport never owns or changes capability result and never sends customer campaigns.
- **Stages/workflows where used:** Sync/async completion and proactive notification; Stage 07/09 details.
- **Trigger and prerequisites:** Committed job/result/notification intent and authorized caller/destination.
- **Inputs/outputs and contract versions:** Job/result ID → status/bounded result/reference; intent → signed idempotent webhook receipt.
- **State and authoritative storage owner:** Job/capability owns result; integration owns delivery attempts/deduplication.
- **Upstream/downstream dependencies:** `C05-05`, `C05-08`, `C05-11`, `C05-13/14`; consumer downstream.
- **Critical-path or supporting-path role:** Polling is critical retrieval; webhook supporting convenience.
- **Failure effect and user-visible status:** Delivery pending/retrying/failed while result remains authoritative/succeeded; polling recovery remains.
- **Timeout/retry/idempotency/cancellation:** Safe repeated GET; webhook at-least-once with delivery ID and bounded later policy; cancellation stops pending delivery where safe.
- **Security and tenant-isolation controls:** Tenant-bound lookup, opaque/signed object access, authorized callback, SSRF/signing controls deferred.
- **Observability and audit:** Retrieval/delivery attempts, acknowledgements, failures, destination health, correlation.
- **Scaling/resource isolation:** Shared workers initially; separate delivery pool on measured backlog.
- **Simplest viable implementation:** Job/result HTTP endpoints plus delivery records dispatched by shared workers.
- **Alternative considered and rejection reason:** Capability-owned callbacks, SSE baseline, broker dependency; couples computation or lacks need.
- **Operational burden and owner:** Integration role; destination/runbook management.
- **Reconsideration/extraction trigger:** Consumer contract evidence or measured delivery isolation need.
- **Effect if removed, moved, delayed, or replaced:** Polling removal leaves no universal result path; webhook may be delayed without losing results.

### Component specification — C05-13 Operational PostgreSQL

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-001`, `ARK-FR-003`, `ARK-FR-007`; `ARK-NFR-001`, `ARK-NFR-004`, `ARK-NFR-006`; `ARK-CON-002`, `ARK-CON-004`, `ARK-CON-005`.
- **Responsibility and non-responsibilities:** Durable operational/control/catalog/job/registry/audit metadata in owned schemas; not large history/artifact payloads.
- **Stages/workflows where used:** Every control/job/catalog/registry transition; Stage 06/08/13/15.
- **Trigger and prerequisites:** Module repository operation under authenticated/worker tenant context.
- **Inputs/outputs and contract versions:** Narrow module persistence commands/queries; schemas/migrations versioned by owner.
- **State and authoritative storage owner:** Shared cluster infrastructure; each module owns schemas/tables/migrations/writer.
- **Upstream/downstream dependencies:** All stateful modules; object store holds large objects.
- **Critical-path or supporting-path role:** Critical shared infrastructure with logical failure boundaries.
- **Failure effect and user-visible status:** Fail closed/pause work; committed state survives process restart; no false acceptance.
- **Timeout/retry/idempotency/cancellation:** Transactions, uniqueness, leases/CAS; retries at owner boundaries, not blind transaction replay.
- **Security and tenant-isolation controls:** Tenant keys, least-privilege schema roles, RLS defense-in-depth, encrypted connections later.
- **Observability and audit:** Query/transaction latency, errors, locks/contention, connections, storage, claim behavior.
- **Scaling/resource isolation:** Index/query/batch/pool tuning first; extraction/split only via ADR-003.
- **Simplest viable implementation:** One PostgreSQL cluster with module-owned schemas.
- **Alternative considered and rejection reason:** DB per module/service or shared unrestricted schema; unsupported burden or boundary erosion.
- **Operational burden and owner:** Platform DB role plus each module migration owner.
- **Reconsideration/extraction trigger:** Measured capacity/reliability/compliance boundary after simpler remedies.
- **Effect if removed, moved, delayed, or replaced:** Initial durable design fails; replacement requires safe migration and same ownership semantics.

### Component specification — C05-14 Object storage / ARK data lake

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-002`, `ARK-FR-003`, `ARK-FR-007`; `ARK-NFR-001`, `ARK-NFR-002`, `ARK-NFR-005`; `ARK-CON-004`.
- **Responsibility and non-responsibilities:** Store immutable raw, canonical/curated, capability-derived, large results, models/artifacts, quality/lineage evidence; not operational job/control authority.
- **Stages/workflows where used:** Ingestion, training, inference, result retrieval; Stage 06/10/15.
- **Trigger and prerequisites:** Registered tenant/source/dataset/version/run identity and authorized write/read.
- **Inputs/outputs and contract versions:** Object bytes/files + metadata → immutable tenant/version-qualified reference/checksum; authorized reference → content.
- **State and authoritative storage owner:** Data platform owns raw/curated namespaces; each capability owns derived/result/artifact namespaces.
- **Upstream/downstream dependencies:** Ingestion/capabilities/registry/catalog; operational metadata in PostgreSQL.
- **Critical-path or supporting-path role:** Critical for large data/artifacts; supporting for small inline results.
- **Failure effect and user-visible status:** Upload/read failure prevents readiness/success; orphan/partial object never published as ready.
- **Timeout/retry/idempotency/cancellation:** Content/checksum/idempotency identity, multipart retry later, cancellation leaves unreferenced partial cleanup.
- **Security and tenant-isolation controls:** Tenant/path namespace, scoped access, opaque references, encryption/access policy later, no public raw paths.
- **Observability and audit:** Bytes/objects, checksum failure, access denial, latency, orphan cleanup, lineage access.
- **Scaling/resource isolation:** Native object partition/namespaces; no invented tiers; lifecycle/retention later.
- **Simplest viable implementation:** One object-storage interface with enforced path/metadata conventions.
- **Alternative considered and rejection reason:** Large payloads in PostgreSQL or direct consumer buckets; violates baseline/control.
- **Operational burden and owner:** Data/platform storage plus capability namespace owners.
- **Reconsideration/extraction trigger:** Residency/compliance/provider constraint or measured storage boundary.
- **Effect if removed, moved, delayed, or replaced:** Raw-first reproducibility and large artifacts/results fail; provider may change behind interface.

### Component specification — C05-15 Capability-owned feature/result/state storage

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-006`, `ARK-FR-009`; `ARK-NFR-001`, `ARK-NFR-002`; `ARK-CON-002`, `ARK-CON-004`.
- **Responsibility and non-responsibilities:** Hold capability-private derived features, results, configuration/state, evaluation references; no shared universal feature/business state or other-capability writes.
- **Stages/workflows where used:** Capability preparation/execution/evaluation; Stage 06/10.
- **Trigger and prerequisites:** Authorized capability job with dataset/feature schema/version.
- **Inputs/outputs and contract versions:** Versioned derived rows/objects/results keyed by tenant/dataset/feature/model/execution.
- **State and authoritative storage owner:** Each capability owns PostgreSQL schema and object-store namespace/migrations.
- **Upstream/downstream dependencies:** Catalog/lake/capability/model registry; result delivery reads public result contract only.
- **Critical-path or supporting-path role:** Critical where features/state/results are persisted.
- **Failure effect and user-visible status:** No terminal success until authoritative result commit; feature failure yields explicit capability failure/ineligibility.
- **Timeout/retry/idempotency/cancellation:** Execution/idempotency-qualified writes; immutable/versioned features where possible; cancellation avoids publishing incomplete result.
- **Security and tenant-isolation controls:** Tenant keys/paths, capability role least privilege, opaque IDs, no cross-schema writes.
- **Observability and audit:** Write/read failure, feature schema/version, counts/quality, result commit, lineage.
- **Scaling/resource isolation:** PostgreSQL for bounded state, object store for large data; separate feature product only on evidence.
- **Simplest viable implementation:** Owned schemas and lake namespaces behind capability repositories.
- **Alternative considered and rejection reason:** Shared feature-store product/universal table; no cross-capability reuse/online consistency need proven.
- **Operational burden and owner:** Per-capability role; schema/quality/migration runbook.
- **Reconsideration/extraction trigger:** Proven online/offline consistency, reuse, latency, or isolation need through ADR-003/Stage 10.
- **Effect if removed, moved, delayed, or replaced:** Capability loses reproducible owned state; provider change must preserve lineage/ownership.

### Component specification — C05-16 Model/artifact registry

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-004`, `ARK-FR-006`, `ARK-FR-009`; `ARK-NFR-001`, `ARK-NFR-002`, `ARK-NFR-006`; `A-03-ML-MIGRATION`.
- **Responsibility and non-responsibilities:** Register immutable artifact identity/location/lineage/evaluation/lifecycle status and active binding; capability owns scientific promotion authority; inference cannot train/activate.
- **Stages/workflows where used:** Training, evaluation, promotion, invocation; Stage 10 details.
- **Trigger and prerequisites:** Explicit authorized lifecycle command with artifact/evaluation evidence.
- **Inputs/outputs and contract versions:** Artifact metadata/object reference/evaluation → registered version; authorized query → exact active bundle or none.
- **State and authoritative storage owner:** Platform registry owns common metadata schema; capability owns artifacts/evaluations/promotion decisions; objects in lake.
- **Upstream/downstream dependencies:** `C05-11`, `C05-14/15`, control/audit; workers consume fixed references.
- **Critical-path or supporting-path role:** Critical version selection; training registration supporting.
- **Failure effect and user-visible status:** Missing/ambiguous/inactive artifact yields ineligible/no execution; never nondeterministic latest lookup.
- **Timeout/retry/idempotency/cancellation:** Idempotent registration by immutable identity; promotion CAS/audited; no inference side effects.
- **Security and tenant-isolation controls:** Tenant/capability namespaces, promotion roles, scoped artifact access.
- **Observability and audit:** Registrations/promotions/rollbacks, selection failure, versions, evaluation links, access.
- **Scaling/resource isolation:** Relational metadata/object artifacts first; standalone product optional later.
- **Simplest viable implementation:** Owned PostgreSQL registry tables and object references with narrow interface.
- **Alternative considered and rejection reason:** Generic mutable shared handler or standalone product now; nondeterminism/unsupported burden.
- **Operational burden and owner:** Platform registry plus each capability lifecycle owner.
- **Reconsideration/extraction trigger:** Stage 10 proves lifecycle controls/scale uniquely require another implementation.
- **Effect if removed, moved, delayed, or replaced:** Reproducibility and explicit activation fail; replacement must preserve immutable lineage.

### Component specification — C05-17 Secrets and technical configuration delivery

- **Classification:** `required now`.
- **Requirement(s):** `ARK-NFR-001`, `ARK-NFR-005`, `ARK-NFR-006`; `A-01-SEC`.
- **Responsibility and non-responsibilities:** Deliver/rotate scoped credentials, signing/encryption keys, and technical runtime settings; no business/scientific policy and no secrets in contracts/logs.
- **Stages/workflows where used:** All protected integrations/runtime roles; Stage 12/15.
- **Trigger and prerequisites:** Authorized workload identity requesting secret/config reference.
- **Inputs/outputs and contract versions:** Secret/config reference → runtime-scoped value/version; values never public output.
- **State and authoritative storage owner:** Environment/platform secret facility; module-owned nonsecret config elsewhere.
- **Upstream/downstream dependencies:** Every DB/storage/provider/webhook integration.
- **Critical-path or supporting-path role:** Critical for protected dependency; fail closed.
- **Failure effect and user-visible status:** Dependency unavailable/auth failure; no fallback to plaintext/default secret.
- **Timeout/retry/idempotency/cancellation:** Bounded retrieval/rotation; no logged retries containing value.
- **Security and tenant-isolation controls:** Workload least privilege, audit, scoped namespaces; tenant-specific keys only if policy requires.
- **Observability and audit:** Reference/version/access/rotation failure without values.
- **Scaling/resource isolation:** Deployment facility; no product/capacity choice now.
- **Simplest viable implementation:** Runtime injection behind application interface.
- **Alternative considered and rejection reason:** Plain files/DB fields/vendor selection now; unsafe/unsupported.
- **Operational burden and owner:** Security/platform operations role.
- **Reconsideration/extraction trigger:** Stage 15 environment/compliance constraints.
- **Effect if removed, moved, delayed, or replaced:** Secure dependencies cannot run; implementation replaceable behind interface.

### Component specification — C05-18 Audit, lineage, usage, and metering ledger

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-001`, `ARK-FR-003`, `ARK-FR-007`, `ARK-FR-010`, `ARK-FR-012`; `ARK-NFR-002`, `ARK-NFR-006`.
- **Responsibility and non-responsibilities:** Durable evidence of actors/decisions/mutations/data/model/execution/result/grant/usage/notification; not diagnostic telemetry or automated invoicing.
- **Stages/workflows where used:** Every authoritative transition; Stage 06/09/10/12/14.
- **Trigger and prerequisites:** Material control/data/lifecycle/security/result action.
- **Inputs/outputs and contract versions:** Tenant/actor/action/target/version/reason/correlation → append-oriented evidence; query/export → authorized trace.
- **State and authoritative storage owner:** Audit/usage schemas and object references; source module retains business authority.
- **Upstream/downstream dependencies:** All modules emit; admin/LAB consume.
- **Critical-path or supporting-path role:** Critical for security-sensitive action and reproducibility; usage may coordinate with result commit.
- **Failure effect and user-visible status:** Mandatory audit failure prevents sensitive mutation/action; diagnostic export failure is separate.
- **Timeout/retry/idempotency/cancellation:** Idempotent evidence identity; append/supersede, not overwrite; retention later.
- **Security and tenant-isolation controls:** Restricted access, tenant isolation, minimization/redaction, tamper-evident controls later.
- **Observability and audit:** Missing emission, write failure, trace completeness, usage reconciliation.
- **Scaling/resource isolation:** PostgreSQL first with large evidence by object reference; archive/partition after measurement/policy.
- **Simplest viable implementation:** Structured append records in owned PostgreSQL tables plus lineage references.
- **Alternative considered and rejection reason:** Application logs or broker-first ledger; not authoritative/unsupported.
- **Operational burden and owner:** Security/governance/platform operations role.
- **Reconsideration/extraction trigger:** Retention/compliance/volume evidence.
- **Effect if removed, moved, delayed, or replaced:** Audit/reproducibility/metering requirements fail; storage may change only preserving semantics.

### Component specification — C05-19 Observability

- **Classification:** `required now`.
- **Requirement(s):** `ARK-NFR-002`, `ARK-NFR-006`, `ARK-NFR-007`; `ARK-FR-012`.
- **Responsibility and non-responsibilities:** Correlated logs/metrics/traces for component/runtime/quality signals; not business/audit truth or evaluation authority.
- **Stages/workflows where used:** All modules/roles; Stage 14 details.
- **Trigger and prerequisites:** Request/job/worker/storage/notification activity.
- **Inputs/outputs and contract versions:** Structured signal with correlation, tenant-safe context, module/operation/version/outcome → telemetry sink.
- **State and authoritative storage owner:** Operations telemetry system; retention/product unresolved.
- **Upstream/downstream dependencies:** All emit; operations/LAB consume.
- **Critical-path or supporting-path role:** Supporting; mandatory audit remains separate.
- **Failure effect and user-visible status:** Visibility degraded/incident; must not fabricate business failure/success.
- **Timeout/retry/idempotency/cancellation:** Bounded async emission; avoid retry storms; detailed policy later.
- **Security and tenant-isolation controls:** Access control, PII/secret/raw-payload minimization, tenant-safe dimensions.
- **Observability and audit:** Dropped signals/export failure/cardinality/volume monitor observability itself.
- **Scaling/resource isolation:** Shared instrumentation first; sinks/exporters scale on measurement.
- **Simplest viable implementation:** Common structured logging/metrics/tracing interfaces in one codebase.
- **Alternative considered and rejection reason:** Per-capability stacks/vendor commitment; duplication/unsupported.
- **Operational burden and owner:** Operations plus module owners for signals/runbooks.
- **Reconsideration/extraction trigger:** Stage 14/15 target/product evidence.
- **Effect if removed, moved, delayed, or replaced:** Operability/LAB evidence fails; backend replaceable behind interface.

### Component specification — C05-20 Administration and operational interfaces

- **Classification:** `required now`.
- **Requirement(s):** `ARK-FR-001`, `ARK-FR-007`, `ARK-FR-010`, `ARK-FR-012`; `ARK-NFR-001`, `ARK-NFR-006`.
- **Responsibility and non-responsibilities:** Authorized tenant/control/config/schedule/job/dataset/artifact/audit inspection and safe commands; no direct SQL, rule bypass, or business-user UI.
- **Stages/workflows where used:** Onboarding, support, incident response, LAB; Stage 07/12/14.
- **Trigger and prerequisites:** Privileged authenticated role and scoped command.
- **Inputs/outputs and contract versions:** Versioned admin query/command → audited result/status.
- **State and authoritative storage owner:** Owning modules retain state; admin surface owns none.
- **Upstream/downstream dependencies:** Operator/LAB upstream; public owner-module admin ports downstream.
- **Critical-path or supporting-path role:** Supporting/operational.
- **Failure effect and user-visible status:** Admin unavailable without corrupting work; unsafe/unauthorized command rejected.
- **Timeout/retry/idempotency/cancellation:** Idempotent mutations, explicit confirmation, job cancellation only through lifecycle.
- **Security and tenant-isolation controls:** Privileged roles, least privilege, tenant scope, immutable audit.
- **Observability and audit:** Every command/outcome/actor/target/version/correlation.
- **Scaling/resource isolation:** Low-volume assumption is not made; optimize from measurements; isolate from public API if risk later.
- **Simplest viable implementation:** Authenticated admin API plus CLI/runbook.
- **Alternative considered and rejection reason:** Bespoke UI/direct DB; unsupported or bypasses ownership.
- **Operational burden and owner:** Platform/control/operations roles.
- **Reconsideration/extraction trigger:** Operator workflow/security evidence.
- **Effect if removed, moved, delayed, or replaced:** Operability/LAB/support gaps; UI can be delayed, minimal API cannot.

### Component specification — C05-21 Internal reliable-publication adapter

- **Classification:** `useful soon`.
- **Requirement(s):** `ARK-FR-011`; `ARK-NFR-004`, `ARK-NFR-006`; `ARK-CON-005`, `ARK-CON-007`.
- **Responsibility and non-responsibilities:** Publish/consume versioned internal coordination facts reliably when a concrete boundary needs temporal decoupling; not external notifications or business truth.
- **Stages/workflows where used:** Potential Stage 09/13 boundaries; absent from first synchronous/direct flows.
- **Trigger and prerequisites:** Approved event contract, idempotent consumer, source commit, delivery/replay/failure semantics.
- **Inputs/outputs and contract versions:** Tenant/correlation/producer/version/event/idempotency → delivery attempts/consumer outcome.
- **State and authoritative storage owner:** Source module owns fact; publication adapter/outbox owns delivery state only.
- **Upstream/downstream dependencies:** Source transaction upstream; public consumer handler downstream.
- **Critical-path or supporting-path role:** Supporting unless a later ADR explicitly makes it critical.
- **Failure effect and user-visible status:** Source fact remains committed; publication pending/failed visible; consumer retry cannot duplicate logical effect.
- **Timeout/retry/idempotency/cancellation:** At-least-once, idempotent consumer, poison/dead-letter policy before activation; no silent loss.
- **Security and tenant-isolation controls:** Tenant-qualified minimal payload, authorized producer/consumer, no PII by default.
- **Observability and audit:** Lag, attempts, duplicate, failure, unhandled version, trace linkage.
- **Scaling/resource isolation:** PostgreSQL outbox/worker first if justified; broker only via `X05-02` trigger.
- **Simplest viable implementation:** Transactional outbox table plus shared worker, when Stage 09/13 requires it.
- **Alternative considered and rejection reason:** Event broker/backbone immediately; no evidence and extra operations.
- **Operational burden and owner:** Platform execution/integration plus producer/consumer owners.
- **Reconsideration/extraction trigger:** Measured fan-out/throughput/replay need after outbox/direct jobs.
- **Effect if removed, moved, delayed, or replaced:** No effect until an approved event path depends on it; direct/job coordination remains.

### Component specification — C05-22 Named-workflow API and coordinator

- **Classification:** `useful soon`.
- **Requirement(s):** `ARK-FR-007`, `ARK-FR-010`; `ARK-NFR-003`, `ARK-NFR-004`; scheduler/orchestration baseline.
- **Responsibility and non-responsibilities:** Expose approved named workflow commands and persist/advance parent-child job state; no generic DAG/DSL, engine product, or capability-private pipeline ownership.
- **Stages/workflows where used:** Only a release-scoped multi-job/proactive workflow; Stage 08/09.
- **Trigger and prerequisites:** Versioned authorized workflow definition with public child operations and failure policy.
- **Inputs/outputs and contract versions:** Workflow request → parent/child references, progress, partial/terminal result.
- **State and authoritative storage owner:** Orchestration owns definition/parent transitions; `C05-08` owns child jobs.
- **Upstream/downstream dependencies:** `C05-04/05/09`; job manager/public capability handlers.
- **Critical-path or supporting-path role:** Critical only for participating workflow.
- **Failure effect and user-visible status:** Persist waiting/partial/failed/cancel; child result remains authoritative if aggregation fails.
- **Timeout/retry/idempotency/cancellation:** Workflow idempotency, restartable transitions, bounded policy retries, child cancellation where supported.
- **Security and tenant-isolation controls:** Children inherit/narrow, never broaden, tenant/grant/data scope.
- **Observability and audit:** Parent-child graph, transitions/waits/retries/partial state, versions.
- **Scaling/resource isolation:** Explicit state machine first; general engine only at `X05-09` trigger.
- **Simplest viable implementation:** Named application command and parent/child PostgreSQL records.
- **Alternative considered and rejection reason:** Caller-programmable workflow or Temporal-like product now; no named complexity evidence.
- **Operational burden and owner:** Platform orchestration plus child capability owners.
- **Reconsideration/extraction trigger:** Named release workflow or measured workflow complexity.
- **Effect if removed, moved, delayed, or replaced:** Single-capability/job flows unaffected; no multi-job aggregate API.

## Analysis and recommendations

### R-05-01 — Keep component boundaries logical and map them to the approved modular monolith

- **Requirement satisfied:** `ARK-CON-001`–`ARK-CON-003`; complete end-to-end component path.
- **Where/when used:** Stage 05 inventory; Stages 06–10, 12–15, 22.
- **Why needed now:** The prompt's component list could otherwise be misread as a service/product list.
- **Simplest viable implementation:** `C05-01`–`C05-22` as public modules/roles/interfaces in one codebase, with owned state and optional same-codebase roles.
- **Alternative considered:** Independently deploy every component.
- **Why not preferred:** Violates ADR-003 extraction gate and lacks scale/team evidence.
- **Trade-offs/operational burden:** Fewer distributed failures; stronger code/schema governance required.
- **Reconsideration trigger:** A specific component passes ADR-003's measured extraction gate.

### R-05-02 — Make PostgreSQL jobs and polling the minimum durable backbone

- **Requirement satisfied:** `ARK-FR-007`, `ARK-FR-008`, `ARK-FR-011`; `ARK-NFR-004`; `ARK-CON-005`.
- **Where/when used:** All durable flows; Stages 07/08/13.
- **Why needed now:** Long/retryable work and result retrieval must survive process failure without speculative broker infrastructure.
- **Simplest viable implementation:** Transactional job/attempt/claim tables, same-codebase workers, job status/result endpoints.
- **Alternative considered:** Broker, per-capability queues, workflow engine, webhook-only delivery.
- **Why not preferred:** Adds truth/operations or lacks universal recoverable retrieval.
- **Trade-offs/operational burden:** Job manager becomes critical; PostgreSQL contention must be measured/managed.
- **Reconsideration trigger:** Approved coordination/throughput/workflow targets fail after indexing/batching/pool isolation.

### R-05-03 — Preserve three independent admission decisions

- **Requirement satisfied:** `ARK-FR-006`, `SC-02-04`.
- **Where/when used:** Every dataset-dependent sync/job execution; Stages 06–10.
- **Why needed now:** Centralizing scientific logic or allowing raw data bypass would reproduce prototype defects.
- **Simplest viable implementation:** `C05-06/07` publishes dataset readiness; `C05-04` returns platform eligibility; `C05-11` returns scientific eligibility.
- **Alternative considered:** One generic eligibility flag/service.
- **Why not preferred:** Hides authority/reason/fallback and couples capabilities.
- **Trade-offs/operational burden:** More explicit states/contracts; safer diagnosis and ownership.
- **Reconsideration trigger:** None for separation; schemas may evolve by later contract decisions.

### R-05-04 — Store large immutable data by reference and bounded operational truth in PostgreSQL

- **Requirement satisfied:** `ARK-FR-003`, `ARK-NFR-002`; `ARK-CON-004`.
- **Where/when used:** Ingestion, datasets, features, results, models; Stages 06/10/15.
- **Why needed now:** Raw-first reproducibility and large histories/artifacts cannot rely on request payloads or operational tables.
- **Simplest viable implementation:** `C05-14` object interface plus `C05-13` owned metadata and `C05-07/16` registries.
- **Alternative considered:** Large payloads in PostgreSQL or direct shared consumer storage.
- **Why not preferred:** Violates baseline, lineage, and ownership.
- **Trade-offs/operational burden:** Requires reference integrity/orphan cleanup/access controls; avoids DB bloat.
- **Reconsideration trigger:** Storage/residency evidence changes implementation, not logical split.

### R-05-05 — Separate authoritative audit from supporting telemetry

- **Requirement satisfied:** `ARK-NFR-002`, `ARK-NFR-006`; `ARK-FR-010`, `ARK-FR-012`.
- **Where/when used:** Every boundary; Stages 12–14/16.
- **Why needed now:** Logs cannot prove security decisions, lineage, usage, or no-action enforcement.
- **Simplest viable implementation:** Transaction/owner-emitted append audit ledger plus shared instrumentation interfaces.
- **Alternative considered:** Use logs as audit or make telemetry critical to every transaction.
- **Why not preferred:** Logs are mutable/lossy; telemetry coupling harms availability.
- **Trade-offs/operational burden:** Two evidence paths must correlate; clearer authority/failure semantics.
- **Reconsideration trigger:** Retention/compliance/volume changes storage, not separation.

### R-05-06 — Defer commonly expected infrastructure until its trigger is evidenced

- **Requirement satisfied:** `ARK-CON-005`, `ARK-CON-007`; ADR-003 anti-overengineering/extraction gate.
- **Where/when used:** Stage 05 rejections; Stages 09/15/17/23.
- **Why needed now:** Load balancer, broker, service registry, cache, gateway/registry products, SSE, and workflow engine are easy to add speculatively.
- **Simplest viable implementation:** Logical edge, direct ports/jobs, polling, owned schemas, relational registries, object storage.
- **Alternative considered:** Preinstall the conventional distributed stack.
- **Why not preferred:** No measured/environment requirement; adds failure/operations/cost.
- **Trade-offs/operational burden:** Some mechanisms may be introduced later; each arrives with known semantics and owner.
- **Reconsideration trigger:** The explicit `X05-*` or ADR-003 trigger for that component.

## Decisions

- Stage 05 introduces no new material architecture decision or ADR. It applies accepted ADR-003 to the end-to-end logical component inventory.
- Required-now is a logical first-version responsibility classification, not a promise of a separate process/product/service.
- Polling and PostgreSQL-backed durable jobs are the minimum async path; signed webhook, named workflow coordination, and reliable internal publication are useful-soon seams, not unconditional products.
- Event broker, general workflow engine, distinct load balancer, shared cache, dynamic service registry, SSE, standalone feature store, and standalone model-registry/gateway products remain conditional/unjustified as recorded.
- No component makes Synapse production-eligible or infers its internals.

## Contradictions and dangerous assumptions

| ID | Tension/hazard | Treatment | Consequence |
|---|---|---|---|
| `C-05-01` | Prompt lists many conventional components, but ADR-003 rejects speculative distribution | Map responsibilities to logical modules; explicitly classify exclusions | Component count does not become service/product count |
| `C-05-02` | Shared PostgreSQL could enable cross-module joins/writes | Owned schemas/migrations/writers and public ports mandatory | Stage 06 must forbid unrestricted shared access |
| `C-05-03` | API gateway could absorb control/science/orchestration | Thin edge only | Eligibility and workflow remain owner modules |
| `C-05-04` | Database task queue is durable truth but may face future scale | Index/batch/pool/role first; broker trigger explicit | No broker now; Stage 17 measures |
| `C-05-05` | Dataset readiness, platform eligibility, and science often collapse into one flag | Three separate owners/outcomes | Consumers receive precise non-success reasons |
| `C-05-06` | Webhook success can be confused with capability success | Result authority and delivery state separate; polling recovery | Notification retry never reruns capability |
| `C-05-07` | Audit and logs are often conflated | Durable audit ledger separate from telemetry | Security-sensitive work may fail closed on audit while telemetry degrades separately |
| `C-05-08` | Feature/model registry names imply standalone products | Logical registries/namespaces on accepted stores first | Stage 10 may later justify products |
| `C-05-09` | Synapse verifier status could pass proactive authorization | Control/policy module authoritative; verifier advisory | Missing/ambiguous policy yields no action |
| `C-05-10` | Stage 05 requested a data/ML specialist, but the thread limit prevented creation | Primary performed evidence-based analysis and records limitation | No fabricated specialist endorsement; user may require another review later |

## Open questions

| ID | Question | Blocking? | Options | Recommended temporary assumption | Effect |
|---|---:|---|---|---|---|
| `Q-05-01` | Which capability/workflow is first release scope? | No for logical path; before roadmap/acceptance | One vertical slice; subset; phases | Keep all modules product-scoped, activate only evidence-ready release slice | Runtime/load cannot yet be committed |
| `Q-05-02` | Exact adapter placement and consumer delivery contract? | Stage 07 | Consumer-owned; ARK-owned; mixed; polling/webhook | Keep cores neutral; polling universal; webhook useful soon | Integration ownership remains conditional |
| `Q-05-03` | Which synchronous operations meet a measured short/predictable boundary? | Before production/API admission | Measure each; async-only default | No unmeasured operation admitted as sync | Stage 07/08 define classifications |
| `Q-05-04` | Exact job states, retry, timeout, lease, cancellation, partial-result semantics? | Stage 08/13 | Per operation policies under common state machine | Preserve responsibility only; no numeric policy invented | Component specs remain implementable at responsibility level |
| `Q-05-05` | Data schemas, readiness policies, retention/deletion/residency? | Stage 06/12/15/production data | Supply policies; tenant policies; scope data | Raw-first/versioned references, durations TBD | Data components remain conditional for production |
| `Q-05-06` | Model/prompt/artifact lifecycle and Synapse internals? | Stage 10/ADR-002 expiries | Evidence; scope out; retain unavailable | Keep registry logical and Synapse non-production-eligible | No hidden provider/model decisions |
| `Q-05-07` | Does a named multi-job workflow require `C05-22`? | Before implementation | None; explicit workflow; general engine | Include seam as useful soon, no engine | Avoids unused orchestration product |
| `Q-05-08` | Should a data/ML specialist re-review Stage 05 when an agent slot becomes available? | Not blocking content; assurance preference | Re-review; rely on primary; defer to Stage 06 specialist | Re-review at Stage 06 or on user request | Records process gap without blocking validated component fields |

## Requirements-traceability updates

| Requirement | Architecture element(s) | Verification direction |
|---|---|---|
| `ARK-FR-001` | `C05-03`, `C05-04`, `C05-13`, `C05-18`, `C05-20` | Subscription/control separation and rejection tests |
| `ARK-FR-002/003` | `C05-01`, `C05-06`–`C05-10`, `C05-14` | Push/bulk, raw-first, validation/publication/lineage tests |
| `ARK-FR-004/005` | `C05-02`–`C05-05`, `C05-11` | Definition/envelope/schema/version tests |
| `ARK-FR-006` | `C05-04`, `C05-07`, `C05-11` | Independent readiness/eligibility scenario tests |
| `ARK-FR-007/008` | `C05-05`, `C05-08`–`C05-10`, `C05-12` | State/restart/duplicate/cancel/result and sync-classification tests |
| `ARK-FR-009` | `C05-10`, `C05-11`, `C05-16` | No inference training/activation; promotion lineage tests |
| `ARK-FR-010` | `C05-03`, `C05-04`, `C05-09`, `C05-18`, `C05-22` | No-action grant/policy negative suite |
| `ARK-FR-011` | `C05-12`, `C05-21` | Internal/external contract and idempotent delivery tests |
| `ARK-FR-012` | `C05-18`–`C05-20` plus all component evidence | LAB contract/isolation/reproducibility/failure suite |
| `ARK-NFR-001` | Tenant context plus every stateful component | Cross-tenant negative suite across rows/objects/jobs/artifacts/results/audit/telemetry |
| `ARK-NFR-002/003` | `C05-05`–`C05-07`, `C05-11`, `C05-14`–`C05-18` | End-to-end lineage and schema compatibility tests |
| `ARK-NFR-004` | `C05-08`–`C05-12`, `C05-21/22` | At-least-once duplicate/fault-injection tests |
| `ARK-NFR-005` | `C05-01`, `C05-03`, `C05-06/07`, `C05-11`, storage/evidence | Opaque-ID/PII/schema/logging/provider tests |
| `ARK-NFR-006` | `C05-18`, `C05-19` integrated across all | Trace/audit/usage completeness tests |
| `ARK-NFR-007` | `X05-*` gates and every component scaling field | Approved targets/measurements before topology/product decisions |
| `ARK-CON-001/002` | All `C05-*` as modules/roles with owned state | Dependency/schema/migration/one-writer checks |
| `ARK-CON-003` | `C05-01`, `C05-05`, `C05-11` | No consumer terminology/dependency in cores |
| `ARK-CON-004/005` | `C05-08`, `C05-13`, `C05-14` | Storage placement and PostgreSQL job-recovery tests |
| `ARK-CON-006` | `C05-01`, `C05-03`, `C05-06/07` | Source-authority/opaque-identity negative tests |
| `ARK-CON-007` | Conditional/rejected inventory | Component trace/trigger review |

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Every component named in governing section evaluated | PASS | Source-instruction coverage maps every bullet |
| Only justified components included; expected unnecessary components rejected | PASS | `C05-*` inventory and `X05-*` table |
| Included component has all component-spec fields | PASS | Twenty-two specifications cover responsibility, interfaces, state, dependencies, failure, reliability, security, observability, scaling, implementation, alternative, burden, owner, trigger, removal effect |
| Control/data/capability/integration/operational boundaries explicit | PASS | Boundary map |
| Complete consumer/source-to-result paths defined | PASS | Sync, async, and ingestion flow tables |
| Component classifications use required taxonomy | PASS | Inventory includes required-now/useful-soon; conditional table includes scale-triggered/optional/unjustified |
| Approved architecture style and ownership rules preserved | PASS | No service-per-component; all owners logical under A-04 |
| Unknown scale/SLO/environment remains unknown | PASS | No numeric target/topology/vendor invented |
| Specialist findings reconciled honestly | PASS WITH RECORDED PROCESS LIMIT | Platform review reconciled; data/ML specialist spawn blocked by thread limit, primary analysis recorded |
| Requirements trace forward to components/tests | PASS | Traceability table |
| User-requested approval before Stage 06 | **PASS** | Sponsor explicitly approved Stage 05 and its outputs on 2026-08-11 |

**Gate result: PASSED AND APPROVED.** All proposed components meet the Stage 05 specification gate. The sponsor explicitly approved Stage 05 and its outputs on 2026-08-11, authorizing Stage 06 to begin.

## Downstream consequences

- Stage 06 must define exact data contracts/lifecycle/ownership while preserving `C05-06/07/13/14/15` boundaries.
- Stage 07 must choose external API shapes, adapter placement, idempotency/error/polling/webhook contracts without changing component authority.
- Stage 08 must define the job state machine, leases, retries, timeouts, cancellation, partial results, worker pools, scheduler, and `C05-22` admission criteria.
- Stage 09 must decide whether `C05-21` is required and whether any `X05-02` broker trigger is met; internal events remain distinct from outward notification.
- Stage 10 must detail `C05-16` and capability lifecycle without a generic mutable model handler or Synapse inference.
- Stages 12–14 must resolve security/audit/telemetry failure policies and measurable targets.
- Stage 15 selects physical placement/products only from environment evidence; logical components do not imply separate deployments.
- Stage 17 measures whether load balancing, caching, broker, registry products, or role extraction triggers exist.
- Stage 22 must expand these three high-level flows into runtime placement/concurrency/critical-path analysis.
- The unavailable Stage 05 data/ML specialist review can be revisited during the Stage 06 authorized data/ML review or on explicit request.

## Exact next-stage inputs

Approved inputs for Stage 06:

1. Approved `outputs/stages/02-system-definition.md`
2. Approved `outputs/stages/03-capability-inventory.md`
3. Approved `outputs/stages/04-architecture-style.md`
4. Approved `outputs/stages/05-end-to-end-architecture.md`
5. Accepted `decisions/ADR-000-temporary-source-evidence-disposition.md` through `ADR-003-architecture-style.md`
6. `sources/normalized/ark-assumptions.md`
7. All seven service cards, preserving ADR-000/002 evidence restrictions
8. `stages/06-data-architecture.md`, `templates/stage-output.md`, and exact governing prompt section **5. Data architecture**

Stage 05 approval is recorded; Stage 06 may consume this artifact.
