# ARK system design — ADR-017/018 publication revision

Status: `POST-PUBLICATION REVISION — ADR-017/018 ACCEPTED; INDEPENDENT RE-ASSURANCE PENDING`

This document assembles the approved ARK architecture through Stage 23, the original Stage 24 assurance, and the sponsor-approved ADR-017/018 revisions. Those changes have not yet received an independent re-assurance pass. This is not a production-readiness statement. All recorded admission blocks remain active.

## 1. Decision authority and evidence boundary

- The human ARK sponsor is the architecture decision-maker.
- AI may analyze, draft, implement and test but has no authority to approve its own work, clear a block, promote a model, authorize an effect, or admit production.
- ADR-016 assigns the sponsor accountability only for the non-production roadmap and Phase 1 scope, contracts, implementation review and test-evidence acceptance.
- Named data/source, scientific, security/governance, integration/cutover, release and production-operations authorities remain unassigned and fail closed at their first applicable Phase 2/3 decisions.
- Repository sources, accepted ADRs, approved stage outputs and `STATUS.md` are authoritative over conversation memory.

## 2. System purpose and boundary

ARK is a tenant-aware capability platform behind consumer systems. It ingests versioned source data, preserves raw evidence, publishes governed immutable dataset versions, executes seven independently owned capability families through common contracts, records results and operational evidence, and conditionally supports scheduled, proactive and external-delivery paths.

The seven capability families are Churn, RFM, Next Purchase Prediction, Recommendation, Synapse Chat, Synapse Message and Synapse Campaign Verifier. Their presence in the product inventory is not production admission:

- `CAP-CHURN`, `CAP-RFM`, `CAP-NPT`, `CAP-REC`: `MIGRATION_BLOCKED`.
- `CAP-SYN-CHAT`, `CAP-SYN-MSG`, `CAP-SYN-VERIFY`: `EVIDENCE_BLOCKED`.

Source platforms retain master-data authority. Consumer-specific translation remains outside capability cores. LAB is an evidence consumer, not implicit promotion authority. ARK does not own probabilistic identity resolution, customer-facing presentation, campaign sending, an arbitrary workflow language, or autonomous agents.

### Account, organization, and business hierarchy

ADR-017 adds the product hierarchy `account → organization membership → organization → business`:

- A person registers an ARK account profile containing at least full name and phone number. The remaining registration fields, verification, credential, recovery, and identity-provider rules are unresolved; production trust remains blocked.
- One account may own one or more organizations. The product term **organization owner** is not an ARK module owner, architecture sponsor, or production-admission authority.
- An organization is the administrative and capability-entitlement container. A business belongs to one organization and is the tenant/data-isolation unit; its opaque `business_id` is the effective `tenant_id` for business data, jobs, models, results, objects, events, usage, and evidence.
- Each organization has one versioned capability pattern. The same enabled capability allowlist applies to every current and future business in the organization, with no per-business exception initially.
- The active `admin` role is organization-scoped. An admin can access all businesses in its organization and can change the capability pattern. Each data/execution operation still derives and authorizes exactly one business tenant; cross-business aggregation/export requires a separate typed contract.
- `viewer` and `tester` are reserved but inactive until their exact permissions and tests are approved. Admin-managed admin membership, ownership transfer, business transfer, and complete account-profile rules remain open.

For the canonical example, Andrew owns the Direct organization, which represents an SMS marketing platform with approximately 1,000 business tenants. One Direct pattern such as `{RFM, Churn}` governs them all; a Direct admin may later change it to `{RFM, Churn, REC}`. Pattern enablement never clears a capability's migration, evidence, data, security, environment, or production-admission block.

### Shared owner billing account and organization credit policies

ADR-018 adds a commercial payer hierarchy without changing business tenancy:

- One stable owner/customer billing account holds the shared credit balance for multiple organizations. Credits do not belong to organizations or businesses, and ARK creates no organization subwallets or credit-transfer workflow.
- Each organization references the shared billing account and receives one effective, versioned `OrganizationCreditPolicy` with optional monthly, daily, and per-job ceilings, hard-limit and warning behavior, and an effective interval.
- An explicit `NULL` ceiling means no organization-specific ceiling for that dimension; it never means a missing policy and never bypasses the owner balance. Zero remains a zero ceiling.
- Credits flow `owner billing account → organization policy → business tenant usage → capability/operation → job`. Every debit traces the billing account, organization, business, capability, job, stable usage event, pricing version, and amount.
- Both financial checks must pass: the organization policy must permit consumption and the shared owner account must have sufficient available credits. Neither check replaces authorization, capability-pattern, dataset-readiness, scientific-eligibility, model, policy, or production-admission gates.
- ARK reserves credits atomically with durable job acceptance, then settles actual priced usage exactly once or releases unused reservation. Retries/replays cannot double-charge; adjustments/refunds are linked append-only entries rather than edits to settled history.
- Only an authorized owner/customer billing administrator may change credit policies or balances initially. Organization-wide `admin` authority from ADR-017 does not imply billing mutation authority.

The example 500,000-credit billing account may serve Organization A (`100,000/month`), Organization B (`250,000/month`), and Organization C (no organization-specific ceiling), while all three still contend for the same shared available balance. Exact pricing, funding, expiry, refund, window/time-zone, partial-failure, and accounting rules remain unresolved and production charging is `CREDIT_BILLING_ADMISSION_BLOCKED`.

## 3. Binding architecture baseline

ARK begins as a boundary-enforced, microservice-ready modular monolith:

- one Python codebase and coordinated immutable release;
- typed in-process module ports and REST/JSON external contracts;
- shared PostgreSQL infrastructure with module-owned schemas, migrations and writers;
- provider-neutral immutable object-storage contract for large raw, curated, result and artifact content;
- PostgreSQL-first durable jobs with attempts, leases, fencing, cancellation, idempotency and reconciliation;
- separate role entrypoints rather than one deployment per module;
- principal-and-membership-derived organization scope plus one derived business tenant context propagated to every business-bearing asset;
- immutable dataset, feature, model, policy, job, result, audit and release identities;
- polling as the universal asynchronous result path;
- conditional events, webhooks and named workflows only after their named gates pass;
- deterministic rules, typed workflows and bounded ML/LLM operations; no agent runtime.

The provisional implementation target is Python, PostgreSQL and one Linux server, operated by the sponsor with AI assistance and no assumed 24/7 team. Containers remain optional; Kubernetes is not selected. This target is a characterization/validation baseline, not a production fitness or availability claim.

## 4. Runtime roles and actual first placement

| Role | Target responsibility | Phase 1 placement |
|---|---|---|
| `api` | Edge, trusted context adapter, control/query ports, sync-eligible calls, submit/poll/result and health | Active in validation |
| `worker-general` | Fenced claims and bounded general/data/fixture handlers | Active in validation |
| `scheduler` | Versioned schedule occurrences and typed job submission only | Absent until a scheduled operation is selected |
| `worker-data` | Resource-isolated ingestion/validation/backfill | Logical handlers co-hosted initially; split only on evidence |
| `worker-ml` | Resource-isolated training/evaluation/batch inference | Absent for blocked profiles; split only on evidence |
| `publisher-delivery` | Conditional outbox/event/webhook processing | Absent and blocked |
| `workflow-coordinator` | Conditional deterministic parent/child graph | Absent; no named workflow |
| `maintenance-migration` | Explicit migrations, reconciliation, restore and local synthetic reset | One-shot validation entrypoint; production privileged use blocked |
| `developer-tools` | Fixtures, schema/contract tools | Local only; excluded from production runtime |

Phase 1 therefore contains only `api`, `worker-general` and one-shot maintenance/developer entrypoints against real PostgreSQL and behavior-compatible object storage, with synthetic multi-organization/multi-business fixtures and a deterministic `POA_FIXTURE_ONLY` REC-shaped handler.

## 5. Authoritative data and execution model

### Data acceptance

The data chain has four separate authorities:

1. structural validity;
2. semantic validity;
3. immutable dataset readiness publication;
4. capability-owned scientific eligibility.

The organization capability pattern, platform entitlement, quota, grant, purpose, organization credit policy, shared owner balance/reservation, and runtime admission are separate non-data control decisions. A capability must appear in the effective organization pattern and pass every other admission gate. Raw evidence is committed before parsing. Candidate objects are undiscoverable until catalog publication. Corrections and backfills create new versions; they never mutate published history.

### Durable execution

The job manager owns logical jobs, attempts, state transitions, leases, fences, idempotency, cancellation and terminal truth. Workers execute exact public handlers but do not own lifecycle state. The critical success order is:

`authorized command → pattern/data/science admission → organization-credit-policy check + owner-balance check → atomic credit reservation + durable job commit → compatible fenced claim → execution-time authority/credit recheck where applicable → policy-applicable pre-effect audit → owner output commit → priced usage settlement/release → FINALIZING → required completion evidence linkage → SUCCEEDED`.

Attempts are at least once. Exactly one logical result/effect is pursued through stable identities, unique constraints, fencing and reconciliation; there is no end-to-end exactly-once execution claim. Delivery retry never reruns capability computation. An ambiguous external effect is reconciled before retry.

### Model lifecycle

Training where applicable, evaluation, registration, promotion and deployment assignment are distinct. Deterministic `NO_TRAINING` and external/provider-hosted `EXTERNAL_NOT_APPLICABLE` profiles do not invent ARK training. Inference never trains, refits, promotes or chooses `latest`. Exact assignment and authorization precede direct load or optional cache access. Cached loading remains `MODEL_CACHE_BLOCKED`. Rollback creates a new compatible assignment for future selection and never rewrites past results.

### Proactive and delivery

Proactive work follows `trigger → Phase A → evaluation job → immutable insight → Phase B → typed intent → execution-time recheck → optional effect`. A verifier or model output is advisory and cannot authorize action. Polling/result truth remains separate from event or webhook delivery state.

## 6. Security, reliability and evidence invariants

- Organization authority derives from the authenticated principal plus a stored active membership. Business tenant identity is then derived from that organization scope plus the stored business parent; body/query/path values never establish authority.
- Organization-wide admin authority permits administration of every member business but never creates an unscoped cross-business data operation. Jobs and capability work remain bound to exactly one business tenant.
- Capability-pattern mutations are versioned, idempotent, optimistic-concurrency protected, and audited. The effective pattern version is pinned to new work and rechecked before execution.
- Caller fields never select the payer, billing account, credit policy, pricing version, or debit amount. Stored business→organization→billing relationships and immutable pricing/policy versions determine them.
- Active reservations count against both shared owner available balance and applicable organization headroom. Ledger/reservation unavailability, insufficient balance, or hard-policy denial fails closed before executable work.
- Financial retries are idempotent by stable reservation and `usage_event_id`; every settlement is attributable and append-only, and organization policy is never represented as a balance.
- Owner-module authorization applies equally to HTTP, in-process, job, object, model, telemetry and recovery paths.
- Rows, objects, datasets, capability state/results, artifacts/cache, jobs, events, secrets, audit, telemetry, usage, exports and LAB evidence remain tenant/purpose scoped.
- Required pre-effect and completion audit evidence is authoritative; diagnostic logs/metrics/traces are supporting and normally buffered asynchronously.
- Owner output is committed before job finalization. A crash in `FINALIZING` retries evidence reconciliation, not science/computation.
- Restore requires a recovery epoch, stale-writer fencing and database↔object/model/audit/deletion/effect reconciliation before roles resume.
- No test, dashboard or successful local run alone clears an evidence, policy, ownership, environment or capacity block.

## 7. Active admission blocks

| Block | Effect |
|---|---|
| Four `MIGRATION_BLOCKED` profiles | No production Churn/RFM/NPT/REC output until exact remediation, evaluation, reproduction, assignment and authority gates pass |
| Three `EVIDENCE_BLOCKED` profiles | No Synapse execution beyond retained interface contracts until authoritative provider/model/prompt/state/safety/evaluation evidence passes |
| `EXTERNAL_TRUST_BLOCKED` | No production caller/workload trust profile |
| `DATA_GOVERNANCE_BLOCKED` | No production data onboarding without classification, purpose, consent, residency, retention, deletion and derived/model policy |
| `CRYPTO_SECRETS_BLOCKED` | No production key/secret mechanism or lifecycle admitted |
| `PRIVILEGED_ACTION_BLOCKED` | No production privileged mutation/recovery/promotion path |
| `EXTERNAL_DELIVERY_BLOCKED` | No webhook or external notification effect |
| `LLM_PROVIDER_BLOCKED` | No provider call or transfer |
| `SUPPLY_CHAIN_BLOCKED` | No production build/provenance/signing/revocation admission |
| `MODEL_CACHE_BLOCKED` | No cached artifact/model load until tenant/capability/purpose/assignment isolation passes |
| `DEPLOYMENT_ENVIRONMENT_BLOCKED` | No concrete production hosting/topology/readiness claim |
| `CAPACITY_ADMISSION_BLOCKED` | No release/profile production sizing or target claim |
| `DATA_CONTRACT_ADMISSION_BLOCKED` | No synthetic/temporary schema becomes a production source/canonical contract |
| `CONSUMER_CUTOVER_BLOCKED` | No legacy/customer migration or cutover |
| `CREDIT_BILLING_ADMISSION_BLOCKED` | No production credit debit until pricing, funding/expiry/refund, policy-window, failure/cancellation, reconciliation/accounting, authority, and concurrency/recovery evidence is approved |

## 8. Stage 23 anti-overengineering classification — included logical elements

“Required now” means required as a logical responsibility/contract for the Phase 1 architecture, not a separately deployed service or purchased product.

**Ownership-capacity rule:** under ADR-016, the sponsor can own/review only the bounded non-production Phase 1 implementation with AI assistance. AI is never accountable capacity. No named current capacity exists for real source/data contracts, capability science, production trust/security/secrets, external delivery, named workflows, release, production observability/operations, extracted services, infrastructure fleets or purchased platforms. Any element needing those authorities remains inactive even if its logical interface is present.

The active admission blocks are required-now negative control states, not software components, runtime roles or deployables. Their implementation is the fail-closed state/decision/test contract in the owning module; clearing one requires its recorded evidence and authority and does not add or activate a platform product.

| Element | Concrete requirement | Needed now? | Simpler outcome | Operational burden | Current ownership capacity | Class | Measurable later trigger |
|---|---|---|---|---|---|---|---|
| `C05-01` Consumer adapter boundary | Keep consumer schemas out of capability cores | Yes, as an external boundary | Phase 1 test client; no ARK adapter service | Consumer mapping and cutover coordination | Sponsor can review test client only | required now | Concrete consumer/cutover contract plus integration owner |
| `C05-02` Logical edge/API | Versioned transport, correlation and routing | Yes | Controllers/middleware inside `api` | Route compatibility, limits and ingress security | Sponsor can review bounded non-production surface | required now | Product only for mandated ingress/security or measured edge scale |
| `C05-03` Auth and tenant context | Principal + stored membership derive organization scope; stored parent derives one business tenant and delegated identity | Yes, as a contract | Test-only trust/membership adapter | Identity integration, membership revocation and secret operations | Test adapter only; production owner absent | required now | Concrete provider after trust evidence and named security owner |
| `C05-04` Control/eligibility/policy | Account/organization/membership/business registry, uniform capability pattern, shared owner billing account, organization credit policies/reservations, entitlement, grant, quota and fail-closed decisions | Yes | Owned PostgreSQL records and typed ports | Membership/pattern/credit lifecycle, shared-balance contention, races, audit and administration | Sponsor can review Phase 1 fixture rules | required now | Policy/billing product only after measured rule/admin burden or mandated accounting/provider evidence |
| `C05-05` Capability/job API | Common bounded envelope and durable lifecycle | Yes | Shared API namespace over typed ports | Schema compatibility and idempotency | Sponsor can review Phase 1 contract | required now | Network separation only after ADR-003 extraction trigger |
| `C05-06` Ingestion/validation/publication | Raw-first immutable data lifecycle | Yes for synthetic fixture | Bounded push/reference handlers | Validation, quarantine, lineage, correction and storage | Fixture only; real data authority absent | required now | Real activation needs ADR-011 evidence/owner; streaming/lake product needs measured source/freshness/volume gap |
| `C05-07` Dataset catalog/readiness | Separate readiness authority and lineage | Yes for fixture | PostgreSQL metadata plus object refs | Version, retention, correction and publication recovery | Fixture only; production governance owner absent | required now | Standalone catalog only after governance/scale gap and owner |
| `C05-08` PostgreSQL job manager | Durable acceptance/retry/cancel/result truth | Yes | PostgreSQL claims, no broker | Lease/fence/recovery/backpressure and DB operations | Sponsor can operate bounded validation lane only | required now | Broker assists wake-up only after measured dispatch gap and owner |
| `C05-09` Scheduler | Create deterministic occurrences for scheduled work | No Phase 1 schedule exists | Same-release loop and occurrence table | Calendar semantics, misfire recovery and on-call ownership | No named schedule owner | useful soon | Selected scheduled operation, approved profile and owner |
| `C05-10` Worker runtime | Run long/retryable work outside requests | Yes | One `worker-general` role | Supervision, cancellation, resource bounds and recovery | Sponsor can operate bounded validation worker | required now | Split roles only on measured dependency/resource/isolation need |
| `C05-11a` Seven capability definitions/contracts | Preserve complete product scope | Yes as design contracts, not implementations | Versioned definitions only | Contract maintenance and evidence tracking | Sponsor can accept contracts; science remains unowned | required now | No later-add trigger; implementations are separate row |
| `C05-11b` Deterministic fixture capability port | Exercise boundaries without invented science | Yes | One `POA_FIXTURE_ONLY` handler | Fixture isolation and risk of misuse | Sponsor can review bounded fixture | required now | Replace only after one profile’s scope/evidence gate |
| `C05-11c` Real capability implementations | Deliver selected business capability | No current profile is admitted | Implement one selected module, not seven | Data/science/provider/security/evaluation/operations | Required authorities are unassigned | useful soon | Sponsor-selected slice plus exact profile evidence and named owners |
| `C05-12a` Polling result delivery | Universal async recovery and truth | Yes | Job/result endpoints in `api` | Retention, access control and client polling load | Within bounded Phase 1 capacity | required now | Removal only through superseding consumer contract/ADR |
| `C05-12b` Webhook notification | Optional consumer push | No named admitted receiver | Polling | Destination/secret/egress/retry/ambiguity/on-call | Security/integration/operations owners absent | useful soon | Named consumer and owner plus ADR-008 delivery exit |
| `C05-13` Operational PostgreSQL | Durable operational/catalog/job/evidence state | Yes | One cluster with owned schemas | Migrations, backup, tuning, recovery and isolation | Validation operation only; production owner absent | required now | Split DB only after extraction/isolation/scale evidence |
| `C05-14` Object-storage contract | Large immutable raw/result/artifact refs | Yes | Behavior-compatible object interface | Lifecycle, deletion, consistency, backup and capacity | Test adapter only; production owner/product unknown | required now | Additional data-lake product only on governed query/retention/scale evidence |
| `C05-15` Capability feature/result/state namespaces | Preserve owner/version boundaries | Yes | Owned PostgreSQL/object namespaces | Schema/version/retention/recovery per capability | Fixture namespace within sponsor review | required now | Standalone feature product only on shared online reuse/skew/latency gap |
| `C05-16a` Minimal artifact/release identity | Reproducible build and fixture evidence | Yes | Release manifest and immutable refs | Digest/provenance/compatibility retention | Within Phase 1 review capacity | required now | No later-add trigger; richer registry is separate row |
| `C05-16b` Logical model/artifact registry | Promotion and exact assignment for admitted models | No model slice is admitted | Owned metadata/object refs, no product | Scientific governance, revocation, serving and release operations | Required owners absent | useful soon | First admitted model-backed slice with named owners |
| `C05-17` Secret/config delivery interface | Keep secrets out of code and requests | Yes as interface | Test config adapter | Rotation, access, audit and incident response | Test config only; production security/operations absent | required now | Production mechanism after environment evidence and named owner |
| `C05-18` Audit/lineage/usage/credit ledger | Authoritative evidence, metering, reservation and charge attribution | Yes | Append-oriented PostgreSQL records/object refs and reconstructable balance projections | Financial idempotency, fail-closed availability, retention, access and reconciliation | Bounded synthetic evidence within sponsor review | required now | Dedicated ledger/billing product only on accounting/provider/scale/independence evidence |
| `C05-19` Observability interfaces | Correlation, diagnosis and truthful health | Yes minimally | Structured signals and exporter seam | Cardinality, redaction, retention, alert and on-call | Minimal validation signals only | required now | Richer backend/signals after approved objectives/environment and owner |
| `C05-20` Admin/operations interfaces | Organization-wide business/pattern administration, owner billing-policy/ledger/reconciliation operations, and safe migrate/inspect | Yes for validation | Narrow API/CLI and one-shot role | Separated organization-vs-billing privilege, step-up, ETag/idempotency, audit and runbooks | Sponsor can use synthetic non-production commands only | required now | Production privilege/charging needs ADR-008/018 exits and named operations/billing owners |
| `C05-21` Reliable publication/outbox | Avoid losing promised facts/delivery intents | No promise/subscriber exists | Direct owner truth plus polling | Outbox cleanup, retries, replay and subscriber support | Integration/operations owners absent | useful soon | Named promised fact/delivery subscriber and owner |
| `C05-22` Named workflow coordinator | Recover a specific multi-step graph | No named graph exists | Direct call or explicit parent/child jobs | Graph compatibility, compensation and recovery | Workflow owner absent | optional | Approved named graph whose recovery cannot fit direct/simple job composition |

No included element is justified as an independently deployed microservice in Phase 1. The first runtime has three process classes, not 22 services.

## 9. Stage 23 anti-overengineering classification — deferred or rejected mechanisms

For every row below, current named operating capacity is absent unless the mechanism is explicitly a reversible sponsor-reviewed Phase 1 implementation choice. AI does not supply that capacity. Each remains absent until both its measurable trigger and accountable owner/runbook exist.

| Mechanism | Concrete requirement now? | Simpler outcome | Operational burden | Current capacity | Class | Measurable later trigger |
|---|---|---|---|---|---|---|
| Load balancer / API replicas | None | One logical ingress | Health routing, rollout and multi-instance diagnosis | Absent | scale-triggered | Measured replica/availability/ingress need |
| Event broker/backbone | None | PostgreSQL jobs and conditional outbox | Cluster, partitions, schemas, replay and on-call | Absent | scale-triggered | Approved fan-out/replay/claim-latency gap after tuning |
| Streaming/CDC | None | Push/reference/micro-batch/schedule | Offsets, ordering, backfill, source coordination and recovery | Absent | scale-triggered | Authoritative source plus measured freshness/volume/watermark need |
| SSE | None | Polling; conditional webhook | Connection fleet, resume and proxy behavior | Absent | optional | Approved interactive progress requirement and connection evidence |
| Separate gateway product | None | Logical edge middleware | Product policy, deployment, upgrades and incident response | Absent | optional | Mandated ingress/WAF/routing gap |
| Service registry/discovery | None | Static same-release configuration | Registration, health, convergence and outage mode | Absent | unjustified | Independently deployed dynamic service estate |
| Shared cache tier | None | Direct indexed reads and bounded local caches | Eviction, invalidation, tenant isolation and recovery | Absent | scale-triggered | Persistent measured bottleneck plus safe identity/invalidation contract |
| Standalone feature store | None | Capability-owned versioned features | Online/offline sync, serving, registry and governance | Absent | unjustified | Governed shared online reuse/skew/latency requirement |
| Standalone model registry/MLOps suite | None | Logical registry/jobs/evidence | Product operation, migration, integration and lock-in | Absent | optional | Proven lifecycle/scale control gap uniquely met by product |
| Generic workflow engine | None | Explicit parent/child state for named graphs | New state machine, workers, history, upgrades and recovery | Absent | scale-triggered | Approved timer/signal/compensation/graph load makes simple coordinator unsafe |
| Microservice/service-per-capability | None | Enforced modules and role entrypoints | Network failures, deployment fleet, contracts and on-call | Absent | unjustified | ADR-003 measured owner/scale/hardware/security trigger per extraction |
| gRPC/service mesh | None | In-process ports and REST/JSON | IDL, proxies, certificates, tracing and compatibility | Absent | unjustified | Measured extracted RPC requirement and owner |
| Kubernetes/operators | None | Supervisor or simple optional containers | Cluster/security/network/upgrade/on-call expertise | Absent | unjustified | Measured fleet/placement/availability/policy need and staffed runbook |
| Permanent environment fleet | None | Local/shared validation and temporary evidence lanes | Cost, drift, patching, secrets and cleanup | Absent | unjustified | Named durable environment requirement and owner |
| GPU pool | None | CPU paths | Drivers, scheduling, utilization and model compatibility | Absent | scale-triggered | Repeatable performance/TCO gain after profile admission |
| Rust rewrite | None | Python baseline and profiling | Dual toolchains, migration, interoperability and expertise | Absent | scale-triggered | Measured Python limit not fixed simply plus approved migration/TCO |
| Additional lakehouse/warehouse | None | Object interface plus PostgreSQL metadata | Governance, catalogs, copies, compute and recovery | Absent | scale-triggered | Governed analytical/query/retention need unmet by current contract |
| Vector store/retrieval | None | No semantic retrieval path | Index lifecycle, tenant deletion, quality and capacity | Absent | unjustified | Governed corpus plus semantic quality/latency target |
| Agent runtime/memory/tools | None | Typed operations, rules, jobs and named workflows | Autonomy controls, tools, memory, evaluation, cost and security | Absent | unjustified | Full Stage 11 re-entry and explicit sponsor approval |
| MCP/A2A | None | Typed ports/REST/jobs | Protocol security, discovery, compatibility and operations | Absent | unjustified | Justified agent-tool or peer-agent relationship |
| Dedicated LLM/model gateway | None | Capability adapters and exact assignment/provider contract | Routing, policy, quota, observability and failure domain | Absent | optional | Multiple admitted workloads prove shared control/scale need |
| Managed-service/vendor purchase | None | Provider-neutral logical contracts | Procurement, privacy, lock-in, outage and exit management | Absent | optional | Concrete need, benchmark, security/recovery fit, TCO/exit and budget approval |
| Multi-region/active-active/autoscaling | None | One explicit failure domain and measured vertical/role ladder | Distributed consistency, failover, testing, cost and 24/7 operation | Absent | unjustified | Approved SLO/RPO/RTO/workload/team/budget evidence |

## 10. Roadmap and stopping points

1. **Phase 1 — proof of architecture:** synthetic async REC-shaped contract fixture through real PostgreSQL/object semantics. No production/scientific claim.
2. **Phase 2 — one sponsor-selected validation slice:** one consumer, source-contract family and capability operation after exact data/science/security/integration authorities and evidence exist.
3. **Phase 3 — production hardening/admission:** clear every applicable block independently, rehearse release/restore/recovery/runbooks and approve numeric profiles. This is the earliest point a production claim may be considered.
4. **Phase 4 — scale-driven change:** optimize code/query/batching first, then vertical sizing, role split, replicas or products only on measured triggers.
5. **Phase 5 — optional capabilities:** events/webhooks, proactive actions, named workflows, Synapse, streaming, vector or agent work only under their cumulative re-entry gates.

## 11. Top unresolved decisions

1. Phase 2 consumer, capability operation and business outcome.
2. Authoritative source/canonical contracts and stable identifiers.
3. Named data/source-contract authority.
4. Named capability-scientific/evaluation/promotion authority and thresholds.
5. Production trust, identity, network, TLS, secrets and privileged mechanisms.
6. Classification, consent/purpose, residency, retention, deletion and backup policy.
7. Production Linux/PostgreSQL/object/telemetry/backup/patching environment and runbooks.
8. Workload, latency, freshness, availability, completion, recovery, growth and cost targets.
9. Named security, integration, release and production-operations authorities and support scope.
10. LAB acceptance authority and business/scientific acceptance criteria.

## 12. Publication-set map

- `ARK-diagrams.md` — seven original required architecture diagrams, ADR-017 hierarchy and ADR-018 credit-flow diagrams, and status legend.
- `ARK-interface-contracts.md` — external/internal contracts, schemas and compatibility rules.
- `ARK-execution-flows.md` — runtime order and critical/supporting paths for eight original use cases plus ADR-017 organization-admin and ADR-018 credit-reservation flows.
- `ARK-implementation-roadmap.md` — phases, Phase 1 backlog, gates and postponements.
- `ARK-requirements-traceability.md` — requirement-to-design/test evidence and reverse trace.
- `ARK-architecture-decisions.md` — ADR-000 through ADR-018 and supersession state.
- `ARK-risks-and-open-questions.md` — active blocks, risks, questions, contradictions and re-entry decisions.

## 13. Non-technical executive summary

ARK will begin as one carefully divided Python system using PostgreSQL, not as a fleet of microservices. The first milestone uses only synthetic data to prove account/organization/business membership, organization-wide admin access, uniform capability-pattern enforcement, one shared owner credit pool with organization policy gates, fully attributed retry-safe reservation/settlement, cross-organization and cross-business isolation, traceable raw-to-dataset processing, recoverable background work, and duplicate-safe retry. It does not deploy a real recommendation model, payment processing, production billing, or any production AI capability.

Four detailed ML capabilities still require remediation and scientific approval; three Synapse capabilities lack authoritative provider and implementation evidence. Production identity, data policy, secrets, delivery, hosting, capacity and operating ownership are also unresolved and remain disabled. The sponsor can approve the bounded non-production milestone; AI can implement and test but cannot approve, promote or operate production by implication.

The design deliberately excludes Kubernetes, brokers, agents, feature-store products, microservices and other expensive infrastructure until measurements and named owners prove they are needed. This keeps Phase 1 understandable for one sponsor while preserving explicit seams for later evidence-driven growth.

## 14. Closing-deliverable and completeness references

The exact ten-item publication map and final completeness checklist are in `ARK-requirements-traceability.md — Ten closing deliverables map`; `— Publication completeness checklist`. Decisions required now and safely deferred are in `ARK-risks-and-open-questions.md — Decisions required now`; `— Decisions safely deferred`.

## 15. Source basis

This publication revision is assembled from approved Stages 00–23, the original completed Stage 24 baseline, accepted ADR-000 through ADR-018, and both 2026-08-15 sponsor-decision sources. Detailed historical contracts remain authoritative except where ADR-017/018 explicitly refine tenant, control, usage, and interface context. Independent re-assurance of the revised publication remains pending.

| Publication subject | Exact approved basis |
|---|---|
| Boundary, actors and outcomes | `outputs/stages/02-system-definition.md — System boundary`; `— Core use cases`; `— Success criteria` |
| Capabilities and blocked profiles | `outputs/stages/03-capability-inventory.md — Capability inventory`; `outputs/stages/10-mlops.md — Capability ML profiles and production-admission gates` |
| Style and logical components | `outputs/stages/04-architecture-style.md — Decisions`; `outputs/stages/05-end-to-end-architecture.md — Component inventory`; accepted ADR-003 |
| Data boundaries and acceptance | `outputs/stages/06-data-architecture.md — Data boundaries and invariants`; `— Four-layer acceptance model`; `— Zone and authoritative-writer matrix` |
| APIs and integrations | `outputs/stages/07-api-integration.md — External resource and operation surface`; `— Internal application-port contracts`; accepted ADR-004 |
| Jobs, orchestration and proactive action | `outputs/stages/08-execution-orchestration.md — Internal job state machine`; `outputs/stages/09-events-proactive-actions.md — Two-phase fail-closed decision order`; accepted ADR-005 and ADR-006 |
| ML lifecycle and no-agent result | `outputs/stages/10-mlops.md — Lifecycle principles and ownership boundary`; `— Capability ML profiles and production-admission gates`; `outputs/stages/11-agent-architecture.md — Decisions` |
| Security, reliability and observability | `outputs/stages/12-security-governance.md — Production security-admission register`; `outputs/stages/13-reliability.md — Reliability invariants`; `outputs/stages/14-observability-evaluation.md — Observability invariants` |
| Deployment, testing and capacity | `outputs/stages/15-deployment-infrastructure.md — Deployable runtime-role matrix`; `outputs/stages/16-testing.md — Release and block transition gates`; `outputs/stages/17-capacity-cost.md — Production capacity-admission record` |
| Effective decisions, roadmap and runtime | `outputs/stages/18-architecture-decisions.md — Complete ADR register`; `— Supersession and refinement register`; `outputs/stages/20-roadmap.md — Roadmap at a glance`; `outputs/stages/22-runtime-execution-analysis.md — Runtime element usage and placement matrix` |
| Post-publication organization/business authorization refinement | `sources/sponsor-decisions/2026-08-15-owner-organization-business.md`; accepted ADR-017; revised final interface, execution, diagram, roadmap, traceability, and risk artifacts |
| Post-publication credit-management refinement | `sources/sponsor-decisions/2026-08-15-owner-billing-credit-management.md`; accepted ADR-018; revised control, interface, execution, diagram, roadmap, traceability, and risk artifacts |

Stage 24 independently assured the pre-ADR-017/018 source fidelity, consistency and implementability and reported no unresolved Critical, High, or material Medium defect after repairs. It does not constitute independent assurance of the post-publication revisions.
