# ADR-003 — Starting architecture style and boundary principles

Status: `ACCEPTED`

Date: 2026-08-11

Decision owner: ARK design sponsor (user approval)

## Context and requirements

ARK must begin with one architecture style that supports a multi-tenant capability platform, seven logically independent ML/AI capabilities, durable ingestion and execution, reproducible data/model lineage, strict tenant and state isolation, and future extraction without committing to distributed operations prematurely.

The authoritative baseline declares a microservice-ready modular monolith: one repository, coordinated releases, initially one PostgreSQL cluster, and optionally distinct API, scheduler, and capability-worker runtime roles. It also requires module-owned logic, contracts, persistence, migrations, model lifecycle, tests, monitoring, and runbooks; one authoritative writer per table/state set; and extraction only for measured scaling, hardware, deployment, ownership, reliability, or compliance needs. Scale, team capacity, deployment environment, SLOs, budget, and named accountable owners remain unresolved.

Evidence: `sources/normalized/ark-assumptions.md — Product and architecture`; `— Execution, orchestration, and proactive operation`; `— Security, ownership, and operations`; `outputs/stages/02-system-definition.md — ARK-CON-001 through ARK-CON-007`; `outputs/stages/03-capability-inventory.md — Shared platform versus capability responsibility`.

## Decision

ARK will start as a **microservice-ready modular monolith with explicit contract and state ownership, supported by durable-job and data-pipeline patterns**.

1. Use one repository and coordinated releases. Define hard logical modules with public application contracts, owned state/schema/migrations, one authoritative writer, dependency rules, and contract tests.
2. Permit API, scheduler, ingestion, and resource/capability worker roles to run separately from the same codebase when lifecycle, failure, or resource isolation requires it. Runtime-role separation is not microservice extraction.
3. Use direct in-process calls through public module interfaces for short local coordination. Use the shared durable job lifecycle for scheduled, long-running, retryable, backfill, training, ingestion, and batch work.
4. Use data-pipeline structure inside ingestion and ML workflows. Do not treat the whole platform as a pipeline because control-plane, interactive, permission, and query responsibilities also exist.
5. Keep event-driven behavior conditional. Internal events and external notifications remain distinct contracts; add reliable publication/outbox or a broker only when later stages establish a concrete reliability, decoupling, throughput, or integration requirement.
6. Do not adopt service-per-capability microservices, distributed SOA/ESB infrastructure, an event backbone, or agentic architecture as the starting style.
7. Keep physical topology, cloud/platform, vendor, network, runtime packaging, and numeric capacity/SLO decisions open for their governing later stages.

The following boundary principles are mandatory:

- Capability modules own their business/ML logic, operation schemas, scientific eligibility, configuration, private persistence, migrations, artifacts, evaluations, results, monitoring rules, and runbooks.
- Shared platform modules own authenticated tenant context, subscriptions/entitlements/quotas/grants, common envelope and lifecycle, dataset/artifact registry interfaces, audit/lineage/metering, and outward-action governance.
- Consumer translation remains outside capability cores. Adapter placement remains a Stage 07 decision.
- Control authority is isolated from execution; dataset readiness from scientific eligibility; training/promotion from inference; internal coordination from external notification; authoritative permission/policy from advisory capability output.
- Tenant isolation applies regardless of whether a call is in-process or crosses a runtime boundary.

`A-04-OWNERSHIP` is accepted with this decision: logical owner roles in the Stage 04 responsibility map are sufficient for architecture design, but named accountable product, data, platform, ML/capability, security, integration, and operations owners remain `TBD`. No capability may be promoted or enabled for production, and no module may be extracted into an independently operated service, until the relevant named owner and runbook/on-call authority are assigned. This assumption replaces the expired `A-03-OWNERSHIP` treatment and expires when authoritative assignments are supplied, or before Stage 20 approval, service extraction, or any production-readiness decision—whichever occurs first.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| Boundary-enforced modular monolith with durable-job/data-pipeline patterns | Matches the declared baseline; simplest operational model; supports current migration and later extraction | Requires disciplined dependency, schema, contract, and ownership enforcement; coordinated release is a coupling point | Selected | Apply the extraction gate below |
| Service-per-capability microservices | Independent deploy/scale/failure boundaries | Distributed failure, consistency, compatibility, security, observability, deployment, and on-call burden before scale/team evidence or stable contracts | Rejected now | A specific module satisfies extraction criteria and has an accountable owner |
| Distributed service-oriented architecture / ESB | Centralized service governance and integration | Adds network/service governance and risks central business orchestration without a current need | Rejected now; contract discipline retained | Authoritative external service/governance constraint emerges |
| Event-driven platform as the primary style | Temporal decoupling and scalable fan-out | Ordering, replay, schema, poison-message, idempotency, and broker operations are unsupported by measured need | Rejected as top-level style | PostgreSQL-backed coordination cannot meet an approved measured need |
| Data-pipeline architecture for the whole system | Natural fit for ingestion, training, backfill, and batch inference | Does not cover control-plane, synchronous, permission, configuration, and query responsibilities | Retained only as an internal workload pattern | Not applicable as a whole-system replacement without a scope change |
| Agentic architecture | Could support autonomous planning/tool selection | No evidenced autonomy/tool/memory need; adds nondeterminism, authorization, safety, and evaluation burden | Rejected | Stage 11 receives a bounded evidenced need that deterministic workflow cannot satisfy |
| Undisciplined monolith with shared business state | Lowest immediate implementation friction | Violates module ownership, tenant/state isolation, reproducibility, and extraction readiness | Rejected | Never without a superseding requirement and ADR |

## Rationale

The selected style is the only option that satisfies the declared starting constraint while remaining honest about unknown scale, team, deployment, and operating targets. It preserves in-process simplicity for a system whose contracts and prototype migrations are still stabilizing, while using owned module state, narrow contracts, durable lifecycle, and dependency tests to create credible extraction seams.

Multiple ML capabilities do not by themselves justify multiple services. The immediate architectural risk is boundary erosion inside shared code and storage, not insufficient distributed infrastructure.

## Consequences and trade-offs

- ARK begins with one codebase and coordinated release, reducing deployment and distributed-systems burden.
- Logical modules and runtime roles may fail or scale differently, but independent deployment is not promised.
- The initially shared PostgreSQL cluster is logically partitioned by module-owned schemas and authoritative writers; convenience joins and cross-writes are prohibited.
- Module API/version discipline, dependency enforcement, owned migrations, contract tests, and architecture checks become mandatory engineering work.
- Some changes require coordinated release until a measured extraction is approved.
- Durable jobs and pipelines are first-class patterns without requiring a broker or workflow product.
- Later extraction remains possible but will require stable contracts, independent migrations, observability, operational ownership, and a dedicated ADR.
- Named ownership and operating fitness remain blocked under `A-04-OWNERSHIP`, `A-01-SCALE`, and `A-01-OPS`.

## Implementation constraints

### Acceptable coupling

- Same repository, coordinated release, and shared build/contract tooling.
- In-process calls through another module's public application interface.
- Shared technical value types for authenticated tenant context, IDs, operational envelope, versions, errors/outcomes, and correlation—without shared capability business rules.
- One PostgreSQL cluster and connection infrastructure with module-owned schemas, migrations, and writers.
- Shared object-storage, job-lifecycle, registry, telemetry, audit, metering, secrets, and configuration-delivery interfaces.
- Separately runnable roles built from the same source when later stage placement requires them.

### Mandatory isolation and forbidden sharing

- No capability imports another capability's internals, writes its tables, owns its migrations, or activates its models.
- No shared mutable business/domain model, universal customer/profile object, unrestricted SQL join layer, generic cross-capability model handler, process-local scheduler as durable truth, or shared tenant/PII debug files.
- No body field, phone, or consumer identifier is tenant authority; tenant comes from the authenticated principal.
- No inference-time training/activation and no capability output—including campaign-verifier `accepted`—authorizes external action.
- No consumer schema enters capability cores; no undocumented Synapse provider, state, prompt, tool, memory, or agent behavior is inferred.
- No separate service database, broker, workflow engine, service mesh, Kubernetes requirement, agent framework, or other platform product is introduced by this ADR.

### Service-extraction gate

A module may be extracted only through a dedicated ADR after a measured need persists despite simpler remedies and the module has a stable public contract, owned data/migrations, tenant controls, idempotency, observability, runbook, and named accountable owner. Qualifying evidence is one or more of:

1. Approved workload/SLO targets are repeatedly missed because demand cannot be contained by profiling, optimization, vertical scaling, worker-pool isolation, or a separate runtime role.
2. Incompatible runtime dependencies, accelerator hardware, or security controls materially constrain the shared runtime.
3. Coordinated-release delay or incident exposure measurably prevents an accountable owner from meeting an approved change/recovery objective.
4. A named staffed team accepts independent contract, state, deployment, on-call, and runbook responsibility, and shared ownership is a measured bottleneck.
5. Module failures breach other modules' approved targets after in-process and runtime-role isolation have been tried.
6. An authoritative security, compliance, residency, key, network, or audit duty requires a boundary that logical/schema isolation cannot satisfy.
7. PostgreSQL job coordination/shared deployment cannot meet approved throughput or backpressure targets after indexing, batching, and worker isolation are exhausted.
8. Recurrent incompatible dependency/release requirements cannot be contained by modular packaging and compatibility contracts.

Capability count, code size, anticipated growth, developer preference, or architectural fashion are not extraction triggers.

## Validation evidence

- User approval dated 2026-08-11 explicitly covers Stage 04 and its outputs, the evidence-based service-extraction gate, the starting architecture style and boundary principles, and `A-04-OWNERSHIP`.
- Independent read-only `platform_architect` review evaluated modular monolith, microservices, service-oriented, event-driven, data-pipeline, agentic, and combined styles and found no evidence superseding the baseline.
- `outputs/stages/04-architecture-style.md` maps every governing prompt bullet, module boundary, coupling rule, isolation rule, sharing rule, and extraction trigger.
- Required boundary tests include dependency-direction checks, module API tests, schema/migration ownership checks, one-writer checks, cross-tenant tests, and absence of private cross-capability calls/writes.
- Unknown numeric and organizational inputs remain explicit rather than being converted into claims of production fitness.

## Reconsideration trigger

Any service-extraction criterion above; authoritative team/release/deployment constraints; approved workload/SLO measurements; a compliance/residency boundary; a product-boundary change; or new evidence invalidating a module boundary.

## Supersedes / superseded by

Resolves Stage 01 `TEAM-04` by selecting one repository, coordinated releases, module ownership, contract tests, owned migrations, and runbooks as the starting mechanics. `A-04-OWNERSHIP` replaces expired `A-03-OWNERSHIP` for named-assignment uncertainty. It does not supersede ADR-000, ADR-001, or ADR-002. Not superseded.

The Stage 04 routing file requested `decisions/ADR-001-architecture-style.md`, but ADR-001 is already an accepted Stage 01 decision. Per `AGENTS.md — Output discipline`, accepted decisions are not overwritten; the next unused identifier, ADR-003, is used instead.
