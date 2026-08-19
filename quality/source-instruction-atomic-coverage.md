# Atomic source-instruction coverage register

This register is the literal Stage 24 mapping for every prescriptive item in `sources/normalized/system-design-prompt.md`. Each stable ID names one atomic instruction or one indivisible compound instruction. `Covered` means the cited artifact contains a concrete disposition; it does not clear any production-admission block.

Destination abbreviations expand to exact repository paths:

| Abbreviation | Exact path |
|---|---|
| `S02`–`S23` | `outputs/stages/{stage-number}-{stage-name}.md` as named in `outputs/stages/README.md` |
| `FSD` | `outputs/final/ARK-system-design.md` |
| `FIC` | `outputs/final/ARK-interface-contracts.md` |
| `FEF` | `outputs/final/ARK-execution-flows.md` |
| `FRM` | `outputs/final/ARK-implementation-roadmap.md` |
| `FRT` | `outputs/final/ARK-requirements-traceability.md` |
| `FRQ` | `outputs/final/ARK-risks-and-open-questions.md` |
| `FAD` | `outputs/final/ARK-architecture-decisions.md` |
| `FDG` | `outputs/final/ARK-diagrams.md` |

## Working rules and process order

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `WR-01` | Do not jump directly to a final diagram | `WORKFLOW.md — Stage sequence`; `S19 — Purpose and scope` | Covered |
| `WR-02` | Identify architecture-changing missing information first | `S01 — Open questions`; `FRQ — Top ten unresolved questions` | Covered |
| `WR-03` | Ask one organized question batch across business/data/ML/integration/scale/security/operations/team | `S01 — Organized question set` | Covered |
| `WR-04` | Distinguish facts | Every `S00`–`S24 — Facts` section | Covered |
| `WR-05` | Distinguish assumptions | Every `S00`–`S24 — Assumptions` section; `STATUS.md — Active assumptions` | Covered |
| `WR-06` | Distinguish recommendations | Every applicable stage `— Analysis and recommendations` | Covered |
| `WR-07` | Distinguish decisions requiring confirmation | Every stage `— Decisions` and `— Open questions`; `STATUS.md` | Covered |
| `WR-08` | Use labeled temporary assumptions when the sponsor cannot answer and state effect | `S01 — Assumptions`; `S18 — Temporary-assumption lifecycle register` | Covered |
| `WR-09` | Never invent scale, latency, security, or availability requirements | `S02 — Constraints`; `S17 — Facts`; `FRQ — Active production-admission blocks` | Covered |
| `WR-10` | Prefer the simplest safe architecture | `S04 — Starting-style recommendation`; `FSD — Binding architecture baseline` | Covered |
| `WR-11` | Do not assume microservices/Kubernetes/Kafka/mesh/feature store/vector DB/agent/MCP/A2A/streaming | `FSD — Stage 23 anti-overengineering classification — deferred or rejected mechanisms` | Covered |
| `WR-12` | Prove autonomy before calling an AI component an agent | `S11 — Candidate-by-candidate justification matrix`; `FAD — ADR-013` | Covered |
| `WR-13` | Otherwise use a deterministic or ML capability | `S11 — Decisions`; `FEF — UC-08 — Agentic workflow` | Covered |
| `WR-14` | Treat ML services as independently owned capabilities despite shared infrastructure | `S03 — Shared platform versus capability responsibility`; `S05 — Boundary map` | Covered |
| `WR-15` | Distinguish sync/async/scheduled/batch/event/continuous execution | `S08 — Execution-mode classification`; `FEF — Activation and notation` | Covered |
| `WR-16` | Separate current architecture from future possibilities | `FSD — Binding architecture baseline`; `— Stage 23 anti-overengineering classification — deferred or rejected mechanisms` | Covered |
| `WR-17` | Major recommendation states requirement | Stage recommendation blocks `— Requirement/where`; `FRT — Forward trace` | Covered |
| `WR-18` | Major recommendation states why needed now | Stage recommendation blocks; `FSD — Stage 23 anti-overengineering classification — included logical elements` | Covered |
| `WR-19` | Major recommendation states simplest viable implementation | Stage recommendation blocks; `FSD — Simpler outcome` column | Covered |
| `WR-20` | Major recommendation gives an alternative | `S04 — Architecture-style comparison`; ADR alternative sections | Covered |
| `WR-21` | Major recommendation explains why alternative is not preferred | Stage recommendation blocks; ADR rationale/trade-offs | Covered |
| `WR-22` | Major recommendation gives reconsideration condition | `FAD — Effective ADR register`; `FSD — Measurable later trigger` columns | Covered |
| `WR-23` | Surface contradictions/dangerous assumptions | Every stage `— Contradictions and dangerous assumptions`; `FRQ` | Covered |
| `WR-24` | Use specific designs/interfaces/flows/examples, not textbook lists | `FIC`; `FEF`; `FDG` | Covered |
| `PROC-01` | Perform design in prescribed order after clarification | `WORKFLOW.md — Stage sequence`; `STATUS.md — Current stage` | Covered |

## 1. System definition

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `SYS-01` | Define business goals | `S02 — Business goals` | Covered |
| `SYS-02` | Define users and consuming systems | `S02 — Users and consuming systems` | Covered |
| `SYS-03` | Define system boundary | `S02 — System boundary`; `FDG — 1. System context` | Covered |
| `SYS-04` | Define inside/outside responsibilities | `S02 — System boundary` | Covered |
| `SYS-05` | Define core use cases | `S02 — Core use cases` | Covered |
| `SYS-06` | Define out-of-scope capabilities | `S02 — Out of scope` | Covered |
| `SYS-07` | Define success criteria | `S02 — Success criteria` | Covered |
| `SYS-08` | Define functional requirements | `S02 — Functional requirements`; `FRT — Forward trace` | Covered |
| `SYS-09` | Define non-functional requirements | `S02 — Non-functional requirements`; `FRT — Forward trace` | Covered |
| `SYS-10` | Define constraints and assumptions | `S02 — Constraints`; `— Assumptions` | Covered |
| `SYS-11` | Trace each important requirement to its architecture element | `FRT — Forward trace`; `— Reverse trace from Phase 1 required elements` | Covered |

## 2. Capability and service inventory

All `CAP-*` rows apply separately to CAP-CHURN, CAP-RFM, CAP-NPT, CAP-REC, CAP-SYN-CHAT, CAP-SYN-MSG, and CAP-SYN-VERIFY.

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `CAP-01` | Name and purpose | `S03 — Capability contract — CAP-* / Identity and business purpose` | Covered |
| `CAP-02` | Business value | `S03 — Capability contract — CAP-* / Identity and business purpose` | Covered |
| `CAP-03` | Owner | `S03 — Capability contract — CAP-* / Ownership and dependencies`; `S10 — Registry, evaluation, and accountable promotion` | Covered; named authorities blocked |
| `CAP-04` | Input and output | `S03 — Capability contract — CAP-* / Input contracts`; `— Output contracts` | Covered |
| `CAP-05` | Input/output schemas | `S03 — Capability contract — CAP-* / Input contracts`; `— Output contracts` | Covered |
| `CAP-06` | Data requirements | `S03 — Capability contract — CAP-* / Data readiness and capability eligibility` | Covered |
| `CAP-07` | Invocation mode | `S03 — Capability contract — CAP-* / Operations and invocation` | Covered |
| `CAP-08` | Sync/async behavior | `S03 — Capability contract — CAP-* / Operations and invocation` | Covered |
| `CAP-09` | Expected latency | `S03 — Capability contract — CAP-* / Configuration, reliability, and operation`; `S17 — Per-capability workload model` | Covered; numeric objectives unknown |
| `CAP-10` | Dependencies | `S03 — Capability contract — CAP-* / Ownership and dependencies` | Covered |
| `CAP-11` | Preprocessing | `S03 — Capability contract — CAP-* / Processing and ML lifecycle` | Covered |
| `CAP-12` | Model or algorithm | `S03 — Capability contract — CAP-* / Processing and ML lifecycle`; `S10 — Capability ML profiles and production-admission gates` | Covered; evidence bounds preserved |
| `CAP-13` | Training requirements | `S03 — Capability contract — CAP-* / Processing and ML lifecycle`; `S10 — Training contract` | Covered |
| `CAP-14` | Inference workflow | `S03 — Capability contract — CAP-* / Processing and ML lifecycle`; `FEF — UC-01/UC-02` | Covered |
| `CAP-15` | State owned | `S03 — Capability contract — CAP-* / Ownership and dependencies`; `S05 — Component specification — C05-15` | Covered |
| `CAP-16` | Storage owned | `S03 — Capability contract — CAP-* / Ownership and dependencies`; `S06 — Zone and authoritative-writer matrix` | Covered |
| `CAP-17` | Configuration and thresholds | `S03 — Capability contract — CAP-* / Configuration, reliability, and operation`; `S10 — Capability ML profiles and production-admission gates` | Covered; unknowns block activation |
| `CAP-18` | Model/version handling | `S10 — Deployment assignment, selection, and model loading`; `FIC — Compatibility and versioning` | Covered |
| `CAP-19` | Eligibility/readiness requirements | `S03 — Capability contract — CAP-* / Data readiness and capability eligibility`; `S06 — Four-layer acceptance model` | Covered |
| `CAP-20` | Fallback behavior | `S03 — Capability contract — CAP-* / Configuration, reliability, and operation`; `S13 — Critical-path failure matrices` | Covered |
| `CAP-21` | Failure modes | `S03 — Capability contract — CAP-* / Configuration, reliability, and operation`; `S13 — Critical-path failure matrices` | Covered |
| `CAP-22` | Evaluation metrics | `S03 — Capability contract — CAP-* / Gaps, assumptions, decisions, and acceptance tests`; `S10 — Capability ML profiles and production-admission gates` | Covered; required thresholds remain blocked |
| `CAP-23` | Monitoring signals | `S03 — Capability contract — CAP-* / Configuration, reliability, and operation`; `S14 — Component observability matrix` | Covered |
| `CAP-24` | Security/privacy | `S03 — Capability contract — CAP-* / Gaps, assumptions, decisions, and acceptance tests`; `S12 — Tenant-bearing asset control matrix` | Covered |
| `CAP-25` | Separate shared platform from capability-specific responsibility | `S03 — Shared platform versus capability responsibility`; `S05 — Boundary map` | Covered |

## 3. Architecture drivers and style

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `STYLE-01` | Evaluate modular monolith | `S04 — Architecture-style comparison` | Covered |
| `STYLE-02` | Evaluate microservices | `S04 — Architecture-style comparison` | Covered |
| `STYLE-03` | Evaluate service-oriented architecture | `S04 — Architecture-style comparison` | Covered |
| `STYLE-04` | Evaluate event-driven architecture | `S04 — Architecture-style comparison` | Covered |
| `STYLE-05` | Evaluate data-pipeline architecture | `S04 — Architecture-style comparison` | Covered |
| `STYLE-06` | Evaluate agentic architecture | `S04 — Architecture-style comparison`; `S11 — Decisions` | Covered |
| `STYLE-07` | Evaluate justified combinations | `S04 — Starting-style recommendation` | Covered |
| `STYLE-08` | Recommend one starting architecture | `S04 — Starting-style recommendation`; `FSD — Binding architecture baseline` | Covered |
| `STYLE-09` | Explain fit to scale/team/maturity | `S04 — Fit qualifications` | Covered |
| `STYLE-10` | Define module/ownership boundaries | `S04 — Logical module and ownership boundaries` | Covered |
| `STYLE-11` | State acceptable coupling | `S04 — Boundary principles / Acceptable coupling` | Covered |
| `STYLE-12` | State mandatory isolation | `S04 — Boundary principles / Mandatory isolation` | Covered |
| `STYLE-13` | State what is shared | `S04 — Boundary principles / Shared infrastructure` | Covered |
| `STYLE-14` | State what is forbidden to share | `S04 — Boundary principles / Forbidden sharing` | Covered |
| `STYLE-15` | Define service-extraction triggers | `S04 — Service-extraction gate`; ADR-003 | Covered |
| `STYLE-16` | Do not infer microservices from multiple ML capabilities | `S04 — R-04-01`; `FSD — Stage 23 anti-overengineering classification — deferred or rejected mechanisms` | Covered |

## 4. End-to-end architecture

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `E2E-01` | Consumer applications | `S05 — Component specification — C05-01`; `FDG — 1. System context` | Covered |
| `E2E-02` | Consumer adapters/anti-corruption layers | `S05 — Component specification — C05-01` | Covered |
| `E2E-03` | Load balancer | `S05 — Conditional and rejected expected components`; `FSD — deferred or rejected mechanisms` | Covered; not selected |
| `E2E-04` | API gateway | `S05 — Component specification — C05-02` | Covered as logical edge, no product |
| `E2E-05` | Authentication/authorization | `S05 — Component specification — C05-03`; `S12 — R-12-01` | Covered |
| `E2E-06` | Tenant identification | `S12 — Security invariants`; `FIC — Required headers and context` | Covered |
| `E2E-07` | Plans/entitlements/quotas/rate limits | `S05 — Component specification — C05-04`; `S07 — Rate limits, quotas, and timeouts` | Covered |
| `E2E-08` | Versioned capability APIs | `S05 — Component specification — C05-05`; `FIC — Public resource and operation surface` | Covered |
| `E2E-09` | Workflow/orchestration API | `S05 — Component specification — C05-22`; `S08 — Conditional named-workflow contract` | Covered; inactive |
| `E2E-10` | Data ingestion | `S05 — Component specification — C05-06`; `S06 — R-06-01` | Covered |
| `E2E-11` | Schema/semantic validation | `S06 — Four-layer acceptance model` | Covered |
| `E2E-12` | Dataset catalog | `S05 — Component specification — C05-07` | Covered |
| `E2E-13` | Data eligibility/capability readiness | `S06 — Four-layer acceptance model` | Covered |
| `E2E-14` | Job manager | `S05 — Component specification — C05-08`; `S08 — Internal job state machine` | Covered |
| `E2E-15` | Task queue/workers | `S05 — Component specification — C05-10`; `S08 — PostgreSQL task dispatch` | Covered; no broker queue |
| `E2E-16` | Scheduler | `S05 — Component specification — C05-09`; `FSD — included logical elements` | Covered; outside Phase 1 |
| `E2E-17` | Workflow orchestration | `S05 — Component specification — C05-22`; `S08 — Conditional named-workflow contract` | Covered; inactive |
| `E2E-18` | Event producers/consumers | `S09 — Internal reliable publication and broker disposition` | Covered; conditional |
| `E2E-19` | Event broker if justified | `S09 — Internal reliable publication and broker disposition`; `FSD — deferred or rejected mechanisms` | Covered; unjustified now |
| `E2E-20` | Notification delivery | `S05 — Component specification — C05-12`; `S09 — External delivery state and semantics` | Covered; blocked |
| `E2E-21` | Webhook/polling/SSE/other delivery | `S07 — Callback/webhook contract`; `FSD — included/deferred classifications` | Covered; polling baseline |
| `E2E-22` | Configuration/policy management | `S05 — Component specification — C05-04` | Covered |
| `E2E-23` | Service registry only if needed | `S05 — Conditional and rejected expected components`; `FSD — deferred or rejected mechanisms` | Covered; unjustified |
| `E2E-24` | Caching | `S12 — Tenant-bearing asset control matrix`; `FSD — deferred or rejected mechanisms` | Covered; bounded/local only |
| `E2E-25` | Operational databases | `S05 — Component specification — C05-13` | Covered |
| `E2E-26` | Object storage/data lake | `S05 — Component specification — C05-14`; `S06 — Zone and authoritative-writer matrix` | Covered; interface now, product deferred |
| `E2E-27` | Feature/state storage | `S05 — Component specification — C05-15` | Covered |
| `E2E-28` | Model registry | `S05 — Component specification — C05-16`; `S10 — Registry, evaluation, and accountable promotion` | Covered; minimal identity now, registry later |
| `E2E-29` | Secrets management | `S05 — Component specification — C05-17`; `S12 — Secrets and key-control contract` | Covered; production mechanism blocked |
| `E2E-30` | Audit logging | `S05 — Component specification — C05-18`; `S12 — Security audit contract` | Covered |
| `E2E-31` | Observability | `S05 — Component specification — C05-19`; `S14 — Observability invariants` | Covered |
| `E2E-32` | Admin/operational interfaces | `S05 — Component specification — C05-20` | Covered |
| `E2E-S01` | Component responsibility | Every `S05 — Component specification — C05-*` | Covered |
| `E2E-S02` | Why component exists | Every `S05 — Component specification — C05-*` | Covered |
| `E2E-S03` | Required in first version? | `FSD — included logical elements / Needed now?` | Covered |
| `E2E-S04` | Inputs/outputs | Every `S05 — Component specification — C05-*` | Covered |
| `E2E-S05` | State/data ownership | Every `S05 — Component specification — C05-*` | Covered |
| `E2E-S06` | Upstream/downstream dependencies | Every `S05 — Component specification — C05-*`; `S22 — Runtime element usage and placement matrix` | Covered |
| `E2E-S07` | Failure behavior | Every `S05 — Component specification — C05-*`; `S13 — Critical-path failure matrices` | Covered |
| `E2E-S08` | Retry/idempotency | Every `S05 — Component specification — C05-*`; `S08 — Retry and idempotency boundary` | Covered |
| `E2E-S09` | Scaling approach | Every `S05 — Component specification — C05-*`; `S17 — Scaling and purchase-decision ladder` | Covered |
| `E2E-S10` | Security controls | Every `S05 — Component specification — C05-*`; `S12 — Tenant-bearing asset control matrix` | Covered |
| `E2E-S11` | Monitoring signals | Every `S05 — Component specification — C05-*`; `S14 — Component observability matrix` | Covered |
| `E2E-S12` | Simplest implementation | Every `S05 — Component specification — C05-*`; `FSD — Simpler outcome` | Covered |
| `E2E-S13` | Explicitly disposition commonly expected unnecessary components | `S05 — Conditional and rejected expected components`; `FSD — deferred or rejected mechanisms` | Covered |

## 5. Data architecture

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `DATA-01` | Data-source integration | `S06 — R-06-01 — Integration-mode policy` | Covered |
| `DATA-02` | Push/pull/file/CDC/batch/streaming options | `S06 — R-06-01 — Integration-mode policy`; `— Anti-overengineering classification` | Covered |
| `DATA-03` | Canonical data contracts | `S06 — Source-registration and canonical contract envelope`; `— R-06-02` | Covered |
| `DATA-04` | Schema versioning | `S06 — Version and compatibility policy` | Covered |
| `DATA-05` | Technical validation | `S06 — Four-layer acceptance model` | Covered |
| `DATA-06` | Semantic validation | `S06 — Four-layer acceptance model` | Covered |
| `DATA-07` | Tenant isolation | `S06 — Tenant and access-isolation rules` | Covered |
| `DATA-08` | Raw/validated/processed/feature/prediction/audit data | `S06 — Zone and authoritative-writer matrix` | Covered |
| `DATA-09` | Storage ownership | `S06 — Zone and authoritative-writer matrix` | Covered |
| `DATA-10` | Retention/deletion | `S06 — Retention, correction, and deletion model` | Covered; policy values blocked |
| `DATA-11` | Lineage/provenance | `S06 — Lineage and provenance graph` | Covered |
| `DATA-12` | PII handling | `S06 — PII minimization and classification`; `S12 — R-12-03` | Covered |
| `DATA-13` | Encryption | `S06 — Encryption-control contract`; `S12 — Encryption and integrity controls` | Covered |
| `DATA-14` | Data-quality monitoring | `S06 — Data-quality monitoring and ownership`; `S14 — Data/model evaluation signals` | Covered |
| `DATA-15` | Backfill/reprocessing | `S06 — Backfill and reprocessing protocol` | Covered |
| `DATA-16` | Duplicate/late data | `S06 — Incremental changes, duplicates, corrections, and late data` | Covered |
| `DATA-17` | Separate structural validity | `S06 — Four-layer acceptance model` | Covered |
| `DATA-18` | Separate semantic validity | `S06 — Four-layer acceptance model` | Covered |
| `DATA-19` | Separate capability sufficiency | `S06 — Four-layer acceptance model` | Covered |
| `DATA-20` | Include example lifecycle | `S06 — Concrete data lifecycle — transaction file to recommendation result`; `FDG — 6. Data lifecycle` | Covered |

## 6. API and integration design

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `API-01` | External APIs | `S07 — External resource and operation surface`; `FIC — Public resource and operation surface` | Covered |
| `API-02` | Internal module/service contracts | `S07 — Internal application-port contracts`; `FIC — Internal public ports` | Covered |
| `API-03` | Endpoint responsibilities | `S07 — Endpoint contract matrix` | Covered |
| `API-04` | Request/response examples | `S07 — Operation request schema`; `— Standard synchronous response`; `FIC` | Covered |
| `API-05` | Sync versus async API | `S07 — Synchronous versus asynchronous decision rule` | Covered |
| `API-06` | Job submission/status APIs | `S07 — Concrete capability example — recommendation batch submission`; `— Job contract` | Covered |
| `API-07` | Pagination | `S07 — Cursor-pagination contract` | Covered |
| `API-08` | Idempotency keys | `S07 — Idempotency contract` | Covered |
| `API-09` | Correlation IDs | `S07 — Correlation and propagation contract` | Covered |
| `API-10` | Error model | `S07 — Error model`; `FIC — Error/problem contract` | Covered |
| `API-11` | API versioning | `S07 — Versioning and compatibility`; `FIC — Compatibility and versioning` | Covered |
| `API-12` | Rate limiting | `S07 — Rate limits, quotas, and timeouts` | Covered |
| `API-13` | Timeout behavior | `S07 — Rate limits, quotas, and timeouts`; `S08 — Timeout and deadline semantics` | Covered |
| `API-14` | Webhook/event contracts | `S07 — Callback/webhook contract`; `S09 — Versioned internal domain-event schema example` | Covered |
| `API-15` | Authentication/authorization | `S07 — Common headers and operational envelope`; `S12 — R-12-01` | Covered |
| `API-16` | Tenant-context propagation | `S07 — Correlation and propagation contract`; `S12 — Workload identity and delegated execution` | Covered |
| `API-17` | Evaluate unified capability API | `S07 — API shape decision` | Covered |
| `API-18` | Evaluate separate per-capability APIs | `S07 — API shape decision` | Covered |
| `API-19` | Evaluate workflow API | `S07 — API shape decision`; `S08 — Conditional named-workflow contract` | Covered |
| `API-20` | Decide combination | `S07 — API shape decision`; ADR-004 | Covered |
| `API-21` | Provide example API/event schemas | `FIC — Common operation request`; `— Durable submission and job resource`; `— Event envelope and webhook delivery` | Covered |

## 7. Execution and orchestration

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `EXEC-01` | Immediate inference | `S08 — Synchronous execution`; `FEF — UC-01` | Covered; production profiles blocked |
| `EXEC-02` | Long-running inference | `S08 — Durable job execution`; `FEF — UC-02` | Covered |
| `EXEC-03` | Training jobs | `S08 — Durable job execution`; `FEF — UC-06` | Covered; blocked |
| `EXEC-04` | Scheduled execution | `S08 — Schedule contract and occurrence algorithm`; `FEF — UC-03` | Covered; inactive |
| `EXEC-05` | Batch execution | `S08 — Durable job execution`; `FEF — UC-02` | Covered |
| `EXEC-06` | Event-triggered execution | `S08 — Event-triggered submission`; `FEF — UC-04` | Covered; inactive |
| `EXEC-07` | Continuous processing if justified | `S08 — Execution-mode classification`; `FSD — deferred mechanisms / Streaming/CDC` | Covered; unjustified |
| `EXEC-08` | Multi-service workflows | `S08 — Conditional named-workflow contract`; `FEF — UC-07` | Covered; inactive |
| `EXEC-09` | Cancellation | `S08 — Cancellation semantics` | Covered |
| `EXEC-10` | Retries | `S08 — Retry and idempotency boundary` | Covered |
| `EXEC-11` | Timeout | `S08 — Timeout and deadline semantics` | Covered |
| `EXEC-12` | Partial failure | `S08 — Partial result and fallback semantics`; `S13 — Critical-path failure matrices` | Covered |
| `EXEC-13` | Compensation | `S08 — Conditional named-workflow contract`; `S13 — Recovery and reconciliation` | Covered |
| `EXEC-14` | Job prioritization | `S08 — Priority, fairness, concurrency, and backpressure` | Covered |
| `EXEC-15` | Concurrency limits | `S08 — Priority, fairness, concurrency, and backpressure` | Covered; values blocked |
| `EXEC-16` | Duplicate requests | `S08 — Retry and idempotency boundary` | Covered |
| `EXEC-17` | Exactly-once vs practical at-least-once | `S08 — Retry and idempotency boundary`; ADR-005 | Covered |
| `EXEC-R01` | Distinguish API gateway responsibility | `S08 — Responsibility separation` | Covered |
| `EXEC-R02` | Distinguish job manager responsibility | `S08 — Responsibility separation` | Covered |
| `EXEC-R03` | Distinguish scheduler responsibility | `S08 — Responsibility separation` | Covered |
| `EXEC-R04` | Distinguish queue responsibility | `S08 — Responsibility separation` | Covered |
| `EXEC-R05` | Distinguish worker responsibility | `S08 — Responsibility separation` | Covered |
| `EXEC-R06` | Distinguish workflow orchestrator responsibility | `S08 — Responsibility separation` | Covered |
| `EXEC-R07` | Distinguish event broker responsibility | `S08 — Responsibility separation` | Covered |
| `EXEC-R08` | Distinguish event handler responsibility | `S08 — Responsibility separation` | Covered |
| `EXEC-R09` | Distinguish notification delivery responsibility | `S08 — Responsibility separation`; `S09 — External delivery state and semantics` | Covered |
| `EXEC-R10` | Do not collapse responsibilities into a vague event system | `S08 — Responsibility separation`; `S09 — Event taxonomy and authority` | Covered |

## 8. Event and proactive-action architecture

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `EVT-01` | Evaluation trigger | `S09 — Evaluation-trigger contract` | Covered |
| `EVT-02` | Tenant schedules/permissions/thresholds/channels | `S09 — Subscription management and APIs`; `— Two-phase fail-closed decision order` | Covered |
| `EVT-03` | Output to domain event/actionable insight | `S09 — Insight/result/action/delivery authority`; `— Two-phase fail-closed decision order` | Covered |
| `EVT-04` | Event schema | `S09 — Versioned internal domain-event schema example`; `FIC — Event envelope and webhook delivery` | Covered |
| `EVT-05` | Event versioning | `S09 — Event schema/versioning rules` | Covered |
| `EVT-06` | Routing | `S09 — Routing and subscriber contract` | Covered |
| `EVT-07` | Subscription management | `S09 — Subscription management and APIs` | Covered |
| `EVT-08` | Webhook/other delivery | `S09 — Versioned external webhook schema example`; `— External delivery state and semantics` | Covered; blocked |
| `EVT-09` | Retries/exponential backoff | `S09 — External delivery state and semantics`; `S13 — CP-13-06` | Covered; numeric profile blocked |
| `EVT-10` | Dead-letter handling | `S09 — External delivery state and semantics`; `S13 — CP-13-06` | Covered |
| `EVT-11` | Deduplication | `S09 — Two-phase fail-closed decision order`; `— External delivery state and semantics` | Covered |
| `EVT-12` | Ordering | `S09 — Event schema/versioning rules`; `— External delivery state and semantics` | Covered |
| `EVT-13` | Expiration | `S09 — Versioned internal domain-event schema example`; `— External delivery state and semantics` | Covered |
| `EVT-14` | Throttling | `S09 — Two-phase fail-closed decision order`; `— External delivery state and semantics` | Covered |
| `EVT-15` | Acknowledgement | `S09 — External delivery state and semantics`; `S13 — CP-13-06` | Covered |
| `EVT-16` | Replay | `S09 — External delivery state and semantics`; `S13 — CP-13-06` | Covered |
| `EVT-17` | Audit history | `S09 — Audit and evidence contract`; `S14 — Critical-workflow observability matrix` | Covered |
| `EVT-T01` | Distinguish internal technical events | `S09 — Event taxonomy and authority` | Covered |
| `EVT-T02` | Distinguish business/domain events | `S09 — Event taxonomy and authority` | Covered |
| `EVT-T03` | Distinguish commands | `S09 — Event taxonomy and authority` | Covered |
| `EVT-T04` | Distinguish notifications | `S09 — Event taxonomy and authority` | Covered |
| `EVT-T05` | Distinguish actionable ML insights | `S09 — Event taxonomy and authority` | Covered |

## 9. ML and MLOps

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `ML-01` | Experiment tracking | `S10 — Experiment and run records` | Covered |
| `ML-02` | Dataset versioning | `S10 — Lifecycle principles and ownership boundary`; `S06 — Version and compatibility policy` | Covered |
| `ML-03` | Feature definitions | `S10 — Feature definition and materialization contract` | Covered |
| `ML-04` | Training pipeline | `S10 — Training contract` | Covered |
| `ML-05` | Model evaluation | `S10 — Registry, evaluation, and accountable promotion` | Covered |
| `ML-06` | Approval/promotion | `S10 — Registry, evaluation, and accountable promotion` | Covered; authority blocked |
| `ML-07` | Model registry | `S10 — Registry, evaluation, and accountable promotion` | Covered |
| `ML-08` | Deployment strategy | `S10 — Deployment assignment, selection, and model loading` | Covered |
| `ML-09` | Online/batch inference | `S10 — Serving contracts`; `FEF — UC-01/UC-02` | Covered |
| `ML-10` | Model loading | `S10 — Deployment assignment, selection, and model loading`; `S12 — Model and artifact access` | Covered; cache blocked |
| `ML-11` | Model-version selection | `S10 — Deployment assignment, selection, and model loading` | Covered |
| `ML-12` | Shadow/canary | `S10 — Deployment, shadow, canary, and rollback` | Covered; conditional |
| `ML-13` | Rollback | `S10 — Deployment, shadow, canary, and rollback` | Covered |
| `ML-14` | Drift detection | `S10 — Monitoring, feedback, drift, and retraining` | Covered |
| `ML-15` | Data-quality monitoring | `S10 — Monitoring, feedback, drift, and retraining`; `S14 — Data/model evaluation signals` | Covered |
| `ML-16` | Performance monitoring | `S10 — Monitoring, feedback, drift, and retraining`; `S14 — SLI catalog and SLO-admission plan` | Covered |
| `ML-17` | Feedback collection | `S10 — Monitoring, feedback, drift, and retraining` | Covered |
| `ML-18` | Retraining triggers | `S10 — Monitoring, feedback, drift, and retraining` | Covered; never auto-promotes |
| `ML-19` | Explainability | `S10 — Capability ML profiles and production-admission gates` | Covered; evidence/criteria blocked |
| `ML-20` | Reproducibility | `S10 — Reproduction manifests and procedure` | Covered |
| `ML-21` | Fairness/safety where applicable | `S10 — Registry, evaluation, and accountable promotion`; `— Capability ML profiles and production-admission gates` | Covered; criteria blocked |
| `ML-22` | Decide whether full feature store is justified | `S10 — Anti-overengineering assessment`; `FSD — deferred mechanisms / Standalone feature store` | Covered; unjustified |
| `ML-23` | Preserve feature definitions/version/PIT/training-serving consistency without full store | `S10 — Feature definition and materialization contract` | Covered |

## 10. Agent architecture only if justified

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `AGT-01` | Agent goal | `S11 — Candidate-by-candidate justification matrix`; `— Future agent re-entry gate` | Covered; no agent selected |
| `AGT-02` | Reason it must be an agent | `S11 — Candidate-by-candidate justification matrix` | Covered; none justified |
| `AGT-03` | Tools | `S11 — Future agent re-entry gate` | Covered conditionally |
| `AGT-04` | Available context | `S11 — Future agent re-entry gate` | Covered conditionally |
| `AGT-05` | Memory/state | `S11 — Future agent re-entry gate` | Covered conditionally |
| `AGT-06` | Planning boundaries | `S11 — Future agent re-entry gate` | Covered conditionally |
| `AGT-07` | Permissions | `S11 — Future agent re-entry gate` | Covered conditionally |
| `AGT-08` | Human approval points | `S11 — Future agent re-entry gate` | Covered conditionally |
| `AGT-09` | Termination criteria | `S11 — Future agent re-entry gate` | Covered conditionally |
| `AGT-10` | Maximum steps/time/cost | `S11 — Future agent re-entry gate` | Covered conditionally |
| `AGT-11` | Output contract | `S11 — Future agent re-entry gate` | Covered conditionally |
| `AGT-12` | Evaluation | `S11 — Future agent re-entry gate`; `S16 — Agent evaluation disposition` | Covered conditionally |
| `AGT-13` | Observability | `S11 — Future agent re-entry gate` | Covered conditionally |
| `AGT-14` | Failure/fallback | `S11 — Future agent re-entry gate` | Covered conditionally |
| `AGT-15` | Injection/exfiltration controls | `S11 — Future agent re-entry gate`; `S12 — Bounded LLM/Synapse security gate` | Covered conditionally |
| `AGT-16` | Choose among REST/gRPC/events/MCP/A2A/other | `S11 — Interface disposition` | Covered |
| `AGT-17` | Do not add MCP/A2A without actual relationship | `S11 — Interface disposition`; `FSD — deferred mechanisms / MCP/A2A` | Covered |

## 11. Security, privacy, and governance

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `SEC-01` | Tenant isolation | `S12 — Tenant-bearing asset control matrix` | Covered |
| `SEC-02` | Identity/access management | `S12 — R-12-01 — Identity, authentication, and authorization contract` | Covered; production trust blocked |
| `SEC-03` | Service-to-service authentication | `S12 — Workload identity and delegated execution` | Covered; mechanism blocked |
| `SEC-04` | Least privilege | `S12 — Authorization and privilege-separation rules` | Covered |
| `SEC-05` | Secrets handling | `S12 — Secrets and key-control contract` | Covered; mechanism blocked |
| `SEC-06` | Encryption in transit/at rest | `S12 — Encryption and integrity controls` | Covered; profile blocked |
| `SEC-07` | PII protection | `S12 — Classification, minimization, and provider-transfer controls` | Covered |
| `SEC-08` | Data residency | `S12 — Residency and location-policy contract` | Covered; policy blocked |
| `SEC-09` | Auditability | `S12 — Security audit contract` | Covered |
| `SEC-10` | Consent/permission | `S12 — Purpose, consent, and action-authority controls` | Covered; policy blocked |
| `SEC-11` | Retention/deletion | `S12 — Lifecycle governance` | Covered; values blocked |
| `SEC-12` | Model access controls | `S12 — Model and artifact access`; ADR-008 | Covered; cache blocked |
| `SEC-13` | Prompt/tool agent security | `S12 — Bounded LLM/Synapse security gate`; `S11 — Future agent re-entry gate` | Covered conditionally |
| `SEC-14` | Abuse prevention | `S12 — R-12-05 — Abuse, confused-deputy, and egress prevention` | Covered |
| `SEC-15` | Dependency/supply-chain risks | `S12 — R-12-06 — Software, model, and build supply chain` | Covered; production profile blocked |
| `SEC-16` | Concise realistic threat model | `S12 — Threat model` | Covered |

## 12. Reliability and failure design

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `REL-01` | Analyze unavailable dependencies | `S13 — Critical-path failure matrices` | Covered |
| `REL-02` | Analyze invalid/incomplete datasets | `S13 — CP-13-03 — ingestion/publication`; `S16 — Data-quality test matrix` | Covered |
| `REL-03` | Analyze queue backlog | `S13 — Critical-path failure matrices`; `S08 — Priority, fairness, concurrency, and backpressure` | Covered |
| `REL-04` | Analyze worker crash | `S13 — CP-13-02 — durable job` | Covered |
| `REL-05` | Analyze duplicate execution | `S13 — CP-13-02 — durable job` | Covered |
| `REL-06` | Analyze partial workflow completion | `S13 — CP-13-08 — conditional workflow` | Covered |
| `REL-07` | Analyze stale cache | `S13 — Critical-path failure matrices`; `S12 — Model and artifact access` | Covered |
| `REL-08` | Analyze storage outage | `S13 — Critical-path failure matrices`; `— Required logical recovery order` | Covered |
| `REL-09` | Analyze unavailable model | `S13 — CP-13-04 — ML lifecycle`; `S10 — Capability ML profiles and production-admission gates` | Covered |
| `REL-10` | Analyze event-delivery failure | `S13 — CP-13-06 — event/delivery conditional` | Covered |
| `REL-11` | Analyze tenant misconfiguration | `S13 — CP-13-01/05/07`; `S12 — Security invariants` | Covered |
| `REL-12` | Analyze poison messages | `S13 — CP-13-06 — event/delivery conditional` | Covered |
| `REL-13` | Analyze schema incompatibility | `S13 — Critical-path failure matrices`; `S07 — Versioning and compatibility` | Covered |
| `REL-14` | Analyze agent loops/unsafe actions | `S13 — Agent-related failure disposition`; `S11 — Future agent re-entry gate` | Covered; N/A now |
| `REL-P01` | Specify timeouts | `S13 — Timeout and deadline contract` | Covered |
| `REL-P02` | Specify retries | `S13 — Retry and recovery policy` | Covered |
| `REL-P03` | Specify circuit breakers | `S13 — Reliability-pattern disposition` | Covered where justified |
| `REL-P04` | Specify idempotency | `S13 — Reliability invariants`; `S08 — Retry and idempotency boundary` | Covered |
| `REL-P05` | Specify dead-letter handling | `S13 — CP-13-06`; `S09 — External delivery state and semantics` | Covered conditionally |
| `REL-P06` | Specify graceful degradation | `S13 — Reliability-pattern disposition` | Covered |
| `REL-P07` | Specify fallback | `S13 — Critical-path failure matrices` | Covered |
| `REL-P08` | Specify recovery | `S13 — Required logical recovery order` | Covered |
| `REL-P09` | Specify reconciliation | `S13 — Required logical recovery order` | Covered |
| `REL-P10` | Specify disaster recovery | `S13 — Backup, restore, and disaster-recovery contract`; `S15 — Backup, restore, and disaster-recovery deployment contract` | Covered; objectives blocked |
| `REL-P11` | Apply patterns only when benefit exceeds complexity | `S13 — Reliability-pattern disposition`; `FSD — deferred mechanisms` | Covered |

## 13. Observability and evaluation

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `OBS-01` | Structured logs | `S14 — Common telemetry and evidence contract` | Covered |
| `OBS-02` | Metrics | `S14 — Common telemetry and evidence contract` | Covered |
| `OBS-03` | Traces | `S14 — Common telemetry and evidence contract` | Covered |
| `OBS-04` | Correlation across APIs/jobs/models/events | `S14 — Common telemetry and evidence contract`; `— Critical-workflow observability matrix` | Covered |
| `OBS-05` | Health checks | `S14 — Health and readiness semantics` | Covered |
| `OBS-06` | Dashboards | `S14 — Dashboard disposition` | Covered; product deferred |
| `OBS-07` | Alerts | `S14 — Alert policy and conditions` | Covered; thresholds/owners blocked |
| `OBS-08` | Audit logs | `S14 — Audit versus telemetry`; `S12 — Security audit contract` | Covered |
| `OBS-09` | Per-tenant usage | `S14 — Per-tenant usage and cost contract` | Covered |
| `OBS-10` | Model-quality metrics | `S14 — Data/model evaluation signals` | Covered |
| `OBS-11` | Data-quality metrics | `S14 — Data/model evaluation signals` | Covered |
| `OBS-12` | Cost metrics | `S14 — Per-tenant usage and cost contract` | Covered |
| `OBS-13` | Agent execution traces if applicable | `S14 — Agent evaluation disposition`; `S11 — Future agent re-entry gate` | Covered; N/A now |
| `OBS-14` | Specify key SLIs | `S14 — SLI catalog and SLO-admission plan` | Covered |
| `OBS-15` | Propose SLOs only with sufficient evidence | `S14 — SLI catalog and SLO-admission plan`; `S17 — Facts` | Covered; no invented SLOs |

## 14. Deployment and infrastructure

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `DEP-01` | Recommend simplest adequate deployment | `S15 — Conditional starting deployment`; ADR-009 | Covered |
| `DEP-02` | Environments | `S15 — Environment model` | Covered |
| `DEP-03` | Configuration | `S15 — Configuration contract` | Covered |
| `DEP-04` | Containers | `S15 — Process supervision and optional containers` | Covered; optional |
| `DEP-05` | CI/CD | `S15 — Coordinated CI/CD and release pipeline` | Covered |
| `DEP-06` | Database migrations | `S15 — Database and data migrations` | Covered |
| `DEP-07` | Model deployment | `S15 — Model/artifact deployment` | Covered; profiles blocked |
| `DEP-08` | Infrastructure as code | `S15 — Infrastructure-as-code disposition` | Covered; conditional |
| `DEP-09` | Secrets | `S15 — Secrets and environment delivery`; `S12 — Secrets and key-control contract` | Covered; mechanism blocked |
| `DEP-10` | Scaling | `S15 — Scaling ladder` | Covered |
| `DEP-11` | Backups | `S15 — Backup, restore, and disaster-recovery deployment contract` | Covered |
| `DEP-12` | Rollback | `S15 — Layer-specific rollback and forward-fix` | Covered |
| `DEP-13` | Release strategies | `S15 — Coordinated CI/CD and release pipeline` | Covered |
| `DEP-14` | Development/testing environments | `S15 — Developer and test environments` | Covered |
| `DEP-15` | Do not automatically recommend Kubernetes; compare simpler approach | `S15 — Deployment alternatives and Kubernetes comparison`; `FSD — deferred mechanisms / Kubernetes/operators` | Covered; not selected |

## 15. Testing strategy

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `TST-01` | Unit tests | `S16 — Test-level catalog` | Covered |
| `TST-02` | Contract tests | `S16 — Test-level catalog`; `FIC — Canonical contract conformance tests` | Covered |
| `TST-03` | Integration tests | `S16 — Test-level catalog` | Covered |
| `TST-04` | End-to-end tests | `S16 — Test-level catalog`; `— Contract and critical-risk verification matrix` | Covered |
| `TST-05` | Data-quality tests | `S16 — Data-quality test matrix` | Covered |
| `TST-06` | Model-evaluation tests | `S16 — Capability production-admission test matrix` | Covered; profiles blocked |
| `TST-07` | Event-delivery tests | `S16 — Conditional event and delivery test lanes` | Covered; path inactive |
| `TST-08` | Load tests | `S16 — Load, performance, and resource-characterization plan` | Covered; targets blocked |
| `TST-09` | Resilience tests | `S16 — Resilience, migration, release, and recovery suite` | Covered |
| `TST-10` | Security tests | `S16 — Security production-admission test matrix` | Covered |
| `TST-11` | Tenant-isolation tests | `S16 — Tenant-isolation suite by asset` | Covered |
| `TST-12` | Agent evaluations if applicable | `S16 — Agent evaluation disposition` | Covered; N/A now |
| `TST-13` | Identify highest-risk pre-production scenarios | `S16 — Contract and critical-risk verification matrix`; `— Release and block transition gates` | Covered |

## 16. Capacity, performance, and cost

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `CPC-01` | Capacity model from known facts/labeled assumptions | `S17 — Capacity-model evidence rules` | Covered |
| `CPC-02` | Tenants | `S17 — Workload-envelope variables` | Covered symbolically; values unknown |
| `CPC-03` | Requests | `S17 — Workload-envelope variables` | Covered symbolically |
| `CPC-04` | Data volume | `S17 — Data volume and storage-growth model` | Covered symbolically |
| `CPC-05` | Batch sizes | `S17 — Workload-envelope variables`; `— Per-capability workload model` | Covered symbolically |
| `CPC-06` | Concurrent jobs | `S17 — Job, concurrency, and backlog model` | Covered symbolically |
| `CPC-07` | Event volume | `S17 — Event, delivery, and telemetry workload` | Covered symbolically |
| `CPC-08` | Storage growth | `S17 — Data volume and storage-growth model` | Covered symbolically |
| `CPC-09` | Model memory | `S17 — Artifact/model memory and load model` | Covered symbolically |
| `CPC-10` | CPU/GPU | `S17 — Per-capability workload model`; `— CPU/GPU disposition` | Covered; no GPU purchase justified |
| `CPC-11` | Latency | `S17 — Workload-envelope variables`; `— Benchmark and measurement plan` | Covered; objectives unknown |
| `CPC-12` | Cost drivers | `S17 — Cost model`; `— Synapse/provider cost model` | Covered symbolically |
| `CPC-13` | Identify measurements needed before infrastructure decision | `S17 — Benchmark and measurement plan`; `— Production capacity-admission record` | Covered |

## 17. Architecture decisions

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `ADR-F01` | Record decision | Every `decisions/ADR-000`–`ADR-016 — Decision`; `S18 — Complete ADR register` | Covered |
| `ADR-F02` | Record context | Every ADR `— Context` | Covered |
| `ADR-F03` | Record chosen option | Every ADR `— Decision` | Covered |
| `ADR-F04` | Record alternatives | Every ADR `— Alternatives considered` | Covered |
| `ADR-F05` | Record reason | Every ADR `— Rationale` | Covered |
| `ADR-F06` | Record trade-offs | Every ADR `— Consequences and trade-offs` | Covered |
| `ADR-F07` | Record risks | Every ADR `— Risks` | Covered |
| `ADR-F08` | Record status | Every ADR metadata; `S18 — Complete ADR register` | Covered |
| `ADR-F09` | Record reconsideration trigger | Every ADR `— Reconsideration trigger` | Covered |
| `ADR-C01` | Modular monolith vs microservices | ADR-003; `S18 — Decision-comparison coverage` | Covered |
| `ADR-C02` | Shared vs separate databases | ADR-003/010; `S18 — Decision-comparison coverage` | Covered |
| `ADR-C03` | Push vs pull ingestion | ADR-011; `S18 — Decision-comparison coverage` | Covered |
| `ADR-C04` | Sync vs async processing | ADR-004/005; `S18 — Decision-comparison coverage` | Covered |
| `ADR-C05` | Queue vs event broker | ADR-005/015; `S18 — Decision-comparison coverage` | Covered |
| `ADR-C06` | Scheduled vs event-driven | ADR-006; `S18 — Decision-comparison coverage` | Covered |
| `ADR-C07` | REST vs gRPC | ADR-004; `S18 — Decision-comparison coverage` | Covered |
| `ADR-C08` | Build vs buy | ADR-014; `S18 — Decision-comparison coverage` | Covered |
| `ADR-C09` | Rules/ML capability vs AI agent | ADR-013; `S18 — Decision-comparison coverage` | Covered |
| `ADR-C10` | Basic feature management vs feature store | ADR-012; `S18 — Decision-comparison coverage` | Covered |

## 18. Diagrams

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `DGM-01` | System context diagram | `FDG — 1. System context` | Covered |
| `DGM-02` | Logical container/component diagram | `FDG — 2. Logical container/component architecture` | Covered |
| `DGM-03` | Synchronous request flow | `FDG — 3. Bounded synchronous flow` | Covered |
| `DGM-04` | Asynchronous job flow | `FDG — 4. Durable asynchronous flow` | Covered |
| `DGM-05` | Proactive ML event-delivery flow | `FDG — 5. Proactive insight and conditional delivery` | Covered |
| `DGM-06` | Data lifecycle | `FDG — 6. Data lifecycle` | Covered |
| `DGM-07` | Deployment architecture | `FDG — 7. Provisional deployment and Phase 1 placement` | Covered |
| `DGM-08` | Keep diagrams readable/consistent; avoid all details in one | `FDG — Status and notation`; seven bounded diagrams; render evidence in `S24` | Covered |

## 19. Implementation roadmap

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `RDM-01` | Walking skeleton/proof phase | `FRM — Phase 1 — walking skeleton / proof of architecture` | Covered |
| `RDM-02` | MVP phase | `FRM — Phase 2 — sponsor-selected MVP/validation slice` | Covered |
| `RDM-03` | Production hardening | `FRM — Phase 3 — production hardening and admission` | Covered |
| `RDM-04` | Scale-driven improvements | `FRM — Phase 4 — scale-driven improvements` | Covered |
| `RDM-05` | Optional future capabilities | `FRM — Phase 5 — optional future capabilities` | Covered |
| `RDM-F01` | Every phase states scope | Each `FRM — Phase 1`–`Phase 5 / Scope` | Covered |
| `RDM-F02` | Every phase states tasks | Each `FRM — Phase 1`–`Phase 5 / Tasks` | Covered |
| `RDM-F03` | Every phase states deliverables | Each `FRM — Phase 1`–`Phase 5 / Deliverables` | Covered |
| `RDM-F04` | Every phase states dependencies | Each `FRM — Phase 1`–`Phase 5 / Dependencies` | Covered |
| `RDM-F05` | Every phase states acceptance criteria | Each `FRM — Phase 1`–`Phase 5 / Acceptance criteria` | Covered |
| `RDM-F06` | Every phase states major risks | Each `FRM — Phase 1`–`Phase 5 / Major risks` | Covered |
| `RDM-F07` | Every phase states deliberate postponements | Each `FRM — Phase 1`–`Phase 5 / Deliberate postponements` | Covered |
| `RDM-06` | Skeleton proves a realistic request through important boundaries despite temporary internals | `FRM — Phase 1`; `S20 — Phase 1 proof-of-architecture contract` | Covered |

## 20. Ten closing deliverables

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `DEL-01` | Recommended starting architecture | `FSD — Binding architecture baseline` | Covered |
| `DEL-02` | Minimal first-version component list | `FSD — Runtime roles and actual first placement`; `FRM — Phase 1` | Covered |
| `DEL-03` | Explicitly postponed components | `FSD — Stage 23 anti-overengineering classification — deferred or rejected mechanisms` | Covered |
| `DEL-04` | Top ten unresolved questions | `FRQ — Top ten unresolved questions` | Covered |
| `DEL-05` | Top ten risks | `FRQ — Top ten risks` | Covered |
| `DEL-06` | First implementation milestone | `FRM — Phase 1` | Covered |
| `DEL-07` | Decisions required now | `FRQ — Decisions required now` | Covered |
| `DEL-08` | Decisions safely deferred | `FRQ — Decisions safely deferred` | Covered |
| `DEL-09` | Architecture completeness checklist | `FRT — Publication completeness checklist`; `quality/final-acceptance-checklist.md` | Covered; Stage 24 sign-off passed |
| `DEL-10` | Non-technical executive summary | `FSD — Non-technical executive summary` | Covered |

## Runtime placement and execution-flow analysis

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `RUN-U01` | State stages/workflows using every significant element | `S22 — Runtime element usage and placement matrix`; every `FEF — UC-* / A. Stage usage table` | Covered |
| `RUN-U02` | State exact activation trigger | Same A tables `Trigger` column | Covered |
| `RUN-U03` | State prerequisites | Same A tables `Prerequisites` column | Covered |
| `RUN-U04` | State invoker | `S22 — Runtime element usage and placement matrix`; UC narratives | Covered |
| `RUN-U05` | State universal vs conditional participation | A tables `Execution mode`/activation labels | Covered |
| `RUN-U06` | State placement reason | A tables `Reason used here` | Covered |
| `RUN-U07` | State requirement satisfied | `S22 — Requirements-traceability updates`; `FRT` | Covered |
| `RUN-U08` | Explain absence from other stages | `S22 — Runtime element usage and placement matrix`; activation labels | Covered |
| `RUN-U09` | Explain removal/move/delay/replacement effect | `S22 — Runtime element usage and placement matrix` | Covered |
| `RUN-U10` | Classify critical vs supporting | A tables and `FEF — Critical/supporting path separation` per UC | Covered |
| `RUN-U11` | Do not call conditional components universally active | `FEF — Activation and notation`; every UC activation | Covered |
| `RUN-M01` | Classify sequential/blocking | Every UC A/B table `Execution mode`/`Critical-path status` | Covered |
| `RUN-M02` | Classify sequential/asynchronous | Same | Covered |
| `RUN-M03` | Classify parallel/blocking fan-in | Same | Covered |
| `RUN-M04` | Classify parallel/non-blocking | Same | Covered |
| `RUN-M05` | Classify event-triggered | Same | Covered |
| `RUN-M06` | Classify scheduled | Same | Covered |
| `RUN-M07` | Classify conditional | Same | Covered |
| `RUN-M08` | Classify background/out-of-band | Same | Covered |
| `RUN-D01` | Explain serial vs concurrent reasoning | Every UC `B. Execution dependency table`; runtime narrative | Covered |
| `RUN-D02` | State prerequisite data/state | B tables `Depends on` | Covered |
| `RUN-D03` | State independent parallel steps | B tables `Can run in parallel with` | Covered |
| `RUN-D04` | State multi-predecessor waits | B tables `Synchronization requirement` | Covered |
| `RUN-D05` | State synchronization/fan-in | B tables `Synchronization requirement` | Covered |
| `RUN-D06` | State ordering guarantee | B tables `Ordering requirement` | Covered |
| `RUN-D07` | State concurrency limits | UC narratives; `S08 — Priority, fairness, concurrency, and backpressure` | Covered; values blocked |
| `RUN-D08` | State race risks | UC narratives and failure effects | Covered |
| `RUN-D09` | State consistency requirements | UC narratives; `S13 — Reliability invariants` | Covered |
| `RUN-D10` | State timeout/cancellation | UC narratives; `S08 — Timeout and deadline semantics`; `— Cancellation semantics` | Covered |
| `RUN-D11` | State branch/downstream failure effects | A tables `Failure effect`; B tables | Covered |
| `RUN-D12` | State step vs whole-workflow retry boundary | B tables `Retry boundary` | Covered |
| `RUN-D13` | Parallelize only when ordering/state/transaction/resource/consistency allow | B tables; UC narratives | Covered |
| `RUN-C01` | Separate result/commit critical path | Every UC `Critical/supporting path separation` | Covered |
| `RUN-C02` | Separate background work | Same | Covered |
| `RUN-C03` | Separate operational side effects | Same | Covered |
| `RUN-C04` | Separate monitoring/observability | Same | Covered |
| `RUN-C05` | Separate audit/compliance | Same | Covered |
| `RUN-C06` | Separate notification/event delivery | Same | Covered |
| `RUN-O01` | Inline trace-context/essential instrumentation | `S14 — Inline instrumentation versus asynchronous export`; UC narratives | Covered |
| `RUN-O02` | Buffer telemetry export asynchronously | `S14 — Inline instrumentation versus asynchronous export`; UC diagrams | Covered |
| `RUN-O03` | Telemetry export normally does not fail business operation | `S14 — Telemetry outage and degradation behavior` | Covered |
| `RUN-O04` | Mandatory audit may require stronger synchronous/transactional guarantee | `S13 — Authoritative commit and finalization contract`; UC narratives | Covered |
| `RUN-O05` | Explain observability path precisely, not “runs in parallel” | Every UC `Critical/supporting path separation`; `S14` | Covered |

## Required execution artifacts and use cases

Every `ART-*` schema item is present in every UC-01 through UC-08 package in `FEF`; explicit `N/A` is used for the unjustified agent flow.

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `ART-A01` | A table: stage | Every `FEF — UC-* / A. Stage usage table`, `Stage` column | Covered |
| `ART-A02` | A table: component/module/function | Same, `Component/operation` | Covered |
| `ART-A03` | A table: trigger | Same, `Trigger` | Covered |
| `ART-A04` | A table: reason used at stage | Same, `Reason used here` | Covered |
| `ART-A05` | A table: prerequisites | Same, `Prerequisites` | Covered |
| `ART-A06` | A table: input | Same, `Input` | Covered |
| `ART-A07` | A table: output | Same, `Output` | Covered |
| `ART-A08` | A table: execution mode | Same, `Execution mode` | Covered |
| `ART-A09` | A table: blocking/non-blocking | Same, `Blocking?` | Covered |
| `ART-A10` | A table: failure effect | Same, `Failure effect` | Covered |
| `ART-A11` | A table: next step | Same, `Next step` | Covered |
| `ART-B01` | B table: operation | Every `FEF — UC-* / B. Execution dependency table`, `Operation` | Covered |
| `ART-B02` | B table: depends on | Same, `Depends on` | Covered |
| `ART-B03` | B table: parallel peers | Same, `Can run in parallel with` | Covered |
| `ART-B04` | B table: synchronization | Same, `Synchronization requirement` | Covered |
| `ART-B05` | B table: ordering | Same, `Ordering requirement` | Covered |
| `ART-B06` | B table: critical-path status | Same, `Critical-path status` | Covered |
| `ART-B07` | B table: retry boundary | Same, `Retry boundary` | Covered |
| `ART-C01` | Narrative from trigger to result including branches/background/failures/retries/delivery | Every `FEF — UC-* / C. Runtime narrative` | Covered |
| `ART-D01` | Diagram distinguishes sequential operations | Every `FEF — UC-* / D. Mermaid execution diagram` | Covered |
| `ART-D02` | Diagram distinguishes parallel branches | Same | Covered |
| `ART-D03` | Diagram distinguishes asynchronous work | Same | Covered |
| `ART-D04` | Diagram distinguishes events | Same | Covered |
| `ART-D05` | Diagram distinguishes conditions | Same | Covered |
| `ART-D06` | Diagram distinguishes synchronization | Same | Covered |
| `ART-D07` | Diagram distinguishes background work | Same | Covered |
| `ART-D08` | Diagram shows final response/delivery | Same | Covered |
| `UC-01` | Synchronous inference package | `FEF — UC-01 — Synchronous inference` | Covered; target contract blocked |
| `UC-02` | Async inference/batch package | `FEF — UC-02 — Asynchronous inference or batch job` | Covered; Phase 1 fixture runnable only |
| `UC-03` | Scheduled ML package | `FEF — UC-03 — Scheduled ML execution` | Covered; inactive |
| `UC-04` | Event-triggered package | `FEF — UC-04 — Event-triggered execution` | Covered; inactive |
| `UC-05` | Proactive insight/webhook package | `FEF — UC-05 — Proactive insight and webhook delivery` | Covered; inactive/blocked |
| `UC-06` | Model training/deployment package | `FEF — UC-06 — Model training and deployment` | Covered; profiles blocked |
| `UC-07` | Multi-capability workflow package | `FEF — UC-07 — Multi-capability workflow` | Covered; conditional illustration |
| `UC-08` | Agentic package if justified | `FEF — UC-08 — Agentic workflow` | Covered as N/A; no agent justified |
| `ART-SCOPE` | Analyze only architecturally significant functions | `S22 — Scope boundary`; `FEF — Scope and authority` | Covered |

## Anti-overengineering test

| ID | Atomic instruction | Exact destination | Status |
|---|---|---|---|
| `AOE-01` | State concrete requirement | `FSD — Stage 23 anti-overengineering classification` / `Concrete requirement` columns | Covered |
| `AOE-02` | State whether needed now | Same / `Needed now?` or `Concrete requirement now?` | Covered |
| `AOE-03` | State simpler outcome | Same / `Simpler outcome` | Covered |
| `AOE-04` | State operational burden | Same / `Operational burden` | Covered |
| `AOE-05` | State current team capacity | Same / `Current ownership capacity` or `Current capacity`; ADR-016 rule | Covered |
| `AOE-06` | State measurable later trigger | Same / `Measurable later trigger` | Covered |
| `AOE-07` | Classify required now | `FSD — included logical elements` / `Class` | Covered |
| `AOE-08` | Classify useful soon | Same | Covered |
| `AOE-09` | Classify scale-triggered | `FSD — deferred or rejected mechanisms` / `Class` | Covered |
| `AOE-10` | Classify optional | Same | Covered |
| `AOE-11` | Classify unjustified | Same | Covered |
| `AOE-12` | Treat many independent services/products as warning and re-evaluate | `FSD — No included element is justified as an independently deployed microservice`; ADR-003 | Covered |
| `AOE-13` | Design is implementation-ready without pretending unknowns are decided | `FRM — Phase 1`; `FRQ — Active production-admission blocks`; `S24 — Completion-gate evidence` | Covered |

## Register completeness

- Stable IDs cover every prescriptive list item and compound instruction in the normalized system-design prompt, including all capability-contract fields, component-specification fields, runtime sub-bullets, ten deliverables, and six anti-overengineering questions.
- Project-information statements are source facts rather than instructions; their fidelity is traced in `S00 — Normalized-source inventory`, `S01 — Facts`, and `S02 — Facts`.
- No row is `Pending`. Rows marked blocked describe activation evidence, not missing architecture coverage.
