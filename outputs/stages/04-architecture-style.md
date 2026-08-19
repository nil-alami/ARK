# Stage 04 — Architecture drivers and style

Status: `APPROVED`

## Purpose and scope

Evaluate the architecture styles named by the governing prompt against ARK's approved requirements, current maturity, organizational uncertainty, capability boundaries, and known scale evidence; recommend one starting style; define boundary, coupling, isolation, sharing, and extraction principles; and record the material decision in an ADR.

This stage selects logical architecture style and starting release mechanics only. It does not design the end-to-end component topology, choose infrastructure products/vendors, allocate runtime placement, set numeric operating targets, or declare production fitness.

The sponsor approved this artifact, `decisions/ADR-003-architecture-style.md`, the evidence-based service-extraction gate, the starting style and boundary principles, and `A-04-OWNERSHIP` on 2026-08-11.

## Inputs read in full

- `AGENTS.md` — all sections
- `WORKFLOW.md` — all sections
- `STATUS.md` — all sections after recording Stage 03 approval
- `SOURCE_MANIFEST.md` — all sections
- `AGENT-ROSTER.md` — all sections
- `stages/STAGE-CONTRACT.md` — all sections
- `stages/04-architecture-style.md` — all sections
- `templates/stage-output.md` — all sections
- `templates/adr.md` — all sections
- `sources/normalized/system-design-prompt.md` — **3. Architecture drivers and style** exactly
- `sources/normalized/ark-assumptions.md` — all sections
- `outputs/stages/02-system-definition.md` — all sections
- `outputs/stages/03-capability-inventory.md` — all sections
- `decisions/ADR-000-temporary-source-evidence-disposition.md` — all sections
- `decisions/ADR-001-stage-01-requirements-baseline.md` — all sections
- `decisions/ADR-002-stage-03-capability-evidence-disposition.md` — all sections

The Stage 04-authorized `platform_architect` performed an independent bounded, read-only fit analysis covering all named styles, drivers, boundaries, extraction triggers, anti-overengineering risks, and gate gaps. It reported no evidence-based reason to supersede the declared modular-monolith baseline. The primary agent reconciled its findings against source precedence and is the sole writer.

## Source-instruction coverage

| Source requirement | Addressed in | Status/evidence |
|---|---|---|
| Evaluate modular monolith | Style comparison; R-04-01 | Addressed; selected as top-level starting style |
| Evaluate microservices | Style comparison | Addressed; deferred pending measured extraction need and owner |
| Evaluate service-oriented architecture | Style comparison | Addressed; contract discipline retained, distributed SOA/ESB rejected now |
| Evaluate event-driven architecture | Style comparison; R-04-04 | Addressed; conditional coordination/reliable-publication pattern only |
| Evaluate data-pipeline architecture | Style comparison; R-04-03 | Addressed; required workload pattern, not whole-system style |
| Evaluate agentic architecture | Style comparison; R-04-05 | Addressed; no current fit/evidence |
| Evaluate a justified combination | Style comparison; recommendation | Addressed narrowly: modular monolith plus durable-job/data-pipeline patterns; conditional events |
| Recommend one starting architecture | Starting-style recommendation; ADR-003 | Addressed; approval required |
| Explain fit to scale, team, and maturity | Driver analysis; fit qualifications | Addressed without inventing scale or staffing |
| Define module and ownership boundaries | Logical boundary map | Addressed; named people remain TBD under accepted A-04-OWNERSHIP |
| Define acceptable coupling | Boundary principles | Addressed |
| Define mandatory isolation | Boundary principles | Addressed |
| Define what is shared and forbidden | Boundary principles | Addressed |
| Define extraction triggers | Service-extraction gate | Addressed with measurable evidence categories and prerequisites |
| Do not select microservices merely because ML capabilities are plural | Style comparison; anti-overengineering | Satisfied |
| Obtain independent platform fit analysis | Inputs/read-in-full note and completion gate | Satisfied |
| Create architecture-style ADR | `decisions/ADR-003-architecture-style.md` | Proposed; next unused ID used because ADR-001 is already accepted |

## Facts

### Architecture drivers

| ID | Driver/classification | Architectural effect | Evidence |
|---|---|---|---|
| `DRV-04-01` | ARK is a multi-tenant capability platform with independently consumable, versioned, observable, and metered capabilities — approved baseline | Requires stable logical contracts and tenant isolation, not necessarily independent deployment | `ark-assumptions.md — Product and architecture`; `Stage 02 — Business goals` |
| `DRV-04-02` | One repository, coordinated releases, initially one PostgreSQL cluster, with optional API/scheduler/worker roles — approved baseline | Strongly favors a microservice-ready modular monolith with optional runtime-role isolation | `ark-assumptions.md — Product and architecture`; `Stage 02 — ARK-CON-001` |
| `DRV-04-03` | Each capability owns logic, configuration, contracts, state, migrations, model lifecycle, tests, monitoring, and runbook — mandatory constraint | Requires hard module boundaries, public ports, owned schemas/migrations, and one writer | `ark-assumptions.md — Product and architecture`; `Stage 02 — ARK-CON-002`; `Stage 03 — Shared platform versus capability responsibility` |
| `DRV-04-04` | Control plane and execution/data plane remain distinct — mandatory logical boundary | Requires dependency, authority, and failure separation; does not by itself require separate services | `ark-assumptions.md — Product and architecture`; `Stage 02 — System boundary` |
| `DRV-04-05` | Ingestion, training, backfills, schedules, and large/retryable work use durable async jobs; PostgreSQL starts as durable job truth — approved execution constraint | Requires durable-job and pipeline patterns; does not justify a broker/workflow product now | `ark-assumptions.md — Ingestion and the ARK data lake`; `— Execution, orchestration, and proactive operation`; `Stage 02 — ARK-FR-007, ARK-CON-005` |
| `DRV-04-06` | Capability cores are consumer-neutral and contracts are bounded/versioned — mandatory integration constraint | Requires contract-oriented modules and adapters outside cores; distributed SOA is not implied | `ark-assumptions.md — Integration and contracts`; `Stage 02 — ARK-NFR-003, ARK-CON-003` |
| `DRV-04-07` | Tenant, lineage, artifact, audit, usage, and telemetry isolation applies to every state class — mandatory security/reliability driver | Isolation rules must hold across in-process and runtime boundaries | `ark-assumptions.md — Security, ownership, and operations`; `Stage 02 — ARK-NFR-001, ARK-NFR-002, ARK-NFR-006` |
| `DRV-04-08` | Four detailed capabilities are defective prototypes and Synapse is interface-only/non-production-eligible — approved evidence disposition | Favors incremental contract/state remediation rather than a distributed rewrite; prohibits agent inference | `Stage 03 — Contradictions and dangerous assumptions`; `ADR-002 — Decision` |
| `DRV-04-09` | Scale, traffic, latency, capacity, SLO, availability, recovery, environment, budget, and staffing are unknown — unresolved/temporary | Prohibits claims that a distributed style is required or that the selected style is proven at production scale | `Stage 02 — A-01-SCALE, A-01-OPS, A-01-TEAM`; `— ARK-NFR-007, ARK-CON-007`; `STATUS.md — Known blockers` |
| `DRV-04-10` | Multiple capability modules exist but independent teams/releases and accountable owners are not established — unresolved | Logical independence is required; independent operation is not currently justified | `Stage 01 — TEAM-01, TEAM-04`; `Stage 03 — A-03-OWNERSHIP` |

### Fit qualifications

- **Scale:** the recommendation optimizes for reversible change under unknown scale; it is not a capacity or SLO claim.
- **Team:** the recommendation avoids operations that require multiple independently staffed service teams. It does not claim a specific team size or skill level.
- **Maturity:** capability contracts and state boundaries are still being repaired. Adding network/distributed-data failure modes before those seams stabilize would increase migration risk.
- **Compliance/deployment:** no authoritative duty or environment currently requires separate network, key, region, database, or deployment boundaries.
- **Change:** the baseline allows role separation and later extraction, so evidence can be gathered before irreversible distribution.

No evidence supersedes the declared modular-monolith baseline.

## Assumptions

| ID | Assumption | Why needed | Architectural effect | Risk | Validation/expiry |
|---|---|---|---|---|---|
| `A-04-OWNERSHIP` (accepted) | Logical platform, data, integration, security/control, operations, and per-capability owner roles are sufficient for architecture design; named accountable people remain TBD; production promotion and service extraction are prohibited until the relevant named owner and runbook/on-call authority are assigned | `A-03-OWNERSHIP` expires before Stage 04 approval, while no roster has been supplied | Lets the logical responsibility map be approved without inventing teams or leaving state unowned | Actual organization may require different grouping; operating feasibility remains unknown | Authoritative assignments, or before Stage 20 approval, any service extraction, or any production-readiness decision—whichever is earlier |

`TEAM-04` is not extended as an assumption. Accepted ADR-003 resolves it by selecting one repository, coordinated releases, module ownership, contract tests, owned migrations, and runbooks as the starting mechanics. All other active assumptions retain their existing scope and expiry.

## Analysis and recommendations

### Architecture-style comparison

| Style | Current fit | Appropriate participation now | Why not the starting alternative | Burden/trade-off | Reconsideration |
|---|---|---|---|---|---|
| Modular monolith | **High** | Top-level style: one repository/release, explicit modules, owned schemas; optional runtime roles | Selected | Demands dependency rules, contract tests, one-writer enforcement, owned migrations; releases are coordinated | Service-extraction gate |
| Microservices | **Low/deferred** | Design extraction seams; deploy none merely because there are seven capabilities | No measured scale/hardware/deployment/ownership/reliability/compliance driver | Network failure, API compatibility, distributed consistency/tracing/security/deployment/on-call burden | One module meets a measured extraction trigger and has an owner |
| Service-oriented architecture | **Partial boundary discipline** | Versioned public interfaces, common envelope, consumer-neutral contracts | A distributed service estate/ESB is unsupported | Central integration/service governance can become new coupling and duplicates distributed burden | Authoritative distributed-service/governance constraint |
| Event-driven architecture | **Conditional pattern** | Internal coordination/reliable publication where later justified; external notifications remain distinct | No measured need for an event backbone; PostgreSQL job truth is approved | Ordering, replay, idempotency, poison handling, schema and broker operations | PostgreSQL/direct job coordination cannot meet approved measured needs |
| Data-pipeline architecture | **High workload-pattern fit** | Ingestion, normalization, dataset publication, training, backfill, batch inference | Does not cover tenant control, synchronous APIs, grants, configuration, or queries as whole-system style | Durable stage state/lineage/retry work is required anyway | Individual stages/roles scale on measurements |
| Agentic architecture | **No fit** | None | No evidenced planning, tools, memory, autonomy, or action contract; Synapse naming proves none | Nondeterminism, authorization, safety, evaluation, and operational burden | Stage 11 receives a bounded need deterministic workflow cannot satisfy |
| Narrow combination | **High** | Modular monolith top-level; durable-job/data-pipeline patterns; conditional reliable events | Selected combination must not be read as multiple coequal distributed styles | Preserves required patterns and avoids speculative infrastructure | Each optional mechanism retains its own trigger |

### Starting-style recommendation

Start with a **microservice-ready modular monolith with explicit contract and state ownership, supported by durable-job and data-pipeline patterns**.

The monolith is a release/dependency boundary, not a shared business-data free-for-all. A same-process call must obey the same public module contract and tenant/authority checks that would be required after extraction. API, scheduler, ingestion, and resource/capability worker roles may be built from the same codebase and run separately later when lifecycle or resource isolation requires it; that remains runtime-role separation, not independent-service extraction.

### Logical module and ownership boundaries

These are logical boundaries, not deployable-component or team-count commitments.

| Logical boundary | Responsibility/authority | Owned state | Public dependency surface | Failure/isolation rule |
|---|---|---|---|---|
| Edge/API boundary | Authentication enforcement, routing, API/version/request limits, request identity; no business/scientific logic | Minimal edge configuration only | Versioned public API and authenticated tenant context | Reject invalid edge requests before business side effects |
| Tenant/control module | Tenant, subscription, entitlement, quota, configuration, proactive grants, usage authority | Control records, grants, quotas, configuration, audit decisions | Control commands/queries and platform-eligibility decision | Fail closed; unavailable authority causes no execution/action |
| Ingestion and dataset-readiness module | Register inputs; preserve raw; validate/normalize/quality/policy/freshness; publish immutable ready datasets | Ingestion runs, dataset/version metadata, readiness, lineage; raw/curated objects through storage interfaces | Push/bulk registration and dataset-reference/readiness contracts | Failed transform keeps raw evidence and publishes no ready version |
| Durable job and scheduling module | Shared state, idempotency, schedules, retry, progress, cancellation, result references, notifications | Job/schedule/retry/result-reference state | Submit/status/cancel/result contract | Scheduler creates jobs; durable state survives worker/process failure; no capability pipeline ownership |
| Capability definition/invocation boundary | Common envelope/definition schema and routing to a public capability port | Definition metadata only | Definition discovery, envelope validation, bounded invocation | Platform checks do not centralize scientific logic |
| Seven capability modules | Capability-specific logic, schema, eligibility, ML lifecycle, private state, results, tests, monitoring, runbook | Per-capability configuration, migrations, features/derived data, artifacts, evaluations, results | Public operations, scientific eligibility, bounded result | One capability cannot import/write/corrupt another; Synapse remains interface-only |
| Proactive permission/policy module | Deterministic grant, scope, policy, freshness, quota, cooldown/deduplication, no-action authority | Authoritative grants/policy decisions/deduplication/audit | Authorization decision and auditable workflow request | Missing/stale/ambiguous/failed policy causes no action; LLM verifier is advisory |
| External integration/notification boundary | Consumer translation and outward result/notification delivery; exact adapter placement deferred | Delivery/idempotency state only where ARK owns delivery | Consumer-neutral result/notification and adapter contracts | Delivery failure is separate from capability result; no consumer schema in core |
| Shared technical infrastructure | Persistence/object access, telemetry, secrets/config delivery, technical contract tooling | Technical configuration only; no shared business ownership | Narrow infrastructure interfaces | Failure is surfaced; no unrestricted access to module state |

### Boundary principles

#### Acceptable coupling

- One repository, coordinated release, and common build/contract tooling.
- In-process calls through another module's public application interface.
- Shared technical types for authenticated tenant context, opaque IDs, operational envelope, versions, standard errors/outcomes, and correlation.
- One PostgreSQL cluster/connection infrastructure with module-owned schemas, migrations, and authoritative writers.
- Shared object-storage, job-lifecycle, dataset/artifact registry, telemetry, audit, metering, secrets, and configuration-delivery interfaces.
- Separately runnable roles produced from the same codebase when later placement requires them.
- Transactions confined to orchestration plus state owned by one authoritative module; convenience does not justify cross-module writes.

#### Mandatory isolation

- Tenant scope across rows, object paths, datasets, artifacts/models, jobs, events, caches, quotas, audit, usage, and telemetry.
- Capability business logic, contracts, configuration, schema/tables, migrations, artifacts/models, evaluations, results, monitoring, and runbook.
- Control authority from execution logic.
- Dataset readiness from scientific eligibility.
- Training/evaluation/promotion/activation from inference.
- Internal coordination from external notifications.
- Authoritative permission/policy from advisory capability output.
- Consumer/platform adapters from capability cores.
- Large historical/artifact objects from operational PostgreSQL state.
- Durable job state from worker process lifetime.
- Synapse behind only its documented interface until evidence resolves internals.

#### Shared infrastructure

Share only requirement-backed platform mechanisms: repository/build/release and contract tooling; PostgreSQL cluster/pooling with owned schemas; object-storage interface; authenticated tenant-context propagation; common envelope/outcomes/schema tooling; one durable job/scheduling lifecycle; dataset/artifact registry interfaces and lineage identities; telemetry/audit/metering/cost interfaces; secrets/configuration delivery. Reliable outbox/event infrastructure is not selected here and must be justified by later reliability/integration design.

#### Forbidden sharing

- Mutable shared business/domain models or a universal customer/profile object.
- Cross-capability internal imports, table writes, migrations, private-method orchestration, or model activation.
- Unrestricted SQL joins or generic repositories that bypass owner APIs/read models.
- Generic mutable model handlers permitting nondeterministic cross-capability selection.
- Process-local scheduler/status state as durable lifecycle truth.
- Phone, body `businessId`, or caller data as tenant authority.
- Shared tenant/PII debug files or unscoped caches/artifact namespaces.
- Inference-time training/activation.
- Capability results, including verifier `accepted`, as external-action authorization.
- Consumer-specific schemas inside capability cores.
- Inferred shared Synapse provider, prompt, state, memory, tools, or agent runtime.
- Separate service databases, broker, workflow engine, service mesh, Kubernetes, agent framework, or similar product without traced evidence.

### Service-extraction gate

Extraction requires a dedicated ADR, a named accountable service owner, a stable public contract, owned data/schema/migrations, independent idempotency and tenant controls, observable workload/failure evidence, a runbook, and proof that simpler remedies were attempted. At least one of these evidence categories must be present:

| Trigger | Required evidence before extraction |
|---|---|
| Scaling | Repeated breach of an approved target that profiling, optimization, vertical scaling, batching, worker-pool isolation, or a separate runtime role cannot contain |
| Hardware/runtime | Incompatible dependency, accelerator, runtime, or security control materially constrains or destabilizes the shared runtime |
| Deployment cadence | Measured coordinated-release delay or incident exposure prevents an accountable owner from meeting an approved change/recovery objective |
| Ownership | Named staffed team accepts independent contract/state/deployment/on-call/runbook responsibility and shared ownership is a documented bottleneck |
| Reliability/blast radius | Module failures breach other modules' approved targets after in-process and runtime-role isolation are tried |
| Security/compliance/residency | Authoritative duty requires independent data/key/network/region/audit boundary that logical/schema isolation cannot meet |
| Coordination capacity | PostgreSQL-backed job coordination/shared deployment misses approved throughput/backpressure targets after indexing, batching, and worker isolation |
| Independent evolution | Recurrent incompatible dependencies/releases cannot be contained through packaging and compatibility contracts |

Capability count, code size, anticipated growth, developer preference, or fashion are not extraction triggers.

### R-04-01 — Select the boundary-enforced modular monolith

- **Requirement satisfied:** `ARK-CON-001`, `ARK-CON-002`, `ARK-CON-007`; prompt requirement to recommend one starting architecture.
- **Where/when used:** Stage 04 ADR; governing baseline for Stages 05–10, 12–15, 20, and 22.
- **Why needed now:** later stages need a stable dependency/release frame without inventing distributed topology.
- **Simplest viable implementation:** one repository/release; public module ports; owned schemas/migrations; one writer; dependency/contract tests; optional same-codebase runtime roles.
- **Alternative considered:** service per capability.
- **Why not preferred:** no measured scale/hardware/deployment/ownership/reliability/compliance driver and no independent staffing evidence.
- **Trade-offs/operational burden:** simpler operations and migration; requires strong boundary governance and coordinated releases.
- **Reconsideration trigger:** a module passes the service-extraction gate.

### R-04-02 — Enforce ownership with code, contract, and storage controls

- **Requirement satisfied:** `ARK-NFR-001`–`004`, `ARK-CON-002`, `SC-02-06`, `SC-02-09`.
- **Where/when used:** Stages 05–07, 10, 12, 16, and implementation governance.
- **Why needed now:** current prototypes cross-write and share platform/database internals; a monolith without enforced ownership would preserve the primary defect.
- **Simplest viable implementation:** explicit dependency direction; module APIs; owned schemas/migrations; one-writer checks; approved read models; tenant-context tests.
- **Alternative considered:** shared domain/data layer for implementation convenience.
- **Why not preferred:** it destroys authoritative ownership, isolation, reproducibility, and credible extraction seams.
- **Trade-offs/operational burden:** duplicates some translation and demands contract/migration discipline; prevents hidden coupling.
- **Reconsideration trigger:** an explicitly cross-cutting platform domain is proven to have one authority and no capability semantics, then approved by ADR.

### R-04-03 — Use one durable lifecycle and pipeline pattern for asynchronous work

- **Requirement satisfied:** `ARK-FR-002`, `ARK-FR-003`, `ARK-FR-007`, `ARK-FR-008`, `ARK-NFR-004`, `ARK-CON-004`, `ARK-CON-005`.
- **Where/when used:** Stages 05, 06, 08, 10, 13, and 22.
- **Why needed now:** ingestion, training, schedules, backfills, and batch inference cannot rely on request/process lifetime.
- **Simplest viable implementation:** PostgreSQL-backed shared jobs with idempotent same-codebase workers and object references; private capability pipelines behind public job handlers.
- **Alternative considered:** per-capability lifecycle or a broker/workflow product now.
- **Why not preferred:** duplicates durable state or adds unsupported infrastructure/operations before measured need.
- **Trade-offs/operational burden:** shared job module becomes critical and needs state/recovery discipline; avoids multiple lifecycle implementations.
- **Reconsideration trigger:** measured PostgreSQL coordination/workflow complexity cannot meet approved needs after simpler remedies.

### R-04-04 — Keep events conditional and separate from external notifications

- **Requirement satisfied:** `ARK-FR-011`, `ARK-NFR-004`, `ARK-CON-005`, `ARK-CON-007`.
- **Where/when used:** Stages 07, 09, 13, and 22.
- **Why needed now:** later stages need a rule that prevents both synchronous overcoupling and speculative event infrastructure.
- **Simplest viable implementation:** direct public module calls and durable jobs initially; define internal event versus external notification contracts; add reliable publication only at a proven boundary.
- **Alternative considered:** event-driven platform and broker from the start.
- **Why not preferred:** throughput/decoupling needs are unmeasured and ordering/replay/schema/poison operations add burden.
- **Trade-offs/operational burden:** some initial coordination remains direct/coordinated; events can be introduced deliberately when their semantics are known.
- **Reconsideration trigger:** a measured fan-out, reliability, latency, or integration boundary cannot be met by direct/job coordination.

### R-04-05 — Exclude agentic architecture

- **Requirement satisfied:** `ARK-CON-007`, `ARK-FR-010`, `A-03-SYNAPSE`; prompt requires agentic-style evaluation.
- **Where/when used:** Stage 11 gate and Synapse-related Stages 05, 07, 10, and 12.
- **Why needed now:** names containing “Agent” could otherwise smuggle autonomy or agent infrastructure into the design.
- **Simplest viable implementation:** treat Synapse as bounded synchronous interface adapters and deterministic governed workflows.
- **Alternative considered:** agent framework, memory, tools, planning, or autonomous action.
- **Why not preferred:** none is evidenced; each adds safety, authorization, evaluation, nondeterminism, and operations problems.
- **Trade-offs/operational burden:** possible future agent use is deferred; current contracts remain testable and fail-closed.
- **Reconsideration trigger:** Stage 11 receives authoritative evidence of a bounded autonomous need that deterministic workflow cannot satisfy.

### R-04-06 — Make extraction an evidence gate, not an aspiration

- **Requirement satisfied:** source extraction rule, `ARK-CON-001`, `ARK-CON-007`, `ARK-NFR-007`.
- **Where/when used:** every later component/placement decision, especially Stages 15, 17, 20, 22, and 23.
- **Why needed now:** “microservice-ready” is otherwise easily misread as a promise to distribute later regardless of evidence.
- **Simplest viable implementation:** require the prerequisites, a qualifying measured trigger, proof of attempted simpler remedies, and a dedicated ADR.
- **Alternative considered:** roadmap-based extraction by capability count or anticipated growth.
- **Why not preferred:** it invents scale/organization and creates irreversible operating burden.
- **Trade-offs/operational burden:** extraction may occur later than some teams prefer; every extraction has a defensible owner, contract, and benefit.
- **Reconsideration trigger:** any tabled extraction category is evidenced.

## Decisions

- Accepted `ADR-003` selects the starting style, boundary principles, release mechanics, and service-extraction gate.
- Accepted `A-04-OWNERSHIP` replaces expired `A-03-OWNERSHIP` for architecture work while continuing to block production/extraction without named authorities.
- Accepted `ADR-000`, `ADR-001`, and `ADR-002` remain binding.
- `TEAM-04` is resolved by the proposed one-repository/coordinated-release decision; team size, named roster, on-call capacity, budget, deadline, and production operating fitness remain unresolved.
- No end-to-end topology, deployable service count, vendor, cloud, gateway product, broker, workflow engine, database product change, service mesh, Kubernetes platform, agent framework, capacity, SLO, or cost decision is made.

## Contradictions and dangerous assumptions

| ID | Evidence/tension | Treatment | Consequence |
|---|---|---|---|
| `C-04-01` | “Microservice-ready” can be misread as a future service-per-capability commitment | Extraction requires measured evidence, prerequisites, owner, and ADR | Module seams are mandatory; service extraction is not |
| `C-04-02` | A monolith can become a shared-data monolith, contrary to capability ownership | Owned schemas/migrations/writers, public ports, and dependency tests are mandatory | Boundary enforcement is part of the style, not optional hygiene |
| `C-04-03` | One PostgreSQL cluster is shared, but state/business ownership is not | Share infrastructure only; prohibit cross-writes and unrestricted access | Later data design must preserve schema/authority isolation |
| `C-04-04` | API/scheduler/workers may run separately, but Stage 04 cannot choose runtime topology | Treat roles as permitted packaging seams, not selected deployments | Stages 05/08/15/22 decide placement from requirements/measurements |
| `C-04-05` | Durable pipeline/event patterns might be presented as coequal architectures | Data pipelines are workload patterns; events are conditional | One top-level style remains modular monolith |
| `C-04-06` | Synapse “Agent” names suggest agentic style | ADR-000/002 restrict evidence to interface facts and prohibit agent inference | Stage 11 must find new authoritative evidence or record no agent architecture |
| `C-04-07` | Team/scale fit is requested but actual team and scale are unknown | Fit is to uncertainty, reversibility, and authorized constraints—not an empirical capacity claim | Production fitness and independent-service viability remain unresolved |
| `C-04-08` | `A-03-OWNERSHIP` expired before Stage 04 approval | Accepted `A-04-OWNERSHIP` explicitly replaces it with a tighter production/extraction block | Named owner assignments still expire later |
| `C-04-09` | Stage routing requests `ADR-001-architecture-style.md`, but accepted ADR-001 already exists | Preserve accepted ADR; use next unused `ADR-003`; record collision | No duplicate/overwritten decision history |

## Open questions

| ID | Question | Blocking? | Options | Recommended temporary assumption | Effect |
|---|---:|---|---|---|---|
| `Q-04-01` | Who are the named product/data/platform/security/integration/operations and per-capability owners, including on-call/runbook authorities? | Yes for production/extraction; approval needed now for design deferral | Supply assignments; approve logical roles temporarily; stop | Approve `A-04-OWNERSHIP` | Allows logical style work; keeps production/extraction blocked; expires by Stage 20/production/extraction |
| `Q-04-02` | What measured workload, latency, concurrency, backlog, hardware, SLO, availability, and recovery evidence exists? | No for reversible style; yes for extraction/production | Supply targets/measurements; retain unknowns | Keep `A-01-SCALE`/`A-01-OPS` scope; make no capacity claim | Stage 15/17/22 remain conditional |
| `Q-04-03` | What deployment environment, region/network/key/residency constraints are authoritative? | No for logical style; may block Stage 15 | Supply environment; portable role model; mandated topology | Keep topology open | No physical boundary is selected |
| `Q-04-04` | Does any capability require independent release or a dedicated incompatible runtime now? | No evidence; yes before extraction | Supply evidence; coordinated release; selective runtime roles | Approve ADR-003 coordinated release and extraction gate | Resolves TEAM-04 without promising services |
| `Q-04-05` | Where do consumer adapters live operationally? | No for style; Stage 07 decision | Consumer-owned; ARK integration boundary; mixed | Keep capability cores neutral and placement provisional | Does not change the selected style |
| `Q-04-06` | Which capabilities/use cases are release-scoped first? | No for style; blocks roadmap/acceptance planning | One slice; subset; phases | Keep all seven product-scoped, no simultaneous delivery claim | No service count or runtime commitment follows |

## Requirements-traceability updates

| Requirement/criterion | Stage 04 architecture response | Validation/evidence |
|---|---|---|
| `ARK-FR-001` | Tenant/control module is logically separate from ingestion and execution | Module API and no-side-effect authorization tests |
| `ARK-FR-002/003` | Ingestion/readiness boundary uses durable pipeline patterns and object references | Stage 06 contract/lineage/failure tests |
| `ARK-FR-004/005` | Public module ports, definitions, and common envelope are architecture seams | Contract/schema/dependency tests |
| `ARK-FR-006` | Dataset readiness, platform eligibility, and scientific eligibility are isolated responsibilities | Scenario/dependency tests |
| `ARK-FR-007/008` | One durable job module; same-codebase worker roles permitted; sync only after classification | State/restart/operation-classification tests |
| `ARK-FR-009` | Training/promotion is isolated from inference inside each capability | Negative side-effect/dependency tests |
| `ARK-FR-010` | Proactive permission/policy is separate from advisory capability output | No-action authorization suite |
| `ARK-FR-011` | Internal coordination and external notification remain distinct contracts; event infrastructure conditional | Contract/idempotency tests |
| `ARK-FR-012` | Boundary and extraction rules produce evidence LAB can inspect | Architecture/module/isolation evidence bundle |
| `ARK-NFR-001` | Tenant scope is mandatory across every module/shared mechanism | Cross-tenant negative suite |
| `ARK-NFR-002/003` | Contract-oriented modules, independent version references, and owned state preserve reproducibility | Lineage and schema/version checks |
| `ARK-NFR-004` | Durable jobs and any later events assume at-least-once/idempotent effects | Duplicate/restart tests |
| `ARK-NFR-005/006` | Opaque IDs and shared privacy-safe audit/telemetry interfaces | Schema/privacy/trace completeness tests |
| `ARK-NFR-007` | No extraction or production claim without approved measured targets | Target register plus extraction ADR evidence |
| `ARK-CON-001` | Selected boundary-enforced modular monolith with measured extraction gate | Accepted ADR-003 |
| `ARK-CON-002` | Module-owned business logic/state/migrations/model lifecycle; no cross-import/write | Dependency, schema, migration, one-writer checks |
| `ARK-CON-003` | Adapter/consumer translation excluded from capability cores | Boundary tests; placement deferred to Stage 07 |
| `ARK-CON-004/005` | Shared object/data-lake interface and PostgreSQL operational/job truth retained | Later storage/job recovery tests |
| `ARK-CON-006` | No new identity ownership; opaque source identifiers enter through data boundary | Contract/negative tests |
| `ARK-CON-007` | Microservices/broker/agent/vendor/topology require later traced evidence | ADR-003 extraction/optional-mechanism gates |
| `SC-02-06/09` | Mandatory tenant and module ownership isolation | Static/runtime negative suite |
| `A-03-ML-MIGRATION` | Prototype cross-writes/lifecycle defects cannot shape module ownership | Migration work retained for Stages 10/16 |
| `A-03-SYNAPSE` | Synapse remains interface-bound and non-agentic | No hidden dependency/state claim |

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Every architecture style in the governing section evaluated | PASS | Comparative matrix covers modular monolith, microservices, SOA, event-driven, data-pipeline, agentic, and narrow combination |
| One starting architecture recommended | PASS | Approved boundary-enforced microservice-ready modular monolith plus durable-job/data-pipeline patterns |
| Scale, team, and maturity fit explained without invented facts | PASS | Driver and fit-qualification sections |
| Module and ownership boundaries defined | PASS | Logical boundary map and accepted `A-04-OWNERSHIP` |
| Acceptable coupling and mandatory isolation defined | PASS | Boundary principles |
| Shared and forbidden state/infrastructure defined | PASS | Boundary principles |
| Service-extraction triggers are measurable and anti-overengineering-safe | PASS | Extraction gate and non-triggers |
| Declared baseline evaluated for supersession | PASS | No evidence-based supersession reason found |
| Independent platform-architect fit analysis reconciled | PASS | Reviewer agreed with selected style and identified ownership/ADR-number gate risks |
| Material decision recorded without overwriting an accepted ADR | PASS | Proposed `ADR-003`; routing collision documented |
| Explicit user approval of style/boundaries/replacement ownership disposition | PASS | User approval dated 2026-08-11 |

**Gate result: PASSED BY EXPLICIT APPROVAL.** On 2026-08-11 the sponsor approved Stage 04 and its outputs, the evidence-based service-extraction gate, the starting architecture style and boundary principles, and `A-04-OWNERSHIP`.

## Downstream consequences

- Stage 05 must assemble the end-to-end logical architecture inside these module boundaries without turning every boundary into a service.
- Stages 06–10 must use module-owned state and public contracts; data pipelines/jobs are patterns within the selected style.
- Stage 07 decides adapter placement but cannot put consumer schemas in capability cores.
- Stage 08 defines runtime-role/job execution without assuming broker/workflow/service topology.
- Stage 09 may justify outbox/events at concrete coordination/notification boundaries but cannot adopt an event backbone by default.
- Stage 10 preserves per-capability model lifecycle and the shared registry/job interfaces without a generic cross-capability mutable model handler.
- Stage 11 must record no agent architecture unless new bounded authoritative evidence passes its justification gate.
- Stages 12–14 must make tenant, authority, failure, telemetry, and evaluation isolation enforceable across in-process and runtime calls.
- Stages 15, 17, and 22 must use measurements/constraints to place roles and may propose extraction only through ADR-003's gate.
- Stage 20 cannot approve operating ownership or extraction sequencing until `A-04-OWNERSHIP` is replaced by named assignments.
- Stage 23 must challenge any distributed component that lacks a direct requirement and trigger.

## Exact next-stage inputs

After explicit Stage 04 approval:

1. `outputs/stages/00-source-audit.md`
2. `outputs/stages/01-discovery-and-questions.md`
3. `outputs/stages/02-system-definition.md`
4. `outputs/stages/03-capability-inventory.md`
5. Approved `outputs/stages/04-architecture-style.md`
6. Accepted `decisions/ADR-000-temporary-source-evidence-disposition.md`
7. Accepted `decisions/ADR-001-stage-01-requirements-baseline.md`
8. Accepted `decisions/ADR-002-stage-03-capability-evidence-disposition.md`
9. Accepted `decisions/ADR-003-architecture-style.md`, including active `A-04-OWNERSHIP`
10. `sources/normalized/ark-assumptions.md`
11. `stages/05-end-to-end-architecture.md` and its exact governing prompt section/templates

Do not read or execute Stage 05 until Stage 04 receives explicit approval.
