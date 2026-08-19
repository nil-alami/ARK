# ADR-007 — Versioned ML lifecycle and production admission

Status: `ACCEPTED`

Date: 2026-08-12

Decision owner: ARK sponsor (human user), by explicit approval on 2026-08-12; capability scientific, release, security/policy, and operations authorities remain unassigned

## Context and requirements

ARK must track contract, dataset, feature-schema, model, code, configuration, and execution versions independently; separate training from inference; reproduce training and predictions; evaluate and promote models through accountable gates; support safe activation and rollback; and avoid unjustified feature-store or MLOps products.

Accepted ADR-002 temporarily treated Churn, RFM, NPT, and REC prototype behavior as migration evidence under `A-03-ML-MIGRATION`, and the three Synapse capabilities as interface-only/non-production under `A-03-SYNAPSE`. Both dispositions reach an explicit expiry at the applicable Stage 10 decision. They cannot be silently extended.

Current evidence cannot pass the literal Stage 10 operational gate:

- Churn, RFM, NPT, and REC lack approved production feature/label semantics, evaluation policies, artifact bundles, promotion authorities, and remediation evidence. Each also contains training/serving, registry, contract, or persistence defects.
- Synapse cards omit provider/model, prompts/policies, data/state, safety, reliability, evaluation, and lifecycle evidence; only HTTP interface shapes are authoritative.
- Accepted `A-04-OWNERSHIP` blocks promotion and production enablement until named accountable lifecycle and runbook/on-call authorities exist.

The decision must preserve all seven named capability entries without treating missing evidence or prototype defaults as approved production behavior.

## Decision

1. ARK adopts the Stage 10 lifecycle contract in `outputs/stages/10-mlops.md` as the target production-admission architecture:
   - shared platform mechanisms provide immutable dataset/evidence references, durable jobs, experiment/registry metadata, audited promotion records, exact deployment assignments, artifact integrity, and common telemetry;
   - each capability owns feature/label/prompt semantics, training, evaluation, scientific eligibility, model/configuration bundle compatibility, inference, explanations, drift, feedback interpretation, retraining criteria, and fallbacks;
   - training, evaluation, promotion, deployment assignment, and inference are separate operations;
   - inference may not train, fit/refit preprocessing, register, promote, or activate implicitly;
   - model selection uses an exact immutable deployment assignment, never `latest`, directory order, or a mutable active flag;
   - rollback creates a new assignment to a previously approved, compatible, non-revoked bundle and never rewrites historical results.

2. Replace `A-03-ML-MIGRATION` at its Stage 10 expiry with four explicit capability production-admission states:
   - `CAP-CHURN: MIGRATION_BLOCKED`
   - `CAP-RFM: MIGRATION_BLOCKED`
   - `CAP-NPT: MIGRATION_BLOCKED`
   - `CAP-REC: MIGRATION_BLOCKED`

   Current algorithms, thresholds, feature semantics, artifacts, scores, mappings, training behavior, persistence, and prototype fallbacks remain migration evidence only. This is a durable negative readiness decision, not an assumption and not approval of current behavior. A capability exits `MIGRATION_BLOCKED` only through a later evidence-backed decision showing its Stage 10 profile-specific remediation, reproducibility, evaluation, named authority, deployment, rollback, and Stage 16 test gates pass.

3. Replace the Stage 10 portion of `A-03-SYNAPSE` with three explicit evidence states:
   - `CAP-SYN-CHAT: EVIDENCE_BLOCKED`
   - `CAP-SYN-MSG: EVIDENCE_BLOCKED`
   - `CAP-SYN-VERIFY: EVIDENCE_BLOCKED`

   Only the documented interface shapes remain in the inventory. No provider/model, prompt, training/fine-tuning, retrieval, tool, memory, agent, state, data access, safety, reliability, evaluation, proactive, or external-action behavior is inferred. The verifier remains advisory and cannot authorize policy or action. A Synapse capability exits `EVIDENCE_BLOCKED` only after authoritative evidence is registered and the affected Stage 03/10 contracts and later security/observability/deployment gates are reviewed, or it is explicitly scoped out.

4. The blocked profiles satisfy inventory disposition only after sponsor acceptance of this ADR. They do not satisfy production readiness or historical training/prediction reproduction, and they may not execute as production capabilities. Until this ADR is accepted or missing evidence is supplied, Stage 10 remains blocked and Stage 11 is unauthorized.

5. Promotion and activation require immutable evaluation evidence plus named accountable authority. Logical roles may be designed under `A-04-OWNERSHIP`, but no artifact may be promoted or tenant-enabled while those names, permitted role combinations/separation, and runbook/on-call authorities are absent.

6. PostgreSQL metadata plus immutable object storage is the initial experiment/artifact/registry mechanism. A full feature-store product, standalone registry/experiment suite, dedicated model-serving gateway, training workflow engine, broker/streaming feature pipeline, and separate rollout/drift platform are not selected.

7. Capability-owned versioned transformation packages, immutable feature datasets, point-in-time rules, exact cutoffs, feature/label manifests, compatibility checks, and golden training-serving conformance tests preserve consistency without a full feature store.

8. Shadow and canary are conditional deployment-assignment modes. No rollout percentage, duration, cohort, metric threshold, or automatic expansion is selected without authoritative requirements and measured evidence. Retraining triggers create candidates only and never auto-promote.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| Accept target lifecycle plus explicit blocked profiles | Preserves all named capabilities, expires old assumptions honestly, prevents unsafe enablement, and permits later evidence-based re-entry | No current ML/AI capability is production-admitted; later decisions/tests required | Recommended | Replace a profile when its evidence and gates pass |
| Continue ADR-002 assumptions | Avoids a decision now | Violates explicit expiry and can turn temporary prototype/interface evidence into an indefinite baseline | Rejected | Not applicable |
| Approve prototype algorithms/contracts as production baseline | Fastest apparent path | Contradicts documented defects, separation rules, reproducibility, and accountable promotion | Rejected | Only after remediation/evidence, which becomes the recommended option |
| Remove all seven capabilities from ARK scope | Simplifies gate | Contradicts the authoritative named inventory without sponsor scope decision | Not selected | Sponsor explicitly scopes out named capabilities |
| Keep Stage 10 blocked until all implementation evidence exists | Strict literal gate with no negative disposition | Prevents later design stages from addressing security/reliability/testing concerns needed for re-entry | Viable alternative requiring sponsor choice | Sponsor rejects blocked-profile disposition |
| Select a full MLOps/feature-store suite now | Bundled tooling and familiar UI | Adds vendor, operating, migration, ownership, and consistency complexity without evidenced need | Rejected | Measured triggers in Stage 10 anti-overengineering table pass |

## Rationale

The selected proposal is the smallest fail-closed decision that respects source authority and the Stage 10 expiry. It converts temporary evidence assumptions into explicit production-admission states with testable re-entry criteria, while preserving the seven-capability inventory. It does not claim that an unavailable capability is reproducible; it makes that failure durable and visible.

Separating artifact registration, scientific approval, deployment assignment, and execution prevents a model file or registry row from becoming authority. Reusing Stage 06 datasets, Stage 08 jobs, Stage 05 logical registry/storage components, and existing module boundaries achieves the required lifecycle without a new platform product.

## Consequences and trade-offs

- No current capability may be described as production-ready, promoted, activated, or reproducible from approved evidence.
- Stage 10 remains blocked until the sponsor accepts the negative production-scope dispositions or supplies authoritative evidence.
- After acceptance, later stages may consume the target lifecycle and blocked profiles, but they may not silently enable a capability.
- Each re-entry decision must name the exact capability profile, evidence, approved metrics/thresholds, owners, compatibility, rollout/rollback, and tests; one capability's approval does not approve another.
- Historical prototype compatibility is not promised. Consumer migration requirements remain a separate explicit decision.
- Provider-hosted LLM reproducibility is historical-request/evidence reconstruction unless the provider proves deterministic regeneration; byte identity is not claimed.
- Offline/batch replay may be sufficient for rollout; a separate online routing platform is not required.
- The design carries more metadata and disciplined approvals than the prototypes, but that cost is required for tenant isolation, auditability, rollback, and scientific truth.

## Implementation constraints

- Preserve one authoritative writer per registry, promotion, assignment, capability artifact/result, feedback, and audit record.
- Store large datasets, feature materializations, artifacts, reports, and manifests by immutable tenant-scoped object reference and checksum; PostgreSQL stores bounded metadata.
- Make contract, dataset, feature, label, split, code, environment, artifact bundle, evaluation policy/report, configuration/policy, handler, deployment assignment, execution, and result identities independently queryable.
- Pin admitted versions before a job executes and retain them across retry; never resolve a mutable alias during an attempt.
- Require artifact digest, format, tenant/capability namespace, schema/preprocessor/handler/runtime compatibility, promotion state, assignment interval, and revocation checks before load.
- Keep local caches bounded and keyed by exact bundle digest; a cache is never selection authority.
- Preserve past predictions/results and activation history during rollback/revocation; corrected output is a new execution/version.
- Require explicit fairness/safety applicability per capability. Do not collect protected attributes without approved purpose/policy.
- Treat missing/late feedback as unknown, not negative; retain attribution and correction lineage.
- Block production activation while named scientific, release, security/policy where applicable, and operations/runbook authorities or required evaluation thresholds are absent.
- No Stage 11 agent conclusion, provider/tool/memory behavior, or external-action authority follows from this ADR.

## Validation evidence

- `outputs/stages/10-mlops.md` maps every governing Stage 10 requirement and defines the ownership split, independent identity graph, training and inference manifests, point-in-time feature controls, registry/promotion/assignment/rollback contracts, monitoring/feedback/retraining semantics, capability profiles, and optional-product triggers.
- The Stage 10-authorized read-only `data_mlops_architect` found that the literal current gate fails, recommended explicit negative readiness dispositions at the two ADR-002 expiries, and confirmed that a standalone feature store is unjustified. Those findings are reconciled in this ADR and the Stage 10 blocked gate.
- Required future validation is enumerated per capability in `outputs/stages/10-mlops.md — Capability ML profiles and production-admission gates` and `— Requirements-traceability updates`.
- User approval dated 2026-08-12: “I accept ADR-007’s explicit production-admission dispositions and approve Stage 10 as written. Record the approval and execute only Stage 11.”

## Reconsideration trigger

- A capability supplies authoritative feature/label/prompt/provider/policy, training, evaluation, ownership, deployment, rollback, safety, and test evidence sufficient to exit its blocked profile.
- The sponsor explicitly scopes a capability out or changes its product boundary.
- Measured multi-capability online feature reuse, skew, latency, registry scale, rollout complexity, training orchestration, or operational isolation passes an optional-product trigger.
- Stage 12–17 evidence materially changes lifecycle, security, reliability, deployment, testing, or capacity constraints.
- A provider/model contract invalidates recorded reproducibility, retention, or rollback assumptions.

## Supersedes / superseded by

If accepted, this ADR replaces `A-03-ML-MIGRATION` and the Stage 10 MLOps portion of `A-03-SYNAPSE` from accepted ADR-002. It does not supersede ADR-002's historical evidence ruling, normalized-only source restrictions, advisory verifier boundary, or later Stage 12/14/15/production-enablement gates. It refines ADR-003 through ADR-006 without superseding them. Superseded by: none.
