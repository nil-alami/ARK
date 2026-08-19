# Stage 20 — Implementation roadmap

**Status:** APPROVED  
**Prepared:** 2026-08-13  
**Stage owner:** Primary architecture agent  
**Authorized specialist:** `platform_architect` (read-only sequencing and dependency review)

## Purpose and scope

Turn the approved ARK design into an implementable, evidence-gated sequence covering the walking skeleton/proof of architecture, MVP, production hardening, scale-driven improvements, and optional future capabilities required by `sources/normalized/system-design-prompt.md — 19. Implementation roadmap`.

The roadmap orders work; it does not invent a delivery date, staffing plan, budget, production topology, first business capability, numeric SLO, or production approval. “Built,” “tested,” “MVP,” and “production-admitted” are distinct states. Stage 21 is not executed.

## Inputs read in full

- `WORKFLOW.md`
- `STATUS.md`
- `SOURCE_MANIFEST.md`
- `stages/STAGE-CONTRACT.md`
- `stages/20-roadmap.md`
- `templates/stage-output.md`
- `sources/normalized/system-design-prompt.md — 19. Implementation roadmap`
- Approved `outputs/stages/02-system-definition.md` through `outputs/stages/19-diagrams.md`
- Accepted ADR-000 through ADR-015 and the effective register in approved Stage 18; accepted ADR-016 recorded during Stage 20
- `quality/source-instruction-coverage.md`

## Specialist reconciliation

Stage 20 explicitly authorizes `platform_architect`. The specialist reviewed the walking-skeleton choice, dependency ordering, phase entry/exit gates, production-block preservation, and prevention of speculative future infrastructure. It found the sequence defensible and identified expired `A-04-OWNERSHIP` as the sole approval blocker. The sponsor then approved accepted ADR-016, assigning the human sponsor accountability for the non-production roadmap and Phase 1 while keeping every later specialist and production authority fail-closed. The primary agent reconciled the review and remains the sole authoritative writer.

## Source-instruction coverage

| Governing requirement | Roadmap section | Status |
|---|---|---|
| Walking skeleton/proof of architecture | Phase 1 and first milestone backlog | Covered |
| MVP | Phase 2 | Covered |
| Production hardening | Phase 3 | Covered |
| Scale-driven improvements | Phase 4 | Covered |
| Optional future capabilities | Phase 5 | Covered |
| Scope, tasks, deliverables, dependencies, acceptance, risks, postponements for every phase | Per-phase contract tables | Covered |
| One realistic request through important boundaries | Phase 1 vertical proof | Covered without production admission |

## Confirmed facts

1. The approved starting architecture is one coordinated Python codebase and release, PostgreSQL-first durable state, provider-neutral object storage, and initially co-hosted Linux runtime roles. It is not a service-per-capability system and makes no production-fitness claim. ADR-003, ADR-005, ADR-009, and ADR-010.
2. The product scope contains seven capability families, but a simultaneous first release is explicitly out of scope and the first capability/consumer/source slice is unresolved. `outputs/stages/02-system-definition.md — Core use cases; Out of scope`.
3. Churn, RFM, NPT, and REC remain `MIGRATION_BLOCKED`. The three Synapse capabilities remain `EVIDENCE_BLOCKED`. A roadmap task or passing platform test cannot clear either state. ADR-007 and Stage 10.
4. All eight ADR-008 security states, `DEPLOYMENT_ENVIRONMENT_BLOCKED`, per-release/profile `CAPACITY_ADMISSION_BLOCKED`, `DATA_CONTRACT_ADMISSION_BLOCKED`, and `CONSUMER_CUTOVER_BLOCKED` remain cumulative. ADR-016 narrows `A-04-OWNERSHIP` only for human-sponsor accountability over Stage 20 and non-production Phase 1; every later authority gate remains cumulative. Stage 18 and ADR-016.
5. Stage 16 defines merge, candidate, shared-validation, capability-re-entry, security, delivery/workflow, environment, and production-release gates. No waiver may bypass an active production block, tenant isolation, mandatory audit, unauthorized effects, data/model integrity, or secret protection.
6. The sponsor will operate the initial project with AI assistance and no assumed 24/7 team. AI may implement and analyze, but cannot own approvals, production authority, spend, scientific promotion, security decisions, or operations accountability. ADR-009 and approved Stages 15–16.
7. No current evidence justifies Kubernetes, a broker, a workflow engine, a feature-store product, gRPC, microservice extraction, agent infrastructure, vector storage, GPU infrastructure, Rust, a separate lakehouse product, or a vendor purchase. Accepted ADRs and Stage 17.

## Active block-preservation register

| State | Roadmap treatment |
|---|---|
| Four `MIGRATION_BLOCKED` profiles | Phase 1 uses only a conspicuous test double; Phase 2 requires exact per-profile re-entry and recorded approval |
| Three `EVIDENCE_BLOCKED` profiles | No Synapse/provider call in Phase 1; each remains unavailable until its full evidence gate passes |
| `EXTERNAL_TRUST_BLOCKED` | Test-only trust adapter in Phase 1; exact production trust evidence required in Phase 3 |
| `DATA_GOVERNANCE_BLOCKED` | Synthetic data only in Phase 1; classification/purpose/retention/deletion/residency authority required before production data |
| `CRYPTO_SECRETS_BLOCKED` | No production secret or key claim; exact environment mechanism and lifecycle required in Phase 3 |
| `PRIVILEGED_ACTION_BLOCKED` | No promotion, grant mutation, deletion, sensitive export, proactive effect, or recovery authority is enabled by the roadmap |
| `EXTERNAL_DELIVERY_BLOCKED` | Polling is authoritative; webhook/publisher remains absent unless separately admitted |
| `LLM_PROVIDER_BLOCKED` | No Synapse/provider execution or transfer; Phase 5 re-entry only |
| `SUPPLY_CHAIN_BLOCKED` | Phase 1 produces local evidence only; production build identity/signing/separation/revocation remains Phase 3 gated |
| `MODEL_CACHE_BLOCKED` | Phase 1 loads no production model; exact authorization-before-cache tests remain required for any admitted cached load |
| `DEPLOYMENT_ENVIRONMENT_BLOCKED` | Local/validation lanes are not production; exact production environment and runbooks required in Phase 3 |
| `CAPACITY_ADMISSION_BLOCKED` | Phase 1/2 characterize only; approved targets, workload and headroom required before production |
| `DATA_CONTRACT_ADMISSION_BLOCKED` | Synthetic test contract cannot clear it; each Phase 2 concrete contract requires ADR-011 evidence/authority |
| `CONSUMER_CUTOVER_BLOCKED` | Phase 1 has no migration; each real cutover requires ADR-015 packet and approval |
| `A-04-OWNERSHIP` / ADR-016 | Stage-20 expiry is narrowly superseded for sponsor-accountable non-production Phase 1; all data/scientific/security/integration/release/production and extraction gates remain fail-closed |

## Assumptions and roadmap rules

| ID | Classification | Treatment |
|---|---|---|
| `A-20-01` | Temporary implementation assumption | The walking skeleton uses synthetic, non-production fixtures for two isolated tenants, a test-only trust adapter, and a contract-compatible deterministic CAP-REC handler double. It expires when the skeleton is accepted or before any shared/customer environment, whichever comes first. |
| `A-20-02` | Temporary implementation assumption | The skeleton uses an explicitly test-only synthetic source contract through the real push/referenced-bulk ingestion path. It cannot be configured as a production source contract and cannot clear or bypass `DATA_CONTRACT_ADMISSION_BLOCKED`. Same expiry as `A-20-01`. |
| `A-20-03` | Explicit non-assumption | CAP-REC is chosen only because Stage 07 already contains a concrete batch-submission contract. This is not a decision that REC is the MVP or first production capability. |
| `A-20-04` | Sequencing rule | Each phase may build negative/block behavior before its external evidence exists. It may not simulate block clearance or report production readiness. |
| `A-20-05` | Planning rule | No calendar duration, person count, budget, velocity, or numeric objective is estimated until authoritative inputs exist. Milestones are dependency- and evidence-ordered. |
| `A-20-06` | Dispositioned | Accepted ADR-016 replaces the expired Stage-20 treatment: the human sponsor owns non-production Phase 1 decisions; missing later authorities remain explicit blocks. |

## Roadmap at a glance

| Phase | Outcome | May begin when | Exit meaning | Does not mean |
|---|---|---|---|---|
| 1. Walking skeleton / proof of architecture | One realistic async request crosses the critical platform boundaries using governed test doubles | Approved architecture and local development dependencies available | Architecture seams, durable lifecycle, tenant isolation, evidence, and recovery are executable | Capability readiness, source admission, external trust, production fitness, or MVP scope approval |
| 2. MVP — first admitted vertical slice | One sponsor-selected consumer/source/capability slice works in a controlled validation environment | Phase 1 passes and sponsor supplies the slice/owners/contracts | Release-scoped behavior and evidence are complete for that slice | Public production, all seven capabilities, external delivery, proactive action, or scale claims |
| 3. Production hardening | A release candidate satisfies every applicable production-admission gate | MVP evidence exists and exact environment/authority/target inputs are supplied | Candidate is technically and operationally eligible for explicit release decision | Automatic deployment, business acceptance, or clearance of unrelated capability paths |
| 4. Scale-driven improvements | Measured bottlenecks are addressed with the least costly remedy | Approved targets exist and repeatable measurements show a miss | Specific approved target is met with regression/recovery/cost evidence | General permission to distribute, add platforms, or buy products |
| 5. Optional future capabilities | Additional slices/mechanisms enter only through their recorded re-entry gates | Sponsor selects scope and all affected gates have evidence | Only the approved optional slice is admitted | Default platform expansion |

## Phase 1 — Walking skeleton / proof of architecture

### Realistic vertical proof

Prove the approved Stage 06 transaction-to-recommendation lifecycle and Stage 07 request:

`POST /v1/capabilities/CAP-REC/versions/1.0/operations/recommendation-generate-batch:submit`

for a synthetic tenant. First, the test client submits synthetic transaction/catalog/inventory data through the real push or referenced-bulk boundary; ARK preserves raw evidence and exercises structural validation, semantic validation, and immutable readiness publication. The recommendation request then references those exact dataset versions. The edge derives tenant context from a test credential, the control module returns a versioned test grant/entitlement decision, the API creates one durable job, a worker claims it with a lease/fence, the catalog and capability public port independently evaluate readiness/eligibility, a deterministic contract fixture returns a bounded non-scientific result, the result/audit/lineage/usage commit becomes authoritative, and the caller polls the stable job/result resources.

The handler must identify itself as `POA_FIXTURE_ONLY`. It does not load a production model, fit data, call Synapse, rank customer offers scientifically, authorize action, publish an event, or deliver a webhook. CAP-REC remains `MIGRATION_BLOCKED`.

### Phase contract

| Field | Phase 1 disposition |
|---|---|
| Scope | One repository/release; `api`, `worker-general`, and one-shot maintenance/developer entrypoints; minimal owner modules for AuthContext, control decisions, definitions, ingestion/catalog, jobs/attempts, fixture capability, results, audit/lineage/usage, PostgreSQL, and object-reference contract. A scheduler is unnecessary for this explicit client request and remains outside the skeleton. |
| Tasks | Establish module dependency rules; create reproducible local build/config; create additive bootstrap migrations; implement typed AuthContext and two-tenant fixtures; publish one immutable capability definition; implement job/attempt/lease/fence/idempotency state; implement test-only push/reference ingestion, raw preservation, structural/semantic validation and readiness publication; implement deterministic handler; implement authoritative finalization; expose polling/cancel semantics; add structured correlation and health; automate critical tests. |
| Deliverables | Runnable local release with `api`, `worker-general`, and migration/maintenance entrypoints; schema migrations; API schemas; synthetic source/dataset fixture manifest; one end-to-end trace/evidence manifest; ingestion failure, restart, duplicate, stale-fence, cross-tenant and denial tests; operator instructions for local start, migrate, run, inspect, and reset fixture state. |
| Dependencies | Approved ADR-003/004/005/008/009/010/015; Stage 07 request/job contracts; Stage 08 state machine; Stage 12 tenant rules; Stage 13 recovery invariants; Stage 16 fixture/test contracts; named non-production implementation/contract/test accountability supplied by the ownership decision below. No external production evidence is an entry dependency because all authorities/providers are test-only and fail closed. |
| Acceptance criteria | The first-milestone checklist below passes; the same idempotency key returns one logical job; process death/reclaim yields one terminal result; stale attempt cannot finalize; forged/cross-tenant references are denied without leakage; result resolves exact fixture/release/config/handler/run identities; mandatory audit failure prevents success; polling remains authoritative; every active production block remains visible. |
| Major risks | A test double may be mistaken for REC progress; shared PostgreSQL may erode module ownership; happy-path work may omit crash windows; local auth may leak into deployable configuration; fixture reset may destroy non-fixture data. |
| Deliberately postponed | Real capability algorithms/models, real source ingestion, production identity/secrets, external provider/webhook, proactive action, named workflows, publisher role, customer migration/cutover, business UI, billing, numeric performance/SLOs, production hosting, HA/DR, containers as a mandate, and every scale/future component. |

### First implementation milestone — engineering-ready backlog

This is the first buildable milestone. Items are ordered by dependency; independent test/schema work may proceed in parallel only after the governing contract exists.

| Order | Work item | Concrete output | Verification / done condition | Trace |
|---:|---|---|---|---|
| 1 | Repository and release skeleton | One Python project with enforced public module boundaries and role entrypoints; immutable release/config identity injected at startup | Dependency test rejects private cross-module import; all roles report the same release identity | ADR-003/009; `ARK-CON-001/002` |
| 2 | Local infrastructure contracts | PostgreSQL connection/migration boundary and object-reference adapter for synthetic fixtures; no large payload in job/result tables | Clean bootstrap and repeat bootstrap pass; object access is tenant/owner/version scoped | ADR-010; `ARK-CON-004` |
| 3 | Owner-schema bootstrap | Additive schemas/tables for definition, test control, catalog, job/attempt, result, and audit/evidence owners | One-writer/role tests prevent direct cross-owner mutation | Stages 05–06; ADR-010 |
| 4 | Trusted request context | Test-only credential adapter produces immutable subject/tenant/scopes/correlation; request body tenant is ignored as authority | Two-tenant forged-ID and body-tenant negative tests pass | ADR-008; `ARK-NFR-001` |
| 5 | Capability definition | Immutable CAP-REC `1.0` definition exposing only the Stage 07 batch-submit operation and marking implementation `POA_FIXTURE_ONLY` | Definition schema/compatibility test passes; no uncontracted endpoint exists | `ARK-FR-004/008`; Stage 07 |
| 6 | Synthetic ingestion and dataset publication | Test-only source contract submits exact synthetic objects for two tenants through push/reference APIs; worker preserves raw data, validates structural and semantic rules, and publishes exact ready versions | Invalid data keeps raw evidence but publishes no READY version; four acceptance authorities remain distinct; production source-admission state remains blocked | Stage 06; ADR-011 |
| 7 | Control admission | Versioned test subscription/entitlement/quota/grant decision port separated from enablement and execution | Disabled, unauthorized, quota-denied, and ambiguous cases create no job | `ARK-FR-001`; Stage 12 |
| 8 | Durable submission | Stage 07 submit endpoint validates envelope/references and atomically creates/replays one job by tenant/operation/idempotency key | Duplicate and concurrent submissions return the same logical job; DB failure returns no acceptance | ADR-004/005; CP-13-02 |
| 9 | Worker claim and recovery | Worker claims an attempt with lease/fence/handler version; heartbeat, expiry, cancellation request, and stale-attempt rejection work | Kill/restart, lease expiry, cancel/finalize race, incompatible handler, and poison fixture tests pass | Stage 08; Stage 13 |
| 10 | Independent readiness and fixture eligibility | Catalog returns readiness; fixture capability returns eligibility separately | NOT_READY and INELIGIBLE remain distinct and produce no fabricated result | `ARK-FR-006`; SC-02-04 |
| 11 | Fenced deterministic result | Fixture handler emits a bounded stable result under exact input/handler/config identities; owner commits result once | Duplicate attempts cannot duplicate/replace terminal result; object/reference mismatch fails safely | `ARK-NFR-002/004`; ADR-005 |
| 12 | Finalization and evidence | Terminal transition coordinates result reference, lineage, audit, and usage evidence; telemetry is separate | Crash at each finalization window resolves truthfully; unavailable mandatory audit prevents success | Stages 13–14; CP-13-01/02 |
| 13 | Polling and cancellation contract | `GET /v1/jobs/{job_id}`, result endpoint, and supported cancellation response map internal state to public vocabulary | Response loss/retry remains idempotent; unknown progress is null; cross-tenant read denied | Stage 07 job contract |
| 14 | Automated proof packet | Immutable manifest for build/migration/fixtures/tests/correlation and a short local runbook | One command sequence builds/migrates/starts/submits/polls; test suite emits traceable evidence | Stage 16 test manifest |

### Skeleton exit decision

Phase 1 exits only when all fourteen items pass against real PostgreSQL and behavior-compatible object storage in a disposable validation environment and an isolated restart/fault lane. Failure blocks Phase 2 planning assumptions but does not justify a broker, microservice, workflow engine, Kubernetes, or product purchase. The remedy order is contract/code/query/state-machine correction first.

## Phase 2 — MVP: first admitted vertical slice

“MVP” means a controlled, release-scoped vertical slice suitable for sponsor/LAB validation. It is not automatically public production.

### Phase contract

| Field | Phase 2 disposition |
|---|---|
| Scope | Exactly one sponsor-selected consumer, one source-contract family, one capability operation, its required data contracts, common job/result APIs, and evidence projection. Reuse the Phase 1 platform spine; replace only test-only authorities and the handler needed for that slice. |
| Tasks | Record release scope and named logical/accountable owners; approve consumer mapping and source/data contracts; clear `DATA_CONTRACT_ADMISSION_BLOCKED` for exact contracts; implement push or referenced-bulk raw-first ingestion; implement structural/semantic/readiness gates; remediate the selected capability profile and complete its data/model/evaluation/reproduction/assignment contract; implement environment-compatible identity/secrets for the validation lane; complete consumer/LAB contract, negative, migration, recovery, and evidence suites; document fallback/non-success semantics. |
| Deliverables | Versioned consumer adapter; admitted source contracts; ingestion and catalog pipeline; one real capability handler/bundle or explicitly approved deterministic profile; complete definition/API/result schemas; controlled validation environment release; immutable evidence and reproduction package; operator and consumer runbooks. |
| Dependencies | Phase 1 PASS; sponsor selection of slice; named source/data/capability/release/security/integration authorities as applicable; exact capability-card remediation evidence; affected ADR-007/008/011/015 gates; Stage 16 suites. |
| Acceptance criteria | Raw-to-ready lineage is reproducible; structural, semantic, readiness, and eligibility failures remain distinct; selected capability passes its exact ADR-007 re-entry suite and recorded decision; consumer cannot access another tenant; duplicate/retry/restart gives one logical result; LAB can consume minimized evidence; no unrelated capability/block is cleared. |
| Major risks | Selecting scope by prototype convenience rather than value/evidence; allowing MVP pressure to bypass block authorities; coupling the platform to one consumer; copying prototype schemas/paths/side effects; treating LAB acceptance as promotion authority. |
| Deliberately postponed | Every unselected capability/source/consumer; proactive external action; webhook unless the selected consumer proves it necessary and clears its gate; generic workflow; agent; real-time streaming; broker; standalone feature/MLOps products; microservice extraction; production HA/scale claims. |

### MVP selection gate

Before capability implementation begins, the sponsor must record:

1. consumer and use case;
2. capability and operation;
3. exact source/canonical contracts and dataset purposes;
4. business/scientific acceptance authority and non-numeric criteria, then approved numeric criteria when required;
5. named accountable owners for data, capability science, release, security/integration, and operations responsibilities that the slice exercises;
6. validation environment and permitted data classification;
7. whether polling alone is sufficient;
8. explicit exclusions and fallback/non-success behavior.

Without this packet, Phase 2 remains planned but inactive. The roadmap does not silently select REC merely because Phase 1 used its contract fixture.

## Phase 3 — Production hardening and admission

### Phase contract

| Field | Phase 3 disposition |
|---|---|
| Scope | Harden only the selected MVP slice and shared runtime paths it actually uses for one exact production environment/release profile. |
| Tasks | Name separated authorities and operating responsibilities; approve operation/SLO/recovery/retention/cost profiles; implement exact identity, workload identity, TLS/network, secrets/keys, egress, data governance, privileged-action, and supply-chain mechanisms; validate immutable build/promotion; finalize deployment/IaC and migrations; implement backup/restore/recovery epoch and reconciliation; establish health/SLI/alert/runbook contracts; execute load, resilience, tenant-isolation, deletion, rollback, and incident exercises; prepare release decision packet. |
| Deliverables | Environment manifest; signed/provenanced release; exact configuration and migration set; approved security/data policies; backup/restore evidence; operation profiles and measured results; dashboards/alerts bound to owners/runbooks; support and incident procedures appropriate to the sponsor-operated model; production acceptance manifest. |
| Dependencies | Phase 2 PASS; authoritative hosting/network/provider inputs; named accountable authorities; approved SLO/RPO/RTO/retention/budget/usage inputs; exact exit evidence for every applicable ADR-008 block; deployment and capacity packets; no unresolved critical/high defect. |
| Acceptance criteria | Each applicable block has its own evidence, tests, named authority, and recorded clearance; restore/reconciliation prevents stale effects; release/migration/rollback work from prior compatible state; workload fits approved limits with headroom; alerts have owners/runbooks; sponsor explicitly approves the release. |
| Major risks | Single-host failure/resource domain; single-operator overload; false confidence from validation fixtures; incomplete secrets/backup recovery; numeric targets added after testing; clearing a shared block too broadly; release rollback that cannot undo data/model/external effects. |
| Deliberately postponed | Unused capability/provider/delivery paths; additional environments/regions/HA; autoscaling; Kubernetes; broker; service extraction; GPU; Rust/lakehouse; feature store; agents; any product not required by the selected environment. |

### Production admission is a join, not a phase checkbox

The release remains unavailable until all applicable paths join successfully:

`scope + owners + source/data contracts + capability profile + security blocks + deployment environment + capacity profile + migration/recovery + consumer/cutover (if any) + delivery/provider (if any) + test/evidence manifest + explicit sponsor decision`.

Completing Phase 3 tasks cannot clear an inapplicable or unrelated capability globally, and a managed service cannot substitute for evidence or authority.

## Phase 4 — Scale-driven improvements

### Phase contract

| Field | Phase 4 disposition |
|---|---|
| Scope | Address one repeatable measured miss against one approved target at a time while preserving logical contracts and tenant authority. |
| Tasks | Reproduce bottleneck with exact workload/release/profile; remove code/query/serialization waste; bound payload/batch/checkpoint and tune backpressure/fairness; vertically size within approved limits; adjust worker pools and split same-codebase roles only for measured contention/dependency/hardware/security; add simple replicas; tune PostgreSQL/object access; recalculate total cost and recovery; invoke a dedicated ADR only if a material mechanism/topology changes. |
| Deliverables | Before/after benchmark and cost evidence; updated operation profile; regression/tenant fairness/recovery tests; capacity headroom decision; revised runbook and deployment manifest; ADR when its threshold is crossed. |
| Dependencies | Production or representative controlled workload; approved numeric objective; reliable Stage 14 signals; Stage 17 benchmark dimensions; named owner and budget authority for any spend. |
| Acceptance criteria | The exact target is met repeatably without violating correctness, isolation, recovery, cost, or another tenant/profile; simpler remedies are documented before adding infrastructure; rollback and failure behavior remain tested. |
| Major risks | Benchmark overfitting; scaling the wrong bottleneck; DB connection/I/O contention; breaking fairness; multiplying operational components; hiding sponsor time/cost; confusing replicas with service extraction. |
| Deliberately postponed | Kubernetes, broker, streaming, feature store, GPU pool, vector retrieval, service extraction, gRPC, or vendor platform until its independent accepted ADR trigger and full operating evidence pass. |

### Approved scaling ladder

1. Correct algorithms, queries, serialization, indexes, copies, and unnecessary work.
2. Bound inputs, batches, concurrency, checkpoints, retries, retention, and backpressure.
3. Vertically size the simple host, runtime roles, PostgreSQL, and storage within approved limits.
4. Split same-codebase worker roles for measured dependencies/resources/security—not by capability count.
5. Add simple API/worker replicas with safe leases, connection budgets, and coordinated release identity.
6. Tune/partition owner data and object-transfer patterns without breaking ownership.
7. Only then evaluate Kubernetes, broker, streaming, product adoption, or module extraction through the accepted trigger and ADR process.

## Phase 5 — Optional future capabilities and mechanisms

### Phase contract

| Field | Phase 5 disposition |
|---|---|
| Scope | Sponsor-selected additions treated as independent vertical-slice proposals, never a default “platform completion” program. |
| Tasks | Identify bounded need and owner; map affected requirements/ADRs/blocks; obtain authoritative evidence; compare smallest existing-mechanism solution; implement adapter/module behind public contract; execute security/reliability/observability/test/capacity gates; approve material decision and release separately. |
| Deliverables | Scope packet; evidence inventory; decision/ADR when material; implementation and migrations; complete evaluation/test/operations evidence; explicit admission or rejection record. |
| Dependencies | Existing release stability plus the addition-specific re-entry gate below. |
| Acceptance criteria | Addition meets a named requirement and approved target, preserves owner/tenant/effect authority, passes all affected gates, has an accountable operator and rollback/exit path, and does not activate unrelated mechanisms. |
| Major risks | “Optional” becoming assumed scope; product-led architecture; cross-capability coupling; new trust/egress/cost boundaries; operational load exceeding a sponsor-operated system. |
| Deliberately postponed | Every candidate until its exact trigger passes; absence from a release is intentional, not technical debt by itself. |

### Optional-capability re-entry map

| Candidate | Minimum re-entry evidence | Required preserved boundary |
|---|---|---|
| Another detailed ML capability | Exact ADR-007 profile remediation, evaluation/reproduction, owner and release evidence | No inference-time training/activation; exact assignment and rollback |
| Synapse capability | Authoritative provider/model/prompt/state/safety/privacy/cost evidence plus ADR-007/008 exit suites | Interface-only until admitted; model output remains advisory where required |
| Proactive action / webhook | Named grant/policy/action, destination and consumer contract; Phase A/B/at-effect tests; delivery security/runbook | Insight/model/event never grants authority; delivery separate from result |
| Named workflow | Concrete deterministic multi-operation scenario and Stage 08 restart/compensation contract | Public jobs only; no generic DSL/engine or private calls |
| Event broker / streaming / CDC | Named subscribers/source, measured freshness/fan-out/dispatch/replay need, security/retention/recovery/owner evidence | Source fact and job/result authority remain outside transport |
| Feature-store product | Measured governed cross-capability reuse, online/offline skew, latency or registry-scale failure | Capability scientific ownership and exact PIT/version lineage |
| Vector retrieval | Governed corpus plus semantic quality/latency target that ordinary retrieval cannot meet | Tenant/purpose/provenance and injection/exfiltration controls |
| GPU / specialized worker | Repeatable accelerator benefit or incompatible dependency/resource isolation need | Profile-specific role; no GPU platform by aspiration |
| Microservice extraction / gRPC | ADR-003 extraction criterion plus measured transport/deployment/ownership need | Same logical contract, tenant authority and migration plan |
| Kubernetes | Accepted fleet/placement/availability/policy need after simpler runtime remedies | Does not imply service-per-module, mesh, broker, or operators |
| Rust or additional lake infrastructure | Measured Python/data-path limit or authoritative ecosystem/operating requirement | Contract compatibility, migration, recovery, ownership and TCO |
| Agent / MCP / A2A | Full Stage 11 re-entry proof and downstream security/evaluation/execution/cost gates | Deterministic action/promotion/security authority remains external |
| Managed/vendor service | Concrete requirement, benchmark, security/recovery fit, TCO/exit comparison, budget and sponsor approval | ARK owns domain/control contracts; product does not clear blocks |

## Dependency and evidence-gate matrix

| Workstream | Phase 1 | Phase 2 | Phase 3 | Phase 4/5 | Blocking authority/evidence |
|---|---|---|---|---|---|
| Product/release scope | Fixture scenario only | One selected slice required | Exact production release | Each addition independently | Sponsor/product authority; B-01 |
| Ownership | Human sponsor accountable for non-production scope/contracts/implementation review/test evidence; logical module/state owners retained | Named data/scientific/integration authorities for exercised Phase 2 decisions | All production/separated security/release/operations authorities required | Owner/on-call for added component | ADR-016 and preserved `A-04-OWNERSHIP` gates |
| Source/data contract | Synthetic fixture only | Exact contract must clear block | Governance/retention/deletion/backup complete | New source repeats gate | ADR-011; `DATA_CONTRACT_ADMISSION_BLOCKED` |
| Capability | Deterministic test double | One exact profile re-entry | Only admitted assignment runs | Each capability independent | ADR-007 and Stage 10 profile authority |
| Trust/security | Test-only adapter and negative behavior | Validation-lane mechanisms | Every applicable ADR-008 block cleared | New boundary reopens review | Named security/governance authorities |
| Jobs/reliability | Full durable semantics required | Real handler uses same spine | Recovery profiles and exercises | Benchmark before mechanism change | ADR-005; Stages 13/16 |
| Consumer/cutover | Contract test caller; no cutover | Exact adapter; cutover optional and separately blocked | Approved cutover packet if exercised | Each consumer/version repeats gate | ADR-015; `CONSUMER_CUTOVER_BLOCKED` |
| Delivery/events | Absent | Polling by default | Only if separately admitted | Trigger-specific | ADR-006/008; `EXTERNAL_DELIVERY_BLOCKED` |
| Provider/LLM | Absent | Absent unless selected Synapse slice clears evidence | Exact provider gate | Reopen on provider/model change | ADR-007/008; `LLM_PROVIDER_BLOCKED` |
| Deployment | Local dev/test | Controlled validation lane | Exact environment/release admitted | Evidence-driven scale | ADR-009; deployment block |
| Capacity/cost | Characterization only | Measure selected slice | Approved profile/headroom/cost | One measured miss at a time | Stage 17; capacity block |
| Supply chain | Reproducible local evidence | Candidate provenance/scans | Production signing/separation/revocation | Reassess new products | `SUPPLY_CHAIN_BLOCKED` |

## Milestone-to-requirement, decision, test, and evidence trace

| Milestone | Requirements | ADRs/design | Minimum tests | Observable durable evidence |
|---|---|---|---|---|
| `M20-01` Walking skeleton | `ARK-FR-001/004–008`, `ARK-NFR-001–006`, `ARK-CON-001–005` | ADR-003/004/005/008/009/010/015 | Unit, contract, PostgreSQL integration, CP-13-01/02, tenant isolation, restart/fence/finalization | Release/config/migration/fixture/job/attempt/result/audit/lineage correlation manifest |
| `M20-02` First vertical slice | Adds `ARK-FR-002/003/009/012` as applicable | ADR-007/011/012 plus selected profile | Raw-to-ready data quality, capability evaluation/reproduction, consumer/LAB E2E | Exact source/dataset/feature/artifact/evaluation/assignment/result evidence |
| `M20-03` Production candidate | All applicable requirements including `ARK-NFR-007` and SC-02-11/12 | ADR-008/009/014 and all blocks | Security races, migration, restore, resilience, load/profile, supply chain, deletion, runbook exercises | Signed candidate, target register, block-clearance decisions, restore/load/security reports |
| `M20-04` Scale change | Requirement/target that measured miss demonstrates | Relevant reconsideration trigger/new ADR | Before/after performance, regression, isolation, recovery, cost | Immutable benchmark/profile and decision record |
| `M20-05` Optional addition | Named source requirement only | Addition-specific ADR/re-entry gate | Full affected Stage 16 matrix | Scope/evidence/decision/release/runbook package |

## Cross-phase risk register

| Risk | Earliest control | Escalation / stop condition |
|---|---|---|
| Test fixtures or handler escape into a shared/customer environment | Build manifest marks fixture artifacts and roles; deployable configuration rejects them outside local lane | Stop candidate creation; treat as critical supply-chain/release defect |
| AI-generated implementation silently broadens authority or scope | Contract tests, owner-schema/dependency checks, review against accepted ADRs | No merge; human sponsor decides material changes |
| One-person operation becomes unsafe | Minimal component count, automation, truthful health, runbooks, bounded support profile | Production blocked until operable ownership/support is accepted |
| Platform spine is overbuilt before slice selection | Phase 1 backlog fixed to one request and negative invariants | Defer generic UI, plugins, broker, workflow, feature/MLOps suites |
| MVP chosen before evidence/owners | MVP selection gate | Phase 2 inactive; do not infer REC selection |
| Capability prototype defects copied into target | Test double first; profile remediation and reproduction gate | Capability remains blocked |
| Shared database boundaries erode | Owned schemas/roles/migrations and public ports | No merge or extraction until repaired |
| External effects become coupled to retries | Stable effect identity, at-effect recheck, ambiguity reconciliation | Delivery/action remains undeployed |
| Production is declared from local or validation success | Cumulative admission join and explicit sponsor decision | No production release |
| Scale technology is selected from preference | Stage 17 measurements and ADR reconsideration trigger | Reject addition; continue simplest measured remedy |

## Resolved ownership decision

### Confirmed conflict

Accepted ADR-003 states that `A-04-OWNERSHIP` expires when assignments arrive **or before Stage 20 approval**, service extraction, or any production-readiness decision—whichever comes first. `STATUS.md` still records product, data, platform, capability/scientific, security, integration, release, and operations owners as unknown. The earlier decision that the sponsor will operate ARK with AI assistance establishes an operating model, but it does not silently assign every accountability or satisfy later separation-of-duties gates.

No file existence, roadmap detail, specialist review, or AI implementation could substitute for a human decision. The sponsor supplied that decision and accepted ADR-016 on 2026-08-13.

### Alternatives

| Alternative | Effect | Risks/trade-offs | Disposition |
|---|---|---|---|
| Supply named accountable people/services for all owner roles now | Fully expires `A-04-OWNERSHIP` through actual assignments | May be impossible before MVP scope and qualified specialists are known | Not selected; remains available later |
| Approve a narrow superseding ownership decision | The human ARK sponsor is accountable for the non-production roadmap and Phase 1 implementation/contract/test decisions, with AI as a non-authoritative implementer; data-contract, scientific promotion, security/governance, integration/cutover, release, and production-operations authorities remain unassigned and block their first applicable Phase 2/3 decision | Allows buildable Phase 1 while deferring specialist names; does not permit production, extraction, privileged action, external delivery/provider use, or block clearance | **Selected and accepted as ADR-016** |
| Make no decision | Preserve the prior record unchanged | Would leave Stage 20 in progress | Rejected by sponsor decision |

### Accepted ADR-016 scope

ADR-016 narrowly supersedes only the Stage-20-expiry treatment of `A-04-OWNERSHIP`:

1. The human ARK sponsor is the accountable decision owner for the non-production roadmap, Phase 1 scope, contract acceptance, implementation review, and test-evidence acceptance.
2. AI may draft and implement but owns no authority and cannot approve its own output.
3. Named data/source-contract authority is required before any concrete Phase 2 source contract clears `DATA_CONTRACT_ADMISSION_BLOCKED`.
4. Named capability/scientific authority is required before any ADR-007 capability profile can clear or promote/assign an artifact.
5. Named security/governance and privileged-operation authorities, including required separation, are required before any ADR-008 block clearance or privileged production operation.
6. Named integration/consumer authority is required before cutover, external delivery, or provider activation.
7. Named release and production-operations accountability, with accepted runbook/support/on-call scope, is required before Phase 3 production admission.
8. Service extraction remains prohibited without ADR-003's named staffed ownership and all extraction evidence.

This disposition changes sequencing accountability only. It clears no production-admission block and does not assign the sponsor scientific/security qualifications by implication.

## Analysis and recommendations

### R-20-01 — Start with the async recommendation contract fixture, not a production capability

**Requirement/where:** source Section 19 walking skeleton; first implementation milestone. **Why now:** Stage 07 provides a concrete request that crosses the edge, tenant/control, catalog, durable job, worker, capability port, result, and evidence boundaries, while every actual capability remains blocked. **Simplest implementation:** a deterministic `POA_FIXTURE_ONLY` handler over synthetic immutable references. **Alternative:** remediate a real model first. **Why rejected:** it couples platform proof to unresolved scientific/source evidence and can falsely imply production progress. **Trade-off:** the first visible result has no business/scientific value. **Reconsideration:** Phase 1 passes and the sponsor selects an admitted Phase 2 slice.

### R-20-02 — Make evidence gates the roadmap clock

**Requirement/where:** all phases; Stage 16 and Stage 18. **Why now:** calendar and staffing inputs are unknown, while dependencies and exit evidence are explicit. **Simplest implementation:** milestone entry/exit gates and cumulative block joins. **Alternative:** dates and percentage-complete estimates. **Why rejected:** they would be fabricated and could reward bypassing evidence. **Trade-off:** the roadmap cannot promise a date. **Reconsideration:** authoritative scope, staff, dependencies and delivery constraints are supplied.

### R-20-03 — Admit one vertical slice before broad platform completion

**Requirement/where:** MVP and anti-overengineering constraint. **Why now:** all seven capabilities have distinct evidence gaps and no first-release scope exists. **Simplest implementation:** sponsor-selected consumer/source/capability slice on the common spine. **Alternative:** implement all capability adapters and platform features in parallel. **Why rejected:** multiplies migration, science, test and operating work before value/evidence. **Trade-off:** other capability contracts remain designed but unavailable. **Reconsideration:** first slice passes and the sponsor explicitly sequences another.

### R-20-04 — Separate hardening from scale technology

**Requirement/where:** Phases 3–4; ADR-009 and Stage 17. **Why now:** security, restore, migrations, operations, and measured objectives are required even at small scale; distribution is not. **Simplest implementation:** harden the simple role-based release, then measure. **Alternative:** add orchestration/distribution during hardening. **Why rejected:** increases failure modes without evidence. **Trade-off:** the provisional host remains a shared failure/resource domain until approved needs justify change. **Reconsideration:** an approved target is repeatedly missed after simpler remedies.

## Decisions

- Adopt the five evidence-ordered phases and the first implementation milestone above as the completed Stage 20 roadmap.
- Use the CAP-REC batch request only as a contract-compatible proof fixture; do not select REC as MVP or clear its `MIGRATION_BLOCKED` status.
- Require the Phase 2 MVP selection packet before real capability implementation.
- Treat production admission as the cumulative join of all applicable evidence/authority gates, never as completion of a roadmap phase alone.
- Add future infrastructure or capabilities only through the accepted measurable trigger and explicit decision process.
- Create no ADR because this roadmap sequences accepted decisions and introduces no new architecture mechanism.
- Do not execute Stage 21.

## Contradictions and dangerous assumptions

| ID | Finding | Resolution | Consequence |
|---|---|---|---|
| `C-20-01` | Source requires a realistic skeleton, but no capability is production-admitted | Use a real approved request contract with a conspicuous deterministic test handler and synthetic data | Boundaries are proven without false capability admission |
| `C-20-02` | Using CAP-REC could be mistaken for MVP selection | `A-20-03`, artifact/release labels, and the independent MVP selection gate forbid that inference | Release scope remains a human decision |
| `C-20-03` | MVP normally implies production value, while environment/security inputs are missing | Define Phase 2 as controlled release-scoped validation; Phase 3 performs production admission | No production claim from MVP completion |
| `C-20-04` | The skeleton needs identity/data/model behavior while those production paths are blocked | Use test-only identity and synthetic fixture authorities; implement negative block behavior | Blocks remain active and testable |
| `C-20-05` | “One Linux server” may be read as a deployment commitment | Treat it as the local/benchmark baseline until environment gate passes | No HA/topology/size claim |
| `C-20-06` | AI is expected to code the project but cannot be an accountable owner | AI performs implementation under tests/review; sponsor/named humans or authorized services hold decisions | No authority is delegated to model output |
| `C-20-07` | Production hardening can become a catch-all platform build | Limit it to the admitted slice and actual environment paths | Unused mechanisms remain undeployed |
| `C-20-08` | Scale-driven work can smuggle future products into MVP | Phase 4 has measured entry criteria and simplest-remedy ordering | `ARK-CON-007` remains enforceable |
| `C-20-09` | `A-04-OWNERSHIP` expired before Stage 20 approval, while full later-phase assignments do not yet exist | Accepted ADR-016 assigns sponsor accountability only for non-production Phase 1 and retains later authority blocks | No silent extension, false qualification, or production authority |

## Open questions and decisions requiring human input

| ID | Question | Needed by | Current safe disposition |
|---|---|---|---|
| `Q-20-01` | Which consumer, capability operation, and business outcome form the MVP slice? | Before Phase 2 | Build Phase 1 only; do not infer REC selection |
| `Q-20-02` | Which exact source/canonical contracts and stable identifiers are available? | Before Phase 2 data activation | Synthetic fixture only; preserve data-contract block |
| `Q-20-03` | Who owns product, data, capability science, security, release, integration and operations decisions? | Before respective Phase 2 decisions and all production work | Logical roles only; preserve `A-04-OWNERSHIP` |
| `Q-20-04` | What validation and production environments, identity, network, secrets, object storage, backup and telemetry facilities exist? | Validation lane / Phase 3 | Local contracts only; preserve ADR-008/009 blocks |
| `Q-20-05` | What business/model acceptance criteria and LAB authority apply? | Capability re-entry and MVP acceptance | No numeric/business claim; LAB evidence consumer only |
| `Q-20-06` | What latency, throughput, freshness, availability, recovery, retention, scale and cost targets apply? | Phase 3 and any Phase 4 change | Characterize only; preserve capacity/deployment blocks |
| `Q-20-07` | Is polling sufficient for the first consumer, and is any cutover required? | MVP contract | Polling default; webhook and cutover blocked |
| `Q-20-08` | What support hours, incident expectations, and acceptable sponsor operating burden apply? | Phase 3 | No 24/7 assumption; production support profile blocked |
| `Q-20-09` | Which named authorities will assume the Phase 2/3 data, scientific, security, integration, release, and production-operations decisions? | Before each first applicable decision | ADR-016 keeps each path fail-closed until assignment |

## Requirements-traceability updates

| Requirement | Roadmap coverage | Exit evidence |
|---|---|---|
| `ARK-FR-001` | Phase 1 control separation; Phase 2 tenant setup | Enablement/denial/job-absence tests |
| `ARK-FR-002/003` | Phase 2 raw-to-ready ingestion | Source contract, four-layer tests and lineage |
| `ARK-FR-004–008` | Phase 1 common definition, envelope and durable lifecycle | Contract, idempotency, restart, polling and result evidence |
| `ARK-FR-009` | Phase 2 profile remediation; Phase 5 additional capabilities | Exact lifecycle/reproduction/assignment evidence |
| `ARK-FR-010/011` | Deliberately postponed unless selected; Phase 5 gate | Phase A/B/effect/delivery evidence |
| `ARK-FR-012` | Phase 2 minimized validation evidence | LAB contract/evidence package without implicit authority |
| `ARK-NFR-001–006` | Phase 1 executable invariants, strengthened in Phases 2–3 | Isolation, lineage, compatibility, restart, minimization, correlation suites |
| `ARK-NFR-007` | Phase 3 target/admission; Phase 4 measurement | Approved profiles and measured results |
| `ARK-CON-001–006` | Phase 1 repo/role/store/ownership choices; Phase 2 source ownership | Boundary, storage, source and job tests |
| `ARK-CON-007` | Phase 4/5 measurable re-entry map | Requirement, benchmark, alternatives, owner, cost and ADR evidence |
| SC-02-01–12 | Milestone trace and phase exit criteria | Stage 16 evidence manifest mapped to each exercised criterion |

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Five required roadmap phases | PASS | Phases 1–5 |
| Every phase has scope/tasks/deliverables/dependencies/acceptance/risks/postponements | PASS | Per-phase contract tables |
| Walking skeleton proves one realistic request | PASS | Exact Stage 07 CAP-REC async request with test-only deterministic internals |
| Engineering can start first milestone | PASS | Fourteen ordered work items with outputs, done conditions and trace |
| Milestones trace to requirements/ADRs/tests/evidence | PASS | Milestone trace matrix |
| No future-scale component appears in MVP | PASS | MVP postponements and Phase 4/5 triggers |
| Active production blocks remain fail-closed | PASS | Dependency/evidence matrix and admission join |
| No date, staffing, budget, numeric target or first-release scope invented | PASS | Assumptions/rules and open questions |
| Authorized platform sequencing review | PASS FOR SEQUENCE | Reviewer found the five-phase sequence defensible and all non-ownership constraints preserved |
| `A-04-OWNERSHIP` expiry resolved | PASS | Accepted ADR-016 supplies narrow sponsor accountability and preserves all later authority blocks |
| Stage 21 not executed | PASS | Scope and stop condition |

**Gate result: PASS.** The roadmap structure and authorized sequencing review pass. Accepted ADR-016 resolves the Stage-20 ownership expiry without clearing any later authority or production block. Stage 20 is complete. Stage 21 remains unauthorized until explicitly instructed.

## Downstream consequences

- Stage 21 must assemble provisional deliverables from approved stages and must present this roadmap without inventing dates or turning optional phases into committed scope.
- Stage 22 must use Phase 1 and the eventual MVP slice to select the required runtime/execution use cases while preserving role/component distinctions.
- Stage 23 must challenge every Phase 1/MVP component and every Phase 4/5 candidate against the anti-overengineering gate.
- Stage 24 must verify that the publication preserves all roadmap evidence gates and does not report blocked work as production-ready.

## Exact next-stage inputs and stop condition

Stage 20 is complete. Do not execute Stage 21 until explicitly instructed.

After the user explicitly instructs continuation, Stage 21 must read:

1. Approved `outputs/stages/00-source-audit.md` through `outputs/stages/19-diagrams.md`
2. Completed `outputs/stages/20-roadmap.md`
3. Accepted ADR-000 through ADR-016 and Stage 18 effective register plus ADR-016's narrow ownership refinement
4. `sources/normalized/system-design-prompt.md — 20. Final deliverables`
5. `stages/21-provisional-final-deliverables.md`
6. All active production blocks, unresolved questions, deliberate postponements, and Stage 20 phase gates

Stage 21 may create only the provisional deliverable assembly named by its stage file and must stop before Stage 22.

## Approval record

The sponsor explicitly approved Stage 20 and ADR-016 as recorded on 2026-08-13 and authorized execution of Stage 21 only.
