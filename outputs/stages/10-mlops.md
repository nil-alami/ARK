# Stage 10 — ML and MLOps architecture

Status: `APPROVED`

## Purpose and scope

Define the smallest implementable ML lifecycle that lets ARK reproduce, evaluate, approve, activate, observe, and roll back every production-eligible model or AI configuration without turning prototype behavior into a production contract. This stage binds the approved dataset, API, job, event, capability, artifact, audit, and ownership boundaries from Stages 03 and 05–09.

The design covers Churn, RFM, NPT, REC, Synapse Chatbot, Synapse Message Generator, and Synapse Campaign Verifier. It does not approve current prototype algorithms or thresholds, make Synapse production-eligible, select an MLOps/feature-store vendor, invent numerical quality or rollout thresholds, define deployment topology, or execute Stage 11. The sponsor accepted ADR-007's explicit negative production-scope dispositions and approved Stage 10 as written on 2026-08-12; that accepted disposition satisfies the inventory side of the gate without inventing lifecycle evidence. All seven profiles remain unavailable for production until their re-entry gates pass.

The sponsor explicitly approved Stage 09 and ADR-006 on 2026-08-12 and authorized execution of Stage 10 only.

## Inputs read in full

- `AGENTS.md` — all sections
- `WORKFLOW.md` — all sections
- `STATUS.md` — all sections after recording Stage 09/ADR-006 approval
- `SOURCE_MANIFEST.md` — all sections
- `stages/STAGE-CONTRACT.md` — all sections
- `stages/10-mlops.md` — all sections
- `templates/stage-output.md` — all sections
- `templates/adr.md` — all sections
- `sources/normalized/system-design-prompt.md` — **9. ML and MLOps architecture** exactly
- `sources/normalized/ark-assumptions.md` — all sections
- `outputs/stages/03-capability-inventory.md` — all sections
- `outputs/stages/05-end-to-end-architecture.md` through `outputs/stages/09-events-proactive-actions.md` — all sections
- `decisions/ADR-002-stage-03-capability-evidence-disposition.md` through accepted `decisions/ADR-006-governed-proactive-action-and-delivery.md` — all sections
- `sources/normalized/service-cards/churnobyl.md` — all sections
- `sources/normalized/service-cards/RFM.md` — all sections
- `sources/normalized/service-cards/next_purchase_prediction.md` — all sections
- `sources/normalized/service-cards/recommender.md` — all sections
- `sources/normalized/service-cards/Synapse_chatbot.md` — all sections
- `sources/normalized/service-cards/synapse_message_generator.md` — all sections
- `sources/normalized/service-cards/synapse_campaign_verifier.md` — all sections

The Stage 10-authorized `data_mlops_architect` performed a bounded read-only review. Its findings are reconciled into the independent identity model, capability/platform ownership split, promotion authority, rollback safety, feature-store decision, per-capability activation gates, Synapse evidence boundary, and completion-gate evidence below. The primary agent remains the sole writer.

## Source-instruction coverage

| Source requirement | Addressed in | Status/evidence |
|---|---|---|
| Experiment tracking | Experiment and training records | Addressed with immutable run manifest and comparison lineage |
| Dataset versioning | Independent version identity; reproducibility | Consumes Stage 06 immutable dataset versions and quality evidence |
| Feature definitions | Feature and point-in-time contract | Capability-owned, versioned definitions and transforms |
| Training pipeline | Explicit training flow | Durable job; inference cannot train or activate |
| Model evaluation | Evaluation and promotion | Versioned evaluation policies, reports, slices, and applicability decisions |
| Approval/promotion | Evaluation and promotion | Separate scientific, control/release, and operational gates with named authority required before activation |
| Model registry | Logical registry contract | PostgreSQL metadata plus immutable object references; no standalone product |
| Deployment strategy | Deployment assignment and loading | Immutable assignment to exact compatible bundle |
| Online and batch inference | Inference modes | Sync only after measured admission; durable batch is current default for four evidenced prototypes |
| Model loading | Deployment assignment and loading | Digest verification, compatibility check, bounded cache, no `latest` |
| Model version selection | Deployment assignment and loading | Deterministic tenant/capability/operation/environment assignment |
| Shadow/canary | Rollout modes | Supported only through explicit safe policy and measurable evaluation path |
| Rollback | Rollback protocol | Assignment reversion to approved compatible bundle; immutable history |
| Drift detection | Monitoring, feedback, retraining | Data, feature, prediction, and outcome/performance drift separated |
| Data-quality monitoring | Monitoring, feedback, retraining | Stage 06 quality evidence plus capability scientific sufficiency |
| Performance monitoring | Monitoring, feedback, retraining | Capability-owned metrics/slices; thresholds remain approval inputs |
| Feedback collection | Monitoring, feedback, retraining | Versioned, consent/purpose-bound feedback linked to prediction/exposure |
| Retraining triggers | Monitoring, feedback, retraining | Trigger submits a candidate training job; never auto-promotes |
| Explainability | Capability evaluation profiles | Semantics and applicability defined per capability |
| Reproducibility | Reproduction manifests and procedure | Exact evidence graph for training and inference, with declared nondeterminism |
| Fairness/safety | Capability evaluation profiles | Mandatory applicability decision and capability-specific evidence |
| Full feature-store decision | Feature-store decision | Not justified; simpler versioned offline/PIT controls specified |

## Facts

1. ARK already requires contract, dataset, feature-schema, model, code, and execution versions to be tracked independently. `sources/normalized/ark-assumptions.md — Integration and contracts`, item 10.
2. Each capability owns its model lifecycle, scientific eligibility, fallbacks, artifacts, tests, monitoring rules, and runbook; shared infrastructure cannot become shared business ownership. `sources/normalized/ark-assumptions.md — Product and architecture`, items 3–4; `outputs/stages/05-end-to-end-architecture.md — C05-11 and C05-16`.
3. Stage 06 established immutable dataset versions, readiness/quality evidence, temporal lineage, and service-owned derived namespaces. PostgreSQL stores metadata; object storage carries large datasets and artifacts. `outputs/stages/06-data-architecture.md — Data-layer contract`; `— Lineage and versioning`.
4. Stage 08 requires training and large/batch inference to be durable jobs, fixes admitted handler/code versions, and forbids inference from implicitly training or activating. `outputs/stages/08-execution-orchestration.md — Execution-mode disposition`; `— Durable execution flow`.
5. Stage 09 requires every committed insight to retain exact dataset, feature, model/artifact, configuration, policy, code, and execution references, but the capability result cannot authorize external action. `outputs/stages/09-events-proactive-actions.md — Insight-to-decision conversion`.
6. Churn, RFM, NPT, and REC are non-production migration evidence. Their cards document implicit or per-run training, unversioned features, artifact-selection defects, result-contract defects, unsafe fallbacks, and cross-boundary persistence. `outputs/stages/03-capability-inventory.md — CAP-CHURN through CAP-REC`.
7. The three Synapse cards establish only synchronous HTTP shapes and reported cost. Provider/model, prompt, training/fine-tuning, policy, safety, state, data access, reliability, and evaluation evidence are absent. `outputs/stages/03-capability-inventory.md — CAP-SYN-CHAT through CAP-SYN-VERIFY`.
8. All seven capabilities lack a complete set of named accountable production, ML/scientific, and operations/runbook owners. `outputs/stages/03-capability-inventory.md — Capability evidence matrix`; accepted `ADR-003 — A-04-OWNERSHIP`.
9. No traffic, SLO, business KPI, compliance duty, deployment environment, model-quality threshold, rollout percentage, or retraining cadence is authoritative. `outputs/stages/01-discovery-and-questions.md — Active temporary assumptions`.

## Assumptions

Stage 10 introduces no new temporary assumption and does not silently extend either Stage 10 expiry in ADR-002. Accepted ADR-007 explicitly replaces the affected dispositions with durable negative production-admission profiles. No affected capability is production-enabled by this approval.

| ID | Assumption | Why needed | Architectural effect | Risk | Validation/expiry |
|---|---|---|---|---|---|
| `A-01-SCALE` | Numeric latency, throughput, resource, rollout, and quality targets remain unknown | Prevent fabricated gates | Every enabled operation must supply measured policy values before activation | Production fitness unproven | Stage 17 and authoritative requirements |
| `A-01-SEC` | Least privilege, tenant binding, audit, privacy, and fail-closed policy remain mandatory while exact roles/duties are unknown | ML evidence can expose sensitive data or create consequential decisions | Promotion and feedback require policy/security approval where applicable | Later duties may be stricter | Stage 12 and authoritative policy evidence |
| `A-01-OPS` | Operational targets and support ownership are unknown | Prevent invented availability/recovery claims | Registry and worker contracts are logical; activation needs runbook/on-call and measured policies | Operational readiness blocked | Stages 13–15/17/20 |
| `A-04-OWNERSHIP` | Logical owner roles suffice for design; named authorities remain unresolved | Stage 10 needs accountable gates without inventing people | Model promotion/deployment and production enablement remain blocked until named authorities are assigned | Team segregation may differ | Before production/extraction/Stage 20 |
| `A-07-INTEGRATION` | Polling remains authoritative and external delivery stays conditional | MLOps completion must not depend on callbacks | Training/evaluation/inference results are retrievable by reference | Consumer contract may differ | Existing per-portion expiry |

### Stage 10 disposition of expiring ADR-002 assumptions

| Expiring disposition | Stage 10 replacement accepted in ADR-007 | Consequence |
|---|---|---|
| `A-03-ML-MIGRATION` | Churn, RFM, NPT, and REC become explicitly `MIGRATION_BLOCKED` capability profiles. The target lifecycle below is the production-admission contract; current algorithms, thresholds, and artifacts remain evidence only until each capability passes its profile-specific gate. | No indefinite assumption and no accidental compatibility promise; activation is evidence-based per capability. |
| `A-03-SYNAPSE` at the Stage 10 boundary | The three Synapse operations become explicitly `EVIDENCE_BLOCKED` ML profiles. Only their recorded API interfaces may be retained; production execution is denied until the complete generation/evaluation evidence bundle below is approved, or the capability is scoped out. | No inferred provider, prompt, agent, training, tool, memory, safety, or action behavior. Later security/operations gates still apply. |

## Analysis and recommendations

### Lifecycle principles and ownership boundary

| Concern | Shared ARK platform responsibility | Capability-owned responsibility | Invariant |
|---|---|---|---|
| Dataset evidence | Immutable dataset catalog/version/readiness/lineage interfaces | Required datasets, labels, cutoffs, scientific sufficiency | Ready data is not scientific eligibility |
| Experiment metadata | Common manifest schema, tenant isolation, immutable references, comparison/query API | Hypothesis, algorithm, parameters, metrics, interpretation | Tracker records evidence; it does not approve a model |
| Features | Storage primitives, dataset refs, lineage plumbing | Feature meaning, transform code, schema, PIT rules, train/serve tests | No shared module may redefine a capability feature |
| Training execution | Stage 08 job lifecycle, routing, leases, audit, artifact storage adapter | Training pipeline, splits, seeds, algorithm, checkpoints, candidate output | Training is explicit; inference never submits it as a side effect |
| Evaluation | Evidence storage and LAB/test interfaces | Metrics, slices, thresholds, fairness/safety applicability, comparison | Telemetry/LAB evidence is not promotion authority |
| Registry | PostgreSQL metadata contract and object-storage integrity | Artifact compatibility, semantic type, model bundle content | Registry presence is not approval or activation |
| Promotion | Authorization/audit record mechanism | Scientific recommendation and capability-specific gate | Named authorized decision required; no `latest` promotion |
| Deployment | Versioned assignment/activation and worker compatibility interface | Loading adapter, health/conformance checks, inference semantics | Deployment assignment is distinct from artifact and promotion |
| Monitoring/feedback | Common telemetry, lineage, feedback ingress envelope | Drift definitions, outcome attribution, retraining recommendation | Drift can create a candidate job, never auto-promote |
| Rollback | Audited assignment transition and revocation mechanism | Compatibility and result-validity rules | Rollback changes future selection; it never rewrites past results |

This preserves the approved modular-monolith boundary. Logical services are module contracts in the same codebase and PostgreSQL/object-storage foundation; they are not separate deployables.

### Independent identity and evidence graph

The following identifiers are independent. Reusing one as another or storing only a composite `model_version` is prohibited.

| Identity | Minimum meaning/evidence |
|---|---|
| `capability_contract_version` | Operation, inputs, outputs, status/error semantics |
| `dataset_version_ref[]` | Immutable tenant-scoped inputs, object digests, readiness/quality/lineage refs |
| `feature_definition_version` | Names, types, units, null rules, availability time, owner, transform refs |
| `feature_schema_version` | Ordered serving/training schema and compatibility policy |
| `feature_transform_code_version` | Source/package/image digest implementing features |
| `label_definition_version` | Target, horizon/window, censoring, exclusions, leakage rules; `NOT_APPLICABLE` when no training |
| `split_policy_version` | Temporal/PIT train-validation-test boundaries and grouping rules |
| `training_code_version` | Source revision plus immutable build/image digest |
| `runtime_environment_version` | Language/library/OS/accelerator lock and determinism flags |
| `experiment_id` / `training_run_id` | Hypothesis/comparison identity and one attempted execution |
| `artifact_id` / `artifact_version` | Semantic artifact identity, bytes digest, format, size, tenant/capability namespace |
| `model_bundle_version` | Exact compatible model, preprocessor, encoder, label map, prompt/policy, or ranking components |
| `evaluation_policy_version` / `evaluation_report_id` | Required metrics/slices/gates and immutable measured evidence |
| `promotion_decision_id` | Actor/authority, decision, rationale, evidence set, time, constraints |
| `deployment_assignment_version` | Tenant/capability/operation/environment to exact approved bundle and rollout mode |
| `capability_config_version` / `policy_version` | Thresholds, horizons, ranking/decoding/business/safety rules |
| `handler_version` / `execution_id` | Exact Stage 08 executable and job/attempt/fence context |
| `result_id` / `prediction_evidence_id` | Immutable output plus all resolved references, observed/as-of time, outcome/fallback |

Every record includes tenant, owner module, created time, actor or execution principal, classification/purpose, and audit reference as applicable. Large payloads remain immutable objects by reference. Aliases such as `candidate` or `production` are query conveniences only; authoritative selection resolves to immutable IDs and digests.

### Experiment and training records

An `ExperimentRun` records hypothesis, baseline, dataset/feature/label/split/code/environment/config refs, seeds, hardware/nondeterminism flags, parent run, metrics, artifacts, status, and author. It is append-only after finalization. Failed and cancelled runs remain visible; deleting an unfavorable run is prohibited.

An explicit training flow is:

1. An authenticated caller submits a versioned capability training operation with immutable datasets and configuration.
2. Control, data readiness, purpose, entitlement, and training permission are checked before Stage 08 creates a durable job.
3. The worker resolves exact code/environment/feature/label/split versions; mutable aliases are rejected.
4. Capability code validates scientific sufficiency and builds PIT-correct features without reading post-cutoff data.
5. Training writes checkpoints only to the run namespace; no candidate is active.
6. The capability evaluates the candidate on untouched validation/test data using a versioned evaluation policy.
7. Immutable artifacts, run manifest, evaluation report, and digests are registered. Registry failure prevents successful finalization.
8. A separate promotion decision may approve the candidate. A separate deployment assignment may activate it.

Retries retain the admitted versions and logical run identity; attempt identities differ. Retry after an ambiguous external/provider effect requires idempotency or reconciliation. Cancellation occurs only at declared safe points. Partial artifacts are quarantined/unreferenced, not selectable.

### Feature and point-in-time contract

Each capability owns a versioned `FeatureDefinitionSet` containing feature name, semantic description, type/unit, entity key, source dataset fields, event/effective/ingested-time meaning, availability delay, observation window, null/default policy, transformation reference, online/offline availability, privacy classification, and owner.

Training examples use an explicit `as_of`/cutoff. A feature is eligible only if its source fact was effective and available under the declared PIT policy at that cutoff. Corrections create new dataset/feature materialization versions; they never mutate an old training snapshot. The training manifest stores the exact row/object digests or immutable partition manifest.

Training-serving consistency is preserved by:

- one versioned transformation package or two implementations with mandatory golden-data conformance tests;
- ordered feature schema and compatibility checks before load/inference;
- immutable offline feature materializations in capability-owned object namespaces;
- explicit online lookup contract only for a measured online operation;
- PIT/leakage, null/default, unit, category-vocabulary, and boundary-time tests;
- feature values or a privacy-safe reproducible feature-vector reference in each prediction record;
- no inference-time fitting, scaler refitting, vocabulary building, or label remapping.

### Feature-store decision

**Decision: a full feature-store product is not justified.** Current evidenced workloads are four tenant-oriented batch prototypes plus three interface-only online LLM calls. No authoritative shared-feature reuse, low-latency feature lookup SLO, online/offline skew incident history, streaming update rate, or organizational need for an independent feature platform exists.

The simplest implementation is capability-owned feature definitions and transform packages; Stage 06 immutable datasets/materializations in object storage; PostgreSQL metadata/lineage; and optional bounded owner-module lookup tables for an approved online feature. This is `C05-15`, not a new shared business-feature owner.

A feature-store product may be reconsidered only when measured evidence shows multiple production capabilities require the same governed features online, PIT joins/backfills cannot be operated safely with these controls, training-serving skew persists despite conformance tests, or latency/scale/ownership isolation justifies extraction. Vendor preference alone is not a trigger.

### Registry, evaluation, and accountable promotion

The logical registry is PostgreSQL metadata plus immutable artifacts in object storage. It stores artifact type, tenant/capability namespace, digest, format, compatibility signature, lineage, state, evaluation refs, revocation, and retention/legal constraints. It does not store large artifacts in PostgreSQL and does not need a standalone registry product.

Artifact states are descriptive: `REGISTERED | QUARANTINED | ELIGIBLE_FOR_REVIEW | REVOKED | RETIRED`. Approval and activation live in separate immutable records; changing a registry flag cannot deploy a model.

Promotion passes only when all applicable gates have evidence:

1. input/label/feature/contract completeness and PIT/leakage checks;
2. reproducible training run and immutable artifact digests;
3. capability-owned evaluation against approved metrics, baselines, slices, and thresholds;
4. calibration, explainability, fairness, content/safety, or human review where the applicability record requires it;
5. artifact/handler/schema/environment compatibility and security/privacy/data-policy review;
6. operational load, failure, rollback, monitoring, cost, and runbook readiness;
7. named authorized scientific recommendation and named release/activation approval under the approved separation policy.

The same person may hold more than one logical role only if Stage 12 policy explicitly permits it; the system must not silently assume self-approval. Because accountable names and numerical thresholds are missing, no current capability can pass production promotion today.

`PromotionDecision` records candidate bundle, evaluation/policy refs, baseline, disposition `APPROVED | REJECTED | CONDITIONAL`, actors/roles, constraints, expiry, rationale, and audit. `CONDITIONAL` is not selectable unless every stated condition is resolved and an effective deployment assignment is separately approved.

### Deployment assignment, selection, and model loading

`DeploymentAssignment` resolves `{tenant, capability, operation, environment, effective interval}` to one exact approved `model_bundle_version`, handler, feature schema, configuration/policy, and rollout mode. Overlapping active assignments for the same scope are rejected. Selection never queries “newest,” unversioned “active,” directory contents, or model version `1` by convention.

Before serving, a worker:

1. resolves the immutable assignment under principal-derived tenant;
2. verifies promotion state, effective interval, revocation, operation, handler, schema, and environment compatibility;
3. fetches artifacts by tenant-scoped reference and verifies digest/size/format;
4. constructs the bundle without fitting or mutation;
5. runs capability load/health conformance checks;
6. uses a bounded local cache keyed by exact bundle digest only; the registry/assignment remains authoritative;
7. records the resolved bundle and evidence in the result.

Load failure keeps a currently healthy previous assignment in service only when it remains approved, compatible, and policy-valid. Otherwise the operation fails or returns an explicitly approved degraded/fallback outcome. It never trains, refits, silently chooses another model, or returns a fabricated score.

### Online and batch inference

| Mode | Stage 10 treatment | Current capability implication |
|---|---|---|
| Immediate synchronous | Allowed only for an approved bounded operation with measured deadline/resource/provider behavior and idempotent evidence commit | No Churn/RFM/NPT/REC prototype qualifies; Synapse interface shape alone does not prove fitness |
| Durable batch | Stage 08 job with fixed dataset/config/bundle/handler versions, manifest output, truthful partial policy, and immutable results | Default production target for Churn, RFM, NPT, and REC |
| Scheduled inference | Scheduler submits the same durable batch operation; schedule cannot select/train a model | Allowed only after operation activation and policy values |
| Shadow | Candidate receives the same versioned input but its result is isolated from business/action paths | Conditional on privacy, cost, deterministic pairing, and comparison evidence |
| Canary | Bounded authorized traffic/tenant cohort uses candidate assignment with defined success/abort signals | Conditional; no percentage, duration, cohort, or automatic expansion invented |

Shadow/canary modes are fields and audited state transitions in the assignment contract, not justification for a new routing service. A direct staged activation with rollback may be simpler when the operation is offline, outputs are not consumed until reviewed, and the approved policy permits it.

### Rollback and revocation

Rollback creates a new assignment version pointing to a previously approved, non-revoked, compatible bundle. It does not mutate the failed assignment, artifact, promotion record, prediction, experiment, or result. The rollback actor records reason, incident/evaluation evidence, effective time, and audit reference.

If no prior compatible bundle exists, the capability becomes unavailable or uses an explicitly approved non-model fallback; compatibility must never be guessed. Revocation prevents new selections and triggers impact analysis for active assignments, caches, pending jobs, results, and required reprocessing. Past predictions retain the bundle that produced them and are not rewritten; corrected results require a new authorized execution/version.

### Monitoring, feedback, drift, and retraining

| Signal | Primary owner | Required distinction/action |
|---|---|---|
| Dataset quality/freshness | Data platform + source owner | Stage 06 readiness; failed data does not become model drift |
| Feature quality/skew/drift | Capability | Compare approved reference/current distributions and transform conformance |
| Prediction/output drift | Capability | Distribution, coverage, fallback, confidence/score semantics; not proof of performance |
| Outcome/performance drift | Capability | Only after versioned labels/outcomes arrive with defined attribution delay |
| Operational performance | Platform operations + capability | Load/inference/training latency, failures, resource/cost by exact version |
| Safety/fairness | Capability + policy authority | Required only under an explicit applicability/policy record, then mandatory for promotion/monitoring |

Feedback is an immutable, tenant-scoped contract linking opaque subject/item, `result_id`/prediction/exposure, outcome type/value/time, source event identity, attribution window/policy, consent/purpose, schema version, and correction/tombstone lineage. Missing feedback is visible; it is never treated as a negative outcome. Duplicate and late feedback follow Stage 06 version/correction rules.

A retraining trigger may be schedule, material ready dataset version, approved drift threshold, performance degradation, policy expiry, or explicit authorized request. It creates a candidate training job with a reason/evidence reference. It never changes deployment assignment or bypasses evaluation/promotion. Numerical thresholds, cadence, cooldown, and minimum outcome counts remain capability policy inputs and production blockers.

### Reproduction manifests and procedure

Every training result has a finalized `TrainingRunManifest`; every prediction/result has a `PredictionEvidenceManifest`.

`TrainingRunManifest` includes all identity rows above plus input partition/object hashes, feature/label/split manifests, seeds, environment lock/image digest, parameters, library versions, hardware/nondeterminism flags, checkpoints, output artifact digests, evaluation report, job/attempt/fence, logs/trace refs, and declared comparison tolerance.

`PredictionEvidenceManifest` includes tenant/capability/operation/contract, request/context and dataset refs, as-of/cutoff, feature schema/transform and privacy-safe vector ref, exact deployment assignment/bundle/artifact digests, configuration/prompt/policy, handler/environment, random seed/decoding parameters where applicable, execution/job/attempt, output/result hash, fallback/degraded reason, and audit/usage refs.

Reproduction procedure:

1. authorize access to the historical evidence without changing it;
2. resolve and checksum every immutable input/artifact/code/environment reference;
3. reconstruct the PIT feature/label snapshot;
4. execute the admitted handler in the recorded environment with the recorded configuration/seeds;
5. compare to the recorded artifact/result using the declared exact or tolerance-based rule;
6. persist a new `ReproductionReport` linked to the original; never overwrite evidence.

For inherently nondeterministic/provider-hosted LLM calls, reproducibility means reconstructing the exact request context and proving the historical response, provider/model identifier, prompt/policy/config, parameters, provider receipt, usage, and evaluations. Byte-identical regeneration is not claimed unless the provider contract proves it. If ARK did not train/fine-tune the provider model, the training evidence is explicitly `EXTERNAL_NOT_APPLICABLE` plus approved provider/model provenance; any later fine-tuning must use the full training manifest.

### Capability ML profiles and production-admission gates

#### CAP-CHURN — `MIGRATION_BLOCKED`

- Required bundle: versioned churn feature/label definitions, scaler/preprocessor, model, calibration, score semantics, explanation policy, configuration, and handler.
- Evaluation: temporal/PIT holdout; discrimination and calibration; threshold/confusion/cost evidence without inventing business costs; stability and slices; forced-score/fallback analysis; reason-code fidelity; fairness applicability if outcomes influence offers/treatment.
- Required remediation: remove train-on-inference and scaler refit; separate training/scoring data; deterministic artifact selection/upload; define target-free inference; remove or explicitly approve/evaluate `new=0` and missing-prediction `100`; canonical opaque join and owned result persistence.
- Activation gate: exact score/probability semantics and lifecycle evidence approved; replay reproduces results; load/persistence failure cannot report success.

#### CAP-RFM — `MIGRATION_BLOCKED`

- Required bundle: R/F/M feature/window/currency definitions, transforms/scaler, optional clustering model, stable semantic-label mapping, weight/config policy, and handler. If an approved deterministic rules approach replaces training, the profile records `NO_TRAINING` rather than inventing a model.
- Evaluation: cluster/segment stability, size/coverage, inertia and appropriate clustering diagnostics, temporal transition stability, semantic mapping correctness, downstream usefulness, and fairness/impact applicability.
- Required remediation: fix feature aliases and recency direction; make industry weights effective/versioned; stop per-run semantic relabeling unless explicitly versioned/evaluated; remove Boolean/DataFrame ambiguity; deterministic artifact lookup/upload; no inference-time training/refit; schema output only `0..4` or an approved replacement.
- Activation gate: same data/features/model/mapping/config reproduce the same segment meaning; insufficient population is explicit and no shared-profile cross-write occurs.

#### CAP-NPT — `MIGRATION_BLOCKED`

- Required bundle: transaction/snapshot feature schema, calendar, label/horizon/censoring definitions, classifier, survival model, routing policy, preprocessor, output mapper, configuration, and handler as one compatible assignment.
- Evaluation: strict temporal splits; classifier F1/confusion plus probability calibration; survival concordance/time-dependent AUC/Brier and horizon calibration; routing/fallback and served-contract correctness; slices and fairness applicability for campaign/offer use.
- Required remediation: restore an active contracted operation; fix configured paths and CLF/RSF output names; remove fast-test RSF configuration from production consideration; prevent load-error retraining; support only approved horizons; isolate debug artifacts; guarantee atomic classifier/survival compatibility.
- Activation gate: output schema and horizon semantics are exact; incompatible bundle cannot activate; ineligible customers and CLF fallback are truthful; replay is idempotent.

#### CAP-REC — `MIGRATION_BLOCKED`

- Required bundle: source/candidate/ranking/filter/diversity/explore-exploit policies, product metadata artifacts, optional learned candidate models, configuration, feature/feedback definitions, and handler.
- Evaluation: temporal holdout Recall/Precision/HitRate/NDCG/MAP at approved K, coverage, diversity, novelty, stability, availability/constraint correctness, cold-start/fallback quality, source ablations, exposure/feedback bias, product/category exposure fairness, and business experiment evidence when available.
- Required remediation: separate any learned ALS fitting from generation and persist/evaluate/select an exact artifact, or approve a non-model algorithm profile before use; repair the top-level gate/fallback contradiction; make partial source loss explicit; ensure empty output is not served success; version feedback/attribution; isolate customer debug data.
- Activation gate: exact datasets/policies/artifacts reproduce ranking under declared tie/random rules; unavailable/unauthorized items cannot rank; feedback retries do not duplicate outcomes/cost.

#### CAP-SYN-CHAT — `EVIDENCE_BLOCKED`

- Required generation bundle: provider/model or hosted deployment ID, system/prompt templates, context assembly/truncation, safety/content policy, decoding/tool/memory declarations, configuration, handler, pricing/usage policy, retention/data-transfer terms, and evaluation suite.
- Evaluation: response quality/relevance, factual/context fidelity, language/channel fitness, refusal/safety, prompt injection, privacy leakage, harmful/bias slices where applicable, latency/cost, and human/LAB rubric. No tools, autonomous memory, or action authority may be inferred.
- Activation gate: authoritative evidence, named owners, tenant-bound/bounded inputs, provider/privacy/security approval, measured synchronous fitness, explicit failure/fallback, and full prediction evidence.

#### CAP-SYN-MSG — `EVIDENCE_BLOCKED`

- Required generation bundle: all Synapse shared evidence plus Persian prompt/version, offer/context authority, length unit/validation, channel and prohibited-claim policies.
- Evaluation: Persian fluency, relevance, offer/occasion fidelity, channel/length compliance, safety/refusal, bias where applicable, latency/cost, and human/LAB rubric.
- Activation gate: generated text is content only; it cannot authorize or deliver a campaign. All provider/prompt/safety/context evidence and exact result lineage must be approved.

#### CAP-SYN-VERIFY — `EVIDENCE_BLOCKED`

- Required generation bundle: provider/model/prompt, exact verification policy/reference/config schemas, safety and failure semantics, authority disclaimer, configuration, handler, and evaluation suite.
- Evaluation: precision/recall or adjudicated agreement against an approved labeled corpus, false-accept/false-reject analysis, calibration only if a score is introduced, robustness/injection, explanation fidelity, bias/safety applicability, latency/cost, and human review.
- Activation gate: `accepted | rejected | failed` remains advisory and cannot replace deterministic policy, permission, grant, or human approval. Empty/opaque references or undocumented agent settings cannot be production inputs.

### Anti-overengineering assessment

| Candidate component | Classification now | Simplest implementation / rejection reason | Reconsideration trigger |
|---|---|---|---|
| Experiment tracker | Required logical capability | PostgreSQL metadata + object evidence; no vendor product | Query/scale/collaboration evidence exceeds simple implementation |
| Dataset/lineage catalog | Already required | Reuse Stage 06 catalog | N/A; do not duplicate |
| Feature store product | Rejected now | Capability definitions/materializations/PIT tests | Measured multi-capability online reuse/skew/latency/operability need |
| Model registry product | Rejected now | `C05-16` PostgreSQL metadata + object storage | Scale, governance, interoperability, or independent ownership evidence |
| Dedicated model-serving gateway | Rejected now | Capability handlers/workers load exact assignments | Multiple measured online workloads need independent scaling/protocol |
| Training orchestrator/workflow engine | Rejected now | Stage 08 durable jobs + private capability pipeline | Approved complex workflow satisfies ADR-005/Stage 08 trigger |
| Broker/streaming feature pipeline | Rejected now | Dataset versions, schedules, conditional outbox only | Measured latency/volume/fan-out need |
| Shadow/canary routing service | Rejected now | Assignment mode in existing control/API/worker boundary | Measured high-volume routing complexity or independent release boundary |
| Drift platform | Rejected now | Capability metrics/evaluation jobs + shared telemetry | Cross-capability operational evidence justifies product/extraction |

## Decisions

- Recommend `decisions/ADR-007-versioned-ml-lifecycle-and-production-admission.md`.
- Shared ARK provides registry/evidence/job/assignment mechanisms; each capability owns feature, label, training, evaluation, inference, drift, and fallback semantics.
- Training, evaluation, promotion, and activation are separate durable/audited operations. Inference never implicitly trains, refits, or activates.
- Exact deployment assignment, not `latest` or a mutable active row, selects the bundle.
- PostgreSQL metadata plus immutable object storage is the initial experiment/artifact/registry implementation.
- A full feature-store product, model-serving gateway, MLOps vendor suite, workflow engine, broker, and standalone rollout/drift service are not justified now.
- Promotion requires versioned evidence and named accountable authority; current missing ownership/threshold evidence blocks all production promotions.
- Churn/RFM/NPT/REC are `MIGRATION_BLOCKED`; Synapse operations are `EVIDENCE_BLOCKED`. These are explicit admission states, not indefinite assumptions.
- Shadow/canary are supported conditional modes, not mandatory rollout products or invented numerical policies.
- Retraining triggers create candidates only; no automatic promotion or action authority follows from drift, feedback, an evaluation, or a verifier response.

## Contradictions and dangerous assumptions

| ID | Tension/hazard | Treatment | Consequence |
|---|---|---|---|
| `C-10-01` | Prototype missing-model behavior treats inference as training | Prohibited; explicit training job and deployment assignment | No accidental unreviewed model activation |
| `C-10-02` | A registry `active` flag can collapse registration, approval, and deployment | Separate artifact, promotion, and assignment records | Auditable authority and rollback |
| `C-10-03` | `latest` or version `1` looks convenient | Exact immutable selection only | Retry/replay cannot silently change science |
| `C-10-04` | Training and serving may recompute features differently | Versioned transform/PIT contract and conformance tests | Skew/leakage becomes detectable and blocking |
| `C-10-05` | Current thresholds/algorithms appear authoritative because they are documented | Migration evidence only until capability gate approval | No silent compatibility or quality claim |
| `C-10-06` | REC fresh ALS can be described as ordinary inference | Learned fitting must have explicit lifecycle or an approved non-model profile | Current run remains blocked |
| `C-10-07` | Synapse API names imply agents, tools, prompts, memory, or production safety | Interface-only evidence; `EVIDENCE_BLOCKED` | No invented internals or Stage 11 conclusion |
| `C-10-08` | LLM regeneration can be claimed byte-reproducible | Reconstruct historical request/response/evaluation; record nondeterminism | Honest reproducibility contract |
| `C-10-09` | Drift alert may automatically retrain/promote | Alert may submit authorized candidate job only | Human/policy promotion gate preserved |
| `C-10-10` | Rollback might rewrite historical results | New assignment affects future selection only | Audit and causal history remain true |
| `C-10-11` | Fairness is either omitted or universally fabricated | Mandatory applicability decision with scoped evidence | No ungrounded protected-attribute collection or missing review |
| `C-10-12` | Feature-store/model-serving products appear necessary for completeness | Logical contracts on existing stores/workers satisfy current evidence | Anti-overengineering preserved |
| `C-10-13` | LAB/metrics can be mistaken for decision authority | Evaluation evidence and promotion authority remain separate | No automated science-to-production authority |
| `C-10-14` | A previous bundle is always a safe rollback | Recheck approval, revocation, schema/handler/data compatibility | Unavailable is safer than incompatible service |

## Open questions

| ID | Question | Blocking? | Options | Recommended temporary treatment | Effect |
|---|---:|---|---|---|---|
| `Q-10-01` | Who are the named scientific recommender, promotion/release approver, security/policy reviewer, and operations/runbook owner per capability? | Before production promotion | Assign people/teams and segregation policy | Remain blocked under `A-04-OWNERSHIP` | Design complete; activation denied |
| `Q-10-02` | What metric, slice, baseline, tolerance, drift, rollback, and expiry thresholds apply per capability? | Before evaluation policy approval | Evidence-based per profile | No default values | No fabricated quality claim |
| `Q-10-03` | Which exact labels, horizons, windows, feature definitions, and scientific minimums are approved for Churn/RFM/NPT/REC? | Before training/promotion | Capability contracts | Preserve Stage 03 target and block production | Prototype values remain evidence only |
| `Q-10-04` | Does REC use evaluated persistent learned artifacts or an explicitly approved non-model/ephemeral algorithm profile? | Before REC activation | Persist lifecycle; omit learned source; approve bounded fit/generate semantics | Current ALS path prohibited | Prevents hidden training |
| `Q-10-05` | Can authoritative Synapse implementation/provider/model/prompt/policy/data/state/safety/evaluation evidence be supplied, or are capabilities scoped out? | Before any Synapse enablement | Supply evidence; scope out | `EVIDENCE_BLOCKED` | Interface inventory retained safely |
| `Q-10-06` | Which capabilities need shadow, canary, or direct staged activation, and what cohorts/signals/abort rules apply? | Before rollout | Per operation risk/evidence | Support contract only; activate none | No invented percentages |
| `Q-10-07` | What feedback/outcome sources, attribution windows, consent/purpose, and correction rules are authoritative? | Before outcome evaluation/retraining | Versioned capability feedback contracts | Treat missing as unknown | Avoid false negatives/causal claims |
| `Q-10-08` | Which operations qualify for immediate synchronous inference after measurement? | Before sync activation | Sync; durable job | Durable batch by default; Synapse unavailable | Preserves Stage 08 admission rule |

## Requirements-traceability updates

| Requirement | Stage 10 design response | Verification direction |
|---|---|---|
| `ARK-FR-004/005` | Capability-owned versioned feature/model/prompt/policy bundles and immutable results | Contract/schema/ownership tests |
| `ARK-FR-006` | Readiness, scientific eligibility, degraded/fallback, and activation state remain distinct | Outcome matrix and fail-closed tests |
| `ARK-FR-007` | Training/evaluation/batch/monitoring use the approved durable job manager | State/retry/cancel/finalization tests |
| `ARK-FR-008/009` | Measured sync admission; explicit training; no inference activation | Negative lifecycle/load tests |
| `ARK-FR-010/011` | Insight/evaluation cannot authorize action; notifications remain separate | No-action and state-isolation tests |
| `ARK-FR-012` | Complete training/prediction/reproduction evidence graph | Manifest completeness/replay tests |
| `ARK-NFR-001` | Tenant-scoped datasets/features/models/experiments/assignments/caches/results | Cross-tenant access/load/promotion tests |
| `ARK-NFR-002/003` | Independent version axes and immutable digests | Historical reproduction/compatibility tests |
| `ARK-NFR-004` | Idempotent jobs/effects, fixed versions, rollback assignment | Retry/duplicate/crash/rollback fault injection |
| `ARK-NFR-005` | Opaque IDs, purpose/classification, privacy-safe vector/feedback evidence | Schema/log/provider-transfer review |
| `ARK-NFR-006` | Correlation across data/run/artifact/evaluation/promotion/deployment/result | Trace graph completeness tests |
| `ARK-NFR-007` | No invented metrics/scale; optional product triggers are measurable | Policy completeness and anti-overengineering review |
| `ARK-CON-001/002` | Same-codebase logical registry/capability modules and one authoritative writer | Dependency/schema-write tests |
| `ARK-CON-004/005` | Object references for large evidence; PostgreSQL metadata/job truth | Integrity/orphan/recovery tests |
| `ARK-CON-007` | No feature-store/MLOps suite/serving gateway/broker/workflow product without evidence | Component inventory and ADR review |
| `SC-02-04/05/06/08/09/10/11/12` | Explicit eligibility, recovery, isolation, lineage, no unauthorized action, ownership, and documented production blocks | Per-capability activation suites |

`quality/source-instruction-coverage.md` marks source prompt section 9 covered by this artifact. Coverage status does not imply sponsor approval.

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Every governing Stage 10 topic addressed | PASS | Source-instruction coverage maps all required topics |
| Platform/capability lifecycle ownership explicit | PASS | Ownership matrix and lifecycle flows |
| Independent versions and evidence graph implementable | PASS | Identity matrix and two manifests |
| Training and prediction can be reconstructed from immutable evidence | PASS VIA EXPLICIT UNAVAILABLE DISPOSITION | No current profile may emit a production result; re-entry requires the target manifests/procedure and reproduction proof |
| Each of seven capabilities has a reproduction/evaluation disposition | PASS | Accepted ADR-007 establishes four `MIGRATION_BLOCKED` and three `EVIDENCE_BLOCKED` profiles with re-entry gates |
| Provider-hosted/LLM nondeterminism treated honestly | PASS | Historical request/response evidence; no byte-identical claim |
| Promotion and rollback have accountable gates | PASS; PRODUCTION ACTIVATION BLOCKED | Separate records/roles are defined; named accountable authorities remain mandatory before re-entry/activation under `A-04-OWNERSHIP` |
| Inference cannot train/refit/activate | PASS | Explicit negative invariant and per-capability remediation |
| Registry/deployment/loading/version selection implementable | PASS | PostgreSQL/object registry, exact assignment, digest/compatibility loading |
| Online/batch/shadow/canary/rollback dispositioned | PASS | Mode table and rollback protocol; no invented rollout values |
| Drift/data quality/performance/feedback/retraining separated | PASS | Monitoring ownership/action matrix |
| Explainability/fairness/safety addressed per capability | PASS | Capability profiles and mandatory applicability decisions |
| Feature-store choice justified | PASS | Product rejected; PIT/version/conformance controls and reconsideration gate |
| Expiring ADR-002 assumptions not silently extended | PASS | Accepted ADR-007 replaces them with explicit blocked profiles and no production enablement |
| Anti-overengineering test applied | PASS | Component classification table |
| Authorized specialist review reconciled | PASS | `data_mlops_architect` findings incorporated; no authoritative edits delegated |
| ADR-007 | PASS | Sponsor accepted the material lifecycle/admission decision on 2026-08-12 |
| Stage 11 not executed | PASS | No Stage 11 artifact or decision created |

**Gate result: PASSED AND APPROVED.** The target architecture provides the evidence and accountable-gate contracts needed for any admitted capability. Accepted ADR-007 makes the present lack of reproducible approved evidence explicit through four `MIGRATION_BLOCKED` and three `EVIDENCE_BLOCKED` profiles, so none can emit a production result until its exact re-entry evidence and named authorities pass. The sponsor accepted those negative production-scope dispositions and approved Stage 10 as written on 2026-08-12.

## Downstream consequences

- Stage 11 must consume the Synapse `EVIDENCE_BLOCKED` boundary and may not infer an agent, tool, memory, planner, or autonomous authority from interface names.
- Stage 12 must define named role binding/separation, training/feedback purpose and consent, provider transfer/retention, artifact/secrets/signing, protected-attribute policy, and model/prompt supply-chain controls.
- Stage 13 must define registry/artifact availability, retry/reconciliation, corruption/revocation, cache failure, rollback incidents, orphan cleanup, and disaster recovery.
- Stage 14 must implement evaluation/quality/drift/usage/cost telemetry and LAB evidence without becoming promotion authority.
- Stage 15 must place CPU/GPU/provider/training/serving roles and stores from measured profiles; logical pools/components are not automatically services.
- Stage 16 must make each capability activation gate executable, including PIT/leakage, reproducibility, compatibility, load, retry, rollback, safety, and migration tests.
- Stage 17 must provide the numeric capacity/cost/latency/quality/rollout evidence needed to activate or extract optional components.
- Stage 18 must include ADR-007 after sponsor disposition.
- Stage 20 must assign named lifecycle/runbook authorities and sequence capability remediation before production enablement.

## Exact next-stage inputs

Approved inputs for Stage 11:

1. Approved `outputs/stages/03-capability-inventory.md`
2. Approved `outputs/stages/08-execution-orchestration.md`
3. Approved `outputs/stages/09-events-proactive-actions.md`
4. Approved `outputs/stages/10-mlops.md`
5. Accepted `decisions/ADR-002-stage-03-capability-evidence-disposition.md` through `decisions/ADR-007-versioned-ml-lifecycle-and-production-admission.md`
6. `sources/normalized/ark-assumptions.md`
7. The three Synapse service cards under their interface-only and `EVIDENCE_BLOCKED` restrictions
8. `stages/11-agent-architecture.md`, `templates/stage-output.md`, and exact governing prompt section **10. Agent architecture, only if justified**

Stage 10 and ADR-007 are approved; the sponsor authorized execution of Stage 11 only.
