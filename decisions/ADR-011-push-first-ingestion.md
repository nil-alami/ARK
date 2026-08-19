# ADR-011 — Push-first ingestion with referenced bulk data

Status: `ACCEPTED`

Date: 2026-08-13

Decision owner: ARK design sponsor; explicitly approved with Stage 18 on 2026-08-13

## Context and requirements

The governing decision section requires an explicit push-versus-pull ingestion decision. ARK consumes tenant data from authoritative upstream systems while preserving raw evidence, immutable versions, corrections, lineage, and distinct structural, semantic, readiness, and capability-eligibility gates. Source cadence, freshness, volume, connectivity, and streaming needs are not yet authoritative.

## Decision

Use authenticated push APIs for small increments and micro-batches, and registered direct object upload/reference for initial loads, backfills, and large datasets. Pull, federation, CDC, and streaming are source-specific exceptions that require an authoritative source contract plus measured freshness/volume need and an owned recovery model. Direct shared-database integration is unsupported.

The temporary `A-01-DATA` treatment expired before Stage 06 approval and is not extended. Replace it with `DATA_CONTRACT_ADMISSION_BLOCKED`: no source or canonical contract may be activated until its authoritative identifiers, event semantics, correction/tombstone rules, schema/version rules, tenant and source authority, data owner, and contract owner are approved and its Stage 06/16 validation evidence passes. The approved Stage 06 logical contract families remain design constraints, not evidence that any concrete source contract is admitted.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| Push/micro-batch plus object-reference bulk | Clear ownership, bounded contracts, simple retries, raw-first evidence | Upstreams must implement delivery and corrections | Selected | A source proves it cannot satisfy an approved requirement |
| ARK polling/pull | Central scheduling | Credentials/connectivity, source load, ambiguous ownership and cursor recovery | Conditional exception | Named source contract and operating owner require it |
| Direct shared-database reads | Fast prototype access | Coupling, authority, schema and security violations | Rejected | No trigger under current boundary |
| CDC/streaming by default | Low-latency continuous flow | Ordering, replay, checkpoint, schema and broker operations without need | Rejected now | Measured freshness/volume requirement passes the streaming gate |
| Federation/query-in-place | Less copying | Availability, reproducibility, performance and authorization depend on upstream | Conditional exception | Approved bounded query contract and SLO evidence |

## Rationale

Push and object-reference bulk are the smallest mechanisms that keep upstreams authoritative while giving ARK immutable intake evidence and durable reprocessing. They avoid permanent source credentials and continuous-processing infrastructure before a real need exists.

## Consequences and trade-offs

- Upstreams own delivery, stable identifiers, sequence/correction semantics, and source contract compliance.
- ARK owns accepted raw evidence, validation, normalization, publication, lineage, and reconciliation.
- Near-real-time behavior is not promised; each source needs a measured freshness profile.
- An exception adds source-specific security, retry, cursor/checkpoint, recovery, and operational work.

## Implementation constraints

- Principal-derived tenant and source authorization; body tenant IDs are not authority.
- Raw evidence is preserved before later acceptance stages.
- Idempotency, corrections/tombstones, sequence/cursor, schema/version, and replay behavior are explicit per source.
- Large payloads use tenant-scoped opaque object references.
- No broker/stream processor or pull connector is introduced merely for completeness.
- `DATA_CONTRACT_ADMISSION_BLOCKED` is fail-closed and independent of structural test success; only the named source/data authorities plus recorded approval can clear it for a concrete contract.

## Validation evidence

- Explicit sponsor approval of `outputs/stages/06-data-architecture.md` on 2026-08-11.
- Accepted ARK baseline in `sources/normalized/ark-assumptions.md — Ingestion and the ARK data lake`.
- Approved Stages 08, 13, 16, and 17 provide job, failure, test, and capacity gates.

## Reconsideration trigger

A named source cannot meet an approved freshness, volume, reliability, or ownership objective through push/object paths, and the proposed pull/federation/CDC/streaming alternative has exact contracts, tenant/security controls, checkpoint/replay semantics, owner/runbook, benchmark, and cost evidence.

## Supersedes / superseded by

Records the approved Stage 06 ingestion decision, refines ADR-003's conditional event stance, and replaces expired `A-01-DATA` with the explicit fail-closed contract-admission disposition above. Superseded by: none.
