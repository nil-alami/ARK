# ARK architecture decisions — ADR-017/018 publication revision

Status: `POST-PUBLICATION REVISION — ADR-017/018 ACCEPTED; INDEPENDENT RE-ASSURANCE PENDING`

Accepted ADR files remain immutable authority. This index summarizes effective scope; it does not reactivate superseded clauses.

| ADR | Effective decision | Status / current effect |
|---|---|---|
| ADR-000 | Six normalized-only cards are temporary evidence; Synapse is interface-only | Accepted; provenance/internal evidence remains missing |
| ADR-001 | Stage 01 requirements baseline and time-bounded assumptions | Accepted historical; later ADRs replace named portions |
| ADR-002 | Stage 03 capability evidence dispositions | Accepted historical; ownership and Stage 10 ML/Synapse treatments replaced |
| ADR-003 | Boundary-enforced modular monolith and service-extraction gate | Accepted; no extraction qualifies |
| ADR-004 | REST/JSON combined API and consumer adapter boundary | Accepted; trust replaced by ADR-008, cutover by ADR-015 |
| ADR-005 | PostgreSQL-first durable job state machine | Accepted; broker/engine remains evidence-triggered |
| ADR-006 | Deterministic proactive authority and separate delivery | Accepted; paths remain conditional/blocked |
| ADR-007 | Versioned ML lifecycle; four migration and three evidence blocks | Accepted; cache clause narrowly superseded by ADR-008 |
| ADR-008 | Zero-trust tenant/governance boundary and eight security blocks | Accepted; none cleared |
| ADR-009 | Provisional Python/PostgreSQL/one-Linux-server target | Accepted; production environment remains blocked |
| ADR-010 | Shared PostgreSQL infrastructure with owned schemas and object storage | Accepted |
| ADR-011 | Push-first ingestion and concrete contract admission gate | Accepted; `DATA_CONTRACT_ADMISSION_BLOCKED` active |
| ADR-012 | Capability-owned feature management before feature-store product | Accepted |
| ADR-013 | Deterministic rules/workflows/ML; no agent justified by current evidence | Accepted; future agent re-entry cumulative |
| ADR-014 | Build ARK-owned contracts; buy platforms conditionally from evidence | Accepted |
| ADR-015 | REST/JSON and typed ports before gRPC; explicit consumer cutover gate | Accepted; `CONSUMER_CUTOVER_BLOCKED` active |
| ADR-016 | Sponsor accountability only for non-production roadmap/Phase 1 | Accepted; later authorities remain unassigned/fail-closed |
| ADR-017 | Business-level tenant isolation under organization-wide capability pattern and admin scope | Accepted; refines ADR-008 and API context, activates no capability and clears no block |
| ADR-018 | Shared owner billing balance, organization credit policy and job-linked reservation/settlement | Accepted; no organization wallets; production charging is `CREDIT_BILLING_ADMISSION_BLOCKED` |

## Effective supersession register

- ADR-008 replaces Stage 01 trust/security deferrals and the trust portion of ADR-004 with explicit fail-closed production controls.
- ADR-008 narrowly replaces ADR-007’s digest-only cache wording with authorization keyed by tenant, capability/owner, purpose, exact assignment/version and bundle digest; shared bytes require explicit classification.
- ADR-007 replaces ADR-002 `A-03-ML-MIGRATION` and `A-03-SYNAPSE` with explicit per-profile blocks.
- ADR-011 replaces expired `A-01-DATA` for source/canonical activation.
- ADR-015 replaces the expired coexistence/cutover portion of `A-07-INTEGRATION`.
- ADR-016 narrows ADR-003 `A-04-OWNERSHIP` only for Stage 20 and non-production Phase 1; it does not assign later authorities.
- ADR-017 refines ADR-008's single tenant context into stored organization membership/administrative scope plus a derived business tenant/data scope. It refines ADR-004/015 context without changing REST/JSON or typed ports, and it adds no deployable component.
- ADR-018 adds a commercial owner/customer billing boundary above organizations, while preserving organization policy and business tenant scopes. It refines ADR-017/008 plus C05-04/C05-18 usage/quota/audit behavior and adds no deployable or organization subwallet.

## Decisions intentionally not made

No accepted decision selects a production host/provider, HA/DR topology, numeric SLO/RPO/RTO/capacity/cost, identity/secrets/telemetry product, complete account/enrollment fields, phone verification/uniqueness, production source contract, MVP capability slice, scientific thresholds, viewer/tester permission mapping, admin-managed admin membership, ownership/business/billing transfer, cross-business aggregation/export, pricing formula/unit/rounding/currency/tax, credit purchase/grant/expiry/refund/adjustment, policy-window time zone, partial/failure charging, payment processor, accounting system, webhook consumer, broker, feature-store/MLOps product, microservice, gRPC, Kubernetes, GPU, Rust, additional lakehouse, vector store, agent/MCP/A2A, or vendor purchase.

## Reconsideration discipline

A material change requires new evidence, alternatives, owner/operational burden, measurable success and a new or superseding ADR. File existence, passing tests, a local run, AI recommendation or dashboard signal is not approval.

## Provenance

Exact context, alternatives, consequences and triggers are in `decisions/ADR-000-temporary-source-evidence-disposition.md` through `decisions/ADR-018-owner-billing-account-credit-policy-and-reservation.md`. ADR-000 through ADR-016 are indexed by `outputs/stages/18-architecture-decisions.md — Supersession and refinement register`; `— Temporary-assumption lifecycle`; `— Accepted ADR index`. ADR-017/018 are post-publication sponsor evidence governed by their accepted records pending independent re-assurance of the revised publication.
