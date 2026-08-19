# ML SERVICE CARD
===============

**Service name:** Next Purchase Prediction (NPT) / Nostradamus  
**Service ID/version:** `nostradamus` / package `0.1.0`  
**Owner:** AFE AI ML team — explicit production owner/CODEOWNERS entry not found  
**Reviewed implementation:** [nostradamus.py](<C:/Users/AFE AI/PycharmProjects/select-family/engine/engine/nostradamus/nostradamus.py>)  
**Feature contract:** [features_schema.yaml](<C:/Users/AFE AI/PycharmProjects/select-family/engine/engine/nostradamus/configs/customer_snapshot/features_schema.yaml>)  
**Output/persistence contract:** [output.py](<C:/Users/AFE AI/PycharmProjects/select-family/engine/engine/nostradamus/pipelines/output.py>), [persistence.py](<C:/Users/AFE AI/PycharmProjects/select-family/engine/engine/nostradamus/pipelines/persistence.py>)

## Current readiness assessment

**Status: not production-ready in the reviewed working tree.**

The intended NPT design is clear, but four material blockers exist:

1. NPT is commented out of the main engine workflow in [engine/main.py](<C:/Users/AFE AI/PycharmProjects/select-family/engine/main.py>); therefore, no active API or worker path invokes it.
2. Two configured paths do not match the files’ current locations:
   - Code expects `configs/state/snapshot_state.yaml`; the file is under `configs/customer_snapshot/snapshot_state.yaml`.
   - Code expects `nostradamus/data/business_domains.json`; the file is under `configs/businesses/business_domains.json`.
3. Model-output field names do not match final-output field names:
   - CLF emits `y_pred` and probability columns but does not populate `clf_bucket`.
   - RSF emits `expected_t_days`; the merger expects `rsf_expected_days_rsf`, while a later fallback expects `rsf_expected_t_days`.
   - Consequently, the reviewed pipeline can calculate predictions but still produce `nostradamus.served=false`.
4. The final `DataFrame` is not a stable public schema: merge suffixes and model diagnostic columns can leak into the response, and dynamic horizons such as 7 or 14 days are not fully supported by the hard-coded final bucket mapper.

The checkout contains in-progress local changes, so these path issues may be transitional, but they are real for the reviewed state.

## INFRASTRUCTURE CLASSIFICATION

1. **Request-driven or proactive?**  
   **Request-driven.** Work starts only when `Nostradamus.run(whatson_id, ...)` is called. It does not independently discover customers and emit platform events. Once invoked, it can proactively create a missing calendar policy and train missing models.

2. **Stateless or stateful?**  
   **Stateful.** It depends on customer snapshots, business calendar policies, snapshot schema state, per-business model artifacts, the model registry, and optionally historical prediction batches.

3. **Synchronous or asynchronous?**  
   **Currently synchronous and blocking.** Architecturally it should be an asynchronous business-level job because it can recompute hundreds of thousands of snapshots and bootstrap two models.

4. **Online or batch-oriented?**  
   **Batch-oriented.** One invocation processes all eligible customers of one business. No single-customer low-latency inference path exists.

5. **Raw data or derived data?**  
   **Primarily raw data.** It directly reads transaction rows and derives NPT-specific customer snapshots. It also consumes derived configuration and state: calendars, feature schema, model registry, and model artifacts.

---

# 1. PURPOSE

- Predict when each eligible customer will make their next purchase.
- Produce either:
  - a CLF time window such as 0–7, 8–15, 16–30, or greater than the horizon; or
  - an RSF-refined point estimate for customers considered likely to purchase soon.
- Intended consumers are the Select platform, BCDP/customer-profile functionality, campaign targeting, and downstream customer engagement systems.
- The capability exists to support time-sensitive actions: reminders, offers, replenishment campaigns, and customer outreach near the predicted purchase time.
- No active downstream consumer is currently wired in the main engine.

# 2. TRIGGER / EXECUTION MODE

- **Current entry point:** direct Python method call:
  - `Nostradamus.run(...)`
  - convenience `main(whatson_id, persist_predictions=False)`
- **Mode:** request-triggered, business-scoped batch.
- **Current execution:** synchronous.
- **Recommended platform mode:** asynchronous job submitted by API, schedule, or transaction-data-readiness event.
- **Schedule:** none in code.
- **Events consumed/emitted:** none.
- **Can initiate work proactively?**
  - No independent discovery or event publication.
  - Once called, it may train absent CLF/RSF models and create a missing business calendar.

# 3. INPUT CONTRACT

## Required invocation input

- `whatson_id: int`
  - Tenant/business identifier used against the Whatson transaction system.
  - Resolved internally to `business_id`.
  - No explicit positive-integer validation is performed before database access.

## Optional invocation inputs

- `allow_train_if_missing: bool = True`
  - When `True`, missing CLF or RSF models are trained during the same run.
  - When `False`, a missing model raises `RuntimeError`.
- `persist_predictions: bool = False`
  - When `True`, the final result is appended to `CustomerNextPurchasePredictions`.
- `batch_id: UUID | str | None`
  - Supported by the lower-level persistence method.
  - Not exposed by `run()`, so callers cannot make a complete run idempotent.

## Required datasets

These are data dependencies, not API payload fields.

### Raw transaction dataset

Fetched internally from the Badger/Whatson-release transaction source:

| Field | Type/requirement | Meaning |
|---|---|---|
| `Phone` | Nonblank string | Customer grouping key |
| `At` → `transaction_date` | Valid timestamp | Purchase-event time |
| `Amount` | Numeric, strictly greater than zero | Purchase-event amount |
| `WhatsonId` | Numeric identifier | Business/tenant identifier |
| `SourceType` → `source_type` | Integer in `{0,1,2,3}` | Transaction source |
| `Id` | Fetched but not used in validation/modeling | Source transaction identifier |

The service treats every valid row as a canonical purchase event. It does not currently deduplicate by `Id` or validate order status/event grain.

`Items` and product-category data are not required by the current active feature set.

### Business and identity data

- `whatson_id → business_id` mapping.
- Business record and `Type`, used when a calendar policy must be created.
- For persistence only:
  - `Businesses`
  - `Cdp`
  - `Bcdps`
  - a unique `(business_id, phone) → BcdpId` resolution.

### Configuration and model data

- Active `BusinessCalendars` row or a valid business-domain cadence mapping.
- Customer snapshot schema and active snapshot version.
- Active per-business CLF and RSF records in `select_model_files`.
- Corresponding local model artifacts under `MODELS_STORAGE`.

## Minimum data requirements

### Business-level readiness

- At least **200 valid transaction rows inside the extracted lookback window**.
- Extraction window: latest transaction date minus **365 days** through the latest transaction date.
- Invalid rows are removed before applying the 200-row threshold.

### Customer/snapshot eligibility

A snapshot is eligible only when:

- `has_history == 1`
- `frequency >= 2`
- `recency_days` is present and between `0` and `365`
- `tenure_days >= 7`
- core features are non-null:
  - `recency_days`
  - `frequency`
  - `has_history`
  - `tenure_days`
- `gap_mean` is present and nonnegative for repeat-purchase histories.

### Training-only requirements

- At least **500 observed events in validation** and **500 in test**.
- The CLF path performs an early check requiring at least 1,000 total observed CLF events.
- Both CLF and RSF temporal splitting must be able to create ordered, nonempty train/validation/test periods satisfying those event floors.

## Input schema/version

- No versioned external API schema exists.
- Intended active customer-snapshot contract: **version 2**.
- CLF model metadata uses `npt_hgb_v1`.
- CLF bucket/horizon metadata uses `canonical_v1`.
- Current configured snapshot-state path does not resolve to the version-2 state file.

# 4. OUTPUT CONTRACT

## Primary output

A pandas `DataFrame`, intended to contain one row per `(business_id, phone)`, chosen from that customer’s latest generated eligible snapshot.

Normal execution drops ineligible customers instead of returning an explicit result for each customer.

## Stable intended serving fields

| Field | Type | Meaning |
|---|---|---|
| `business_id` | integer | Internal business identifier |
| `phone` | string | Customer key |
| `snapshot_date` | date | Feature as-of date |
| `snapshot_version` | integer | Snapshot feature-contract version |
| `calendar_version` | integer | Business calendar version |
| `nostradamus.served` | boolean | Whether a usable prediction exists |
| `nostradamus.rsf_apply` | boolean | Whether RSF produced the selected point prediction |
| `nostradamus.next_event_date` | nullable date | RSF point estimate |
| `nostradamus.next_event_from` | nullable date | Inclusive CLF window lower bound |
| `nostradamus.next_event_to` | nullable date | Inclusive CLF window upper bound |

CLF window semantics for a 30-day horizon:

| Bucket | From | To |
|---|---:|---:|
| `d0_7` | snapshot + 0 days | snapshot + 7 days |
| `d8_15` | snapshot + 8 days | snapshot + 15 days |
| `d16_30` | snapshot + 16 days | snapshot + 30 days |
| `gt_30` | snapshot + 31 days | `null` |

## Current diagnostic/model fields

The returned `DataFrame` can also include:

- `clf_applied`
- `clf_bucket`, `clf_bucket_idx`
- `clf_horizon_days`
- `p_d0_7`, `p_d8_15`, `p_d16_30`, `p_gt_<horizon>`
- `max_prob`
- `p_near`
- `clf_model_id`
- `rsf_routed`, `rsf_route_reason`, `rsf_applied`
- `risk_score`
- `buy_prob_30`, `buy_prob_60`, `buy_prob_90`
- `expected_t_days`, `median_t_days`
- `rsf_model_id`
- split, model-version, horizon-version, and merge-suffixed fields.

These are not currently whitelisted into a stable API response.

## Scores/confidence

- **CLF bucket probabilities:** probability per time bucket.
- **`max_prob`:** largest CLF bucket probability.
- **`p_near`:**  
  `p_d0_7 + p_d8_15 + p_d16_30`
- **RSF routing threshold:** `p_near >= 0.55`.
- **RSF outputs:**
  - probability of purchase by 30/60/90 days,
  - expected time in days,
  - median time in days,
  - risk proxy `-expected_time`.
- `rsf_confidence` is initialized but never populated.

## Persisted output schema

When enabled, rows are appended to `public."CustomerNextPurchasePredictions"` with:

- `Id`
- `BcdpId`
- `BusinessId`
- `SnapshotDate`
- `CreatedAt`
- `BatchId`
- `Served`
- `RsfApply`
- `PredictionSource`: `NONE | CLF | RSF`
- `NextEventDate`
- `NextEventFrom`
- `NextEventTo`
- `ClfBucket`
- `ClfHorizonDays`
- `PNear`
- `RsfExpectedDays`
- `SnapshotVersion`
- `CalendarVersion`
- `ClfModelId`
- `RsfModelId`

`(BatchId, BcdpId)` is intended to be unique.

## Possible statuses

The requested statuses are **not currently implemented as a run envelope**.

- `SUCCESS`: should mean the batch completed and predictions were produced/persisted as requested.
- `PARTIAL`: no current representation; persistence is all-or-nothing.
- `FAILED`: currently represented by an exception.
- `NOT_ELIGIBLE`: currently represented inconsistently by an empty `DataFrame`, an unserved `DataFrame`, or omission of ineligible customers.

A production API should expose these explicitly rather than requiring consumers to infer them.

# 5. HIGH-LEVEL WORKFLOW

```text
whatson_id
  ↓
Resolve business_id and transaction bounds
  ↓
Fetch last 365 days of raw transactions
  ↓
Validate rows and enforce 200-transaction floor
  ↓
Load/create business calendar and snapshot version
  ↓
Generate customer × snapshot-date feature rows
  ↓
Upsert CustomerSnapshots
  ↓
Apply cold-start/customer eligibility rules
  ↓
Load CLF model
  ├─ missing → create future labels → temporal split → train → register
  └─ found   → inference
  ↓
Predict CLF bucket probabilities
  ↓
Compute p_near and route rows where p_near ≥ 0.55
  ↓
Load RSF model
  ├─ missing → create survival labels → temporal split → train → register
  └─ found   → inference on routed rows
  ↓
Merge CLF and RSF predictions
  ↓
Select latest snapshot per customer
  ↓
Build Nostradamus serving fields
  ↓
Return DataFrame
  ↓ optional
Resolve phone → BcdpId and append immutable prediction batch
```

# 6. ELIGIBILITY / PRECONDITIONS

- Valid `whatson_id` with a resolvable business.
- At least 200 usable transactions in the 365-day lookback.
- Required source columns and valid values.
- Source database, dev database, and model storage must be reachable.
- Snapshot schema and snapshot-state files must exist at configured locations.
- A valid active calendar must exist or be creatable.
- Customer must have at least two purchases and seven days of observed tenure.
- Required snapshot features must be complete.
- For existing-model inference:
  - model feature contract must match the active snapshot schema;
  - model classes must match the active bucket definition.
- For model bootstrap:
  - labels must be constructible;
  - temporal periods must contain at least 500 validation and 500 test events.
- For persistence:
  - prediction table must exist;
  - each phone must map to exactly one BCDP customer for the business.
- No explicit tenant entitlement/configuration check exists.

# 7. DEPENDENCIES

## Internal

- Shared `DataFetcher`, `QueryRunner`, `PostgresqlCRUD`, and `DBEngines`.
- Shared [model_handler.py](<C:/Users/AFE AI/PycharmProjects/select-family/engine/engine/model_handler/model_handler.py>).
- Customer snapshot builder.
- CLF pipeline using `HistGradientBoostingClassifier`.
- RSF pipeline using `RandomSurvivalForest`.
- Labeling, temporal splitting, routing, output construction, and persistence modules.

## External

- PostgreSQL:
  - Badger/Whatson release transactions
  - Orbit/Whatson release identity and business metadata
  - Whatson dev snapshots, calendars, model registry, and predictions
- S3-compatible client is configured, but active model loading currently reads a local path; the relevant download call is commented out.
- Local filesystem for model and debug artifacts.

## Data

- Raw transaction history.
- Business identity and type.
- Customer/BCDP identity mapping.
- Business calendar policies.
- Customer snapshot rows.
- Active model registry records.

## Models/artifacts

- Per-business HGB classifier.
- Per-business random survival forest artifact containing:
  - RSF pipeline,
  - feature encoder,
  - missing-value state,
  - feature list,
  - training/model configuration.
- Local examples exist under `artifacts/models_storage`, but the active path is environment-driven.

## Libraries

- Python 3.11+
- pandas, NumPy
- scikit-learn
- scikit-survival
- SQLAlchemy/PostgreSQL driver
- joblib
- PyYAML
- boto3
- dotenv

Several imported runtime dependencies are not fully declared in the project’s main dependency list.

# 8. STATE & STORAGE

## Reads

- Raw transactions and transaction bounds/counts.
- Business mapping and business type.
- Active `BusinessCalendars` policy.
- Snapshot schema/state YAML.
- `select_model_files`.
- CLF and RSF joblib artifacts.
- BCDP identity tables during persistence.

## Writes

- `CustomerSnapshots`: upserted using:
  - business,
  - phone,
  - snapshot date,
  - calendar version,
  - snapshot version.
- `BusinessCalendars`: created/updated when no active policy exists.
- `select_model_files` and model files when training.
- `CustomerNextPurchasePredictions` when persistence is enabled.
- Local debug CSVs:
  - `rsf_pred_df.csv`
  - `out_after_rsf.csv`
  - `final_out.csv`

## Persistent state

- Business calendar history.
- Snapshot schema version history.
- Derived customer snapshots.
- Per-business models and registry metadata.
- Optional immutable prediction batches.

## Cache

- No explicit online cache.
- Loaded models live only in the `Nostradamus` object for the duration of that object; the handler rechecks model storage during a run.

## Intermediate artifacts

- Large in-memory transaction, snapshot, label, CLF, RSF, and merged `DataFrame`s.
- Debug CSVs are overwritten at shared filenames, creating concurrency and data-leakage risks across tenants.

# 9. EXECUTION PROFILE

- **Execution:** synchronous, CPU-bound and database-I/O-bound.
- **Workload shape:** one business, all eligible customers.
- **GPU:** not required or used.
- **CPU:** ordinary multicore CPU; current snapshot loop is mostly sequential.
- **RSF parallelism:** configured with `n_jobs=1`.
- **RAM:** not specified; must hold transactions, all snapshots, probabilities, labels, and merged results in memory.
- **Parallelizable:** across businesses with isolated artifact paths and database controls. Current shared CSV filenames prevent safe concurrent execution.
- **Snapshot DB chunk size:** 1,000 rows.
- **Identity-resolution chunk size:** 500 phones.

Observed historical run:

- 21,567 transactions
- 292,873 snapshot rows
- 51,320 eligible rows
- 17,910 RSF-routed rows
- 2,217 final customers
- approximately **2 minutes 50 seconds**

Another recorded snapshot stage produced 27,296 rows in approximately 5–22 seconds, depending mainly on database-write time. Evidence is in [nostradamus.log](<C:/Users/AFE AI/PycharmProjects/select-family/engine/engine/nostradamus/logs/nostradamus.log>).

**Expected scale risk:** daily-cadence businesses multiply customers by daily snapshot dates. The service recomputes the capped window rather than incrementally updating only new snapshots.

**Timeout considerations:** no timeout or cancellation mechanism exists. API-thread execution would be unsafe; use a job queue with execution timeout, heartbeat, and cancellation.

# 10. CONFIGURATION

## Data and eligibility

- `LOOKBACK_DAYS = 365`
- `MIN_NPT_TRANSACTION_COUNT = 200`
- `MIN_TENURE_DAYS = 7`
- Daily snapshot lookback: 30 days
- Snapshot cadences:
  - daily
  - weekly
  - fortnightly
  - monthly
- Default cadence: fortnightly

## Prediction horizon and routing

- CLF maximum horizon: 30 days
- Target future-coverage eligibility: 80%
- Preferred dynamic horizons: 30, 14, or 7 days
- Near buckets:
  - `d0_7`
  - `d8_15`
  - `d16_30`
- `P_NEAR_THRESHOLD = 0.55`
- A `min_top_class_prob = 0.35` value exists in configuration but is not enforced by the active router.
- RSF evaluation grids: 30, 60, 90 days.

## Training split

- Train time fraction: 70%
- Validation time fraction: 15%
- Remaining approximately 15% for test.
- Minimum validation events: 500.
- Minimum test events: 500.
- Split-boundary adjustment limit: 200 iterations.

## CLF model

- Algorithm: histogram gradient boosting.
- Max depth: 4.
- Learning rate: 0.05.
- Max iterations: 800.
- Minimum leaf samples: 15.
- L2 regularization: 4.0.
- Early stopping enabled.
- Validation fraction: 0.1.
- Random seed: 42.

## RSF model

Current configuration is explicitly marked as a **fast-test configuration**, not a production configuration:

- Trees: 5.
- Minimum leaf samples: 10.
- Max features: 1.
- Max depth: 3.
- Jobs: 1.
- Random seed: 42.
- Additional RSF eligibility gate: disabled.

## Tenant-specific configuration

- Separate CLF and RSF per `business_id`.
- Separate calendar policy per business.
- Horizon derived from the business’s observed timeline.
- No explicit tenant entitlement or configurable per-tenant routing threshold.

## Environment configuration

- `MODELS_STORAGE`
- `MODEL_ENDPOINT_URL`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `BUCKET`
- `NOSTRADAMUS_PREDICTIONS_READ_DB`
- `NOSTRADAMUS_PREDICTIONS_WRITE_DB`
- Database connection settings used by `DBEngines`.

# 11. FAILURE / FALLBACK

## Possible failures

- Business mapping missing; current indexing can raise `IndexError`.
- No transactions or fewer than 200 valid transactions.
- Required transaction columns missing or all rows invalid.
- Snapshot state/configuration path missing or malformed.
- Business-domain configuration missing.
- Calendar creation/update failure.
- `CustomerSnapshots` table or required unique constraint missing.
- No eligible customer snapshots.
  - Empty eligibility is not consistently handled because the orchestrator checks `None`, not `.empty`.
- Missing model with training disabled.
- Insufficient labeled validation/test events.
- Feature schema/model feature incompatibility.
- Model artifact missing or unreadable.
- CLF class IDs incompatible with current horizon.
- RSF preprocessing artifact incomplete.
- CLF/RSF output-name mismatch prevents final serving.
- Dynamic bucket names not supported by the hard-coded final mapper.
- Local debug-artifact collisions during concurrent runs.
- Persistence cannot resolve a phone to exactly one BCDP customer.
- Database insert or connection failure.

## Retryable?

- No automatic retries are implemented.
- Transient DB/model-storage errors are potentially retryable at job level.
- Data-contract, model-contract, missing-identity, and insufficient-history errors are not retryable without correcting data/configuration.
- A failed persistence attempt may be retried safely only with the same caller-controlled `batch_id`; `run()` currently does not expose one.

## Fallback

- Intended model fallback:
  - customers below the RSF routing threshold retain the CLF window.
- Missing model fallback:
  - train a model if `allow_train_if_missing=True`.
- Data-not-ready fallback:
  - return empty or unserved results.
- There is no fallback from an RSF execution exception back to CLF; the whole run fails.
- Model load errors are treated as “model missing,” which may unexpectedly trigger expensive retraining.

## Partial-result behavior

- No formal `PARTIAL` status.
- Ineligible customers are normally omitted.
- Persistence validates and writes the batch transactionally; one unresolved/ambiguous BCDP identity rejects the entire batch.
- Existing predictions already stored from earlier batches remain unchanged.

## Error contract

Inference mostly raises ordinary `ValueError`, `KeyError`, `RuntimeError`, or database exceptions.

Persistence provides structured codes including:

- `NPT_OUTPUT_COLUMNS_MISSING`
- `NPT_BUSINESS_MISMATCH`
- `NPT_PHONE_MISSING`
- `NPT_SNAPSHOT_DATE_INVALID`
- `DUPLICATE_CURRENT_NPT_PREDICTION`
- `INVALID_NPT_STATE`
- `INVALID_NPT_WINDOW`
- `INVALID_NPT_PROBABILITY`
- `INVALID_NPT_VERSION`
- `INVALID_NPT_HORIZON`
- `INVALID_NPT_EXPECTED_DAYS`
- `BUSINESS_NOT_FOUND`
- `NPT_BCDP_NOT_FOUND`
- `NPT_BCDP_AMBIGUOUS`
- `DATABASE_CONFIGURATION_ERROR`
- `DATABASE_CONNECTION_FAILED`
- `NPT_PREDICTION_WRITE_FAILED`

# 12. INTEGRATION

## API

- No dedicated NPT HTTP API.
- No request or response DTO.
- Main-engine integration exists only as commented code.

Recommended job submission contract:

```json
{
  "whatson_id": 129502,
  "allow_train_if_missing": false,
  "persist_predictions": true,
  "idempotency_key": "platform-generated-key"
}
```

Recommended result envelope:

```json
{
  "status": "SUCCESS",
  "job_id": "uuid",
  "business_id": 44,
  "batch_id": "uuid",
  "snapshot_version": 2,
  "calendar_version": 1,
  "counts": {
    "input_transactions": 0,
    "eligible_customers": 0,
    "served_customers": 0,
    "clf_customers": 0,
    "rsf_customers": 0
  },
  "predictions": [],
  "errors": []
}
```

## Events emitted

- None currently.
- Recommended:
  - `npt.job.completed`
  - `npt.job.failed`
  - optionally `npt.prediction.created` per persisted batch, not per customer unless required.

## Events consumed

- None currently.
- Suitable future triggers:
  - transaction-data-ready,
  - customer-feature-snapshot-ready,
  - model-approved,
  - scheduled tenant refresh.

## Job type

- Business-scoped batch prediction.
- Training should be a separate job type rather than a side effect of inference.

## Result retrieval

- Current: returned directly as a pandas `DataFrame`.
- Optional persisted results: query `CustomerNextPurchasePredictions` by:
  - `BatchId`,
  - `BusinessId`,
  - `BcdpId`,
  - newest `CreatedAt`.

## Idempotency

- Snapshot upsert is intended to be repeatable for the same business/phone/date/calendar/snapshot versions.
- Prediction persistence is append-only.
- `(BatchId, BcdpId)` prevents duplicate rows within one batch.
- Because `run()` generates a new batch UUID and does not accept an idempotency key, repeated requests can create duplicate semantic batches.

## Versioning

- Package version: `0.1.0`.
- Snapshot version: intended active version 2.
- Calendar version: per-business integer.
- CLF model and horizon labels have string versions.
- Persisted rows retain model IDs and snapshot/calendar versions.
- No public API version or complete feature-signature compatibility check exists.

# 13. OBSERVABILITY

## Current observability

The implementation logs:

- run start/completion;
- stage start/completion;
- business ID;
- transaction, snapshot, eligible, routed, prediction, and customer counts;
- model IDs;
- snapshot feature-build, DB-upsert, and total timing;
- local debug CSVs.

It does not expose a metrics endpoint, distributed traces, job heartbeats, or a consistent run ID across every log record.

## Required operational metrics

- Job success/failure/not-eligible/partial counts.
- Total and per-stage latency.
- Queue time and job age.
- Database query/upsert/persistence latency.
- Model load and training time.
- Input, snapshot, eligible, routed, served, CLF, RSF, and persisted row counts.
- Retry and timeout counts.
- Memory high-water mark and CPU utilization.
- Artifact and database write failures.

## Required data metrics

- Transaction freshness and lookback coverage.
- Valid/invalid/dropped row counts by rule.
- Customer count and transactions per customer.
- Duplicate event/transaction IDs.
- Amount validity and outlier rates.
- Feature missingness, infinities, and range violations.
- Snapshot count by date/cadence.
- Eligibility rate and rejection reason.
- Phone-to-BCDP resolution coverage.

## Required ML metrics

### CLF

- Model ID/version and feature-schema version.
- Bucket distribution and probability distribution.
- Macro and weighted F1.
- Top-2 accuracy.
- Confusion matrix.
- Calibration/Brier or log-loss.
- Actual purchase rate by predicted bucket.
- `p_near` distribution and RSF routing rate.

### RSF

- Model ID/version.
- Concordance index.
- Time-dependent AUC at 30/60/90 days.
- Brier score and integrated Brier score.
- Expected-days distribution.
- Calibration by predicted time window.
- Censoring/event rate.

### Contract-health alerts

- Nonzero CLF predictions with missing `clf_bucket`.
- Routed rows with no RSF point result.
- `served=false` rate unexpectedly near 100%.
- Output fields with `_x`/`_y` merge suffixes.
- Model feature signature differing from snapshot schema.
- Missing snapshot/domain configuration paths.

# 14. OWNERSHIP / ISOLATION

## Owns

The NPT service should exclusively own:

- next-purchase label semantics;
- dynamic horizon and bucket definitions;
- CLF and RSF models;
- near-time routing policy;
- NPT feature/snapshot contract if these snapshots are not made a shared platform asset;
- NPT model-performance evaluation;
- next-purchase prediction history and serving contract;
- NPT job lifecycle and idempotency rules.

## May access

Through explicit contracts:

- canonical purchase-event or transaction-data service;
- tenant/business metadata service;
- versioned customer-feature service;
- model registry/artifact store;
- identity-resolution service for BCDP IDs;
- its own calendar, snapshot, model, and prediction stores.

## Must NOT directly access

In the target multi-ML-service architecture, NPT should not directly:

- query operational raw transaction tables;
- query `Businesses`, `Cdp`, or `Bcdps`;
- write generic shared customer tables without an ownership contract;
- depend on Churn, RFM, or REC implementation modules;
- use shared unversioned model-handler internals;
- mutate other services’ settings or results;
- expose phone numbers in uncontrolled logs or shared debug files;
- overwrite tenant-independent local artifact filenames.

## Current isolation gaps

- Direct connections to three database roles.
- Direct BCDP identity lookup by phone.
- Direct writes to generically named `CustomerSnapshots` and `BusinessCalendars`.
- Shared model handler imports Churn, RFM, and NPT types/implementations.
- Raw transaction ingestion and feature generation are embedded in the same service.
- Shared local debug paths are not tenant/run isolated.

For the multi-service platform, the preferred boundary is:

```text
Canonical purchase events
          ↓
Versioned shared/customer features
          ↓
NPT asynchronous business job
          ↓
Versioned NPT prediction batch
          ↓
Platform retrieves result or consumes completion event
```

This preserves the critical distinction between the small API/job request (`whatson_id`, options, idempotency key) and the much larger versioned data contract that NPT needs to execute.