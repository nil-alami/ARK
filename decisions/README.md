# Architecture decision records

Use `templates/adr.md`. Name records `ADR-NNN-short-title.md`.

Accepted ADRs are immutable historical decisions. To change one, create a new ADR that states which record it supersedes, why evidence changed, and which completed stages must be revised.

The decision index is produced during Stage 18 and published in `outputs/final/ARK-architecture-decisions.md`.

## Working ADR inventory

This operational inventory does not replace the Stage 18 decision index.

| ADR | Decision | Status |
|---|---|---|
| `ADR-000-temporary-source-evidence-disposition.md` | Temporary source-evidence disposition | Accepted |
| `ADR-001-stage-01-requirements-baseline.md` | Stage 01 requirements baseline | Accepted — partially replaced/dispositioned |
| `ADR-002-stage-03-capability-evidence-disposition.md` | Stage 03 capability-evidence disposition | Accepted historical — ownership and Stage-10 ML/Synapse portions replaced |
| `ADR-003-architecture-style.md` | Starting architecture style and boundary principles | Accepted |
| `ADR-004-api-contract-boundary.md` | API contract and integration boundary | Accepted — trust portion replaced; cutover treatment expired |
| `ADR-005-postgresql-job-state-machine.md` | PostgreSQL-first durable job state machine | Accepted |
| `ADR-006-governed-proactive-action-and-delivery.md` | Governed proactive action and delivery boundary | Accepted |
| `ADR-007-versioned-ml-lifecycle-and-production-admission.md` | Versioned ML lifecycle and production admission | Accepted — local cache clause narrowly superseded by ADR-008 |
| `ADR-008-zero-trust-tenant-and-governance-boundary.md` | Zero-trust tenant and governance boundary | Accepted |
| `ADR-009-provisional-python-postgresql-linux-target.md` | Provisional Python, PostgreSQL, and single-Linux-server target | Accepted — provisional target; production blocked |
| `ADR-010-shared-postgresql-owned-schemas-and-object-storage.md` | Shared PostgreSQL infrastructure with owned schemas and object storage | Accepted |
| `ADR-011-push-first-ingestion.md` | Push-first ingestion with referenced bulk data | Accepted — establishes `DATA_CONTRACT_ADMISSION_BLOCKED` |
| `ADR-012-basic-feature-management-before-feature-store.md` | Capability-owned feature management before a feature-store product | Accepted |
| `ADR-013-deterministic-rules-ml-no-agent.md` | Deterministic rules, workflows, and ML; no agent justified by current evidence | Accepted |
| `ADR-014-build-owned-contracts-buy-conditionally.md` | Build ARK-owned contracts; buy or add platforms only from evidence | Accepted |
| `ADR-015-rest-json-and-typed-ports-before-grpc.md` | REST/JSON externally and typed ports internally; no gRPC requirement | Accepted — establishes `CONSUMER_CUTOVER_BLOCKED` |
| `ADR-016-phase-specific-ownership-accountability.md` | Human sponsor accountability for non-production roadmap and Phase 1; later authorities remain fail-closed | Accepted — narrowly supersedes ADR-003 `A-04-OWNERSHIP` Stage-20 expiry treatment |
| `ADR-017-organization-business-capability-pattern-and-admin-scope.md` | Business-level tenant isolation under organization-wide capability patterns and admin scope | Accepted — refines ADR-008 tenant context and ADR-004/015 interface context; clears no production block |
| `ADR-018-owner-billing-account-credit-policy-and-reservation.md` | Shared owner billing balance, organization credit policies, and idempotent job-linked reservation/settlement | Accepted — refines ADR-017/008 and C05-04/C05-18; production charging remains blocked |

Partial supersessions through ADR-016 are recorded in `outputs/stages/18-architecture-decisions.md — Supersession and refinement register`. Post-publication ADR-017 and ADR-018 are indexed in the revised architecture-decision publication and must be included in the next independent assurance baseline. File status alone must not be used to infer that every clause remains current.
