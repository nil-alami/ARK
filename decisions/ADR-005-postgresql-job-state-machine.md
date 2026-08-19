# ADR-005 — PostgreSQL-first durable job state machine

Status: `ACCEPTED`

Date: 2026-08-11

Decision owner: ARK design sponsor (user approval)

## Context and requirements

ARK needs one durable execution contract for asynchronous inference, ingestion, batch, backfill/reprocessing, training/evaluation, schedules, and any later approved event-triggered or named workflow submissions. That contract must make retries, cancellation, timeout, partial failure, crash recovery, routing, concurrency, duplicate suppression, and result truth implementable without introducing a broker or general workflow product without evidence.

Approved Stages 02, 05, 06, and 07 require one durable lifecycle, PostgreSQL as the initial operational authority, at-least-once worker behavior with idempotent visible effects, exact immutable input/version references, owner-committed results before success, stable public job states, and notification delivery separate from result truth. Stage 08 owns the internal state graph and component responsibilities but does not authorize Stage 09 events/actions or Stage 10 model lifecycle semantics.

Evidence: `sources/normalized/ark-assumptions.md — Execution, orchestration, and proactive operation`; `outputs/stages/02-system-definition.md — ARK-FR-007/008`, `— ARK-NFR-004/006`; `outputs/stages/05-end-to-end-architecture.md — Consumer-to-result flow: durable asynchronous operation`, `— C05-08 through C05-12`, `— C05-21/C05-22`; `outputs/stages/06-data-architecture.md — Backfill and reprocessing protocol`, `— Version and compatibility policy`; `outputs/stages/07-api-integration.md — Job contract`, `— Idempotency contract`; `decisions/ADR-003-architecture-style.md`; `decisions/ADR-004-api-contract-boundary.md`.

## Decision

ARK will use one PostgreSQL-first durable job system with these boundaries:

1. The job-manager module owns `jobs`, `job_attempts`, command idempotency records, concurrency leases, claims, heartbeats, retry scheduling, deadlines, cancellation, progress, result references, and the stable public-state mapping. A queue is an indexed claimable projection over owned job records, not a second authority.
2. Internal job states are `ACCEPTED | WAITING | READY | RUNNING | RETRY_WAIT | FINALIZING | CANCELLATION_REQUESTED | SUCCEEDED | FAILED | CANCELLED`. Terminal states are immutable. `WAITING` records an explicit dependency, not-before, compatible-worker, resource, or admission hold. `FINALIZING` records that the authoritative owner output exists while required job/evidence linkage is being reconciled.
3. Attempts are separate records with states `LEASED | RUNNING | COMPLETED | FAILED | TIMED_OUT | ABANDONED | CANCELLED`. Claiming creates a monotonic attempt number and fencing token in a short transaction; computation never holds database row locks.
4. Every mutable attempt, progress, owner-effect, result, and terminal command supplies the current job/attempt/fence and expected state version. Lease expiry permits another attempt, so execution is at least once; stale attempts cannot commit through ARK-owned boundaries.
5. Success is two-step. The capability/data owner idempotently commits its immutable authoritative output, then the job manager enters `FINALIZING` and links required result, lineage, audit, and usage evidence before `SUCCEEDED`. Recovery retries finalization, not completed science or data work.
6. A versioned job policy fixes handler/version, routing/resource class, priority, retry, timeout, partial-result, and concurrency scopes at admission. Policy—not the caller—assigns priority. A compatible worker must remain available for admitted handler/code versions; retries never select `latest` silently.
7. The scheduler owns schedules and deterministic occurrence identities but only submits ordinary idempotent jobs. Workers invoke one typed public handler. A conditional named workflow coordinator may submit and observe public child jobs only after a named workflow is approved. Conditional event handlers may map an approved event to the same job command only after Stage 09 approval.
8. There is no end-to-end exactly-once claim. ARK targets one logical accepted job and one logical owner effect where idempotency, immutable identity, fencing, uniqueness, and reconciliation prove it. Ambiguous external effects are reconciled, not blindly retried.
9. A broker, continuous processor, generic workflow engine, per-capability job system, or distributed transaction framework is not selected. Each requires the explicit measured triggers and dedicated decision gates in Stage 08.
10. This decision does not make Synapse production-eligible and does not infer Synapse retry, background-job, agent, event, provider, or idempotency behavior.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| In-memory/process-local jobs | Minimal initial code | Loses truth on restart; unsafe retry/cancel/status; duplicates prototype defects | Rejected | Never for accepted durable work |
| PostgreSQL jobs plus polling/leases/fencing | Uses approved authority; transactional idempotency/state; smallest operable design | Critical-table tuning, cleanup, reapers, backups, and runbooks required | Selected | Measured broker or workflow-engine trigger passes |
| External broker as job queue | Dispatch scaling and consumer isolation | Adds transport/operations and risks dual truth; no measured need | Rejected now | PostgreSQL dispatch repeatedly misses approved targets after simpler remedies, or an approved boundary needs fan-out/replay/ordering |
| General workflow engine | Durable timers/signals/graphs | Adds engine state, migration, recovery, skills, and ownership without a named complex workflow | Rejected now | Named workflow exceeds explicit PostgreSQL coordinator against approved recoverability/operability objectives |
| Per-capability job managers | Local autonomy | Duplicates lifecycle/API/retry/operations and fragments truth | Rejected | A specific module passes ADR-003 extraction gate and preserves the shared contract |
| Exactly-once execution claim | Simple consumer story | False under crashes, lease expiry, external calls, and redelivery | Rejected | No practical trigger; only bounded logical effects may be proven once |

## Rationale

PostgreSQL already owns the approved operational job truth and can atomically bind submission idempotency, state transitions, attempt leases, concurrency reservations, and result references. Separating jobs from attempts handles crash/retry reality. Separating owner output commit from terminal finalization prevents recomputation when a crash occurs after scientific/data publication but before job/evidence completion. The design is executable without preselecting deployment products or numeric capacity values.

## Consequences and trade-offs

- The job schema, transition commands, claim queries, indexes, reaper, and finalizer become critical platform code requiring fault-injection and recovery testing.
- Accepted work remains durable under backpressure; capacity policy may reject before admission but cannot drop a `202` job afterward.
- At-least-once attempts require each activated handler and external dependency to document idempotency, fencing, ambiguous-outcome, retry, timeout, partial, and cancellation behavior.
- Stable public states remain compatible with ADR-004 while internal reasons/states can evolve additively.
- Training, ingestion, and capability handlers share lifecycle mechanics but retain output/scientific ownership.
- Numeric lease, heartbeat, retry, deadline, concurrency, priority-aging, and retention values remain blocking activation inputs under `A-01-SCALE` and later operations/performance stages.
- Optional event, workflow, notification, broker, and continuous-processing mechanisms remain inactive until their owning stages and gates approve them.

## Implementation constraints

- All job and attempt transitions are job-manager compare-and-set commands; workers cannot write lifecycle tables directly.
- The current attempt ID, monotonic attempt number, opaque fence, lease expiry, and state version are checked on every mutable command and owner publication boundary.
- A heartbeat cannot extend an attempt beyond its operation/attempt bound or the overall job deadline.
- Expired leases are reconciled only by the job manager/reaper; stale workers cannot heartbeat, publish, finalize, or release another attempt's concurrency.
- `SUCCEEDED` requires authoritative owner output plus required evidence references. A valid `INELIGIBLE`, `DEGRADED`, `FALLBACK`, or dataset `NOT_READY` outcome may coexist with successful execution when its operation contract says so.
- Cancellation is cooperative and idempotent. It cannot erase an owner output that won the publication race, and it cannot claim an external effect was rolled back.
- Retry policies are immutable/versioned per admitted job; no infinite retry and no blind retry of ambiguous external effects.
- Partial output is forbidden unless the operation contract explicitly defines a useful immutable partial manifest and aggregation rule.
- Scheduler occurrence identity is `{tenant, schedule_id, schedule_version, scheduled_for}`; scheduler submits through the same job port and never executes handlers.
- Worker handler/resource compatibility is versioned. No retry or migration silently changes code, handler, data, model, feature, configuration, or policy versions.
- Large inputs, checkpoints, outputs, manifests, and evidence remain tenant-scoped opaque references.
- No broker, external queue, generic DAG/DSL, stream processor, distributed lock product, saga framework, or per-capability job service follows from this ADR.

## Validation evidence

- User approval dated 2026-08-12: “I approve Stage 08 and ADR-005 as written. Record the approval and execute only Stage 09.”
- `outputs/stages/08-execution-orchestration.md` maps every governing execution/orchestration concern and records state/attempt contracts, transition ownership, public mapping, claim/lease/reaper behavior, routing, fairness, concurrency, backpressure, retry, timeout, cancellation, partial, compensation, schedule, conditional workflow/event, and component boundaries.
- The Stage 08-authorized independent `platform_architect` review confirmed the PostgreSQL-first state authority and required the reconciled `WAITING`, `FINALIZING`, attempt-state, compatible-handler, and no-recomputation details.
- Required verification includes transition-model tests; concurrent duplicate/claim/cancel/result races; lease-loss and stale-fence injection; crash between owner commit and finalization; schedule duplicate/misfire tests; ambiguous downstream outcomes; tenant/pool starvation; handler-version compatibility; and restart/recovery tests.

## Reconsideration trigger

- PostgreSQL claim/transition load repeatedly violates an approved latency/throughput or database-isolation objective after query/index/batch/poll tuning, concurrency caps, workload separation, and same-codebase runtime-role isolation.
- An approved event boundary requires fan-out, replay retention, ordering, or independent producer/consumer operation that direct calls, jobs, or a PostgreSQL outbox cannot meet.
- A named workflow's timers, signals, human waits, graph, compensations, or recovery burden makes the explicit coordinator measurably unsafe or unmaintainable.
- An approved continuous-processing requirement passes the Stage 06/08 event-time, replay, checkpoint, state, recovery, ownership, and operating-burden gate.
- A specific module passes ADR-003's service-extraction gate.

## Supersedes / superseded by

This ADR refines the durable-job portion of accepted ADR-003 and the internal job details intentionally deferred by accepted ADR-004. It does not supersede ADR-000 through ADR-004. Superseded by: none.
