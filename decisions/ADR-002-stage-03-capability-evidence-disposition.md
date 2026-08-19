# ADR-002 — Stage 03 capability-evidence disposition

Status: `ACCEPTED`

Date: 2026-08-11

Decision owner: ARK design sponsor (user approval)

## Context and requirements

Stage 03 must represent every named ML/AI capability with a compact contract and must stop for an explicit disposition when a named capability lacks sufficient evidence. Seven cards are present. Churn, RFM, next-purchase prediction (NPT), and recommendation (REC) describe current prototype behavior in enough detail to expose material contract, correctness, lifecycle, ownership, and isolation gaps. The three Synapse cards are admitted by `ADR-000` only as interface-contract evidence; their undocumented implementation, model, prompt, policy, state, safety, and operational behavior must remain unresolved.

The Stage 01 assumptions that deferred capability ownership and ML lifecycle questions expire at the Stage 03 gate. A narrow replacement decision is therefore required before Stage 03 can pass without inventing facts or silently removing named capabilities.

Evidence: `stages/03-capability-inventory.md — Gate`; `outputs/stages/01-discovery-and-questions.md — ML-01, ML-04, ML-05, ML-06`; `decisions/ADR-000-temporary-source-evidence-disposition.md — Decision`; `outputs/stages/03-capability-inventory.md — Completion-gate evidence`.

## Decision

The sponsor accepts the following temporary dispositions:

1. **`A-03-OWNERSHIP` — logical owners pending accountable assignments.** Each capability remains a distinct logical ownership boundary. Its named accountable product/ML/operations owner is `TBD`. No capability may be declared production-ready, promoted, or enabled for tenants until those authorities and a runbook owner are assigned. This assumption expires before Stage 04 approval for architecture responsibility mapping, or earlier when authoritative ownership assignments are supplied.
2. **`A-03-ML-MIGRATION` — prototype behavior is migration evidence, not the production contract.** Churn, RFM, NPT, and REC retain their documented current behavior solely as implementation and migration evidence. The intended contracts in the Stage 03 inventory are provisional target requirements. Inference must not train or activate a model implicitly; current thresholds, algorithms, feature semantics, forced scores, per-run relabeling, test configurations, and persistence behavior are not accepted as production decisions. This assumption expires for each capability when its contract, remediation evidence, lifecycle, evaluation gates, and promotion authority are approved, and no later than the applicable Stage 10 and Stage 16 decisions.
3. **`A-03-SYNAPSE` — retain interface-only capabilities as non-production-eligible.** Chatbot, message generator, and campaign verifier remain in the product capability inventory using only their documented HTTP interfaces. Every undocumented internal remains `UNRESOLVED`. They are not production-eligible until authoritative implementation, provider/model, prompt/policy, data-access, state, safety, privacy, reliability, observability, evaluation, and ownership evidence is supplied. No agentic behavior, tools, autonomous memory, proactive authority, external-action authority, or direct platform/private-state access is inferred. The campaign verifier's `accepted | rejected | failed` response is advisory evidence only and is not authoritative permission or policy enforcement. This assumption expires when authoritative evidence is registered, the capability is explicitly scoped out, or before the relevant Stage 10, Stage 12, Stage 14, Stage 15, or production-enablement decision—whichever comes first.

Approval of this ADR dispositions the evidence gaps for workflow design only. It does not declare any capability production-ready, approve current algorithms or thresholds, authorize external data transfer to an LLM, select a provider or platform, or permit later stages to fill unresolved fields by convention.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| Supply authoritative originals, implementations, configuration, policy, ownership, and operational evidence | Replaces temporary gaps with verifiable contracts | Evidence is not currently available | Preferred long-term | Use whenever evidence is available |
| Explicitly remove under-evidenced capabilities from ARK product scope | Removes unsupported capability commitments | Changes the approved product boundary | Not selected | Sponsor chooses a narrower product scope |
| Approve the three temporary dispositions above | Preserves all named capabilities and lets reversible architecture work continue without invented internals | Production eligibility remains blocked; expiry points require later evidence and decisions | Recommended short-term | Replace each assumption at its expiry |
| Infer conventional implementation, safety, storage, agent, or ownership details | Produces apparently complete contracts | Violates source authority and conceals material risk | Rejected | Never without evidence or explicit decision |

## Rationale

The proposed disposition is the smallest reversible choice that preserves the Stage 02 product boundary, honors the Synapse evidence restriction, and prevents known prototype behavior from becoming an accidental production contract. It separates inventory completeness from production readiness and creates explicit expiry points for every temporary treatment.

## Consequences and trade-offs

- Stage 03 may pass after explicit sponsor approval; Stage 04 then becomes the next incomplete stage.
- All seven capabilities remain visible, but none gains production approval from this decision.
- Stage 04 may assign logical architecture responsibilities, but it may not imply staffed teams or independent deployments.
- Stages 05–16 must consume the intended contracts and migration gaps, not normalize current prototype defects into platform behavior.
- Synapse-dependent design remains bounded to interface integration until authoritative internals arrive.
- Production planning remains unable to commit owners, quality gates, capacity, SLOs, recovery, cost, or compliance targets.

## Implementation constraints

- Cite the relevant `A-03-*` identifier wherever a downstream design depends materially on it.
- Keep current implementation facts, intended ARK requirements, recommendations, and unresolved fields visibly separate.
- Do not mutate source cards or treat normalized-only evidence as provenance-verified originals.
- Do not permit inference to train or activate a model.
- Do not treat a Synapse endpoint name or response enum as proof of agentic behavior, authoritative policy enforcement, persistence, safety controls, or external-action authority.
- Reopen the affected capability contract when an assumption expires or new evidence conflicts with it.

## Validation evidence

- User approval dated 2026-08-11: “I approve Stage 03 and its outputs.”
- All seven named cards are represented in `outputs/stages/03-capability-inventory.md`.
- One configured `capability_analyst` reviewed each card under the Stage 03 authorization.
- `ADR-000` restricts Synapse facts to documented interfaces.
- The Stage 03 inventory records current behavior, intended boundaries, migration work, unresolved evidence, and acceptance tests separately.

## Reconsideration trigger

Any assumption expiry above; receipt of original or implementation evidence; accountable owner assignment; a capability-scope change; or discovery that an intended contract is unsafe, infeasible, or inconsistent with authoritative evidence.

## Supersedes / superseded by

If accepted, this ADR replaces `A-01-ML` only for ML-01, ML-04, ML-05, and ML-06 at the Stage 03 gate; all unrelated portions of the accepted Stage 01 baseline remain active until their own expiry points. It does not supersede `ADR-000` or `ADR-001`. Not superseded.
