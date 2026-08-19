# Stage 01 — Discovery and architecture-driving questions

Status: `APPROVED`

## Purpose and scope

Establish the requirements baseline for ARK without designing the system: restate approved facts and decisions, expose material unknowns in one organized batch, propose reversible temporary assumptions where answers are unavailable, and separate decisions needed now from choices that can safely wait.

## Inputs read in full

- `AGENTS.md` — all sections
- `WORKFLOW.md` — all sections
- `STATUS.md` — all sections
- `SOURCE_MANIFEST.md` — all sections
- `stages/STAGE-CONTRACT.md` — all sections
- `stages/01-discovery-and-questions.md` — all sections
- `templates/stage-output.md` — all sections
- `outputs/stages/00-source-audit.md` — all sections
- `decisions/ADR-000-temporary-source-evidence-disposition.md` — all sections
- `sources/normalized/system-design-prompt.md` — `Project information` and `Working rules`
- `sources/normalized/ark-assumptions.md` — all sections
- All seven files under `sources/normalized/service-cards/` — all sections, subject to `ADR-000`

The configured `source_auditor` completed a bounded, read-only review of known facts, question completeness, dangerous assumptions, and the approval gate. It found no missing question group and recommended limiting immediate decisions to MVP/product boundary, proactive-action authority, and CDP/identity ownership; that prioritization is reconciled below. The primary agent remains the sole author of this artifact.

## Source-instruction coverage

| Source requirement | Addressed in | Status/evidence |
|---|---|---|
| Restate known facts without changing status | Facts | Addressed with source citations |
| Ask one organized batch grouped by business, data, ML, integration, scale, security, operations, and team constraints | Open questions | Addressed; all eight required groups are present |
| Give every unanswered question a temporary assumption and architectural effect | Open questions | Addressed; every row includes assumption, effect, risk, and expiry |
| Distinguish facts, assumptions, recommendations, decisions, and unresolved questions | Entire artifact | Addressed in separate sections |
| Do not invent scale, latency, security, or availability requirements | Proposed assumptions and Scale questions | Addressed; numeric targets remain unknown |
| Identify contradictions or dangerous assumptions | Contradictions and dangerous assumptions | Addressed |
| Split decisions needed now from decisions that can wait | Decision timing | Addressed |
| Avoid premature component/product choices | Recommendations and questions | Addressed; no broker, orchestrator, cluster, agent framework, feature store, or vector database is selected |

## Facts

### Product and scope facts

- ARK is a multi-tenant AI capability platform intended to help businesses understand customers, predict behavior, personalize recommendations and communications, and run policy-compliant campaigns. `sources/normalized/system-design-prompt.md — Project information`; `sources/normalized/ark-assumptions.md — Product and architecture`.
- Consumers are Direct, Whatson, POS, LAB, future external client platforms, and business users acting through those platforms. LAB is a validation platform, not an ML capability. `sources/normalized/system-design-prompt.md — Project information`.
- The seven initial capabilities are Churn, RFM, NPT, REC, Synapse chatbot, Synapse message generator, and Synapse campaign-policy verifier. `sources/normalized/system-design-prompt.md — Project information`.
- The current project is a prototype/architecture-design effort transitioning toward an MVP/platform skeleton. `sources/normalized/system-design-prompt.md — Project information`.

### Approved architectural baseline facts

- The starting style is a microservice-ready modular monolith with independent capability ownership; extraction requires measured scaling, hardware, deployment, ownership, reliability, or compliance justification. `sources/normalized/ark-assumptions.md — Product and architecture`.
- ARK's core is platform-neutral. Consumer/platform terminology belongs in adapters outside capability cores. `sources/normalized/ark-assumptions.md — Integration and contracts`.
- Subscription, ingestion, and execution are separate interactions. Push APIs are the default for incremental data, object-storage upload is for large/history loads, and streaming is conditional on measured need. `sources/normalized/ark-assumptions.md — Ingestion and the ARK data lake`.
- ARK will retain immutable raw inputs and versioned curated datasets in a data lake; PostgreSQL is for operational metadata and state, not large historical payloads. `sources/normalized/ark-assumptions.md — Ingestion and the ARK data lake`.
- Dataset readiness and capability scientific eligibility are separate, and results must explicitly distinguish eligible, degraded, fallback, and ineligible outcomes. `sources/normalized/ark-assumptions.md — Integration and contracts`.
- One durable platform job manager owns lifecycle state; capabilities own workers and computation. Short predictable work may be synchronous, while ingestion, training, batch inference, backfills, schedules, and retryable work are durable jobs. `sources/normalized/ark-assumptions.md — Execution, orchestration, and proactive operation`.
- Tenant identity comes from the authenticated principal, isolation applies across all state and telemetry, and every table has one authoritative writer. `sources/normalized/ark-assumptions.md — Security, ownership, and operations`.
- Proactive operation requires an explicit, scoped, time-bounded tenant grant; ARK must not execute outside it. `sources/normalized/ark-assumptions.md — Execution, orchestration, and proactive operation`.

### Workload and sensitivity facts

- Expected workload types include interactive API requests, incremental events, scheduled jobs, historical uploads, batch training/inference, and webhook/event notifications; their volumes are unknown. `sources/normalized/system-design-prompt.md — Project information`.
- Lightweight inference/chat may need real-time or near-real-time behavior, while ingestion, training, backfills, large predictions, and campaign workflows are asynchronous; no numeric latency target is approved. `sources/normalized/system-design-prompt.md — Project information`.
- Data may include PII or pseudonymous identifiers, behavioral and transactional history, financial purchase values, campaign content, and model outputs. `sources/normalized/system-design-prompt.md — Project information`.
- ARK minimizes unnecessary PII and prefers tenant-scoped opaque identifiers; presentation data should remain in consuming platforms unless explicitly required. `sources/normalized/ark-assumptions.md — Security, ownership, and operations`.

### Current-state facts, not target decisions

- Current capability code is Python/FastAPI-based and has Whatson/BCDP coupling, shared persistence, direct database access, and process-local scheduling that the governing prompt says must be removed. `sources/normalized/system-design-prompt.md — Project information`; capability cards — `OWNERSHIP / ISOLATION`.
- Churn and RFM are synchronous tenant-wide flows behind a combined endpoint; NPT is not active in the main workflow and has serving-contract defects; REC lacks a recommendation-generation API or active schedule. Capability cards — `TRIGGER / EXECUTION MODE`, `Current readiness assessment`, and `INTEGRATION`.
- The three Synapse cards document synchronous HTTP interfaces but not their internal models, state, dependencies, safety controls, ownership, or operating behavior. Under `ADR-000`, only explicit interface facts are admitted. `decisions/ADR-000-temporary-source-evidence-disposition.md — Decision`.

### Explicitly unknown facts

- Tenant/customer counts, traffic, data volumes, concurrency, SLOs, availability/recovery targets, deployment environment, team size, budget, and delivery deadline are unknown. `sources/normalized/system-design-prompt.md — Project information`.
- Retention/residency, identity-resolution policy, CDP positioning, exact proactive-permission semantics, observability levels, and later service-extraction needs are unresolved. `sources/normalized/system-design-prompt.md — Project information`.

## Assumptions

The following temporary assumptions are approved under `decisions/ADR-001-stage-01-requirements-baseline.md — Decision`. They are active only until their stated validation or expiry conditions and must not be silently extended.

| ID | Assumption | Why needed | Architectural effect | Risk | Validation/expiry |
|---|---|---|---|---|---|
| A-01-BUS | ARK remains an AI capability platform behind consuming platforms, not the customer master/CDP, campaign sender, or direct business-user UI; all seven capabilities remain product scope but MVP order is unresolved | Provides a provisional system boundary without inventing delivery scope | Stage 02 can define ARK's boundary while roadmap order remains open | A consumer may require direct UI, CDP ownership, or first-release scope | Expires on answers B-01 through B-05 |
| A-01-DATA | Source platforms remain systems of record; they provide stable tenant-scoped opaque IDs; ARK stores versioned raw/curated copies and does not probabilistically merge identities | Prevents current phone/BCDP coupling from becoming target identity design | Allows bounded contracts and lineage while leaving detailed domain schemas open | Source platforms may lack stable IDs or deletion/residency support | Expires on answers D-01 through D-05 |
| A-01-ML | Current implementations are non-production migration evidence; training is separately authorized from inference; unavailable evidence produces explicit degraded/ineligible results; Synapse remains non-agentic interface-only functionality | Avoids promoting known prototype defects or inventing agent behavior | Stage 02 can state responsibilities without accepting current algorithms/contracts as production-ready | May postpone a desired bootstrap-training or agentic use case | Expires on answers ML-01 through ML-06 and the Stage 03 gate |
| A-01-INT | Consumer-specific adapters remain outside ARK; tenant context comes from authenticated service identity; short calls may be synchronous and durable work uses job/result patterns; no outward action occurs without an explicit workflow/grant | Preserves the approved integration boundary while protocols are unknown | Later API work can compare concrete patterns without embedding platform coupling | Consumer constraints may require a different delivery method | Expires on answers INT-01 through INT-05 |
| A-01-SCALE | Numeric scale, latency, availability, recovery, and cost targets remain unknown; ARK will measure them before irreversible infrastructure or purchase decisions | The prompt prohibits invented values | Stage 02 records unknown NFRs; later stages use measurement points and conditional triggers, not fabricated capacity | Early estimates remain provisional and production sizing cannot be approved | Expires when S-01 through S-04 receive measured targets |
| A-01-SEC | Least privilege, authenticated tenant binding, minimal PII, auditable grants, and policy-before-action are mandatory; an LLM verifier alone cannot authorize an external campaign action | Provides a safe provisional boundary consistent with approved assumptions | Security stages can preserve enforcement and human/deterministic fallback points without selecting an IdP or compliance regime | Unknown legal duties or provider contracts may require stricter controls | Expires on SEC-01 through SEC-06 and authoritative policy evidence |
| A-01-OPS | Deployment, support, recovery, and observability targets remain undecided; no Kubernetes, broker, or workflow product is assumed; LAB is an external validation consumer until its promotion role is clarified | Prevents premature infrastructure commitment | Deployment and operations choices stay conditional | Some existing environment may impose hard constraints not yet captured | Expires on OPS-01 through OPS-05 |
| A-01-TEAM | Team capacity, deadline, and budget remain unknown; preserve the approved modular-monolith baseline and avoid commitments requiring separate service teams or new licensed platforms | Ownership capacity materially controls architecture | Stage 02 can define logical ownership without assuming independent teams/deployments | Delivery planning remains uncertain | Expires on TEAM-01 through TEAM-04 |

## Analysis and recommendations

### R-01-01 — Approve a provisional requirements baseline instead of inventing answers

- Requirement satisfied: identify material missing information first and distinguish facts, assumptions, recommendations, and decisions.
- Exact stage/workflow where used: Stage 01 approval and input to Stage 02 system definition.
- Why needed now: many architecture drivers are unknown, but the workflow can continue safely if their unknown status and reversible assumptions are explicitly approved.
- Simplest viable implementation: answer the “needed now” questions and either answer, defer, or authorize the proposed assumption for every remaining row.
- Alternative considered: infer typical startup scale, cloud, Kubernetes, Kafka, SLO, compliance, and staffing values.
- Why the alternative is not preferred: it violates the governing prompt and could lock ARK into unjustified operational burden.
- Trade-offs and operational burden: preserves evidence quality but makes later infrastructure/capacity results conditional.
- Measurable reconsideration trigger: a new confirmed requirement or measurement that invalidates an approved temporary assumption.

### R-01-02 — Resolve boundary, authority, and safety choices before numeric optimization

- Requirement satisfied: prioritize decisions that materially change system responsibilities and critical controls.
- Exact stage/workflow where used: Stage 02 boundary definition, Stage 03 capability contracts, and Stage 12 security/governance.
- Why needed now: who owns customer identity, capability outcomes, campaign authorization, and production promotion changes the system more fundamentally than a queue or deployment-product choice.
- Simplest viable implementation: decide or temporarily approve the product boundary, source-of-truth/identity model, capability ownership, training/promotion authority, consumer trust boundary, and proactive-action policy.
- Alternative considered: choose infrastructure first and adapt responsibilities later.
- Why the alternative is not preferred: responsibility changes cause more rework and risk than replaceable infrastructure mechanisms.
- Trade-offs and operational burden: delays some technology decisions but reduces rework and security ambiguity.
- Measurable reconsideration trigger: confirmed scale/SLO/environment constraints that cannot be met inside the approved responsibility boundaries.

### R-01-03 — Treat prototype behavior as migration evidence, not production acceptance

- Requirement satisfied: separate current architecture from the intended target and expose dangerous assumptions.
- Exact stage/workflow where used: Stages 02–03 and the implementation roadmap.
- Why needed now: cards document current defects, inconsistent contracts, direct database coupling, missing auth checks, and synchronous batch behavior.
- Simplest viable implementation: preserve useful business semantics and verified interfaces while requiring explicit production contracts and acceptance evidence later.
- Alternative considered: standardize the target around the current combined endpoint, shared profile writes, and train-on-demand behavior.
- Why the alternative is not preferred: it conflicts with higher-authority decisions and carries known correctness, security, and reliability defects.
- Trade-offs and operational burden: requires migration work and contract adapters but prevents prototype debt from becoming platform policy.
- Measurable reconsideration trigger: verified remediation evidence showing a current contract or implementation already satisfies the later-stage gate.

## Decisions

- `decisions/ADR-000-temporary-source-evidence-disposition.md` remains accepted and governs source use.
- `decisions/ADR-001-stage-01-requirements-baseline.md` is accepted: the Stage 01 requirements baseline is approved and `A-01-BUS`, `A-01-DATA`, `A-01-ML`, `A-01-INT`, `A-01-SCALE`, `A-01-SEC`, `A-01-OPS`, and `A-01-TEAM` are active until their stated expiry points.
- The approval does not select an architecture component, deployment platform, vendor, SLO, capacity value, compliance duty, budget, deadline, or MVP sequence.

## Contradictions and dangerous assumptions

| ID | Evidence | Classification and current treatment | Downstream consequence |
|---|---|---|---|
| C-01-01 | Approved platform-neutral core versus direct Whatson/BCDP/database coupling in current cards | Current-target gap; higher-authority baseline wins | Stage 02 must keep consumer adapters outside the core; migration constraints remain open |
| C-01-02 | Approved durable job lifecycle versus synchronous tenant batches, process-local schedules, and implicit training during inference | Current-target gap | Do not infer that current request semantics are acceptable production contracts |
| C-01-03 | “Real-time or near-real-time” is stated for lightweight paths, but no numeric target or verified benchmark exists | Dangerous precision assumption | No latency SLO or scaling topology may be invented; ask S-03 |
| C-01-04 | Synapse APIs use “Agent” identifiers, but admitted evidence shows request/response LLM interfaces and no autonomous planning/tool-use contract | Naming conflict, not agent justification | Treat as non-agentic unless ML-05 later supplies evidence; Stage 11 remains independent |
| C-01-05 | Policy must be enforced before action, but the verifier's policy semantics, authority, thresholds, and fallback are undocumented | Safety-critical evidence gap | No proactive campaign send may rely solely on the verifier; ask SEC-03 and SEC-04 |
| C-01-06 | Tenant identity must come from an authenticated principal, while current cards accept business/tenant identifiers in payloads and some routes lack enforcement | Security gap | Current endpoints are not target trust contracts; ask INT-02 and SEC-01 |
| C-01-07 | Data-lake retention and immutable raw storage are approved, while deletion, consent, residency, and retention periods are unknown | Governance tension | Data design must remain conditional and cannot approve production retention until D-04/SEC-02 are answered |
| C-01-08 | All seven capabilities are named as initial, but MVP order, release scope, owners, and deadline are unknown | Scope risk | Do not interpret “initial” as simultaneous first-release delivery; ask B-01 and TEAM-02 |
| C-01-09 | Churn has uncalibrated/forced scores, RFM semantic ranking is defective, NPT serving fields mismatch, and REC low-data fallback is bypassed | Current correctness risk | Treat all four as non-production until Stage 03 distinguishes intended contracts from implemented behavior |
| C-01-10 | Modular-monolith baseline is approved, while Kubernetes, brokers, streaming, service mesh, feature store, vector database, and agent frameworks remain unproven | Overengineering risk | Technology choices remain postponed until measurable triggers exist |

## Open questions

All questions remain unanswered unless the user supplies an answer. They are non-blocking while covered by the temporary assumptions approved in `ADR-001`, but each must be revisited by its stated expiry point. “Needed now” records the boundary decisions that would otherwise have blocked Stage 01; their recommended temporary treatment is now authorized.

### Business

Evidence basis: `sources/normalized/system-design-prompt.md — Project information`; `sources/normalized/ark-assumptions.md — Product and architecture`.

| ID | Question | Timing / blocking | Options | Recommended temporary assumption | Architectural effect, risk, and expiry |
|---|---|---|---|---|---|
| B-01 | Which capabilities and end-to-end use case must the MVP deliver first, and which may follow? | Needed now | One vertical slice; core predictive set; all seven together; user-defined order | Keep all seven in product scope but make no simultaneous-delivery commitment; choose the first slice before roadmap approval | Stage 02 keeps a broad product boundary; schedule remains provisional. Risk: effort ambiguity. Expires before Stage 20 or when priority is supplied |
| B-02 | Confirm ARK's product boundary: AI capability platform behind consumers, or also CDP/customer master, campaign sender, and direct business-user application? | Needed now | Platform only; platform plus selected roles; full CDP/engagement product | Platform only; consuming systems own customer master, presentation, and channel execution | Prevents duplicated systems of record and excess PII. Risk: a required direct product surface may be omitted. Expires on explicit product-positioning decision |
| B-03 | Which consumers onboard first, and may future external clients call ARK directly or only through managed platform adapters? | Can wait under A-01-BUS | Internal platforms only; external direct API; both | Initial platform-to-platform integration for Direct/Whatson/POS/LAB; external direct access deferred | Bounds public API/IAM scope. Risk: later external onboarding adds controls. Expires when launch consumers are named |
| B-04 | What business outcomes and LAB acceptance criteria define success for the platform and each capability? | Needed now or authorize technical-gate assumption | Business lift; model-quality gates; technical/platform gates; combined | Use evidenced technical gates—contract correctness, isolation, reproducibility, explicit eligibility, and safe failure—without inventing numeric business lift | Enables testable Stage 02 criteria while business KPIs remain open. Risk: product value is not quantified. Expires before production acceptance |
| B-05 | Which commercial/control-plane functions are required for the first release: subscriptions, entitlements, quotas, metering, chargeback, invoicing? | Can wait if deferred | Full billing; entitlements/metering only; internal controls only | Require entitlements, quotas, and usage records; postpone automated billing/invoicing | Preserves governed multi-tenancy without building finance integration. Risk: later billing schema changes. Expires before external commercialization |

### Data

Evidence basis: `sources/normalized/ark-assumptions.md — Ingestion and the ARK data lake`; capability cards — `INPUT CONTRACT` and `OWNERSHIP / ISOLATION`.

| ID | Question | Timing / blocking | Options | Recommended temporary assumption | Architectural effect, risk, and expiry |
|---|---|---|---|---|---|
| D-01 | Which system is authoritative for tenant, customer, transaction, catalog, inventory, consent, campaign, and delivery-feedback data? | Needed now | Name one owner per domain; ARK owns selected masters; shared ownership | Upstream platforms remain systems of record; ARK owns ingestion metadata, immutable versions, derived features/results, and audit lineage | Establishes one-writer boundaries. Risk: upstream ownership may be unclear. Expires when domain owners are confirmed |
| D-02 | What canonical tenant/customer/product identifiers exist, and is deterministic cross-platform identity mapping available? | Needed now | Platform-provided opaque IDs; ARK mapping; external identity service; probabilistic resolution | Require stable tenant-scoped opaque IDs and explicit mappings; do not use phone as canonical identity or probabilistically merge people | Reduces PII and cross-tenant risk. Risk: some platforms may lack stable IDs. Expires before canonical-contract approval |
| D-03 | What are the authoritative transaction/catalog semantics—event grain, status, refunds/cancellations, currency, timezone, duplicate/correction rules, inventory meaning? | Can wait under A-01-DATA until Stage 06 | Supply domain rules; define per-source adapters; declare unsupported cases | Preserve source events raw; require explicit canonical semantics before publication; mark insufficient/ambiguous data not ready | Prevents incorrect RFM/churn/REC/NPT features. Risk: capabilities remain ineligible. Expires before Stage 06 contracts are approved |
| D-04 | What retention, deletion, residency, consent, legal-hold, and backup-copy rules apply by data class and tenant? | Can wait under A-01-DATA/A-01-SEC; required before production data design | Supply policies; tenant-configurable policy; single platform policy | Keep periods/residency unknown, minimize PII, make policy metadata explicit, and do not approve production storage until duties are supplied | Avoids invented compliance. Risk: storage/deletion design remains conditional. Expires before production data onboarding |
| D-05 | What freshness, ingestion cadence, historical backfill size, late/correction rate, and genuine streaming/CDC needs exist per domain/capability? | Can wait if measured | Push/micro-batch; file; pull; CDC; stream by use case | Push/micro-batch plus object upload; no stream/CDC unless latency or volume proves need; expose timestamps and readiness | Keeps ingestion simple and scalable by evidence. Risk: later low-latency need may require change. Expires when workload measurements exist |

### ML and AI

Evidence basis: capability cards; `sources/normalized/system-design-prompt.md — Working rules`; `ADR-000`.

| ID | Question | Timing / blocking | Options | Recommended temporary assumption | Architectural effect, risk, and expiry |
|---|---|---|---|---|---|
| ML-01 | Who is accountable for each capability's contract, scientific eligibility, model lifecycle, thresholds, monitoring, and runbook? | Can wait under A-01-ML until Stage 03/04 | Named owner per capability; one temporary ML team owner; split product/ML/operations ownership | Record owner as TBD and assign no cross-capability business ownership; require owners before Stage 03 approval | Preserves logical boundaries but limits escalation and promotion authority. Expires at Stage 03 gate |
| ML-02 | Who may trigger training/retraining, and may missing-model inference automatically train and activate a model? | Can wait under A-01-ML until Stage 03/10 | Automatic bootstrap; explicit job; owner-approved promotion; tenant-controlled training | Separate training from inference; require explicit authorization and evaluation/promotion record; do not auto-activate from an inference request | Prevents surprise cost and unvalidated models. Risk: cold tenants receive ineligible status. Expires on approved lifecycle policy |
| ML-03 | What model-quality, calibration, fairness, explainability, feedback, and retraining gates apply per capability? | Can wait numerically; governance needed now | Supply thresholds; capability-owned gates; LAB-owned gates | Require versioned evaluation and owner/LAB approval without inventing numeric thresholds | Enables governance contracts but not production acceptance. Risk: promotion stays blocked. Expires before model deployment approval |
| ML-04 | How should current Churn forced scores, RFM semantic defects, NPT serving defects, and REC low-data fallback contradiction be dispositioned? | Can wait under A-01-ML until Stage 03 | Fix before migration; preserve compatibility; scope feature out; accept known limitation | Treat current outputs as non-production and non-contractual; require explicit intended contract and remediation evidence in Stage 03 | Prevents known errors becoming platform behavior. Risk: migration scope grows. Expires when each capability contract is approved |
| ML-05 | Does any Synapse capability require autonomous planning, dynamic tool selection, memory, or multi-step reasoning? | Can wait under A-01-ML until Stage 11 | Normal LLM service; deterministic workflow; bounded agent; out of scope | Treat all three as normal synchronous LLM-backed services; no agent framework, tools, autonomous memory, or proactive authority | Avoids unjustified agent architecture. Risk: a real agentic need may emerge. Expires on documented use-case evidence and Stage 11 review |
| ML-06 | What Synapse provider/model, prompt/policy versions, context sources, languages, safety evaluation, cost limits, and fallback behavior are authoritative? | Needed before Stage 03; can be deferred now under ADR-000 | Supply evidence; scope functions; retain interface-only | Keep all undocumented internals unresolved; do not infer provider, storage, safety, or fallback | Preserves evidence integrity. Risk: Stage 03 may block. Expires when authoritative Synapse evidence arrives |

### Integration

Evidence basis: `sources/normalized/ark-assumptions.md — Integration and contracts`; capability cards — `INTEGRATION`.

| ID | Question | Timing / blocking | Options | Recommended temporary assumption | Architectural effect, risk, and expiry |
|---|---|---|---|---|---|
| INT-01 | Who builds and operates Direct/Whatson/POS/LAB adapters, and which consumer-specific schemas/protocols must they support? | Can wait under A-01-INT until Stage 07 | Consumer teams; ARK team; shared integration team | Consumer/platform side owns translation adapters; ARK owns stable platform-neutral contracts | Keeps core decoupled. Risk: consumer teams may lack capacity. Expires when integration ownership is assigned |
| INT-02 | What identity provider, credential type, service trust, tenant claim, and authorization model must integrations use? | Can wait under A-01-INT/A-01-SEC until Stage 07/12 | OAuth/OIDC; mTLS; API keys; signed platform tokens; combination | Require authenticated service identity and a trusted tenant claim; never trust request-body tenant ID; defer concrete protocol | Preserves trust boundary without vendor choice. Risk: legacy clients need gateway adapters. Expires before external API contract approval |
| INT-03 | For each use case, which result mode is required: immediate response, job polling, webhook, server-sent stream, or domain event? | Can wait per use case | Map consumers to modes | Sync only for short predictable operations; durable job plus polling and optional signed webhook for long work; events only for demonstrated subscribers | Keeps contracts explicit and simple. Risk: consumer constraints may differ. Expires during Stage 07 |
| INT-04 | Which cross-capability and proactive workflows are genuinely required in the first release, including detect → generate → verify → notify/action? | Needed now | None; insight-only; deterministic approved workflow; bounded agentic workflow | Produce insights only unless a specific authorized deterministic workflow is approved; no autonomous external action | Limits blast radius and orchestration scope. Risk: reduces automation. Expires when a concrete workflow and grant semantics are approved |
| INT-05 | What coexistence, compatibility, and cutover constraints apply while removing Whatson/BCDP direct coupling and shared writes? | Can wait under A-01-INT until roadmap/integration design | Big-bang replacement; strangler/adapters; dual-write; read-only compatibility | Use adapters around legacy interfaces and migrate incrementally; avoid new cross-module writes and avoid ungoverned dual-write | Reduces migration risk. Risk: temporary adapter burden. Expires when migration/cutover plan is approved |

### Scale, performance, and availability

Evidence basis: `sources/normalized/system-design-prompt.md — Project information` explicitly marks these values unknown.

| ID | Question | Timing / blocking | Options | Recommended temporary assumption | Architectural effect, risk, and expiry |
|---|---|---|---|---|---|
| S-01 | What are current and 12–24 month ranges for tenants, customers/tenant, transactions/day, history size, catalog size, and storage growth? | Can wait only under unknown-scale assumption | Supply measured ranges and growth | Keep numeric scale unknown; instrument the walking skeleton and avoid irreversible scaling products | Prevents fabricated capacity. Risk: estimates remain conditional. Expires before Stage 17 commitments |
| S-02 | What are peak/average interactive requests, ingestion events, concurrent jobs, scheduled tenant fan-out, webhook volume, and seasonality? | Can wait only under unknown-scale assumption | Supply workload profile | Keep rates unknown; distinguish workload classes and collect queue/runtime/concurrency measurements | Allows logical separation without sizing. Risk: first deployment capacity is provisional. Expires before load testing/infrastructure sizing |
| S-03 | What numeric latency, freshness, and batch-completion objectives apply by use case? | Can wait only under unknown-SLO assumption | Supply p50/p95/p99 and deadlines; classify best-effort | Do not invent numeric SLOs; retain qualitative short-interactive versus durable-async split and measure baselines | Avoids false promises. Risk: API and UX acceptance remains incomplete. Expires before Stage 14 SLO or production acceptance |
| S-04 | What availability, maintenance-window, noisy-neighbor, RPO, RTO, and degradation requirements apply? | Can wait only under unknown-availability assumption | Supply service tiers and recovery targets | Do not invent availability/RPO/RTO; preserve tenant isolation and explicit degraded/ineligible behavior; measure and revisit | Avoids unjustified HA/DR complexity. Risk: production topology cannot be approved. Expires before Stages 13 and 15 gates |

### Security, privacy, and governance

Evidence basis: `sources/normalized/ark-assumptions.md — Security, ownership, and operations`; prompt sensitivity and proactive-action statements.

| ID | Question | Timing / blocking | Options | Recommended temporary assumption | Architectural effect, risk, and expiry |
|---|---|---|---|---|---|
| SEC-01 | Which human/service roles exist, who administers tenants and subscriptions, and how are tenant claims bound to authenticated principals? | Can wait under A-01-SEC until Stage 07/12 | Define role/claim model; federate consumer roles; ARK-local IAM | Use least-privilege platform/service roles and authenticated tenant claims; no request-field tenant authority | Sets security boundary. Risk: actual IdP/role hierarchy may differ. Expires before Stage 12 approval |
| SEC-02 | Which regulatory, contractual, residency, breach-notification, audit, and data-subject obligations apply? | Can wait under A-01-SEC until Stage 12; required before production | Name jurisdictions/contracts; declare none; unknown pending legal review | Treat duties as unknown, minimize data, retain traceability, and block production compliance claims until confirmed | Prevents invented compliance. Risk: later redesign. Expires on legal/security decision |
| SEC-03 | Who may create, approve, revoke, and audit proactive grants, and what actions/channels, scopes, thresholds, cooldowns, quotas, and expirations are allowed? | Needed now | Tenant admin; platform admin; dual approval; no proactive actions | Require explicit tenant-admin grant, auditable scope/expiry/revocation, and insight-only fallback when action is not authorized | Defines safe control boundary. Risk: workflow may be more restrictive than desired. Expires on approved permission semantics |
| SEC-04 | Is the Synapse campaign verifier advisory, an enforcement input, or the sole authorization authority; what deterministic rules or human approval remain mandatory? | Needed now | Advisory; layered enforcement; sole decision maker | Verifier is advisory/one input only; deterministic policy/permission checks remain authoritative and ambiguous cases require human approval or no action | Prevents unsafe LLM authorization. Risk: slower campaigns. Expires on authoritative policy evidence |
| SEC-05 | May customer/campaign data be sent to an external LLM, and what provider retention, training, residency, prompt-injection, tool, and exfiltration controls apply? | Can wait under A-01-SEC/ADR-000; required before Synapse production | Approved provider contract; self-hosted; redact; disable | Send no secrets or unrestricted raw PII; do not enable external processing until provider/data-use terms are approved; no tools under current evidence | Protects data but may leave Synapse non-runnable. Expires on provider/security approval |
| SEC-06 | What encryption, key ownership/rotation, secrets platform, privileged-access, and audit-retention requirements apply? | Can wait under baseline controls | Central keys; tenant keys; customer-managed keys; environment-specific | Require encryption in transit/at rest, managed secrets, least privilege, and audited privileged access; defer product/key topology | Keeps controls technology-neutral. Risk: tenant-key requirements may force redesign. Expires during Stage 12/15 |

### Operations

Evidence basis: prompt deployment unknowns; approved separation of API, scheduler, and worker runtime roles.

| ID | Question | Timing / blocking | Options | Recommended temporary assumption | Architectural effect, risk, and expiry |
|---|---|---|---|---|---|
| OPS-01 | What deployment target, cloud/on-premises constraints, regions, network boundaries, existing container platform, and managed-service restrictions apply? | Can wait under A-01-OPS until Stage 15 | Existing VMs/containers; managed platform; Kubernetes; on-prem; hybrid | Keep environment unknown and design logical/runtime roles portably; do not assume Kubernetes or a specific cloud | Avoids lock-in. Risk: infrastructure design stays conditional. Expires before Stage 15 |
| OPS-02 | What environments, CI/CD, release cadence, migration windows, rollback policy, and change approvals already exist? | Can wait under coordinated-release baseline | Supply current delivery process | One repository and coordinated releases; capability-owned tests/migrations; no independent deployability promise | Fits approved modular monolith. Risk: existing governance may impose more steps. Expires before roadmap/CI-CD design |
| OPS-03 | What support hours, on-call model, incident ownership, dashboards, alerting, trace/log/audit retention, and per-tenant reporting are required? | Can wait under unknown operations baseline | 24/7; business hours; tiered support | Require structured correlation and durable security audit; defer numeric alerts, retention, and 24/7 commitments | Enables observable skeleton without invented operations. Risk: staffing mismatch. Expires before Stage 14/production readiness |
| OPS-04 | What backup, restore, disaster-recovery test, reconciliation, and regional-failure obligations exist? | Can wait under unknown recovery targets | Supply tiers/RPO/RTO; single-region best effort | Back up operational metadata and preserve immutable/versioned artifacts; do not promise RPO/RTO or multi-region | Keeps recoverability in scope without overbuilding. Risk: topology may change. Expires before Stages 13 and 15 |
| OPS-05 | What exactly does LAB validate, with which test data, environments, acceptance authority, reproducibility evidence, and promotion veto? | Can wait under B-04/A-01-OPS until Stage 16 | Advisory testing; mandatory release gate; model-only; end-to-end platform validation | LAB validates contracts, tenant isolation, reproducibility, failure behavior, and capability evaluation evidence; numeric thresholds remain owner-approved/TBD | Gives LAB a bounded consumer role. Risk: actual authority may be broader/narrower. Expires when LAB operating contract is supplied |

### Team constraints

Evidence basis: `sources/normalized/system-design-prompt.md — Project information` identifies team size, budget, and deadline as unknown.

| ID | Question | Timing / blocking | Options | Recommended temporary assumption | Architectural effect, risk, and expiry |
|---|---|---|---|---|---|
| TEAM-01 | What teams, headcount, skills, on-call capacity, and named product/ML/data/platform/security owners are available? | Can wait under A-01-TEAM until Stage 04/20 | Supply roster/skills; one cross-functional team; multiple capability teams | Assume one small cross-functional team with logical capability ownership, but no independently staffed microservices | Reinforces modular monolith and low operational burden. Risk: “small” is not a sizing fact and may be wrong. Expires when roster is supplied |
| TEAM-02 | What delivery deadline, milestones, contractual commitments, and capability sequencing constraints exist? | Can wait under A-01-TEAM until Stage 20 | Supply date/phases; no fixed deadline; external commitments | Keep deadline unknown; do not promise simultaneous seven-capability delivery; prioritize a walking skeleton after B-01 is answered | Prevents fictional schedule. Risk: roadmap cannot be dated. Expires before Stage 20 |
| TEAM-03 | What budget, cloud/LLM spend ceiling, licensing, procurement lead time, and build-versus-buy constraints apply? | Can wait under no-purchase assumption | Supply budget/vendors; open-source only; managed services allowed | Make no purchase or managed-platform commitment; expose cost drivers and measure usage | Avoids unauthorized spend. Risk: later procurement changes design. Expires before Stage 17 commitments |
| TEAM-04 | Must capabilities release independently, and what repository, CODEOWNERS, review, documentation, and runbook standards are required? | Can wait under modular-monolith baseline | Coordinated releases; selective independent workers; independent services | One repository/coordinated releases with module ownership, contract tests, owned migrations, and runbooks; extraction only on approved triggers | Preserves simplicity. Risk: organizational autonomy needs may require extraction. Expires before Stage 04 approval |

## Decision timing

### Decisions whose temporary treatment is authorized under ADR-001

- MVP priority and product boundary: B-01, B-02, and the temporary technical success criteria in B-04.
- Customer/CDP system-of-record and canonical identity boundary: D-01 and D-02.
- Proactive-action boundary and campaign-verifier authority: INT-04, SEC-03, and SEC-04.
- The overall requirements baseline and all eight temporary assumptions are explicitly approved by `ADR-001`; the underlying questions remain unresolved.

### Decisions that can safely wait under the stated assumptions

- Consumer onboarding and billing automation: B-03 and B-05.
- Data semantics, policy details, and ingestion cadence/streaming triggers: D-03 through D-05.
- Capability ownership/lifecycle, prototype remediation, agent classification, numeric model thresholds, and detailed Synapse internals, subject to later gates: ML-01 through ML-06.
- Adapter/trust/migration ownership and per-use-case delivery mechanisms: INT-01 through INT-03 and INT-05.
- Numeric capacity, SLO, availability, and recovery targets until measured, but before production commitments: S-01 through S-04.
- IAM/compliance/LLM provider/key details except the immediate proactive-action questions: SEC-01, SEC-02, SEC-05, and SEC-06.
- Deployment environment, LAB operating contract, detailed CI/CD, on-call/observability thresholds, and disaster-recovery topology: OPS-01 through OPS-05.
- Team capacity, deadline, budget/vendor choices, and independent-release mechanics: TEAM-01 through TEAM-04.
- Specific broker, workflow engine, Kubernetes, service mesh, feature store, vector database, agent framework, MCP/A2A, and real-time streaming choices until a later requirement justifies them.

## Requirements-traceability updates

| Trace ID | Requirement | Source | Stage 01 status | Downstream use |
|---|---|---|---|---|
| RT-01-001 | Multi-tenant AI capability platform serving named consuming platforms | `system-design-prompt.md — Project information`; `ark-assumptions.md — Product and architecture` | Fact; boundary confirmation B-02/B-03 pending | Stage 02 system boundary/context |
| RT-01-002 | Seven initial capabilities and LAB validation consumer | `system-design-prompt.md — Project information`; `ADR-000` | Fact; MVP order and Synapse evidence pending | Stages 02, 03, 16, 20 |
| RT-01-003 | Platform-neutral core with independent capability ownership | `ark-assumptions.md — Product and architecture`; `Integration and contracts` | Approved baseline; owners/adapters pending | Stages 02–07 |
| RT-01-004 | Push-first versioned data lake with readiness separate from capability eligibility | `ark-assumptions.md — Ingestion and the ARK data lake`; `Integration and contracts` | Approved baseline; semantics/policies pending | Stages 03, 05, 06 |
| RT-01-005 | Durable shared job lifecycle and explicit execution modes | `ark-assumptions.md — Execution, orchestration, and proactive operation` | Approved baseline; SLO/use-case mapping pending | Stages 05, 07–09, 22 |
| RT-01-006 | Strict tenant isolation, minimal PII, policy before action | `ark-assumptions.md — Security, ownership, and operations` | Approved baseline; IAM/legal/grant semantics pending | Stages 07, 09, 12, 13 |
| RT-01-007 | No invented scale, SLO, availability, deployment, team, budget, or deadline | `system-design-prompt.md — Working rules` | Preserved as explicit unknowns | Stages 02, 04, 13–17, 20 |
| RT-01-008 | Avoid unjustified microservices/infrastructure/agents | `system-design-prompt.md — Working rules` | Preserved; choices postponed | Stages 04, 08–11, 15, 17, 23 |

## Completion-gate evidence

| Gate item | Result |
|---|---|
| Project-information facts restated without changing status | Pass |
| Every Working-rules requirement addressed | Pass |
| One organized question batch covers all eight required groups | Pass |
| Every question has options, a temporary assumption, effect, risk, and expiry | Pass |
| Decisions needed now versus can wait are explicit | Pass |
| Contradictions and dangerous assumptions are visible | Pass |
| Traceability updated and downstream inputs listed | Pass |
| No later-stage architecture/product decision smuggled in | Pass |
| User approved the requirements baseline, answered questions, or authorized temporary assumptions | Pass — `decisions/ADR-001-stage-01-requirements-baseline.md — Decision` |

Stage 01 is `APPROVED`. `STATUS.md` advances to Stage 02; Stage 02 is not executed in this update.

## Downstream consequences

- Stage 02 may define the system boundary and success criteria using this approved baseline.
- Any authorized temporary assumption remains explicitly reversible and may make later stage outputs conditional.
- Stage 03 must reapply the evidence gate to incomplete Synapse contracts and distinguish intended from implemented behavior for Churn, RFM, NPT, and REC.
- Unknown numeric scale/SLO/availability values prohibit irreversible infrastructure, capacity, and purchase commitments.
- New user answers must be recorded in `decisions/` and must supersede conflicting temporary assumptions explicitly.

## Exact next-stage inputs

Stage 02 must read:

- `stages/02-system-definition.md`.
- The approved `outputs/stages/01-discovery-and-questions.md`.
- `decisions/ADR-001-stage-01-requirements-baseline.md`.
- `outputs/stages/00-source-audit.md` and `decisions/ADR-000-temporary-source-evidence-disposition.md`.
- `sources/normalized/system-design-prompt.md — 1. System definition`.
- `sources/normalized/ark-assumptions.md` in full.
