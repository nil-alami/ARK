# Stage 13 — Reliability and failure design

**Status:** APPROVED  
**Completed:** 2026-08-12  
**Stage owner:** Primary architecture agent  
**Authorized specialist:** `assurance_reviewer` (read-only failure challenge)

## Purpose and scope

Define truthful failure, containment, retry, recovery, reconciliation, stale-data, partial-result, poison-input, and disaster-recovery behavior for every approved ARK critical path. This stage applies the reliability concerns in `sources/normalized/system-design-prompt.md — 12. Reliability and failure design` to the actual Stage 05–12 contracts.

This stage does not select a database, object-store, identity, secrets, queue, cache, model-serving, backup, or disaster-recovery product. It does not invent latency, retry, retention, recovery-point, recovery-time, availability, backlog, or capacity values. It does not clear any capability, security, provider, delivery, ownership, or production-admission block. It does not activate a webhook, broker, named workflow, Synapse interface, model profile, proactive external action, or agent. Stage 14 is not executed.

## Inputs read in full

- `WORKFLOW.md`
- `STATUS.md`
- `SOURCE_MANIFEST.md`
- `stages/STAGE-CONTRACT.md`
- `stages/13-reliability.md`
- `templates/stage-output.md`
- `sources/normalized/system-design-prompt.md` — especially **12. Reliability and failure design**
- Approved `outputs/stages/05-end-to-end-architecture.md`
- Approved `outputs/stages/06-data-architecture.md`
- Approved `outputs/stages/07-api-integration.md`
- Approved `outputs/stages/08-execution-orchestration.md`
- Approved `outputs/stages/09-events-proactive-actions.md`
- Approved `outputs/stages/10-mlops.md`
- Approved `outputs/stages/11-agent-architecture.md`
- Approved `outputs/stages/12-security-governance.md`
- Accepted `decisions/ADR-004-api-contract-boundary.md`
- Accepted `decisions/ADR-005-postgresql-job-state-machine.md`
- Accepted `decisions/ADR-006-governed-proactive-action-and-delivery.md`
- Accepted `decisions/ADR-007-versioned-ml-lifecycle-and-production-admission.md`
- Accepted `decisions/ADR-008-zero-trust-tenant-and-governance-boundary.md`

## Specialist reconciliation

The Stage 13-authorized `assurance_reviewer` performed a bounded, read-only adversarial challenge of the failure categories, actual ARK critical paths, containment and retry boundaries, user-visible truth, consistency effects, recovery roles, verification steps, partial/stale semantics, poison handling, replay, disaster recovery, and production-admission preservation. Its initial review identified the Phase A/Phase B ordering defect plus three contract clarifications. The primary agent corrected the proactive order, public partial-result state, recovery-epoch treatment, and scheduling-policy wording. The final reviewer pass reported no critical or high defect and recommended `PASS`. The primary agent remains the sole authoritative writer.

## Source-instruction coverage

| Governing concern | Stage 13 disposition |
|---|---|
| Unavailable dependencies | Fail-closed or explicitly degraded by dependency class; no fabricated success |
| Invalid or incomplete datasets | Raw evidence retained; candidate quarantined; no ready publication or model execution |
| Queue backlog | Admission/backpressure and truthful waiting/age; no silent dropping or unbounded retry |
| Worker crash | Lease expiry, stale-fence rejection, safe reclaim or reconciliation |
| Duplicate execution | Stable logical identity, idempotency, fencing, uniqueness, and result/effect reconciliation |
| Partial workflow completion | Default `FORBID_PARTIAL`; explicit immutable partial manifest only under an approved operation contract |
| Stale cache | Cache is never authority; tenant/purpose/assignment-aware keys and authoritative revalidation |
| Storage outage | No false acceptance/readiness/success; pause, preserve committed truth, then reconcile |
| Model unavailable | Exact approved assignment only; previous/fallback only if explicitly approved and compatible; otherwise unavailable |
| Event delivery failure | Result/source fact remains authoritative; delivery retries independently, then dead-letters |
| Tenant misconfiguration | Fail closed before effect; no default tenant, entitlement, grant, destination, secret, or model |
| Poisonous messages | Quarantine/dead-letter after classification; no blind retry loop; authorized replay only after correction |
| Schema incompatibility | Reject/quarantine unsupported version; coexistence or explicit migration, never guessed interpretation |
| Agent loops or unsafe actions | No agent is currently justified or selected; deterministic proactive effects retain Stage 09 gates; future agents must re-enter Stage 11 |
| Timeout, retry, circuit breaker, idempotency, dead-letter, degradation, fallback, recovery, reconciliation, DR | Applied only to the paths where each pattern has a demonstrated purpose; no universal product or policy invented |

## Confirmed facts

1. ARK has three approved foundational critical paths: synchronous eligible operation, durable asynchronous operation, and source-to-ready-dataset publication. Proactive evaluation/action and conditional delivery extend those paths but do not replace their authorities. `outputs/stages/05-end-to-end-architecture.md — Consumer-to-result flow: synchronous eligible operation`, `— Consumer-to-result flow: durable asynchronous operation`, `— Source-to-ready-dataset flow`; `outputs/stages/09-events-proactive-actions.md — Two-phase fail-closed decision order`.
2. PostgreSQL is the authoritative logical store for jobs, attempts, leases, idempotency, schedules, control state, and bounded metadata. At-least-once attempts become logically-once effects through immutable admission, fences, unique identities, and reconciliation. `outputs/stages/08-execution-orchestration.md — Authoritative job and attempt state machines`; accepted ADR-005.
3. Large raw, curated, feature, result, artifact, and evidence bytes use immutable object references. A candidate object is not authoritative until its owner commits the matching catalog/result/registry reference. `outputs/stages/06-data-architecture.md — Zone and authoritative-writer matrix`; `— Concrete data lifecycle — transaction file to recommendation result`.
4. Public polling is authoritative for asynchronous recovery. Delivery state is separate from job, result, insight, action, and source-fact truth. `outputs/stages/07-api-integration.md — Job contract`; `outputs/stages/09-events-proactive-actions.md — External delivery contract`.
5. Capability execution binds exact dataset, feature, configuration, code/handler, artifact/model, and policy identities. Retry, replay, rollback, or restoration cannot silently select `latest` or change scientific meaning. `outputs/stages/10-mlops.md — Independent identity and evidence graph`; accepted ADR-007.
6. Mandatory identity, authorization, policy, secret/key access, and audit evidence fail closed. Diagnostic telemetry is not authoritative audit and cannot be used to backfill an action that occurred without mandatory audit. `outputs/stages/12-security-governance.md — Security invariants`; `— Audit, privileged operations, and governance separation`; accepted ADR-008.
7. Churn, RFM, NPT, and REC remain `MIGRATION_BLOCKED`; all three Synapse interfaces remain `EVIDENCE_BLOCKED`; all eight ADR-008 security-admission blocks remain active. Reliability design cannot turn a blocked capability into an available fallback. Accepted ADR-007; accepted ADR-008.
8. No production agent is justified or selected from admitted evidence. Agent-loop handling is therefore not an active runtime path. Any future adaptive agent must pass the Stage 11 re-entry gate and remain subordinate to Stage 08/09/10/12 authority. `outputs/stages/11-agent-architecture.md — Future agent re-entry gate`.

## Temporary assumptions

| ID | Temporary assumption | Reliability effect | Expiry / evidence required |
|---|---|---|---|
| `A-01-SCALE` | Traffic, duration, backlog, concurrency, latency, and availability targets remain unknown | Contracts require per-operation deadlines, retry ceilings, admission/backpressure, and capacity alarms without assigning values | Measured S-01 through S-04; Stage 17 |
| `A-01-OPS` | Deployment, support, recovery, and environment are unknown | Logical restore/reconcile order is defined; topology, RPO/RTO and failover mechanism are not | OPS-01 through OPS-05; Stages 15/17/20 |
| `A-04-OWNERSHIP` | Named accountable and on-call people are unknown | Every matrix names a logical owner role; production remains blocked until roster/runbook/escalation are approved | Stage 20 and production readiness |
| `A-07-INTEGRATION` | Polling remains universal; webhook and internal event paths remain conditional | Delivery recovery is specified but cannot be activated without consumer/security/SLO policy | Approved consumer contract and ADR-008 admission evidence |

These are inherited temporary assumptions. Stage 13 neither extends an expired assumption nor creates a new production entitlement.

## Reliability invariants

1. **Truth before availability.** An unavailable dependency yields an explicit unavailable, not-ready, ineligible, waiting, failed, or delivery-degraded outcome; it never yields fabricated success.
2. **Committed owner state is the recovery anchor.** HTTP responses, worker memory, queue visibility, caches, logs, metrics, and notification acknowledgements are observations—not authority.
3. **Retry preserves meaning.** A retry retains tenant, purpose, operation, logical request/job/effect, admitted input and dataset versions, handler/code, model assignment, policy, and authorization scope. If meaning must change, create a new authorized command/version.
4. **Ambiguity is reconciled before repetition.** After timeout or crash at an external or irreversible effect boundary, inspect the stable effect identity and provider/owner evidence. Never blindly retry an effect whose outcome is unknown.
5. **Stale attempts cannot act.** Every attempt-scoped commit or effect checks the current job state/version, attempt, lease/fence, tenant, cancellation/deadline, and time-sensitive authority.
6. **Partial is never implicit success.** The default is `FORBID_PARTIAL`. An explicitly supported partial result has a typed manifest of completed, failed, omitted, and unknown partitions plus exact input/version lineage and a degraded outcome label.
7. **Cache loss is a miss; cache staleness is not authority.** Cache entries use accepted ADR-008 tenant/capability/purpose/assignment-aware identity. Revocation, policy, readiness, grants, and current authority are revalidated at their required owner boundary.
8. **Recovery does not weaken security.** Break-glass, replay, restore, reconciliation, retry override, or fallback cannot bypass identity, tenant isolation, policy, separation of duties, audit, exact assignment, or production-admission blocks.
9. **Poison is isolated, not amplified.** Deterministic validation/schema failures are quarantined or dead-lettered with bounded diagnostic evidence; automated retries stop. Replay requires an authorized correction and preserves provenance.
10. **Numeric policy is mandatory before activation.** Every active operation must have approved deadlines, attempt ceiling, backoff/jitter, lease/heartbeat, idempotency/replay retention, backlog/admission, partial/fallback, and escalation policy. Missing values block activation; this stage does not invent them.

### Authoritative commit and finalization contract

- A capability or data owner first writes any large immutable candidate object. The object is non-authoritative until a unique owner result, dataset, or artifact record commits its digest, exact admitted identities, and logical result identity.
- Mandatory pre-effect audit admission/intent must succeed before sensitive computation, mutation, external action, or privileged operation begins. The owner commit records a stable required-audit/evidence identity and finalization obligation; it does not pretend that two independent owners share an atomic transaction.
- Public success is not exposed until the owner result and all success-critical lineage, usage/reservation, and mandatory completion-audit obligations have been verified. A result committed before that verification remains held in `FINALIZING`/non-published owner state.
- A finalizer looks up output by unique `{tenant_id, job_id, logical_result_id}` and validates digest, admitted input/dataset/handler/model/policy identities, the committing attempt's valid fence at commit time, and required evidence references. In ordinary operation the current attempt/fence/recovery epoch must match. After restore, a reconciler running under the new recovery epoch may finalize an exact owner output proven committed at or before the accepted recovery point; the new epoch still rejects every stale worker or new effect from a pre-restore attempt. An exact match is linked and finalized idempotently. A conflicting output is never overwritten or selected; it becomes an administrative reconciliation incident. A missing output may be recomputed only when the declared operation/effect contract proves that safe; otherwise the job fails or remains held for reconciliation.
- If the response is lost after finalization, the same idempotency key returns the already finalized outcome. If audit/evidence completion remains unavailable, retries target the missing evidence obligation by its stable identity and do not rerun the computation or external effect.

## Failure classification and pattern policy

| Class | Examples | Automated retry | Containment and terminal behavior |
|---|---|---|---|
| Transient, side-effect-free | bounded dependency timeout before owner commit, temporary object read error | Yes, only under admitted policy, deadline, backoff/jitter, and current authority | Remain waiting/retryable; exhaust to explicit dependency failure |
| Transaction conflict with known no-effect | compare-and-set conflict, serialization failure whose transaction did not commit | Re-read owner state and retry boundedly | Never replay a transaction body without revalidating state and fence |
| Permanent input/contract | malformed payload, unknown schema, checksum mismatch, invalid dataset semantics | No automated retry of same bytes/version | Reject or quarantine; require corrected input/new version |
| Scientific or policy ineligibility | not-ready dataset, missing required feature, revoked grant, unavailable approved model | No retry loop | Explicit ineligible/unavailable/suppressed outcome; new evidence or authority required |
| Ambiguous effect | webhook timeout, provider call timeout after send, connection loss during external mutation | No blind retry | Reconcile by stable effect/idempotency identity; retry only if evidence proves no effect or receiver contract deduplicates |
| Worker/process loss | heartbeat/lease expiry, restart during computation | Safe reclaim only if current fence and effect contract allow it | Old attempt becomes abandoned/timed out; stale writes rejected |
| Shared authoritative dependency outage | PostgreSQL, mandatory audit, identity/policy/secrets | No bypass/fallback to stale authority | Stop admission/effects, preserve committed truth, health-gate/fail fast, recover and reconcile |
| Delivery/publication poison | unsupported event version, repeated deterministic handler failure | Bounded attempts then dead-letter | Source fact/result unchanged; alert logical owner; authorized corrected replay only |

### Timeouts, retries, and circuit behavior

- Every network/dependency call and operation has a caller deadline no later than its enclosing request/job deadline. Cancellation propagation is bounded by declared safe points; timeout does not prove rollback.
- Immediate synchronous work has no silent background continuation. Deadline expiry returns an explicit timeout/unknown-commit status appropriate to the boundary; an idempotent client retry uses the same key.
- Durable retries are scheduled state transitions, never tight worker loops. Policy includes eligible failure classes, maximum attempts, deadline, backoff/jitter, and escalation/dead-letter or terminal outcome.
- A circuit/health gate is justified only for a repeatedly failing remote or optional dependency where fast rejection protects shared resources. Opening it changes the outcome to explicit dependency-unavailable; it never substitutes stale identity, policy, audit, secret, dataset, model, or result data.
- PostgreSQL job truth is not hidden behind a circuit that fabricates acceptance. If its owner transaction cannot commit, the command is not accepted.

### Idempotency, reconciliation, and replay boundary

- API: `{principal tenant, operation, idempotency key}` plus canonical request hash identifies one logical command. Same key/hash replays the recorded result; same key/different hash conflicts.
- Job: one immutable admitted job and operation version; attempts differ, but fences and unique result/effect identities prevent stale or duplicate commit.
- Object publication: immutable object/checksum plus candidate identity may be retried; catalog/result/registry publication is a conditional idempotent owner commit.
- Schedule: one `{schedule version, occurrence}` may create at most one logical job.
- Event/handler: one `{event_id, handler_version}` logical handling outcome; a replay generation is delivery work, not a new source fact.
- External delivery/effect: stable logical event/effect identity and receiver idempotency are required. Transport timeout is `AMBIGUOUS` until reconciliation; it is not evidence of failure.
- Administrative replay requires permission, reason, immutable original reference, compatible schema/handler, current tenant/policy scope, mandatory audit availability, and a recorded new attempt/generation. Replay never changes the original occurred time or silently reauthorizes old work.

## Critical-path failure matrices

The `Recovery owner` column names the authoritative logical role. Under `A-04-OWNERSHIP`, each role still needs an approved named accountable/on-call roster before production.

### CP-13-01 — Synchronous authenticated capability request

Path: adapter/edge → identity/tenant/control → versioned capability operation → readiness/scientific eligibility → exact execution bundle → result/audit commit → response.

| Failure | Detection | Containment | User-visible status | Retry boundary | Consistency effect | Recovery owner | Verification step |
|---|---|---|---|---|---|---|---|
| Identity, entitlement, policy, quota, secret, or mandatory audit unavailable/misconfigured | Validator/owner lookup or pre-effect audit fails; version missing/revoked | Fail before execution/effect; no default or cached authority | Authentication/authorization/control/dependency unavailable, with concealed detail as required | Client may retry same idempotent request after dependency health; no bypass | No result/effect commit; reservation reconciled if already created | Identity/control/security owner | Fault-inject each dependency; prove zero capability/effect records and complete denial audit where available |
| Invalid request, unsupported schema/version, or tenant/resource mismatch | Edge and owner structural/resource checks | Reject before state change; rate-limit repeated poison | Stable validation/version/not-found-or-denied error | Corrected request is new hash/key; same poison not auto-retried | No business mutation | API/capability owner | Contract, IDOR, body-tenant and unknown-version negative tests |
| Readiness stale/revoked, model unavailable, or bundle load/integrity failure | Catalog/assignment/revocation/digest/compatibility check | No model execution; invalidate relevant local entry; preserve approved healthy assignment only if still exact and valid | `NOT_READY`, `INELIGIBLE`, or explicit capability unavailable/degraded policy outcome | New dataset/assignment or same request after recovery; never select `latest` | No fabricated result; existing immutable results unchanged | Dataset or capability/model owner | Revoke/corrupt/remove artifact and prove no stale/alternate selection |
| Execution exceeds deadline or process fails before commit | Enclosing deadline/process health; no owner result exists | Stop at safe point; no background continuation | Timeout/failed; if commit boundary ambiguous, status points to idempotency reconciliation | Same key; owner idempotency record determines replay/conflict | At most one logical result; unreferenced candidates cleaned later | Capability owner | Kill/timeout before, during, after candidate creation and at result transaction boundary |
| Result/lineage/usage/audit finalization fails or response is lost | Owner result identity, finalization obligation and later idempotency lookup | Hold committed result from public success until required evidence finalizes; retry missing obligation, not computation; delivery is not authority | `FINALIZING`/dependency failure if incomplete; replayed success if finalized and response lost | Same key and stable evidence IDs only | No false success, duplicate result/usage, or assumed cross-owner atomicity | Capability/audit/metering owners | Drop connections before/after candidate, result, audit/evidence and response; prove one result and exact finalization obligations |

### CP-13-02 — Durable job, schedule, batch, training, backfill, or long inference

Path: idempotent submit/occurrence → PostgreSQL job → admission/waiting/ready → leased fenced attempt → checkpoint/compute → owner result → finalization → polling/delivery.

| Failure | Detection | Containment | User-visible status | Retry boundary | Consistency effect | Recovery owner | Verification step |
|---|---|---|---|---|---|---|---|
| PostgreSQL unavailable at submission/claim/transition | Transaction failure/health probe; no durable acknowledgement | Do not accept new command; stop claims/transitions; running attempts cannot commit without fence check | Request not accepted/dependency unavailable; committed jobs retain last truthful public state | Submit with same key after recovery; workers reacquire, never infer state from memory | Committed job truth preserved; uncertain worker computation has no authority | Job-platform/database owner | Outage at submit, claim, heartbeat, finalize; restore and prove no lost/duplicate logical job/effect |
| Queue backlog, dependency wait, or admission saturation | Queue age/depth, oldest-ready age, configured pool/tenant limits, deadline risk | Backpressure/reject new work per approved policy; configured tenant/pool concurrency and fairness; no unbounded concurrency or selected weighting algorithm | `ACCEPTED`/waiting with reason and age; explicit capacity/deadline failure when policy requires | Scheduler releases only when eligible; not a worker retry storm | No data mutation until attempt; occurrence/idempotency remains one | Job-platform owner | Load/backlog test proves bounded admission, configured isolation/fairness, deadline and no starvation under approved policy |
| Worker crash, lease loss, heartbeat loss, or stale attempt | Lease expiry/fence mismatch/process signal | Mark prior attempt abandoned/timed out; reclaim only with new attempt/fence; reject stale effects | Job remains running/retry-wait or terminal failure per policy | New attempt with same admitted job versions; side effects reconcile first | At most one owner commit; stale candidate remains unreferenced | Job-platform + capability owner | Kill worker at safe points; delay old worker; prove fence rejects its checkpoint/result/effect |
| Duplicate submit/occurrence/attempt | Unique idempotency/occurrence/effect constraint or fence conflict | Return existing job; discard/reconcile duplicate attempt | Same job reference/status | No new logical work for same identity | One job/result/effect; attempts remain auditable | Job-platform owner | Concurrent duplicate and same-key/different-hash tests |
| Handler/schema/version incompatible or poison job | Worker compatibility/admission check; repeat deterministic failure signature | Do not execute guessed handler; isolate queue item; terminal fail/dead-letter operational record after bounded classification | Explicit incompatible/invalid job failure | Deploy compatible handler and authorized replay/new job; no endless retry | Original admitted job immutable; no partial effect | Job-platform + operation owner | Submit unsupported handler/version; prove other jobs progress and poison does not loop |
| Cancellation/deadline races finalization | CAS on state/version, current fence/recovery epoch, cancellation/deadline check at safe point | `FINALIZING` reconciles the unique owner output and evidence obligations; no claim that external effects were undone | `CANCELLATION_REQUESTED`, then truthful succeeded/failed/cancelled outcome | Retry only missing finalization obligation or per terminal/ambiguous policy; cancellation is not replay | Owner result/effect and terminal state reconcile to one outcome; conflicting output is held for administration | Job-platform + result/effect owner | Race cancel/timeout with object/result/evidence commit; crash finalizer; prove discovery of exact committed output and conflict rejection |
| Partial partition failure | Partition manifest and declared operation partial policy | Default fail whole logical result; if approved, publish immutable partial manifest with omissions/failures | Public job `FAILED` when partial is forbidden; when explicitly accepted, public job `SUCCEEDED` with separate capability outcome `DEGRADED` and immutable partial manifest | Retry failed partitions only when deterministic identity and policy define merge; otherwise new job | Never mix versions; completed child/partition outputs immutable and referenced explicitly | Capability owner | Inject one partition failure and verify public state, domain outcome, manifest, lineage, aggregation, and no duplicate outputs |

### CP-13-03 — Source ingestion to ready dataset publication

Path: source registration/upload → immutable raw → structural validation → semantic/policy/quality evaluation → immutable candidate → atomic catalog/readiness/lineage publication.

| Failure | Detection | Containment | User-visible status | Retry boundary | Consistency effect | Recovery owner | Verification step |
|---|---|---|---|---|---|---|---|
| Upload/object-store unavailable, truncated, or checksum mismatch | Storage error, length/checksum/media validation | Do not acknowledge complete registration or advance validation; retain verifiable raw only | Upload/ingestion failed or pending; no ready dataset | Retry immutable object transfer by upload/run identity; corrected bytes require new checksum/version | No candidate/catalog publication; partial multipart remains unreferenced cleanup work | Ingestion/object-storage owner | Interrupt multipart writes, corrupt bytes, repeat upload; prove checksum and one logical registration |
| Unknown/incompatible source schema or invalid/incomplete records | Structural validation, declared compatibility, required partition/field checks | Quarantine raw/report; no semantic or ready publication | Explicit structural failure with bounded reason report | Same bytes not auto-retried; corrected source contract/input is new version/run | Raw evidence preserved; ready pointer unchanged | Source-contract/ingestion owner | Unknown version, missing partition, parse/type/bounds and decompression fault tests |
| Semantic, policy, freshness, quality, cursor, sequence, duplicate, or correction ambiguity | Domain/policy/quality checks and cursor reconciliation | Quarantine/reject or mark not-ready/stale; never last-write-wins ambiguity | Explicit semantic/policy/quality/stale/reconciliation status | Retry only after authoritative mapping/policy/source correction; duplicates map to existing logical input | No new ready version; prior immutable ready version remains separately identifiable and only usable if still policy-valid | Canonical/data-governance owner | Late/correction/duplicate/gap/regression/revocation scenarios prove no silent truth change |
| Candidate write succeeds but catalog/readiness commit fails | Missing catalog reference or failed owner transaction; orphan scan | Candidate stays unreferenced/invisible to consumers | Ingestion not ready/failed; candidate is not success | Idempotent publication after object integrity and policy recheck; otherwise cleanup | Atomic metadata authority prevents partial publication | Dataset-catalog owner | Crash after candidate write and before/during catalog commit; prove no discoverable ready dataset |
| Catalog unavailable or readiness evidence stale | Query failure/version/expiry/revocation check | Capability admission fails closed; no cached ready assertion substitutes | `NOT_READY`/data dependency unavailable | Retry after authoritative recovery; new readiness decision if versions changed | No execution against unverifiable dataset | Dataset-catalog owner | Outage/revocation while submitting and before result commit; prove recheck and no use of stale readiness |
| Reprocessing/backfill partially completes | Job/partition manifest and publication state | No overwrite of earlier version; default no ready publication until complete | Failed or explicit partial candidate—not a ready dataset | Resume only exact run/partition identities or create new reprocessing run | Version graph/impact manifest preserves old and candidate states | Data-platform/capability owner | Kill multi-part backfill; verify manifests, no mixed version, deterministic resume/cleanup |

### CP-13-04 — Model/artifact training, registration, assignment, loading, inference, and rollback

| Failure | Detection | Containment | User-visible status | Retry boundary | Consistency effect | Recovery owner | Verification step |
|---|---|---|---|---|---|---|---|
| Training/evaluation input invalid, incomplete, leaked, or incompatible | Dataset/readiness/PIT/schema/label/evaluation gates | No candidate promotion/assignment; quarantine evidence | Training/evaluation failed or ineligible | New corrected run; attempt retry only transient and version-preserving | No change to active assignment | Capability scientific owner | PIT/leakage/missing-partition/schema fault suite proves no promotion |
| Artifact/registry write unavailable, corrupt, or provenance incomplete | Digest/signature/provenance/registry transaction | Candidate unreferenced/unselectable; training job cannot finalize success | Training/registration failed | Retry exact immutable registration after integrity check | Active assignment unchanged; orphan artifact tracked | Registry + capability owner | Corrupt/truncate artifact and fail registry commit at each boundary |
| Promotion/assignment authority, audit, compatibility, or ownership missing | Promotion gate and ADR-008 privileged-action checks | Reject assignment mutation; no automatic promotion | Operation blocked/denied | New authorized decision after evidence; never worker retry | Prior assignment remains exact and auditable | Release/model-governance owner | Negative role/separation/audit/compatibility and concurrent CAS tests |
| Active artifact unavailable, revoked, cache-corrupt, or load fails | Exact assignment/digest/revocation/runtime compatibility/load health | Evict invalid cache entry; use prior/fallback only when explicitly approved, exact, compatible, and policy-valid; otherwise unavailable | Capability unavailable or approved named degraded outcome | Bounded reload same assignment; rollback is a new authorized assignment; no alternate search | Historical results retain original bundle; no silent model change | Capability/model-serving owner | Delete/revoke/corrupt/cache-collide and prove tenant/purpose/assignment isolation and exact selection |
| Inference provider/model timeout or ambiguous external effect | Adapter deadline/idempotency/provider evidence | Synapse remains blocked; any future provider path reconciles before retry and cannot act externally | Explicit unavailable/ambiguous/degraded only under approved profile | Provider-specific idempotent retry policy after admission; no current Synapse retry | No fabricated response, action, or usage; metering reconciles by stable call identity | Capability/provider owner | Future activation suite: timeout before/after send, duplicate, provider error, malformed output, cost reconciliation |
| Rollback/restore creates version mismatch | Assignment compatibility and reproduction manifest checks | Do not activate or serve incompatible bundle | Assignment/operation unavailable | Select only explicitly approved compatible assignment through governed command | No rewrite of past predictions; corrected output is new execution/version | Release + capability owner | Restore old registry/catalog snapshot and prove compatibility/revocation blocks stale assignment |

### CP-13-05 — Scheduled proactive evaluation and governed internal action

Path: schedule occurrence/trigger → Phase A evaluation-admission checks and mandatory audit → evaluation job → immutable insight → Phase B post-insight action/delivery checks, reservation, decision, mandatory audit, and typed intent → idempotent task/delivery submission → execution/delivery-time recheck → bounded effect.

| Failure | Detection | Containment | User-visible status | Retry boundary | Consistency effect | Recovery owner | Verification step |
|---|---|---|---|---|---|---|---|
| Duplicate/missed/delayed schedule occurrence or Phase A admission failure | Deterministic occurrence identity, scheduler lag/reconciliation, then authenticated provenance, entitlement/subscription, standing authorization, dataset readiness/freshness, evaluation quota/runtime, cooldown/dedupe, and mandatory admission-audit checks | Deduplicate; catch up only within approved freshness/expiry policy; fail/defer/suppress before job submission; an expired occurrence is recorded and never executed late | Scheduled evaluation delayed, missed, expired, deferred, suppressed, or one job reference | Reconcile occurrences, then Phase A may submit the same occurrence identity only while all current admission checks pass | At most one logical evaluation per schedule version/occurrence; no evaluation job before Phase A completes | Scheduler/control/audit owner | Clock/restart/concurrent scheduler, expired catch-up, stale grant/readiness, quota and audit-outage tests prove no unauthorized job |
| Evaluation job fails or produces missing/ineligible insight | Stage 08 outcome plus exact admitted dataset/model/handler and scientific outcome | No Phase B decision, intent, task, or delivery from missing/ineligible result | Evaluation failed/not-ready/ineligible | New evaluation after evidence; delivery/task retry never reruns evaluation | Any committed insight is immutable evidence; no action identity exists | Capability/proactive owner | Crash/fail evaluation and remove required evidence; prove no Phase B resource |
| Phase B authorization, freshness, threshold, policy, action quota/reservation, cooldown/dedupe, destination, or mandatory audit unavailable/races | Post-insight exact-version checks and transactional decision/reservation/audit/intent commit; version/CAS mismatch | `REPORT_ONLY`, suppress, defer, or fail closed; release/reconcile action reservations; no typed task/delivery intent on incomplete decision | Report-only/suppressed/deferred/control unavailable | Retry Phase B with same decision identity only while current authority permits; never treat Phase A as action authority | No double action reservation/consumption/task/delivery; immutable insight remains | Proactive-control/integration/audit owners | Revoke grant/data/model between evaluation and Phase B; race duplicate/quota/destination/audit failures; prove no unauthorized intent |
| Intent handler/worker crash or revocation between accepted task/delivery and effect | Idempotent intent identity, Stage 08 fence, and execution/delivery-time recheck | Reject stale attempt; cancel future work; do not claim external rollback | Cancelled/suppressed/failed or truthful completed/ambiguous effect | New attempt only when task/effect idempotent and authority still current; ambiguous effect reconciles | One task/delivery/effect identity; audit records race/outcome | Task/effect or delivery owner | Kill/revoke after Phase B at intent, submission and effect boundaries; prove no policy bypass or duplicate effect |
| Unsafe LLM/verifier output or hypothetical agent behavior | Typed validation and authority separation; no agent selected | Treat output as advisory/untrusted; deterministic policy remains outside | No action/suppressed or capability unavailable | No autonomous loop/retry | No LLM output becomes grant, task, promotion, or delivery authority | Capability/security owner | Malicious/accepted verifier output and injection tests prove zero direct effect |

### CP-13-06 — Conditional internal publication and external notification delivery

This path remains inactive until its ADR-006/008 activation gates pass. The matrix is the required pre-activation reliability contract, not evidence that webhook or broker infrastructure exists.

| Failure | Detection | Containment | User-visible status | Retry boundary | Consistency effect | Recovery owner | Verification step |
|---|---|---|---|---|---|---|---|
| Crash between source fact/decision and publication intent | Transactional outbox/notification-intent invariant and reconciliation scan | For an activated promise, commit source decision and intent without crash gap; otherwise no delivery claim | Source result remains available; delivery pending | Publisher retries intent, never recomputes source fact | Source fact/action/result remains single authority | Producer + publication owner | Crash at every transaction edge; prove no committed promised fact lacks intent |
| Publisher/handler crash or duplicate delivery | Lease/fence, `{event_id, handler_version}` dedupe, delivery identity | Reclaim safely; consumer applies typed idempotent command only | Pending/retrying; result unaffected | Bounded attempt policy; no new event ID | At least once transport, one logical handler/effect | Publication/consumer owner | Kill publisher/handler and duplicate messages; prove one logical outcome |
| Unsupported schema or poison payload/handler | Schema registry/declared range and deterministic failure classification | Quarantine/dead-letter per consumer; keep unrelated deliveries moving | Dead-letter/incompatible with reason; source result unchanged | Correct handler/schema then authorized replay generation | Original event immutable; no guessed interpretation | Event-schema + consumer owner | Unknown/malformed version and poison ordering tests; verify isolation and lag visibility |
| Endpoint unavailable, rate-limits, or circuit opens | Delivery timeout/response class/endpoint health | Bounded backoff/jitter and destination-specific circuit; polling remains authoritative | Pending/retrying/dead-letter/expired | Same event/delivery identity; respect receiver retry guidance only within policy | No capability rerun or action reauthorization | Integration/delivery owner | Timeout/429/5xx/outage tests prove bounded retries and no upstream duplicate work |
| Webhook acknowledgement ambiguous | Timeout/connection loss after send | Mark ambiguous; query receiver if contract permits or retry only with receiver dedupe | Ambiguous/retrying; polling exposes authoritative result | Stable `event_id`; never invent new logical notification | Downstream may have received; ARK audit preserves uncertainty until reconciled | Integration + consumer owner | Drop acknowledgement after receiver commit; prove dedupe and truthful ambiguity |
| Destination revoked/misconfigured, secret unavailable, SSRF/policy failure | Phase B/at-send destination, secret, policy, expiry, and egress checks | Disable/suppress; never send to caller-supplied/default destination | Delivery blocked/suppressed/dead-letter; result remains available | New registration/secret/authority required; replay rechecks all controls | No external disclosure/effect | Integration/security owner | Rotate/revoke destination/secret during retry and verify zero wrong-target delivery |

### CP-13-07 — Privileged administration, recovery, replay, promotion, and configuration

| Failure | Detection | Containment | User-visible status | Retry boundary | Consistency effect | Recovery owner | Verification step |
|---|---|---|---|---|---|---|---|
| Identity/step-up/role/separation/audit unavailable | ADR-008 privileged-operation preconditions | Fail closed; no local emergency default | Operation denied/blocked | New authenticated command after recovery | No privileged mutation | Security/control owner | Outage and role-combination negative tests prove zero state change |
| Concurrent or stale configuration/grant/assignment mutation | ETag/version/CAS conflict and audit old/new refs | Reject stale write; re-read current owner state | Conflict with current version | Human/automation resubmits an explicit revised command | One ordered owner history; no lost update | Owning control/release role | Concurrent mutation/race fault test |
| Administrative retry/replay after response loss | Stable command/idempotency identity and audit lookup | Return prior committed outcome or conflict; never repeat by guess | Prior outcome or explicit unknown pending reconciliation | Same key only; different intent is a new command | At most one privileged logical effect | Owning admin interface | Drop response at commit and prove one mutation/audit entry |
| Recovery tool or operator proposes unsafe scope expansion | Authorization, tenant/resource scope, dry-run/impact manifest, mandatory approval/audit | Reject or constrain to exact named objects/jobs/events/versions; no wildcard tenant recovery | Denied or bounded recovery plan | Corrected approved plan is new command | No cross-tenant or untracked mutation | Security + affected owner | Cross-tenant, broad selector, stale snapshot, revoked authority tests |
| Retention/deletion partially applies or storage/backup copy is unavailable | Per-item deletion manifest covers rows, objects, indexes/caches, backups and governed model derivatives with policy/legal-hold refs | Continue only safe exact-item operations; mark held/exempt/failed items; never report aggregate completion early | Deletion pending/partially failed/held/exempt with bounded manifest | Retry same item/effect identity after dependency recovery; policy change is a new authorized command | Deleted items are not recreated by retry/restore; remaining copies stay explicit and access-restricted | Data-governance + each storage owner | Fail each storage class, apply legal hold, restore an older backup; prove manifest truth and no silent resurrection/access |

### CP-13-08 — Conditional named multi-capability workflow

No named workflow is active. If one is approved later, it is a deterministic immutable graph over typed Stage 08 child jobs, not a general agent.

| Failure | Detection | Containment | User-visible status | Retry boundary | Consistency effect | Recovery owner | Verification step |
|---|---|---|---|---|---|---|---|
| Child fails/times out/cancels or dependency never becomes ready | Parent observes authoritative child/dependency states and deadline | Apply declared fail-fast, continue, compensate, or wait policy; default fail, not implied partial | Parent waiting/failed/cancellation-requested or explicit partial manifest | Retry child only through its own idempotent job contract; parent transition restartable | Child results remain authoritative; parent never rewrites them | Workflow + child owner | Fault each graph edge/state and restart coordinator; compare parent/child lineage |
| Coordinator crashes or duplicates transition | Durable parent state/version/CAS and deterministic next-step identity | Reclaim; duplicate transition creates no duplicate child | Parent retains last truthful state | Resume from committed graph state | At most one child per node/iteration identity | Workflow/job-platform owner | Kill before/after child submit and parent transition; prove one graph |
| Compensation unavailable or effect ambiguous | Typed compensation/effect status and reconciliation | Stop and expose residual effects; never claim atomic rollback | Failed with compensation/residual-effect manifest | Reconcile original effect first; bounded compensation command only if authorized/idempotent | Completed external/child effects remain explicit | Workflow + effect owner | Fail compensation and lose acknowledgement; prove residual truth and no blind repeat |
| Workflow definition/child schema incompatible | Immutable workflow/child contract compatibility check | Do not start or advance incompatible node | Incompatible/blocked | New approved workflow version/migration | Running workflow retains admitted definition | Workflow owner | Deploy incompatible child handler during run; prove no silent upgrade |

## Cross-cutting failure-category coverage

| Required source failure | Primary paths | Required disposition |
|---|---|---|
| Unavailable dependencies | CP-01–07 | Fail closed for authority/commit; bounded explicit degradation only under approved operation policy |
| Invalid/incomplete datasets | CP-03/04/05 | Quarantine/not-ready; no training/inference/action |
| Queue backlog | CP-02/05/06/08 | Admission/backpressure, tenant/pool isolation, age/deadline truth, measured escalation |
| Worker crash | CP-02/05/06/08 | Lease expiry, new fence, reconcile effects, stale-attempt rejection |
| Duplicate execution | CP-01–08 | Stable logical identities, uniqueness, idempotency, fencing, no semantic version drift |
| Partial workflow completion | CP-02/03/08 | Default failure; explicit typed manifest only when approved; completed child truth preserved |
| Stale cache | CP-01/03/04/05/07 | Cache miss/eviction plus authoritative recheck; no authority from cache |
| Storage outage | CP-01–04/06/07 | No acceptance/readiness/success without owner commit; recover and reconcile |
| Model unavailable | CP-01/04/05 | Exact approved fallback or explicit unavailable; no `latest`, auto-train, or blocked Synapse path |
| Event delivery failure | CP-06 | Independent bounded retry/dead-letter/replay; result/source fact unchanged |
| Tenant misconfiguration | CP-01–07 | Fail closed; no defaults, cross-tenant recovery, wrong destination, or secret/model selection |
| Poisonous messages | CP-02/03/06 | Quarantine/dead-letter; halt automated retry; authorized corrected replay |
| Schema incompatibility | CP-01–04/06/08 | Reject/quarantine or explicit coexistence/migration; never guess |
| Agent loops/unsafe actions | CP-05/08 | No agent active; advisory output cannot act; future agent re-enters Stage 11 and inherits all gates |

## Partial-result and stale-data semantics

| Object/path | Partial semantics | Stale semantics |
|---|---|---|
| Synchronous response | No implicit partial response. Optional fields may be absent only when the versioned operation schema defines them; degraded outcome is typed and policy-approved | Exact readiness/config/model/policy versions are returned or referenced; unavailable authority cannot be replaced with cached truth |
| Durable batch/inference/training | `FORBID_PARTIAL` by default. Approved partial policy produces an immutable manifest and cannot satisfy a full-result consumer | Job retains admitted versions. A retry cannot switch inputs/models; revocation/freshness checks determine whether it may continue/finalize |
| Dataset publication | No ready dataset until required object set, quality evidence, lineage, and catalog transaction pass. Partial candidates remain unreferenced/not-ready | Prior version remains immutable but is usable only if current readiness/freshness/policy permits it; no generic “last known good” rule |
| Model/artifact | Partial/corrupt artifact is unselectable. Registration/promotion is not successful without complete evidence | Cache/previous assignment is usable only when exact, approved, compatible, unrevoked, tenant/purpose-authorized, and within operation policy |
| Proactive insight/action | Partial or stale evidence cannot authorize a task. The insight is immutable; eligibility may expire | Phase A, Phase B, and at-effect checks use current authority/version; old accepted verifier output has no authority |
| Workflow | Completed children remain truthful; parent partial output requires declared graph policy and residual/failure manifest | Parent/children retain admitted workflow/handler/input versions; recovery does not hot-upgrade them |
| Delivery | Delivery failure is not partial computation. Polling returns authoritative result while delivery state is pending/dead-lettered | Replay preserves original fact/payload hash/version and rechecks current destination/security/expiry; it does not recompute or reauthorize |

## Recovery and reconciliation operations

Every operation below is typed, tenant/resource-scoped, idempotent, authorized, and mandatorily audited. It operates on exact identities and supports dry-run/impact evidence where practical. Named human assignment remains blocked under `A-04-OWNERSHIP`.

| Operation | Scope and authority | Reconciliation result |
|---|---|---|
| Job reaper/reconciler | Expired leases, stuck `RUNNING/FINALIZING/CANCELLATION_REQUESTED`, current fence and owner-result evidence | Abandon/retry/finalize/fail exactly one job without duplicating effect |
| Orphan-object reconciler | Candidate/multipart/artifact objects not referenced by a committed owner record; retention/legal-hold policy required | Attach only through valid idempotent owner publication or quarantine/delete by governed policy |
| Catalog/object integrity reconciler | Exact catalog references, object checksums, lineage and readiness state | Revoke/block corrupt or missing version; never synthesize bytes/readiness |
| Schedule reconciler | Schedule version, occurrence identities, current grant/freshness/catch-up policy | Submit missing eligible occurrence or record expired/suppressed; dedupe duplicates |
| Reservation/usage reconciler | Job/effect/result identities versus quota/cooldown/usage records | Commit/release/adjust once with reason and evidence; no caller-supplied counters |
| Outbox/delivery reconciler | Source fact/decision, notification intent, publication/delivery attempts, destination authority | Restore pending attempt, mark ambiguous/dead-letter/expired, or authorized replay; no recompute |
| Model assignment/cache reconciler | Exact assignment, registry digest, revocation, tenant/capability/purpose/runtime compatibility | Evict invalid cache; retain/restore only approved assignment; block capability if none |
| Audit/trace completeness reconciler | Required evidence IDs across request/job/result/event/effect | Missing mandatory pre-effect audit is an incident, not backfillable authorization; diagnostic gaps are reported separately |

### Poison and dead-letter rules

1. Classify before retry: transient infrastructure, deterministic input/schema, handler defect, authorization/policy, or ambiguous effect.
2. A poison item must not block unrelated tenant/pool/consumer work; isolation key and ordering consequences are explicit per activated operation.
3. Store bounded reason code, schema/handler version, payload hash and protected object reference where retention permits; do not copy sensitive payloads into logs.
4. Exhaustion becomes terminal job failure, quarantine, or per-consumer dead-letter state. A “DLQ” is a logical PostgreSQL record unless a later broker is independently justified.
5. Replay requires correction/compatible handler, present authority, current security checks, reason, immutable original reference, and new attempt/generation. It never erases the original failure.

## Backup, restore, and disaster-recovery contract

### Required logical recovery order

1. **Declare and contain:** identify affected tenant/environment/components; stop or fence writers, schedulers, publishers, and privileged mutations whose authority/consistency cannot be proven.
2. **Establish trusted control:** restore/verify identity, authorization, secret/key, mandatory audit, time, configuration, and approved recovery authority. There is no unaudited recovery mode.
3. **Restore authoritative metadata/state:** restore PostgreSQL owner schemas and integrity evidence from an approved, encrypted, tenant/residency-compliant backup. Verify transaction and referential consistency before enabling writers.
4. **Verify immutable bytes:** verify object inventory, digests, registry/catalog references, retention/legal holds, and tenant namespaces. Missing/corrupt objects revoke readiness/assignment rather than being fabricated.
5. **Classify recovery-point mismatch:** a database reference with no valid object is `MISSING_OR_CORRUPT` and remains unavailable pending verified byte recovery; an object with no committed database reference is `ORPHANED` and remains quarantined pending exact idempotent reattachment or governed cleanup. Neither case selects or recomputes data silently.
6. **Fence the pre-restore world:** advance an authoritative recovery epoch, expire every pre-restore lease/fence/session, isolate old workers and publishers, and require the new epoch on attempts/effects. Restored credentials, grants, endpoints, schedules, assignments, and deletion state are revalidated before use.
7. **Reconcile execution and external reality:** compare jobs, attempts, checkpoints, results, reservations, schedules, outbox rows, deliveries, deletion manifests, and external effect/provider evidence. Work or effects that may have occurred after the restored database recovery point remain `AMBIGUOUS` until reconciled; there is no blind mass replay.
8. **Invalidate derived caches:** rebuild only from restored authoritative state using ADR-008 cache identity and current revocation/assignment/policy checks.
9. **Resume in bounded phases:** health/read-only queries, control and polling, submissions, workers by pool, scheduler, then any separately admitted delivery path. Preserve backpressure.
10. **Verify and close:** run trace, tenant-isolation, integrity, duplicate/effect, readiness, assignment, deletion, and audit checks; record loss window, unresolved ambiguity, customer-visible status, and follow-up evidence.

### Disaster-recovery admission requirements

- Approved deployment topology and failure domains; backup owner, restore owner, security approver, service owner, incident commander, and on-call roster.
- Per data/control class RPO, RTO, backup frequency, retention, residency, encryption/key recovery, legal-hold/deletion behavior, and dependency ordering.
- PostgreSQL and object backups whose cross-store consistency can be reconciled through immutable identities; no claim of atomic cross-store snapshot unless proven.
- Restore environment isolation, provenance, malware/supply-chain verification, secret rotation, access review, and prevention of restored jobs/schedules/webhooks running before reconciliation.
- Periodic restore and regional/environment loss exercises with evidence for integrity, tenant isolation, job/effect dedupe, model assignment, readiness, audit completeness, and actual recovery times.

Because topology, targets, policies, products, and named owners are absent, disaster recovery is **logically specified but production-blocked**. Stage 13 makes no availability, zero-data-loss, automatic-failover, or regional-survival claim.

## Graceful degradation and fallback register

| Dependency/failure | Allowed degradation/fallback | Forbidden fallback |
|---|---|---|
| Diagnostic telemetry exporter | Continue owner operation if authoritative audit and safety controls succeed; buffer/drop only by later approved observability policy and expose degraded visibility | Treat telemetry as audit or hide prolonged loss |
| Notification delivery | Polling remains authoritative; result/insight stays available; delivery enters retry/dead-letter | Rerun capability/action or mark result failed |
| Optional approved partial batch policy | Return typed partial manifest only to consumers whose contract accepts it | Ordinary success or mixed-version merge |
| Model/artifact load | Exact prior or non-model fallback only when separately approved, compatible, current, tenant/purpose-authorized, and named in the operation profile | `latest`, cross-tenant cache, automatic training, blocked capability, or guessed compatibility |
| Catalog/readiness | None for an unverifiable dataset; explicit not-ready/unavailable | Cached ready flag or last dataset without current policy |
| Identity/control/policy/secrets/mandatory audit | None; fail closed | Local default, stale grant, plaintext secret, act-then-backfill audit |
| PostgreSQL owner state | None for acceptance/transition/effect truth; read-only cached presentation may be labeled stale only if it carries no authority and contract permits | Memory/log/queue state as business truth |
| Synapse/provider | None while `EVIDENCE_BLOCKED` and `LLM_PROVIDER_BLOCKED`; future explicit bounded profile required | Silent alternate provider/model or local unapproved generation |

## Anti-overengineering assessment

| Pattern/component | Disposition | Reason |
|---|---|---|
| PostgreSQL leases/fences/idempotency/reconciliation | Required now | Approved durable paths require crash/duplicate safety and truthful state |
| Per-operation timeout/retry/backoff policies | Required before activation | Failure behavior differs by operation and effect boundary; values require measurement |
| Transactional outbox/dead-letter records | Conditional | Required only for a promised external notification or named internal subscriber; not platform-wide today |
| Circuit breakers | Selective | Useful for repeated remote/optional dependency failure; never an authority fallback or universal wrapper |
| Shared cache tier | Unjustified now | No measured hot path; invalidation, tenant/version staleness, and authorization burden exceed evidenced value |
| Broker/stream processor | Unjustified now | PostgreSQL jobs/schedules/outbox cover approved needs; no measured fan-out/ordering/replay trigger |
| Workflow engine | Unjustified now | No active named workflow and deterministic PostgreSQL parent/child graph is sufficient if one appears |
| Active-active database/automatic regional failover | Unjustified now | Failure domains, topology, RPO/RTO, consistency and budget are unknown |
| Chaos platform | Unjustified as a product | Required fault-injection scenarios can start in existing test/runtime tooling; product follows proven scale need |
| Universal fallback/“last known good” | Rejected | Can violate tenant, policy, readiness, scientific validity, and exact assignment |
| Agentic recovery loop | Rejected | No agent justified; recovery is typed, bounded, authorized, and auditable |

## Recommendations

### R-13-01 — Make committed owner state and stable effect identity the recovery anchor

**Requirement/where:** `ARK-NFR-004/006`, critical paths CP-01–08. **Why now:** crash, duplicate, timeout, and response loss cannot be resolved from process or transport state. **Simplest implementation:** PostgreSQL owner records, immutable object refs, idempotency/effect IDs, attempts/fences, and reconciliation commands. **Alternative rejected:** infer outcome from retry/HTTP/queue/log state. **Trade-off:** explicit state and runbooks; truthful recovery. **Reconsideration:** never remove the invariant; physical mechanism may change through a superseding ADR.

### R-13-02 — Configure reliability by operation and failure class, not one global retry policy

**Requirement/where:** source Section 12; API, job, data, model, and delivery paths. **Why now:** a safe object read retry is not equivalent to a model assignment, privileged mutation, or ambiguous webhook. **Simplest implementation:** versioned operation reliability profile referenced at admission. **Alternative rejected:** universal retry/circuit/DLQ wrapper. **Trade-off:** more explicit policy/test cases; prevents retry amplification and duplicated effects. **Reconsideration:** common defaults may be factored only after measured profiles prove equivalence.

### R-13-03 — Keep partial and stale outcomes explicit and non-authoritative

**Requirement/where:** invalid/incomplete data, partial workflow, stale cache, model unavailable. **Why now:** silent degradation would violate scientific and policy truth. **Simplest implementation:** default `FORBID_PARTIAL`, typed manifests, exact as-of/version references, and owner rechecks. **Alternative rejected:** last-known-good or ordinary-success fallback. **Trade-off:** lower apparent availability; honest and reproducible outcomes. **Reconsideration:** only an operation-specific approved consumer/scientific policy may add a bounded fallback.

### R-13-04 — Treat disaster recovery as restore plus reconciliation, not infrastructure failover alone

**Requirement/where:** storage outage, duplicate execution, event delivery, model state, tenant controls. **Why now:** PostgreSQL, immutable objects, external effects, caches, and deliveries cannot be assumed to share one atomic snapshot. **Simplest implementation:** ordered containment/restore/integrity/reconcile/resume procedure over exact identities. **Alternative rejected:** claim automatic failover/zero loss without topology or targets. **Trade-off:** exercises and reconciliation tooling required; no false recovery guarantee. **Reconsideration:** Stage 15/17 evidence may select topology and numeric targets without weakening reconciliation.

## Decisions

- Adopt the ten reliability invariants, failure classes, retry/reconciliation boundaries, CP-13-01 through CP-13-08 matrices, partial/stale semantics, poison rules, and logical disaster-recovery order as the Stage 13 reliability baseline, subject to sponsor approval.
- Preserve accepted ADR-004 through ADR-008 unchanged. No new ADR is proposed because Stage 13 operationalizes their existing API, job, action/delivery, capability-admission, and security boundaries rather than choosing a new architecture style or superseding a material accepted decision.
- Keep all ADR-007 capability dispositions and ADR-008 production-admission blocks active. A reliability fallback is never a production-admission bypass.
- Require an approved per-operation numeric reliability profile and named recovery/on-call ownership before activation; values remain unresolved rather than invented.
- Keep Stage 14 unstarted until the sponsor approves Stage 13 and explicitly authorizes continuation.

## Contradictions and dangerous assumptions

| ID | Finding | Resolution | Consequence |
|---|---|---|---|
| `C-13-01` | Availability pressure can encourage stale entitlement/readiness/model cache use | Authoritative owner recheck and fail-closed dependency classification prevail | Lower apparent availability; no cross-tenant/policy/scientific violation |
| `C-13-02` | At-least-once retry can be mistaken for exactly-once execution | Only logical effects are deduplicated; attempts and ambiguous external outcomes remain explicit | No exactly-once transport or process claim |
| `C-13-03` | “Dead-letter” can imply a selected broker | It is a logical PostgreSQL job/publication/delivery state unless a broker trigger later passes | No speculative infrastructure |
| `C-13-04` | A previous model/dataset may look like a universal high-availability fallback | Use is allowed only by exact approved, compatible, current operation policy | No silent semantic drift or blocked-profile activation |
| `C-13-05` | Restoring a database backup can resurrect jobs, schedules, grants, endpoints, assignments, or secrets | Restore is contained; reconcile authority, revocation, fences, effects, and caches before resuming writers | No automatic post-restore execution |
| `C-13-06` | Audit outage recovery can tempt act-now/backfill-later behavior | Mandatory-audit operations remain blocked; later evidence records the incident but cannot retroactively authorize an effect | Security boundary preserved |
| `C-13-07` | Stage 11 source category names agent loops, but no agent is selected | Mark inactive for current design; deterministic unsafe-action controls remain covered; future agent re-enters Stage 11 | No invented agent runtime/runbook |
| `C-13-08` | A logical recovery matrix may be read as a production availability claim | Numeric policies, topology, products, named owners, and exercises are still required activation evidence | No RPO/RTO/availability/failover claim |

## Open questions and production inputs

| ID | Question / missing evidence | Required before | Temporary disposition |
|---|---|---|---|
| `Q-13-01` | What deadlines, attempt ceilings, backoff/jitter, leases/heartbeats, safe points, and terminal classifications apply to each operation? | Any operation activation | Missing profile blocks activation |
| `Q-13-02` | What queue-age, backlog, concurrency, tenant/pool fairness, and admission thresholds apply? | Load/production readiness | Measure in Stage 17; no guessed scaling component |
| `Q-13-03` | What idempotency, result, checkpoint, outbox, dead-letter, replay, and evidence retention windows match client/recovery contracts? | Production configuration | Must be no shorter than approved retry/reconciliation need and obey governance policy |
| `Q-13-04` | Which operations allow partial results, stale presentation, prior model, or non-model fallback, and which consumers accept them? | Each such operation | Default forbid/unavailable |
| `Q-13-05` | What failure domains, RPO/RTO, backup/restore topology, retention/residency/key recovery, and exercise frequency apply? | Deployment/production readiness | Logical restore order only; no DR claim |
| `Q-13-06` | Who are the named service, database, storage, data, capability, security, release, delivery, incident, and on-call recovery owners? | Production readiness | Logical roles only; `A-04-OWNERSHIP` remains blocking |
| `Q-13-07` | What receiver/provider idempotency and outcome-query contracts exist for each external effect/delivery? | External path activation | No blind retry; webhook/Synapse remain blocked |
| `Q-13-08` | What data-loss/customer-notification/incident severity and unreconciled-ambiguity policies apply? | Operational readiness | Report truthful unresolved state; no invented support promise |

## Requirement-to-design traceability updates

| Requirement | Stage 13 design evidence | Validation evidence required later |
|---|---|---|
| `ARK-FR-002/003` | CP-03 raw-first validation, quarantine, atomic readiness, backfill/reconciliation | Invalid/incomplete/duplicate/late/correction/storage fault suite |
| `ARK-FR-004/005/006` | CP-01 exact contract/readiness/scientific outcomes and no fabricated fallback | Contract, stale-readiness, model-unavailable and result-commit tests |
| `ARK-FR-007/008` | CP-02 durable lifecycle, backlog, crash, duplicate, cancellation, partial and poison recovery | State/lease/fence/retry/backlog/finalization fault injection |
| `ARK-FR-009` | CP-04 exact lifecycle, artifact integrity, assignment, cache and rollback incidents | Training/registry/load/revocation/reproduction/rollback tests |
| `ARK-FR-010/011` | CP-05/06 fail-closed proactive gates and independent delivery recovery | Revocation/race/audit/timeout/dedupe/dead-letter/replay tests |
| `ARK-FR-012` | Stable identities and reconciliation across request, data, job, result, insight, action, event, delivery and recovery | End-to-end trace completeness and recovery evidence |
| `ARK-NFR-001/003` | Dependency and tenant misconfiguration fail closed; recovery preserves security | Cross-tenant/authority/secret/audit/recovery negative tests |
| `ARK-NFR-002` | Partial/stale/schema/data-quality failures cannot become ready/success | Quality/freshness/schema/lineage and partial-manifest tests |
| `ARK-NFR-004` | At-least-once attempts, stable identities, fences, idempotent effects, ambiguity reconciliation | Duplicate/crash/timeout/stale-fence/external-effect fault injection |
| `ARK-NFR-005` | Failure isolation by tenant/pool/consumer and bounded admission/retry | Noisy-neighbor, backlog, poison and retry-storm load tests |
| `ARK-NFR-006` | Committed owner state, immutable failure/replay/recovery audit and DR verification | Trace/audit integrity, restore, orphan and effect-reconciliation tests |
| `ARK-NFR-007` | No unsupported numeric or availability claim; profiles and DR targets remain measured gates | Stage 17 capacity/cost/target evidence and exercises |
| `ARK-CON-001/002/003` | Owner modules and schemas remain recovery boundaries; no cross-write/shared-truth shortcut | Dependency, DB-role, object-namespace and restore-isolation tests |
| `ARK-CON-004/005` | Immutable bytes by reference plus PostgreSQL jobs/outbox first; no broker/cache/engine by default | Storage/catalog/job/outbox recovery and anti-overengineering evidence |
| `ARK-CON-006/007` | Push/batch baseline and conditional delivery keep explicit retry/replay boundaries | Integration and conditional activation fault suites |
| `SC-02-04/05/06/08/09/10/11/12` | Truthful failure, explicit reconciliation, tenant isolation, no unsafe action, owner roles, target blocks, and acceptance evidence | Stage 16 reliability/security suites plus Stage 20 named ownership |

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Every actual critical path is enumerated | PASS | CP-13-01 through CP-13-08, including inactive conditional paths explicitly labeled |
| Every path states detection | PASS | `Detection` column in every critical-path matrix |
| Every path states containment | PASS | `Containment` column plus cross-cutting invariants |
| Every path states user-visible status | PASS | `User-visible status` column; delivery/result and partial/success truth remain separate |
| Every path states retry boundary | PASS | `Retry boundary` column plus failure classification and idempotency/replay contract |
| Every path states data-consistency effect | PASS | `Consistency effect` column; owner commit, immutable versions, fences, and manifests |
| Every path states recovery owner | PASS LOGICALLY; PRODUCTION BLOCKED | Logical role in each row; named roster remains `A-04-OWNERSHIP`/`Q-13-06` |
| Every path states verification | PASS | `Verification step` column provides fault scenario/evidence target |
| All governing failure categories covered | PASS | Source-instruction and cross-cutting coverage matrices |
| Partial-result and stale-data semantics explicit | PASS | Dedicated object/path matrix and invariants 6–7 |
| Poison, replay, recovery, reconciliation, and DR explicit | PASS | Dedicated sections and logical restore order |
| Patterns justified without universal overengineering | PASS | Failure-class/pattern policy and anti-overengineering table |
| Approved authority and production blocks preserved | PASS | Facts, invariants, fallback register, decisions and contradictions |
| Authorized assurance challenge reconciled | PASS | Initial findings corrected; final read-only pass reported no critical/high defect and recommended `PASS` |
| Stage 14 not executed | PASS | Scope, decisions, and next-stage stop condition |

**Gate result: PASSED AND APPROVED.** CP-13-01 through CP-13-08 each state detection, containment, user-visible status, retry boundary, data-consistency effect, recovery owner, and verification. Every governing failure category is dispositioned; partial/stale, poison, finalization, reconciliation, cross-store recovery and disaster-recovery semantics are explicit; no accepted authority or production-admission block is weakened. The authorized final assurance review reported no critical or high defect, workspace structure/source-integrity validation passed, and the sponsor explicitly approved Stage 13 on 2026-08-13, authorizing Stage 14 only.

## Downstream consequences

- Stage 14 must define signals and evaluation evidence for every detection, queue/backlog, retry, circuit, fence, stale/partial, poison/dead-letter, reconciliation, audit-gap, restore, and dependency-health condition here, while keeping authoritative audit separate from telemetry.
- Stage 15 must map the logical failure domains, writer fencing, dependency order, backup/restore roles, and conditional components to an approved deployment topology without claiming active-active or automatic failover without evidence.
- Stage 16 must implement the matrix verification steps as contract, integration, fault-injection, security, recovery, restore, and end-to-end suites.
- Stage 17 must supply measured deadlines, retries, backlog/admission, resource isolation, retention, RPO/RTO, availability and cost evidence.
- Stage 20 must name accountable service/recovery/on-call owners, escalation, runbooks, and sequence production admission without weakening ADR-007/008 blocks.
- Stage 23 must retain the rejection/deferment of broker, shared cache, workflow engine, active-active topology, and agentic recovery until their evidence triggers pass.

## Exact next-stage inputs and stop condition

Stage 13 is approved and Stage 14 is authorized. Do not execute Stage 15.

Stage 14 must read:

1. Approved `outputs/stages/00-source-audit.md` through `outputs/stages/13-reliability.md`
2. Accepted ADR-000 through ADR-008
3. `sources/normalized/system-design-prompt.md` section **13. Observability and evaluation**
4. Capability/service-card observability and evaluation sections selected through `SOURCE_MANIFEST.md`
5. `stages/14-observability-evaluation.md`, `templates/stage-output.md`, and any directly referenced matrices

Execute Stage 14 only. Do not begin Stage 15 until Stage 14 passes its gate and the sponsor explicitly authorizes continuation.
