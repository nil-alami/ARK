# ARK Reference MVP implementation backlog

Status: `PLANNED — NO IMPLEMENTATION STARTED`

> **ADR-017/018 change:** this historical slice backlog predates the organization/business and shared-credit models. Before further evidence is accepted, insert both mandatory impact revisions; existing slice numbers do not imply either is complete.

## Execution rules

- Implement slices in order. Do not begin a later slice until the prior slice's acceptance criteria, required tests, trace events, README update, and sponsor review evidence are complete.
- Each slice ends in one demonstrable end-to-end behavior through Gradio → FastAPI → owner modules/PostgreSQL → worker where applicable → polling/replay.
- The primary implementation label is always `POA_FIXTURE_ONLY`; no slice clears a production, capability, data-contract, trust, delivery, deployment, capacity, or cutover block.
- Each slice uses real PostgreSQL semantics and the immutable local object adapter for integration/E2E tests. Unit mocks do not satisfy slice acceptance.
- Fault hooks and test credentials are usable only under the `reference_mvp` profile.
- AI may implement and test, but only the human sponsor accepts slice evidence and changes status.
- Any material change to accepted architecture or scope stops implementation for a new/superseding decision; passing tests cannot authorize it.

## Ordered slice summary

| Order | Slice | Demonstrable end-to-end behavior | Scenario | Depends on |
|---:|---|---|---|---|
| 1 | `MVP-SLICE-01` walking trace | Eligible synthetic Recommendation run succeeds and renders complete trace/result | S-01 | Plan approval and local dependencies |
| 2 | `MVP-SLICE-02` quarantine lane | Mixed-validity batch quarantines invalid rows and still returns a result from accepted rows | S-02 | Slice 01 |
| 3 | `MVP-SLICE-03` ineligible lane | READY dataset fails fixture eligibility and terminates with no job/result | S-03 | Slice 02 |
| 4 | `MVP-SLICE-04` retry lane | First attempt fails; second attempt under same job produces one result | S-04 | Slice 03 |
| 5 | `MVP-SLICE-05` delivery isolation | Job/result succeeds while no-network simulated delivery fails independently | S-05 | Slice 04 |
| 6 | `MVP-SLICE-06` stored replay | Prior run is reconstructed from stored events without new compute/effects | S-06 | Slice 05 |

## MVP-SLICE-01 — Successful eligible walking trace

### End-to-end behavior

From the Gradio console, Tenant A submits the registered eligible fixture. FastAPI derives the tenant, creates a run, stores raw data, validates and normalizes it, publishes a READY dataset, evaluates fixture eligibility, creates one durable job, and returns polling resources. `worker-general` claims a fenced attempt, generates fixture features/candidates/ranking, persists one result, finalizes evidence, and succeeds. Gradio renders the stored trace and result.

### Included work

- Establish one Python release, dependency lock, module boundaries, role entrypoints, and `reference_mvp` startup guard.
- Add owner-qualified PostgreSQL migrations and immutable local object adapter.
- Implement Pydantic common IDs/context/problem/run/fixture/job/result/trace contracts.
- Implement FastAPI scenario/run/job/result/trace endpoints required by S-01.
- Implement two-tenant test trust adapter, one immutable fixture control decision, raw receipt, clean validation, normalization/readiness, and fixture eligibility.
- Implement job admission, attempts, claim/lease/fence, heartbeat, result report, `FINALIZING`, completion evidence, and terminal polling.
- Implement deterministic fixture features, candidates, ranking, rules, and immutable result.
- Implement append-only trace ledger and Gradio console/timeline.
- Add migration/start/stop/run/reset commands; reset must target only marked demo data.

### Acceptance criteria

- S-01 criteria in `docs/mvp/SCENARIOS.md` pass through the running UI/API/worker.
- Required trace events from run initialization through `result.polled` exist in canonical order, validate against schema 1.0, and resolve owner resources.
- Same tenant/key/body returns one run/job; changed body conflicts; another tenant may reuse the client key without collision.
- Raw object exists before validation; result exists before finalization/success.
- Gradio imports no ARK owner/repository module and displays permanent fixture/active-block warnings.
- No scheduler, publisher, webhook, external provider, model loader, agent, broker, workflow engine, Kubernetes, or production IAM dependency appears in build/runtime manifests.

### Required tests

- Unit/property: clean validators, normalization, eligibility, features, candidate/rank/rules, state machine, trace schema.
- Architecture: module import direction, one-writer repositories/migrations, API-only UI, forbidden dependency/role absence.
- Contract: run/job/result/event/problem schemas, unknown-field and unsupported-version rejection.
- Integration: PostgreSQL bootstrap/re-bootstrap, raw-first/object digest, idempotency, claim/fence, result-before-finalization, event atomicity.
- E2E: Gradio-client submission/polling for S-01 with real PostgreSQL and worker process.
- Isolation/redaction: two-tenant foreign refs, colliding IDs/keys, no sensitive trace/result/log fields.
- Resilience: lost HTTP response replay and worker stop before claim.

### Structured trace events

At minimum: `run.initialized`, `tenant.context.derived`, `data.received`, validation start/completion, zero-count `quarantine.completed`, `normalization.completed`, `dataset.readiness.published`, `capability.eligibility.evaluated`, `job.created`, attempt claim/recheck, feature/candidate/ranking/rules completion, `result.persisted`, `job.finalizing`, `completion_evidence.linked`, `job.succeeded`, and `result.polled`.

### README change

Create `implementation/README.md` with the README contract from `docs/mvp/TECHNICAL-PLAN.md`, including exact migrate/start/run/poll/stop/reset instructions and explicit non-production/non-scientific warnings. Add Slice 01 evidence/test commands and known limits.

### Demonstration shortcuts versus production decisions

- Shortcut: test credentials, synthetic contract, deterministic Recommendation fixture, local object adapter, bounded demo timing values, Gradio UI.
- Unchanged decisions: modular-monolith ownership, REST/typed ports, PostgreSQL jobs, result-before-finalization, polling, no agent/broker/Kubernetes.
- Blocks unchanged: all active blocks, especially CAP-REC `MIGRATION_BLOCKED`, `DATA_CONTRACT_ADMISSION_BLOCKED`, `EXTERNAL_TRUST_BLOCKED`, and deployment/capacity blocks.

## MVP-SLICE-02 — Partial input and quarantine lane

### End-to-end behavior

The user selects S-02. The full raw batch is stored, invalid rows receive stable quarantine dispositions, accepted rows normalize into a READY dataset, and the same durable Recommendation path returns a result derived only from accepted rows. Gradio shows validation/quarantine and result panels separately.

### Included work

- Add row-level validation reason taxonomy and quarantine owner repository/API.
- Add partial-acceptance policy to the immutable synthetic contract.
- Add safe quarantine summary/details, accepted-row lineage, and UI panel.
- Make reprocessing/idempotency avoid duplicate quarantine rows.

### Acceptance criteria

- S-02 criteria pass end to end.
- Raw, accepted, rejected, normalized, and result counts reconcile exactly.
- Invalid row refs cannot appear in normalized dataset, feature set, candidates, ranking, or result lineage.
- Quarantine API and events expose only safe ordinal/hash/reason/ref fields.
- Repeating the command returns the same run/quarantine/result truth.

### Required tests

- Mutation/property tests per row reason code and mixed batches.
- Integration tests for quarantine uniqueness, transaction boundaries, accepted-only normalization, and lineage reconciliation.
- Cross-tenant quarantine/list/inference tests.
- E2E S-02 UI/API/worker test plus trace completeness.
- Crash after raw receipt and during validation, proving no false READY.

### Structured trace events

Slice 01 events plus one or more bounded `row.quarantined` events and a nonzero `quarantine.completed`; validation, dataset, and result events carry accepted/rejected aggregate counts.

### README change

Update `implementation/README.md` with S-02 run instructions, reason-code table, safe inspection commands, partial-acceptance warning, and tests/evidence.

### Demonstration shortcuts versus production decisions

- Shortcut: fixture row rules and quarantine lifecycle have no production retention/privacy semantics.
- Unchanged decisions: raw-first preservation; invalid data cannot become canonical; readiness and eligibility remain distinct.
- Blocks unchanged: `DATA_CONTRACT_ADMISSION_BLOCKED` and `DATA_GOVERNANCE_BLOCKED` remain active.

## MVP-SLICE-03 — Scientifically ineligible lane

### End-to-end behavior

The user selects S-03. Structurally valid data becomes a READY dataset, but fixture capability eligibility returns `INELIGIBLE`. The run terminates without a job, attempt, feature, candidate, ranking, or result, and Gradio explains the layer boundary.

### Included work

- Add versioned fixture eligibility decision/reason object and terminal ineligible run projection.
- Add UI distinction among validation, readiness, and fixture eligibility.
- Add negative-effect assertions/read model.

### Acceptance criteria

- S-03 criteria pass end to end.
- Eligibility executes only after a committed READY dataset.
- No job/result/compute-stage owner rows or events exist.
- Run/API/UI outcome is ineligible, not failed/unavailable/succeeded.
- The visible reason is explicitly fixture-only and cannot be interpreted as scientific approval.

### Required tests

- Eligibility boundary unit/property tests around the fixture threshold.
- Integration test asserting zero job/result/effect rows.
- Contract test for terminal ineligible run and problem/outcome separation.
- Cross-tenant ineligible run concealment.
- E2E S-03 UI/API test and prohibited-event assertion.

### Structured trace events

Events through `dataset.readiness.published`, then `capability.eligibility.evaluated` with `INELIGIBLE` and `run.ineligible`. Job/feature/candidate/ranking/result/finalization events are forbidden.

### README change

Update `implementation/README.md` with S-03 instructions, layer/outcome explanation, no-job verification query/command, and fixture-threshold warning.

### Demonstration shortcuts versus production decisions

- Shortcut: deterministic sufficiency threshold is only a teaching fixture.
- Unchanged decision: data readiness never equals capability eligibility.
- Blocks unchanged: CAP-REC remains `MIGRATION_BLOCKED`; no scientific owner/threshold is assigned.

## MVP-SLICE-04 — Execution failure and retry lane

### End-to-end behavior

The user selects S-04. One job is admitted; attempt 1 fails at the registered post-claim/pre-result fault boundary; the job enters retry wait; attempt 2 with a new fence succeeds; Gradio groups both attempts under the one logical job/result.

### Included work

- Add immutable demo retry policy and server-owned fail-once scenario hook.
- Complete failed attempt, retry scheduling, re-claim, fence invalidation, and attempt grouping.
- Add optional deterministic barriers/process-kill harness for integration tests.

### Acceptance criteria

- S-04 criteria pass end to end.
- One job, two attempts/fences, one result, and one terminal success exist.
- Retry pins exact original identities/versions and only retries the classified transient failure.
- Attempt 1 is unable to heartbeat/report/persist/finalize after attempt 2 claims.
- No arbitrary client fault directive or fault hook works outside `reference_mvp`.

### Required tests

- State-machine/property tests for failure/retry/terminal transitions.
- Concurrent claim and stale-fence negative tests.
- Worker kill/lease expiry/reaper test against PostgreSQL.
- Result publication race and crash-after-result-before-finalization test.
- E2E S-04 UI/API/worker timeline test.

### Structured trace events

Slice 01 events with attempt 1 `job.attempt.claimed`, `job.execution_recheck.passed`, `job.attempt.failed`, `job.retry.scheduled`; then attempt 2 claim/recheck and the single compute/result/finalization sequence. Fault events carry `INJECTED_FAULT`, never stack/raw data.

### README change

Update `implementation/README.md` with S-04 commands, attempt/fence interpretation, demo timing values, safe fault-hook restrictions, restart/reconcile steps, and tests/evidence.

### Demonstration shortcuts versus production decisions

- Shortcut: only one registered transient fault and small demo timing/retry values.
- Unchanged decisions: at-least-once attempts, no exactly-once claim, fencing, one logical owner result, finalization retry not recompute.
- Blocks unchanged: no production reliability/SLO/capacity/operations claim.

## MVP-SLICE-05 — Result-delivery failure isolation

### End-to-end behavior

The user selects S-05. Recommendation computation and job finalization succeed. A separate no-network delivery simulator records a failed intent/attempt. Gradio continues to show the authoritative successful result and a separately failed simulated delivery.

### Included work

- Add delivery-simulation owner records/port and server-owned S-05 scenario policy.
- Add result-to-simulated-intent causation and separate UI panel.
- Enforce no URL/destination/network stack in simulator.

### Acceptance criteria

- S-05 criteria pass end to end.
- Result/job `SUCCEEDED` and delivery simulation `FAILED` coexist truthfully.
- Delivery failure creates no new job/attempt/result and does not alter result digest.
- Build/static/runtime tests prove the simulator cannot perform network egress or register arbitrary destinations.
- UI and README state that this does not implement a webhook/publisher or clear `EXTERNAL_DELIVERY_BLOCKED`.

### Required tests

- Result/delivery state separation contract/property tests.
- PostgreSQL integration for distinct intent/attempt identities and idempotency.
- No-network/URL-field schema/static tests.
- No-recompute row/event count assertion.
- E2E S-05 UI/API/worker/simulator test.

### Structured trace events

The complete success sequence through `job.succeeded` and `result.polled`, followed by `delivery.intent.created` and `delivery.attempt.failed` with `SIMULATED_BEHAVIOR`, `DELIVERY_SIMULATOR`, and `DEMO_RECEIVER_UNAVAILABLE`.

### README change

Update `implementation/README.md` with S-05 run/inspection commands, authoritative-result versus delivery explanation, no-network proof, and unchanged external-delivery block.

### Demonstration shortcuts versus production decisions

- Shortcut: local deterministic receiver failure with no network, signing, DNS, egress, or ambiguity.
- Unchanged decisions: polling authoritative; delivery state separate; delivery retry never reruns capability work.
- Blocks unchanged: `EXTERNAL_DELIVERY_BLOCKED`, production trust/secrets, consumer/cutover blocks.

## MVP-SLICE-06 — Stored-run replay and closure

### End-to-end behavior

The user opens a completed run and requests stored replay. FastAPI returns an authorized consistent snapshot of its stored events/resources. Gradio renders `REPLAY — NO EXECUTION`. A replay-access event is appended after the snapshot, while job/attempt/result/quarantine/delivery counts remain unchanged.

### Included work

- Implement replay snapshot/cutoff, event hash verification, resource authorization, and replay access evidence.
- Add replay UI and integrity/gap display.
- Complete evidence export, scenario matrix command, and sponsor-operable README.

### Acceptance criteria

- S-06 criteria pass for representative S-01 through S-05 runs, including retry and delivery-failed histories.
- Event IDs/order/hashes/resources match stored truth through the snapshot cutoff.
- Replay creates no compute/effect and is concealed cross-tenant.
- Tampered/missing event/resource yields an integrity problem, never a synthetic success.
- All six slices/scenarios pass from a clean migration, after restart, and after scope-checked demo reset.
- Final evidence manifest maps scenarios, requirements, tests, events, versions, shortcuts, active blocks, and sponsor acceptance.

### Required tests

- Snapshot/order/hash/integrity integration and property tests.
- Zero-new-effect database diff assertions.
- Cross-tenant replay concealment and payload redaction.
- E2E replay UI test for clean, quarantine, ineligible, retry, and delivery-failed runs.
- Clean bootstrap/restart/reset/full scenario regression and forbidden-component manifest test.

### Structured trace events

No historical event is rewritten. The replay response includes stored events through `snapshot_sequence`; `run.replay.accessed` is appended after that cutoff with `REPLAYED` and no compute/job/result/delivery causation.

### README change

Finalize `implementation/README.md`: clean setup, process topology, all scenarios, polling/replay, evidence export, restart/reconcile/reset, troubleshooting, exact dependency/runtime matrix, fixture/fault safety, shortcuts, active blocks, and explicitly absent infrastructure.

### Demonstration shortcuts versus production decisions

- Shortcut: replay is a local evidence/presentation feature, not event reprocessing or disaster recovery.
- Unchanged decisions: immutable identities, tenant authorization, stored owner truth, no replayed effects.
- Blocks unchanged: all production/science/data/security/environment/capacity/cutover blocks.

## Closure activities (not an additional implementation slice)

After Slice 06 passes, the human sponsor reviews the immutable evidence packet and either accepts the Reference MVP demonstration or records defects. Closure updates only `implementation/MVP-STATUS.md` and `implementation/MVP-TRACEABILITY.md`; it does not create an architecture approval, production release, Phase 2 entry, or block transition.

## Global definition of done

- Six end-to-end scenario behaviors are demonstrable from Gradio and reproducible by API/test automation.
- Every slice has sponsor-reviewed acceptance evidence, required tests, trace events, and README updates.
- Real/simplified/simulated behavior remains visible in UI, trace, README, result, and evidence manifest.
- All active production blocks remain explicit and unchanged.
- No postponed/not-applicable component has become a hidden dependency or runtime role.
- `implementation/MVP-TRACEABILITY.md` has no uncovered required flow, scenario, slice criterion, or trace requirement.
