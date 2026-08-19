# ADR-014 — Build ARK-owned contracts; buy or add platforms only from evidence

Status: `ACCEPTED`

Date: 2026-08-13

Decision owner: ARK design sponsor; explicitly approved with Stage 18 on 2026-08-13

## Context and requirements

The governing decision section requires an explicit build-versus-buy decision. ARK has domain-specific tenant, data, job, model, policy, evidence, and capability contracts that it must own. Hosting products, budget, procurement constraints, prices, support targets, workload scale, and a staffed operations team are unknown. The sponsor selected Python/PostgreSQL/one Linux server provisionally and made no purchase commitment.

## Decision

Build and own ARK's domain/control contracts, module boundaries, schemas, migrations, capability logic, tests, evidence, and runbooks using the approved Python/PostgreSQL baseline and provider-neutral adapters. Do not build substitute infrastructure products when a selected environment service can satisfy an approved contract. Do not buy or select managed platforms, licensed suites, specialized data/ML products, or vendors without a release-scoped requirement, benchmark, security/recovery fit, sponsor operating-cost comparison, budget authority, and explicit material decision.

This is not an “always build” or “never buy” rule. It keeps both self-hosted and managed implementations open while no evidence authorizes a purchase.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| Build all infrastructure in-house | Maximum control | Reinvents databases, storage, identity, secrets, telemetry and operations | Rejected | No reasonable trigger |
| Buy an integrated platform stack now | Faster product assembly | Lock-in, cost, migration, hidden semantics and operator burden without requirements | Rejected now | Exact requirement/TCO/authority packet passes |
| Own ARK contracts and use replaceable built/managed adapters conditionally | Preserves domain authority and portability; permits low-toil managed choices later | Requires interface discipline and explicit evaluations | Selected | Evaluate each concrete component independently |
| Adopt only free/open-source products by default | Avoids license purchase | Still creates hosting, patching, recovery and sponsor-time cost | Rejected as a universal policy | Budget/procurement policy supplied |

## Rationale

ARK cannot outsource its business/scientific/control authority, but it also should not recreate commodity infrastructure. Provider-neutral contracts and the Stage 17 total-cost model let the sponsor compare self-hosted and managed options only when the actual environment, workload, targets, and prices exist.

## Consequences and trade-offs

- No current vendor, managed service, license, or purchase is approved.
- Sponsor time, patching, backup/restore, incident work, egress, lock-in and migration are part of total cost.
- Selected products remain subordinate to ARK ownership, tenant, evidence, recovery and portability contracts.
- Material future purchases/builds require their own approval and possibly a superseding/refining ADR.

## Implementation constraints

- No provider-specific semantics leak into capability cores.
- No product clears ADR-007/008 or deployment/capacity blocks merely by being managed.
- Compare exact measured quantities, price/version/currency, support model, security, backup/restore, exit/migration, sponsor hours and alternatives.
- AI may assist analysis and implementation but cannot approve spend, hold authority, or replace accountable operations.

## Validation evidence

- Sponsor approval of Stage 15 and ADR-009 on 2026-08-13.
- Sponsor approval of Stage 17 on 2026-08-13, including no purchase/build commitment and the evidence-triggered scaling/build-buy ladder.
- Approved Stages 10, 12, 14, 16, and 17 define product-neutral gates and total-cost evidence.

## Reconsideration trigger

A concrete component has an approved requirement and target, repeatable baseline measurements, failed simpler remedies, named owner/runbook, security/recovery evidence, total-cost and exit comparison, budget authority, and explicit sponsor approval.

## Supersedes / superseded by

Records the approved build/buy disposition of Stages 15 and 17 and operationalizes ADR-009. Supersedes none. Superseded by: none.
