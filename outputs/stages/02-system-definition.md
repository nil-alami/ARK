# Stage 02 — System definition

Status: `APPROVED`

## Purpose and scope

Define what ARK is responsible for, who consumes it, which outcomes and use cases it supports, what remains outside its boundary, and the stable functional, non-functional, and constraint requirements that later architecture must satisfy. This stage defines logical responsibilities only; it does not select an architecture style, deployment topology, product, vendor, protocol, or numeric operating target.

## Inputs read in full

- `AGENTS.md` — all sections
- `WORKFLOW.md` — all sections
- `STATUS.md` — all sections
- `SOURCE_MANIFEST.md` — all sections
- `stages/STAGE-CONTRACT.md` — all sections
- `stages/02-system-definition.md` — all sections
- `templates/stage-output.md` — all sections
- `templates/requirements-traceability.md` — all sections
- `outputs/stages/00-source-audit.md` — all sections
- `outputs/stages/01-discovery-and-questions.md` — all sections
- `decisions/ADR-000-temporary-source-evidence-disposition.md` — all sections
- `decisions/ADR-001-stage-01-requirements-baseline.md` — all sections
- `sources/normalized/system-design-prompt.md` — `1. System definition`
- `sources/normalized/ark-assumptions.md` — all sections

The Stage 02-authorized `platform_architect` completed a bounded, read-only review of the system boundary, candidate requirements, testability, gate risks, and downstream consequences. The primary agent reconciled its findings against source precedence and is the sole author of this artifact.

## Source-instruction coverage

| Governing requirement | Addressed in | Status/evidence |
|---|---|---|
| Define business goals | Business goals | Addressed |
| Define users and consuming systems | Users and consuming systems | Addressed; unresolved named owners remain explicit |
| Define system boundary | System boundary | Addressed with inside/outside responsibility table |
| Define responsibilities inside and outside ARK | System boundary | Addressed; provisional placements are labeled |
| Define core use cases | Core use cases | Addressed without committing to MVP sequence |
| Define out-of-scope capabilities | Out of scope | Addressed |
| Define success criteria | Success criteria | Addressed with testable evidence or provisional status |
| Define functional requirements | Functional requirements | Addressed with stable `ARK-FR-*` IDs |
| Define non-functional requirements | Non-functional requirements | Addressed with stable `ARK-NFR-*` IDs; unknown numeric targets remain provisional |
| Define constraints and assumptions | Constraints; Assumptions | Addressed with stable `ARK-CON-*` IDs and approved `A-01-*` references |
| Start requirements traceability | Requirements-traceability updates | Addressed using the required matrix fields |
| Do not choose an architecture style | Decisions; Constraints | Satisfied; the declared modular-monolith baseline is carried forward as source evidence for Stage 04, not re-selected here |

## Facts

### Business goals

- Provide one multi-tenant platform through which consuming systems can use independently consumable, versioned, observable, and metered AI capabilities. `sources/normalized/ark-assumptions.md — Product and architecture`.
- Help businesses understand customers, predict behavior, personalize recommendations and communications, and support policy-compliant campaigns. `outputs/stages/01-discovery-and-questions.md — Product and scope facts`.
- Replace current platform-specific coupling and prototype behavior with platform-neutral, governed contracts and reproducible execution, without accepting documented prototype defects as target semantics. `outputs/stages/01-discovery-and-questions.md — Current-state facts, not target decisions`; `— R-01-03`.
- Allow capabilities to evolve independently at the logical ownership and contract level while adding deployment independence only when later evidence justifies it. `sources/normalized/ark-assumptions.md — Product and architecture`.
- Make data, eligibility, execution, outputs, permissions, usage, and failures traceable so consumers and LAB can evaluate behavior safely. `sources/normalized/ark-assumptions.md — Integration and contracts`; `— Security, ownership, and operations`.

Business-lift measures, commercial outcomes, delivery dates, and capability order are not facts; they remain unresolved under `A-01-BUS` and `A-01-TEAM`.

### Users and consuming systems

| Actor | Relationship to ARK | Known or provisional status |
|---|---|---|
| Direct, Whatson, and POS | Consuming platforms that provide data, request capabilities, receive results, and translate platform-specific concepts | Named consumers; adapter ownership is provisional under `A-01-INT` |
| LAB | External validation consumer for contracts, isolation, reproducibility, evaluation evidence, and failure behavior | It is not an ML capability; its promotion/veto authority remains unresolved under `A-01-OPS` |
| Future external client platforms | Potential future consumers through stable platform-neutral contracts | In product context; direct public access and onboarding timing are unresolved under `A-01-BUS` |
| Business users | Indirect beneficiaries who act through consuming platforms | Direct ARK business-user UI is outside the provisional boundary under `A-01-BUS` |
| Tenant/platform administrators | Logical actors that manage subscription, entitlement, quota, configuration, and proactive grants | Required by control responsibilities; identity provider, role names, and approval hierarchy remain unresolved under `A-01-SEC` |
| Capability, platform, data, security, and operations owners | Logical operators accountable for contracts, models, data, controls, and runbooks | Responsibilities are required, but named teams and staffing remain unresolved under `A-01-TEAM` |

Evidence: `sources/normalized/system-design-prompt.md — Project information`; `sources/normalized/ark-assumptions.md — Product and architecture`; `outputs/stages/01-discovery-and-questions.md — Product and scope facts`, `— Open questions`.

### System boundary

The boundary below describes ownership of behavior and state, not deployable services.

| Inside ARK | Outside ARK |
|---|---|
| Tenant-scoped subscriptions, entitlements, quotas, configuration, proactive grants, usage records, and audit state | Automated invoicing/payment collection for the initial scope; commercial policy remains unresolved |
| Authentication enforcement at the ARK boundary and binding tenant context to an authenticated principal | Identity-provider operation, credential issuance, and consumer user-session management; concrete trust protocol remains unresolved |
| Platform-neutral versioned API, capability-definition, data, job, result, error, and notification contracts | Consumer-specific terminology, UI models, and schema/protocol translation; consumer-side adapter ownership is provisional under `A-01-INT` |
| Ingestion registration and processing; immutable raw preservation; validation, normalization, quality/policy/freshness checks; lineage; and publication of ready versioned datasets | Authoritative customer, transaction, catalog, inventory, consent, campaign, and delivery-feedback systems of record under `A-01-BUS` and `A-01-DATA` |
| ARK-owned operational metadata and service-owned derived datasets, features, results, models, and artifacts | Customer-master/CDP ownership and probabilistic cross-platform identity resolution under `A-01-BUS` and `A-01-DATA` |
| Dataset-readiness, subscription/quota/model checks, and capability-owned scientific eligibility | Supplying stable tenant-scoped opaque identifiers and authoritative domain semantics/policies |
| Capability definition and execution for Churn, RFM, NPT, REC, Synapse chatbot, Synapse message generator, and Synapse campaign verifier, subject to evidence and release scope | Acceptance of current prototype algorithms/contracts as production semantics; Stage 03 must assess each capability |
| Shared durable lifecycle for ingestion, training, backfills, scheduled work, large inference, retries, results, and notifications | Consumer process lifetime as the reliability boundary for durable work |
| Explicit eligible, degraded, fallback, ineligible, failed, and authorization outcomes | Silent invention of unavailable data or implicit training/model activation from inference |
| Validation of proactive grants, scope, freshness, quota, threshold, cooldown/deduplication, and auditable execution/notification | Customer-facing channel delivery and campaign sending under `A-01-BUS` and `A-01-INT` |
| Cross-cutting lineage, observability, security audit, metering, and cost attribution | LAB implementation and governance; ARK exposes evidence to LAB but does not own LAB |
| Explicitly admitted Synapse interface behavior | Undocumented Synapse providers, models, prompts, memory, tools, persistence, safety controls, policy authority, and failure behavior under `ADR-000` |

Evidence: `sources/normalized/ark-assumptions.md — Product and architecture`, `— Integration and contracts`, `— Ingestion and the ARK data lake`, `— Execution, orchestration, and proactive operation`, `— Security, ownership, and operations`; `decisions/ADR-000-temporary-source-evidence-disposition.md — Decision`; `decisions/ADR-001-stage-01-requirements-baseline.md — Decision`.

### Core use cases

1. Register and configure a tenant, then manage capability subscriptions, entitlements, quotas, and settings without implicitly ingesting data or executing a capability.
2. Accept small incremental/micro-batch data through push contracts and large or historical data by registered object reference.
3. Preserve source input, validate and normalize it, assess quality/policy/freshness, and publish a traceable immutable dataset version or an explicit not-ready outcome.
4. Discover a release-scoped capability's machine-readable operations, inputs, outputs, dependencies, execution modes, thresholds, and fallbacks.
5. Invoke a short, predictable capability operation synchronously using a common operational envelope and a capability-specific payload.
6. Submit, observe, cancel where supported, and retrieve results for ingestion, training, backfill, scheduled, batch-inference, and retryable work through a durable job lifecycle.
7. Evaluate dataset readiness, platform eligibility, and capability scientific eligibility independently, returning explicit eligible, degraded, fallback, or ineligible outcomes.
8. Retrieve small results inline or large results by reference with the versions and lineage needed for reproduction.
9. Train or retrain a model only through an explicitly authorized lifecycle operation and retain evaluation/promotion evidence; this treatment is provisional under `A-01-ML`.
10. Under an active scoped grant, evaluate a condition, validate policy/permission/quota/freshness/deduplication, create auditable work, and notify the consuming platform.
11. When authorization is absent, expired, ambiguous, or insufficient, report the insight without external action.
12. Let LAB validate release-scoped contracts, tenant isolation, reproducibility, capability evaluation evidence, and failure behavior; precise LAB acceptance authority remains provisional.
13. Audit and meter each tenant-scoped request, ingestion run, job, output, grant decision, and outward notification.

These are product-scope use cases, not a commitment to deliver all seven capabilities or all use cases in the same MVP release. Evidence: `outputs/stages/01-discovery-and-questions.md — B-01`; `decisions/ADR-001-stage-01-requirements-baseline.md — Decision`.

### Out of scope

- Acting as the customer master, CDP, probabilistic identity-resolution system, presentation application, or customer-facing campaign/channel sender under the active `A-01-BUS`, `A-01-DATA`, and `A-01-INT` assumptions.
- A direct ARK business-user UI and consumer-owned workflow UX.
- Automated billing/invoicing and payment collection in the provisional initial scope; entitlements, quotas, metering, and usage records remain inside.
- A simultaneous first release of all seven named capabilities or a dated MVP sequence; B-01 and TEAM-02 remain unresolved.
- Accepting current prototype coupling, schedulers, endpoints, model behaviors, or known defects as the target contract.
- Capability-internal ML redesign, model choice, numeric quality thresholds, or production-readiness approval; these begin in Stage 03 and later ML stages.
- Autonomous planning, dynamic tool selection, persistent agent memory, or agent frameworks without later evidence and Stage 11 justification.
- Direct shared-database product integration and new cross-module writes.
- Default real-time streaming, service-per-capability deployment, Kubernetes, a broker, a workflow product, service mesh, feature store, vector database, MCP/A2A, or any vendor selection without a later traced requirement.
- Numeric latency, throughput, capacity, availability, RPO, RTO, retention, cost, or business-lift commitments while those inputs remain unknown.
- Any claim about undocumented Synapse internals or production safety.

### Success criteria

| ID | Success criterion | Acceptance evidence | Status |
|---|---|---|---|
| SC-02-01 | Enabling a capability does not itself ingest data or execute it | Contract test separates subscription, ingestion, and execution | Testable |
| SC-02-02 | A successful ingestion can be traced from raw input through validation to one immutable ready dataset version; a failed transformation retains raw evidence and publishes no ready version | Ingestion acceptance and lineage tests | Testable |
| SC-02-03 | Every release-scoped capability exposes a valid machine-readable definition and accepts the shared operational envelope without consumer-specific core terminology | Definition-schema and consumer contract tests | Testable |
| SC-02-04 | Readiness, platform eligibility, and scientific eligibility failures are distinguishable and never fabricate missing data | Scenario tests for each layer and outcome class | Testable |
| SC-02-05 | Durable work has observable lifecycle state across process interruption, retry, duplicate delivery, cancellation where supported, and result retrieval | Job state-machine and restart/recovery tests | Testable |
| SC-02-06 | A principal for one tenant cannot access or influence another tenant's rows, objects, datasets, models, jobs, events, caches, quotas, audit, or telemetry | Cross-tenant negative suite | Testable |
| SC-02-07 | An output resolves to tenant, source contract, dataset, feature schema, model, code, and execution versions | End-to-end lineage query | Testable |
| SC-02-08 | Missing, expired, revoked, out-of-scope, stale, duplicate, or quota-exceeded proactive authorization produces no external action | Proactive authorization negative suite | Testable under active `A-01-SEC`/`A-01-INT` |
| SC-02-09 | Capability cores remain platform-neutral and no module writes another capability's state | Dependency, schema-ownership, and contract tests | Testable |
| SC-02-10 | LAB can execute a technical validation suite covering contracts, isolation, reproducibility, evaluation evidence, and failure behavior | LAB-facing acceptance suite | Provisional under `A-01-OPS`; promotion authority and numeric gates TBD |
| SC-02-11 | Business outcome and model-quality acceptance targets are defined before production acceptance | Sponsor/LAB-approved KPI and evaluation record | Provisional under `A-01-BUS` and `A-01-ML`; no numeric target approved |
| SC-02-12 | Performance, freshness, capacity, availability, recovery, retention, and cost targets are defined and measured before an irreversible production commitment | Approved target register plus measured evidence | Provisional under `A-01-SCALE`, `A-01-DATA`, and `A-01-OPS` |

## Assumptions

All assumptions below were approved in `decisions/ADR-001-stage-01-requirements-baseline.md — Decision`. Stage 02 narrows none of them and does not extend their expiry.

| ID | Assumption used in this stage | Architectural effect | Risk | Validation/expiry |
|---|---|---|---|---|
| A-01-BUS | ARK is an AI capability platform behind consumers, not the customer master/CDP, campaign sender, or direct business-user UI; all seven capabilities remain product scope but MVP order is unresolved | Defines the provisional product boundary and out-of-scope list | A desired product surface or release scope may be omitted | B-01 through B-05 |
| A-01-DATA | Source platforms remain systems of record, supply stable tenant-scoped opaque IDs, and ARK does not probabilistically merge identities | Defines data ownership and identity boundary | Upstreams may not provide adequate identifiers or policy semantics | D-01 through D-05 |
| A-01-ML | Prototype behavior is migration evidence; training is separate from inference; unavailable evidence yields explicit non-success outcomes; Synapse remains non-agentic and interface-only | Keeps capability responsibilities testable without accepting undocumented or defective behavior | Stage 03 may be unable to complete some capability contracts | ML-01 through ML-06 and the Stage 03 gate |
| A-01-INT | Consumer-specific adapters remain outside ARK; authenticated service identity supplies tenant context; long work uses durable semantics; no outward action occurs without grant/workflow | Defines provisional adapter and external-action boundaries | Consumer ownership or delivery needs may differ | INT-01 through INT-05 |
| A-01-SCALE | Numeric scale, latency, availability, recovery, and cost targets remain unknown and must be measured before irreversible commitments | Makes `ARK-NFR-007` and success criteria SC-02-12 provisional | Production fitness cannot yet be demonstrated | Measured answers to S-01 through S-04 |
| A-01-SEC | Least privilege, authenticated tenant binding, minimal PII, auditable grants, and policy-before-action are mandatory; an LLM verifier cannot solely authorize action | Defines fail-closed safety behavior | Legal/provider obligations may be stricter | SEC-01 through SEC-06 and authoritative policy evidence |
| A-01-OPS | Deployment, support, recovery, and observability targets remain undecided; LAB is an external validation consumer | Keeps topology and operational targets open | Existing environment or LAB authority may change the boundary | OPS-01 through OPS-05 |
| A-01-TEAM | Team capacity, deadline, and budget remain unknown; no independently staffed services or new licensed platforms are assumed | Keeps logical ownership separate from staffing/deployment claims | Roadmap and operating feasibility remain provisional | TEAM-01 through TEAM-04 |

## Functional requirements

| Requirement ID | Requirement | Priority/status | Acceptance evidence |
|---|---|---|---|
| ARK-FR-001 | ARK shall manage tenant-scoped subscriptions, entitlements, quotas, configuration, permissions/grants, audit records, and usage records separately from ingestion and capability execution | Required | Enabling a capability neither ingests data nor runs it; unsubscribed, unauthorized, or over-quota requests receive an explicit rejection |
| ARK-FR-002 | ARK shall accept incremental push/micro-batch ingestion and referenced bulk uploads, while treating pull, federation, and streaming as conditional exceptions | Required | Contract tests cover push and bulk-reference registration; direct shared-database integration is rejected |
| ARK-FR-003 | ARK shall preserve raw inputs before normalization and publish an immutable dataset version only after authentication, registration, validation, normalization, quality, policy, and readiness checks | Required | Failure retains raw evidence and publishes no ready version; success records tenant/source/dataset/version/run identities |
| ARK-FR-004 | ARK shall expose a machine-readable definition for every release-scoped capability drawn from the seven named capability families | Required; capability evidence subject to Stage 03 | Definition-schema validation covers operations, inputs, outputs, dependencies, modes, thresholds, and fallbacks; unavailable fields remain explicit |
| ARK-FR-005 | Every capability invocation shall use a common operational envelope with authenticated tenant/caller context, request and idempotency IDs, execution mode, dataset references, callback configuration, and version context, plus capability-specific input/output | Required | Contract tests reject missing/invalid envelope context and verify capability payload independence |
| ARK-FR-006 | ARK shall distinguish dataset readiness, platform eligibility, and capability scientific eligibility and return explicit eligible, degraded, fallback, or ineligible outcomes without inventing unavailable data | Required | Independent scenario tests fail each layer and verify the expected outcome |
| ARK-FR-007 | ARK shall execute ingestion, training, backfills, large inference, scheduled work, and retryable workflows through one durable platform job lifecycle supporting state, retry, scheduling, cancellation, progress, idempotency, results, audit, and notification | Required | State-transition, persistence/restart, cancellation, retry, and duplicate-delivery tests |
| ARK-FR-008 | ARK shall reserve synchronous execution for operations classified as short and predictable; other operations shall use durable job/result semantics | Required; numeric classification threshold provisional under `A-01-SCALE` | Each operation declares an execution class; no long/retryable operation depends on request-process lifetime |
| ARK-FR-009 | Training/retraining and model activation shall require an explicit authorized lifecycle operation and shall not be triggered or activated implicitly by inference | Provisional under `A-01-ML` | Inference without an active model creates no training/activation side effect and returns the documented non-success/fallback outcome |
| ARK-FR-010 | ARK shall perform proactive work only within an active scoped tenant grant and shall otherwise report the finding without external action | Required; exact semantics provisional under `A-01-INT`/`A-01-SEC` | Negative tests cover absent, expired, revoked, quota-exceeded, stale, duplicate, and out-of-scope grants |
| ARK-FR-011 | ARK shall distinguish internal coordination events from external consumer notifications and expose completion/results through a consumer-approved contract without embedding consumer schemas in capability cores | Required; delivery mechanism deferred to Stage 07/09 | Contract tests demonstrate separate internal/external message types and adapter translation |
| ARK-FR-012 | ARK shall provide LAB with release-scoped contracts and reproducibility, isolation, evaluation, and failure evidence | Provisional under `A-01-BUS`/`A-01-OPS` | LAB-facing acceptance suite validates those properties; promotion authority and numeric gates remain TBD |

## Non-functional requirements

| Requirement ID | Requirement | Priority/status | Acceptance evidence |
|---|---|---|---|
| ARK-NFR-001 | Tenant identity shall derive from the authenticated principal, and tenant isolation shall cover rows, object paths, datasets, models, jobs, events, caches, quotas, audit, and telemetry | Required | Cross-tenant negative tests for each state class; a forged request-body tenant ID cannot change scope |
| ARK-NFR-002 | Every output shall be reproducible and traceable to tenant, source contract, dataset, feature schema, model, code, and execution versions | Required | A lineage query from any output resolves every required version reference |
| ARK-NFR-003 | Public contracts shall be small, bounded, platform-neutral, machine-readable, and independently versioned | Required | Schema linting and compatibility tests; no consumer-specific terminology in capability contracts |
| ARK-NFR-004 | Durable workers shall tolerate at-least-once delivery and make externally visible side effects idempotent | Required | Duplicate-delivery and worker-restart tests produce one logical result/action |
| ARK-NFR-005 | ARK shall minimize unnecessary PII and use tenant-scoped opaque identifiers where possible; presentation data remains outside unless explicitly required | Required; identifier availability provisional under `A-01-DATA` | Data-classification and schema tests reject undocumented direct identifiers; approved exceptions are traceable |
| ARK-NFR-006 | Requests, ingestion runs, jobs, outputs, grants, outward notifications, and usage shall carry correlation, audit, lineage, metering, and cost-attribution evidence | Required; numeric retention/alert thresholds unknown | End-to-end trace test correlates one operation across all participating records |
| ARK-NFR-007 | Every operation shall declare its execution class and receive approved measurable latency, freshness, completion, availability, and recovery targets before production acceptance | Provisional under `A-01-SCALE` | Stage 02 acceptance is an explicit TBD target record; later acceptance requires approved values and measured results |

## Constraints

| Requirement ID | Constraint | Priority/status | Acceptance evidence |
|---|---|---|---|
| ARK-CON-001 | Carry forward the declared microservice-ready modular-monolith baseline: one repository, coordinated releases, and no independent-service extraction without measured justification; Stage 04 evaluates architecture style | Approved source constraint; not a Stage 02 style selection | Repository/release design and any extraction ADR demonstrate measured scaling, hardware, deployment, ownership, reliability, or compliance justification |
| ARK-CON-002 | Each capability owns its domain logic, configuration, contracts, persistence, migrations, model lifecycle, tests, monitoring rules, and runbooks and shall not import another capability's internals or write another module's state | Required; named owners TBD | Dependency, schema-ownership, migration, and one-writer checks |
| ARK-CON-003 | Capability cores remain consumer/platform-neutral; translation occurs outside capability cores, while placement wholly outside ARK is provisional under `A-01-INT` | Required/provisional placement | Boundary and dependency checks show no consumer adapter dependency in a capability core |
| ARK-CON-004 | Large historical payloads and artifacts use the ARK data lake/object storage; PostgreSQL holds operational metadata, registry, jobs, cursors, and state rather than large historical payloads | Approved source constraint; size threshold TBD | Storage contract routes large data by reference and rejects use of operational tables as a history payload store |
| ARK-CON-005 | PostgreSQL is the initial durable source of truth for the shared job lifecycle; a broker or workflow engine requires later evidence and an approved decision | Approved source constraint | Restart/recovery tests use the initial durable source; any added mechanism cites a measured trigger and ADR |
| ARK-CON-006 | Source platforms remain authoritative for master data, provide stable tenant-scoped opaque identifiers, and ARK does not perform probabilistic identity merging | Provisional under `A-01-DATA` | Ownership/identity contract tests; unresolved identities yield not-ready/ineligible behavior |
| ARK-CON-007 | No microservice extraction, Kubernetes, broker, streaming platform, service mesh, feature store, vector database, agent framework, MCP/A2A, vendor, or numeric capacity/SLO commitment may be introduced without a traced requirement and measurable reconsideration trigger | Required anti-overengineering constraint | Component/decision inventory links every addition to a requirement, rejected alternative, and trigger |

## Analysis and recommendations

### R-02-01 — Adopt the provisional “capability platform behind consumers” boundary

- Requirement satisfied: define the system boundary and responsibilities inside and outside ARK.
- Exact stage/workflow where used: Stage 02 definition; input to Stages 03, 05–07, 09, 12, and 20.
- Why needed now: capability, data, identity, UI, and campaign-delivery ownership determine which requirements belong to ARK before components or interfaces are designed.
- Simplest viable implementation: ARK owns governed capability/data/job/result/grant/audit behavior; upstream and consuming platforms remain systems of record and own presentation/channel delivery, with consumer-side adapter ownership explicitly provisional.
- Alternative considered: make ARK the CDP, identity resolver, business UI, and campaign sender.
- Why the alternative is not preferred: no approved requirement assigns those responsibilities, and doing so would duplicate systems of record, increase PII and channel risk, and violate `A-01-BUS`/`A-01-DATA`.
- Trade-offs and operational burden: minimizes boundary breadth and coupling, but requires explicit integration ownership and may be revised if product positioning changes.
- Measurable reconsideration trigger: authoritative answers to B-02, B-03, D-01, D-02, INT-01, or a consumer use case that cannot be satisfied through the current boundary.

### R-02-02 — Define logical responsibility and failure boundaries without deployment units

- Requirement satisfied: make responsibilities unambiguous while obeying the instruction not to select architecture style.
- Exact stage/workflow where used: Stages 03–09 and Stage 22 runtime/execution analysis.
- Why needed now: later stages need stable ownership for access/control, ingestion, jobs, capabilities, proactive authorization, results, and audit even though runtime placement is not decided.
- Simplest viable implementation: treat the rows in the system-boundary table and `ARK-CON-002` as logical ownership boundaries with contract and state isolation, not as services.
- Alternative considered: create a separately deployable component for every responsibility or capability now.
- Why the alternative is not preferred: scale, team, topology, ownership, and SLO evidence are absent, and Stage 04 owns architecture-style evaluation.
- Trade-offs and operational burden: preserves simplicity and reversibility; later extraction may require adapters or migrations if measured drivers emerge.
- Measurable reconsideration trigger: measured scaling, hardware, deployment, ownership, reliability, or compliance needs that cannot be isolated inside the carried-forward baseline.

### R-02-03 — Use testable technical success criteria while keeping business and numeric operating targets provisional

- Requirement satisfied: define success criteria and make every requirement testable or explicitly provisional.
- Exact stage/workflow where used: Stage 02 gate; Stages 13–17 and production acceptance.
- Why needed now: contract correctness, isolation, reproducibility, eligibility, and safe failure can be verified without inventing scale, SLO, recovery, cost, or business-lift values.
- Simplest viable implementation: adopt SC-02-01 through SC-02-10 as technical acceptance criteria and retain explicit TBD evidence for SC-02-11/12 and `ARK-NFR-007`.
- Alternative considered: insert conventional p95 latency, availability, RPO/RTO, retention, and business-uplift targets.
- Why the alternative is not preferred: the governing prompt and `A-01-SCALE` prohibit invented commitments.
- Trade-offs and operational burden: enables a verifiable skeleton but cannot establish production fitness or economic value until owners provide targets and measurements.
- Measurable reconsideration trigger: approved answers to B-04, ML-03, S-01 through S-04, D-04, SEC-02, OPS-03/04, or measured prototype baselines.

### R-02-04 — Keep capability product scope separate from release scope and evidence sufficiency

- Requirement satisfied: define core use cases and scope without claiming unsupported capability completeness.
- Exact stage/workflow where used: Stage 03 inventory, Stage 16 validation, and Stage 20 roadmap.
- Why needed now: seven capability families are named, but MVP order is unknown and Synapse evidence is interface-only.
- Simplest viable implementation: keep all seven in product scope, require a machine-readable definition only for release-scoped capabilities, and let Stage 03 apply its per-capability evidence gate.
- Alternative considered: promise simultaneous MVP delivery or infer missing Synapse internals.
- Why the alternative is not preferred: neither is supported by approved evidence and both would hide material risk.
- Trade-offs and operational burden: preserves intended breadth but may leave Stage 03 blocked and the roadmap undated.
- Measurable reconsideration trigger: an approved MVP sequence, a scope change, or authoritative Synapse implementation/configuration/policy evidence.

## Decisions

- `decisions/ADR-000-temporary-source-evidence-disposition.md` remains accepted; Synapse contributes explicit interface facts only.
- `decisions/ADR-001-stage-01-requirements-baseline.md` remains accepted; all eight `A-01-*` assumptions are active only until their existing expiry points.
- Stage 02 introduces no new material architectural decision and therefore creates no ADR.
- The boundary, use cases, success criteria, and stable requirement IDs in this artifact are the completed Stage 02 system definition.
- No architecture style, deployment unit, cloud, vendor, broker, workflow engine, agent framework, capacity, SLO, recovery target, compliance regime, budget, deadline, or MVP order is selected here.

## Contradictions and dangerous assumptions

| ID | Evidence | Classification and treatment | Consequence |
|---|---|---|---|
| C-02-01 | `ark-assumptions.md` declares an initial modular-monolith baseline while Stage 02 says not to choose architecture style | Scope tension, not a source conflict: carry the accepted baseline as an input constraint and defer evaluation or supersession to Stage 04 | No deployment/service topology is inferred in Stage 02 |
| C-02-02 | The source requires immutable raw retention, but deletion, consent, residency, legal-hold, and backup-copy rules are unknown | Governance tension under `A-01-DATA`/`A-01-SEC` | Production data onboarding and lifecycle approval remain blocked until later policy evidence |
| C-02-03 | Permissioned proactive operation is in scope, but `A-01-BUS`/`A-01-INT` place campaign delivery outside ARK | Boundary clarification: ARK validates grants, creates auditable work, and notifies a platform; direct customer-channel delivery remains outside unless explicitly approved | Stage 09 must define authorized workflows without assuming sender ownership |
| C-02-04 | All seven capabilities are named as initial, but MVP priority and delivery constraints are unknown | Scope/schedule ambiguity | Product boundary includes seven families; release scope is explicitly unresolved |
| C-02-05 | Lightweight calls may be real-time or near-real-time, but no numeric latency, throughput, availability, RPO, or RTO exists | Dangerous precision assumption | `ARK-NFR-007` remains provisional and no production fitness claim is made |
| C-02-06 | Current implementations use direct database/platform coupling and synchronous/process-local behavior contrary to the target baseline | Current-target gap | Current behavior is migration evidence and does not define the system boundary or accepted contracts |
| C-02-07 | Synapse identifiers use “Agent,” but admitted evidence proves only synchronous interface fragments | Naming/evidence gap | No autonomous behavior, tools, memory, policy authority, or agent framework enters the definition |
| C-02-08 | ARK capabilities may be metered and potentially billable, but billing scope is unresolved and B-05 defers automated invoicing | Product-scope ambiguity | Entitlements, quotas, metering, and usage records are inside; automated invoicing/payment collection is provisionally outside |
| C-02-09 | The baseline requires adapters outside capability cores, while `A-01-INT` places them on the consumer/platform side | Assumption is stronger than the enduring source fact | Stage 07 must decide adapter ownership; only core neutrality is non-provisional |

## Open questions

These are non-blocking for Stage 02 because their temporary treatment is authorized by `ADR-001`. They retain the exact expiry conditions in Stage 01.

| ID | Question | Blocking? | Options | Recommended temporary assumption | Effect |
|---|---|---:|---|---|---|
| OQ-02-01 | Which capability/use case is the first MVP slice, and what business/LAB outcomes approve it? | No for Stage 02; before Stage 20/production acceptance | One vertical slice; named subset; all seven phased | Keep all seven in product scope, no simultaneous-delivery claim, and use technical gates without numeric business lift | Roadmap and business-success criteria remain provisional |
| OQ-02-02 | Is ARK permanently limited to the capability-platform boundary, and who owns adapters and direct external-client access? | No under `A-01-BUS`/`A-01-INT`; before Stage 07 | Platform only; expanded roles; direct external API; managed adapters | Keep CDP/UI/sender outside and place translation with consumers provisionally | May change public interfaces, IAM, and ownership |
| OQ-02-03 | What are authoritative master-data owners, identifiers, domain semantics, retention, deletion, consent, residency, and legal-hold rules? | No under `A-01-DATA`/`A-01-SEC`; required before production data approval | Supply per-domain owners/policies; tenant policy; scope data out | Upstreams own masters, stable opaque IDs are required, policy durations remain unknown | Stage 06/12/15 remain conditional |
| OQ-02-04 | What complete contracts, owners, lifecycle rules, thresholds, and implementation evidence exist for each capability, especially Synapse? | Likely Stage 03 blocker | Supply evidence; approve further bounded assumptions; scope capability out | Keep prototype behavior non-production and Synapse interface-only | Capability inventory may stop for approval |
| OQ-02-05 | What exact proactive grants, actions, verifier authority, human/deterministic controls, and notification contracts apply? | No for Stage 02; before Stage 09/12 or external action | Insight only; deterministic authorized workflow; other approved boundary | Fail closed; verifier is not sole authority; no direct channel action | Limits automation while preserving safety |
| OQ-02-06 | What numeric scale, latency, freshness, completion, availability, recovery, retention, and cost targets apply? | No under `A-01-SCALE`; before production commitments | Owner targets; measured tiers; best effort where approved | Keep values unknown and measure before irreversible choices | Sizing, SLO, recovery, and cost acceptance remain unavailable |
| OQ-02-07 | What deployment environment, support model, team ownership/capacity, budget, and delivery deadline apply? | No under `A-01-OPS`/`A-01-TEAM`; before Stages 04/15/17/20 as stated in Stage 01 | Supply constraints; retain temporary assumptions | Keep logical ownership, portable roles, no purchase/date commitment | Topology and roadmap remain conditional |

## Requirements-traceability updates

The following starts the durable requirements traceability matrix. “Logical responsibility” is not a deployable component selection.

| Requirement ID | Type | Requirement | Source | Priority/status | Acceptance evidence | Architecture element(s) | Interface/data contract | Test(s) | Stage/ADR | Open issue |
|---|---|---|---|---|---|---|---|---|---|---|
| ARK-FR-001 | FR | Separate tenant controls from ingestion and execution | `sources/normalized/ark-assumptions.md — Product and architecture`; `sources/normalized/ark-assumptions.md — Ingestion and the ARK data lake` | Required | Separation/rejection evidence | Control responsibility | Tenant/subscription/entitlement/grant/usage contracts | Contract and authorization tests | Stage 02 | B-05 billing boundary |
| ARK-FR-002 | FR | Accept push/micro-batch and referenced bulk ingestion | `sources/normalized/ark-assumptions.md — Ingestion and the ARK data lake` | Required | Ingestion contract evidence | Ingestion responsibility | Incremental and bulk-reference contracts | Contract/negative tests | Stage 02 | D-05 exceptions/cadence |
| ARK-FR-003 | FR | Preserve raw input and publish checked immutable dataset versions | `sources/normalized/ark-assumptions.md — Ingestion and the ARK data lake` | Required | Raw retention/readiness evidence | Ingestion/data responsibility | Raw object, ingestion run, dataset version, quality report | Failure and lineage tests | Stage 02 | D-03/D-04 semantics/policy |
| ARK-FR-004 | FR | Publish definitions for release-scoped capabilities | `sources/normalized/ark-assumptions.md — Integration and contracts`; `sources/normalized/system-design-prompt.md — Project information` | Required; Stage 03 evidence gate | Schema validation | Capability ownership | Capability definition | Schema/coverage tests | Stage 02; ADR-000 | MVP scope; Synapse gaps |
| ARK-FR-005 | FR | Use common operational envelope plus capability-specific payload | `sources/normalized/ark-assumptions.md — Integration and contracts` | Required | Contract evidence | Access/execution responsibilities | Operational envelope | Contract tests | Stage 02 | Auth/callback protocol |
| ARK-FR-006 | FR | Separate readiness, platform eligibility, and scientific eligibility | `sources/normalized/ark-assumptions.md — Integration and contracts` | Required | Outcome scenario evidence | Data/platform/capability responsibilities | Readiness and outcome contracts | Scenario tests | Stage 02 | Capability thresholds |
| ARK-FR-007 | FR | Use one durable lifecycle for asynchronous work | `sources/normalized/ark-assumptions.md — Execution, orchestration, and proactive operation` | Required | State/recovery evidence | Job-lifecycle responsibility | Job/status/error/result contracts | State/restart/duplicate tests | Stage 02 | Numeric retry/timeout policy |
| ARK-FR-008 | FR | Restrict synchronous mode to short predictable work | `sources/normalized/ark-assumptions.md — Execution, orchestration, and proactive operation` | Required; threshold provisional | Operation classification | Execution responsibility | Execution-mode declaration | Classification/lifetime tests | Stage 02; A-01-SCALE | Numeric boundary TBD |
| ARK-FR-009 | FR/ML | Require explicit training and activation lifecycle | `outputs/stages/01-discovery-and-questions.md — Assumptions (A-01-ML)` | Provisional | No implicit training evidence | Capability/model-lifecycle responsibility | Training/promotion records | Negative inference-side-effect test | Stage 02; ADR-001 | ML-02/03 |
| ARK-FR-010 | FR/SECURITY | Require active scoped grant for proactive work | `sources/normalized/ark-assumptions.md — Execution, orchestration, and proactive operation`; `outputs/stages/01-discovery-and-questions.md — Assumptions (A-01-SEC)` | Required; semantics provisional | No-action negative suite | Proactive authorization responsibility | Grant/workflow/audit contracts | Authorization scenario tests | Stage 02; ADR-001 | SEC-03/04; INT-04 |
| ARK-FR-011 | FR | Separate internal events and external notifications | `sources/normalized/ark-assumptions.md — Security, ownership, and operations` | Required; mechanism deferred | Message separation evidence | Coordination/integration responsibilities | Internal event and external notification contracts | Contract/idempotency tests | Stage 02 | INT-03; Stage 07/09 |
| ARK-FR-012 | FR | Expose release evidence to LAB | `sources/normalized/system-design-prompt.md — Project information`; `outputs/stages/01-discovery-and-questions.md — Assumptions (A-01-OPS)` | Provisional | LAB acceptance suite | Validation boundary | Validation evidence contract | End-to-end acceptance tests | Stage 02; ADR-001 | OPS-05/B-04 |
| ARK-NFR-001 | NFR/SECURITY | Enforce authenticated tenant binding and isolation across all state | `sources/normalized/ark-assumptions.md — Security, ownership, and operations` | Required | Cross-tenant negative evidence | All logical responsibilities | Authenticated context/tenant keys | Isolation suite | Stage 02 | SEC-01 protocol/roles |
| ARK-NFR-002 | NFR | Make outputs reproducible through independent version references | `sources/normalized/ark-assumptions.md — Integration and contracts`; `sources/normalized/ark-assumptions.md — Security, ownership, and operations` | Required | Complete lineage | Data/execution/capability responsibilities | Version and lineage contracts | End-to-end lineage test | Stage 02 | Retention of evidence |
| ARK-NFR-003 | NFR | Keep public contracts bounded, neutral, machine-readable, versioned | `sources/normalized/ark-assumptions.md — Integration and contracts` | Required | Lint/compatibility evidence | Contract boundary | All public schemas | Schema/consumer tests | Stage 02 | Version policy detail |
| ARK-NFR-004 | NFR/RELIABILITY | Tolerate at-least-once delivery with idempotent effects | `sources/normalized/ark-assumptions.md — Execution, orchestration, and proactive operation` | Required | Duplicate/restart evidence | Job/capability/integration responsibilities | Idempotency/result/notification contracts | Fault-injection tests | Stage 02 | Retry ceilings TBD |
| ARK-NFR-005 | NFR/DATA/SECURITY | Minimize PII and prefer tenant-scoped opaque IDs | `sources/normalized/ark-assumptions.md — Security, ownership, and operations`; `outputs/stages/01-discovery-and-questions.md — Assumptions (A-01-DATA)` | Required; identifier availability provisional | Classification/schema evidence | Data and contract boundaries | Identifier/data-classification contracts | Schema/privacy tests | Stage 02; ADR-001 | D-02/SEC-02 |
| ARK-NFR-006 | NFR/OPERATIONS | Correlate audit, lineage, observability, usage, and cost evidence | `sources/normalized/ark-assumptions.md — Security, ownership, and operations` | Required; numeric retention unknown | End-to-end trace | Platform-wide concern | Common correlation/audit/usage envelope | Trace completeness tests | Stage 02 | OPS-03/SEC-06 |
| ARK-NFR-007 | NFR | Define and measure operating targets before production acceptance | `sources/normalized/system-design-prompt.md — Project information`; `outputs/stages/01-discovery-and-questions.md — Assumptions (A-01-SCALE)` | Provisional | Approved target register and measurements | All runtime responsibilities later | Operation classification/SLO record | Later performance/recovery tests | Stage 02; ADR-001 | S-01 through S-04 |
| ARK-CON-001 | CONSTRAINT | Carry forward the declared modular-monolith baseline for Stage 04 evaluation | `sources/normalized/ark-assumptions.md — Product and architecture` | Approved source constraint | Repository/release/extraction evidence | Architecture-style decision deferred | N/A | Boundary/dependency checks | Stage 02; Stage 04 | Measured extraction drivers |
| ARK-CON-002 | CONSTRAINT | Preserve capability ownership and prohibit internal imports/cross-writes | `sources/normalized/ark-assumptions.md — Product and architecture`; `sources/normalized/ark-assumptions.md — Security, ownership, and operations` | Required; owners TBD | Ownership/dependency evidence | Capability boundaries | Module APIs/schemas/migrations | Static/dependency/DB tests | Stage 02 | ML-01/TEAM-01 |
| ARK-CON-003 | CONSTRAINT | Keep capability cores consumer-neutral; adapter ownership provisional | `sources/normalized/ark-assumptions.md — Integration and contracts`; `outputs/stages/01-discovery-and-questions.md — Assumptions (A-01-INT)` | Required/provisional placement | Boundary evidence | Integration boundary | Adapter/core contracts | Dependency tests | Stage 02; ADR-001 | INT-01 |
| ARK-CON-004 | CONSTRAINT/DATA | Put large history/artifacts in lake/object storage and operational state in PostgreSQL | `sources/normalized/ark-assumptions.md — Ingestion and the ARK data lake` | Approved source constraint; size TBD | Storage placement evidence | Data and operational-state responsibilities | Object references/storage policy | Storage contract tests | Stage 02 | Size/retention thresholds |
| ARK-CON-005 | CONSTRAINT | Use PostgreSQL initially as durable job truth; later mechanisms need evidence | `sources/normalized/ark-assumptions.md — Execution, orchestration, and proactive operation` | Approved source constraint | Restart/recovery evidence | Job-lifecycle responsibility | Job state contract | Recovery tests | Stage 02 | Scale/workflow trigger |
| ARK-CON-006 | CONSTRAINT/DATA | Keep upstream master ownership and prohibit probabilistic identity merging | `outputs/stages/01-discovery-and-questions.md — Assumptions (A-01-DATA)` | Provisional | Identity/ownership evidence | External data boundary | Source/identifier mapping contract | Contract/negative tests | Stage 02; ADR-001 | D-01/D-02 |
| ARK-CON-007 | CONSTRAINT | Require traced evidence before adding infrastructure, agents, vendors, or numeric commitments | `sources/normalized/system-design-prompt.md — Working rules`; `outputs/stages/01-discovery-and-questions.md — Assumptions (A-01-SCALE, A-01-OPS, A-01-TEAM)` | Required | Decision/component traceability | All later design | ADR/component specifications | Stage 23 challenge | Stage 02; ADR-001 | Measurements and approved constraints |

## Completion-gate evidence

| Gate item | Result |
|---|---|
| Every bullet in `system-design-prompt.md — 1. System definition` is addressed | Pass — source-instruction coverage maps every item |
| Business goals, users, consumers, use cases, and responsibilities are classified and cited | Pass |
| Inside/outside boundaries are unambiguous | Pass — stronger provisional placements are labeled with their `A-01-*` basis |
| Out-of-scope items are explicit | Pass |
| Stable `ARK-FR-*`, `ARK-NFR-*`, and `ARK-CON-*` IDs exist | Pass — 12 FRs, 7 NFRs, and 7 constraints |
| Every requirement is testable or explicitly provisional | Pass — every row has acceptance evidence and status; provisional rows cite active assumptions |
| Unknown scale/SLO/availability/recovery/cost values remain unknown | Pass — no numeric value is introduced; `ARK-NFR-007` and SC-02-12 retain explicit TBD evidence |
| Requirements traceability matrix started using the required fields | Pass — all 26 Stage 02 requirements are represented |
| Contradictions and dangerous assumptions are visible | Pass |
| No architecture style or later-stage product/topology decision is selected | Pass — logical responsibilities only; Stage 04 retains style evaluation |
| Downstream consequences and exact next-stage inputs are present | Pass |
| Stage-specific platform-architect review reconciled | Pass — no unresolved Stage 02 critical defect reported |

Stage 02 is `APPROVED`. Its completion gate passes, and the user approved this output before Stage 03 began.

## Downstream consequences

- Stage 03 must create or assess complete capability contracts against `ARK-FR-004` through `ARK-FR-009`, distinguish intended/current behavior, and reapply the Synapse evidence gate.
- Stage 03 may stop because Synapse ownership, dependencies, state, configuration, safety, failure behavior, observability, and policy authority remain unsupported.
- Stage 04 must evaluate architecture drivers while treating `ARK-CON-001` as a carried-forward baseline rather than a style newly chosen in Stage 02.
- Stages 05–09 must preserve the logical responsibility and failure boundaries without assuming separate deployments or infrastructure products.
- Stage 06 must resolve canonical semantics, identity, retention, deletion, consent, residency, and readiness contracts before production data approval.
- Stage 07 must decide adapter ownership, trust protocol, and per-use-case response/notification modes.
- Stages 09 and 12 must define proactive grant semantics and deterministic policy authority; the LLM verifier remains non-authoritative under the active assumption.
- Stages 13–17 cannot approve production reliability, topology, sizing, cost, or purchase commitments until numeric targets and workload evidence exist.
- Stage 16 must clarify LAB's acceptance authority and convert provisional technical gates into an executable acceptance contract.
- Stage 20 cannot sequence or date delivery until MVP priority, team, budget, and deadline are supplied.
- Stage 23 must reject any component without a direct requirement link and a measurable reconsideration trigger.

## Exact next-stage inputs

After explicit user approval of this Stage 02 output, Stage 03 must read:

- `WORKFLOW.md`, `STATUS.md`, `SOURCE_MANIFEST.md`, and `stages/STAGE-CONTRACT.md`.
- `stages/03-capability-inventory.md`.
- `outputs/stages/00-source-audit.md`, `outputs/stages/01-discovery-and-questions.md`, and `outputs/stages/02-system-definition.md` in full.
- `decisions/ADR-000-temporary-source-evidence-disposition.md` and `decisions/ADR-001-stage-01-requirements-baseline.md` in full.
- `sources/normalized/system-design-prompt.md — 2. Capability and service inventory`.
- `sources/normalized/ark-assumptions.md` in full.
- All seven admitted capability cards under `sources/normalized/service-cards/`, preserving temporary provenance labels and the Synapse interface-only constraint.
- `templates/stage-output.md`, `templates/service-contract.md`, and `templates/requirements-traceability.md`.
