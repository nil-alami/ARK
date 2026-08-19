# Stage 21 — Provisional closing deliverables

Status: `APPROVED — PROVISIONAL`

Approval record: explicitly approved by the human ARK sponsor on 2026-08-14. The approval accepts the Stage 21 provisional synthesis; it does not waive Stages 22–24, clear any production-admission block, or authorize publication.

## Purpose and scope

Assemble the ten closing deliverables required by `sources/normalized/system-design-prompt.md — 20. Final deliverables` in the exact requested order, using only approved Stages 02–20 and accepted ADR-000 through ADR-016.

This package is deliberately **provisional**. Stage 22 runtime-placement and execution-flow analysis, Stage 23 anti-overengineering review/publication, and Stage 24 independent assurance have not run. Nothing here is a production-readiness statement, a publication artifact, an approval of an unresolved capability, or permission to start implementation beyond the sponsor-accountable non-production Phase 1 defined in ADR-016.

## Inputs read in full

- `WORKFLOW.md`
- `STATUS.md`
- `SOURCE_MANIFEST.md`
- `stages/STAGE-CONTRACT.md`
- `stages/21-provisional-final-deliverables.md`
- `templates/stage-output.md`
- `sources/normalized/system-design-prompt.md — 20. Final deliverables`
- Approved `outputs/stages/02-system-definition.md` through `outputs/stages/20-roadmap.md`
- Accepted `decisions/ADR-000-temporary-source-evidence-disposition.md` through `decisions/ADR-016-phase-specific-ownership-accountability.md`
- `quality/source-instruction-coverage.md`

## Source-instruction coverage

| Required closing deliverable | Section below | Status |
|---:|---|---|
| 1. Recommended starting architecture | Deliverable 1 | Covered |
| 2. Minimal component list for first version | Deliverable 2 | Covered |
| 3. Components explicitly postponed | Deliverable 3 | Covered |
| 4. Top ten unresolved questions | Deliverable 4 | Covered; none falsely closed |
| 5. Top ten risks | Deliverable 5 | Covered |
| 6. First implementation milestone | Deliverable 6 | Covered |
| 7. Decisions that must be made now | Deliverable 7 | Covered |
| 8. Decisions that can safely wait | Deliverable 8 | Covered |
| 9. Architecture completeness checklist | Deliverable 9 | Covered with provisional gaps |
| 10. Non-technical executive summary | Deliverable 10 | Covered |

## Facts, assumptions, and status legend

- **Approved baseline:** Stages 00–20 and ADR-000 through ADR-016 are authoritative project state.
- **Buildable now:** only the non-production Phase 1 proof-of-architecture under human-sponsor accountability and synthetic/test-only authorities.
- **Unavailable:** all production capability, external trust/delivery/provider, concrete source contract, customer cutover, privileged action, production deployment, and production capacity paths remain blocked by their accepted gates.
- **Not selected:** microservices, Kubernetes, broker/event backbone, workflow product, standalone feature store/MLOps suite, gRPC, agent runtime/MCP/A2A, vector store, GPU platform, Rust, additional lakehouse product, and any vendor purchase.
- **Provisional synthesis:** this artifact will be checked and expanded by Stages 22–24; it does not replace its source stage artifacts.

### Active admission states preserved by this package

- Capability: four `MIGRATION_BLOCKED` and three `EVIDENCE_BLOCKED` profiles.
- Security/governance: `EXTERNAL_TRUST_BLOCKED`, `DATA_GOVERNANCE_BLOCKED`, `CRYPTO_SECRETS_BLOCKED`, `PRIVILEGED_ACTION_BLOCKED`, `EXTERNAL_DELIVERY_BLOCKED`, `LLM_PROVIDER_BLOCKED`, `SUPPLY_CHAIN_BLOCKED`, and `MODEL_CACHE_BLOCKED`.
- Environment and scale: `DEPLOYMENT_ENVIRONMENT_BLOCKED` and per-release/profile `CAPACITY_ADMISSION_BLOCKED`.
- Contracts and transition: `DATA_CONTRACT_ADMISSION_BLOCKED` and `CONSUMER_CUTOVER_BLOCKED`.
- Ownership: ADR-016 permits only sponsor-accountable non-production Phase 1; later data/scientific/security/integration/release/production and extraction authorities remain unassigned and fail-closed.

These states are cumulative. Stage 21 clears none of them.

## 1. Recommended starting architecture

Start ARK as a **boundary-enforced, microservice-ready Python modular monolith** with one repository and coordinated immutable releases. Run distinct role entrypoints only where lifecycle requires them; the Phase 1 proof needs `api`, `worker-general`, and one-shot migration/maintenance entrypoints, while scheduler, publisher, workflow coordinator, data-worker, and ML-worker splits remain conditional.

Use:

- versioned REST/JSON at the external boundary and typed in-process module ports internally;
- principal-derived immutable tenant context, owner-module authorization, and fail-closed control decisions;
- PostgreSQL as the first durable authority for module-owned operational schemas, job/attempt/lease/fence state, registry/catalog metadata, audit, and bounded results;
- provider-neutral object storage for immutable raw, canonical, feature, result, artifact, and evidence objects by opaque tenant/owner/version reference;
- push/micro-batch and referenced-bulk ingestion, with structural validity, semantic validity, dataset readiness, and capability eligibility as four independent decisions;
- PostgreSQL-backed durable jobs and polling for long/retryable work, with at-least-once attempts and one logical result/effect;
- capability-owned versioned feature/model/result contracts, exact artifact assignment, deterministic policy authority, mandatory audit, and supporting telemetry;
- a provisional Python/PostgreSQL/one-Linux-server implementation and benchmark target, optionally containerized, with no production-fitness or HA claim.

The Phase 1 vertical proof uses the approved recommendation-batch contract only as a `POA_FIXTURE_ONLY` shape over synthetic data. REC remains `MIGRATION_BLOCKED` and is not selected as MVP.

**Evidence:** ADR-003/004/005/008–016; approved Stages 05–08, 10, 12–15, 19–20.

## 2. Minimal component list for the first version

“First version” here means the Phase 1 non-production walking skeleton, not the MVP or production release.

| Minimal element | First-version responsibility | State/authority | Why required now | Explicit boundary |
|---|---|---|---|---|
| Python repository, module rules, and coordinated release identity | Enforce public module dependencies and one compatible build | Source/release manifest | Prevent an undisciplined monolith from becoming the implementation | No independent services |
| `api` role | REST routing, contract validation, correlation and result/job resources | Stateless where possible | Exercises the approved consumer boundary | No business/scientific authority |
| Test-only trust/AuthContext adapter | Produce immutable subject, tenant, scope and correlation for two synthetic tenants | Test configuration only | Proves body tenant cannot establish authority | Cannot be configured for shared/production use |
| Tenant control decision module | Test subscription, entitlement, quota and grant decisions | Owner PostgreSQL schema | Proves enablement, admission and execution are separate | No scientific/data readiness decision |
| Capability definition and job API module | Publish immutable CAP-REC fixture definition and typed submit/poll/cancel contracts | Definition/job owner schemas | Proves common operational envelope and versioned capability contract | `POA_FIXTURE_ONLY`; not REC admission |
| Ingestion/validation/publication module | Push/reference synthetic objects, preserve raw, validate and publish immutable ready versions | Raw/object namespaces plus ingestion metadata | Proves the complete data boundary rather than preloading ready rows | Test source does not clear `DATA_CONTRACT_ADMISSION_BLOCKED` |
| Dataset catalog/readiness module | Own exact dataset version/readiness/lineage query | Catalog schema | Separates platform readiness from capability eligibility | No capability science |
| PostgreSQL durable job manager | Job, attempt, lease, fence, idempotency, cancellation and finalization truth | Job owner schema | Core async/recovery architecture proof | No broker/workflow engine |
| `worker-general` role | Claim fenced attempts and invoke typed ingestion/capability handlers | Ephemeral process; job context only | Proves restart/retry and owner-port execution | No scheduler required for explicit request |
| Deterministic CAP-REC port fixture | Return bounded stable non-scientific result from exact synthetic references | Capability fixture namespace | Exercises capability ownership without copying prototype/model behavior | No training, ranking claim, model/cache or promotion |
| Result/object persistence | Commit bounded result metadata and immutable large result/reference | Capability-owned schema/object namespace | Makes polling and recovery authoritative | One writer; no cross-capability state |
| Audit/lineage/usage evidence | Record mandatory authority/evidence chain | Evidence owner schema/object refs | Proves reproducibility and fail-closed audit behavior | Telemetry is not audit authority |
| Observability and health interfaces | Structured logs/metrics/traces, correlation and truthful role health | Supporting telemetry | Makes fault testing diagnosable | May degrade only within approved test rules |
| Migration/maintenance entrypoint and local runbook | Bootstrap schemas/fixtures, inspect/reconcile/reset only synthetic state | Explicit one-shot privileged local role | Lets one sponsor reproduce the proof safely | No production credentials or broad worker privilege |

**Evidence:** Stage 05 `C05-*` inventory; Stage 20 Phase 1 and fourteen-item backlog; ADR-016.

## 3. Components explicitly postponed

| Postponed component/path | Status | Evidence required before reconsideration |
|---|---|---|
| Real implementations of Churn, RFM, NPT and REC | Four `MIGRATION_BLOCKED` profiles | Exact ADR-007 remediation, evaluation, reproduction, assignment, owners and release decision |
| Synapse Chat, Message and Verifier | Three `EVIDENCE_BLOCKED` profiles; `LLM_PROVIDER_BLOCKED` | Authoritative provider/model/prompt/state/data/safety/privacy/cost evidence and named owners |
| Production source/canonical contracts | `DATA_CONTRACT_ADMISSION_BLOCKED` | Identifiers, schemas, corrections, ownership, validation and explicit approval per ADR-011 |
| Real customer/legacy cutover | `CONSUMER_CUTOVER_BLOCKED` | Consumer/version inventory, mappings, dual-run/reconciliation/rollback, acceptance authority and tests |
| Webhooks, publisher-delivery role and external effects | `EXTERNAL_DELIVERY_BLOCKED`; role absent | Named destination/consumer, SSRF/signature/replay/egress/retry/runbook and authority evidence |
| Proactive action | Privileged/security and capability gates active | Named grant/policy/action semantics, Phase A/B/at-effect tests, mandatory audit and authorities |
| Scheduler in the walking skeleton | Not needed for explicit Phase 1 request | A selected scheduled operation or proactive evaluation |
| Named workflow coordinator | Conditional and undeployed | A concrete deterministic cross-operation workflow with restart/compensation evidence |
| Event broker, streaming platform and CDC | Unselected | Named subscriber/source and measured dispatch/fan-out/freshness/replay need after simpler remedies |
| Standalone feature store/MLOps suite | Unselected | Governed reuse/skew/online-latency/registry-scale need not met by existing contracts |
| Model cache | `MODEL_CACHE_BLOCKED` | Authorization-before-load isolation tests and admitted exact assignment |
| Separate data/ML worker processes or GPU pool | Conditional | Measured dependency, contention, hardware, security or accelerator benefit |
| Microservice extraction, service registry, gRPC and mesh | Unselected | ADR-003 extraction gate, stable owner/state/contracts and measured transport/operation need |
| Kubernetes or orchestration platform | Unselected | Measured fleet/placement/availability/policy need plus staffed owner/runbook |
| Agent runtime, autonomous tools/memory, MCP or A2A | No agent justified | Complete Stage 11 re-entry proof and every downstream safety/evaluation gate |
| Vector retrieval/database | Unselected | Governed corpus and measured semantic quality/latency requirement |
| Rust or additional data-lake/lakehouse infrastructure | Unselected | Measured Python/data-path limit or authoritative ecosystem requirement, migration and TCO evidence |
| Vendor/managed-service purchase | No purchase selected | Concrete requirement, benchmark, security/recovery fit, TCO/exit, budget authority and sponsor approval |
| Production Linux topology, HA, DR and autoscaling | `DEPLOYMENT_ENVIRONMENT_BLOCKED` and `CAPACITY_ADMISSION_BLOCKED` | Exact environment, targets, workload, backup/restore, runbooks, headroom and approval |

## 4. Top ten unresolved questions

| Rank | Question | Needed by | Current safe disposition |
|---:|---|---|---|
| 1 | Which consumer, capability operation and business outcome form the MVP vertical slice? | Before Phase 2 | Phase 1 only; REC fixture is not MVP selection |
| 2 | Which authoritative source/canonical contracts and stable opaque identifiers exist for that slice? | Before Phase 2 data activation | Synthetic test contract only; data-contract block remains |
| 3 | Who will be the named data/source-contract authority? | First concrete data-contract admission | Unassigned and fail-closed under ADR-016 |
| 4 | Who will own capability science, evaluation, promotion and artifact assignment for the selected capability? | Capability re-entry | Unassigned; every capability profile remains blocked |
| 5 | What exact external and workload identity, authorization, network/TLS, key/secrets and privileged-operation mechanisms apply? | Validation boundary and Phase 3 | Test-only trust locally; ADR-008 blocks remain |
| 6 | What data classification, purpose/consent, residency, retention, deletion/legal-hold, backup and derived/model policy applies? | Real data onboarding/production | `DATA_GOVERNANCE_BLOCKED` |
| 7 | What production Linux hosting, PostgreSQL/object placement, telemetry, backup/restore, patching and incident environment exists? | Phase 3 | Provisional single-server characterization only |
| 8 | What workload, latency, freshness, availability, completion, RPO/RTO, retention, growth and cost targets are approved? | Production/capacity decision | Symbolic measurement only; no numeric claim |
| 9 | Who will own security/governance, integration/consumer acceptance, release and production operations, with what separation and support/on-call scope? | First affected Phase 2 decision and Phase 3 | Unassigned and fail-closed; no 24/7 assumption |
| 10 | What authority does LAB have, and what business/scientific thresholds determine acceptance? | MVP/capability acceptance | LAB remains a minimized evidence consumer, not implicit promotion authority |

These consolidate rather than erase the forty discovery questions. Original provenance for six normalized-only cards and authoritative Synapse internals also remain open under ADR-000.

## 5. Top ten risks

| Rank | Risk | Impact | Current mitigation / trigger |
|---:|---|---|---|
| 1 | A test fixture or temporary handler is mistaken for production capability progress | Unsafe release and false scientific claims | `POA_FIXTURE_ONLY`, build guards, negative block tests, ADR-007 |
| 2 | Tenant authority/isolation fails across rows, objects, jobs, models, cache, evidence or telemetry | Cross-tenant exposure or influence | Principal-derived tenant, owned namespaces/RLS defense, full adversarial suite |
| 3 | Shared PostgreSQL becomes shared business-state ownership | Boundary erosion, unsafe joins/writes, hard extraction | Owned schemas/migrations/writers, typed ports and dependency tests |
| 4 | Crash, retry, lease expiry or response loss produces duplicate or false results/effects | Corrupt truth or external harm | Job/attempt/fence/idempotency/finalization and ambiguous-effect reconciliation |
| 5 | Prototype defects are copied into target capability behavior | Invalid predictions and irreproducible science | Four `MIGRATION_BLOCKED` profiles and explicit remediation/reproduction gates |
| 6 | Undocumented Synapse/provider behavior is inferred or enabled | Privacy, safety, cost, reliability and authority failure | Interface-only evidence; `EVIDENCE_BLOCKED` and `LLM_PROVIDER_BLOCKED` |
| 7 | Model/LLM/insight/event output is allowed to authorize proactive action | Unauthorized customer effect | Deterministic Phase A/B/at-effect authority and mandatory audit outside models |
| 8 | Local one-server success is called production-ready or highly available | Operational outage/data-loss exposure | Deployment/capacity blocks, explicit single failure domain, restore/profile gates |
| 9 | A single sponsor plus AI becomes an unreviewed authority bottleneck | Self-approval, unsafe operations, incomplete runbooks | ADR-016 narrow accountability; later named/separated authorities remain mandatory |
| 10 | Future-scale products are introduced before measured need | Excess complexity, cost and recovery burden | ADR triggers, Stage 17 measurement ladder, Stage 23 anti-overengineering review |

## 6. First implementation milestone

Build the **non-production asynchronous recommendation-contract walking skeleton** described in approved Stage 20, using synthetic two-tenant data and a deterministic `POA_FIXTURE_ONLY` handler.

The ordered milestone is:

1. Create one Python project/release skeleton with enforced public module dependencies and `api`, `worker-general`, and migration/maintenance entrypoints.
2. Establish PostgreSQL and object-reference contracts and additive owner-schema migrations.
3. Implement test-only AuthContext with principal-derived tenant and cross-tenant denial.
4. Publish the immutable fixture capability definition and common submit/poll/cancel contracts.
5. Exercise test-only push/reference ingestion, raw preservation, structural validation, semantic validation and immutable readiness publication.
6. Implement separated subscription/entitlement/quota/grant decisions.
7. Implement atomic job submission/replay, attempts, leases, fences, cancellation and handler compatibility.
8. Implement the deterministic capability fixture with independent eligibility and one authoritative result.
9. Commit lineage, audit and usage evidence; keep telemetry supporting.
10. Automate duplicate, concurrent, crash, lease-expiry, stale-fence, cancellation/finalization, audit-outage, invalid-data and cross-tenant tests against real PostgreSQL and behavior-compatible object storage.
11. Produce the immutable proof evidence manifest and sponsor-operable local runbook.

Exit requires all fourteen detailed Stage 20 backlog items to pass in clean and isolated fault lanes. Exit proves architecture plumbing only; it clears no capability, source, trust, security, deployment, capacity, cutover, provider or delivery block.

**Evidence:** approved Stage 20 — Phase 1 and first implementation milestone; ADR-016.

## 7. Decisions that must be made now

### Already decided and binding for the first milestone

- Use the approved modular-monolith/Python/PostgreSQL/object-contract baseline and the Stage 20 Phase 1 boundary.
- Keep Phase 1 non-production, synthetic-only and visibly fixture-based.
- The human sponsor is accountable for Phase 1 scope, contract acceptance, implementation review and test-evidence acceptance; AI has no approval authority.
- Use the REC request only as the proof shape, not as MVP selection.
- Keep scheduler, delivery/publisher, workflows, external providers and every future-scale component outside Phase 1.

### Reversible implementation choices required at milestone kickoff

The sponsor/implementer must record exact supported choices for:

1. Python/runtime and dependency-lock version;
2. package/module layout and dependency-enforcement rule;
3. database migration mechanism and local PostgreSQL version/profile;
4. behavior-compatible local object-storage/test adapter;
5. REST schema generation/validation and test runner;
6. process supervision for the local roles;
7. immutable local build/config/fixture identity format;
8. safe fixture reset boundary and task-created-data guard.

These are implementation records, not permission to select production vendors or change accepted contracts. If a choice changes topology, authority, protocol, durable mechanism, or irreversible cost, it needs an ADR instead of an implementation note.

No additional product, capability, production, vendor, scale or scientific decision is required to begin Phase 1.

## 8. Decisions that can safely wait

| Decision | Safe deferral point | Why it can wait |
|---|---|---|
| MVP consumer/capability/source slice | Before Phase 2 | Phase 1 is contract-fixture only and reusable |
| Real capability algorithms, model families and numeric quality thresholds | Capability-specific re-entry | Roadmap must not redesign science; profiles remain unavailable |
| Exact production IAM, secrets, crypto, network and governance products/policies | Before their validation/Phase 3 gates | Provider-neutral fail-closed contracts already exist |
| Production hosting/provider, server size, containers and HA/DR topology | Before production environment admission | Local baseline proves behavior, not fitness |
| Webhook/event delivery and proactive action | When a named consumer/action requires them | Polling remains authoritative and safer |
| Scheduler activation | When the selected operation is scheduled | Explicit Phase 1 request needs no scheduler |
| Broker/streaming/CDC | After measured dispatch/fan-out/freshness failure | PostgreSQL jobs and push/bulk satisfy present evidence |
| Feature-store, MLOps or model-registry product | After measured reuse/skew/scale need | Existing owned metadata/object contracts provide required semantics |
| Microservice extraction and gRPC | After a specific ADR-003 extraction/transport trigger | Logical boundaries work in process first |
| Kubernetes/autoscaling | After approved fleet/availability/placement need | One small role-based target minimizes operator burden |
| GPU, Rust, extra lake/lakehouse or vector infrastructure | After repeatable measured need | No current workload justifies them |
| Agent runtime, MCP or A2A | After complete Stage 11 re-entry | No current irreducible autonomy requirement |
| Vendor/managed-service purchases | After concrete requirement/TCO/budget approval | No present purchase evidence or authority |
| Detailed Phase 2/3 staffing and support model | Before the first affected decision | ADR-016 keeps later authority paths blocked |

## 9. Architecture completeness checklist

| Concern | Status | Authoritative evidence / remaining gate |
|---|---|---|
| Source inventory and integrity | Complete with declared provenance limits | Stage 00, manifest/checksums, ADR-000 |
| System boundary, goals, use cases and requirements | Complete logically | Stages 01–02; business/MVP questions remain |
| Seven capability contracts | Complete as evidence-bounded inventory | Stage 03; 4 migration and 3 evidence blocks remain |
| Architecture style and ownership | Complete for design/Phase 1 | ADR-003 and ADR-016; later named authorities remain |
| Logical components and end-to-end paths | Complete | Stage 05 |
| Data zones, contracts, lineage and acceptance authorities | Complete logically | Stage 06/ADR-011; concrete contracts/governance blocked |
| External API and integration boundary | Complete logically | Stage 07/ADR-004/015; cutover blocked |
| Execution, jobs, retries, idempotency and scheduling | Complete logically | Stage 08/ADR-005 |
| Proactive/event/delivery authority and failure semantics | Complete logically; paths inactive | Stage 09/ADR-006; security/delivery gates remain |
| ML lifecycle, features, registry, evaluation and rollback | Complete logically | Stage 10/ADR-007/012; all profiles blocked |
| Agent decision | Complete for current evidence | Stage 11/ADR-013; no agent selected |
| Security, privacy and governance | Complete logical fail-closed design | Stage 12/ADR-008; eight production blocks remain |
| Reliability and recovery | Complete logical contracts | Stage 13; numeric profiles/environment evidence remain |
| Observability and evaluation | Complete logical schemas/evidence | Stage 14; products/targets/retention/owners remain |
| Deployment and infrastructure | Complete provisional baseline | Stage 15/ADR-009/014; production environment blocked |
| Testing strategy | Complete | Stage 16; tests cannot alone clear evidence/authority blocks |
| Capacity/performance/cost | Complete symbolic model and benchmarks | Stage 17; production capacity blocked |
| Architecture decisions | Complete through ADR-016 | Stage 18 register plus ADR-016 refinement |
| Seven diagrams | Complete and rendered | Stage 19 |
| Implementation roadmap | Complete and approved | Stage 20 |
| Ten closing deliverables | Complete provisionally | This Stage 21 artifact |
| Runtime placement and required execution-flow analysis | **Pending** | Stage 22 |
| Full anti-overengineering challenge and publication set | **Pending** | Stage 23 |
| Independent assurance and publication readiness | **Pending** | Stage 24 |

**Provisional completeness result:** all Stage 21 inputs and ten closing items are present and traceable. The ARK design must not be described as published or fully assured until Stages 22–24 pass.

## 10. Executive summary for non-technical stakeholders

ARK is designed as one carefully divided software system rather than a collection of premature microservices. It will initially use Python and PostgreSQL, with large data and model files kept behind a separate storage interface. The first engineering milestone is intentionally small: prove that synthetic tenant data can enter safely, become a traceable dataset, run through a durable background job, produce one recoverable result, and remain isolated from another tenant.

This milestone does not deploy a real recommendation model or any other production AI capability. The four detailed ML capabilities need remediation and scientific approval; the three Synapse capabilities lack sufficient provider and implementation evidence. External notifications, customer cutovers, privileged actions and production hosting also remain disabled until their security, ownership and operational evidence is approved.

The human sponsor owns the non-production roadmap and reviews AI-assisted implementation. AI can help build and test the system but cannot approve itself, promote models, accept security risk or authorize production. Specialized data, scientific, security, integration, release and production-operations owners must be assigned before their decisions arise.

The design deliberately postpones Kubernetes, brokers, agents, feature stores, microservices and other expensive infrastructure until measurements prove a need. This keeps the first version understandable and operable while retaining clear seams for later growth.

## Analysis and recommendations

### R-21-01 — Treat this package as an index-backed synthesis, not a replacement design

**Requirement/where:** Stage 21 synthesis and Stages 23–24 publication. **Why now:** compressing twenty approved stages can erase qualifications. **Simplest implementation:** every closing item states its evidence and gates; detailed stages remain authoritative. **Alternative:** copy every contract into this artifact. **Why rejected:** duplication would drift and become unreadable. **Trade-off:** implementers must follow links to detailed stage artifacts. **Reconsideration:** Stage 23 assembles the dedicated publication artifacts.

### R-21-02 — Keep “first version,” “MVP,” and “production” visibly separate

**Requirement/where:** deliverables 1, 2 and 6; ADR-007/008/016. **Why now:** the first milestone is buildable while all real capabilities and production paths remain blocked. **Simplest implementation:** use the Stage 20 phase vocabulary and repeat the non-production qualifier. **Alternative:** call the skeleton an MVP. **Why rejected:** it would invent business scope and imply readiness. **Trade-off:** stakeholder messaging must explain why the first result is a fixture. **Reconsideration:** the sponsor selects and admits a Phase 2 slice.

## Decisions

- Adopt the ten ordered items above as the Stage 21 provisional closing package.
- Preserve approved stage artifacts and ADRs as authoritative detail; this package is a synthesis/index.
- Create no final publication files under `outputs/final/` in Stage 21.
- Create no new ADR because synthesis introduces no new material mechanism or authority decision.
- Keep every production block and unresolved question open exactly as recorded.
- Do not execute Stage 22 without explicit instruction.

## Contradictions and dangerous assumptions revealed during synthesis

| ID | Finding | Authoritative resolution | Upstream handling |
|---|---|---|---|
| `C-21-01` | Approved Stage 18's assumption register predates ADR-016 and still describes `A-04-OWNERSHIP` without the Phase 1 refinement | ADR-016 is the later authoritative narrow supersession | Stage 23 decision publication must append ADR-016; do not rewrite accepted history |
| `C-21-02` | Stage 20 `Q-20-03` retains historical wording “Logical roles only; preserve A-04-OWNERSHIP” | ADR-016 assigns human-sponsor Phase 1 accountability while retaining later missing authorities | Treat as drafting residue inside an approved artifact; Stage 23 uses ADR-016 effective state |
| `C-21-03` | Older stages use provisional assumptions (`A-01-DATA`, trust, cutover, ownership) that later decisions replaced | ADR-008, ADR-011, ADR-015 and ADR-016 govern their exact scopes | Stage 23 effective-risk/decision assembly must use the supersession register, not isolated old wording |
| `C-21-04` | “Final deliverables” is the source heading, but workflow prohibits claiming finality before Stage 24 | This artifact is explicitly provisional | User-facing and durable status must retain “provisional” through Stage 24 |
| `C-21-05` | “Minimal first version” can be confused with MVP | Stage 20 defines Phase 1 skeleton separately from Phase 2 MVP | All later assembly must preserve the distinction |

No contradiction requires reopening an approved architectural decision. The listed older wording is historical or superseded by accepted later evidence.

## Open questions

The authoritative prioritized list is Deliverable 4. None is closed by this synthesis. Stage 22 may expose additional placement questions but may not answer them without evidence.

## Requirements-traceability updates

| Requirement | Stage 21 evidence |
|---|---|
| Prompt Section 20 items 1–10 | Ten numbered deliverables in exact order |
| `ARK-CON-007` anti-overengineering | Postponed-component table and measurement triggers; Stage 23 still pending |
| `ARK-FR-001–012`, `ARK-NFR-001–007` | Architecture/checklist and milestone references to approved stages |
| ADR-007/008 production blocks | Deliverables 1–6 and 9 preserve unavailable states |
| ADR-016 authority | Deliverables 2, 4–7, 9 and executive summary |

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| All ten items exist in exact requested order | PASS | Numbered sections 1–10 |
| Every item traces to approved evidence | PASS | Inline evidence plus completeness checklist |
| Unresolved questions remain open | PASS | Ranked questions and explicit safe dispositions |
| Package is visibly provisional | PASS | Title, purpose, checklist and decisions |
| No blocked path is represented as available | PASS | Status legend, postponements, risks and checklist |
| Inconsistencies revealed by synthesis are recorded | PASS | `C-21-01` through `C-21-05` |
| No Stage 22 work is smuggled in | PASS | Runtime participation detail remains explicitly pending |
| No publication artifact created | PASS | `outputs/final/` unchanged |

**Gate result: PASS — PROVISIONAL ONLY.** Stage 21 satisfies its synthesis gate. It does not satisfy Stages 22–24 or authorize publication/production.

## Downstream consequences

- Stage 22 must supply exact usage/placement, execution/dependency, critical/supporting-path analysis and required execution-flow artifacts for significant elements.
- Stage 23 must apply the full anti-overengineering challenge, reconcile the effective decision/supersession state including ADR-016, and create the publication set.
- Stage 24 must independently challenge completeness and all publication claims before the design can be described without the provisional qualifier.

## Exact next-stage inputs

Stage 21 is complete. Do not execute Stage 22 until explicitly instructed.

When authorized, Stage 22 must read:

1. Approved `outputs/stages/00-source-audit.md` through `outputs/stages/20-roadmap.md`
2. Completed `outputs/stages/21-provisional-final-deliverables.md`
3. Accepted ADR-000 through ADR-016 and the effective supersession register
4. `sources/normalized/system-design-prompt.md — Runtime placement and execution-flow analysis`
5. `stages/22-runtime-execution-analysis.md`
6. The seven Stage 19 diagrams, Stage 20 first milestone, all eight required use cases, and every active/conditional/block state

Stage 22 may produce only `outputs/stages/22-runtime-execution-analysis.md` and must stop before Stage 23.
