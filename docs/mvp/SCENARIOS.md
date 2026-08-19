# ARK Reference MVP scenarios

Status: `PLANNED`

> **ADR-017/018 notice:** these scenarios predate both revisions. The next set must add the hierarchy/pattern/admin cases in `docs/mvp/ADR-017-IMPACT.md` and the shared-balance/policy/reservation/settlement cases in `docs/mvp/ADR-018-IMPACT.md`.

## Scenario contract

All scenarios use versioned, synthetic fixtures and the same public run API. Scenario selection chooses fixture data and permitted fault hooks; it never changes architecture, grants production authority, or accepts arbitrary fault instructions from a caller.

Common constants:

- environment profile: `reference_mvp`;
- capability: `CAP-REC` version `1.0-demo`;
- operation: `recommendation-generate-batch`;
- handler: `poa_fixture_recommendation` version `1.0`;
- implementation label: `POA_FIXTURE_ONLY`;
- synthetic contract: `demo-transactions/1.0`;
- configuration: `demo-rec-policy/1.0`;
- authoritative result path: job/result polling;
- trace contract: `ark.reference-mvp.trace-event/1.0`.

The example fixture identifiers below are stable logical names. Concrete UUIDs are assigned per run and carried through the trace.

## S-01 — Successful eligible recommendation

### Intent

Prove the complete clean path from run initialization through persisted and retrieved Recommendation-shaped output.

### Fixture

- Tenant A test credential.
- Structurally and semantically valid transactions for two customers.
- Sellable catalog and available inventory.
- At least one customer meets the fixture eligibility rule.
- No fault hook and no simulated external delivery request.

### Expected order and outcome

1. Run and tenant context persist.
2. Raw input persists before validation.
3. Validation accepts all rows; quarantine count is zero.
4. Normalized dataset publishes `READY`.
5. Fixture capability eligibility returns `ELIGIBLE`.
6. One job and one attempt run.
7. Features, candidates, ranking, and business rules complete.
8. One immutable result is persisted.
9. Job transitions through `FINALIZING` to `SUCCEEDED`.
10. Polling returns the same result and exact lineage.

### Acceptance criteria

- One run, one logical job, one attempt, and one result exist.
- Result items are available, unique, deterministically ordered, and capped by configured top-k.
- Every required stage event exists exactly once unless the contract permits a summary event per customer.
- The result and UI display `POA_FIXTURE_ONLY` and all active-block warnings.
- Repeating the submit with the same tenant/idempotency key and canonical body returns the original run/job; a changed body conflicts.

### Required tests

- strict API/schema contract;
- PostgreSQL integration for run/job/result/event commits;
- deterministic ranking/tie-break golden test;
- idempotent replay/conflict test;
- two-tenant result concealment test;
- end-to-end UI/API polling test.

## S-02 — Partially invalid input with quarantined rows

### Intent

Prove that row-level structural failures remain visible and quarantined while a valid subset can proceed under an explicit fixture acceptance policy.

### Fixture

- Tenant A test credential.
- A bounded transaction batch containing valid rows plus rows with invalid timestamp, missing item identifier, and invalid monetary value.
- Valid catalog/inventory for the accepted rows.
- The accepted subset still satisfies fixture eligibility.

### Expected order and outcome

- Raw batch is stored in full.
- Structural report records accepted and rejected counts by stable reason code.
- Rejected rows are represented by tenant-scoped quarantine refs and safe row ordinals/hashes, never raw values in trace payloads.
- Normalization consumes only accepted rows.
- Dataset publishes `READY_WITH_QUARANTINE` in the demo vocabulary while the public dataset readiness remains `READY` plus quality report/reference.
- Recommendation job succeeds over the accepted subset.
- UI shows quarantine summary separately from result truth.

### Acceptance criteria

- Every rejected row has exactly one quarantine disposition and no normalized/result lineage.
- Every accepted row resolves from raw ref through normalized dataset lineage.
- Quarantine count and reason totals equal the validation report.
- A retry or replay creates no duplicate quarantine records.
- Result metadata explicitly reports the input quality status and accepted/rejected counts.

### Required tests

- row mutation/property tests for each reason code;
- raw-first crash-boundary test;
- quarantine uniqueness and cross-tenant concealment tests;
- accepted-only normalization test;
- end-to-end partial-input scenario test.

## S-03 — Structurally valid but scientifically ineligible data

### Intent

Prove that structural/readiness success does not imply capability eligibility or create a fabricated recommendation.

### Fixture

- Tenant B test credential.
- All rows satisfy the synthetic source schema and normalization rules.
- Catalog/inventory are valid.
- Transaction history intentionally fails the versioned fixture sufficiency rule, such as no customer reaching the minimum distinct purchase-history condition.

### Expected order and outcome

- Data receipt, validation, normalization, and dataset readiness succeed.
- Fixture eligibility returns `INELIGIBLE` with `INSUFFICIENT_HISTORY_FIXTURE`.
- No Recommendation execution job, attempt, features, candidates, ranking, or result is created.
- The run reaches terminal `INELIGIBLE` as a truthful domain outcome, not an infrastructure failure.

### Acceptance criteria

- Structural report has zero invalid rows.
- Dataset is `READY` before eligibility evaluation.
- No job/result rows or compute-stage events exist.
- API/UI clearly say “fixture eligibility; no scientific REC claim.”
- Repeating or replaying the run preserves the same reason and absence of effects.

### Required tests

- layer-separation unit/property tests;
- database negative-effect assertion;
- reason-code contract test;
- end-to-end ineligible scenario test.

## S-04 — Execution failure followed by retry

### Intent

Prove attempt-level retry, lease/fence ownership, and one logical result under a deterministic injected failure.

### Fixture

- Eligible Tenant A data.
- Server-owned scenario hook `FAIL_FIRST_ATTEMPT_AFTER_CLAIM_BEFORE_RESULT`.
- Versioned demo retry policy: at most two attempts; retry only the classified injected transient fault.

### Expected order and outcome

1. One logical job is created.
2. Attempt 1 is claimed with fence 1 and emits compute start.
3. The permitted fault raises `DEMO_TRANSIENT_EXECUTION_FAILURE`; attempt 1 becomes failed/retryable and job enters `RETRY_WAIT`.
4. Attempt 2 receives a new attempt identity/fence and reruns the exact pinned handler/inputs.
5. Attempt 2 commits the only result; job finalizes and succeeds.

### Acceptance criteria

- Exactly one job, two attempts, two distinct fences, and one result exist.
- Attempt 1 cannot heartbeat, persist a result, or finalize after attempt 2 claims.
- Retry retains tenant, run, correlation, input, configuration, release, and handler identities.
- Trace shows failure classification and retry linkage without stack traces or raw data.
- UI groups attempts under one job and does not depict two recommendations.

### Required tests

- job state-machine/property test;
- deterministic fail-once integration test;
- stale-fence publication/finalization negative test;
- worker restart/reclaim test;
- end-to-end retry timeline test.

## S-05 — Result-delivery failure

### Intent

Prove that result persistence and job truth are independent from a delivery attempt.

### Fixture

- Eligible Tenant A data.
- Local no-network delivery simulator enabled for this scenario only.
- Simulator deterministically returns `DEMO_RECEIVER_UNAVAILABLE`.

### Expected order and outcome

- Recommendation computation, result owner commit, evidence finalization, and job `SUCCEEDED` occur first.
- A separate simulated delivery intent/attempt records `FAILED`.
- Polling continues to return the successful result.
- No retry of capability computation occurs; no internet/network call occurs.

### Acceptance criteria

- Job/result state is `SUCCEEDED`; simulated delivery state is `FAILED`.
- Result digest and attempt count are unchanged by delivery failure.
- Trace causation links delivery to the committed result but uses a distinct delivery identity.
- UI displays separate “authoritative result” and “simulated delivery” panels plus `EXTERNAL_DELIVERY_BLOCKED` warning.
- Network-egress test proves the simulator cannot resolve or call a URL.

### Required tests

- result-versus-delivery state contract;
- no-recompute assertion;
- no-network adapter test;
- delivery trace-schema test;
- end-to-end failure-isolation scenario.

## S-06 — Stored-run replay

### Intent

Prove deterministic reconstruction of a prior run from persisted events and resources without resubmission or computation.

### Fixture

- Any completed S-01 through S-05 run, with S-04 preferred to show attempt grouping.
- Same-tenant test credential.

### Expected order and outcome

- `GET /demo/v1/runs/{run_id}/replay` authenticates and takes a snapshot cursor equal to the highest committed event sequence.
- It returns stored run metadata, events `1..snapshot_sequence`, and authorized resource summaries in original order.
- The trace owner may append `run.replay.accessed` after the snapshot for audit; that new event is not recursively included in the current replay.
- No ingestion, eligibility, job submission, attempt, result, or delivery command runs.

### Acceptance criteria

- Replayed event IDs, sequence numbers, payload hashes, and resource refs match stored truth.
- Job/attempt/result/quarantine/delivery row counts do not change.
- Cross-tenant replay is concealed/denied and leaks neither existence nor counts.
- Replaying twice returns equivalent snapshots for the same requested cutoff, excluding separate access-audit events.
- UI marks the view `REPLAY — NO EXECUTION`.

### Required tests

- snapshot ordering and hash-integrity integration test;
- zero-new-effect database assertion;
- cross-tenant replay negative test;
- replay of partial, failed-attempt, and delivery-failed traces;
- end-to-end Gradio replay test.

## Scenario summary

| Scenario | Dataset outcome | Eligibility | Job attempts | Result truth | Delivery truth | Terminal run outcome |
|---|---|---|---:|---|---|---|
| S-01 eligible | `READY` | `ELIGIBLE` | 1 | persisted/retrievable | not requested | `SUCCEEDED` |
| S-02 partial invalid | `READY` with quarantine report | `ELIGIBLE` | 1 | persisted/retrievable with quality summary | not requested | `SUCCEEDED_WITH_QUARANTINE` demo display; job `SUCCEEDED` |
| S-03 ineligible | `READY` | `INELIGIBLE` | 0 | none | none | `INELIGIBLE` |
| S-04 retry | `READY` | `ELIGIBLE` | 2 | one persisted result | not requested | `SUCCEEDED` |
| S-05 delivery failure | `READY` | `ELIGIBLE` | 1 | persisted/retrievable | simulated `FAILED` | run/job `SUCCEEDED`; delivery separate |
| S-06 replay | unchanged | unchanged | unchanged | read only | read only | `REPLAYED` presentation only; stored run unchanged |

## Global scenario assertions

- All event sequences are monotonic per run and all events validate against the trace contract.
- No raw row, credential, secret, direct identifier, or exception stack appears in a trace event or Gradio view.
- Two tenants using colliding client idempotency values never share a run, job, event, quarantine item, or result.
- No scenario trains, loads, promotes, or assigns a model; emits an internal production event; sends a webhook; invokes an LLM; or clears a block.
- All visible deterministic features, scores, thresholds, and rules are labeled fixture-only.
