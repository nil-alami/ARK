# ADR-012 — Capability-owned feature management before a feature-store product

Status: `ACCEPTED`

Date: 2026-08-13

Decision owner: ARK design sponsor; explicitly approved with Stage 18 on 2026-08-13

## Context and requirements

The governing decision section requires an explicit basic-feature-management-versus-feature-store decision. ARK needs reproducible training/serving transformations, point-in-time correctness, independently versioned feature/label definitions, immutable feature datasets, compatibility checks, and capability ownership. There is no evidence of shared online feature serving, multi-capability reuse, skew, registry scale, or latency that requires a standalone feature store.

## Decision

Use capability-owned versioned transformation packages, feature and label manifests, point-in-time rules and cutoffs, immutable feature datasets/materializations, PostgreSQL metadata, object storage, exact lineage, and golden training-serving conformance tests. Do not select a standalone feature-store product, shared mutable feature table, or cross-capability feature owner.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| Capability-owned versioned transformations and immutable feature datasets | Preserves science ownership and reproducibility using existing stores/jobs | Reuse is explicit rather than automatic; disciplined manifests/tests required | Selected | Measured trigger below |
| Full feature-store product | Online/offline registry, serving and reuse tooling | Vendor/product, migration, semantics, operations and shared-ownership burden | Rejected now | Governed shared reuse/skew/latency/scale need passes |
| Shared mutable feature tables | Easy reuse | Cross-capability coupling, unclear ownership, leakage and drift | Rejected | Never without a superseding ownership model |
| Recompute ad hoc in training and inference | Minimal platform work | Skew, leakage and irreproducibility | Rejected | Never for admitted production profiles |

## Rationale

The required invariants are contracts and evidence, not a product. Existing object storage, PostgreSQL metadata, durable jobs, and capability modules can implement them with lower operational burden while all capability profiles remain blocked.

## Consequences and trade-offs

- Each capability maintains transforms, PIT rules, manifests, conformance tests and derived namespaces.
- Cross-capability reuse must have an explicit owner and versioned public data contract.
- No online feature-serving latency or availability claim exists.
- A future feature store requires migration, tenant isolation, lifecycle, recovery, owner and total-cost evidence.

## Implementation constraints

- Training and serving pin exact dataset/feature/label/transform/code identities.
- No inference-time fitting or implicit feature definition changes.
- No capability reads another capability's private features or mutable state.
- Tenant/capability/purpose isolation applies to materializations and caches.
- Preserve ADR-007/008 admission blocks.

## Validation evidence

- Explicit sponsor approval of Stage 10 and ADR-007 on 2026-08-12.
- Approved Stage 06 data ownership/versioning, Stage 14 evaluation, Stage 16 tests, and Stage 17 triggers.

## Reconsideration trigger

Measured multi-capability governed reuse, online/offline skew, online serving latency/availability, feature registry scale, or operational duplication repeatedly violates an approved target after existing data-contract/materialization remedies, with named owner, security, migration, recovery, benchmark, and cost evidence.

## Supersedes / superseded by

Records and refines accepted ADR-007 Decision items 6–7. Supersedes none. Superseded by: none.
