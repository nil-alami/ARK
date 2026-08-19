# Stage 03 — Capability and service inventory

Status: `APPROVED`

## Purpose and scope

Inventory every named ARK ML/AI capability and express its current evidence, intended ARK contract, ownership boundary, production-readiness gaps, migration work, and acceptance conditions. This stage does not choose physical services, vendors, deployment topology, numeric operating targets, or release sequence.

The sponsor approved Stage 03 and its outputs on 2026-08-11, including the temporary dispositions in `decisions/ADR-002-stage-03-capability-evidence-disposition.md`.

## Inputs read in full

- `AGENTS.md`
- `WORKFLOW.md`
- `STATUS.md`
- `SOURCE_MANIFEST.md`
- `stages/STAGE-CONTRACT.md`
- `stages/03-capability-inventory.md`
- `templates/stage-output.md`
- `templates/service-contract.md`
- `templates/requirements-traceability.md`
- `sources/normalized/system-design-prompt.md`, especially **2. Capability and service inventory**
- `sources/normalized/ark-assumptions.md`
- `sources/normalized/service-cards/churnobyl.md`
- `sources/normalized/service-cards/RFM.md`
- `sources/normalized/service-cards/next_purchase_prediction.md`
- `sources/normalized/service-cards/recommender.md`
- `sources/normalized/service-cards/Synapse_chatbot.md`
- `sources/normalized/service-cards/synapse_message_generator.md`
- `sources/normalized/service-cards/synapse_campaign_verifier.md`
- `outputs/stages/00-source-audit.md`
- `outputs/stages/01-discovery-and-questions.md`
- `outputs/stages/02-system-definition.md`
- `decisions/ADR-000-temporary-source-evidence-disposition.md`
- `decisions/ADR-001-stage-01-requirements-baseline.md`

## Source-instruction coverage

| Governing instruction | Coverage in this artifact |
|---|---|
| Identify business capabilities and proposed modules/services | Inventory summary and seven capability contracts |
| Provide purpose, value, owner, inputs/outputs, invocation, dependencies, processing, lifecycle, state, configuration, eligibility, reliability, evaluation, security, operation, and migration | Common ARK contract plus each capability's template-aligned subsections |
| Separate shared platform from capability responsibilities | Responsibility-boundary table and per-capability ownership subsections |
| Separate current facts, intended contract, and migration work | Evidence notation and explicit `Current`, `Intended`, and `Migration` entries |
| Do not omit a named capability | All seven physical cards are mapped one-to-one below |
| Apply the evidence gate | Synapse internals and missing accountable owners remain unresolved; proposed dispositions are in ADR-002 |
| Use authorized analysts | One configured `capability_analyst` review was run per card; the primary agent reconciled all results and is the only writer |

## Evidence notation

- **`FACT`** — explicit evidence from an admitted source. For six normalized-only cards, this remains temporary evidence under `ADR-000`.
- **`IFACE`** — explicit Synapse interface fact only. It says nothing about undocumented implementation behavior.
- **`ARK`** — an approved ARK baseline decision or stable Stage 02 requirement.
- **`ASSUMPTION`** — temporary treatment requiring the cited approval and expiry.
- **`RECOMMENDATION`** — proposed target behavior, not an approved implementation choice.
- **`UNRESOLVED`** — evidence is absent or conflicting; no conventional behavior is inferred.

## Facts

### Capability inventory

| ID | Named capability/card | Business use | Evidence class | Current execution evidence | Stage 03 readiness |
|---|---|---|---|---|---|
| `CAP-CHURN` | Churn / Churnobyl | Produce customer churn risk for retention use | Original-backed normalized card | Synchronous tenant batch, scheduled batch, and new-transaction path | Non-production migration evidence |
| `CAP-RFM` | RFM / Shepherd | Segment customers by recency, frequency, and monetary behavior | Checksum-pinned normalized-only card | Synchronous tenant batch and daily process-local schedule | Non-production migration evidence |
| `CAP-NPT` | Next purchase prediction / Nostradamus | Estimate whether and when a customer will purchase again | Checksum-pinned normalized-only card | Commented/inactive synchronous tenant batch | Explicitly not production-ready |
| `CAP-REC` | Recommendation / REC | Rank products for a customer | Checksum-pinned normalized-only card | In-process/CLI tenant batch; supporting metadata/feedback APIs | Non-production migration evidence |
| `CAP-SYN-CHAT` | Synapse chatbot | Return a conversational LLM response to supplied customer context/history | Checksum-pinned interface-only card | Synchronous HTTP request/response | Interface known; internals unresolved; not production-eligible |
| `CAP-SYN-MSG` | Synapse message generator | Return Persian churn or occasion marketing text | Checksum-pinned interface-only card | Two synchronous HTTP operations | Interface known; internals unresolved; not production-eligible |
| `CAP-SYN-VERIFY` | Synapse campaign verifier | Return an LLM assessment of supplied campaign material | Checksum-pinned interface-only card | Synchronous HTTP request/response | Interface known; internals unresolved; not production-eligible |

No named capability is physically missing. The three Synapse cards lack the internal evidence needed for a production-capable contract, and all seven lack named accountable owners. Evidence: the seven cards' **ML SERVICE CARD**, **OWNERSHIP**, and **INFRASTRUCTURE CLASSIFICATION** sections; `ADR-000 — Decision`.

### Shared platform versus capability responsibility

| Concern | Shared ARK platform responsibility | Capability responsibility | Forbidden inference/access |
|---|---|---|---|
| Identity and tenancy | Authenticate principal; derive tenant context; authorize entitlement and scoped grants | Validate capability-specific identifiers within the authenticated tenant | Body `businessId` or phone number is not tenant authority |
| Contracts and lifecycle | Common envelope, request/idempotency identity, durable job/result state, cancellation, standard outcomes | Versioned operation/input/output schemas and capability-specific status reasons | Capability cannot invent a separate platform lifecycle |
| Data readiness | Register immutable tenant-scoped dataset versions; structural/semantic/policy checks and lineage | Define minimum scientific data, feature semantics, freshness, eligibility, and fallback | No unrestricted shared SQL or private-store reads |
| ML lifecycle | Registry interfaces, immutable artifact lineage, authorization and audit mechanisms | Training/evaluation/promotion policy, model/feature/config selection, rollback criteria | Inference cannot implicitly train or activate |
| State | Tenant-isolated storage primitives and access controls | Own capability results, private artifacts, configuration, evaluation evidence, and migrations | No cross-capability writes or consumer-schema ownership |
| External action | Grants, permission/policy checks, quotas, deduplication, freshness, audit, and outward-action adapter | Return an outcome or advisory recommendation | No capability response alone authorizes or sends an action |
| Observability | Correlation, audit, usage/metering envelope, common telemetry interfaces | Capability quality, drift, fallback, model, and runbook signals | No unnecessary raw PII in telemetry |
| Deployment | Later stages determine placement from evidence | Declare execution/resource characteristics and constraints | Logical ownership does not imply a microservice |

Evidence: `sources/normalized/ark-assumptions.md — Product and architecture`, **Integration and contracts**, **Data and ML**, **Security, ownership, and operations**; `outputs/stages/02-system-definition.md — Functional requirements`, **Non-functional requirements**, **Constraints**.

## Assumptions

The following assumptions became active when the sponsor accepted `ADR-002` on 2026-08-11:

| ID | Temporary treatment | Expiry |
|---|---|---|
| `A-03-OWNERSHIP` | Preserve one logical owner boundary per capability; accountable names remain `TBD`; prohibit production readiness/promotion until assigned | Before Stage 04 approval or authoritative assignments, whichever is earlier |
| `A-03-ML-MIGRATION` | Treat current Churn/RFM/NPT/REC algorithms, thresholds, contracts, state, and defects as migration evidence; use the intended contract below as provisional target requirements | Per capability on approved remediation/lifecycle evidence, no later than relevant Stage 10/16 decisions |
| `A-03-SYNAPSE` | Retain all three Synapse capabilities as interface-only and non-production-eligible; preserve all undocumented internals as unresolved; verifier output is advisory only | Authoritative evidence, explicit scope-out, or the relevant Stage 10/12/14/15 or production-enablement decision |

Accepted `ADR-002` replaces the expired `A-01-ML` treatment for ML-01, ML-04, ML-05, and ML-06 at this gate. Other `A-01-*` assumptions remain active only to their recorded expiry points.

## Common intended ARK contract inherited by all seven capabilities

Each contract below inherits these target requirements; capability-specific differences and unresolved facts follow it.

- **Operational envelope:** authenticated tenant context; request and idempotency identity; operation and execution mode; contract/configuration/code versions; dataset references; model/artifact versions when applicable; callback only where approved; correlation context.
- **Invocation:** synchronous only after measured short and predictable runtime; otherwise a durable asynchronous job with accepted/queued/running/terminal states and result reference. No numeric boundary is invented.
- **Readiness:** distinguish request validation, dataset readiness, platform eligibility, scientific/capability eligibility, and execution result. Capability outcomes are `ELIGIBLE | DEGRADED | FALLBACK | INELIGIBLE`; missing/unready data is not fabricated.
- **Lifecycle:** training, evaluation, promotion, activation, rollback, and retirement are explicit authorized operations. Inference does not train or activate.
- **Results:** bounded, versioned, consumer-neutral schema; small results may be inline and large results use tenant-scoped references; include explicit outcome/reason and sufficient lineage for reproducibility.
- **Reliability:** define idempotency, retryability, cancellation, timeout, partial/degraded behavior, dependency failure, replay, and at-least-once handling before production admission.
- **Security/privacy:** principal-derived tenant identity, least privilege, opaque tenant-scoped customer identifiers, data minimization, controlled external-provider transfer, secrets isolation, and no cross-tenant access.
- **Observability/evaluation:** tenant/request/job correlation; input, feature, model, prompt/policy/config/code/execution versions; latency, outcome, failures, fallback, resource/usage/cost; capability-specific quality and drift evidence; privacy-safe audit.
- **Production admission:** named owner/runbook, approved contract, measured operating targets, passing isolation/reliability/quality/safety tests, and promotion evidence.

Evidence: `outputs/stages/02-system-definition.md — ARK-FR-004` through `ARK-FR-012`, `ARK-NFR-001` through `ARK-NFR-007`, `ARK-CON-001` through `ARK-CON-007`; `sources/normalized/system-design-prompt.md — 2. Capability and service inventory`.

---

## Capability contract — CAP-CHURN: Churn / Churnobyl

### Identity and business purpose

- **Capability ID/version:** `CAP-CHURN`; current service `churnobyl` `0.1.0`, API `v1` (`FACT`).
- **Business value:** provide churn risk to support retention prioritization (`FACT`); business KPI and acceptance target are `UNRESOLVED`.
- **Owner:** card says `TBD`; intended logical owner is CAP-CHURN; accountable product/ML/operations owners are `UNRESOLVED`.
- **Current implementation evidence:** detailed prototype with material security, lifecycle, correctness, and ownership defects.
- **Intended ARK boundary:** own churn feature semantics, training/evaluation/promotion, eligibility, score/result contract, configuration, artifacts, and runbook; not shared profiles, platform lifecycle, or outbound action.

Evidence: `churnobyl.md — ML SERVICE CARD`, **1. PURPOSE**, **14. OWNERSHIP / ISOLATION**.

### Operations and invocation

| Operation | Current fact | Intended ARK treatment |
|---|---|---|
| Tenant churn scoring | `POST /api/v1/services/run/`; synchronous full-tenant run | Durable async `churn-score-batch`; result by job/result reference |
| Scheduled scoring | Process-local daily schedule at 11:01 | External durable schedule submits the same idempotent operation; exact cadence remains tenant policy/TBD |
| New transaction | Dedicated API path documented | Event or request trigger must resolve immutable input and active versions; exact trigger remains unresolved |
| Training | Missing model can cause training during inference | Explicit separately authorized train/evaluate/promote/activate operations |

Current latency, timeout, concurrency, batch-size, and availability targets are `UNRESOLVED`. Evidence: `churnobyl.md — 2. TRIGGER / EXECUTION MODE`, **5. HIGH-LEVEL WORKFLOW**, **9. EXECUTION PROFILE**, **12. INTEGRATION**.

### Input contracts

- **Current:** tenant/business identifier plus BCDP customer/profile and transaction-derived fields. Features include churn candidate, monetary slope, buy counts, gap ratio, extrema, and churn window; mobile/phone and Whatson identifiers appear in the implementation evidence.
- **Current hazard:** schemas, authoritative feature definitions, tenant binding, immutable dataset identity, and common envelope are incomplete.
- **Intended:** common envelope plus a registered churn feature-dataset reference; versioned schema defining opaque customer ID, observation/as-of time, transaction window, churn labels, feature names/types/units/nullability, and training versus inference purpose.
- **Required/optional fields and exact dataset schema:** `UNRESOLVED`; current fields are compatibility evidence, not an accepted target schema.

Evidence: `churnobyl.md — 3. INPUT CONTRACT`, **4. OUTPUT CONTRACT**, **5. HIGH-LEVEL WORKFLOW**.

### Data readiness and capability eligibility

- **Current:** card documents feature/customer availability checks and hard score overrides; completeness, freshness, lineage, and policy readiness are insufficiently specified.
- **Intended dataset readiness:** authenticated tenant, immutable validated feature dataset, observation time, required transaction coverage, label/feature version, and active artifact.
- **Scientific eligibility:** capability-owned minimum history and model applicability; exact thresholds are `UNRESOLVED`.
- **Outcomes:** explicit eligible/degraded/fallback/ineligible reasons. New or insufficient-history customers may use an approved neutral fallback, but the documented forced `0`/`100` outputs are not approved production semantics.

### Processing and ML lifecycle

- **Current preprocessing/model:** StandardScaler and XGBoost; current run may train on the scoring batch, refit the scaler during inference, and activate implicitly.
- **Current hazards:** uncalibrated probability-like score; new customers forced to `0`; missing old customers forced to `100`; same-batch fitting; nondurable/process-local scheduling.
- **Intended:** fixed versioned feature pipeline; separate training dataset; evaluated model and calibration policy; explicit artifact lineage and promotion; immutable active model/scaler/feature versions selected before inference.
- **Evaluation:** discrimination, calibration, segment/tenant stability, label leakage, drift, forced/fallback behavior, reproducibility, and business usefulness; numeric gates and promotion authority are `UNRESOLVED`.

Evidence: `churnobyl.md — 5. HIGH-LEVEL WORKFLOW`, **6. ELIGIBILITY / PRECONDITIONS**, **10. CONFIGURATION**, **11. FAILURE / FALLBACK**.

### Output contracts

- **Current:** per-customer churn score/status and persistence into shared BCDP/profile structures; exact consumer-neutral schema is not established.
- **Intended:** tenant-scoped result reference or bounded rows containing opaque customer ID, observation time, score with defined scale/semantics, optional calibrated probability only if validated, eligibility/fallback reason, explanation reference, and full dataset/feature/model/config/code/execution lineage.
- **Status/error:** inherit the common outcome model; do not report success when authoritative persistence fails.
- **Events:** no accepted event contract yet; `UNRESOLVED`.

### Ownership and dependencies

- **Current reads/writes:** full BCDP/shared profile, generic model handler, process registry/status; cross-capability and shared-state writes violate the intended boundary.
- **Intended owned state:** churn datasets/features where capability-specific, model/scaler artifacts, evaluations, active-version bindings, results, configuration, and migrations.
- **Approved interfaces:** shared dataset registry, artifact registry, job lifecycle, result store, and an external projection adapter.
- **Forbidden:** direct shared-profile mutation, other capability state, raw phone as platform identity, unrestricted shared SQL.
- **Migration:** replace direct BCDP writes with owned result plus separately governed projection; replace process-local registry/scheduler and implicit training.

### Configuration, reliability, and operation

- **Configuration:** all thresholds/windows/model parameters must be versioned; current values are evidence only. Tenant override policy is `UNRESOLVED`.
- **Reliability:** add idempotent durable batch, restart/checkpoint/replay, bounded dependency failures, truthful terminal status, cancellation, and partial-result policy.
- **Security/privacy:** enforce principal-derived tenant; replace phone/mobile use with opaque IDs where possible; least-privilege reads and no cross-tenant model/result access.
- **Observability/quality:** stage/job latency, counts, readiness/fallback, feature quality/drift, calibration/discrimination, active versions, write failures, and resource use; targets TBD.
- **Scaling/runbook:** resource profile, SLOs, recovery, and named on-call/runbook owner are `UNRESOLVED`.

### Gaps, assumptions, decisions, and acceptance tests

- **Gaps:** accountable owner, exact target schema, label policy, thresholds, calibration/promotion gates, capacity/SLO, fallback, and migration compatibility.
- **Assumption needed:** `A-03-OWNERSHIP` and `A-03-ML-MIGRATION`.
- **Acceptance:** inference never trains/activates; repeated batch is idempotent; scores are reproducible from lineage; forced-score behavior is removed or explicitly approved/evaluated; cross-tenant and direct-profile-write tests fail safely; dependency-write failure cannot yield false success.
- **Traceability:** `ARK-FR-004`–`009`, `ARK-NFR-001`–`007`, `ARK-CON-002`–`003`, `SC-02-04`, `SC-02-06`, `SC-02-09`–`011`.

---

## Capability contract — CAP-RFM: RFM / Shepherd

### Identity and business purpose

- **Capability ID/version:** `CAP-RFM`; current `shepherd` `0.1.0`, API `v1` (`FACT`, temporary evidence).
- **Business value:** segment customers using recency, frequency, and monetary behavior for downstream targeting; KPI/acceptance target `UNRESOLVED`.
- **Owner:** `TBD`; intended logical owner CAP-RFM; accountable authorities `UNRESOLVED`.
- **Current implementation evidence:** detailed prototype with semantic, versioning, lifecycle, and persistence defects.
- **Intended ARK boundary:** own RFM feature semantics, segment policy/model lifecycle, eligibility, results, evaluation, and runbook.

Evidence: `RFM.md — ML SERVICE CARD`, **1. PURPOSE**, **14. OWNERSHIP / ISOLATION**.

### Operations and invocation

| Operation | Current fact | Intended ARK treatment |
|---|---|---|
| Combined tenant run | Synchronous full-tenant endpoint; no independently valid public RFM endpoint | Durable async `rfm-segment-batch` operation |
| Scheduled run | Process-local daily 11:01 | External durable scheduler submits same idempotent job; cadence TBD |
| Training | Missing model may train during inference | Explicit train/evaluate/promote/activate lifecycle |

Latency/resource/availability targets are `UNRESOLVED`. Evidence: `RFM.md — 2. TRIGGER / EXECUTION MODE`, **5. HIGH-LEVEL WORKFLOW**, **9. EXECUTION PROFILE**, **12. INTEGRATION**.

### Input contracts

- **Current:** RFM recency, frequency, monetary values plus mobile and business identifiers; direct BCDP/profile access.
- **Current hazard:** feature alias mismatch means configured weights may not apply; feature semantics and window/as-of definitions are not stable contracts.
- **Intended:** common envelope plus immutable RFM feature-dataset reference with opaque customer ID, as-of time, transaction window, recency units/direction, frequency definition, monetary unit/currency policy, null/outlier policy, and schema/feature version.
- Exact target fields, minimum data, and tenant configuration remain `UNRESOLVED`.

### Data readiness and capability eligibility

- **Current:** structural availability and clustering preconditions are partial; downstream range expectations conflict with produced labels.
- **Intended:** dataset freshness/completeness/policy readiness separate from scientific minimum population, nonzero variance, stable features, active mapping/model, and supported tenant configuration.
- **Outcomes:** explicit eligible/degraded/fallback/ineligible; no silent per-run semantic change.
- Exact sample/coverage/stability thresholds are `UNRESOLVED`.

### Processing and ML lifecycle

- **Current:** StandardScaler, optional PCA, KMeans with five clusters; label ordering is recalculated per run.
- **Current defects:** weights may not apply; recency is not inverted for desirable-value ordering; per-run relabeling is unstable; Boolean/DataFrame and model upload/load contracts mismatch; registry selection can be nondeterministic; consumers may accept label `5` although output is `0..4`.
- **Intended:** versioned deterministic RFM transformation and segment-label semantic policy; explicit choice of fixed rules versus trained clustering; stable label mapping; explicit artifact lifecycle; no request-time training.
- **Evaluation:** cluster stability/separation, semantic ordering, population coverage, drift, reproducibility, downstream usefulness, and fairness/segment sanity; gates TBD.

Evidence: `RFM.md — 3. INPUT CONTRACT`, **4. OUTPUT CONTRACT**, **5. HIGH-LEVEL WORKFLOW**, **10. CONFIGURATION**, **11. FAILURE / FALLBACK**.

### Output contracts

- **Current:** segment enum `0..4` plus history, stored in shared profile structures; semantic meaning can change per run.
- **Intended:** result rows with opaque customer ID, as-of time, stable segment code and versioned business meaning, R/F/M components or explanation reference, eligibility/fallback reason, and feature/model/mapping/config/code/execution lineage.
- **Status/error/events:** inherit common model; accepted event contract is `UNRESOLVED`.

### Ownership and dependencies

- **Current:** direct BCDP/shared database/model-handler/process-status access and cross-capability orchestration.
- **Intended owned state:** RFM feature definitions, optional model/artifacts, mapping policy, evaluations, results/history, configuration, migrations.
- **Forbidden:** shared-profile mutation, other capability orchestration/state, phone as authority, unrestricted model lookup.
- **Migration:** extract a standalone capability operation; move projection outside CAP-RFM; make mapping/artifact selection deterministic.

### Configuration, reliability, and operation

- **Configuration:** feature weights, window, number of segments, PCA/model parameters, mapping policy, and fallbacks must be versioned; current values are not production decisions.
- **Reliability:** durable idempotent job, deterministic rerun, no success on failed persistence, cancellation/partial policy, and stable artifact lookup.
- **Security/privacy:** tenant isolation, opaque IDs, least privilege, minimized telemetry.
- **Observability/quality:** population/readiness, feature distributions, cluster stability, mapping versions, drift, output distribution, failures, latency/resource use; thresholds TBD.
- **Runbook/scale:** `UNRESOLVED`.

### Gaps, assumptions, decisions, and acceptance tests

- **Gaps:** owner, stable label semantics, algorithm choice, feature definitions, thresholds/gates, exact output schema, capacity/SLO.
- **Assumption needed:** `A-03-OWNERSHIP` and `A-03-ML-MIGRATION`.
- **Acceptance:** configured weights take effect; recency direction is policy-correct; same inputs/versions reproduce labels; emitted enum matches schema; missing model never triggers inference training; no cross-tenant or shared-profile writes; job replay is idempotent.
- **Traceability:** `ARK-FR-004`–`009`, `ARK-NFR-001`–`007`, `ARK-CON-002`–`003`, `SC-02-04`, `SC-02-06`, `SC-02-09`–`011`.

---

## Capability contract — CAP-NPT: Next purchase prediction / Nostradamus

### Identity and business purpose

- **Capability ID/version:** `CAP-NPT`; current `nostradamus` `0.1.0` (`FACT`, temporary evidence).
- **Business value:** predict purchase recurrence and timing for planning/engagement; KPI and consumer decision semantics `UNRESOLVED`.
- **Owner:** AFE AI ML team is associated but no accountable production owner is assigned.
- **Current implementation evidence:** card explicitly says not production-ready; active API/worker is absent/commented.
- **Intended ARK boundary:** own NPT feature/label definitions, classifier/survival lifecycle, eligibility, forecast contract, evaluation, artifacts, configuration, and runbook.

Evidence: `next_purchase_prediction.md — ML SERVICE CARD`, **1. PURPOSE**, **14. OWNERSHIP / ISOLATION**, **16. OPEN GAPS / TODO**.

### Operations and invocation

| Operation | Current fact | Intended ARK treatment |
|---|---|---|
| Tenant prediction batch | Synchronous code path; API/worker inactive/commented | Durable async `next-purchase-predict-batch` |
| Training | Missing artifacts can train during inference | Explicit classifier and survival train/evaluate/promote/activate operations |
| Online prediction/events | No active accepted contract | `UNRESOLVED`; do not add without requirement |

Current transaction floor/window and per-customer gates are prototype evidence only. Latency/scale targets are unresolved. Evidence: `next_purchase_prediction.md — 2. TRIGGER / EXECUTION MODE`, **5. HIGH-LEVEL WORKFLOW**, **9. EXECUTION PROFILE**, **12. INTEGRATION**.

### Input contracts

- **Current:** transaction history, customer/business identifiers, calendar/context and configuration; documented tenant transaction floor `200` over `365` days and customer checks such as frequency/tenure are not approved target thresholds.
- **Intended:** common envelope plus immutable transaction/feature dataset reference with opaque customer/product IDs, purchase time, amount/currency policy, observation/as-of time, censoring rules, horizon definition, label version, calendar version, and purpose.
- **Current hazards:** configuration paths are inconsistent; classifier/survival output names do not match the served schema.
- Exact schema and thresholds remain `UNRESOLVED`.

### Data readiness and capability eligibility

- **Current:** tenant and customer history gates exist, but prototype defects can yield computed results with `served=false`.
- **Intended:** separate dataset structural/semantic/freshness readiness; classifier eligibility; survival/time eligibility; horizon/config/model readiness; explicit degraded/fallback/ineligible reasons.
- No unsupported customer prediction may be fabricated. Exact minimums require evaluation and approval.

### Processing and ML lifecycle

- **Current:** HistGradientBoosting classifier plus random survival forest; artifacts may be trained at inference; survival configuration is explicitly a fast-test setup; dynamic horizon mapping is defective.
- **Intended:** versioned preprocessing/feature pipeline; explicit label/horizon/censoring semantics; independently evaluated compatible classifier and survival artifacts; atomic active bundle selection; no implicit training.
- **Evaluation:** classifier calibration/discrimination, time-to-event calibration/ranking, horizon accuracy, censoring/coverage, leakage, stability/drift, subgroup/tenant behavior, and business utility; numeric gates TBD.

Evidence: `next_purchase_prediction.md — 3. INPUT CONTRACT`, **5. HIGH-LEVEL WORKFLOW**, **6. ELIGIBILITY / PRECONDITIONS**, **10. CONFIGURATION**, **11. FAILURE / FALLBACK**.

### Output contracts

- **Current:** DataFrame and optional `CustomerNextPurchasePredictions`; classifier/RSF fields mismatch the intended served schema; calculation does not guarantee `served=true`.
- **Intended:** opaque customer ID, as-of time, eligibility, defined horizon(s), purchase probability per horizon, optional time estimate/distribution with semantics, confidence/uncertainty only if valid, reason/explanation reference, and full dataset/feature/calendar/model-bundle/config/code/execution lineage.
- **Status/error:** capability success is distinct from scientific eligibility and projection success; schema names/types must be single-source and versioned.
- **Events:** `UNRESOLVED`.

### Ownership and dependencies

- **Current:** direct access spans three database roles, BCDP phone lookup, generic snapshot/calendar/model stores, and shared debug CSVs.
- **Intended owned state:** NPT feature/label definitions, classifier/survival artifacts and bundle, evaluation, results, configuration, migrations.
- **Approved interfaces:** registered datasets/calendar, artifact registry, durable job/result store, external projector.
- **Forbidden:** phone-based tenant/customer authority, generic shared writes, debug files with tenant/customer data, other capability state.
- **Migration:** activate a real bounded operation only after schema/lifecycle repair; replace direct storage and debug-file flows.

### Configuration, reliability, and operation

- **Configuration:** horizons, history rules, label/censoring definitions, model parameters, thresholds, and calendar version must be versioned; fast-test values are not production settings.
- **Reliability:** atomic two-artifact compatibility, idempotent durable job, deterministic replay, truthful served/status semantics, retry/cancel/partial behavior.
- **Security/privacy:** tenant isolation, opaque IDs, restricted datasets/artifacts/results, no shared debug PII.
- **Observability/quality:** per-stage failures, eligible/served counts, output distributions, calibration/survival metrics, drift, active bundle/version, latency/resource use; targets TBD.
- **Runbook/owner/scale:** `UNRESOLVED`.

### Gaps, assumptions, decisions, and acceptance tests

- **Gaps:** production owner, active operation, canonical schema, horizons/labels, artifact compatibility, thresholds/gates, runtime/capacity/SLO, fallback.
- **Assumption needed:** `A-03-OWNERSHIP` and `A-03-ML-MIGRATION`.
- **Acceptance:** service fields exactly match schema; horizon mapping is correct; inference cannot train; incompatible classifier/survival bundles cannot activate; `served` truthfully reflects a consumable result; insufficient history returns explicit ineligible/fallback; no cross-tenant/debug leakage; replay is idempotent.
- **Traceability:** `ARK-FR-004`–`009`, `ARK-NFR-001`–`007`, `ARK-CON-002`–`003`, `SC-02-04`, `SC-02-06`, `SC-02-09`–`011`.

---

## Capability contract — CAP-REC: Recommendation / REC

### Identity and business purpose

- **Capability ID/version:** `CAP-REC`; current `REC` `0.1.0`, algorithm label `heuristic_v1` (`FACT`, temporary evidence).
- **Business value:** provide ranked product recommendations; business KPI/consumer placement/acceptance target `UNRESOLVED`.
- **Owner:** `TBD`; logical owner CAP-REC; accountable authorities unresolved.
- **Current implementation evidence:** in-process/CLI pipeline with model, fallback, schema, state, and isolation gaps.
- **Intended ARK boundary:** own candidate/ranking/fallback/feedback semantics, training/evaluation, eligibility, results, configuration, artifacts, and runbook.

Evidence: `recommender.md — ML SERVICE CARD`, **1. PURPOSE**, **14. OWNERSHIP / ISOLATION**.

### Operations and invocation

| Operation | Current fact | Intended ARK treatment |
|---|---|---|
| Recommendation generation | In-process/CLI tenant batch; no public generation endpoint or scheduler | Durable async `recommendation-generate-batch`; online operation only if separately bounded/measured |
| Product metadata/event inputs | Supporting synchronous APIs exist | Versioned ingestion/feedback interfaces with tenant/idempotency identity |
| ALS training | Fresh ALS model trained inside every generation run then discarded | Explicit training/artifact lifecycle or an explicit approved ephemeral algorithm decision |

Evidence: `recommender.md — 2. TRIGGER / EXECUTION MODE`, **5. HIGH-LEVEL WORKFLOW**, **9. EXECUTION PROFILE**, **12. INTEGRATION**.

### Input contracts

- **Current:** raw transactions, catalog/inventory, product metadata/history, customer and business identifiers; multiple direct stores and BCDP/phone lookup.
- **Intended:** common envelope plus immutable transaction, catalog/inventory, product-metadata, and optional feedback dataset references; opaque customer/product IDs; as-of time; availability, price/currency, event semantics, ranking-policy version, and requested top-K/context.
- **Current hazard:** a tenant-wide `200`-transaction gate prevents the documented low-data fallback from running.
- Exact schemas, required datasets, freshness, and bounds remain `UNRESOLVED`.

### Data readiness and capability eligibility

- **Current:** top-level data gate, per-algorithm conditions, and fallbacks conflict; `served=true` can accompany empty results.
- **Intended:** separate catalog/inventory readiness, transaction/metadata/feedback readiness, tenant/customer/item eligibility, algorithm eligibility, and ranked-result validity.
- **Fallback:** explicit popularity/content/co-occurrence/no-result policy with reason and lineage; no silent source omission.
- Exact minimums and business constraints are `UNRESOLVED`.

### Processing and ML lifecycle

- **Current:** ALS, co-occurrence, content-based filtering, fallback, ranking, and bandit-related logic; ALS retrains each run and is not persisted.
- **Intended:** versioned candidate-source interfaces, deterministic merge/dedup/filter/rank policy, explicit inventory/business constraints, and an approved choice for learned versus ephemeral artifacts; feedback/bandit updates separated from request-time inference.
- **Evaluation:** coverage, relevance/ranking, diversity/novelty, availability correctness, cold-start/fallback quality, stability, bias, drift, latency/cost, and offline/online usefulness; gates TBD.

Evidence: `recommender.md — 3. INPUT CONTRACT`, **5. HIGH-LEVEL WORKFLOW**, **6. ELIGIBILITY / PRECONDITIONS**, **10. CONFIGURATION**, **11. FAILURE / FALLBACK**.

### Output contracts

- **Current:** large DataFrame-rich dictionary and optional top-three persistence; empty output can be marked served.
- **Intended:** bounded result/reference with opaque customer ID, as-of/context, ordered product items, rank/score with defined semantics, candidate-source/reason reference, eligibility/fallback/degraded reason, availability snapshot, and full dataset/model/ranking/config/code/execution lineage.
- **Status/error:** empty list is a valid explicit no-result only with truthful reason; persistence/projection is separate from generation success.
- **Events:** accepted result/feedback event contracts are `UNRESOLVED`.

### Ownership and dependencies

- **Current:** multiple databases/BCDP, direct phone lookup, shared model/debug files, and shared top-three persistence.
- **Intended owned state:** REC candidate/ranking artifacts, configuration, evaluations, results, and feedback required for learning; catalog/transaction/customer source data remains externally owned.
- **Approved interfaces:** registered datasets, artifact registry, durable job/results, catalog/inventory contract, feedback ingestion, projector/serving adapter.
- **Forbidden:** profile/catalog/order mutation, another capability's private state, phone as authority, shared debug leakage.
- **Migration:** replace direct reads/writes, establish stable output and feedback ownership, repair low-data fallback, and decide ALS lifecycle.

### Configuration, reliability, and operation

- **Configuration:** top-K, candidate weights, filters, business rules, fallback order, exploration policy, model/ranking versions, and freshness must be versioned; values TBD.
- **Reliability:** idempotent generation/feedback, durable batch replay, deterministic version selection, per-source degraded outcomes, cancellation/timeout/partial-result policy.
- **Security/privacy:** tenant/item/customer isolation, opaque IDs, consent/purpose limits for behavioral data, safe logs.
- **Observability/quality:** source coverage, eligible/served/empty/fallback rates, ranking metrics, unavailable-item leakage, drift, feedback delay, version lineage, latency/resource use; targets TBD.
- **Runbook/scale:** unresolved.

### Gaps, assumptions, decisions, and acceptance tests

- **Gaps:** owner, consumer contract, source schemas, algorithm/artifact decision, eligibility/fallback thresholds, ranking policy, feedback authority, quality gates, scale/SLO.
- **Assumption needed:** `A-03-OWNERSHIP` and `A-03-ML-MIGRATION`.
- **Acceptance:** low-data tenants reach the approved fallback; empty result cannot be misreported; unavailable/unauthorized products never rank; same inputs/versions reproduce output; retries do not duplicate feedback/cost; no direct cross-store writes; tenant isolation holds.
- **Traceability:** `ARK-FR-004`–`009`, `ARK-NFR-001`–`007`, `ARK-CON-002`–`003`, `SC-02-04`, `SC-02-06`, `SC-02-09`–`011`.

---

## Capability contract — CAP-SYN-CHAT: Synapse chatbot

### Identity and business purpose

- **Capability ID/version:** `CAP-SYN-CHAT`; operation `AgentController_chatbot_v1`, API `1.0.0` (`IFACE`).
- **Business value:** return an LLM-generated conversational response and reported cost to the requesting platform; business KPI and production target `UNRESOLVED`.
- **Owner:** blank/`UNRESOLVED`.
- **Current implementation evidence:** interface only. No provider, model, prompt, orchestration, tools, state, storage, safety, or runtime behavior may be inferred.
- **Intended ARK boundary:** bounded response-generation interface only; not an autonomous agent and not an external-action authority.

Evidence: `Synapse_chatbot.md — ML SERVICE CARD`, **1. PURPOSE**, **14. OWNERSHIP / ISOLATION**; `ADR-000 — Decision`.

### Operations and invocation

- **Current interface:** synchronous `POST /dev/v1/agent/chatbot`, API key in `authorization`; immediate HTTP response; no batch/job/event/proactive interface.
- **Latency:** expected/max/timeout `UNRESOLVED`; synchronous production fitness not established.
- **Intended:** common envelope; retain sync only after measurement; no agent, tool, memory, proactive, or async semantics without evidence/requirement.

### Input contracts

- **Required (`IFACE`):** `query:string`, `businessId:number`, `customerId:number`, `history[]` entries `{source: customer|agent, content:string}`, `referenceId:number`.
- **Optional (`IFACE`):** `channel: sms|social-media|push` with documented default `social-media`; `metadata` with `address`, `phone`, `viewedProducts`, and `basket` items whose quantity is at least one.
- **Unresolved:** maximum sizes, nullability, identifier scope, language, content/metadata schemas, history ordering/truncation, defaults beyond the documented channel, prompt/data-injection treatment, idempotency, tenant binding, and schema compatibility.
- **Intended:** authenticated principal is tenant authority; body IDs must match scope; minimize/replace direct PII and use opaque IDs; bound every nested collection/string.

Evidence: `Synapse_chatbot.md — 3. INPUT CONTRACT`, **Request schema**, **Minimum data requirements**.

### Data readiness and capability eligibility

- **Current:** request-field validation and declared API-key authentication only (`IFACE`).
- **Unresolved:** customer/business existence, entitlement, consent, history/metadata authority and freshness, supported language/channel, model/prompt readiness, safety readiness, context length, and fallback.
- **Intended:** explicit request, dataset/context, platform, model/content, and safety eligibility with eligible/degraded/fallback/ineligible reasons; missing context is not invented.

### Processing and ML lifecycle

- **Current evidenced sequence only:** authenticate/validate → generic LLM chat generation → response DTO.
- **All internals `UNRESOLVED`:** provider/model/version, prompt, retrieval, tools, memory, preprocessing, context selection, caching, moderation, postprocessing, training/fine-tuning, activation, evaluation, rollback, and token calculation.
- **Intended recommendation:** version the model/prompt/policy/config/code/execution context; explicit safety and content validation; no inference-time training; no agentic claim.

### Output contracts

- **Required (`IFACE`):** `{cost:number, referenceId:number, response:string, metadata:object}`.
- **HTTP (`IFACE`):** `200` response, `400` validation error; error body unresolved.
- **Unresolved:** cost units/pricing, token counts, metadata schema, empty/refusal semantics, confidence/explanation, safety/fallback/degraded status, other errors, lineage, idempotency, events.
- **Intended:** explicit outcome/reason, defined usage/cost, bounded response/metadata, safety result, and version lineage; text does not authorize an external action.

### Ownership and dependencies

- **Current:** external LLM category only; reads/writes/state/cache/persistence/provider retention and allowed/forbidden accesses are all `UNRESOLVED`.
- **Intended capability-owned:** bounded chat contract, capability configuration, evaluation, and result semantics; state only if later evidenced and explicitly tenant-scoped.
- **Shared:** authentication/tenant, entitlements, lifecycle, audit/metering, secrets/provider interface.
- **Forbidden:** unapproved customer/profile access, cross-capability state, untrusted body tenant authority, direct sending/action.

### Configuration, reliability, and operation

- **Configuration:** channel is evidenced; provider/model/prompt/safety/history limits and tenant overrides unresolved.
- **Reliability:** timeout/retry/idempotency/cancellation/provider failure/fallback unresolved; only validation `400` is evidenced.
- **Security/privacy:** API-key interface evidenced; enforcement, key lifecycle, tenant binding, authorization scopes, PII/provider retention, prompt injection, and content safety unresolved.
- **Observability:** returned cost only; logs/metrics/traces/audit/quality/safety/runbook unresolved.
- **Scaling:** all numeric and resource characteristics unresolved.

### Gaps, assumptions, decisions, and acceptance tests

- **Assumption needed:** `A-03-OWNERSHIP` and `A-03-SYNAPSE`.
- **Acceptance before production:** authoritative implementation/provider/prompt/policy/state/safety evidence registered; body tenant cannot override principal; nested input bounds enforced; cross-tenant/PII/provider-retention controls pass; lineage and defined cost are returned/audited; failures are explicit/no-action; measured sync criteria pass; no autonomous/tool/action behavior exists without later justification.
- **Traceability:** `ARK-FR-004`–`010`, `ARK-NFR-001`–`007`, `ARK-CON-002`–`003`, `ARK-CON-007`, `SC-02-08`–`011`.

---

## Capability contract — CAP-SYN-MSG: Synapse message generator

### Identity and business purpose

- **Capability ID/version:** `CAP-SYN-MSG`; `AgentController_generateChurnMessage_v1` and `AgentController_generateOccasionCampaign_v1`, API `1.0.0` (`IFACE`).
- **Business value:** return Persian churn-prevention or occasion marketing text plus reported cost; KPI/production target unresolved.
- **Owner:** blank/`UNRESOLVED`.
- **Current implementation evidence:** interface only; `AgentController` does not evidence an agent.
- **Intended ARK boundary:** content generation, not campaign authorization or delivery.

Evidence: `synapse_message_generator.md — ML SERVICE CARD`, **1. PURPOSE**, **14. OWNERSHIP / ISOLATION**; `ADR-000 — Decision`.

### Operations and invocation

| Operation | Current interface fact |
|---|---|
| Churn message | Synchronous `POST /dev/v1/agent/churn`, API key, immediate response |
| Occasion campaign message | Synchronous `POST /dev/v1/agent/occasional-campaign`, API key, immediate response |

No bulk, job, proactive, retrieval, or event interface is documented. Latency/timeout/scale are unresolved. Intended use inherits the common envelope and measured synchronous criterion.

### Input contracts

- **Churn required:** `businessId:number`, `customerId:number` (`IFACE`).
- **Occasion required:** `businessId:number`, `occasionName:string`; optional `customerId:number` (`IFACE`).
- **Optional:** `channel: sms|social-media|push`, `offerValue:number`, `offerExpiryHours:number`, `offerPolicy:string`, `maxLength:number` with minimum `1`; occasion also has `occasionType: content|soft-sales|sales-driven` (`IFACE`).
- **Unresolved:** identifier scope, field units/ranges/defaults, currency, max-length unit/maximum, offer authority, required customer/churn/campaign context, locale, idempotency, and tenant binding.
- **Intended:** bounded versioned schema; authenticated tenant; immutable authorized customer/churn/campaign/offer context references; untrusted text treatment.

Evidence: `synapse_message_generator.md — 3. INPUT CONTRACT`, **Operation A: Churn message**, **Operation B: Occasional campaign**.

### Data readiness and capability eligibility

- **Current:** required-field/enumeration/`maxLength >= 1` validation and declared API key only.
- **All dataset/internal readiness unresolved:** customer/business/churn/campaign/offer source, consent, freshness, entitlement, model/prompt/safety readiness, supported language/channel.
- **Intended:** explicit context authority/readiness and scientific/content/safety eligibility; unsafe or unverifiable offer/context yields explicit non-success/no action.

### Processing and ML lifecycle

- **Current evidenced sequence only:** authenticate/validate → generic LLM message generation → response DTO.
- **All internals unresolved:** provider/model/prompt/version, context lookup, retrieval, tools, state, training, decoding, moderation, Persian/length/offer validation, fallback, and cost calculation.
- **Intended recommendation:** version provider/model/prompt/policy/config; validate Persian language, channel/length, offer fidelity, prohibited claims, and safety; no implicit training or agent behavior.

### Output contracts

- **Both operations (`IFACE`):** `{cost:number, response:string}`; primary output described as Persian marketing text.
- **HTTP:** `200` and `400`; error body unresolved.
- **Unresolved:** cost units/tokens/pricing, empty/refusal/fallback status, safety, explanation, lineage, errors beyond 400, persistence/events.
- **Intended:** explicit outcome/reason; language/channel; verified offer/occasion facts; version lineage; defined usage/cost; validation/safety results. Output text never authorizes or sends a campaign.

### Ownership and dependencies

- **Current:** generic external LLM dependency; all data reads/writes/state/storage/cache/history/provider retention unresolved.
- **Intended owned:** bounded generation contracts, configuration/prompt/model lifecycle if evidenced, evaluations, and result semantics.
- **Shared:** authenticated context, entitlements, registered datasets, audit/metering, secrets, outward notification/action adapter.
- **Forbidden:** direct campaign sending, profile/private-state mutation, body-selected tenant, or inferred hidden data access.

### Configuration, reliability, and operation

- **Configuration:** request fields evidenced; service model/prompt/policy/safety/defaults and overrides unresolved.
- **Reliability:** validation 400 evidenced; retry, timeout, idempotency, double-charge, provider failure, fallback unresolved.
- **Security/privacy:** API-key interface evidenced; tenant scopes/key lifecycle, customer/context transfer, provider use/retention, prompt injection and safety unresolved.
- **Observability/evaluation:** cost field only; Persian fluency, relevance, fidelity, length, safety/refusal, human/LAB quality, logs/traces/metrics/runbook all unresolved.
- **Scaling:** unresolved.

### Gaps, assumptions, decisions, and acceptance tests

- **Assumption needed:** `A-03-OWNERSHIP` and `A-03-SYNAPSE`.
- **Acceptance before production:** authoritative internals/safety/ownership evidence; tenant-bound context; exact units/bounds; approved offer authority; safety/Persian/length/fidelity validation; explicit failure/fallback and idempotent metering; model/prompt/policy lineage; measured sync fitness; no direct external action or agent behavior.
- **Traceability:** `ARK-FR-004`–`010`, `ARK-NFR-001`–`007`, `ARK-CON-002`–`003`, `ARK-CON-007`, `SC-02-08`–`011`.

---

## Capability contract — CAP-SYN-VERIFY: Synapse campaign verifier

### Identity and business purpose

- **Capability ID/version:** `CAP-SYN-VERIFY`; `AgentController_callCampaignVerifierAgent_v1`, API `1.0.0` (`IFACE`).
- **Business value:** provide an LLM assessment of caller-supplied campaign material; KPI, legal/policy authority, and production target unresolved.
- **Owner:** blank/`UNRESOLVED`.
- **Current implementation evidence:** interface only; the `accepted | rejected | failed` enum proves an assessment label, not authoritative policy enforcement.
- **Intended ARK boundary:** advisory campaign assessment only. Deterministic grants, policy, permission, quota, freshness, deduplication, and required human approval remain outside and authoritative.

Evidence: `synapse_campaign_verifier.md — ML SERVICE CARD`, **1. PURPOSE**, **4. OUTPUT CONTRACT**, **14. OWNERSHIP / ISOLATION**; `outputs/stages/02-system-definition.md — ARK-FR-010`.

### Operations and invocation

- **Current interface:** synchronous `POST /dev/v1/agent/campaign-verifier`, API key in `authorization`, immediate response.
- **No documented:** async/job, events, proactive monitoring, streaming, training, or activation interface.
- **Latency/resource/timeout/scale:** all unresolved; intended sync admission requires measurement.

### Input contracts

- **Required top-level (`IFACE`):** `payload`, `references[]`, `config[]`, `metadata[]`; no minimum array cardinalities documented.
- **Payload:** `{data: object}` required.
- **Reference:** `{data: object, tags: string[]}` required.
- **Configuration:** `{agent: string, settings: object}` required.
- **Metadata:** `{tag: string, value?: object}`.
- **Unresolved:** every internal object schema, maximum size, allowed agents/settings/tags, empty-array meaning, source authority/version/effective dates, precedence/conflict, tenant/campaign/jurisdiction/channel/policy semantics, and idempotency.
- **Intended:** bounded registered schemas or immutable references with source, authority, scope, version/effective interval, integrity, precedence, and authenticated tenant/caller; caller-controlled settings cannot select unapproved policy/model behavior.

Evidence: `synapse_campaign_verifier.md — 3. INPUT CONTRACT`, **Payload schema**, **Reference schema**, **Configuration schema**, **Metadata schema**.

### Data readiness and capability eligibility

- **Current:** declared API-key authentication and structural field validation only.
- **Unresolved:** authoritative policy/reference completeness, freshness, conflict resolution, entitlement, campaign eligibility, agent/config validity, model/prompt/safety readiness.
- **Intended:** separate request readiness, policy/reference readiness, platform eligibility, capability eligibility, advisory assessment, and authoritative authorization. Missing/stale/conflicting/incomplete evidence cannot yield actionable acceptance.

### Processing and ML lifecycle

- **Current evidenced sequence only:** authenticate/validate → “LLM campaign verification” → response DTO.
- **All internals unresolved:** provider/model/version, prompt/policy, preprocessing, retrieval/tools/memory, deterministic checks, evidence extraction, parsing, confidence, safety, training, evaluation, promotion, rollback, fallback.
- **Intended recommendation:** bind exact payload schema, complete reference/policy set, config, model, prompt, deterministic checks, code, and execution versions; return evidence/reason codes; keep permission enforcement independent.

### Output contracts

- **Required (`IFACE`):** `{cost:number, status:'accepted'|'rejected'|'failed', description:string, error:string}`.
- **HTTP (`IFACE`):** `200` returns this DTO and may contain `failed`; `400` is validation error with undefined body.
- **Unresolved:** empty error semantics, cost units/pricing, confidence/evidence, policy/model lineage, retryability, other error types, partial/fallback, idempotency, events.
- **Intended:** independently represent transport/execution, data/policy readiness, capability eligibility, advisory assessment, and authoritative workflow authorization. `accepted` is never itself permission to act.

### Ownership and dependencies

- **Current:** generic LLM dependency only; internal data/state/storage/cache/provider retention/audit and access boundaries unresolved.
- **Intended capability-owned:** bounded advisory-assessment contract, assessment-specific configuration/prompt/model lifecycle if evidenced, evaluation, and result semantics.
- **External owners:** authoritative campaign policy and action workflow must have separate named authorities, currently unresolved.
- **Forbidden:** campaign sending/approval, direct customer/campaign-state mutation, caller-defined authority, other capability/private storage.

### Configuration, reliability, and operation

- **Configuration:** caller supplies opaque `agent/settings`; allowed values, service configuration, provider/model/prompt/policy versions and override rules unresolved.
- **Reliability:** synchronous/400 evidence only; timeout/retry/idempotency/double cost/provider failure/partial/fallback unresolved. A failed or ambiguous assessment must cause no action.
- **Security/privacy:** API-key interface only; tenant scope, authorization, opaque content sensitivity, external transfer/retention, prompt injection, exfiltration, consent, secrets, and human escalation unresolved.
- **Observability/evaluation:** returned cost/status only; policy coverage, false accept/reject, consistency, adversarial safety, human overrides, lineage, logs/metrics/traces/audit/runbook unresolved.
- **Scaling:** all limits and targets unresolved.

### Gaps, assumptions, decisions, and acceptance tests

- **Assumption needed:** `A-03-OWNERSHIP` and `A-03-SYNAPSE`.
- **Acceptance before production:** authoritative policy and implementation evidence; bounded/versioned inputs; incomplete policy is not accepted; unapproved agent/settings rejected; transport/execution/assessment/authorization are separate; adversarial “accept” text cannot override deterministic controls; absent/revoked grants, stale policy, exceeded quota, duplicate, `failed`, or ambiguity causes no action; lineage/idempotency/cost/privacy/sync tests pass; no agent behavior is inferred.
- **Traceability:** `ARK-FR-004`–`010`, `ARK-NFR-001`–`007`, `ARK-CON-002`–`003`, `ARK-CON-007`, `SC-02-08`–`011`.

## Analysis and recommendations

### R-03-01 — Treat the seven items as logical capability modules, not seven deployment units

The contracts define ownership and failure boundaries. Stage 04 must apply architecture drivers before selecting physical placement. This preserves the approved modular-monolith baseline and passes the anti-overengineering test: separate logic and state ownership are required; separately operated services are not yet justified.

### R-03-02 — Build one shared operational envelope and capability-definition registry

All seven require the same tenant, request/idempotency, execution, dataset, version, result, and audit concepts. Implementing these inconsistently would multiply reliability and isolation defects. The registry must describe supported operations and modes, not hide capability-specific scientific eligibility or schemas.

### R-03-03 — Remediate the four detailed prototypes before production migration

Do not preserve implicit training, direct shared-profile writes, unstable semantics, false served/success states, or bypassed fallbacks for compatibility. Compatibility adapters may read current shapes temporarily, but the owned result contracts and explicit lifecycle above are the target.

### R-03-04 — Keep Synapse integration interface-bound until evidence arrives

Later stages may design authentication, tenant binding, bounded HTTP adapters, standard error/lifecycle mapping, provider-data controls, audit, and no-action enforcement around the documented interfaces. They may not choose hidden providers/models/prompts, assert statelessness, create memory/tools, or treat the verifier as policy authority.

## Decisions

- `ADR-000` remains binding: the six normalized-only cards are temporary; Synapse evidence is interface-only.
- `ADR-001` remains binding except that the cited ML/ownership deferrals reach their Stage 03 expiry here.
- `ADR-002` is `ACCEPTED`; its three temporary dispositions are active only until their recorded expiry points.
- No algorithm, threshold, model, provider, deployment unit, synchronous latency bound, SLO, capacity, budget, or production-readiness decision is made in this stage.

## Contradictions and dangerous assumptions

| ID | Evidence conflict or hazard | Treatment |
|---|---|---|
| `C-03-01` | Churn inference may fit/train and force uncalibrated extremes | Current migration defect; target contract prohibits implicit lifecycle and unapproved score semantics |
| `C-03-02` | RFM weights/direction/labels and artifact interfaces are unstable or contradictory | Current migration defect; stable versioned semantic mapping required |
| `C-03-03` | NPT is declared non-production and has inactive interface/schema/horizon/artifact mismatches | Preserve as unavailable for production until repaired and evaluated |
| `C-03-04` | REC documents fallback paths but its top-level data gate can prevent them; empty output may be served | Require explicit eligibility/fallback and truthful result status |
| `C-03-05` | Detailed prototypes write shared BCDP/profile/process/model/debug state across intended ownership boundaries | Migrate to capability-owned state plus platform/projector interfaces |
| `C-03-06` | Synapse endpoint names contain “Agent” | Not evidence of autonomy, tools, memory, planning, or an agent framework |
| `C-03-07` | Synapse may look stateless because the full request is supplied | Persistence, caching, provider retention, and history are undocumented and remain unresolved |
| `C-03-08` | Campaign verifier emits `accepted` | Advisory label only; not authenticated permission, authoritative policy enforcement, or authorization to send |
| `C-03-09` | All cards lack named accountable production ownership | Requires `A-03-OWNERSHIP`; production readiness remains prohibited |
| `C-03-10` | Body business/customer IDs and phone-like identifiers appear in interfaces/current code | Principal-derived tenant and opaque-ID requirements govern; current fields do not grant authority |

## Open questions

| ID | Question | Required before | Proposed temporary treatment |
|---|---|---|---|
| `Q-03-01` | Who owns each capability contract, scientific decisions, promotion, operations, and runbook? | Stage 04 responsibility approval and any production admission | `A-03-OWNERSHIP` |
| `Q-03-02` | Are the intended Churn/RFM/NPT/REC contracts accepted as migration targets, and which current behaviors require compatibility? | Stage 10 lifecycle and Stage 16 migration planning | `A-03-ML-MIGRATION` |
| `Q-03-03` | Can authoritative Synapse implementation/OpenAPI/configuration/provider/prompt/policy/safety/operations evidence be supplied? | Detailed ML/security/operations design or production enablement | `A-03-SYNAPSE` |
| `Q-03-04` | If evidence cannot be supplied, should one or more Synapse capabilities be scoped out? | Product/release scope decision | Retain interface-only, non-production-eligible |
| `Q-03-05` | What are the authoritative feature, label, window, horizon, fallback, threshold, evaluation, and promotion policies for each detailed capability? | Per-capability build/promotion | Remain unresolved; do not invent |
| `Q-03-06` | What measured latency, volume, resource, SLO, recovery, and cost targets apply per operation? | Execution/deployment/production admission | Preserve unknown; classify by measurement later |
| `Q-03-07` | Which consumer-visible compatibility schemas and projections must be retained? | Stage 07 and Stage 16 | Capability-owned neutral result plus external adapters |

## Requirements-traceability updates

| Requirement | Stage 03 design response | Evidence/test status |
|---|---|---|
| `ARK-FR-004` | Seven machine-readable capability definitions are now scoped by operation/schema/mode/dependency/gap | Contract implementation pending |
| `ARK-FR-005` | Common operational envelope defined as inherited target requirement | Exact wire contract deferred to Stage 07 |
| `ARK-FR-006` | Readiness, platform eligibility, scientific eligibility, execution, and advisory outcomes separated | Per-capability thresholds unresolved |
| `ARK-FR-007` | Detailed batch capabilities target durable lifecycle; Synapse remains sync-interface evidence only | Workflow/store choice deferred |
| `ARK-FR-008` | Sync retained only after measured short/predictable qualification | Measurements absent |
| `ARK-FR-009` | All target contracts prohibit request-time training/activation | Four prototypes require remediation |
| `ARK-FR-010` | Capability output, especially verifier acceptance, cannot authorize external action | Mandatory negative tests specified |
| `ARK-FR-011` | Tenant configuration/version concepts assigned between platform and capabilities | Exact policy deferred |
| `ARK-FR-012` | Capability evaluation, isolation, lineage, failure, reproducibility, and safety test families identified | LAB design deferred |
| `ARK-NFR-001/005` | Principal tenant, opaque IDs, minimal provider/telemetry data, tenant-owned state | Current phone/shared-state paths require migration |
| `ARK-NFR-002/003` | Versioned datasets/features/models/prompts/policies/contracts/results required | Exact schemas/evidence unresolved |
| `ARK-NFR-004` | Idempotent at-least-once behavior and replay required | Current implementations insufficient |
| `ARK-NFR-006` | Correlated audit/usage/cost/version lineage required | Current Synapse exposes only ambiguous cost |
| `ARK-NFR-007` | Production gates require measured targets | No numeric target invented |
| `ARK-CON-002/003` | Capability-owned state and consumer-neutral results; projectors/adapters own consumer writes | Current direct writes are migration defects |
| `ARK-CON-007` | No agent framework or speculative infrastructure introduced | Synapse remains normal interface-bound capability |
| `SC-02-04/06/08/09/10/11` | Lifecycle, explicit ineligibility, no-action policy, isolation, reproducibility, and acceptance evidence mapped into every contract | Approval/evidence still required |

## Completion-gate evidence

| Gate test | Result | Evidence |
|---|---|---|
| Every named capability is present | PASS | Seven card files map to seven contracts above |
| One authorized specialist analysis per card | PASS | Seven bounded `capability_analyst` reviews reconciled by the primary agent |
| Current facts separated from intended contract/migration | PASS | Evidence notation and every capability section |
| Shared platform separated from capability ownership | PASS | Responsibility table plus ownership subsections |
| Missing/insufficient evidence explicitly dispositioned | PASS BY EXPLICIT APPROVAL | `ADR-002` is accepted; Synapse internals and accountable owners remain unresolved under its temporary constraints |
| No unsupported complete-ARK or production-ready claim | PASS | Every readiness/gap is explicit; no capability is declared production-ready |
| No named capability silently omitted | PASS | Inventory and contract count = seven |

**Gate result: PASSED BY EXPLICIT DISPOSITION.** On 2026-08-11 the sponsor approved the Stage 03 inventory and its outputs, activating the three temporary dispositions in accepted `ADR-002`. This approval satisfies the missing-evidence gate for workflow design without declaring any capability production-ready or resolving undocumented Synapse internals.

## Downstream consequences

- Stage 04 must consume these logical boundaries and evaluate architecture style without equating a capability with a deployable service.
- Stages 05–10 must design shared lifecycle, data, integration, execution, event, and ML mechanisms around the intended contracts, while keeping every `UNRESOLVED` field conditional.
- Stage 11 must not propose agent architecture from Synapse naming; it requires separately documented autonomy/tool/memory needs.
- Stage 12 must preserve deterministic authorization and no-action behavior independent of campaign-verifier labels.
- Stages 13–16 must address the listed failure modes, evaluation evidence, placement measurements, and migration defects before implementation planning.
- New originals or implementation evidence must be reconciled against these contracts under `ADR-000`; contradictions invalidate affected downstream work.

## Exact next-stage inputs

After explicit Stage 03 approval and acceptance of a disposition:

1. `outputs/stages/00-source-audit.md`
2. `outputs/stages/01-discovery-and-questions.md`
3. `outputs/stages/02-system-definition.md`
4. `outputs/stages/03-capability-inventory.md`
5. `decisions/ADR-000-temporary-source-evidence-disposition.md`
6. `decisions/ADR-001-stage-01-requirements-baseline.md`
7. Accepted `decisions/ADR-002-stage-03-capability-evidence-disposition.md`
8. `sources/normalized/ark-assumptions.md`
9. All seven service cards
10. `stages/04-architecture-style.md` and its named governing prompt section/template inputs

Do not read or execute Stage 04 until the Stage 03 gate is explicitly approved.
