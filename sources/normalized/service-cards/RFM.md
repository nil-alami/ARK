# ML SERVICE CARD
===============

Service name: RFM Customer Segmentation / Shepherd  
Service ID/version: `shepherd` 0.1.0; HTTP API v1; default model version 1  
Owner: TBD  
Implementation reviewed: [shepherd.py](<C:/Users/AFE AI/PycharmProjects/select-family/engine/engine/shepherd/shepherd.py>), [clustrator.py](<C:/Users/AFE AI/PycharmProjects/select-family/engine/engine/shepherd/clustrator.py>)

## Infrastructure classification

1. **Request-driven or proactive?**  
   API-triggered and scheduled, but not independently proactive. Shepherd does not discover segments and publish events itself; the platform invokes it.

2. **Stateless or stateful?**  
   Stateful. It relies on tenant-specific K-Means models, preprocessing artifacts, model-registry records, current semantic label mappings, and historical customer segments.

3. **Synchronous or asynchronous?**  
   Currently synchronous from the caller’s perspective. Full processing runs in a thread pool but the HTTP request waits. It should be an asynchronous job at production scale.

4. **Online or batch-oriented?**  
   Batch-oriented. It clusters the complete eligible customer population for one tenant.

5. **Raw or derived-data consumer?**  
   The active Shepherd model consumes the derived features `recency`, `frequency`, and `monetary`. Raw transaction aggregation occurs in the shared upstream pipeline.

---

## 1. PURPOSE

- Groups a tenant’s customers into five behaviorally distinct segments using RFM:
  - **Recency:** days since the most recent transaction.
  - **Frequency:** total transaction count.
  - **Monetary:** total transaction amount.
- Converts arbitrary K-Means cluster numbers into business-facing semantic segments.
- Maintains up to five historical segment observations per customer.
- Supplies segment information to the shared BCDP customer profile.
- Supports downstream campaign selection, message personalization, retention strategies, customer analysis, and agent prompt generation.
- Provides stable external enum meanings even though raw K-Means cluster numbers are arbitrary.

Current semantic enums:

| Enum | Segment | Intended meaning |
|---:|---|---|
| `0` | Champions | Best-ranked RFM cluster |
| `1` | Loyal | Second-ranked cluster |
| `2` | Adventurous | Middle-ranked cluster |
| `3` | Hopeless | Fourth-ranked cluster |
| `4` | Ghost | Lowest-ranked cluster |

These labels are relative rankings within a tenant’s current customer population, not universal absolute customer categories.

---

## 2. TRIGGER / EXECUTION MODE

- **Scheduled batch:** The platform worker runs the full pipeline and engine daily at process-local time `11:01`.
- **API-triggered batch:** `POST /api/v1/services/run/`.
- **Internal invocation:** `Shepherd.do_RFM_clustering_for_business(whatson_id, business_data)`.
- **Execution:** Blocking Pandas/scikit-learn work executed in a FastAPI thread pool.
- **Caller semantics:** Synchronous; the HTTP request stays open until all pipeline and engine work completes.
- **Tenant processing:** The daily worker processes tenant/business pairs sequentially.
- **Proactive initiation:** Shepherd cannot initiate runs or publish discoveries independently.
- **Events emitted:** None.
- **Events consumed:** None through an event broker.
- **Standalone RFM mode:** Intended internal `type_='r'` and `do_RFM_clustering_for_all()` paths exist but currently omit required method arguments and are not operational.

---

## 3. INPUT CONTRACT

### Required API input

The only active external trigger is the full Select run:

```json
{
  "whatson_id": 123
}
```

| Field | Type | Validation |
|---|---:|---|
| `whatson_id` | integer | Required; no positive-range or entitlement validation |

There is no RFM-only HTTP endpoint.

### Required internal scoring inputs

```python
do_RFM_clustering_for_business(
    whatson_id: int,
    business_data: pandas.DataFrame
)
```

Required clustering columns:

| Column | Type | Meaning |
|---|---|---|
| `RFM.recency` | numeric | Days since the customer’s latest transaction |
| `RFM.frequency` | numeric/integer | Number of transactions |
| `RFM.monetary` | numeric | Sum of transaction amounts |
| `mobile` | string | Customer key used to associate results |
| `business_id` | integer | Tenant identifier carried in each row |

Optional input:

| Column | Type | Meaning |
|---|---|---|
| `selectData.RFM.cluster_history` | list | Previous segment history loaded from BCDP |

Other fields—including churn, customer state, persona, name, and transaction timestamps—are passed through the platform but are not K-Means features.

### Upstream RFM feature definitions

The current upstream query calculates:

```sql
MAX("At")                                     AS last_transaction
MIN("At")                                     AS first_transaction
EXTRACT(DAY FROM NOW() - MAX("At"))           AS recency
COUNT(*)                                      AS frequency
SUM("Amount")                                 AS monetary
```

The query groups by customer phone and filters by:

- Requested phone batch.
- Tenant/`WhatsonId`.

It does not explicitly filter transaction status, source type, refund state, currency, or negative amounts.

### Required datasets

These are separate from API inputs:

1. **Customer population**
   - Phone
   - registration time
   - name
   - tenant/Whatson identifier

2. **Raw transaction data used upstream**
   - Phone/customer identifier
   - transaction timestamp
   - amount
   - tenant identifier

3. **Tenant identity mapping**
   - external `whatson_id`
   - internal Orbit business ID

4. **Model registry**
   - `select_model_files`
   - expected fields include `id`, `business_id`, `action`, `algorithm`, `file_uri`, `is_active`, `has_preprocess`, and `version`

5. **Previous customer-profile data**
   - `selectData.RFM.cluster_history`

6. **Model artifacts**
   - tenant-specific K-Means model
   - `StandardScaler`
   - optional PCA transformer

7. **Tagging configuration**
   - industry group definitions
   - industry-specific R/F/M weights
   - semantic label order

### Minimum data requirements

Implemented:

- `business_data` must not be empty.
- All three RFM feature columns must exist.
- At least five customer rows are required because K-Means uses five clusters.
- Tenant mapping must return at least one internal business ID.
- Features must be compatible with `StandardScaler` and K-Means.
- Existing model and preprocessor dimensions must match the current three-feature contract.
- Each returned cluster must map to one of the five semantic labels.

Recommended but not enforced:

- Significantly more than five customers; exactly five produces five one-customer clusters.
- No missing or infinite feature values.
- Unique `(tenant_id, customer_id)` rows.
- A defined observation window.
- Common monetary currency/unit.
- Explicit treatment of refunds, cancellations, and negative transactions.
- Minimum transaction history per customer.
- Minimum and maximum cluster size policies.
- Feature freshness and transaction cutoff validation.

### Input schema/version

- HTTP contract: API v1.
- Internal DataFrame: unversioned.
- RFM feature definition: unversioned.
- Feature order is implicit: `recency`, `frequency`, `monetary`.
- Tenant identifiers are inconsistent: upstream rows use `whatson_id` as `business_id`, while model storage uses an internally mapped business ID.

---

## 4. OUTPUT CONTRACT

### Primary internal output

For an eligible tenant, `do_RFM_clustering_for_business()` returns a DataFrame with:

| Field | Type | Meaning |
|---|---|---|
| `mobile` | string | Customer identifier |
| `business_id` | integer | Tenant identifier from the input |
| `RFM.enum` | integer 0–4 | Semantic RFM segment |
| `RFM.cluster_history` | list | Previous and current segments, limited to five |

Example:

```json
{
  "mobile": "customer-mobile",
  "business_id": 123,
  "RFM.enum": 1,
  "RFM.cluster_history": [
    {
      "enum": 2,
      "date": "2026-08-10 11:01:00"
    },
    {
      "enum": 1,
      "date": "2026-08-11 11:01:00"
    }
  ]
}
```

The following are not returned:

- Raw K-Means cluster number.
- Semantic label text.
- Model ID/version.
- Cluster distance.
- Confidence or membership probability.
- Cluster centroid.
- Explanation or reason codes.
- Feature-schema version.

### Persisted output

The combined engine merges RFM results with the full customer record and persists a BCDP structure similar to:

```json
{
  "business_id": 123,
  "mobile": "customer-mobile",
  "select_data": {
    "is_new_user": false,
    "customerState": {},
    "RFM": {
      "recency": 12,
      "frequency": 8,
      "monetary": 2500000,
      "first_transaction": "2025-01-10",
      "last_transaction": "2026-07-30",
      "enum": 1,
      "cluster_history": [
        {
          "enum": 1,
          "date": "2026-08-11 11:01:00"
        }
      ]
    },
    "Churn": {},
    "persona": {}
  }
}
```

The active combined persistence writer divides updates into batches of 1,000 customers.

### Scores/confidence

- No confidence is produced.
- Standard K-Means assigns each customer to the nearest centroid.
- Distance to the assigned centroid is not exposed.
- Semantic enums are calculated by ranking cluster-level RFM profiles, not directly by K-Means.
- `0` is intended to represent the best segment and `4` the worst.

Important semantic issue:

- Shepherd passes names such as `RFM.recency` to a label resolver that recognizes only `recency`, `frequency`, and `monetary`.
- Consequently, configured industry weights are not applied.
- The system falls back to equal weights.
- Recency is not inverted as “lower is better.”
- Higher recency can therefore improve a cluster’s rank, potentially reversing the intended segment meanings.

### Possible return statuses

The internal method currently returns inconsistent types:

- Eligible execution: result DataFrame.
- Empty data: `False`.
- Missing required features: `False`.
- Fewer than five customers: `True`.
- Model acquisition/save failure: `False`.

The combined engine expects a DataFrame and calls `.drop()` before safely checking these Boolean values. Therefore, the Boolean not-eligible/failure paths can make the overall run fail.

Requested status mapping:

- **SUCCESS:** DataFrame produced and persisted.
- **PARTIAL:** Not represented.
- **FAILED:** Boolean `False` internally or application status `2` externally.
- **NOT_ELIGIBLE:** Fewer than five rows should mean not eligible, but currently returns `True` and has no formal status.

### HTTP output

```json
{
  "status": 1,
  "message": "human-readable message",
  "content": {
    "whatson_id": 123,
    "msg": "engine & pipeline both successfull!"
  }
}
```

Current application statuses:

- `1`: Success
- `2`: Unhandled failure

The endpoint returns HTTP 200 for both handled success and failure. FastAPI validation errors can return HTTP 422.

The API does not expose RFM results or a result-retrieval location.

---

## 5. HIGH-LEVEL WORKFLOW

```text
Customer and transaction data
  ↓
Upstream RFM aggregation
  ├─ recency = now - latest transaction
  ├─ frequency = transaction count
  └─ monetary = transaction amount sum
  ↓
Expanded customer DataFrame
  ↓
Validate RFM.recency, RFM.frequency, RFM.monetary
  ↓
Require at least five customers
  ↓
Resolve external whatson_id to internal business ID
  ↓
Read active tenant clustering-model metadata
  ↓
Existing model?
  ├─ Yes
  │   ├─ download K-Means model
  │   ├─ download scaler/PCA if available
  │   └─ predict raw cluster number
  └─ No
      ├─ fit StandardScaler
      ├─ optionally fit two-component PCA
      ├─ train five-cluster K-Means
      ├─ save preprocessors
      ├─ save model and registry record
      └─ return training-batch cluster assignments
  ↓
Calculate mean RFM values for each raw cluster
  ↓
TagWise ranks clusters
  ├─ intended: weighted RFM score
  └─ current: effectively equal weighting, with recency direction bug
  ↓
Assign semantic names
  ↓
Map semantic names to stable enums 0–4
  ↓
Append current enum to history
  ↓
Keep latest five history entries
  ↓
Return per-customer result
  ↓
Combined engine merges RFM result with churn output
  ↓
Calculate CLV
  ↓
Write combined customer profile to BCDP
```

The semantic labels are recalculated from the current scoring population on each run. They are not loaded as an immutable model-version artifact.

---

## 6. ELIGIBILITY / PRECONDITIONS

- Tenant must be present in the Orbit identity mapping.
- Customer population and RFM aggregation must be available.
- At least five customer rows must be supplied.
- Required RFM fields must exist.
- RFM fields must be numeric and usable by scikit-learn.
- Existing model artifacts must be compatible with the current features and preprocessing.
- All five clusters must be labelable.
- Model registry and artifact storage must be reachable if training or loading is required.
- BCDP must be reachable for persistence.
- No tenant entitlement or RFM-enabled flag is checked.
- No explicit feature freshness, observation-window, minimum-transaction, or data-coverage policy exists.
- Customers with missing upstream RFM records receive null RFM fields in the integrated dataset rather than a formal not-eligible status.
- New customers are not separated from mature customers before clustering.

---

## 7. DEPENDENCIES

### Internal

- Shared pipeline and Badger data handlers.
- `ClusteringModelHandler`.
- `KMeansClusterator`.
- `TagWise`.
- `WeightProcessor`.
- `DataFetcher`.
- `PostgresqlCRUD`.
- `QueryRunner`.
- `DBEngines`.
- Combined engine orchestration.
- Churn service’s combined BCDP writer.
- CLV calculation inside Shepherd.
- Daily worker and FastAPI runner.

### External

- Badger PostgreSQL transaction data.
- Orbit PostgreSQL or MSSQL.
- BCDP customer-profile service.
- S3-compatible model artifact storage.
- Local model filesystem.

### Data

- Customer master list.
- Raw transaction data.
- Derived RFM feature batch.
- Business identity mapping.
- Previous RFM histories.
- `select_model_files`.
- `BusinessSettings`.
- Industry weights YAML.

### Model/artifact

- Five-cluster K-Means.
- StandardScaler.
- Optional two-component PCA.
- Semantic cluster ranking configuration.
- Tenant-specific Joblib artifacts.

### Libraries

- Pandas
- NumPy
- scikit-learn
- Joblib
- SQLAlchemy
- Boto3/Botocore
- PyYAML
- FastAPI
- Python dotenv

Several runtime libraries used here are not declared in the project’s main dependency list, which is a deployment reproducibility risk.

---

## 8. STATE & STORAGE

### Reads

- Raw customer and transaction data through the upstream pipeline.
- Orbit tenant identity data.
- `select_model_files`.
- K-Means/scaler/PCA artifacts.
- Previous `selectData.RFM.cluster_history` from BCDP.
- Industry weight configuration.

### Writes

Active combined flow:

- Updated RFM enum/history to BCDP.
- Full combined `select_data` profile to BCDP.
- Model metadata to `select_model_files`.
- Model/preprocessor artifacts to local storage and/or S3.
- `BusinessSettings.ProcessStatus` through engine orchestration.
- Shepherd and worker logs.

Dormant/commented paths:

- `rfm_cluster_labels` persistence.
- Direct Shepherd BCDP writer.
- `rfm` and `rfm_staging` tables exist in pipeline infrastructure but are not used by the active Shepherd scoring path.

### Persistent state

- Tenant K-Means model.
- StandardScaler.
- Optional PCA.
- Model registry record.
- Current customer segment.
- Last five segment-history entries.

### Cache

- No explicit model cache across requests.
- Models are downloaded and loaded for executions.
- Downloaded artifacts are normally removed after loading.
- Newly trained model files may remain locally because model upload is commented out.

### Intermediate artifacts

- Tenant-wide customer DataFrame.
- Three-feature RFM DataFrame.
- Scaled numeric array.
- Optional PCA matrix.
- Raw cluster assignments.
- Cluster profiles and semantic label map.
- Temporary Joblib files.

### Statefulness considerations

- Segment history and model artifacts make the service stateful.
- Semantic label assignment depends on the current population, so identical raw cluster IDs can receive different meanings across runs.
- Multiple simultaneous training runs for the same tenant can compete to create model version 1.

---

## 9. EXECUTION PROFILE

Typical runtime: **TBD; no RFM-specific benchmark or SLO is defined.**

Expected dataset size:

- Entire eligible customer population for one tenant.
- Upstream RFM queries process phone lists in batches of 2,000.
- Clustering itself receives the full tenant customer matrix.

CPU:

- CPU-bound StandardScaler, optional PCA, and K-Means.
- Complexity is approximately proportional to customers × five clusters × iterations × initializations.
- Only three primary numeric features are used.

RAM:

- Entire tenant data, feature matrix, normalized data, and merge results are held in memory.
- Multiple DataFrame copies increase peak memory.

GPU:

- Not required or supported by the active implementation.

Parallelizable:

- Tenant runs are independently parallelizable.
- Current scheduler processes tenants sequentially.
- K-Means uses scikit-learn’s internal implementation.
- Customer aggregation batches can be fetched independently, though current code processes them sequentially.

Current batch sizes:

- Upstream RFM query: 2,000 phone numbers.
- BCDP writes in the combined engine: 1,000 customer records.
- K-Means: complete tenant population.

Timeout considerations:

- BCDP client timeout: 5 seconds per operation.
- No tenant-level clustering timeout.
- No HTTP job timeout.
- No artifact-store timeout policy in Shepherd.
- API requests remain open during upstream aggregation, churn, RFM, CLV, and persistence.

Recommended deployment profile:

- CPU worker process.
- No GPU pool.
- Asynchronous tenant-level jobs.
- Configured customer-count and memory limits.
- Separate training/retraining and inference job types.

---

## 10. CONFIGURATION

### K-Means

- Number of clusters: `5`
- Initialization: `k-means++`
- `n_init`: `auto`
- Maximum iterations: `300`
- Random seed: `42`
- Algorithm: effectively scikit-learn default `lloyd`
- Feature scaler: `StandardScaler`

### PCA

- Components: `2`
- Enabled for new models only when maximum tenant monetary value equals zero.
- This activation condition is not a meaningful PCA eligibility rule and should be redesigned.

### Semantic labels

Ordered best to worst:

```text
Champions
Loyal
Adventurous
Hopeless
Ghost
```

Stable enum mapping:

```text
Champions   → 0
Loyal       → 1
Adventurous → 2
Hopeless    → 3
Ghost       → 4
```

### Industry weighting

- Configured groups: `0–21` and `99`.
- Shepherd always passes industry group `99`.
- Intended group 99 weights:
  - Recency: `0.30`
  - Frequency: `0.30`
  - Monetary: `0.40`
- Due to feature-name alias mismatch, these weights are currently replaced with equal weighting.
- Recency is intended to be lower-is-better, but current prefixed field names prevent inversion.

### Operational

- Minimum rows: `5`
- Segment-history retention: `5`
- Model version default: `1`
- Schedule: daily `11:01`
- Tenant retries: default `3`
- Retry base delay: default `5` seconds plus jitter
- RFM query phone batch: `2,000`
- BCDP write batch: `1,000`
- Customer source filter start: `2018-01-01`
- Model/artifact configuration:
  - `MODELS_STORAGE`
  - `MODEL_ENDPOINT_URL`
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `BUCKET`

Missing configuration:

- Tenant-specific cluster count.
- Observation window.
- Transaction eligibility rules.
- Currency normalization.
- Outlier treatment.
- Log transforms.
- Minimum cluster size.
- Retraining schedule.
- Active model selection policy.
- Model/feature schema compatibility policy.
- Industry group resolution from tenant metadata.

---

## 11. FAILURE / FALLBACK

### Possible failures

- No customer data.
- Missing one or more RFM columns.
- Fewer than five customer rows.
- Missing or null RFM features.
- Empty tenant identity mapping.
- K-Means failure due to invalid data.
- Model-feature dimension mismatch.
- Missing scaler or PCA.
- Model registry returns an inactive or incorrect row.
- S3/local artifact failure.
- TagWise configuration or label mapping failure.
- Unmapped semantic labels producing null enums.
- Duplicate mobile numbers producing incorrect merges or duplicate history.
- BCDP persistence failure.
- API timeout during a full run.

### Retryable?

- Daily tenant executions retry up to three times by default.
- Unexpected failures use exponential backoff plus jitter.
- Missing `Phone` data and explicitly detected empty data are skipped without retry.
- Scheduler-level database/connectivity failures can retry every 60 seconds.
- API-triggered executions do not retry.
- BCDP writes do not have per-batch retry logic.

### Fallback

- Missing active model → train a new five-cluster K-Means model on the current scoring batch.
- Missing configured feature weights → TagWise falls back to equal weights.
- All-zero features in TagWise → clusters are ordered by raw cluster key and assigned labels sequentially.
- Missing previous history → start a new history list.
- All-zero monetary maximum → enable PCA.
- Missing model preprocessor can cause a new scaler to be fitted on the inference batch, although this is not a safe fallback for an existing model.

### Partial-result behavior

- No explicit `PARTIAL` result exists.
- Fewer than five customers returns Boolean `True`, but downstream expects a DataFrame.
- Empty/missing-feature cases return `False`, but downstream still attempts DataFrame operations.
- Artifact save may fail after valid cluster assignments have been calculated; Shepherd then rejects the output because model ID is `-1`.
- BCDP batches committed before a later failure are not rolled back.
- Overall API failure is represented as application status `2` with HTTP 200.

### Significant correctness risks

- Industry weights are not applied because prefixed feature names are not recognized.
- Recency direction is wrong during semantic ranking.
- Label meaning can change between runs because cluster rankings are recalculated from each current batch.
- Five customers technically qualify but produce five singleton clusters.
- New and low-history customers are mixed with mature customers.
- No outlier handling exists; large monetary values can dominate K-Means geometry.
- Raw frequency and monetary values are not log-transformed.
- Missing preprocessors can cause inference-time refitting incompatible with saved centroids.
- Model upload is commented out, while loading expects an S3 artifact.
- Registry selection has no deterministic ordering among multiple model rows.
- The evaluation helper methods contain tuple-handling errors and are not part of a trustworthy production evaluation workflow.

---

## 12. INTEGRATION

### API

```http
POST /api/v1/services/run/
Content-Type: application/json

{"whatson_id": 123}
```

There is no dedicated RFM endpoint.

### Internal API

```python
Shepherd.do_RFM_clustering_for_business(
    whatson_id,
    business_data
)
```

The return type is nominally annotated as Boolean but normally returns a DataFrame.

### Events emitted

- None.

### Events consumed

- None.

### Job type

- Scheduled full-tenant platform batch.
- API-triggered full-tenant platform batch.
- Implicit RFM model bootstrap when no active model exists.

### Result retrieval

- No job ID.
- No polling API.
- No result URI.
- No segment results returned by HTTP.
- Consumers must read the updated BCDP profile.

### Idempotency

- No idempotency or run key.
- Repeating a run appends another cluster-history entry.
- Multiple bootstrap runs can create duplicate model version 1 artifacts or registry rows.
- No transaction/data cutoff is attached to the run, so repeated executions can use changing source data.

### Versioning

- API path: v1.
- Shepherd package: 0.1.0.
- Model version: default 1.
- Feature schema: unversioned.
- Labeling-policy version: unversioned.
- Industry-weight version: unversioned.
- Results do not contain model, feature, or label-policy versions.

### Downstream compatibility

- Shepherd produces enums `0–4`.
- The agent API accepts `rfm_segment` in the range `0–5`; segment `5` has no corresponding Shepherd output.
- The agent receives segment values from its caller rather than querying Shepherd directly.

### Security

A bearer-security object is declared in the API module, but the full-run endpoint does not apply it. The visible route declaration does not enforce authentication or tenant authorization.

---

## 13. OBSERVABILITY

### Currently available

- `engine.shepherd` DEBUG logger.
- Console logs.
- Rotating `logs/shepherd.log`, approximately 1 MB with three backups.
- Worker logs tenant attempts, durations, retries, skips, and failures.
- Pipeline and engine print overall runtimes.
- No RFM-specific metrics endpoint.
- No persisted clustering evaluation report.

### Required operational metrics

- `rfm_runs_total{status,trigger,tenant}`
- `rfm_run_duration_seconds`
- `rfm_queue_time_seconds`
- `rfm_customers_processed_total`
- `rfm_customers_not_eligible_total`
- `rfm_model_load_duration_seconds`
- `rfm_model_training_duration_seconds`
- `rfm_artifact_failures_total`
- `rfm_bcdp_write_duration_seconds`
- `rfm_bcdp_failed_batches_total`
- `rfm_retry_total`
- `rfm_active_jobs`
- `rfm_model_bootstrap_total`

### Required data metrics

- Input customer count.
- Customers with no transactions.
- Missingness by R/F/M field.
- Duplicate customer-key count.
- Transaction and feature freshness.
- Recency minimum/maximum/percentiles.
- Frequency distribution.
- Monetary distribution and currency.
- Negative/refund amount count.
- Rows excluded and exclusion reason.
- Observation-window start/end.
- Outlier counts.

### Required clustering metrics

- Active model ID/version.
- Cluster count.
- Customer count per cluster.
- Smallest cluster ratio.
- K-Means inertia.
- Silhouette score.
- Calinski–Harabasz score.
- Davies–Bouldin score.
- Centroid values in original units.
- Centroid and cluster-size drift.
- Assignment distance distribution.
- Seed/retraining stability.
- Segment transition matrix.
- Semantic label-to-raw-cluster mapping.
- Industry weight group and configuration version.
- Frequency of label-rank changes.

### Required business metrics

- Revenue share by segment.
- Purchase-frequency distribution by segment.
- Campaign response and conversion by segment.
- Retention and churn rate by segment.
- Segment movement over time.
- Percentage of customers entering or leaving Champions/Ghost.
- Incremental campaign lift attributable to segmentation.

### Required structured log context

- `run_id`
- `tenant_id`
- `trigger`
- `model_id`
- `model_version`
- `feature_schema_version`
- `label_policy_version`
- `industry_group`
- `customer_count`
- `cluster_sizes`
- `status`
- `duration_ms`
- `failed_stage`
- `retry_attempt`

Customer phone numbers should be redacted or hashed.

---

## 14. OWNERSHIP / ISOLATION

### Owns

The RFM service should exclusively own:

- Definitions of recency, frequency, and monetary.
- Transaction eligibility and observation-window policy.
- RFM feature schema.
- RFM customer eligibility.
- RFM transformations and scaling.
- Segment model training and inference.
- RFM model versions and artifacts.
- Semantic segment-label policy.
- Segment assignments and history.
- Cluster evaluation reports.
- RFM-specific configuration and monitoring.
- RFM result events and public contracts.

### May access

Through explicit, versioned contracts:

- Canonical tenant and customer identifiers.
- A shared transaction/activity data product.
- Currency and transaction-status reference data.
- RFM-owned model registry and artifact namespace.
- RFM-owned prediction/segment storage.
- Tenant industry classification.
- Platform event publisher.
- Customer-profile projection interface.

### Must NOT directly access

- Churn-owned scores, history, tables, or artifacts.
- Persona-owned data.
- Customer-state-owned data.
- Full shared BCDP documents.
- Other ML services’ feature tables or model records.
- Generic platform databases through unrestricted CRUD.
- Psychographic clustering internals.
- NPT/CLF/RSF artifacts.
- Another service’s object-storage namespace.

### Current ownership violations

The current implementation:

- Constructs Orbit database infrastructure directly.
- Uses a shared generic model handler that also contains psychographic, churn, CLF, and RSF concerns.
- Uses the generic `"clustering"` model namespace rather than an RFM-specific namespace.
- Reads previous RFM state from the shared BCDP profile.
- Depends on the churn service’s combined BCDP writer in the active engine flow.
- Contains psychographic clustering orchestration inside Shepherd.
- Contains CLV calculation that reads RFM, churn, and customer-state fields.
- Has a dormant writer capable of rewriting both RFM and Churn sections of BCDP.
- Uses phone as its customer integration key.
- Relies on an externally prepared `RFM.*` DataFrame without a formal data-product contract.

### Recommended isolation boundary

```text
Shared transaction data product
  ↓
Versioned RFMFeatureBatch
  ↓
RFM service
  ├─ eligibility
  ├─ transformation
  ├─ model training/inference
  ├─ semantic labeling
  └─ segment history
  ↓
RfmSegmentAssigned event/result
  ↓
External customer-profile projector
  ↓
BCDP
```

Recommended public result:

```json
{
  "tenant_id": 123,
  "customer_id": "canonical-customer-id",
  "segment": {
    "code": 1,
    "name": "Loyal"
  },
  "raw_cluster": 3,
  "distance": 0.72,
  "model_version": 4,
  "feature_schema_version": 2,
  "label_policy_version": 3,
  "assigned_at": "2026-08-11T11:01:00Z",
  "status": "SUCCESS"
}
```

RFM should publish only RFM-owned results. A separate integration component should project them into the shared customer profile, and CLV and psychographic clustering should be separate service boundaries.