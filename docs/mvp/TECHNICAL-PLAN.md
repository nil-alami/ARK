# ARK Reference MVP technical plan

Status: `PLANNED — IMPLEMENTATION NOT STARTED`

> **ADR-017/018 notice:** this technical plan predates both revisions. Apply `docs/mvp/ADR-017-IMPACT.md` and `docs/mvp/ADR-018-IMPACT.md` before implementation evidence is refreshed; direct credential→tenant and unpriced job behavior are no longer sufficient architecture proof.

## Decision frame

The technical choices below are reversible Reference MVP implementation choices under ADR-016 sponsor review. They are not new production ADRs. A later production or Phase 2 implementation must reevaluate them against authoritative environment, security, data, scientific, integration, workload, and operating evidence.

## Technology evaluation

| Candidate | Requirement served | Evaluation | MVP disposition | Reconsideration trigger |
|---|---|---|---|---|
| FastAPI | Typed REST boundary, async submit/status/result/trace resources, OpenAPI | Direct fit with Python and Pydantic; small operational surface; keeps Gradio outside core | select for MVP | Named consumer/protocol or measured runtime constraint that cannot be met |
| Pydantic | Strict request/response/fixture/event validation | Makes schemas executable and supports unknown-field rejection and versioned models | select for MVP | Contract tooling must change; logical schemas remain |
| Gradio | Fast local demonstration and trace visualization | Appropriate as an API-only demo console; not suitable evidence for production UX | select for MVP demo client | Product/consumer UI requirements arrive |
| PostgreSQL | Durable run/event/job/attempt/result truth and transaction/race semantics | Required by approved architecture; mocks/SQLite cannot prove leases, constraints, or owner commits | select as authoritative local store | Accepted ADR-005/010 trigger or production environment decision |
| Local immutable object adapter | Raw/normalized/result payload refs and digests | Simplest behavior-compatible adapter for bounded synthetic artifacts | select for MVP only | Shared validation needs object-compatible service semantics or production environment selected |
| Periodic HTTP polling | Universal result/trace recovery and Gradio updates | Matches approved contract and avoids SSE/WebSocket infrastructure | select | Approved interactive latency/load requirement shows polling inadequate |
| SQLAlchemy Core/ORM plus Alembic | PostgreSQL access and additive migrations | Common Python implementation seam; owner repositories can remain explicit | select provisionally; pin versions during implementation | Library incompatibility or migration-control evidence |
| Separate queue/broker | Worker wake-up | Unnecessary; PostgreSQL claim polling is authoritative and sufficient | reject | Measured claim/dispatch gap after query/index/poll tuning |
| Distributed workflow engine | One linear bounded job | No graph/timer/human-wait requirement | reject | Approved named workflow exceeds explicit coordinator safely |
| Kubernetes/containers | Local process lifecycle | Kubernetes has no requirement; containers optional and not needed to prove boundaries | reject mandate | Approved fleet/placement/availability/security need plus staffed runbook |
| Production IAM/secrets stack | Test tenant context | Evidence and authority are unavailable; selecting a product would imply production trust | postpone | ADR-008 exit packet and named security/environment owners |

Specific package/runtime versions are implementation lockfile decisions, not architecture decisions. The implementation slice that establishes the release records the selected supported Python/PostgreSQL/package matrix in its README and evidence manifest.

## Process topology

| Entrypoint | Responsibility | Reads/writes | Explicit non-responsibility |
|---|---|---|---|
| `api` | FastAPI routes, test trust, run initialization, bounded ingestion command, job/status/result/trace queries | Calls public owner ports; no direct foreign-schema writes | Recommendation compute, worker lifecycle, production IAM |
| `worker-general` | Poll/claim jobs, heartbeat/fence, execution rechecks, deterministic fixture handler, result report | Job port plus catalog/capability/result/evidence ports | HTTP authority, job lifecycle table writes, external delivery |
| `gradio-demo` | Scenario selection and API polling/replay visualization | HTTP only | Imports of ARK owner modules/repositories; authoritative state |
| `maintenance` | Additive migrations, fixture seed, scope-checked demo reset, reconciliation inspection | Owner-approved commands | Production privileged/recovery operations |
| `delivery-simulator` | In-process/local adapter used only by S-05 to persist a deterministic failed attempt | Simulated delivery owner port, no socket/network capability | Webhook, DNS, URL, egress, result truth |

The simulator may be hosted in `worker-general` for the demo, but remains a distinct logical module and trace component. No `publisher-delivery` production role is created.

## Proposed repository/module shape

The exact names may be adjusted before code starts, but dependency direction is binding.

```text
src/ark_reference_mvp/
  api/                 # FastAPI controllers and transport models
  demo_ui/             # Gradio API-only client
  context/             # test-only AuthContext adapter
  runs/                # demo run owner and scenario registry
  control/             # fixture admission decisions
  ingestion/           # receipt, validation, quarantine, normalization
  catalog/             # dataset version/readiness owner
  jobs/                # job/attempt/lease/fence/finalization owner
  capabilities/rec_fixture/
                       # eligibility, features, candidates, rank/rules
  results/             # immutable Recommendation-shaped result owner
  evidence/            # trace, bounded audit/lineage/usage
  delivery_sim/        # no-network delivery state
  objects/             # provider-neutral immutable object port + local adapter
  shared_contracts/    # IDs, versions, errors, context, correlation only
  entrypoints/         # api, worker, gradio, maintenance
migrations/            # owner-qualified additive migrations
tests/                 # unit, contract, integration, E2E, architecture
```

Allowed dependency direction is entrypoints/controllers → public application ports → owner domain/repository. Cross-owner repository imports, table writes, and capability-private imports fail architecture tests.

## HTTP contract

### Demo orchestration surface

| Method/path | Behavior | Idempotency / response |
|---|---|---|
| `GET /demo/v1/scenarios` | Returns the six immutable scenario definitions and warnings | Safe read |
| `POST /demo/v1/runs` | Derives tenant; creates one run; receives selected bounded fixture; performs raw receipt/validation/normalization/eligibility; creates Recommendation job only when eligible | Requires `Idempotency-Key`; returns `202` with run/job URLs or terminal ineligible run |
| `GET /demo/v1/runs/{run_id}` | Returns authorized run summary and owner-state refs | Safe read, tenant concealed |
| `GET /demo/v1/runs/{run_id}/events` | Cursor-based trace polling | `after_sequence`, bounded page |
| `GET /demo/v1/runs/{run_id}/quarantine` | Safe quarantine projection | No raw invalid data in response by default |
| `GET /demo/v1/runs/{run_id}/replay` | Snapshot stored run/events/resources | No resubmission or effect |

### Approved job/result subset

| Method/path | Behavior |
|---|---|
| `GET /v1/jobs/{job_id}` | Public job state, progress nullable, attempt summary, result/error refs |
| `POST /v1/jobs/{job_id}:cancel` | Optional backlog slice if needed; idempotent cooperative request |
| `GET /v1/jobs/{job_id}/result` | Bounded result with fixture warnings and lineage refs |

All mutations carry `Authorization`, `Idempotency-Key`, optional bounded `X-Correlation-ID`, and server-generated request ID. The test credential format is local and not documented as a production bearer-token contract.

## Request and result shape

The run request contains only:

- `request_version`;
- `scenario_id` from the registered enum;
- synthetic transaction, catalog, and inventory fixture blocks or registered fixture refs;
- optional `top_k` within the immutable demo policy range.

It contains no tenant authority, arbitrary fault directive, object path, callback URL, model choice, handler choice, or delivery destination.

The Recommendation-shaped result contains:

- run/job/result and correlation identities;
- `implementation_label = POA_FIXTURE_ONLY`;
- per synthetic subject opaque ref and ordered item refs/scores;
- applied fixture rule codes;
- empty/ineligible/quality status where applicable;
- dataset/feature/candidate/ranking/config/handler/release lineage refs;
- explicit `scientific_validity = NOT_EVALUATED` and `production_eligible = false`.

Scores are deterministic demonstration values and must not be named probabilities, propensities, expected revenue, or business lift.

## Data contract and pipeline

### Synthetic input

- Transaction: opaque event/customer/item IDs, UTC timestamp, positive fixture quantity, bounded decimal fixture amount, synthetic currency enum.
- Catalog: opaque item ID, synthetic category, sellable flag.
- Inventory: item ID, available flag, effective timestamp.

The Pydantic envelope rejects unsupported contract versions and unknown fields. Row-level validation records exact stable reason codes. Semantic normalization standardizes timestamps/decimals, deduplicates by fixture event ID with a deterministic conflict rule, validates catalog/inventory references, and publishes an immutable dataset version plus quality report.

### Fixture eligibility

Eligibility is a versioned deterministic teaching rule: a READY dataset must contain enough accepted purchase history to exercise Recommendation stages. The exact threshold is stored in `demo-rec-policy/1.0`, labeled fixture-only, and never reused as a production default.

### Fixture recommendation stages

1. Generate deterministic R/F/V and item/category frequency features.
2. Generate candidates only from sellable/available catalog items, excluding already disallowed items under fixture policy.
3. Compute a stable demonstration score from normalized bounded feature terms.
4. Tie-break by stable opaque item ID.
5. Apply inventory, dedupe, and top-k rules; preserve truthful empty output.

No step fits parameters, loads a model, uses randomness without a recorded deterministic seed, calls a provider, or writes outside capability-owned state.

## PostgreSQL ownership model

Proposed logical schemas/tables:

| Owner schema | Bounded tables |
|---|---|
| `demo_run` | `runs`, `scenario_selections`, `idempotency_records` |
| `control` | `fixture_decisions` |
| `catalog` | `raw_receipts`, `validation_reports`, `quarantine_rows`, `dataset_versions`, `lineage_links` |
| `job` | `jobs`, `job_attempts`, `job_leases`, `job_transition_keys` |
| `rec_fixture` | `eligibility_decisions`, `feature_sets`, `candidate_sets`, `ranked_sets` |
| `result` | `results`, `result_publication_keys` |
| `evidence` | `trace_events`, `run_sequence_counters`, `completion_evidence`, `replay_accesses` |
| `delivery_demo` | `delivery_intents`, `delivery_attempts` |

Owner repositories/migrations are qualified. Foreign keys and read models may connect identities, but only owner ports mutate an owner's tables. Every tenant-bearing row includes trusted `tenant_id`; unique/idempotency keys include tenant scope.

## Job and retry subset

Supported states remain compatible with the final lifecycle:

`ACCEPTED → READY → RUNNING → (RETRY_WAIT → READY → RUNNING)* → FINALIZING → SUCCEEDED`

and truthful `FAILED` / `CANCELLATION_REQUESTED` / `CANCELLED` branches when implemented.

- Claim creates monotonic attempt number, opaque fence, lease expiry, and state version in a short transaction.
- Worker computation holds no row lock.
- Every heartbeat/result/report command supplies job, attempt, fence, and expected version.
- Retry policy is immutable per job. Only S-04's named transient demo fault is retryable in the required scenarios.
- Owner result commit is idempotent by stable result identity and current fence.
- Crash after result commit retries finalization/evidence linkage, not computation.

Concrete lease/poll/retry durations are bounded demo configuration and must be documented as non-production values in the implementation README.

## Gradio console plan

The console contains:

- permanent banner: “Reference MVP — synthetic — POA_FIXTURE_ONLY — not production/scientific”;
- scenario selector with intent and expected outcome;
- optional fixture preview with synthetic-only label;
- run button and returned IDs;
- owner-state summary separate from trace;
- ordered stage timeline colored by implementation class/status;
- attempt grouping and retry link;
- validation/quarantine count panel;
- Recommendation-shaped result panel with science warnings;
- simulated delivery panel separate from result;
- stored replay control and `REPLAY — NO EXECUTION` badge;
- active-block summary.

The UI polls run and event resources periodically, persists the last `sequence_no`, applies bounded exponential backoff on transient API read failure, and stops only on the scenario's declared terminal conditions. UI errors never mutate run truth.

## Failure and fault-hook design

Fault hooks are enumerated server-side scenario configuration, not caller-supplied free-form values. They are compiled/configured out or rejected outside `reference_mvp`.

Required hooks:

- fail first execution attempt after claim and before result commit;
- optionally pause at deterministic state boundaries for tests;
- simulate local delivery receiver unavailable;
- test-only trace/event write failure to prove required transition hold;
- worker process kill in isolated tests.

Each hook emits `INJECTED_FAULT` and cannot accept code, SQL, paths, URLs, durations outside policy, or cross-tenant targets.

## Verification plan

### Test levels

- Unit/property: validators, normalization, eligibility, features, ranking, business rules, job transition model, event schema.
- Architecture: imports, owner repositories/migrations, no forbidden infrastructure/dependencies, Gradio API-only rule.
- Contract: API/problem/job/result/trace/replay compatibility and unknown fields.
- PostgreSQL integration: constraints, transactions, idempotency, claim/fence, raw-first, quarantine, result/finalization, replay snapshot.
- Object adapter: tenant/ref/digest/path traversal/immutability/missing object.
- End-to-end: all six scenarios with API, worker, Gradio client behavior, and real PostgreSQL.
- Security/isolation: two tenants, colliding IDs/keys, body tenant forgery, foreign refs, trace/result/replay concealment, redaction.
- Resilience: worker kill, lease expiry, stale fence, response loss, trace failure, crash after result commit.

### MVP exit criteria

- All scenario acceptance criteria and trace completeness rules pass.
- Every vertical slice README and evidence record exists.
- Tests run against real PostgreSQL and the behavior-compatible object adapter.
- No production-blocking invariant in the exercised scope fails.
- No prohibited dependency or runtime role is present.
- Sponsor can follow the implementation README to migrate, start roles, run each scenario, inspect/replay a run, stop, and reset only demo state.
- `implementation/MVP-STATUS.md` records sponsor evidence acceptance; AI cannot mark the Reference MVP accepted by itself.

## README contract

Each implementation slice creates or updates the closest implementation README. The final implementation README must include:

- purpose and non-production/non-precedent warning;
- exact release/tool/dependency matrix;
- process and module map;
- configuration and fixture-only guardrails;
- migrate/start/stop/run/poll/replay/reset commands;
- scenario catalogue and expected states;
- test commands and evidence locations;
- fault-hook safety;
- demonstration shortcuts versus unchanged production decisions;
- active blocks and explicitly absent components;
- troubleshooting and recovery for local demo state.

## Implementation stopping rule

This file is a plan only. No package scaffold, migration, API, UI, fixture, or application code is authorized by its existence. Implementation begins only on a later explicit sponsor instruction and follows `implementation/MVP-BACKLOG.md` in order.
