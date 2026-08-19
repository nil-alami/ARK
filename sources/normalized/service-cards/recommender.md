# ML SERVICE CARD
===============

Service name: Product Recommendation / REC  
Service ID/version: `REC` 0.1.0; ranking policy `heuristic_v1`  
Owner: TBD  
Implementation reviewed: [REC.py](<C:/Users/AFE AI/PycharmProjects/select-family/engine/engine/REC/REC.py>), [config.py](<C:/Users/AFE AI/PycharmProjects/select-family/engine/engine/REC/configs/config.py>), [recommendation_events](<C:/Users/AFE AI/PycharmProjects/select-family/engine/engine/REC/sub_modules/recommendation_events/functions.py>)

## Infrastructure classification

1. **Request-driven or proactive?**  
   Recommendation generation is currently an in-process/CLI-triggered batch. It is designed for nightly execution but is not wired into the existing scheduler or `/services/run/` API. Supporting product-metadata and recommendation-event capabilities are request-driven APIs.

2. **Stateless or stateful?**  
   Stateful overall. ALS is retrained fresh and discarded on every run, but recommendations, serving events, product metadata, exposure history, and debug artifacts persist.

3. **Synchronous or asynchronous?**  
   Synchronous. `Recommender.recommender()` blocks until the tenant batch finishes. Supporting APIs use a thread pool but wait for completion.

4. **Online or batch-oriented?**  
   Batch-oriented. It generates recommendations for the complete eligible tenant customer population. No low-latency recommendation-serving endpoint exists.

5. **Raw or derived-data consumer?**  
   Both:
   - Raw transactions, catalog, inventory, and customer identifiers.
   - Derived product metadata, interaction weights, serving history, and recommendation events.

---

## 1. PURPOSE

- Produces ranked product recommendations for each eligible customer in a business.
- Combines several recommendation strategies:
  - Implicit-feedback ALS.
  - Basket item-to-item co-occurrence.
  - Same-customer purchase-window similarity.
  - Content-based filtering.
  - Trending, popular, new-arrival, and category-popularity fallbacks.
- Routes each customer to appropriate sources based on their history depth.
- Applies catalog, stock, price, diversity, family, repeat-exposure, and quality constraints.
- Uses an explore/exploit layer to reduce repetitive recommendation loops.
- Optionally persists an immutable top-three recommendation batch per customer.
- Uses recorded delivery events and subsequent purchases as historical feedback for repeat penalties and success bonuses.

Primary consumers are expected to be:

- Campaign and messaging systems.
- Product recommendation surfaces.
- Customer engagement agents.
- Recommendation delivery/event producers.
- Analytics and model-monitoring processes.

---

## 2. TRIGGER / EXECUTION MODE

### Recommendation generation

Current invocation:

```python
Recommender().recommender(
    whatson_id=123,
    debug_recommendation=True,
    topk_per_item=40,
    persist_recommendations=False,
)
```

Also available as a direct script/CLI-style entry point:

```python
main(whatson_id)
```

Characteristics:

- Tenant-wide batch.
- Synchronous.
- Designed in documentation as an offline/nightly process.
- No active scheduler integration was found.
- Not invoked by the existing `/api/v1/services/run/` path.
- No recommendation-generation HTTP endpoint.
- Cannot initiate work proactively.
- Does not publish a “recommendations ready” event.

### Supporting APIs

Product metadata:

```http
POST /api/v1/product-metadata/upsert
```

Recommendation delivery events:

```http
POST /api/v1/recommendation-events
```

Both execute synchronously through a worker thread and return when processing finishes.

---

## 3. INPUT CONTRACT

### Required invocation inputs

| Input | Type | Required | Default | Meaning |
|---|---:|---:|---:|---|
| `whatson_id` | integer | Yes | — | External tenant/account identifier |
| `debug_recommendation` | boolean | No | `true` | Write detailed CSV diagnostics |
| `topk_per_item` | integer | No | `40` | Item-neighbor limit |
| `persist_recommendations` | boolean | No | `false` | Persist final top three per customer |

No explicit validation enforces positive `whatson_id` or `topk_per_item`.

### Required transaction dataset

REC directly fetches the previous 200 days of transactions.

Required transaction-level fields:

| Field | Type | Meaning |
|---|---|---|
| `phone` | string | Customer identifier |
| `transaction_date` | timestamp | Transaction time |
| `transaction_id` | integer | Basket/order identifier |
| `Amount` | numeric | Positive transaction amount |
| `Items` | JSON array | Purchased line items |
| `source_type` | integer enum | Source-specific transaction/product schema |
| `WhatsonId` | integer | Tenant identifier |

Allowed `source_type` values:

| Value | Source |
|---:|---|
| `0` | None/default |
| `1` | Target |
| `2` | Baran |
| `3` | Mahak |

Transaction validation requires:

- Non-empty phone.
- `Amount > 0`.
- Valid timestamp.
- Valid `WhatsonId`.
- Allowed source type.
- A parseable, source-compatible `Items` structure.

Typical item structure:

```json
{
  "ItemId": 179,
  "Name": "Product name",
  "Price": 412.01,
  "Quantity": 1,
  "CategoryId": 2268105407220155392,
  "BrandId": 63
}
```

Baran uses source-specific keys such as:

```json
{
  "ProductId": 179,
  "UnitPrice": 412.01,
  "Quantity": 1
}
```

### Required catalog dataset

Normalized product fields:

| Field | Type | Requirement |
|---|---|---|
| `Id` | integer | Canonical product ID |
| `BusinessId` | integer | Product tenant |
| `CreatedAt` | timestamp | Used for new-arrival logic |
| `Title` | string | Must be non-empty |
| `Price` | numeric | Must be greater than zero |
| `Quantity` | numeric | Must be zero or greater during validation |
| `Status` | integer | Must equal active status `1` |
| `ExternalId` | integer | Required source/canonical mapping |
| `CategoryId` | integer/null | Needed for category logic |
| `BrandId` | integer/null | Needed for brand/CBF logic |
| `Tags`/description | structured/text | Optional content signal |

### Required product metadata

Every candidate product must have:

- `IsRecommendable == true`
- A usable `FamilyKey`

If either metadata column is missing, or no products have acceptable values, the recommender drops the affected catalog rows. Missing columns can effectively make the entire business ineligible.

Additional metadata used by CBF and constraints:

- Category ID.
- Brand ID.
- Normalized title.
- Text/description/tags.
- Family matching method.
- Category/family confidence and detector metadata.

### Required serving-history data

From the previous 30 days:

- `CustomerProductRecommendations`
- `RecommendationEvents`
- BCDP-to-phone mapping
- Customer purchases after recommendation delivery

Derived serving features include:

- Times served in 7, 14, and 30 days.
- Last served time.
- Days since last served.
- Purchases after recommendation delivery.

### Required datasets

Separated from invocation inputs:

1. Tenant identity mapping.
2. Raw transaction history.
3. Product catalog and inventory.
4. Source-specific product-ID mappings.
5. Product attributes and recommendability state.
6. Product category/family metadata.
7. Previous recommendation batches.
8. Recommendation delivery events.
9. BCDP/customer identity mapping.
10. Supporting category/family artifacts:
    - FAISS indexes.
    - Parquet metadata.
    - Compiled category dictionary.
    - Business-domain definitions.
    - Recommendability rules.
11. Optional LLM category fallback configuration.

### Minimum data requirements

Top-level implemented gates:

- At least one valid transaction, product, and line-item row.
- At least `200` valid transactions.
- At least `2` products.
- At least `5` sellable products.
- Products must pass recommendability and family-key filtering.

ALS-specific gates:

- At least `40` users.
- At least `25` items.
- At least `200` unique user-item pairs.
- Average items per user at least `2`.
- Average users per item at least `2`.
- Single-interaction user share no greater than `80%`.
- Single-buyer item share no greater than `80%`.

CBF-specific gates include:

- At least `6` eligible items.
- At least `4` items with metadata.
- Metadata coverage of at least `40%`.
- Sufficient category, brand, or text differentiation.

Co-occurrence uses adaptive gates for:

- Unique item count.
- Multi-item transactions.
- Pair volume.
- Unique customers.
- Available catalog.

### Input schema/version

- No recommendation-generation API schema.
- Internal inputs are database-derived DataFrames.
- Transaction source schemas are configured by source type.
- Feature and interaction schemas are not formally versioned.
- Product metadata artifacts have versions such as `bge-m3_v1`.
- Ranking model/policy is identified as `heuristic_v1`.

---

## 4. OUTPUT CONTRACT

### No-recommendation output

For failed eligibility/readiness:

```json
{
  "run_ts": "2026-08-11T08:00:00Z",
  "status": "NOT_ENOUGH_TX",
  "served": false,
  "topk_per_customer": 20,
  "customer_count": 0,
  "recommendations_by_customer": {},
  "reason": "NO_RECOMMENDATIONS_BUSINESS_NOT_READY",
  "guard": {
    "tx_count": 120,
    "unique_items": 18,
    "unique_customers": 22,
    "multi_item_tx_count": 5,
    "est_pair_volume": 8,
    "status": "NOT_ENOUGH_TX",
    "details": {}
  }
}
```

Possible top-level readiness statuses include:

- `NO_DATA`
- `NOT_ENOUGH_TX`
- `PRODUCT_VOLUME_TOO_SMALL`
- `CATALOG_SELLABLE_TOO_SMALL`

### Successful internal output

The normal result is a Python dictionary containing multiple Pandas DataFrames:

```text
status
served
strategy
als_user_item_candidates
als_item_item_neighbors
als_item_item_candidates
als_quality
customer_routing
personalized_candidates
personalized_candidates_filtered
ranking_source_rows
ranked_pool
final_ranked
debug_counts
recommendation_batch_id                         optional
persisted_customer_product_recommendations       optional
```

Current success value:

```json
{
  "status": "Done",
  "served": true
}
```

This is not a JSON-ready API contract because most values are DataFrames.

### Primary recommendation result

`final_ranked` contains up to 20 recommendations per customer, possibly fewer after constraints and family deduplication.

Core fields:

| Field | Type | Meaning |
|---|---|---|
| `business_id` | integer | Internal business ID |
| `phone` | string | Customer identifier |
| `item_id` | integer | Canonical product ID |
| `run_date` | timestamp | Recommendation generation time |
| `model_version` | string | Currently `heuristic_v1` |
| `final_score` | float | Final heuristic score |
| `pre_bandit_rank` | integer | Rank before explore/exploit mixing |
| `final_rank` | integer | Final serving rank |
| `best_source` | string | Strongest contributing source |
| `source_count` | integer | Number of supporting sources |
| `allowed_sources` | string | Customer-eligible sources |
| `primary_route` | string | Main customer recommendation route |
| `bandit_bucket` | string | `EXPLOIT`, `EXPLORE`, or `EXPLOIT_BACKFILL` |
| `bandit_decision` | string | Selection decision |
| `explore_score` | float/null | Exploration-only score |
| `family_key` | string | Product-family deduplication key |

Source evidence fields:

```text
has_als
has_co_oc
has_cbf
has_fallback
als_score_norm
co_oc_score_norm
cbf_score_norm
fallback_score_norm
als_confidence
co_oc_confidence
cbf_confidence
fallback_confidence
source_evidence_score
agreement_bonus
only_fallback_flag
all_sources_borderline_flag
```

Customer/item context fields:

```text
customer_days_since_last_purchase
customer_activity_segment
customer_depth_segment
customer_orders_lookback
customer_distinct_items_lookback
customer_distinct_categories_lookback
customer_avg_order_gap_days
personalization_multiplier
prior_multiplier
category_affinity_score
price_distance_penalty
customer_item_fit_bonus
popularity_norm
trend_norm
item_prior_bonus
```

Serving-history fields:

```text
times_served_7d
times_served_14d
times_served_30d
last_served_date
days_since_last_served
times_purchased_after_served_30d
repeat_penalty
success_bonus
```

Example recommendation:

```json
{
  "business_id": 123,
  "phone": "customer-mobile",
  "item_id": 179,
  "model_version": "heuristic_v1",
  "final_score": 1.24,
  "pre_bandit_rank": 2,
  "final_rank": 1,
  "best_source": "ALS",
  "source_count": 3,
  "primary_route": "ALS",
  "bandit_bucket": "EXPLOIT",
  "bandit_decision": "exploit_greedy",
  "family_key": "family-42"
}
```

### Score/confidence meaning

- `final_score` is a heuristic ranking value, not a probability.
- Scores are meaningful primarily within a customer’s candidate set.
- Source scores are normalized before fusion.
- Borderline source output can be downweighted.
- Unsafe source output is discarded.
- Agreement across sources contributes a positive bonus.
- Fallback-only and borderline evidence can produce penalties.
- Repeat exposure produces a penalty.
- A prior successful recommendation/purchase relationship produces a bonus.
- No calibrated likelihood of purchase is returned.
- No confidence interval exists.

Approximate scoring structure:

```text
heuristic_score =
    personalization multiplier
      × (source evidence + agreement bonus + customer-item fit)
    + prior multiplier × item prior
    - penalties

final_score =
    heuristic_score
    - repeat penalty
    + success bonus
```

### Persisted recommendation schema

When `persist_recommendations=true`, REC persists the top three per customer:

```json
{
  "recommendation_id": 1001,
  "bcdp_id": 5001,
  "business_id": 123,
  "product_id": 179,
  "recommended_at": "2026-08-11T08:00:00Z",
  "rank": 1,
  "score": 1.24,
  "source": "ALS",
  "model_version": "heuristic_v1",
  "batch_id": "uuid",
  "phone": "customer-mobile"
}
```

Physical table:

```text
CustomerProductRecommendations
```

Uniqueness is enforced within a batch for:

- `(BatchId, BcdpId, Rank)`
- `(BatchId, BcdpId, ProductId)`

### Possible statuses

- **SUCCESS:** `status="Done"` with non-empty `final_ranked`.
- **PARTIAL:** Not explicit. This effectively occurs when one or more sources are unavailable/unsafe but remaining sources produce recommendations.
- **FAILED:** Uncaught exception; no standard result envelope.
- **NOT_ELIGIBLE:** `NO_DATA`, `NOT_ENOUGH_TX`, `PRODUCT_VOLUME_TOO_SMALL`, or `CATALOG_SELLABLE_TOO_SMALL`.
- **NO RESULT AFTER FILTERING:** `NO_CANDIDATES_AFTER_PRE_RANK`.

`served` is set before final post-ranking constraints, so it can disagree with an empty final result. Status and result semantics need normalization.

---

## 5. HIGH-LEVEL WORKFLOW

```text
whatson_id
  ↓
Resolve internal business_id
  ↓
Fetch previous 200 days of transactions
  ↓
Validate transactions and source-specific item structure
  ↓
Detect product-data source from transaction SourceType
  ↓
Fetch and normalize catalog
  ↓
Fetch ProductAttributes
  ↓
Keep only:
  ├─ IsRecommendable = true
  └─ valid FamilyKey
  ↓
Map transaction items to canonical products
  ↓
Explode baskets into one row per line item
  ↓
Build decayed user-item interactions
  ↓
Calculate business readiness summary
  ↓
Top-level readiness gate
  ↓
Validate individual recommendation sources
  ├─ non-collaborative fallback
  ├─ co-occurrence
  ├─ ALS
  └─ CBF
  ↓
Generate available candidate sources
  ├─ trending/popular/new/category-popular
  ├─ basket item-to-item
  ├─ user-window item similarity
  ├─ content-based candidates
  ├─ ALS user-item candidates
  └─ ALS item-item candidates
  ↓
Validate source quality
  ├─ strong → use fully
  ├─ borderline → downweight
  └─ unsafe → discard
  ↓
Attach product family keys
  ↓
Pre-rank hard constraints
  ├─ recommendability/family
  ├─ stock
  ├─ product health
  └─ price outliers
  ↓
Customer-level source routing
  ↓
Personalize and fuse sources
  ↓
On-ranker caps and pruning
  ↓
Load previous 30-day serving events
  ↓
Heuristic ranker
  ├─ source evidence
  ├─ agreement
  ├─ customer/item fit
  ├─ popularity/trend priors
  ├─ repeat penalties
  └─ success bonuses
  ↓
Post-rank score and diversity constraints
  ↓
Explore/exploit bandit
  ↓
Final top 20 per customer
  ↓
Optional persistence of top 3
  ↓
Debug artifacts and returned result dictionary
```

ALS behavior:

```text
Current interaction matrix
  ↓
Train fresh ALS
  ↓
Use factors immediately
  ↓
Discard ALS factors and mappings
```

There is no stored/reused ALS model.

---

## 6. ELIGIBILITY / PRECONDITIONS

### Tenant/business

- `whatson_id` must map to exactly one usable internal business ID.
- All three configured databases must be reachable because the constructor connects to Badger, Orbit, and dev immediately.

### Transactions

- Valid transactions must exist within the last 200 days.
- At least 200 valid transaction rows.
- Positive transaction amount.
- Valid timestamp and phone.
- Recognized source type.
- Parseable line-item JSON.
- Line-item IDs must map to eligible canonical products.

### Catalog

- At least two products.
- At least five sellable products.
- Required product columns available.
- Active status.
- Positive price.
- Usable quantity/inventory.
- Canonical/external product ID mapping.
- `IsRecommendable=true`.
- Valid `FamilyKey`.

### Customer/source eligibility

Individual customers may receive different source routes:

- ALS requires at least two customer interactions.
- Co-occurrence requires at least one usable seed item.
- CBF requires at least two metadata-covered history items.
- Fallback is intended to remain available where catalog supply permits.

### Other conditions

- Product metadata generation must have run before REC if attributes are missing.
- Recommendation history must be accessible for repeat-control features.
- No tenant entitlement/configuration check exists.
- No explicit tenant currency or regional product-policy contract exists.

Important implementation behavior:

Although non-collaborative fallbacks are designed for low-data businesses, the current top-level `MIN_TX_NUM=200` gate returns before those fallback generators run. Businesses with fewer than 200 transactions currently receive no recommendations.

---

## 7. DEPENDENCIES

### Internal

- Transaction and database fetchers.
- Product-source adapters.
- Line-item normalization.
- Interaction builder.
- Business/source guards.
- Candidate generators.
- ALS trainer.
- CBF generator.
- Constraints.
- Customer routing and ranker.
- Serving-history builder.
- Bandit mixer.
- Product metadata submodules.
- Recommendation persistence/event subsystem.
- Debug artifact writers.

### External systems

- Badger PostgreSQL.
- Orbit PostgreSQL or MSSQL.
- Dev PostgreSQL.
- BCDP/CDP identity tables.
- Optional LLM endpoint for category fallback.
- Local artifact filesystem.

### Data stores/tables

- `Transactions`
- `Products`
- `BaranProducts`
- `ProductAttributes`
- `ProductCategories`
- `Businesses`
- `Cdp`
- `Bcdps`
- `CustomerProductRecommendations`
- `RecommendationEvents`

### ML/model dependencies

- `implicit.als.AlternatingLeastSquares`
- SciPy sparse matrices
- NumPy
- Pandas
- FAISS category and family indexes
- BAAI `bge-m3` embeddings for metadata enrichment
- Compiled category dictionary
- Optional OpenAI-compatible LLM client

### Supporting artifact versions

- Category embedding index: `bge-m3_v1`
- Family embedding index: `bge-m3_v1`
- Embedding dimension: 1,024
- FAISS type: `IndexFlatIP`
- Similarity: cosine
- Ranking policy: `heuristic_v1`

### Runtime libraries

- Pandas
- NumPy
- SciPy
- implicit
- scikit-learn-related utilities
- SQLAlchemy
- FAISS
- PyArrow/Parquet support
- OpenAI SDK for optional fallback
- FastAPI
- Pydantic

The project’s main dependency declaration does not currently enumerate all REC runtime dependencies.

---

## 8. STATE & STORAGE

### Reads

- Tenant identity mapping.
- Recent transactions.
- Catalog and inventory.
- Product attributes.
- Previous recommendation batches/events.
- BCDP/customer phone mapping.
- Local metadata dictionaries and embedding indexes.

### Writes

When enabled:

- Immutable recommendation rows to `CustomerProductRecommendations`.
- Delivery events to `RecommendationEvents`.
- Numerous debug CSV files.

Product metadata API:

- Returns an upsert payload for backend persistence.
- The visible route does not itself persist the returned ProductAttributes payload.

### Persistent state

- Product metadata.
- Recommendation batches.
- Delivery event history.
- Customer exposure history.
- Category/family dictionaries and embedding indexes.
- Debug/run histories in CSV form.

### Non-persistent model state

- ALS user factors.
- ALS item factors.
- User/item index mappings.
- Sparse interaction matrix.
- Candidate DataFrames.

These are generated fresh, kept in memory for the current run, and discarded.

### Cache

- No recommendation-result cache.
- No reusable ALS artifact cache.
- Supporting product-metadata indexes may be loaded into process memory.
- No distributed cache or shared feature cache.

### Debug/intermediate artifacts

Default `debug_recommendation=true` writes files including:

```text
no_data_guard_result.csv
not_ready_guard_result.csv
candidate_gen_strategy_vals.csv
non_collab_candidates.csv
co_occurrence_candidates.csv
cbf_candidates.csv
als_user_item_candidates.csv
als_item_item_candidates.csv
rec_run_summary.csv
strategy_state_df.csv
interactions.csv
business_items_similarity.csv
test_second_ranked_pool_df.csv
final_ranked_df_explored.csv
test_2_out.csv
```

These files use shared filenames rather than tenant/run-specific directories. Concurrent runs can overwrite or mix results and may expose phone-level customer data.

---

## 9. EXECUTION PROFILE

Typical runtime: **TBD; no benchmark or SLO is defined.**

Expected scale:

- One tenant at a time.
- All valid transactions from the previous 200 days.
- Complete eligible product catalog.
- All customers represented in the transaction window.
- Up to hundreds of candidates retained per customer before ranking.

CPU:

- CPU-intensive.
- ALS trains 64-dimensional factors for 30 iterations.
- Co-occurrence and CBF perform group, join, and similarity operations.
- Ranker performs multiple tenant-wide DataFrame joins and per-customer groups.
- Implicit ALS may use native/OpenMP CPU threads.

RAM:

- Sparse user-item matrix.
- User and item ALS factor arrays.
- Multiple candidate tables.
- Full catalog and line-item tables.
- Source-level and personalized candidate tables.
- Returned result retains several large intermediate DataFrames.

Approximate ALS factor memory grows with:

```text
64 × (number of users + number of items)
```

Candidate memory can dominate because ALS, CBF, co-occurrence, and fallback rows coexist.

GPU:

- Core recommendation generation does not require a GPU.
- The supporting embedding metadata pipeline may benefit from GPU acceleration when rebuilding embeddings, but the bundled FAISS indexes can be queried on CPU.

Parallelizable:

- Tenants are independently parallelizable.
- Customers can be partitioned during ranking.
- Candidate sources could run independently.
- Current orchestrator executes stages sequentially.
- Shared debug filenames make concurrent execution unsafe without isolation.

Current limits:

- Neighbor cap: 40 per item.
- ALS user-item candidates: 100 per user.
- ALS item-item expansion: 100 per user.
- CBF: up to 50 per user.
- Personalized pool: 100 per user.
- Total on-ranker cap: 200 per user.
- Pre-bandit pool: 30.
- Final output: 20 per user.
- Persisted output: 3 per user.

Timeout considerations:

- No total run timeout.
- No per-stage timeout.
- No database query timeout defined in REC.
- Optional LLM client has no default timeout unless explicitly provided.
- Recommendation event batches are synchronous.
- Full recommendation generation should not be executed inside a normal short-lived HTTP request.

---

## 10. CONFIGURATION

### Data/readiness

| Parameter | Value |
|---|---:|
| Lookback | 200 days |
| Minimum transactions | 200 |
| Minimum sellable catalog | 5 |
| Minimum products | 2 |
| Minimum shoppers | 25 |
| Minimum pair volume baseline | 200 |
| Minimum multi-item rate | 3% |
| Interaction decay constant | 60 days |

### Fallback windows

| Parameter | Value |
|---|---:|
| Trending | 7 days |
| Popular | 90 days |
| New arrival | 20 days |
| Fallback pool | 100 |

### ALS

| Parameter | Value |
|---|---:|
| Factors | 64 |
| Iterations | 30 |
| Regularization | 0.01 in active call |
| Alpha | 40 |
| Random seed | 42 |
| Minimum users | 40 |
| Minimum items | 25 |
| Minimum user-item pairs | 200 |

ALS retrains fresh on every execution.

### CBF

| Signal | Weight |
|---|---:|
| Category | 0.40 |
| Brand | 0.25 |
| Text | 0.25 |
| Price | 0.10 |

### Source fusion

Pre-ranker source weights:

| Source | Weight |
|---|---:|
| ALS | 1.00 |
| CBF | 0.85 |
| Co-occurrence | 0.75 |
| Fallback | 0.30 |

The later heuristic scorer applies another weighting layer, currently approximately:

- ALS: 1.00
- Co-occurrence: 0.90
- CBF: 0.75
- Fallback: 0.50

### Constraints

- Low-stock threshold: 2.
- Maximum price multiplier: 4.
- Minimum mature-product sales: 5.
- Product-age threshold: 100 days.
- Maximum candidates per customer: 200.
- Maximum category candidates per customer before ranking: 10.
- Relative score cutoff: 5%.
- Post-rank minimum score: 0.01.
- Post-rank category cap: 2.
- Post-rank brand cap: 3.
- Maximum price-bucket share: 60%.

### Final ranking/bandit

| Parameter | Value |
|---|---:|
| Final top-k | 20 |
| Rank pool | 30 |
| Bandit epsilon | 0.10 |
| Target explore ratio | 20% |
| Minimum explore score ratio | 0.65 |
| Maximum 7-day serves for exploration | 3 |
| Random seed | 42 |

### Persistence/history

- Recommendation history lookback: 30 days.
- Persisted top-N: 3.
- Model/policy version: `heuristic_v1`.
- Random UUID batch ID.
- Recommendation events per API request: 1–100.
- Event timestamp maximum age: 365 days.

### Metadata/LLM

- Category LLM acceptance threshold: 0.70.
- Environment:
  - `LLM_MODEL`
  - `LLM_API_KEY`
  - `LLM_BASE_URL`
- Recommendation database routing:
  - `RECOMMENDATION_EVENTS_READ_DB`
  - `RECOMMENDATION_EVENTS_WRITE_DB`

### Tenant configuration

The current thresholds and ranking multipliers are global. No tenant-specific configuration store is applied, despite the presence of a generic business-tuning dictionary.

---

## 11. FAILURE / FALLBACK

### Possible failures

- Failure to connect to any of the three databases during constructor initialization.
- Missing tenant mapping.
- Missing/invalid transaction fields.
- Malformed source-specific `Items`.
- Product ID mapping failure.
- Empty product catalog after validation.
- Missing ProductAttributes.
- Missing `IsRecommendable` or `FamilyKey`.
- Too few transactions or sellable products.
- Sparse/invalid interactions.
- ALS native-library or training failure.
- Candidate generator failure.
- Source-quality failure.
- Missing recommendation-history tables.
- Ambiguous or missing BCDP identity.
- Product/business mismatch during persistence.
- Debug artifact write failure.
- Memory exhaustion for large candidate sets.
- LLM/embedding dependency failure in metadata generation.

### Retryable?

- Core recommendation generation has no internal retry.
- No scheduler currently wraps it.
- Supporting API calls have no application retry.
- Database or LLM failures propagate or return failed API responses.
- Recommendation event insertion is atomic, but not retried.

### Fallback behavior

Implemented source-level fallbacks:

- Weak basket co-occurrence → try user-window similarity.
- Unsafe co-occurrence → discard or switch mode.
- Unsafe ALS → discard ALS candidates.
- Unsafe CBF → discard CBF candidates.
- Remaining sources may still generate final recommendations.
- Customers without enough history route toward fallback sources.
- Bandit backfills missing positions from remaining ranked candidates.

Important limitation:

- The top-level 200-transaction gate prevents fallback generation for low-volume businesses. Despite documentation describing non-collaborative fallback for low data, active code returns before that fallback can execute.

### Partial results

Partial operation is implicit:

- One or more sources can fail quality checks while others remain usable.
- Borderline sources are downweighted.
- Unsafe sources are removed.

However, no explicit `PARTIAL` status or list of unavailable sources appears in the primary result contract.

### Failure isolation gaps

- Source generators are not wrapped independently. An exception in ALS, CBF, or co-occurrence can abort the whole run even if other sources were valid.
- Persistence is optional and defaults to false; a successful run may leave no durable recommendations.
- `served` is calculated before final post-rank filtering.
- Debug file writes occur even when recommendation persistence is disabled.
- Entity validation and recommendation insertion use separate databases/transactions, so they are not globally atomic.

### Recommendation-event behavior

- Entire event batch is validated and inserted atomically.
- Missing recommendation IDs cause failure.
- Duplicate `ExternalEventId` values return a conflict rather than silently returning the existing event.
- `ExternalEventId` supplies deduplication protection.
- Timestamps must be timezone-aware and no older than one year.

---

## 12. INTEGRATION

### Recommendation-generation API

None currently.

Recommended job contract:

```http
POST /api/v1/recommendation-jobs
```

```json
{
  "tenant_id": 123,
  "as_of": "2026-08-11T08:00:00Z",
  "persist": true,
  "configuration_version": "rec-config-v1"
}
```

The current integration is a Python method or script.

### Product metadata API

```http
POST /api/v1/product-metadata/upsert
```

This builds metadata results/upsert payloads for requested products. It is a supporting prerequisite, not the recommendation result API.

### Recommendation event API

```http
POST /api/v1/recommendation-events
```

Request:

```json
[
  {
    "RecommendationId": 1001,
    "CreatedAt": "2026-08-11T08:30:00+00:00",
    "ExternalEventId": "provider-event-123"
  }
]
```

Success response:

```json
{
  "status": "success",
  "InsertedCount": 1,
  "Events": [
    {
      "Id": 5001,
      "RecommendationId": 1001,
      "CreatedAt": "2026-08-11T08:30:00Z",
      "ExternalEventId": "provider-event-123"
    }
  ],
  "errorCode": null,
  "errorMessage": null
}
```

### Events emitted

- None from recommendation generation.

### Events consumed

- Recommendation delivery events through HTTP.
- Purchases are inferred from later transaction records rather than consumed as a typed recommendation-conversion event.

### Job type

- Intended nightly tenant batch.
- Fresh ALS training plus inference in the same run.
- Product metadata enrichment request.
- Recommendation delivery-event ingestion.

### Result retrieval

- No recommendation job ID or polling endpoint.
- No customer recommendation lookup/serving endpoint.
- Persisted recommendations can be queried from the database, but no API is exposed for that retrieval.
- Product metadata `job_id` is correlation metadata, not a real asynchronous job.

### Idempotency

Recommendation generation:

- No idempotency key.
- Every persisted run uses a new batch UUID.
- Reruns create another immutable batch.

Recommendation event ingestion:

- Optional `ExternalEventId` has a unique database index.
- Duplicate submission produces a conflict.
- Without `ExternalEventId`, repeated events can be inserted.

### Versioning

- Package: 0.1.0.
- Ranking policy: `heuristic_v1`.
- ALS parameters are not assigned a separate model version.
- Feature/configuration versions are not included in results.
- Product metadata assets have explicit artifact versions.
- API paths use v1.

### Security

The app applies an API-key middleware globally. Core recommendation generation has no independent authorization boundary because it is not exposed as an endpoint.

---

## 13. OBSERVABILITY

### Currently available

- General REC logger.
- Business and source readiness logs.
- Source candidate counts.
- Weakness-check status.
- Extensive debug CSV artifacts.
- Run summaries and strategy-state CSVs.
- Recommendation event API error codes.
- Unit tests for guards, candidate generation, constraints, metadata, serving history, and events.

No REC-specific metrics endpoint or tracing exists.

### Required operational metrics

- `rec_runs_total{status,trigger,tenant}`
- `rec_run_duration_seconds`
- Stage latency:
  - data fetch
  - normalization
  - interaction building
  - ALS training
  - candidate generation by source
  - ranking
  - persistence
- `rec_queue_time_seconds`
- `rec_customers_processed_total`
- `rec_customers_served_total`
- `rec_recommendation_rows_total`
- `rec_persistence_failures_total`
- `rec_event_ingest_total`
- `rec_event_ingest_failures_total`
- CPU and peak RAM per run.

### Required data metrics

- Raw and valid transaction counts.
- Dropped transaction count by reason.
- Catalog row count.
- Sellable product count.
- Recommendability coverage.
- Family-key coverage.
- Category/brand/text metadata coverage.
- Unique customers and products.
- User-item matrix shape, density, and nonzero count.
- Feature and transaction freshness.
- Product-source distribution.
- Unmapped transaction-item rate.

### Required recommendation metrics

- Candidate count by source.
- Source readiness and quality status.
- Customer coverage.
- Catalog coverage.
- Average recommendations per customer.
- Source mix in final top-k.
- Fallback-only customer rate.
- Duplicate family/category rate.
- Score distribution.
- Repeat-exposure rate.
- Explore versus exploit rate.
- Recommendation churn/stability between runs.
- Diversity, novelty, and long-tail coverage.

### Required offline ML metrics

Using temporal holdout:

- Recall@K.
- HitRate@K.
- Precision@K.
- NDCG@K.
- MAP@K.
- Coverage.
- Popularity baseline comparison.
- ALS versus co-occurrence/CBF/fallback lift.
- Performance by cold/new/established customer segment.

### Required business metrics

- Delivery rate.
- Click/open rate if available.
- Purchase-after-recommendation rate.
- Revenue attributed to recommendations.
- Conversion by source.
- Conversion by bandit bucket.
- Incremental lift against holdout/control.
- Repeat recommendation fatigue.
- Product and category exposure fairness.

### Required structured log context

- `run_id`
- `batch_id`
- `tenant_id`
- `whatson_id`
- `as_of`
- `configuration_version`
- `model_version`
- `source`
- `customer_count`
- `product_count`
- `candidate_count`
- `status`
- `failed_stage`
- `duration_ms`

Phones and customer-level histories should not be written unredacted to shared debug files.

---

## 14. OWNERSHIP / ISOLATION

### Owns

REC should exclusively own:

- Recommendation business readiness.
- Interaction weighting.
- Candidate generation.
- Source-quality policies.
- Customer source routing.
- Ranking and scoring.
- Recommendation constraints and diversity policy.
- Explore/exploit policy.
- Recommendation result batches.
- Recommendation exposure history.
- Recommendation feedback/event contract.
- Recommendation evaluation and monitoring.
- Recommendation configuration versions.
- ALS factors during an active run.

### May access

Through explicit, versioned contracts:

- Canonical tenant and customer IDs.
- Transaction/activity data product.
- Product catalog data product.
- Inventory/availability API.
- Product metadata service.
- Product category/family service.
- Customer recommendation-event stream.
- Purchase/conversion-event stream.
- REC-owned database and object namespace.

### Must NOT directly access

- Raw Badger, Orbit, and dev schemas.
- BCDP/CDP identity tables.
- Another service’s customer-profile documents.
- Product metadata implementation tables if metadata is a separate service.
- Churn, RFM, NPT, or persona private storage.
- Generic shared CRUD interfaces.
- Shared source-tree artifact paths for production run output.

### Current ownership violations

The current implementation:

- Constructs three concrete database connections inside `Recommender`.
- Queries Badger, Orbit, and dev schemas directly.
- Resolves customer identity through phone and direct CDP/BCDP queries.
- Validates products/businesses in one database and writes recommendations to another.
- Contains product metadata generation, recommendation generation, persistence, and event ingestion in one package.
- Writes phone-level debug data into shared repository paths.
- Has no dedicated recommendation job/result API.
- Uses environment-selected shared databases for recommendation-event storage.
- Exposes database-shaped DataFrames rather than stable domain DTOs.

### Recommended service boundaries

Product metadata should be independently deployable because it has different infrastructure needs:

```text
Catalog changes
  → Product Metadata service
  → IsRecommendable / Category / Family metadata
```

Recommendation generation:

```text
Transactions + Catalog + Product Metadata + Inventory
  → REC batch job
  → immutable RecommendationBatch
  → RecommendationsGenerated event
  → serving/campaign platform
```

Feedback:

```text
RecommendationDelivered / Clicked / Purchased
  → REC feedback API/event stream
  → exposure and outcome store
  → next ranking run and offline evaluation
```

Recommended public recommendation:

```json
{
  "tenant_id": 123,
  "customer_id": "canonical-customer-id",
  "batch_id": "uuid",
  "generated_at": "2026-08-11T08:00:00Z",
  "model_version": "heuristic_v1",
  "configuration_version": "rec-config-v1",
  "status": "SUCCESS",
  "items": [
    {
      "product_id": 179,
      "rank": 1,
      "score": 1.24,
      "primary_source": "ALS",
      "supporting_sources": ["ALS", "CBF", "POPULAR"],
      "decision": "EXPLOIT",
      "reason_codes": [
        "CATEGORY_AFFINITY",
        "MULTI_SOURCE_SUPPORT"
      ]
    }
  ]
}
```

The REC service should own recommendation decisions and history, while transaction, catalog, inventory, product metadata, identity, and delivery systems remain separate contracted dependencies.