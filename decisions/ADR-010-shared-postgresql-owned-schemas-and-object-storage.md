# ADR-010 — Shared PostgreSQL infrastructure with owned schemas and object storage

Status: `ACCEPTED`

Date: 2026-08-13

Decision owner: ARK design sponsor; explicitly approved with Stage 18 on 2026-08-13

## Context and requirements

The governing decision section requires an explicit shared-versus-separate-database decision. ARK needs transactional operational truth for control, jobs, catalogs, registry, audit, and usage, while large immutable raw, datasets, results, artifacts, and evidence should not become PostgreSQL payloads. Logical capability ownership must not be weakened by shared infrastructure. Exact production placement, scale, retention, and recovery targets remain unknown and blocked.

## Decision

Start with one PostgreSQL cluster as shared physical infrastructure, using module-owned schemas, migrations, roles, tables, and one authoritative writer per state set. Other modules use public application ports or approved bounded read models; unrestricted cross-schema writes/joins are prohibited. Large immutable histories, datasets, features, results, model artifacts, and evidence use a provider-neutral object-storage interface with PostgreSQL holding bounded metadata and opaque references.

Separate databases or clusters are not selected now. A module may receive a separate database only through ADR-003's extraction gate or authoritative security/residency/reliability/scale evidence. A local filesystem is developer/test fixture storage, not an approved production data lake.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| One unrestricted shared schema/database | Lowest coding friction | Cross-writes, hidden coupling, weak ownership and tenant isolation | Rejected | Never without a superseding ownership decision |
| Shared PostgreSQL cluster with owned schemas/writers plus object storage | Simple operations, transactional owner state, explicit boundaries, suitable extraction seam | Requires dependency/schema/RLS/access discipline; shared failure/resource domain | Selected | Exact module passes extraction or database-isolation gate |
| Separate database per module/capability | Stronger physical isolation and independent lifecycle | Connection, migration, backup, consistency, observability and operating burden | Rejected now | Measured scale/failure/release or mandatory security/residency boundary |
| Separate technology per workload | Specialized performance | Polyglot persistence and staffing burden without evidence | Rejected now | Approved workload cannot meet target after existing-store remedies |

## Rationale

Shared infrastructure is the simplest fit for one coordinated modular-monolith release and one human operator. Owned schemas, public ports, least-privilege roles, tenant controls, and tests preserve logical ownership without premature distributed data operations. Object references keep PostgreSQL bounded.

## Consequences and trade-offs

- PostgreSQL and its backups are a shared operational dependency and require contention, recovery, and isolation testing.
- Schema sharing never grants business ownership or direct writes.
- Cross-store publication is metadata-atomic and requires orphan/missing-object reconciliation.
- Separate databases remain possible but require evidence, named ownership, migration, recovery, and cost acceptance.

## Implementation constraints

- Owner-qualified schemas, migrations, roles, repositories, and commands.
- Principal-derived tenant scope and owner authorization on in-process and job paths; RLS is defense in depth.
- No large opaque payloads or histories in operational rows when object references are required.
- No database-per-capability deployment follows from a logical module boundary.
- Preserve all ADR-008 security blocks and `DEPLOYMENT_ENVIRONMENT_BLOCKED`.

## Validation evidence

- Explicit sponsor approval of Stage 04 and ADR-003 on 2026-08-11.
- Explicit sponsor approval of `outputs/stages/06-data-architecture.md` on 2026-08-11.
- Explicit sponsor approval of Stage 15 and ADR-009 on 2026-08-13.
- Approved Stages 12, 13, 16, and 17 define isolation, reconciliation, testing, and measured split triggers.

## Reconsideration trigger

A module passes ADR-003's service-extraction gate; shared-database contention/failure repeatedly violates an approved objective after query/index/pool/role remedies; or an authoritative security, residency, key, audit, recovery, or independent-release requirement mandates physical separation.

## Supersedes / superseded by

Records and refines the database/storage portion of accepted ADR-003, ADR-007, and ADR-009. Supersedes none. Superseded by: none.
