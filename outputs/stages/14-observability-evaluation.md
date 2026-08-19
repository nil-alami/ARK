# Stage 14 — Observability and evaluation

**Status:** APPROVED  
**Completed:** 2026-08-13  
**Stage owner:** Primary architecture agent  
**Authorized specialists:** `platform_architect`, `data_mlops_architect` (read-only, non-overlapping signal reviews)

## Purpose and scope

Define the owner-relevant logs, metrics, traces, correlation, health, dashboards, alerts, authoritative audit, tenant usage, cost evidence, data quality, model quality, and evaluation contracts for the approved ARK architecture and every Stage 13 critical path. This stage distinguishes essential inline evidence from asynchronous diagnostic export and defines measurable service-level indicators without inventing unsupported objectives.

This stage does not select an observability vendor, collector, backend, dashboard product, tracing protocol, deployment topology, retention period, sampling rate, alert threshold, SLO, error budget, business KPI, model-quality threshold, cost budget, or LAB promotion authority. It does not clear any ADR-007 capability disposition or ADR-008 security-admission block. It does not activate Synapse, webhook delivery, a named workflow, an agent, or any conditional infrastructure. Stage 15 is not executed.

## Inputs read in full

- `WORKFLOW.md`
- `STATUS.md`
- `SOURCE_MANIFEST.md`
- `stages/STAGE-CONTRACT.md`
- `stages/14-observability-evaluation.md`
- `templates/stage-output.md`
- `sources/normalized/system-design-prompt.md` — **13. Observability and evaluation**
- Approved `outputs/stages/02-system-definition.md` through `outputs/stages/13-reliability.md`
- Accepted `decisions/ADR-000-temporary-source-evidence-disposition.md` through `decisions/ADR-008-zero-trust-tenant-and-governance-boundary.md`
- `sources/normalized/service-cards/churnobyl.md` — **13. OBSERVABILITY**
- `sources/normalized/service-cards/RFM.md` — **13. OBSERVABILITY**
- `sources/normalized/service-cards/next_purchase_prediction.md` — **13. OBSERVABILITY**
- `sources/normalized/service-cards/recommender.md` — **13. OBSERVABILITY**
- `sources/normalized/service-cards/Synapse_chatbot.md` — **13. OBSERVABILITY**
- `sources/normalized/service-cards/synapse_message_generator.md` — **13. OBSERVABILITY**
- `sources/normalized/service-cards/synapse_campaign_verifier.md` — **13. OBSERVABILITY**

## Specialist reconciliation

The Stage 14-authorized `platform_architect` reviewed platform, control, API, job, storage, delivery, security, reliability, correlation, health, usage, cost, and telemetry-outage signals. The authorized `data_mlops_architect` independently reviewed ingestion, data quality, all seven capability profiles, ML/LLM evaluation, drift, reproducibility, tenant usage, and model cost evidence. Both were read-only and non-overlapping by primary signal ownership. Their findings are reconciled into the common correlation contract, all 22 component rows, all eight critical-path rows, four-layer data/eligibility signals, seven capability profiles, inline/export split, health, dashboards, alerts, SLIs, cost/usage, contradictions, and production blocks below. The data/ML final review identified one material reproduction-observability omission; after explicit reproduction run/report identities, signals, mismatch evidence, and an SLI were added, its final pass reported no critical, high, or material medium defect. The platform final pass likewise reported none. Both recommended `PASS`. The primary agent remains the sole authoritative writer.

## Source-instruction coverage

| Governing requirement | Addressed in | Status/evidence |
|---|---|---|
| Structured logs | Common event envelope; component/workflow matrices | Covered |
| Metrics | Signal taxonomy; component, workflow, and capability matrices | Covered |
| Traces | Correlation and trace propagation contract | Covered |
| Correlation across APIs, jobs, models, and events | Stable identity graph and required fields | Covered |
| Health checks | Health semantics and dependency readiness | Covered |
| Dashboards | Owner-view dashboard register | Covered |
| Alerts | Alert policy and matrix conditions | Covered; numeric thresholds remain production inputs |
| Audit logs | Authoritative audit/evidence separation | Covered; audit is an immutable record, not diagnostic logging |
| Per-tenant usage | Authoritative usage/metering contract | Covered without unbounded metric labels |
| Model-quality metrics | Seven-capability evaluation matrix | Covered or explicitly blocked by absent evidence |
| Data-quality metrics | Ingestion/dataset and capability matrices | Covered |
| Cost metrics | Reservation/commit/reconcile plus resource/provider attribution | Covered; pricing/budgets remain unknown |
| Agent execution traces if applicable | Not applicable to current design | No agent is justified or selected; future agent must reopen Stage 11/14 |
| SLIs and realistic SLOs | SLI catalog and SLO-admission plan | SLIs defined; numeric SLOs not proposed because evidence is insufficient |

## Confirmed facts

1. ARK must correlate requests, ingestion runs, jobs, datasets, models, outputs, grants, proactive decisions, events/deliveries, usage, cost, audit, and diagnostic telemetry. `outputs/stages/02-system-definition.md — ARK-NFR-006`; `outputs/stages/13-reliability.md — Reliability invariants`.
2. Logs, metrics, traces, queue state, caches, and health observations are not business authority. Committed owner records remain the recovery and truth anchor. `outputs/stages/13-reliability.md — Reliability invariants`.
3. Mandatory audit is authoritative and may block privileged/sensitive effects when unavailable. Diagnostic telemetry export is supporting evidence and must not become an authorization or success condition. `outputs/stages/12-security-governance.md — Audit, privileged operations, and governance separation`; accepted ADR-008.
4. Stage 05 defines 22 logical components, including an observability responsibility, while runtime placement and products remain deferred. `outputs/stages/05-end-to-end-architecture.md — Component inventory`.
5. Stage 13 defines eight current or conditional critical paths and requires detection evidence for dependency, backlog, crash, duplicate, partial, stale, poison, delivery, recovery, and DR conditions. `outputs/stages/13-reliability.md — Critical-path failure matrices`.
6. Churn, RFM, NPT, and REC service cards name extensive desired operational, data, and ML/recommendation metrics, but their current implementations lack consistent structured metrics/traces and remain `MIGRATION_BLOCKED`. `sources/normalized/service-cards/* — 13. OBSERVABILITY`; accepted ADR-007.
7. The three Synapse cards expose only sparse response-level `cost` and, for verifier, `status`; provider/model/prompt/evaluation/usage internals remain undocumented and `EVIDENCE_BLOCKED`. `sources/normalized/service-cards/Synapse_* — 13. OBSERVABILITY`; accepted ADR-007.
8. Numeric traffic, latency, availability, freshness, recovery, quality, cost, retention, sampling, and alert targets are not approved. `outputs/stages/02-system-definition.md — A-01-SCALE/A-01-OPS`; approved Stage 13 `Q-13-01` through `Q-13-08`.
9. No production agent is justified or selected from current evidence. `outputs/stages/11-agent-architecture.md — Decisions`.

## Temporary assumptions

| ID | Assumption | Why needed | Architectural effect | Risk | Validation/expiry |
|---|---|---|---|---|---|
| `A-01-SCALE` | Numeric workload and SLO/cost targets remain unknown | Prevent fabricated objectives | Define SLIs and measurement plans only | Production fitness cannot be claimed | Stage 17 measured evidence |
| `A-01-OPS` | Deployment, support, retention, incident, and observability targets remain unknown | Products/topology/on-call cannot be selected | Logical signal ownership and outage behavior only | Operational implementation remains blocked | Stages 15/17/20 |
| `A-04-OWNERSHIP` | Named accountable/on-call owners are absent | Matrices require logical owners | Every dashboard/alert names a role, not a person | Alerts cannot be production-routed | Stage 20 owner roster |
| `A-07-INTEGRATION` | Polling is authoritative and event/webhook paths are conditional | Preserve delivery truth | Conditional delivery signals are design gates, not active telemetry | No delivery SLO claim | Approved consumer contract and admission evidence |

No new temporary assumption is introduced. Existing assumptions retain their approved expiry and cannot enable production.

## Observability invariants

1. **Owner truth is separate from observation.** A log, metric, span, dashboard, alert, or health response cannot create or alter a job, dataset, result, grant, assignment, action, delivery, usage charge, or audit record.
2. **Correlation is mandatory; export is not authority.** The trusted execution context creates stable identifiers inline. Export may be delayed or dropped under policy, but missing export is visible and never changes committed owner truth.
3. **Audit is not a log stream.** Mandatory audit is a tenant-scoped immutable owner record with actor, authority, versions, decision, effect, and evidence references. It has distinct access, integrity, retention, and fail-closed behavior.
4. **No raw PII by default.** Telemetry uses opaque tenant/subject/resource identifiers, redaction/allowlists, bounded error classes, and protected evidence references. Payloads, prompts, history, secrets, tokens, phone numbers, and free-form customer text are excluded unless an approved diagnostic evidence contract says otherwise.
5. **Tenant usage is authoritative ledger state.** High-cardinality tenant/resource usage is queried from tenant-qualified usage/metering records. Shared metrics use bounded dimensions or controlled tenant views; tenant identity is not added indiscriminately to every metric label.
6. **Versions travel with evidence.** Quality, latency, error, drift, usage, and cost evidence references exact contract, dataset, feature, handler/code, configuration/policy, model/artifact/prompt/provider, execution, and environment versions applicable to the operation.
7. **Outcome classes are not collapsed.** Invalid, denied, not-ready, ineligible, unavailable, failed, cancelled, degraded, suppressed, dead-lettered, ambiguous, and succeeded remain distinct in metrics and evaluations.
8. **Alerts are actionable and owned.** An alert states the affected contract/path, condition, severity policy, logical owner, runbook/reconciliation link, and customer/tenant scope. Missing thresholds or owner routing block activation.
9. **Quality gates are versioned decisions.** A metric is not a promotion threshold. Dataset readiness, model evaluation, assignment, and rollback use approved versioned gate records with cohort/window/minimum-evidence definitions.
10. **Observability observes itself.** Export queue age, drops, sampling, redaction failures, cardinality rejection, backend reachability, clock skew, trace completeness, and cost/volume are monitored separately from business health.

## Common telemetry and evidence contract

### Required correlation fields

Fields are included only where applicable; trusted context supplies tenant and actor fields.

| Field family | Required identities |
|---|---|
| Request/control | `environment_id`, trusted `tenant_id`, `principal_id`/`workload_id`, `request_id`, `correlation_id`, `operation_id/version`, `idempotency_key_hash`, `contract_version`, `control/policy/grant/config_version` |
| Execution | `job_id`, `attempt_id`, `fence/recovery_epoch`, `schedule_id/version`, `occurrence_id`, `workflow_id/version`, `parent_job_id`, `handler/code_version`, `retry_attempt`, `deadline_class` |
| Data | `source_id`, `source_contract_version`, `ingestion_run_id`, `dataset_id/version`, `object_ref_hash`, `quality_report_id`, `feature_schema/transform_version`, `as_of`/observation interval |
| ML/LLM | `training/evaluation_run_id`, `reproduction_run_id`, `reproduction_report_id`, `model/artifact_bundle_id/version/digest_ref`, `deployment_assignment_id/version`, `prompt/provider/policy_version` when admitted, `prediction/result_id` |
| Action/delivery | `insight_id`, `decision_id`, `intent_id`, `effect_id`, `event_id/schema_version`, `handler_version`, `delivery_id/generation/attempt`, `destination_id/version` |
| Evidence | `audit_record_id`, `lineage_id`, `usage_effect_id`, `cost_record_id`, `trace_id`, `span_id`, `causation_id`, `replay/recovery_id` |

Raw idempotency keys, secrets, credentials, payloads, object paths, endpoint URLs, prompts, and direct customer identifiers are not telemetry fields. Hashing does not itself make sensitive identifiers safe; classification/access policy still applies.

### Structured log/event envelope

Every diagnostic event has timestamp from a synchronized source; severity; event name and schema version; component/module and logical owner; environment; outcome/status/reason class; safe duration/count/size fields; applicable correlation/version fields; and redaction classification. Exceptions are normalized to bounded type/code and safe stack reference. Free-form messages are supplementary, not the query contract.

Required event families include request admission/result, owner state transition, dependency call outcome, retry/circuit/timeout, lease/fence rejection, dataset validation/readiness, model load/inference/evaluation, proactive Phase A/B/effect recheck, publication/delivery attempt, reconciliation/restore, security denial, audit write outcome, telemetry export/drop, and cost/usage reconciliation.

### Trace propagation and sampling

- W3C-like trace semantics may be implemented later, but the logical contract is vendor-neutral: a caller span propagates trusted `correlation_id` and trace context through module ports, HTTP, job admission, attempt claims, scheduled occurrences, conditional intents/events, and delivery attempts.
- Async boundaries create linked spans rather than pretending one process lifetime. Links preserve request → job → attempt → result and event → handler/delivery generations.
- Tail/head sampling policy is unresolved. Errors, security events, privileged operations, rare failure transitions, and evaluation evidence require durable owner/audit records regardless of trace sampling.
- Baggage is allowlisted and bounded. Tenant authorization never derives from trace baggage.

## Inline instrumentation versus asynchronous export

| Concern | Inline requirement | Asynchronous/supporting behavior | Outage behavior |
|---|---|---|---|
| Trusted context/correlation | Create/validate identifiers at ingress, job/event creation, and attempt claim | Export spans/logs later | Missing/invalid required context rejects admission; exporter loss does not authorize or alter work |
| Owner state and reason | Commit state/reason/version with owner transaction | Project to dashboards/metrics | Owner state remains queryable; projection lag is visible |
| Mandatory audit | Commit required audit intent/evidence before sensitive effect and completion obligation as designed | Read models/export may lag | Fail closed for mandatory-audit operations; never act then backfill authorization |
| Lineage/reproducibility | Commit required version/result references before readiness/success | Build searchable graph/read model | No readiness/success when required lineage is absent |
| Usage/quota/cost | Reserve/commit/release/reconcile by stable effect identity | Aggregate/report/export later | No double charge; missing mandatory reservation blocks admission; reporting lag is explicit |
| Diagnostic logs/metrics/traces | Emit to bounded local/in-process interface without unbounded blocking | Batch/buffer/export with backpressure and policy | Continue only if authoritative controls succeed; count drops, degrade health, preserve bounded resource use |
| Quality/drift evaluation | Commit exact evaluation report/gate evidence for lifecycle decisions | Aggregate trends, dashboards, offline analysis | Promotion/assignment blocked when mandatory evidence unavailable; inference follows its approved current profile |
| Health | Compute bounded local/dependency status without mutating owner state | External polling/aggregation later | Health endpoint failure is diagnostic; routing/topology implications are Stage 15 |

Diagnostic exporters must have bounded queues, memory/disk use, retry/backoff, and drop/sampling policy. They cannot create a retry storm, exhaust worker resources, log raw payloads as fallback, or block ordinary operations indefinitely.

## Health contract

| Probe/view | Meaning | Must not mean |
|---|---|---|
| Liveness | Process/event loop can serve its health contract | Database/model/provider/workload is healthy or request should be routed here |
| Readiness | Runtime role can accept its declared operation class with mandatory local configuration and required dependencies currently usable | All capabilities, tenants, datasets, models, or external destinations are eligible |
| Dependency health | Bounded status/latency of PostgreSQL owner schemas, object storage, identity/control/audit/secrets, registry, exporter, and any admitted remote dependency | Permission to use stale data or bypass an unavailable authority |
| Worker health | Poll/claim loop, heartbeat, handler compatibility, lease renewal, and resource saturation state | A specific job succeeded or stale worker may commit |
| Dataset/model health | Exact readiness/assignment/integrity/freshness/evaluation state | Generic platform readiness or a universal “last known good” fallback |
| Telemetry health | Export lag/drop/cardinality/redaction/trace completeness and backend reachability | Business operation failure or success |

Health endpoints expose no tenant-sensitive inventory, secrets, stack traces, configuration values, object paths, or model/provider details to unauthenticated callers.

## Component observability matrix

Every Stage 05 component is represented. Logical owner roles remain subject to `A-04-OWNERSHIP`.

| Component | Owner-relevant signals | Correlation/version fields | Alert/gate conditions | Telemetry-outage behavior |
|---|---|---|---|---|
| `C05-01` Adapter boundary | Mapping success/failure, unsupported consumer version, delivery/result interpretation latency | request/correlation, consumer/adapter/ARK contract versions | Mapping failures or unknown versions exceed approved policy; redaction failure | Consumer owner retains mapping outcome; ARK result truth unchanged |
| `C05-02` Edge/API | Request rate, latency, size rejection, auth/rate/version/outcome classes, dependency saturation | request/trace, trusted tenant after auth, route/operation/contract | Error/latency/saturation/security-abuse condition under approved policy | Bounded local emission; no raw request fallback; telemetry degraded |
| `C05-03` Identity/tenant | Validation latency/outcome, credential/revocation/assurance failures, tenant mismatch | request, principal/workload, trust-profile/version, tenant | Validator unavailable, anomalous denial/forgery/cross-tenant attempt | Mandatory identity failure blocks request; diagnostic export loss does not bypass |
| `C05-04` Control/policy | Entitlement/quota/grant/config decisions, CAS conflicts, reservations/releases, stale/revoked versions | tenant, resource, decision, policy/grant/config, usage effect | Authority store unavailable, reservation imbalance, repeated conflicts, privileged audit gap | Owner records/audit remain authoritative; fail closed where required |
| `C05-05` Capability/job API | Contract/outcome mix, sync deadline, async admission/replay/conflict, result retrieval | request/idempotency hash, operation/version, job/result | Unknown version, elevated failure/timeout, idempotency conflict anomaly | Public owner state remains queryable; missing diagnostics cannot change response |
| `C05-06` Ingestion pipeline | Upload/validation/normalization/publication counts, latency, quarantine, schema/quality/freshness reasons | source/contract, ingestion/job/attempt, object/dataset/quality versions | Invalid/poison surge, stalled stage, orphan growth, missing raw/catalog evidence | Raw/catalog owner truth remains; no ready publication without evidence |
| `C05-07` Catalog/readiness | Query/publication latency, readiness/stale/revoked mix, lineage/integrity gaps | dataset/version, quality/policy/lineage | Catalog unavailable, stale growth, missing object/lineage, readiness conflict | Capability fails not-ready/unavailable; cached telemetry never grants readiness |
| `C05-08` Job manager | State transitions, queue age/depth, claim/finalize latency, retries, lease/fence rejection, stuck states | job/attempt/fence/epoch, operation/handler | Oldest-ready/deadline risk, stuck finalization, retry/abandonment/duplicate surge | PostgreSQL truth remains; exporter bounded; DB outage means no false acceptance |
| `C05-09` Scheduler | Due/submitted/missed/duplicate/expired occurrences, lag, reconciliation | schedule/version, occurrence, grant/policy | Miss/lag/duplicate/reconciliation failure under approved policy | Occurrence truth retained; no blind catch-up from telemetry |
| `C05-10` Worker roles | Claim/heartbeat/lease, handler compatibility, stage time, resource saturation, cancellation | job/attempt/fence/handler/code | Crash/heartbeat loss, incompatible handler, stale effect rejection, saturation | Work follows leases/fences; telemetry loss cannot keep stale attempt alive |
| `C05-11` Capability modules | Eligibility/outcomes, latency, input/output counts, fallback/partial, quality/drift and exact versions | tenant, execution/result, dataset/feature/config/model/code | Contract-specific quality/gate failure, load/inference error, blocked profile invocation | Result/evaluation records authoritative; no unapproved fallback |
| `C05-12` Result/delivery | Poll/retrieval outcomes, intent/attempt latency, ack/ambiguity/retry/dead-letter/expiry | result/event/delivery/destination versions | Delivery backlog, endpoint/circuit failure, ambiguity, dead-letter growth | Polling/result truth remains; conditional delivery stays blocked until admitted |
| `C05-13` PostgreSQL | Availability, transaction/lock/pool/query/replication-or-backup evidence as applicable, schema capacity | component/schema/environment; no SQL/payload secrets | Owner transaction failure, saturation, integrity/backup/restore verification failure | Critical owner operations fail/pause truthfully; no in-memory authority |
| `C05-14` Object storage/lake | Read/write latency/outcome, checksum, object/ref/orphan/missing counts, namespace denial | tenant-safe object ref hash, dataset/artifact/result, digest | Integrity/missing/orphan/access failure, cleanup/backup evidence gap | No readiness/result/artifact success without valid owner reference |
| `C05-15` Capability storage | Feature/result write/read, schema compatibility, finalization, partial/orphan state | capability, dataset/feature/result/version, job/attempt | Missing/conflicting result, schema mismatch, unfinalized growth | Owner result state remains truth; success held until obligations complete |
| `C05-16` Model registry | Registration/load/promotion/assignment/revocation/compatibility, digest/integrity | artifact/bundle/evaluation/assignment/runtime versions | Missing/corrupt/revoked/incompatible artifact; unauthorized promotion attempt | Exact assignment unavailable; never select latest or bypass blocks |
| `C05-17` Secrets/config delivery | Reference access/rotation/version/failure without values | workload, secret/config reference/version, operation | Retrieval/rotation/expiry/access anomaly | Required operation fails closed; no plaintext/default/log fallback |
| `C05-18` Audit/lineage/usage ledger | Append/finalization completeness, integrity, reconciliation, reservation/charge state | all evidence IDs and versions | Mandatory audit unavailable, lineage gap, usage imbalance, tamper/access anomaly | Mandatory effect blocked; diagnostic export never substitutes |
| `C05-19` Observability | Export lag/drop/retry, buffer/resource use, redaction/cardinality rejection, trace completeness, signal cost | component/environment/exporter/policy version | Sustained blind spot, redaction failure, resource threat, backend outage | Degrade visibility with bounded buffers; no business authority or retry storm |
| `C05-20` Admin/operations | Auth/step-up/command outcomes, dry-run/impact, reconciliation/restore/replay status | actor, command/idempotency, target versions, audit/recovery | Unauthorized/broad/stale command, incomplete recovery, audit failure | Privileged work fails closed; no unaudited emergency path |
| `C05-21` Reliable publication (conditional) | Outbox lag/state, handler attempts/dedupe/schema/dead-letter/replay | event/schema, handler/version, causation/delivery | Crash gap, poison/incompatible schema, backlog/dead-letter | Source fact remains authoritative; no activation without named subscriber |
| `C05-22` Workflow coordinator (conditional) | Parent/child states, waits, transitions, partial/residual/compensation, restart | workflow/version, parent/child jobs, node/effect | Stuck dependency, conflicting transition, failed compensation | Child truth retained; no active workflow or generic engine inferred |

## Critical-workflow observability matrix

| Stage 13 path | Owner-relevant signals | Required correlation | Alert/gate conditions | Telemetry-outage behavior |
|---|---|---|---|---|
| `CP-13-01` Synchronous request | Admission/outcome/latency by class; readiness/model load; result/evidence finalization; response-loss replay | request/idempotency, tenant, operation, dataset/model/result/audit/usage | Dependency unavailable, deadline/ambiguity, finalization obligation stuck, cross-tenant/security anomaly | Result/idempotency/audit records decide truth; diagnostic loss does not fail a committed result |
| `CP-13-02` Durable execution | Admission, queue age, state/attempt transitions, retries, leases/fences, cancellation, partial manifest, finalization | request → job → attempt/fence → result/effect/evidence | backlog/deadline risk, crash/retry storm, stale fence, poison, stuck finalization | PostgreSQL job truth and polling remain; exporter bounded and independently degraded |
| `CP-13-03` Ingestion/publication | Bytes/rows, stage latency, structural/semantic/quality outcomes, freshness, duplicates, candidates/orphans, publication | source/contract → run/job → objects → dataset/quality/lineage | poison/schema surge, incomplete data, stale source, missing/orphan object, catalog failure | Raw/catalog records remain; no ready dataset from telemetry |
| `CP-13-04` ML lifecycle | Training/evaluation/load/inference outcomes; reproduction reference/digest availability, environment/PIT reconstruction, exact-or-approved-tolerance comparison and mismatch reason; quality/drift, assignment/revocation/cache integrity | dataset/feature/code → training/evaluation → artifact/bundle → assignment → prediction, plus `reproduction_run_id`/`reproduction_report_id` linked to the original manifest and comparison | evaluation/gate or reproduction failure, missing reference/digest, reconstruction gap, out-of-tolerance mismatch, artifact integrity/load error, drift gate, blocked profile attempt | Promotion/assignment requires durable evidence; reproduction cannot pass without an immutable complete report; no model fallback from metric state |
| `CP-13-05` Proactive action | Trigger/occurrence lag; Phase A/B reasons; insight outcome; reservations/dedupe; intent/effect/recheck | occurrence → evaluation job/result → decision/audit/intent → task/effect | unauthorized/stale/audit failure, reservation mismatch, duplicate/ambiguous effect | Fail-closed owner decisions remain; verifier/telemetry cannot authorize action |
| `CP-13-06` Publication/delivery (conditional) | Intent/outbox lag, attempts, response class, circuit, ambiguity, dead-letter/expiry/replay | fact/result → event/intent → handler/delivery generations | crash gap, poison/schema, endpoint outage, ambiguity, dead-letter | Source fact/result and polling remain; path stays inactive until admitted |
| `CP-13-07` Privileged/recovery | Identity/step-up, command/CAS, dry-run/impact, deletion manifest, restore/reconcile completeness | actor/audit → command/recovery → exact target/effect/manifests | unauthorized/broad/stale command, partial deletion, audit/integrity failure | Fail closed; no local diagnostic evidence authorizes recovery |
| `CP-13-08` Named workflow (conditional) | Parent/child progress, waits, failure policy, partial/residual, compensation, coordinator restart | workflow/version → node → child jobs/results/effects | stuck graph, incompatible child, conflict, failed compensation | Durable graph/child truth retained; no active workflow assumed |

## Data-quality observability

Each dataset/source contract owns versioned rules, dimensions, reason codes, reference window, evaluation time, completeness/freshness policy, and owner. Measurements are tenant-qualified owner evidence; aggregate telemetry must preserve privacy.

| Dimension | Required evidence and indicators | Gate/alert meaning |
|---|---|---|
| Structural conformance | Parse/decompress/checksum/schema/version outcomes; required/type/bounds/cardinality failures | Quarantine/no ready publication for mandatory failure |
| Completeness | Expected objects/partitions/rows, missing fields/entities, source coverage and manifest completeness | Not-ready or degraded candidate only under explicit contract |
| Validity/semantics | Units/currency/time, referential integrity, range, catalog/inventory/consent/purpose rules | Semantic failure or explicit quality reason; never silently corrected |
| Uniqueness/order | Duplicate identities, collision/conflict, cursor gaps/regressions, late/correction/tombstone counts | Reconciliation or new version; no last-write-wins guess |
| Freshness | source max event time, observation/ingestion lag, partition/watermark completeness, readiness expiry | `STALE`/not-ready under versioned policy |
| Distribution | Row/entity counts, missingness, outliers, feature/category distributions by approved cohort | Drift/evaluation trigger; not automatically model drift or promotion |
| Lineage/integrity | Missing edges/objects, checksum mismatch, orphan/candidate/reference state | Block publication/result; reconciliation incident |
| Tenant/privacy | Cross-tenant denial, unexpected direct identifier/debug artifact, consent/purpose mismatch | Security incident and production gate failure |

## Capability evaluation and model-quality matrix

Metrics below are candidate measures from admitted source evidence. Numeric gates, cohorts, windows, minimum samples, baselines, fairness applicability, and promotion authority remain unresolved and must be versioned before production.

| Capability | Required operational/data signals | Quality/evaluation evidence | Gate/alert and outage behavior |
|---|---|---|---|
| Churn (`MIGRATION_BLOCKED`) | Run/queue/stage/model-load/write/retry; customer/transaction/eligibility/coverage; missingness/freshness/join failures | ROC-AUC, PR-AUC, log loss, Brier/calibration, precision/recall at approved thresholds, score/forced-score distribution, drift/stability by exact bundle | Missing labels/thresholds/evaluation or load/persistence evidence keeps profile blocked; telemetry outage cannot infer quality |
| RFM (`MIGRATION_BLOCKED`) | Run/queue/write/artifact; R/F/M validity, currency/window, exclusions, cluster sizes | inertia, silhouette, Calinski–Harabasz, Davies–Bouldin, centroid/size/assignment drift, seed stability, transition and label mapping; approved business outcomes separately | Missing stable feature/label/mapping/gates keeps blocked; no cluster metric alone authorizes semantic labels |
| NPT (`MIGRATION_BLOCKED`) | Job/stage/queue/load/write/resource; transaction/snapshot/eligible/routed/served counts and contract-health checks | CLF macro/weighted F1, top-2, confusion, calibration/Brier/log loss, bucket outcomes; RSF concordance, time-dependent AUC, Brier/integrated Brier, calibration/censoring | Horizon/label/PIT/schema/bundle/gates required; contract-health failure blocks serving success |
| REC (`MIGRATION_BLOCKED`) | Run/stage/queue/persistence/event/resource; transaction/catalog/sellable/mapping/matrix/source coverage | Recall/Precision/HitRate/NDCG/MAP@K, coverage, baseline/source lift, cold-start slices, diversity/novelty/stability/fairness when applicable; attribution-controlled business outcomes | Availability/constraint correctness is mandatory; absent evaluation/feedback policy keeps blocked; empty output not success |
| Synapse Chatbot (`EVIDENCE_BLOCKED`) | Only response `cost` is documented; future request latency/outcome/token/provider evidence requires admission | No authoritative quality, safety, grounding, refusal, model/prompt, dataset or evaluation contract exists | No production metrics/SLO can be inferred; provider/quality telemetry outage is irrelevant while calls are blocked |
| Synapse Message Generator (`EVIDENCE_BLOCKED`) | Only response token-usage `cost` is documented | Future content quality, factual/claim, language, safety/refusal and campaign-policy evaluation require authoritative contract | Remains unavailable; no alternate model/provider or silent content acceptance |
| Synapse Campaign Verifier (`EVIDENCE_BLOCKED`) | Response `cost` and `status` only | Future policy-reference coverage, false accept/reject, explanation fidelity, safety and adversarial evaluation; output remains advisory | `accepted` never authorizes action; missing evaluation/provider evidence blocks use |

### Evaluation record

Every approved data/model/LLM/recommendation evaluation record contains tenant/use-case scope; question and decision it supports; exact dataset/cohort/split/as-of/label/attribution versions; candidate and baseline bundle versions; metric definitions and uncertainty; missingness/exclusion; slice results; policy/fairness/safety applicability; threshold/gate version and pass/fail reasons; evaluator code/environment; owner/reviewer/approval evidence; and immutable report/object references.

Offline evaluation uses leakage-safe temporal/entity splits appropriate to the capability. Online/business evaluation is admitted only with a versioned exposure/control/attribution/feedback contract, consent/purpose authority, minimum evidence, and external-system provenance. Missing feedback is not a negative outcome. Drift may submit evaluation/training work but never promotes or changes assignment.

### Reproduction record and signals

Each reproduction is a separate durable job identified by `reproduction_run_id` and produces an immutable `reproduction_report_id`. It links the original training or prediction manifest, reference objects/digests, dataset/PIT snapshot, environment/runtime/dependency reconstruction evidence, exact code/handler/feature/model/configuration identities, comparison method, approved numeric tolerance where byte identity is not promised, actual differences, mismatch reason, completeness status, owner/reviewer, and correlation/audit references. Owner-visible signals cover reference/digest availability, reconstruction-stage outcome and duration, exact/tolerance comparison result, missing evidence, mismatch class, and report finalization. Missing diagnostic export cannot create a successful reproduction report.

## Per-tenant usage and cost contract

| Evidence | Authoritative identity and dimensions | Required reconciliation/reporting |
|---|---|---|
| API/job usage | tenant, operation/version, request/job/result, quantity/unit, reservation/commit/release effect | One logical charge/usage effect despite retry; denied/not-ready/failed policies explicit |
| Data/storage | tenant, source/dataset/object class, logical bytes/objects/retention class | Object/catalog reconciliation; shared overhead allocation policy separate |
| Compute | tenant, job/attempt/workload class, runtime/resource quantities, handler/model versions | Attempts separated from billable logical operation; retry policy and shared allocation explicit |
| Model/provider | tenant, prediction/call identity, exact provider/model/prompt when admitted, tokens/units/provider cost evidence | Provider statement/request reconciliation; Synapse remains blocked and response `cost` is not trusted billing authority |
| Delivery | tenant, event/delivery/destination, attempts/bytes/status | Retries visible; one logical notification distinguished from transport attempts |
| Shared platform | environment/component resource totals | Allocation/showback formula requires sponsor policy; never fabricate tenant charge |

Cost indicators include usage quantity, direct provider amount/currency/source/version where authoritative, resource quantity, failed/retried/abandoned work, storage growth, telemetry volume, and budget/policy decision. Prices, currencies, allocation, budgets, alert thresholds, and billing scope remain open. Diagnostic metrics cannot be the billing ledger.

## Dashboard register

| View | Primary audience/owner | Minimum content |
|---|---|---|
| Platform/API | Platform integration/operations | request/outcome/latency, dependency health, saturation, telemetry health, affected operation/version |
| Job/scheduler | Execution owner | admissions, queue age/depth, states, retries, leases/fences, missed occurrences, finalization, tenant/pool isolation |
| Data readiness | Data/source/governance owners | ingestion stages, quarantine/reasons, freshness/completeness/quality, ready/revoked versions, orphans/lineage |
| Capability/ML | Capability/scientific/release owners | exact active bundle, eligibility/outcomes, load/inference, evaluation gates, drift, fallback/partial, blocked status |
| Proactive/delivery | Control/integration/security owners | Phase A/B reasons, reservations, intents/effects, outbox/delivery lag, ambiguity/dead-letter; inactive block state |
| Security/audit | Security/governance | trust/authorization denials, privileged changes, audit integrity/completeness, secret/egress anomalies; restricted access |
| Usage/cost | Tenant control/FinOps/product owner | authoritative usage state, reservations/reconciliation, cost attribution completeness, anomalous retry/waste; tenant-scoped views |
| Reliability/recovery | Service/database/storage/incident owners | CP-13 failures, dependency outages, stuck reconciliation, restore/integrity/fence epoch, unresolved ambiguity |
| Telemetry pipeline | Operations | export lag/drop/retry, buffer saturation, sampling, redaction/cardinality rejection, backend health and telemetry cost |

Dashboards link to authoritative owner queries/evidence and label delayed, sampled, estimated, stale, or incomplete data. A green dashboard is never promotion or recovery evidence by itself.

## Alert policy and conditions

Alert conditions are versioned policies, not hard-coded numbers in this architecture. Each alert requires logical owner, severity, affected tenant/operation/version, detection window, minimum evidence, suppression/dedupe, runbook/reconciliation action, escalation, and closure verification.

Required condition families:

- invariant violations that alert immediately under the approved incident policy: any cross-tenant observation/effect; `READY` without required integrity/quality/lineage/policy evidence; public success without required result/lineage/audit/usage finalization; accepted stale fence/handler/version effect; revoked/unapproved/ambiguous bundle selection; promotion without immutable evaluation evidence; missing feedback treated as performance evidence; blocked Synapse provider execution; verifier output used as authority; or duplicate/unreconciled usage effect;
- mandatory dependency unavailable; readiness/liveness transition; sustained latency/error relative to an approved target;
- queue oldest-age/deadline risk, scheduler miss, stuck job/finalization, retry/timeout/abandonment surge, stale-fence attempt;
- data freshness/completeness/quality/schema/integrity failure, orphan/missing-object growth, readiness revocation;
- model/artifact load/integrity/revocation/assignment failure, evaluation gate failure, approved drift/performance/safety condition;
- control/audit/usage reservation or reconciliation failure, cross-tenant/privileged/secret/egress anomaly;
- outbox/delivery backlog, endpoint circuit, ambiguity, poison/incompatible schema, dead-letter/expiry when path is admitted;
- restore/recovery epoch, unresolved external effect, deletion manifest, backup/integrity exercise failure;
- telemetry exporter lag/drop/resource/cardinality/redaction/trace-completeness failure.

Cardinality, expected denials/not-eligible outcomes, maintenance/recovery state, and multi-symptom incidents must be deduplicated to avoid alert storms. No production alert is activated without named routing and a tested response.

## SLI catalog and SLO-admission plan

| SLI family | Definition boundary | Required dimensions/exclusions | Current disposition |
|---|---|---|---|
| API success availability | eligible, authenticated operations returning contract-defined non-platform-failure outcome / admitted operations | operation/version; separate expected denial/not-ready/ineligible/client-invalid | Measure; no numeric SLO |
| API latency | ingress acceptance to response by outcome and operation class | sync only; separate queueing/async completion; percentile method TBD | Measure distribution; no target |
| Job admission/completion | accepted commands durably recorded; terminal outcomes by admitted workload | operation/tenant pool, outcome, deadline class; cancellations/ineligibility separate | Measure; no numeric SLO |
| Queue delay/deadline | acceptance-to-first-valid-attempt and completion relative to declared deadline | workload/pool/priority/fairness policy | Measure before Stage 17 target |
| Dataset readiness/freshness | admitted source runs publishing valid ready version; age versus source contract | source/contract/tenant/data class; invalid input separate | Policy per source unresolved |
| Result finalization | owner results whose required lineage/audit/usage obligations finalize | operation/result version; conflicts/held states separate | Measure; target unresolved |
| Model inference/load | eligible requests served by exact approved assignment; load/inference latency/failure | capability/bundle/runtime/outcome; blocked profiles excluded | Profiles unavailable; target prohibited |
| Model/data quality | versioned evaluation metric over approved cohort/window | capability, dataset/bundle, slice, minimum sample, uncertainty | Metrics defined; gates/targets unresolved |
| Reproduction | reproduction jobs with complete immutable reports and exact-or-approved-tolerance match; reference/reconstruction/mismatch outcomes and duration | original manifest, `reproduction_run_id/report_id`, dataset/PIT/environment/bundle, comparison/tolerance version | Measure completeness and match; no success/target inferred without approved profile |
| Delivery | admitted notification intents delivered/acknowledged within policy; dead-letter/ambiguity | consumer/destination/event schema; polling/result success separate | Conditional path; no SLO |
| Audit/trace completeness | required records/links present for sampled or all mandated operations | operation/effect class; mandatory audit distinct from diagnostic trace | Mandatory completeness gate; numeric operational target/retention unresolved |
| Usage/cost accuracy | logical effects with reconciled usage/cost evidence | unit/source/currency/allocation version; retry attempts separate | Measure completeness; budgets unknown |
| Recovery | detection, containment, restore/reconcile/resume durations and unresolved loss/ambiguity | failure class/domain/tenant scope/exercise | Measure exercises; no RPO/RTO objective |
| Telemetry availability | expected diagnostic events/spans/series exported within policy without redaction/cardinality violation | signal class/component; sampling/drop policy | Measure observability blind spots; no business SLO |

No numeric SLO is proposed. Sufficient evidence requires: named service/consumer and owner; operation classification; workload and dependency measurements across representative windows; numerator/denominator and exclusions; latency/quality/freshness distribution; failure/recovery history or exercises; business/scientific consequences; support hours; dependency commitments; target and error-budget response; cost; and sponsor approval. Stage 17 may evaluate candidate objectives but cannot infer them from current logs or service-card wish lists.

## Telemetry outage and degradation behavior

| Failure | Detection | Behavior | Forbidden behavior |
|---|---|---|---|
| Local emitter/buffer unavailable | internal error/drop counter and health state | Continue only if bounded and all authoritative evidence succeeds; drop/sample by policy | Block indefinitely, exhaust process, or dump payloads |
| Exporter/backend unavailable | queue age/retry/drop/backend health | Bounded retry/backoff, degrade telemetry health, preserve local owner truth | Retry storm or report business failure/success from export state |
| Cardinality/volume explosion | series/event rejection, buffer/resource budget | Reject unsafe dimensions, sample/aggregate, alert owner | Remove tenant isolation or include raw identifiers to debug |
| Redaction/classification failure | schema/allowlist validation, canary tests | Stop unsafe export, quarantine bounded protected evidence, security incident | Export secrets/PII then rely on later deletion |
| Trace context missing/corrupt | ingress/async-link validation and completeness checks | Generate trusted root for new admissible boundary or reject when required for durable evidence | Accept caller baggage as tenant/authority |
| Clock skew | timestamp/order/lease anomaly | Mark evidence unreliable, use owner sequence/version for truth, alert | Reorder business state from wall-clock telemetry |
| Mandatory audit/lineage/usage writer unavailable | owner write/finalization failure | Follow Stage 12/13 fail-closed or held-finalization contract | Substitute diagnostic log/metric/span |

## Anti-overengineering assessment

| Component/pattern | Disposition | Reason |
|---|---|---|
| Structured telemetry interface and correlation library | Required now | Every component/path needs consistent safe signals and linkage |
| Authoritative audit/usage/evaluation records | Required now | Security, lineage, cost and promotion decisions cannot depend on sampled telemetry |
| Vendor-neutral metrics/log/trace exporters | Required logical seam | Placement/backend deferred; avoids coupling modules to a product |
| Separate observability microservice/platform | Unjustified now | Logical responsibility can run in the approved modular monolith/runtime roles |
| Per-tenant label on every metric | Rejected | Cardinality/privacy risk; authoritative tenant views come from ledger/query contracts |
| Full-fidelity tracing of every payload | Rejected | Privacy/cost burden; traces carry metadata and protected references only |
| APM/vendor, SIEM, data-quality platform, model-monitoring product | Optional/deferred | No environment, scale, compliance, procurement, or unique capability evidence |
| Numeric universal SLO/error budget | Rejected now | Operations differ and evidence/ownership is absent |
| Agent tracing platform | Not applicable | No agent selected; future agent reopens the gate |

## Recommendations

### R-14-01 — Standardize one safe correlation and signal envelope

**Requirement/where:** `ARK-NFR-001/002/006`; every Stage 05 component and CP-13 path. **Why now:** fragmented logs cannot prove end-to-end identity, versions, or failure truth. **Simplest implementation:** shared typed context/event interfaces in the modular monolith, propagated across durable boundaries. **Alternative:** component-specific text logs. **Why rejected:** unsafe, unqueryable, and incomplete. **Trade-off:** schema/version governance and cardinality discipline. **Reconsideration:** export protocols/backends may change after Stage 15/17 evidence; the logical envelope remains.

### R-14-02 — Keep authoritative evidence inline and diagnostic export asynchronous

**Requirement/where:** security, reliability, usage, lineage, and all critical paths. **Why now:** telemetry outages must not fabricate or authorize business outcomes. **Simplest implementation:** owner transactions for audit/lineage/usage/evaluation obligations plus bounded diagnostic exporters. **Alternative:** one log/trace pipeline for audit and operations. **Why rejected:** sampling/loss/availability/access semantics conflict. **Trade-off:** two correlated evidence paths. **Reconsideration:** none without preserving authority separation.

### R-14-03 — Define SLIs now and admit SLOs only through measured owner decisions

**Requirement/where:** source Section 13, `ARK-NFR-007`, Stages 14/17/20. **Why now:** instrumentation must collect the distributions needed for later targets. **Simplest implementation:** versioned SLI definitions and measurement reports; no numeric target yet. **Alternative:** generic availability/latency percentages. **Why rejected:** workload, consequence, hours, dependencies, and owner are unknown. **Trade-off:** production commitments remain blocked; claims remain honest. **Reconsideration:** Stage 17 evidence plus sponsor-approved owner/target register.

### R-14-04 — Treat capability evaluation as immutable decision evidence, not dashboard metrics

**Requirement/where:** `ARK-FR-009/012`, ADR-007, all seven profiles. **Why now:** promotion and availability require reproducible cohort/version/gate context. **Simplest implementation:** immutable evaluation reports referenced by registry/promotion records, with trends projected asynchronously. **Alternative:** promote from current dashboard value. **Why rejected:** windows, slices, uncertainty, lineage, and authority disappear. **Trade-off:** explicit evaluation pipelines/review. **Reconsideration:** thresholds can evolve through versioned policy, not bypass the record.

## Decisions

- Adopt the observability invariants, correlation envelope, inline/export split, health contract, component and critical-path matrices, data/capability evaluation contracts, usage/cost evidence, dashboard/alert register, SLI definitions, and telemetry-outage behavior as the Stage 14 baseline, subject to sponsor approval.
- Do not propose a new ADR: Stage 14 operationalizes accepted audit, lifecycle, reliability, and ownership boundaries without selecting a product/topology or superseding a material decision.
- Preserve all four `MIGRATION_BLOCKED`, three `EVIDENCE_BLOCKED`, and eight ADR-008 security-admission blocks. Signals and dashboards are evidence, not admission.
- Record agent traces as not applicable to the current architecture. Any production-agent proposal must reopen Stage 11 and add its bounded plan/tool/memory/action trace contract here.
- Keep Stage 15 unstarted until Stage 14 passes its gate and the sponsor explicitly authorizes continuation.

## Contradictions and dangerous assumptions

| ID | Finding | Resolution | Consequence |
|---|---|---|---|
| `C-14-01` | Service-card metric names include `{tenant}` and direct business IDs, while Stage 12 requires privacy/cardinality control | Tenant-qualified evidence remains in owner ledger/query views; shared telemetry uses safe bounded dimensions | No indiscriminate tenant labels or raw identifiers |
| `C-14-02` | “Audit logs” can imply ordinary log export | Define audit as immutable authoritative records with separate access/failure semantics | Diagnostic pipeline cannot authorize/backfill effects |
| `C-14-03` | Health or green dashboards may be mistaken for capability readiness/promotion | Health, dataset readiness, scientific eligibility, evaluation and production admission remain separate | No green-metric production enablement |
| `C-14-04` | Current prototype logs/CSVs look like acceptable evaluation evidence | Treat them as migration inputs only; require typed immutable reports and safe telemetry | Four profiles remain `MIGRATION_BLOCKED` |
| `C-14-05` | Synapse response `cost` may look like authoritative billing or sufficient monitoring | It is interface evidence only until provider/model/usage semantics and reconciliation are approved | Three profiles remain `EVIDENCE_BLOCKED` |
| `C-14-06` | SLO request could pressure invention of numeric targets | Define measurable SLIs and explicit admission evidence; no numeric SLO now | Stage 17/20 remain required |
| `C-14-07` | Telemetry loss can tempt raw payload logging or synchronous blocking | Bounded degradation, redaction fail-stop, and authoritative owner evidence prevail | Visibility may degrade without privacy/reliability bypass |
| `C-14-08` | Per-tenant usage can be confused with automated billing | Usage/metering is in scope; prices, allocation, invoicing/payment remain unresolved | No commercial commitment |
| `C-14-09` | Absence of a trace/log can be mistaken for proof that an operation did not occur | Recovery/security consult authoritative owner and audit state; telemetry gaps are diagnostic incidents | No unsafe replay, denial, or exoneration from missing telemetry |

## Open questions

| ID | Question | Blocking? | Options | Recommended temporary assumption | Effect |
|---|---:|---|---|---|---|
| `Q-14-01` | Which telemetry/export/storage products and deployment locations apply? | Before Stage 15 implementation choice | Existing stack; managed product; self-hosted | Keep vendor-neutral interfaces | No product/topology claim |
| `Q-14-02` | What retention, sampling, cardinality, redaction, access, residency, and deletion policies apply by signal/evidence class? | Before production | Per-class governed policies | Minimum safe fields; no raw PII; block unsafe export | Storage/cost/compliance unresolved |
| `Q-14-03` | What numeric SLOs, alert thresholds, windows, maintenance exclusions, and error-budget actions apply per operation? | Before production commitment | Tiered per operation/tenant; best effort; none | Measure SLIs first | No availability/performance promise |
| `Q-14-04` | Who owns each dashboard, alert, runbook, quality gate, incident and on-call route? | Before production | Named roster and escalation | Logical roles under `A-04-OWNERSHIP` | No production alert routing claim |
| `Q-14-05` | Which model/data/business metrics, cohorts, minimum samples, fairness/safety policies, thresholds and promotion authority apply per capability? | Before profile activation | Capability-specific approved gate record | No production gate inferred | All profiles remain blocked |
| `Q-14-06` | What usage units, prices, currencies, allocation, budget, retry charging, and invoicing boundaries apply? | Before billing/budget enforcement | Showback; quotas only; approved billing policy | Record quantities/evidence only | No price/budget/billing claim |
| `Q-14-07` | What authority and evidence interface does LAB have? | Before release acceptance | Advisory evidence consumer; required technical gate; promotion veto | External validation consumer only | LAB cannot silently approve promotion |
| `Q-14-08` | What authoritative provider/model/prompt/token/cost/safety telemetry exists for Synapse? | Before any Synapse request | Supply evidence; self-hosted evidence; scope out; remain unavailable | Remain blocked | No LLM SLI/SLO/evaluation claim |

## Requirements-traceability updates

| Requirement | Stage 14 design evidence | Validation evidence required later |
|---|---|---|
| `ARK-FR-001` | Control, quota, usage, policy and audit signals remain owner-qualified | Decision/reservation/usage/audit trace tests |
| `ARK-FR-002/003` | Ingestion/data-quality/readiness/lineage metrics and alerts | Invalid/stale/duplicate/orphan and trace-completeness suites |
| `ARK-FR-004/005/006` | Capability outcome/version/eligibility/result signals | Contract/outcome/correlation and no-fabricated-success tests |
| `ARK-FR-007/008` | Job/scheduler/worker state, queue, retry, fence, cancellation and finalization evidence | Fault/load/state-transition and trace-link tests |
| `ARK-FR-009` | Immutable evaluation, bundle, assignment, drift and load/inference evidence | Reproduction/promotion/rollback/quality-gate tests |
| `ARK-FR-010/011` | Phase A/B/effect and delivery signals without authority collapse | Revocation/dedupe/ambiguity/dead-letter/audit tests |
| `ARK-FR-012` | LAB-consumable contracts, evaluation, isolation, reproducibility and failure evidence | Release-scoped evidence export and access tests |
| `ARK-NFR-001/005` | Tenant-qualified owner evidence, safe telemetry fields, redaction/access/cardinality | Cross-tenant/PII/secret/telemetry-access negative tests |
| `ARK-NFR-002/006` | Common identity/version graph across APIs/jobs/data/models/events/effects/audit/usage | End-to-end trace and missing-link reconciliation tests |
| `ARK-NFR-003` | Security/audit/integrity/denial signals and fail-closed outage behavior | Tamper, outage, redaction and privileged-operation tests |
| `ARK-NFR-004` | Retry/attempt/fence/duplicate/ambiguity/reconciliation metrics | Crash/timeout/duplicate/stale-fence fault injection |
| `ARK-NFR-005` | Tenant/pool resource and noisy-neighbor observations without unsafe labels | Isolation/backlog/cardinality/load tests |
| `ARK-NFR-007` | Versioned SLI catalog and explicit SLO admission plan | Stage 17 measured targets and cost evidence |
| `ARK-CON-001/002/005` | Shared logical telemetry interfaces, owner records, PostgreSQL-first truth | Dependency/schema/outbox and extraction-boundary tests |
| `ARK-CON-007` | No product, agent platform, universal SLO, or speculative service added | Stage 23 anti-overengineering review |
| `SC-02-04/05/06/08/09/10/11/12` | Outcome truth, recovery, isolation, no-action, owner signals, target blocks, and evaluation evidence | Stage 16 suites and Stage 20 owner/target records |

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Every governing source bullet dispositioned | PASS | Source-instruction coverage table |
| Every Stage 05 component has owner-relevant signals | PASS | `C05-01` through `C05-22` component matrix |
| Every component has correlation/version fields | PASS | Common correlation contract plus component matrix |
| Every component has alert/gate conditions | PASS | Component matrix and alert policy |
| Every component has telemetry-outage behavior | PASS | Component matrix and outage table |
| Every Stage 13 critical path covered | PASS | `CP-13-01` through `CP-13-08` workflow matrix |
| Structured logs, metrics, traces, health, dashboards and alerts defined | PASS | Dedicated contracts/registers |
| Operational telemetry separated from audit/compliance records | PASS | Invariants and inline/export matrix |
| Per-tenant usage and cost addressed safely | PASS | Usage/cost contract and `C-14-01/C-14-08` |
| Data/model/LLM quality and evaluation covered | PASS WITH BLOCKS PRESERVED | Data matrix and seven-capability matrix |
| Agent traces dispositioned | PASS — NOT APPLICABLE | No current agent; explicit future re-entry condition |
| SLIs defined and unsupported SLOs not invented | PASS | SLI catalog and SLO-admission plan |
| Authorized specialist reviews reconciled | PASS | Platform and data/ML final passes reported no critical, high, or material medium defect and recommended `PASS` |
| No Stage 15 design or production enablement | PASS | Scope, decisions, open questions and stop condition |

**Gate result: PASSED AND APPROVED.** Every Stage 05 component and Stage 13 critical path has owner-relevant signals, correlation/version identities, alert/gate conditions, and telemetry-outage behavior. Structured logs, metrics, traces, health, dashboards, alerts, authoritative audit, per-tenant usage, cost, data/model quality, reproduction, and agent-trace applicability are dispositioned. SLIs and measurement plans are defined without unsupported SLOs. Both authorized specialists reported no unresolved critical, high, or material medium defect after reconciliation, workspace structure/source-integrity validation passed, and the sponsor explicitly approved Stage 14 on 2026-08-13, authorizing Stage 15 only.

## Downstream consequences

- Stage 15 must place logical emitters/exporters, evidence stores, health endpoints and access boundaries within an approved environment without selecting topology from Stage 14 alone.
- Stage 16 must test telemetry schemas, correlation completeness, audit separation, redaction, cardinality, outage degradation, every component/path alert condition, and capability evaluation records.
- Stage 17 must collect representative SLI/resource/usage/cost distributions and may propose numeric targets only with owners, consequences, and measured evidence.
- Stage 20 must name dashboard/alert/runbook/on-call, scientific gate, security/audit, usage/cost, and LAB-interface owners.
- Stage 23 must retain the anti-overengineering rejection of a separate observability service, universal tenant labels, full-payload tracing, agent tracing platform, and unsupported monitoring products/SLOs.

## Exact next-stage inputs and stop condition

Stage 14 is approved and Stage 15 is authorized. Do not execute Stage 16.

Stage 15 must read:

1. Approved `outputs/stages/00-source-audit.md` through `outputs/stages/14-observability-evaluation.md`
2. Accepted ADR-000 through ADR-008
3. `sources/normalized/system-design-prompt.md` section **14. Deployment and infrastructure**
4. Current environment/deployment evidence selected through `SOURCE_MANIFEST.md`, if any
5. `stages/15-deployment-infrastructure.md`, `templates/stage-output.md`, and directly referenced placement matrices

Execute Stage 15 only. Do not begin Stage 16 until Stage 15 passes its gate and the sponsor explicitly authorizes continuation.
