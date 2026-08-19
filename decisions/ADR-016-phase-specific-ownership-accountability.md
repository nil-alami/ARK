# ADR-016 — Phase-specific ownership accountability

Status: `ACCEPTED`

Date: 2026-08-13

Decision owner: Human ARK sponsor

## Context and requirements

Accepted ADR-003 introduced `A-04-OWNERSHIP`: logical roles were sufficient during architecture design, but named accountable product, data, platform, capability/scientific, security, integration, and operations owners remained unresolved. That treatment expires before Stage 20 approval, service extraction, or any production-readiness decision—whichever occurs first.

The sponsor has stated that ARK will be developed and operated by the sponsor with AI assistance and without an assumed 24/7 operations team. This identifies the implementation model but does not make AI an authority or silently assign the sponsor every scientific, security, data-contract, integration, release, or production-operations qualification. Stage 20 nevertheless requires accountable ownership for its non-production roadmap and immediately buildable proof-of-architecture milestone.

Evidence: `decisions/ADR-003-architecture-style.md — Decision`; `outputs/stages/18-architecture-decisions.md — Temporary-assumption lifecycle`; `outputs/stages/20-roadmap.md — Blocking ownership decision`; explicit sponsor decision dated 2026-08-13.

## Decision

Replace only the Stage-20-expiry treatment of `A-04-OWNERSHIP` with phase-specific, fail-closed accountability:

1. The human ARK sponsor is accountable for the non-production roadmap, Phase 1 scope, contract acceptance, implementation review, and test-evidence acceptance.
2. AI may perform analysis, drafting, coding, testing, and review assistance but is a non-authoritative implementer. It cannot approve its own output, clear a block, accept risk, authorize spend, promote a model, perform a privileged decision, or act as an accountable owner.
3. Named data/source-contract authority remains unassigned and is required before any concrete Phase 2 source or canonical contract can clear `DATA_CONTRACT_ADMISSION_BLOCKED`.
4. Named capability/scientific authority remains unassigned and is required before any ADR-007 capability profile can clear, or any model/artifact can be promoted or assigned.
5. Named security/governance and privileged-operation authorities remain unassigned. Required separation of duties and named approval are mandatory before any ADR-008 block clearance or privileged production operation.
6. Named integration/consumer authority remains unassigned and is required before consumer cutover, external delivery, or external provider activation.
7. Named release and production-operations accountability remains unassigned. An accepted runbook, support/on-call scope, and applicable separated authorities are required before Phase 3 production admission.
8. Service extraction remains prohibited until ADR-003's evidence gate passes and a named staffed owner accepts independent contract, state, deployment, on-call, and runbook responsibility.
9. This decision clears no production-admission block and authorizes no production release, privileged action, external delivery/provider use, customer cutover, model promotion/assignment, or service extraction.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| Assign all named specialist and production owners now | Fully resolves every ownership gap | People, scope, qualifications, separation, and support expectations are not yet authoritative | Not currently evidenced | Authoritative assignments are available |
| Human sponsor owns non-production roadmap/Phase 1; later authorities remain fail-closed | Makes the first milestone accountable without inventing specialist authority or weakening production gates | Sponsor carries implementation-review burden; later phases cannot proceed without more assignments | Selected | Phase 2/3 reaches the first decision requiring a missing authority |
| Let AI own implementation or approvals | Reduces apparent human workload | No accountable authority, self-approval, unsafe risk acceptance, and conflict with project governance | Rejected | No reconsideration under the current project authority model |
| Leave Stage 20 blocked | Avoids changing ADR-003 | Prevents approval of an otherwise implementable non-production roadmap | Rejected by sponsor decision | Sponsor pauses the project |

## Rationale

The selected option matches the sponsor-operated, AI-assisted project while keeping authority proportional to risk. Phase 1 uses synthetic fixtures, test-only trust, and a deterministic proof handler; the sponsor can accountably accept its contracts and evidence without claiming scientific, security, source-data, integration, or production qualifications. Later decisions remain unavailable until the correct named authorities exist.

This is narrower and safer than assigning all roles to one person by implication. It also avoids blocking non-production engineering work merely because production staffing and scope are not yet known.

## Consequences and trade-offs

- Stage 20 can complete and Phase 1 can be implemented under sponsor accountability.
- The sponsor must review AI-generated implementation and test evidence; AI output is never self-approving.
- Phase 2 may begin planning, but any concrete data contract, capability re-entry, consumer integration, or governed action waits for its named authority.
- Phase 3 production admission remains impossible until release, production-operations, security/governance, and all other applicable ownership requirements are assigned and evidenced.
- A single sponsor remains a concentration of non-production implementation responsibility; automation and bounded scope reduce workload but do not create authority.
- This decision does not establish a 24/7 support commitment or satisfy separation-of-duties requirements.

## Implementation constraints

- Every roadmap work item and evidence manifest identifies whether the accountable actor is the human sponsor or an unresolved later authority.
- Test-only trust, source contracts, fixtures, and handlers are impossible to configure as production artifacts and are identified in the immutable release/evidence manifest.
- Block transitions require the authority named by the governing ADR/stage, tests, evidence, and a recorded decision; sponsor Phase 1 accountability alone is insufficient.
- Privileged production commands, model promotion/assignment, external effects, release promotion, and service extraction remain absent or fail closed until their ownership gates pass.
- Future owner assignments record identity, scope, allowed decisions, required separation, runbook/support responsibility, effective date, and replacement/revocation procedure.

## Validation evidence

- The sponsor explicitly approved the narrow ADR-016 disposition on 2026-08-13 using the exact scope recorded in this decision.
- The Stage 20-authorized `platform_architect` found the five-phase sequence defensible and identified `A-04-OWNERSHIP` expiry as the sole architecture approval blocker.
- `outputs/stages/20-roadmap.md — Active block-preservation register; Blocking ownership decision; Dependency and evidence-gate matrix` preserves every later authority and production block.
- Stage 21 and all later stages remained unexecuted when this decision was recorded.

## Reconsideration trigger

Reconsider when Phase 2 selects a concrete source/capability/consumer, Phase 3 production admission begins, a privileged or external path is proposed, a named owner changes, separation-of-duties policy is supplied, the sponsor operating model changes, or service extraction is proposed. Record assignments or a superseding ADR before the first affected decision.

## Supersedes / superseded by

Narrowly supersedes ADR-003 `A-04-OWNERSHIP` only as to its “before Stage 20 approval” expiry and the use of logical roles for non-production Phase 1. It preserves ADR-003's production-promotion and service-extraction ownership prohibitions and all architecture-style decisions. Superseded by: none.
