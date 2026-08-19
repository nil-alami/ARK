# ML SERVICE CARD
===============

Service name: Churn / Churnobyl  
Service ID/version: `churnobyl` 0.1.0; HTTP API v1; default model version 1  
Owner: TBD  
Implementation reviewed: [churnobyl.py](<C:/Users/AFE AI/PycharmProjects/select-family/engine/engine/churnobyl/churnobyl.py>), [churn.py](<C:/Users/AFE AI/PycharmProjects/select-family/engine/engine/churnobyl/churn.py>)

## Infrastructure classification

1. **Request-driven or proactive?**  
   Both API-triggered and scheduled, but not independently proactive. Full scoring is invoked through an API or by the host’s daily scheduler. The ML service does not discover churn and publish an event by itself.

2. **Stateless or stateful?**  
   Stateful. It depends on tenant-specific model artifacts, preprocessors, model registry records, previous churn history, and persisted customer-profile results.

3. **Synchronous or asynchronous?**  
   Currently synchronous from the caller’s perspective. FastAPI moves blocking work to a thread pool but waits for completion. Full-tenant scoring should architecturally be an asynchronous job.

4. **Online or batch-oriented?**  
   Primarily batch-oriented: all customers for one tenant are scored together. The new-transaction endpoint appears online, but currently reads and rewrites the tenant’s customer dataset, so it does not behave like a lightweight online operation.

5. **Raw or derived-data consumer?**  
   The active model consumes **derived churn features**. Raw transactions are processed by the shared upstream pipeline, outside the churn package.

---

## 1. PURPOSE

- Estimates customer inactivity or lapse risk as a `churn_score` between 0 and 100.
- Treats churn as a probability-like risk of being an inactivity-based churn candidate; it does not prove permanent customer loss.
- Produces a current score and maintains up to five historical score observations per customer.
- Supplies churn information to the combined Select customer profile stored in BCDP.
- The result can subsequently support campaign targeting, customer segmentation, retention actions, and personalized message generation.
- The service exists because transactional businesses cannot directly observe permanent churn; they need an operational approximation based on purchase inactivity and behavior.

The model learns the upstream binary label:

```text
customer inactivity > tenant churn window
    → churn candidate = 1
otherwise
    → churn candidate = 0
```

The resulting score is therefore best described as an **uncalibrated inactivity-risk score**, not a guaranteed probability that a customer will permanently churn.

---

## 2. TRIGGER / EXECUTION MODE

- **Scheduled batch:** The worker runs the complete pipeline and engine daily at process-local time `11:01`.
- **API-triggered batch:** `POST /api/v1/services/run/`.
- **Transaction-triggered update:** `POST /api/v1/services/new-transaction`.
- **Internal call:** `Churnobyl.do_churn_analysis_for_business(whatson_id, expanded)`.
- **Execution:** Blocking Python/Pandas/XGBoost work executed inside a FastAPI thread pool.
- **Caller semantics:** Synchronous; the HTTP request remains open until the pipeline and engine finish.
- **Tenant processing:** The daily worker processes tenants sequentially.
- **Proactive initiation:** Churnobyl itself cannot schedule work or publish discoveries. The external worker initiates scheduled executions.
- **Events emitted:** None.
- **Events consumed:** No broker event. The new-transaction HTTP endpoint acts as an event adapter.

---

## 3. INPUT CONTRACT

### Required API inputs

Full platform run:

```json
{
  "whatson_id": 123
}
```

| Field | Type | Validation |
|---|---:|---|
| `whatson_id` | integer | Required; no positive-range validation |

New transaction:

```json
{
  "whatson_id": 123,
  "phone": "customer-mobile",
  "transaction_id": 456
}
```

| Field | Type | Current use |
|---|---:|---|
| `whatson_id` | integer | Passed directly to BCDP as `business_id` |
| `phone` | string | Customer lookup key |
| `transaction_id` | integer | Required by schema but currently ignored |

### Required internal scoring inputs

`do_churn_analysis_for_business()` receives:

- `whatson_id: int`
- `expanded: pandas.DataFrame`

Minimum model-related DataFrame schema:

| Column | Type | Meaning |
|---|---|---|
| `business_id` | integer | Tenant identifier carried in customer rows |
| `mobile` | string | Customer identifier and prediction join key |
| `is_new_user` | boolean | Forces the final score to zero when true |
| `Churn.candidate` | numeric binary | Training target; currently also required during inference |
| `Churn.monetary_slope` | numeric | 180-day purchase-amount trend |
| `Churn.buy_cnt_30` | numeric/integer | Purchase count during the last 30 days |
| `Churn.buy_cnt_180` | numeric/integer | Purchase count during the last 180 days |
| `Churn.max_buy_amount` | numeric | Maximum historical absolute purchase amount |
| `Churn.min_buy_amount` | numeric | Minimum historical absolute purchase amount |
| `Churn.gap_ratio` | numeric | Most recent interpurchase gap divided by mean gap |
| `Churn.churn_window` | numeric/integer | Tenant-wide inactivity threshold in days |

### Optional internal inputs

- `selectData.Churn.churn_history`: previous history list from BCDP.
- Previous `Churn.churn_score`: accepted but removed before scoring.
- RFM, customer-state, persona, full name, and other customer-profile fields are passed through for later combined persistence; they are not churn-model features.

History format:

```json
[
  {
    "churn_score": 62.4,
    "date": "2026-08-11 11:30:00.123456"
  }
]
```

### Required datasets

These are separate from invocation inputs:

1. **Customer list**
   - `Phone`
   - registration time
   - customer name and identifiers

2. **Raw transaction history used upstream**
   - `AccountId` or customer ID
   - `TxDate`
   - `TotalAmount`

3. **Tenant identity mapping**
   - external `whatson_id`
   - internal Orbit business ID

4. **Model registry**
   - `select_model_files`
   - expected fields include `algorithm`, `version`, `has_preprocess`, and `file_uri`

5. **Previous BCDP profile data**
   - previous churn history
   - required by the new-transaction update path

6. **Model artifacts**
   - tenant-specific XGBoost model
   - optional `StandardScaler`

### Minimum data requirements

Implemented requirements:

- Input customer DataFrame must not be empty.
- All listed feature columns must exist.
- Model features must be numeric.
- `Churn.candidate` must exist even when using an already-trained model.
- The tenant must map to at least one internal business ID.
- New-transaction processing requires the phone to exist in BCDP and requires an appendable history value.
- The raw feature pipeline requires a non-empty transaction table with `AccountId`, `TxDate`, and `TotalAmount`.

Operationally recommended but not enforced:

- At least two purchases for enough customers to calculate meaningful purchase gaps.
- Both positive and negative churn-candidate examples for model training.
- Explicit minimum customer and transaction counts.
- A freshness limit for transactions and features.
- Unique `(tenant_id, customer_id)` rows.
- A fixed, versioned feature schema and feature order.

### Input schema/version

- HTTP envelope: API v1.
- Internal DataFrame: no formal schema version.
- Model feature schema: implicit and unversioned.
- Two tenant identifiers—`whatson_id` and internal `business_id`—are currently used inconsistently.

---

## 4. OUTPUT CONTRACT

### Primary internal output

`do_churn_analysis_for_business()` returns the original customer DataFrame with these churn additions:

| Field | Type | Meaning |
|---|---|---|
| `Churn.churn_score` | float or null | `predict_proba[:,1] × 100`, subject to overrides |
| `Churn.churn_history` | list | Previous and current score observations, limited to five |

Example:

```json
{
  "business_id": 123,
  "mobile": "customer-mobile",
  "Churn.churn_score": 72.43,
  "Churn.churn_history": [
    {
      "churn_score": 60.1,
      "date": "2026-08-10 11:01:00"
    },
    {
      "churn_score": 72.43,
      "date": "2026-08-11 11:01:00"
    }
  ]
}
```

All non-churn input columns are passed through.

### Persisted output

The combined engine repackages flattened fields into a shared BCDP document:

```json
{
  "business_id": 123,
  "mobile": "customer-mobile",
  "select_data": {
    "is_new_user": false,
    "customerState": {},
    "RFM": {},
    "Churn": {
      "candidate": 1,
      "monetary_slope": -10.76,
      "buy_cnt_30": 2,
      "buy_cnt_180": 8,
      "max_buy_amount": 812890,
      "min_buy_amount": 1690,
      "gap_ratio": 1.14,
      "churn_window": 45,
      "churn_score": 72.43,
      "churn_history": []
    },
    "persona": {}
  }
}
```

BCDP writes are divided into batches of 1,000 records.

### Scores/confidence

- `churn_score = XGBoost positive-class probability × 100`.
- Expected numerical range is 0–100.
- No explicit rounding or clipping is performed.
- No confidence interval, uncertainty measure, calibration status, explanation, or reason code is returned.
- A newly trained model scores the same data on which it was trained, so those scores are in-sample.
- Model version and feature version are not included with predictions.

Hard-coded overrides:

- `is_new_user == true` → score `0`.
- Existing customer with a missing prediction → score `100`.

These are business/fallback rules, not model outputs.

### HTTP response schema

Both endpoints return:

```json
{
  "status": 1,
  "message": "human-readable message",
  "content": {
    "whatson_id": 123,
    "msg": "execution detail"
  }
}
```

Current status values:

- `1`: success
- `2`: unhandled failure

Both success and handled failure responses use HTTP 200. FastAPI schema validation failures can return HTTP 422.

### Possible statuses

- **SUCCESS:** Represented by application status `1`.
- **FAILED:** Represented by application status `2`.
- **PARTIAL:** Not represented.
- **NOT_ELIGIBLE:** Not represented.

Important gaps:

- The API does not return customer scores or a result location.
- A BCDP write failure can be ignored by the overall engine and still be reported as success.
- An empty prediction set can return unchanged customer data without an explicit partial or not-eligible status.
- A zero score is incorrectly stored as `null` in churn history because the history conversion treats zero as false.

---

## 5. HIGH-LEVEL WORKFLOW

```text
Raw customers and transactions
  ↓
Upstream shared feature pipeline
  ├─ calculate tenant churn window
  ├─ create candidate label
  ├─ calculate monetary slope
  ├─ calculate 30/180-day counts
  ├─ calculate max/min amount
  └─ calculate gap ratio
  ↓
Expanded customer/CDP DataFrame
  ↓
Select Churn.* fields, business_id and mobile
  ↓
Fill missing count/slope values with zero
  ↓
Resolve external whatson_id to internal business ID
  ↓
Read tenant model metadata
  ↓
Model exists?
  ├─ Yes: download and load model/preprocessor
  └─ No: fit StandardScaler and train XGBoost on current batch
  ↓
predict_proba × 100
  ↓
Keep one prediction per business_id/mobile
  ↓
Merge prediction into customer data by mobile
  ↓
Apply overrides
  ├─ new customer → 0
  └─ missing old-customer prediction → 100
  ↓
Append churn history and keep latest five entries
  ↓
Merge with RFM and calculate CLV
  ↓
Write combined select_data document to BCDP
  ↓
Update BusinessSettings.ProcessStatus
```

A separate new-transaction workflow performs:

```text
HTTP request
  ↓
Read all tenant BCDP customer pages
  ↓
Find customer by phone
  ↓
Set current churn score to 0
  ↓
Append history entry and keep latest five
  ↓
Rewrite the tenant customer-profile dataset to BCDP
  ↓
Return Boolean-derived API status
```

---

## 6. ELIGIBILITY / PRECONDITIONS

- Tenant must exist in the business identity mapping.
- Customer and transaction data must be available upstream.
- Required churn feature columns must exist.
- Customer keys must be usable for joining model output back to customer data.
- Feature values must be accepted by `StandardScaler` and XGBoost.
- Existing models must match the current feature count and order.
- Model storage and registry configuration must be available.
- BCDP must be reachable if results are to be persisted.
- The new-transaction customer must already exist in the fetched BCDP records.
- No entitlement or tenant-feature flag is checked.
- No explicit minimum history, row count, class balance, freshness, or data-quality threshold is enforced.
- New customers are considered eligible but receive a forced score of zero; there is no distinct `INSUFFICIENT_HISTORY` status.

---

## 7. DEPENDENCIES

### Internal

- Shared pipeline and Bumblebee feature calculator.
- `ChurnModelHandler`.
- `DataFetcher`.
- `PostgresqlCRUD`.
- `QueryRunner`.
- `DBEngines`.
- Combined engine orchestration with Shepherd/RFM and CLV.
- FastAPI runner and daily worker.
- Shared logger configuration.

### External

- Orbit PostgreSQL or MSSQL database.
- Badger customer/transaction source through the shared pipeline.
- BCDP customer-profile service through `BusinessCdpClient`.
- S3-compatible model artifact storage through Boto3.
- Local filesystem for temporary and newly saved model artifacts.

### Data

- Customer master data.
- Raw purchase transactions.
- Derived churn feature DataFrame.
- Business identity mapping.
- Existing BCDP churn history.
- `select_model_files` model registry.
- `BusinessSettings` process state.

### Model/artifact

- `XGBClassifier` with binary logistic objective.
- `StandardScaler`.
- Joblib model/preprocessor files.
- Tenant-specific artifact naming such as:

```text
xgboost_{business_id}_v1.joblib
```

### Libraries

- Pandas
- NumPy
- XGBoost
- scikit-learn
- Joblib
- SQLAlchemy
- Boto3/Botocore
- FastAPI
- Protobuf/BCDP client library

Several of these are imported by the service but are not declared in the current `pyproject.toml`, creating a packaging/reproducibility risk.

---

## 8. STATE & STORAGE

### Reads

- Orbit business identity records.
- `select_model_files`.
- Tenant model and preprocessor artifacts.
- BCDP customer documents and prior churn histories.
- Raw transactions and customer data indirectly through the pipeline.

### Writes

- BCDP `select_data`, including churn, RFM, persona, and customer-state sections.
- Model metadata to `select_model_files`.
- Model/preprocessor artifacts to local storage and/or S3.
- `BusinessSettings.ProcessStatus`.
- Rotating churn and worker logs.

An unused method can upsert into a physical `churn` table, but it is not part of the active execution path.

### Persistent state

- Tenant-specific trained models.
- Scalers.
- Model registry entries.
- Latest churn score.
- Last five churn-history entries.
- Overall platform process status.

### Cache

- No explicit inference cache.
- Loaded models are not held in a durable shared cache across service instances.
- Downloaded artifacts are usually deleted after loading.
- A newly trained model may remain on local disk because its S3 upload path is commented out.

### Intermediate artifacts

- Multiple tenant-wide Pandas DataFrames.
- Scaled feature arrays.
- Temporary Joblib files.
- In-memory fitted model and scaler.
- Per-instance mutable fields such as `self.df`, `self.response`, and `self.df_scaled`.

The service is therefore operationally stateful even though individual score calculations resemble input-to-output computation.

---

## 9. EXECUTION PROFILE

Typical runtime: **TBD; no reliable benchmark or service-level objective is defined.**

Expected dataset size:

- One complete tenant customer population per run.
- Complete transaction history is loaded upstream.
- The bundled sample churn dataset contains 39,393 rows, but it is not a declared production scale limit.

CPU:

- CPU-oriented Pandas, scikit-learn, and default XGBoost execution.
- XGBoost configuration uses 300 trees and can consume multiple CPU threads.

RAM:

- Proportional to transaction and customer counts.
- Multiple DataFrame copies, merges, normalization operations, and row-wise transformations increase peak memory.
- No memory guardrail is implemented.

GPU:

- Not required or configured.
- No GPU-specific XGBoost tree method is selected.

Parallelizable:

- Customers and tenants are theoretically parallelizable.
- BCDP writes are chunked.
- The current daily worker processes tenants sequentially.
- Concurrent model training requires isolation of model paths and registry writes.

Batch size:

- Scoring: entire tenant population.
- BCDP persistence: 1,000 customer records per write batch.
- BCDP reads: paginated, default page size 10,000; new-transaction path requests pages of 1,000.

Timeout considerations:

- BCDP client default timeout: 5 seconds per operation.
- No overall model-training or tenant-run timeout.
- No HTTP job timeout defined in service code.
- Long full-tenant runs hold the API request open.
- The new-transaction path scans and rewrites tenant data, so its runtime grows with tenant size.

Recommended execution pattern:

- Full-tenant scoring and bootstrap training: asynchronous batch jobs.
- Single-customer transaction response: synchronous only after redesigning it to avoid full-tenant reads/writes.
- Training and inference should be separate job types.

---

## 10. CONFIGURATION

Current effective configuration:

- XGBoost objective: `binary:logistic`
- Evaluation metric: `logloss`
- Estimators: `300`
- Maximum depth: `5`
- Learning rate: `0.05`
- Recent purchase windows: `30` and `180` days
- Monetary slope window: `180` days
- Gap-ratio window: `180` days
- Churn-window multiplier `k`: `2.0`
- History retention: latest `5` scores
- BCDP write batch: `1,000`
- Model version default: `1`
- Scheduled execution: daily at `11:01`
- Tenant worker retries: default `3`
- Retry base delay: default `5` seconds with jitter
- BCDP timeout: `5` seconds
- Model storage configuration:
  - `MODELS_STORAGE`
  - `MODEL_ENDPOINT_URL`
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `BUCKET`
- BCDP configuration:
  - `CDP_DB_HOST`
  - `CDP_DB_PORT`
  - `CDP_API_KEY`

Configuration issues:

- No `random_state`, class weighting, validation split, calibration, or early stopping.
- Model download uses a hard-coded bucket named `whatsondev` rather than the configured bucket.
- Model version selection is not deterministic: the registry query has no active-model filter or ordering, and the first returned row is used.
- Schedule is hard-coded rather than tenant-configurable.
- No tenant-specific threshold, feature-window, or model-version policy is exposed.
- A separate `compute_churn_threshold()` utility has KM/quantile settings, but it is not connected to the active production feature flow.

---

## 11. FAILURE / FALLBACK

### Possible failures

- Missing or empty customer/transaction data.
- Missing required DataFrame columns.
- Missing tenant mapping, causing access to `business_id[0]` to fail.
- Non-numeric or non-finite features.
- Feature order/count mismatch with an existing model.
- Single-class or insufficient training data.
- Database connection or query failures.
- Model registry inconsistency.
- S3 download/upload failure.
- Missing local model directories.
- BCDP timeout or partial bulk-write failure.
- Phone not found during a new-transaction request.
- Missing/null churn history during append.
- Duplicate mobile numbers causing incorrect or multiplied joins.
- API requests timing out during full batch execution.

### Retryable?

- The daily worker retries tenant runs up to `SELECT_MAX_RETRIES`, default 3.
- It retries unexpected failures with exponential delay and jitter.
- Missing `Phone` data is treated as a non-retryable skip.
- A scheduler-level database/connectivity failure may be retried every 60 seconds; zero maximum retries means unlimited retries.
- The API path itself does not retry.
- BCDP batch writes have no per-batch retry.

### Fallback

- Missing saved model → train a new XGBoost model during the scoring request.
- New customer → score 0.
- Existing customer with missing prediction → score 100.
- Missing `buy_cnt_30`, `buy_cnt_180`, or `monetary_slope` → fill with zero.
- Existing history absent or NaN → treated as an empty list during batch history merge.

### Partial-result behavior

- BCDP batches committed before a later failure remain committed.
- `load_to_bcdp()` returns only `False`; it does not report successful or failed row counts.
- The engine ignores that Boolean and can mark the overall process complete.
- No `PARTIAL` result is exposed.
- Empty prediction results may return unchanged input data.
- Failure to save a newly trained model does not necessarily prevent predictions from being returned.

### Significant correctness risks

- Saved scalers are refitted to each inference batch instead of using `transform()`, creating batch-dependent scores.
- Initial model training and scoring use the same rows, producing in-sample probabilities.
- Inference unnecessarily requires the known target `Churn.candidate`.
- Technical missing predictions are converted to maximum risk.
- Zero is converted to `null` in score history.
- Predictions are merged only by `mobile`, not `(tenant, customer)`.
- New-transaction requests are not idempotent and can append duplicate history entries.
- Model upload is disabled in one save path, while later loading expects the artifact in S3.

---

## 12. INTEGRATION

### API

Full run:

```http
POST /api/v1/services/run/
Content-Type: application/json

{"whatson_id": 123}
```

New transaction:

```http
POST /api/v1/services/new-transaction
Content-Type: application/json

{
  "whatson_id": 123,
  "phone": "customer-mobile",
  "transaction_id": 456
}
```

There is no churn-only batch-scoring API. `/run/` runs the shared pipeline, churn, RFM, CLV, and persistence workflow.

### Events emitted

- None.

### Events consumed

- None through a broker.
- A new transaction is accepted through HTTP, but `transaction_id` is not used or recorded.

### Job type

- Scheduled full-platform tenant batch.
- Request-triggered full-platform tenant batch.
- Transaction-triggered customer score reset.
- Implicit model-training job when no model exists.

### Result retrieval

- No job ID.
- No polling endpoint.
- No result URI.
- No customer-score payload.
- Consumers must read persisted BCDP data separately.

### Idempotency

- No idempotency key or execution ID.
- Repeating a batch appends another churn-history observation.
- Repeating a transaction request appends another zero-score observation.
- `transaction_id` is not checked for duplicates.
- Concurrent missing-model requests can train and register duplicate model version 1 artifacts.

### Versioning

- URL version: `/api/v1`.
- Package version: `0.1.0`.
- Model version: defaults to integer `1`.
- Feature schema is unversioned.
- Output schema is unversioned.
- Predictions do not identify their model or feature version.

### Security

- An HTTP bearer object is declared in the runner module, but neither churn-related endpoint applies it. Authentication and tenant authorization are therefore not enforced by these route declarations.

---

## 13. OBSERVABILITY

### Currently available

- Churn logger at DEBUG level.
- Console output.
- Rotating `logs/churnobyl.log`, approximately 1 MB with three backups.
- Daily worker logs tenant start, retry, success/failure, and total tenant runtime.
- Pipeline and engine print total execution duration.
- No churn-specific metrics endpoint.
- No structured prediction/run audit record.

### Required operational metrics

- `churn_runs_total{status,trigger,tenant}`
- `churn_run_duration_seconds`
- `churn_queue_time_seconds`
- `churn_customers_scored_total`
- `churn_customers_not_eligible_total`
- `churn_partial_runs_total`
- `churn_model_load_duration_seconds`
- `churn_model_training_duration_seconds`
- `churn_bcdp_write_duration_seconds`
- `churn_bcdp_failed_batches_total`
- `churn_retry_total`
- `churn_active_jobs`
- `churn_transaction_reset_latency_seconds`

### Required data metrics

- Input customer count.
- Transaction count.
- Customers without transactions.
- Duplicate mobile/customer-key count.
- Missingness by feature.
- Non-finite and out-of-range feature counts.
- Feature freshness and source maximum timestamp.
- Positive-label rate.
- Customers with insufficient repeat-purchase history.
- Prediction coverage rate.
- Join-match and unmatched-prediction counts.
- History parsing failures.

### Required ML metrics

- Active model ID and version.
- Feature-schema version.
- Training-data interval.
- Training row/customer counts.
- Class balance.
- Holdout ROC-AUC, PR-AUC, log loss, Brier score, precision/recall at operational thresholds.
- Calibration metrics.
- Score distribution by tenant.
- Fraction of forced scores: new-customer zero and missing-prediction 100.
- Population and feature drift.
- Prediction stability across runs.
- Model age and artifact-load failures.

### Required structured log context

Every log should include:

- `run_id`
- `tenant_id`
- `trigger`
- `model_id`
- `model_version`
- `feature_schema_version`
- `customer_count`
- `status`
- `duration_ms`
- `failed_stage`
- `retry_attempt`

Phone numbers and other customer identifiers should be redacted or hashed.

---

## 14. OWNERSHIP / ISOLATION

### Owns

The churn service should exclusively own:

- Churn eligibility rules.
- Churn-window policy.
- Churn feature schema.
- Model training and inference.
- Churn model versions and artifacts.
- Churn predictions.
- Churn prediction history.
- Churn-specific thresholds and configuration.
- Churn training/evaluation records.
- Churn result events and public contracts.

### May access

Through explicit, versioned interfaces:

- Canonical tenant and customer identifiers.
- A shared transaction/activity data product.
- A shared feature platform, if churn features are externally produced.
- Churn-owned model registry and artifact namespace.
- Churn-owned prediction storage.
- Platform event publisher.
- Customer-profile projection interface.

### Must NOT directly access

- RFM-owned state or tables.
- Persona-owned state or tables.
- Customer-state-owned data except through an approved input contract.
- Full shared BCDP documents.
- Generic shared database tables through unrestricted CRUD.
- Another service’s model registry records or artifact directories.
- Other services’ private feature tables.
- Raw Orbit/Badger schemas unless churn explicitly owns that ingestion boundary.
- Tenant identity mapping tables when a canonical tenant ID can be supplied by the caller.

### Current ownership violations

The current implementation:

- Reads and writes complete shared BCDP customer documents.
- Reconstructs RFM, persona, and customer-state sections.
- Writes shared `BusinessSettings`.
- Uses the shared `select_model_files` registry.
- Inherits churn model handling from the clustering model handler.
- Imports clustering and other ML-service types through that shared handler.
- Uses shared S3/filesystem namespaces.
- Depends on externally constructed `Churn.*` fields without a formal data-product contract.

### Recommended isolation boundary

```text
Shared transaction/feature platform
  → versioned ChurnFeatureBatch
  → Churn service
  → churn-owned predictions and history
  → ChurnScoresCalculated event
  → external customer-profile projector
  → BCDP
```

The churn service should publish only churn results. A separate integration component should merge those results into BCDP, preventing churn from overwriting data owned by RFM, persona, or customer-state services.