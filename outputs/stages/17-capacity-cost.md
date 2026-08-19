# Stage 17 — Capacity, performance, and cost

**Status:** APPROVED  
**Completed:** 2026-08-13  
**Stage owner:** Primary architecture agent  
**Authorized specialists:** `platform_architect`, `data_mlops_architect` (independent read-only workload reviews)

## Purpose and scope

Define ARK's initial evidence-bounded capacity, performance, and cost model for the approved Python/PostgreSQL/one-Linux-server implementation target. The model covers tenants, requests, data, batches, jobs, events, storage growth, model memory, CPU/GPU, latency, and cost drivers. Because no release scope, workload quantities, numeric objectives, retention policy, hosting product, or budget is approved, Stage 17 supplies symbolic formulas, benchmark requirements, sensitivity analysis, bottleneck indicators, and measurable scale triggers—not fabricated sizing or price precision.

This stage proposes no purchase, vendor, new language, new data-lake product, Kubernetes cluster, broker, GPU, managed service, or production-capacity commitment. It does not clear `DEPLOYMENT_ENVIRONMENT_BLOCKED`, any ADR-007 capability block, or any ADR-008 security block. Stage 18 is not executed.

## Inputs read in full

- `WORKFLOW.md`
- `STATUS.md`
- `SOURCE_MANIFEST.md`
- `stages/STAGE-CONTRACT.md`
- `stages/17-capacity-cost.md`
- `templates/stage-output.md`
- `sources/normalized/system-design-prompt.md` — **16. Capacity, performance, and cost**
- `sources/normalized/ark-assumptions.md`
- `sources/normalized/service-cards/churnobyl.md`
- `sources/normalized/service-cards/RFM.md`
- `sources/normalized/service-cards/next_purchase_prediction.md`
- `sources/normalized/service-cards/recommender.md`
- `sources/normalized/service-cards/Synapse_chatbot.md`
- `sources/normalized/service-cards/synapse_message_generator.md`
- `sources/normalized/service-cards/synapse_campaign_verifier.md`
- Approved `outputs/stages/02-system-definition.md` through `outputs/stages/16-testing.md`
- Accepted `decisions/ADR-000-temporary-source-evidence-disposition.md` through `decisions/ADR-009-provisional-python-postgresql-linux-target.md`
- `quality/source-instruction-coverage.md`

No authoritative production measurements, provider price sheets, hardware inventory, traffic samples, release-scope declaration, or budget were available.

## Specialist reconciliation

The Stage 17-authorized platform and data/ML specialists independently reviewed distinct workload dimensions. The platform review covered API/control traffic, PostgreSQL jobs and owner state, event/delivery paths, runtime roles, telemetry, backups, single-host contention, cost categories, and infrastructure scale triggers. The data/ML review covered ingestion amplification, immutable data layers, capability batch shapes, training/evaluation/reproduction, artifacts/model memory, CPU/GPU, LLM token/provider costs, and per-profile admission constraints. The primary agent reconciled their evidence into the matrices below and remains the sole authoritative writer.

## Source-instruction coverage

| Source requirement | Addressed in | Status/evidence |
|---|---|---|
| Tenants | Workload symbol register; tenant/fairness model | Covered symbolically; count/distribution unknown |
| Requests | Request/latency model | Covered symbolically; rates/mix unknown |
| Data volume | Data-ingestion and storage-growth models | Covered symbolically; source volumes unknown |
| Batch sizes | Capability and ingestion matrices | Covered; activation values require benchmarks |
| Concurrent jobs | Queue/concurrency formulas | Covered; pool limits require measurements |
| Event volume | Conditional event/delivery model | Covered; current production volume is zero because path is inactive |
| Storage growth | PostgreSQL/object/backup/evidence formulas | Covered; retention and version churn unknown |
| Model memory | Model working-set formula and benchmark | Covered; artifact sizes and residency unknown |
| CPU/GPU | Resource-demand model and accelerator gate | Covered; no GPU selected |
| Latency | Sync and durable completion decompositions | Covered; no target invented |
| Cost drivers | Cost ledger and scenario formulas | Covered; no price or budget invented |
| Measurements before infrastructure decisions | Benchmark and decision-gate registers | Covered |

## Confirmed facts

1. ARK's approved provisional implementation target is Python, PostgreSQL, and one Linux server, sponsor-operated with AI assistance and no assumed 24/7 team. Containers are optional; Kubernetes is not selected; Rust or additional data-lake infrastructure requires later evidence. Accepted ADR-009.
2. PostgreSQL initially owns bounded operational truth, including control state, jobs, attempts, schedules, catalog/registry metadata, audit/usage, and conditional outbox records. Object storage owns large immutable raw, datasets, results, artifacts, and evidence by reference. Approved Stages 05, 06, 08, and 15.
3. Small increments use push/micro-batch contracts; large loads/backfills use registered object references. Streaming requires measured volume or latency evidence. `sources/normalized/ark-assumptions.md — Ingestion and the ARK data lake`.
4. Long, retryable, scheduled, ingestion, training, backfill, and large inference work uses durable jobs. PostgreSQL job attempts are at-least-once, fenced, and idempotent; resource pools prevent heavy work from blocking interactive work. Approved Stage 08 and ADR-005.
5. Churn, RFM, NPT, and REC are batch-oriented and `MIGRATION_BLOCKED`. Their prototype constants and samples are migration evidence, not approved production sizes, objectives, or algorithms. Approved Stages 03 and 10; ADR-007.
6. The three Synapse profiles are synchronous interface-only evidence and `EVIDENCE_BLOCKED`. Their provider, model, token limits, concurrency, CPU/GPU, latency, reliability, and price semantics are unresolved. Their response `cost` field is not verified billing evidence. Approved Stages 03, 10, and 14; ADR-007.
7. Conditional publisher/delivery and workflow roles are not deployed initially. No broker, workflow engine, feature store, vector store, model-serving product, service mesh, or agent runtime is justified. Approved Stages 05, 08, 09, 11, and 15.
8. Numeric tenant counts, traffic, payload/result sizes, data growth, concurrency, latency, freshness, availability, RPO/RTO, retention, model-quality targets, provider prices, budget, and delivery deadline are not approved. Approved Stages 02, 13–16.
9. Stage 16 defines isolated load, soak, resilience, migration, and recovery lanes. A one-server run produces curves and failure points, not capacity or production-fitness approval. Approved Stage 16.

### Prototype observations retained only as calibration fixtures

| Capability | Recorded observation | Valid use | Forbidden inference |
|---|---|---|---|
| Churn | Bundled sample has 39,393 rows; prototype writes batches of 1,000; XGBoost uses 300 trees; daily tenants are sequential | Reproduce a migration benchmark and compare target pipeline behavior | Production customer count, batch optimum, model choice, cadence, or server size |
| RFM | Prototype fetches customer lists in batches of 2,000, writes 1,000, has a five-row minimum, and runs tenants sequentially | Compatibility fixture and low-volume correctness point | Production eligibility floor, concurrency, or capacity limit |
| NPT | Recorded fixture: 21,567 transactions, 292,873 snapshots, 51,320 eligible rows, 17,910 RSF-routed rows, 2,217 customers; another 27,296-row snapshot stage took about 5–22 seconds with database-write sensitivity; chunks of 1,000 | Benchmark fixture for amplification, stage timing, and persistence sensitivity | Production throughput/SLO or approved algorithm/window/floor |
| REC | Prototype reads 200 days, requires 200 valid transactions and five sellable products, and runs CPU-intensive stages sequentially; core generation uses no GPU | Migration fixture for transaction/product/candidate scaling | Production minimums, cadence, algorithm, or hardware |
| Synapse | Each interface returns a cost field; no token/model/provider limits or measured runtime are documented | Interface-contract fixture only | Provider bill, token budget, throughput, latency, CPU/GPU, or production cost |

## Temporary assumptions and explicit blocks

Stage 17 introduces no new temporary assumption and does not silently extend expired deployment uncertainty.

| ID/block | Classification | Capacity/cost effect | Validation/expiry |
|---|---|---|---|
| `A-01-SCALE` | Retained approved assumption | All quantities remain symbols or measured distributions; no production sizing/SLO/cost approval | Release-scoped workload evidence and approved target register |
| `A-04-OWNERSHIP` | Retained accepted assumption | Logical owners may collect evidence; missing named accountable authorities blocks production operation and sensitive admission | Stage 20/production/extraction |
| `DEPLOYMENT_ENVIRONMENT_BLOCKED` | Accepted block | The one-server baseline may be benchmarked, but no production host, network, backup, telemetry, recovery, or operating-cost claim passes | Exact environment, runbooks, targets, tests, and approval |
| Four `MIGRATION_BLOCKED` profiles | Accepted ADR-007 states | Prototype measurements cannot size a production capability until its target pipeline and scientific contract exist | Profile-specific re-entry gate |
| Three `EVIDENCE_BLOCKED` profiles | Accepted ADR-007 states | No Synapse provider/token/latency/cost capacity may be budgeted or called | Authoritative provider/profile evidence and approval |
| Eight ADR-008 security blocks | Accepted production blocks | Security controls, isolation, secrets, delivery, supply-chain and model-cache resource/cost overhead remain measurable but cannot be treated as admitted | Exact ADR-008 exit evidence and approval |

## Workload symbol and input-status register

All rates use one declared measurement interval `Δ`. Percentiles and peak windows must name their calculation method; averages cannot substitute for peaks.

| Symbol | Meaning | Current status | Measurement source/owner |
|---|---|---|---|
| `T_a`, `T_p` | active tenants in `Δ`; simultaneously active peak tenants | Unknown | Control/usage ledger; platform owner |
| `R_o` | admitted request rate for operation `o`, by outcome and tenant tier | Unknown | Edge plus owner usage records |
| `B_in,o`, `B_out,o` | admitted request and response/reference bytes | Unknown | Contract-safe request/result metadata |
| `C_t`, `X_t`, `P_t` | customers, valid transactions in lookback, and sellable products for tenant `t` | Unknown | Ready dataset/catalog manifests |
| `D_s` | accepted raw bytes/rows from source `s` per `Δ` | Unknown | Ingestion/raw owner records |
| `a_l` | byte/row amplification from raw through canonical, curated, feature, snapshot, result, and evidence layer `l` | Unknown; NPT fixture proves it can be material | Benchmark manifests |
| `J_p`, `S_p`, `c_p` | job arrivals, measured service-time distribution, and safe concurrency for pool/operation `p` | Unknown | Job/attempt records plus resource telemetry |
| `E_k`, `F_k` | committed facts of event class `k`; admitted subscriber/delivery fan-out | Event path inactive; future values unknown | Owner/outbox/delivery records |
| `M_b`, `W_b` | resident artifact bytes and peak runtime working memory for bundle `b` | Unknown | Model-load benchmark and process high-water mark |
| `U_cpu,o`, `U_gpu,o` | CPU/GPU seconds per successful unit of operation `o` | Unknown; current core capabilities are CPU-oriented | Isolated capability benchmark |
| `Tok_in,o`, `Tok_out,o`, `Call_o` | provider input/output tokens and calls per Synapse operation | Unknown and blocked | Future admitted provider usage evidence |
| `H_x`, `v_x`, `r_x` | retention duration, version/correction multiplier, replication/backup multiplier for asset class `x` | Unknown and governance-blocked | Approved policy plus storage inventory |
| `P_u` | price per resource/provider unit `u`, effective date/currency/tax/commitment | Unknown | Selected provider or owned-host cost evidence |
| `O_h` | sponsor human operating hours by deploy, backup, restore, incident, patch, evidence task | Unknown | Time ledger/runbook exercise |

## Symbolic capacity model

### Tenant, request, and synchronous latency model

| Estimate | Formula | Input status and sensitivity | Bottleneck indicator | Scale/admission trigger |
|---|---|---|---|---|
| Peak admitted request rate | `R_peak = Σ_o R_o,peak` | All rates unknown; sensitive to tenant simultaneity and polling cadence | Edge saturation, DB pool waits, latency/error knee | First bound request/polling behavior; scale API only if approved objective still fails |
| Request network rate | `Net_req = Σ_o R_o × (B_in,o + B_out,o + protocol overhead_o)` | Sizes/rates unknown; large objects must use references | NIC/ingress/egress saturation or oversized payload rejection | Preserve object-reference path; do not enlarge JSON limits without evidence |
| Synchronous latency | `L_sync,o = L_edge + L_auth + L_control + L_owner-read + L_capability + L_finalize + L_response` | Every term measured separately; Synapse excluded while blocked | p-tail dominated by DB/provider/model load or finalization | Operation remains async/unavailable unless complete measured distribution meets approved target |
| Polling load | `R_poll = Σ_consumers active_jobs × poll_frequency(policy)` | Policy unknown and client behavior highly sensitive | Read pressure grows with job duration/backlog | Bound/adapt polling and page queries before adding push infrastructure |
| Tenant fairness | `share_t,p = admitted_work_t,p / total_admitted_work_p` plus wait/deadline distribution | Tier/quota policy unknown | One tenant drives queue age/resource starvation | Transactional pool/tenant caps and aging first; additional capacity only after policy proof |
| Aggregate network rate | `Net_total = Net_req + Net_object + Net_pg_remote + Net_model + Net_telemetry + Net_backup_restore + Net_delivery + Net_provider` | Topology, rates and bytes are unknown; remote PostgreSQL participation depends on placement; delivery/provider terms are zero while blocked | NIC/bandwidth/latency/egress-cost knee, backup or telemetry interference | Bound/reference/compress/schedule first; change placement or bandwidth only after an approved objective repeatedly fails |

No operation is admitted as synchronous merely because its mean is low. It needs bounded input, dependency, model/provider, tail-latency, timeout, cancellation/ambiguity, and concurrency evidence under an approved operation profile.

### Job, concurrency, and backlog model

For pool `p`, offered utilization is:

`ρ_p = (λ_p × E[S_p]) / c_p`

where `λ_p = J_p / Δ`. This is a diagnostic, not a promise: service-time variance, database contention, tenant fairness, leases, retries, finalization, memory, and dependency limits must also pass.

| Estimate | Formula | Input status and sensitivity | Bottleneck indicator | Scale trigger |
|---|---|---|---|---|
| Required completions | `throughput_required,p = arrivals_p + backlog_reduction_target_p / window` | Arrival and drain target unknown | Oldest-ready age/deadline risk rises | Approve drain objective, then tune batch/concurrency |
| Effective work | `work_p = logical_jobs_p × (1 + retry_attempts_per_logical_job_p + replay_recovery_attempts_per_logical_job_p)`; both amplification terms are dimensionless attempt-equivalents per logical job | Retry/recovery distributions unknown | Attempt amplification, poison or finalization retries | Fix failure source/idempotency before capacity addition |
| Safe concurrency | `c_safe,p = min(c_cpu, c_mem, c_db, c_io, c_dependency, c_policy)` | Every bound measured on exact release/environment | Throughput stops improving or errors/tails rise | Cap at measured knee; split role/host only for persistent contention |
| Queue completion | `L_job = L_admission + L_queue + Σ stage_time + L_finalize` | Stage distributions and objective unknown | Queue/finalize dominates execution | Index/query/checkpoint/batch/pool remedies before broker |
| Lease profile | `lease > measured heartbeat jitter + bounded checkpoint/commit interval`, subject to recovery target | Values unknown; cannot derive from mean runtime | False expiry or slow recovery | Per-operation benchmark and fault tests required before activation |

Pools remain logical until measured dependency, library, memory, CPU/GPU, security, or contention evidence requires process/host separation. Increasing concurrency without checking PostgreSQL connections, locks, object I/O, memory, and external quotas is prohibited.

### Data volume and storage-growth model

Capacity measurement preserves the four independent acceptance authorities. For each ingestion run, structural and semantic stages report input/output/reject/quarantine rows and bytes plus CPU/RSS/I/O/time. Dataset readiness separately reports candidate/published versions, lineage, freshness and policy evidence. Capability eligibility separately reports eligible/ineligible units, reason, required feature/model/config versions and scientific threshold policy. Work from a rejected or not-ready layer contributes measured waste/recovery cost but never becomes admitted downstream demand. A generic `valid_rows` or `ready=true` count cannot merge these layers.

| Acceptance stage | Capacity formula/dimensions | Input status | Owner and bottleneck | Downstream admission/scale trigger |
|---|---|---|---|---|
| Structural validation | `rows_struct_out = rows_in × selectivity_struct`; measure input/output/reject/quarantine bytes, parse/decompress/checksum CPU/RSS/scratch/I/O and stage time | Source shapes, error/selectivity and resource coefficients unknown | Source/data owner; parser, memory, object and quarantine I/O | Structural failure publishes nothing; tune streaming parse/batch/object shape before added compute |
| Semantic validation | `rows_sem_out = rows_struct_out × selectivity_sem`; measure lookup/join/dedupe/correction rows/bytes, reference-state reads, CPU/RSS/DB/object I/O and stage time | Domain rules, duplicate/correction rate, selectivity and coefficients unknown | Data/domain/governance owner; joins, references, DB locks and correction amplification | Semantic ambiguity quarantines/no canonical truth; tune indexes/partition/reference data before scale |
| Dataset readiness/publication | `ready_versions = candidates × readiness_pass_fraction`; measure candidate/published/orphan bytes and objects, lineage/quality/policy evidence, catalog commit and recovery time | Freshness/quality/policy thresholds, pass fraction and version churn unknown | Catalog/data owner; cross-store publication, evidence and object count | Not-ready publishes no `READY`; compact/partition/reconcile before product change |
| Capability eligibility | `eligible_units_cap = ready_units × eligibility_fraction_cap`; measure eligible/ineligible/fallback units/reasons, feature/model/config reads, CPU/RSS/I/O/time | Scientific definitions/thresholds/fractions unknown and profiles blocked | Capability owner; feature materialization, model availability and scientific checks | Ineligible units do not execute/fabricate; optimize exact target pipeline before role/hardware scale |

| Asset | Growth formula | Input status/sensitivity | Primary bottleneck | Scale/retention trigger |
|---|---|---|---|---|
| Immutable raw | `G_raw = Σ_s (D_s / Δ) × H_raw,s × v_raw,s × r_raw,s` | Source rates, correction/version and policy unknown; `H` uses the same time unit as `Δ` | Disk/object capacity, upload time, backup/governance | Object storage is baseline seam; product/placement selected only after measured volume/policy |
| Canonical/curated | `G_curated = Σ_s,l (D_s / Δ) × a_s,l × H_l × v_l × r_l` | Layer amplification unknown; `a` is output bytes per input byte and `H/Δ` is the retained interval count | Transform I/O, duplicate copies, small objects | Compact/partition/reference first; product change only after benchmark |
| Feature/snapshot data | `G_feature = Σ_cap run_rate_cap × rows_per_run_cap × bytes_per_row_cap × H_feature,cap × v_cap × r_cap` | Run rate and all shape/retention coefficients unknown; highly sensitive to temporal snapshots | Snapshot generation, object count, memory and retention | Reduce columns/materialization/checkpoint safely; later engine/language only with profile proof |
| Results | `G_result = Σ_o execution_rate_o × output_units_per_execution_o × bytes_per_unit_o × H_result,o × v_o × r_o` | Execution rate, customer/product cardinality, retention and debug/explanation size unknown | Result commit, retrieval, retention | Keep large results by reference; paginate/project; approve retention |
| Model/evaluation artifacts | `G_model = Σ_cap bundle_creation_rate_cap × bytes_per_bundle_and_evidence_cap × H_model,cap × v_cap × r_cap` | Creation rate, bundle/evidence sizes and retention unknown | Integrity scans, download/load, retention | Lifecycle cleanup only under policy; no mutable overwrite |
| PostgreSQL owner state | `G_pg = Σ_tables rows × (row + index + visibility overhead) + WAL/maintenance headroom` | Row counts/widths/indexes unknown | Working-set misses, WAL, vacuum, locks, backup/restore | Measure queries/bloat/WAL; archive large payloads; partition only from evidence |
| Audit/usage | `G_evidence = logical_effect_rate × records_per_effect × bytes_per_record × H_evidence × r_evidence` | Effect rate, record width, retention and copy factor unknown; mandatory completeness | Write amplification and retention | Schema/minimization/index/partition policy before separate ledger product |
| Diagnostic telemetry | `G_tel = Σ_signals rate × bytes × sampling × H` | Cardinality/sampling/retention unknown | Export bandwidth, backend cost, local buffer pressure | Bounded dimensions/sampling/aggregation; never drop mandatory audit |
| Backups | `G_backup = Σ_x protected_bytes_x × backup_generation_multiplier_x` | Frequency/retention/dedup unknown | Backup window, storage, restore duration | Governed policy and restore evidence required; no RPO/RTO claim |

Peak storage headroom is reported separately from retained growth: `S_peak = retained_live + staging + current_candidates + quarantine + checkpoints + orphan_reconciliation + WAL/temp + backup_restore_workspace`. Every term has logical bytes, physical-copy factor and lifetime; it is never hidden inside a generic retention multiplier.

Capacity reports must show logical bytes, physical bytes, object counts, row counts, index/WAL amplification, version count, retention, backup multiplier, growth per interval, deletion obligations, and restore duration separately. One aggregate “database size” is insufficient.

### Per-capability workload model

| Profile | Dominant dimensions/formula | Input status | Sensitivity and expected bottleneck | Required measurement before sizing | Scale trigger/current release effect |
|---|---|---|---|---|---|
| Churn | `work ≈ f(C_t, X_t/lookback, features, trees, bundle load, result rows)`; memory includes frames + transform + model + result | Target shape/resource coefficients unknown; prototype observations only | Customer/transaction/frame size; tree/model settings; tenant sequentiality; writes | Stage timing, CPU seconds, peak RSS, temp/object/DB I/O, bundle bytes, result bytes under target pipeline | Tune/partition/bound first; split/size only after target miss; remains `MIGRATION_BLOCKED` |
| RFM | `work ≈ aggregate(X_t) + scale/PCA/cluster(C_t × features) + persist(C_t)` | Target algorithm/shape/resource coefficients unknown | Transaction aggregation, clustering working set, per-run fitting/mapping, writes | Same plus cluster/evaluation stability across dataset sizes; explicit lifecycle profile | Tune aggregation/lifecycle first; split/size only after target miss; remains `MIGRATION_BLOCKED` |
| NPT | `snapshot_rows ≈ f(X_t, windows/horizons/calendar)`; train/infer work by snapshots/features/routing; persist customers | One historical fixture; target coefficients and workload unknown | Temporal snapshot amplification, DB writes, CLF/RSF bundles, sequential loops | Amplification curve; per-stage CPU/RSS/I/O; PIT materialization; bundle sizes; eligible/served ratios | Reduce/materialize/checkpoint appropriately first; split/language only after target miss; remains `MIGRATION_BLOCKED` |
| REC | `candidate_work ≈ Σ_customers candidate_count_t`; ranking may approach customer-product interactions depending approved algorithm | Target algorithm/cardinality/resource coefficients unknown | Customer × sellable-product/candidate cardinality, transaction history, ALS/native threads, metadata/embedding path | Candidate/ranking scaling, quality-versus-candidate trade-off, peak RSS/CPU/I/O, result top-k bytes; GPU benchmark only if path requires | Bound candidates/partition/tune first; GPU/role split only after quality-preserving target miss; remains `MIGRATION_BLOCKED` |
| Synapse chatbot | `provider_cost = calls × (Tok_in×price_in + Tok_out×price_out + other units)`; latency includes provider queue/generation | Every provider/model/token/rate/price coefficient unknown and blocked | History/context size, model/provider, retries, output bound and concurrency | Authoritative provider/model/tokenizer, call graph, limits, price/version, latency/error/cost distribution, safety overhead | No sizing/call; re-enter only after evidence/security gate; `EVIDENCE_BLOCKED` |
| Synapse message | Same provider formula; request length/offer/context/output constraints | Every provider/model/token/rate/price coefficient unknown and blocked | Model/prompt/output cap, request mix and retries | Same plus quality/safety corpus and channel-length behavior | No sizing/call; re-enter only after evidence/security gate; `EVIDENCE_BLOCKED` |
| Synapse verifier | Same provider formula over payload/references/config/metadata | Every provider/model/token/rate/price coefficient unknown and blocked | Array/payload/token growth and false decision costs | Same plus policy-reference coverage; remains advisory | No sizing/call; re-enter only after evidence/security gate; `EVIDENCE_BLOCKED` |

Scientific quality and resource efficiency are joint gates. A faster or cheaper pipeline does not pass if its approved quality, safety, reproduction, isolation, or fallback contract fails.

### Feedback, drift, evaluation, and candidate-retraining workload

| Estimate | Formula | Input status/sensitivity | Bottleneck and trigger | Authority constraint |
|---|---|---|---|---|
| Feedback retained growth | `G_feedback = feedback_event_rate × bytes_per_event × H_feedback × v_correction × r_copy` | Arrival, attribution delay/window, duplicates, late/corrections, retention and copies unknown | Linkage/index/storage and delayed correction amplification; tune contract/index/partition before new infrastructure | Missing feedback is unknown, never a negative outcome |
| Outcome attribution work | `work_attribution = feedback_event_rate × candidate_links_per_event × correction_multiplier` | Link density/window and correction rate unknown | Join/reconciliation CPU/DB/object I/O; benchmark by delayed and corrected cohorts | Only authoritative governed outcome contracts participate |
| Drift/evaluation compute | `drift_compute_rate = evaluation_scan_rate × dataset_units_scanned × compute_units_per_dataset_unit` | Cadence, cohorts, metrics, thresholds, scan size and CPU/I/O coefficients unknown | Scan I/O/CPU; schedule in bounded capability pool and scale only after an approved evaluation deadline repeatedly fails | Drift evidence is advisory and cannot promote |
| Drift/evaluation evidence growth | `G_drift_reports = report_creation_rate × bytes_per_report × H_report × v_report × r_copy` | Report rate/size, retention, corrections/versions and copies unknown | Evidence storage, index and reconstruction cost; govern/minimize before new product | Reports remain immutable evidence and cannot authorize promotion |
| Candidate retraining arrivals | `J_train_candidate = authorized_trigger_rate + approved_schedule_rate + explicit_request_rate`, deduped by policy identity | Every trigger/cadence and target profile unknown | Training queue/resource overlap and repeated versions; split/accelerate only after approved objective miss | A threshold may submit candidate work only; training/evaluation/promotion/assignment stay separate |

### Model memory, CPU, and GPU model

| Estimate | Formula | Input status/sensitivity | Decision rule |
|---|---|---|---|
| Resident model memory | `M_resident = Σ simultaneously_loaded_b (M_b + runtime_overhead_b) + cache_metadata` | Bundle sizes, sharing, eviction and concurrency unknown; cache blocked | Start with load-on-demand/exact assignment; enable cache only after ADR-008 isolation evidence and measured benefit |
| Worker peak memory | `M_worker,p = runtime_base + max_concurrent Σ (input_working_set + transforms + model + output_buffer + library_overhead)` | Pandas/snapshot/candidate copies may dominate | Benchmark peak RSS and copy amplification; bound batch/concurrency below OOM/failure knee |
| CPU demand | `cores_equiv = Σ_o arrival_rate_o × CPU_seconds_per_unit_o / approved_utilization_guard` | No rates or CPU/unit measured | Profile algorithm/query/serialization first; vertical size then role split/replica |
| GPU demand | `gpu_time = Σ_o arrival_rate_o × GPU_seconds_per_unit_o` | Core evidenced capability paths do not require GPU; Synapse internals unknown | No GPU. Require supported operation, benchmarked quality/latency/cost benefit, utilization and CPU alternative comparison |

Python remains the baseline. Rust is reconsidered only when profiling attributes an approved-target failure to Python runtime/CPU/memory behavior after algorithmic, query, serialization, batching, vectorization, and concurrency remedies; a representative Rust prototype must demonstrate material end-to-end benefit including integration, safety, build, observability, and sponsor maintenance cost. A data-lake product is reconsidered separately when the approved object/catalog/transform/query/retention workload cannot meet targets with the existing adapter and PostgreSQL metadata model.

### Conditional event and delivery model

Current admitted production event and external-delivery volume is zero because publisher/delivery roles are absent and `EXTERNAL_DELIVERY_BLOCKED` remains active. Contract/fault tests still run.

If a named subscriber is later admitted:

- `E_publish = Σ_k committed_facts_k × admitted_subscribers_k`;
- `E_attempt = E_publish × (1 + retry_rate + replay_rate)`;
- `G_outbox = intent_rate × average_record_bytes × retention`;
- delivery bandwidth and provider cost include payload, signatures, response, retries, dead-letter and audit evidence;
- fan-out, ordering, poison, ambiguity, destination quotas, egress and replay must be measured independently.

A broker is reconsidered only when an admitted multi-subscriber/fan-out workload cannot meet an approved objective after PostgreSQL outbox indexing, batching, bounded handlers, and role scaling, and the operational/cost burden is approved.

## Cost model

### Total-cost formula

For an evaluation window:

`C_total = C_host + C_pg + C_object + C_backup + C_network + C_security + C_observability + C_build_artifact + C_provider + C_LAB + C_human_ops + C_risk_change`

where each term records quantity, unit, unit price, currency, price/version date, tax/commitment assumptions, allocation method, and retry/recovery amplification. Unknown price is `UNKNOWN`, never zero.

| Driver | Quantity basis | Current disposition | Sensitivity/cost guard |
|---|---|---|---|
| Linux compute | provisioned CPU/RAM/disk/runtime hours or owned-hardware depreciation, power and maintenance | Host/product not selected; no price | Peak memory/CPU, always-on roles, overprovisioning; benchmark before purchase |
| PostgreSQL | compute, storage, IOPS, backup, transfer, administration | Same server baseline logically allowed; exact deployment blocked | Jobs/audit/WAL/index/restore load; managed-versus-self-host includes sponsor time |
| Object/lake storage | capacity by class/tier, operations, retrieval, egress, backup/replication | Adapter required; product/placement not selected | Retention/version amplification and many-small-object behavior |
| Network | ingress, egress, inter-role/provider transfer | Topology/provider unknown | Results/objects/telemetry/provider context; co-location does not waive security |
| Security/governance controls | identity/trust, secret/key, policy/audit, scanning/signing, deletion/reconciliation operations and accountable review time | Exact mechanisms, rates and prices unknown; eight security blocks remain active | Control/evidence volume and sponsor/reviewer time; controls cannot be removed to meet cost |
| Observability | events/spans/series, cardinality, ingestion, retention, query | Product/policy unknown | Sampling/retention/cardinality; audit is not discardable telemetry |
| Build/supply chain | CI minutes, artifact/image storage, scans/signing, test lanes | Tool/vendor unknown | Rebuild/test frequency and retained releases/evidence |
| Backup/recovery | backup bytes/operations, recovery environment/time, exercises | Policy and RPO/RTO unknown | Version/retention multiplier and sponsor exercise hours |
| External/LLM provider | calls, tokens/units, retries, moderation/safety and egress | Synapse blocked; current admitted cost zero | Context/output/call count/model price; response `cost` must reconcile to provider evidence |
| LAB evidence consumption | release-scoped package bytes/transfers, validation runs, retained evidence and accountable review time | LAB operating contract, volume, authority and price are unknown; ordinary participation is evidence-consumer only | Release frequency, package size, reruns and retention; LAB cannot become promotion authority through cost allocation |
| Human operation | deploy, patch, monitor, backup/restore, incident, data/model review, release approval hours | Sponsor with AI assistance; no 24/7 team | Tooling may reduce toil, but AI cannot own credentials/approval/accountability |
| Change/risk | migration, lock-in/egress, dual-run, downtime, failure and recovery exposure | Not monetized without evidence | Must be shown qualitatively in build/buy/managed comparisons |

### Cost attribution

Usage is recorded before pricing. For job/operation `o`, attributable quantity includes API/DB/object/provider units, CPU/GPU seconds, peak/allocated memory time, result/evidence bytes retained, delivery attempts, and recovery/retry amplification. Shared baseline cost allocation requires an approved rule—equal, tenant-weighted, usage-weighted, reserved capacity, or sponsor-funded. Stage 17 chooses none. Metering is not invoicing.

### Decision scenarios without price claims

| Scenario | What is evaluated | Current conclusion |
|---|---|---|
| Developer/local | Contract/unit/component work with synthetic fixtures; no production data/credentials | Required; not production cost evidence |
| Single Linux validation host | Coordinated API/scheduler/worker/maintenance behavior, PostgreSQL/object adapter, mixed-load curves and recovery drills | Approved benchmark baseline; no HA or production capacity claim |
| Single-server production candidate | Exact environment, workload, targets, security, backup/restore, sponsor runbooks and costs | `DEPLOYMENT_ENVIRONMENT_BLOCKED`; cannot be approved now |
| Vertical upgrade | Additional CPU/RAM/storage on simple host | First infrastructure remedy only after profiling/tuning and target evidence |
| Role/host split or replicas | Isolate API/data/ML/provider contention or meet failure-domain/availability objective | Conditional on measured target failure and operability/cost approval |
| Managed PostgreSQL/object/telemetry | Compare administration/recovery burden and target fit against self-hosted | No selection; include sponsor hours and lock-in/egress |
| GPU/Rust/lake product/broker/Kubernetes | Specialized acceleration, runtime, data processing, dispatch, or fleet control | Not justified; each has a separate measured trigger below |

## Benchmark and measurement plan

Every benchmark uses the exact release digest, Python/dependency versions, PostgreSQL version/config/schema/index state, process/container mode, Linux environment revision, dataset/model/config/policy versions, warm/cold state, concurrency, fixture provenance, and repetitions. Reports retain distributions, peak resources, failures, correctness/isolation evidence, and raw measurement references—not only averages.

| ID | Workload/fault lane | Variables swept | Required measurements | Gate/use |
|---|---|---|---|---|
| `BM-17-01` | API/auth/control/result polling | operation mix, payload/page size, tenants, clients, poll cadence, warm/cold | throughput, latency distribution, errors/outcomes, CPU/RSS, DB connections/queries/locks, bytes | Sync admission, API/poll bounds |
| `BM-17-02` | PostgreSQL job/scheduler | arrivals, service times, pools, concurrency, retries, finalization, tenant mix | queue age/depth, claim/finalize, lock/WAL/index/bloat, connections, fairness, duplicate/fence outcomes | Safe concurrency/backlog and broker trigger |
| `BM-17-03` | Ingestion raw-to-ready/backfill | bytes/rows/files/object sizes, schema errors, corrections, parallelism | stage latency, amplification, CPU/RSS, DB/object I/O, orphan/quarantine, publish correctness | Batch/checkpoint/object/data-engine decision |
| `BM-17-04` | Churn/RFM/NPT/REC target batch inference | customers, transactions/lookback, products/candidates, features, partitions, concurrency | per-stage CPU seconds, wall distribution, peak RSS/temp/disk, DB/object bytes/ops, artifact load, result size, correctness | Per-profile sizing only after migration gate evidence |
| `BM-17-05` | Training/evaluation/reproduction/feedback/drift | dataset/snapshot/artifact sizes, trials/configs, parallelism, cold/warm load, feedback arrival/late/duplicate/correction/attribution delay, drift scan cadence/units, candidate-trigger rate | resource/time/cost distributions, artifact/evidence/report/feedback growth, attribution/reconciliation work, candidate-job arrivals, reproducibility/quality | ML role/hardware, feedback/drift capacity and promotion evidence; no automatic promotion |
| `BM-17-06` | Model load/cache | bundles, size, tenant/capability/assignment mix, revocation, concurrency | load latency, peak/resident memory, cache hit benefit, isolation/integrity | Cache remains blocked until benefit and ADR-008 gate pass |
| `BM-17-07` | Storage/backup/restore | DB/object/evidence bytes, versions, object count, backup generations, mismatched points | backup window, restore/reconcile time, space/IO, loss/ambiguity, sponsor steps | RPO/RTO and storage/managed-service decisions |
| `BM-17-08` | Telemetry/audit/usage | signal rate/cardinality/sampling/export outage, mandatory evidence rate | overhead, buffer/drop/export lag, storage/cost, redaction and completeness | Observability policy/product sizing |
| `BM-17-09` | Conditional delivery | facts, subscribers, payload, receiver latency/failure, retries/replay | outbox/attempt backlog, DB/network/cost, ambiguity/dedupe/dead-letter truth | Only after named consumer; delivery/broker decision |
| `BM-17-10` | Synapse admitted sandbox | payload/history/reference sizes, token limits, model/provider, concurrency, failures | calls/tokens, latency/error/safety/quality/cost distribution, egress | Only after evidence/security re-entry; no current provider call |
| `BM-17-11` | Mixed one-server soak | admitted API, polling, ingestion, jobs, capability fixtures, PostgreSQL, telemetry, backup overlap | resource curves, latency/queue/fairness, disk/WAL, leaks, thermal/resource saturation, invariant failures | Establish contention/failure knee; never HA proof |
| `BM-17-12` | Cost reconciliation | exact measured resource/provider units and price snapshot | per-operation/tenant/shared quantities, retries, idle baseline, sponsor time, variance | Budget/options only after scope and prices |

Production sizing requires representative low/typical/approved-peak and burst windows, tenant-size distribution, seasonality, growth horizon, failure/recovery load, and headroom policy. No generic multiplication factor is assumed.

## Sensitivity and bottleneck register

| Driver | Sensitive dimensions | Likely constrained seam to measure | Simplest response first |
|---|---|---|---|
| Tenant simultaneity | `T_p`, polling, schedules aligned in time | API/DB pool, queue fairness | Stagger schedules, quotas, admission, indexes |
| Transaction growth/lookback | `X_t`, retention, corrections | object bytes, transforms, snapshots, DB/object I/O | Incremental/versioned partitions, projection, checkpoint/batch tuning |
| Snapshot/window expansion | horizons/windows/features | NPT/feature amplification, memory/disk | Measure materialization; reduce approved redundant work |
| Customer/product cardinality | `C_t × candidate_count`, `P_t` | REC CPU/RAM and result size | Candidate bounding/partitioning under quality gate |
| Retry/recovery rate | attempts/logical work | queue, DB, provider and cost amplification | Fix faults/idempotency/reconciliation before scaling |
| Model bundle count/size | active tenants/assignments, cold starts | worker RSS/load latency/object I/O | Exact load-on-demand; bounded authorized cache only after gate |
| Retention/version policy | `H`, correction and backup multipliers | object/DB/evidence cost and restore | Governance-approved lifecycle/minimization, never silent deletion |
| Telemetry cardinality | labels, tenants, traces, retention | exporter/backend/resource/cost | Safe dimensions, aggregation, sampling; preserve audit |
| LLM context/output/calls | tokens, provider/model, retries | external latency/cost/safety | Explicit caps/minimization/call graph after provider admission |
| Single-host co-location | overlapping API/DB/worker/backup/telemetry peaks | CPU/RAM/disk/IO/failure domain | Schedule/isolate/bound work, vertical size, then split roles/hosts |
| Sponsor operating capacity | alerts, patches, deploys, restores, incidents | runbook completion and recovery time | Automate reproducibly, reduce component count, managed option only if evidence supports |

## Evidence-triggered scaling and build/buy ladder

Each trigger requires an approved objective, repeatable representative benchmark, correctness/security evidence, cost comparison including sponsor time, and a recorded decision. A single noisy run or prototype log is insufficient.

| Change | Measurable trigger | Required comparison | Current disposition |
|---|---|---|---|
| Query/code/batch tuning | Any measured bottleneck | Before/after correctness and resource curve | First response |
| Vertical server sizing | Tuned baseline cannot meet approved peak/headroom on current known host | Candidate CPU/RAM/storage options and cost | Conditional; no purchase proposed |
| Split data/ML/API role or second host | Co-location causes repeatable target/invariant failure and isolated run removes it; or approved failure-domain objective requires it | Same release with/without split, DB/network effect, sponsor burden | Conditional |
| API/worker replicas | Safe concurrency on one role is insufficient and shared dependencies have capacity | Replica curve, scheduler/job safety, routing, cost | Conditional |
| Managed PostgreSQL/object/telemetry | Approved recovery/availability/security target or sponsor workload cannot be met safely self-hosted | Self-hosted versus managed TCO, controls, restore, lock-in/egress | Conditional |
| Rust component | Profile proves Python runtime—not algorithm/query/data design—is the persistent constraint | Representative Python versus Rust end-to-end quality/resource/maintenance evidence | Not selected |
| Additional data-lake/query product | Object adapter + catalog + Python transforms cannot meet approved data/query/retention target | Existing baseline versus product, migration/governance/ops cost | Not selected |
| GPU | Approved training/inference path gains necessary quality/latency/cost benefit with usable utilization | CPU versus GPU end-to-end, queueing, memory, hosting, fallback | Not selected |
| Broker | PostgreSQL job/outbox path misses approved dispatch/fan-out target after tuning and role scaling | DB path versus broker semantics/operations/cost | Not selected |
| Kubernetes | Measured fleet/placement/rollout/policy needs exceed simple process/container/VM operation | Simple runtime versus Kubernetes including sponsor/on-call burden | Not selected |
| Service extraction | ADR-003 ownership/deployment/scale trigger passes | Modular-monolith versus extraction reliability/cost/team evidence | Not selected |

### Explicit anti-overengineering disposition

| Candidate | Current classification | Evidence required to reconsider |
|---|---|---|
| Standalone feature store | Rejected now | Governed cross-capability feature reuse plus measured online/offline skew, serving latency or lifecycle need that existing owned datasets/materializations cannot meet |
| Standalone model registry/tracker/drift platform | Rejected now | Current PostgreSQL/object registry/evaluation contracts repeatedly miss an approved lifecycle, scale, lineage or operations target after tuning |
| Streaming/CDC platform | Rejected now | Authoritative source contract plus measured freshness/volume requirement that push/micro-batch/object ingestion cannot meet |
| Vector database/retrieval | Rejected now | Approved governed corpus and use case with semantic retrieval quality/latency objective unmet by simpler bounded retrieval; Stage 11 conclusion remains unchanged |
| Agent framework/runtime | Rejected now | Full approved Stage 11 re-entry gate, including irreducible autonomy, security, execution, evaluation, ownership and cost evidence |
| MCP | Rejected now | Approved agent-to-tool interoperability need after Stage 11 re-entry; ordinary typed ports remain simpler |
| A2A | Rejected now | At least two justified approved agents with genuine delegation/handoff semantics after Stage 11 re-entry |
| GPU platform | Rejected now | Approved workload demonstrates necessary quality/latency/cost benefit and sustainable utilization over CPU |

## Production capacity-admission record

Stage 17's logical model may pass while production capacity remains blocked. A production operation must provide one immutable profile containing:

1. release-scoped capabilities, consumers, paths, tenant-size distribution and growth horizon;
2. request/job/event/data arrival distributions, bursts, schedules and seasonality;
3. payload/result/data/model sizes and retention/version/backup policies;
4. operation classes, deadlines, concurrency, retry, lease, fairness and partial/fallback policies;
5. latency, freshness, completion, availability, recovery, quality, security and cost objectives with owners;
6. exact environment and price evidence;
7. BM-17 benchmark results at representative and fault/recovery load;
8. resource headroom and saturation policy, not a guessed universal percentage;
9. per-layer backup/restore/reconciliation evidence and sponsor-run runbooks;
10. cost quantities, allocation, budget and variance/overage response;
11. all applicable ADR-007, ADR-008, and deployment block exits with named authorities;
12. explicit sponsor approval of any infrastructure purchase/build commitment.

Absent any item, the profile is `CAPACITY_ADMISSION_BLOCKED`; this is a release/profile state, not a new global architecture component or ADR. It does not replace the existing production blocks.

## Major recommendations

### R-17-01 — Adopt symbolic formulas and immutable workload profiles

**Requirement/where:** source Section 16; `ARK-NFR-007`; Stages 15–17. **Why now:** there are no authoritative quantities, but implementation needs stable measurement names and relationships. **Simplest implementation:** the symbol register plus one versioned profile per operation/release containing inputs, targets and benchmark evidence. **Alternative:** choose conventional small/medium server numbers. **Why rejected:** fabricated precision could cause unsafe or wasteful commitments. **Trade-off:** production sizing waits for evidence. **Reconsideration:** formulas remain; measured values replace `UNKNOWN`.

### R-17-02 — Benchmark the coordinated single-server baseline before distribution

**Requirement/where:** ADR-009; Stage 15 scaling ladder; Stage 16 load plan. **Why now:** the approved target is the cheapest credible place to expose real bottlenecks. **Simplest implementation:** exact-release mixed and isolated BM-17 lanes on one Linux host with real PostgreSQL/object-compatible semantics. **Alternative:** preselect multiple services, managed platforms or Kubernetes. **Why rejected:** no measured target failure, fleet, availability or operating-team evidence. **Trade-off:** one failure/resource domain and no HA claim. **Reconsideration:** an approved objective fails after tuning, or a required failure domain cannot be met.

### R-17-03 — Treat human operating time as a first-class cost

**Requirement/where:** cost drivers; ADR-009 sponsor-operated baseline. **Why now:** a cheap self-hosted stack can be expensive or unsafe for one operator when patch, recovery and incident work is included. **Simplest implementation:** record sponsor hours and runbook outcomes beside machine/provider quantities. **Alternative:** compare infrastructure invoices only. **Why rejected:** hides the dominant constraint for a one-person operation. **Trade-off:** time tracking and qualitative risk evidence. **Reconsideration:** never omit; allocation method may evolve.

### R-17-04 — Keep specialized infrastructure behind independent measured triggers

**Requirement/where:** anti-overengineering and cost decisions. **Why now:** Rust, GPU, a lake product, broker, managed services and Kubernetes solve different problems and must not be bundled into “scale.” **Simplest implementation:** use the evidence-triggered ladder above, one decision at a time. **Alternative:** adopt a conventional ML platform stack. **Why rejected:** it adds cost, failure modes and owner burden without current workload evidence. **Trade-off:** later migration may be required if a trigger passes. **Reconsideration:** exact trigger row passes with sponsor-approved total-cost evidence.

## Decisions

- Adopt the Stage 17 symbolic capacity/performance/cost model, benchmark plan, sensitivity register, and evidence-triggered scaling ladder as the proposed baseline, subject to sponsor approval.
- Make no numeric SLO, capacity, retention, recovery, price, budget, server-size, or monthly-cost decision.
- Make no purchase/build commitment; therefore the Stage 17 workflow purchase/build approval gate is not invoked by a proposed commitment.
- Keep Python/PostgreSQL/one Linux server as the benchmark target only; do not claim production fitness or high availability.
- Keep containers optional and Kubernetes, Rust, GPU, broker, extra data-lake product, managed service, or module extraction unselected until their independent trigger passes.
- Preserve all ADR-007/008 blocks, `DEPLOYMENT_ENVIRONMENT_BLOCKED`, and `A-04-OWNERSHIP`.
- No new ADR is proposed because Stage 17 operationalizes accepted constraints without making a material technology or purchase decision.
- Keep Stage 18 unstarted until Stage 17 passes its gate and the sponsor explicitly authorizes continuation.

## Contradictions and dangerous assumptions

| ID | Finding | Resolution | Consequence |
|---|---|---|---|
| `C-17-01` | The source requests an initial capacity model while every production quantity is unknown | Use formulas/status/sensitivity/measurement gates, not guessed ranges | Logical model can complete; sizing remains blocked |
| `C-17-02` | One Linux server is approved provisionally and may be mistaken for a sized production server | It is the benchmark baseline and explicit single failure domain only | No HA/capacity/production claim |
| `C-17-03` | Prototype samples, batch sizes and timings look like measured production evidence | Retain only as migration fixtures and label every forbidden inference | No capacity/SLO extrapolation |
| `C-17-04` | Synapse response `cost` looks billable | Require provider/model/token/call/price reconciliation after admission | Current admitted provider cost is zero; capability stays blocked |
| `C-17-05` | Higher worker concurrency appears to increase throughput | Safe concurrency is the minimum of CPU, memory, DB, I/O, dependency and policy limits | No blind concurrency/autoscaling |
| `C-17-06` | Immutable/versioned data can produce unbounded storage | Retention/deletion/version/backup policies are mandatory capacity inputs | Governance absence blocks production data sizing |
| `C-17-07` | “Data lake” can be read as requiring a lakehouse product or Rust now | The approved logical object/data-layer contract is product-neutral; additional infrastructure is evidence-triggered | No premature product/language decision |
| `C-17-08` | Self-hosted can look cheaper when sponsor labor and risk are ignored | Include human hours, recovery drills and change/risk evidence | Managed/self-hosted comparison remains honest |
| `C-17-09` | Average rate/latency may hide tenant bursts and scheduled alignment | Require distributions, peak windows, seasonality and fairness | No mean-only admission |
| `C-17-10` | Scaling can be mistaken for clearing capability/security blocks | Capacity evidence is necessary but independent | All blocks remain active |
| `C-17-11` | AI assistance can be priced as an operations team or authority | AI may assist analysis/automation but cannot own credentials, approvals, incidents or hidden runbook state | Sponsor capacity remains explicit |

## Open questions

| ID | Question | Blocking? | Options | Recommended temporary disposition | Effect |
|---|---:|---|---|---|---|
| `Q-17-01` | Which capabilities, consumers and paths are in the first release? | Before production sizing | One vertical slice; subset; all admitted profiles | Benchmark contracts broadly; size only approved release scope | No production workload profile |
| `Q-17-02` | What tenant counts, size distribution, growth, geography, simultaneity and seasonality apply? | Before sizing | Measured/current forecast scenarios | Keep symbols `T_a/T_p`; collect usage/source manifests | No server count/headroom |
| `Q-17-03` | What request/job/data/event rates, payloads, schedules, bursts and retry behavior apply? | Before activation | Measured traces; contractual forecast | Instrument and benchmark; no defaults | Limits/concurrency unresolved |
| `Q-17-04` | What latency, freshness, completion, availability, RPO/RTO and recovery objectives apply per operation? | Before production | Versioned tiers or approved best effort | Measure distributions; no target | No production fitness/HA |
| `Q-17-05` | What retention/version/deletion/backup/replication policy applies per asset? | Before data/storage sizing | Governed class policy | Keep `DATA_GOVERNANCE_BLOCKED`; report inventory only | Storage/backup cost unresolved |
| `Q-17-06` | What exact Linux host/provider, PostgreSQL/object/telemetry placement and prices apply? | Before purchase/production | Existing server; rented VM; managed/self-hosted mix | Benchmark portable baseline first | No hardware/provider/monthly cost |
| `Q-17-07` | What budget, currency, horizon, allocation, variance and overage response apply? | Before cost approval | Cap; forecast; showback; none | Record resource quantities only | No budget/billing claim |
| `Q-17-08` | What sponsor support hours, maintenance windows and acceptable manual workload apply? | Before operability approval | Best effort; defined hours; external managed help | Measure runbook/incident hours; no 24/7 promise | Human capacity remains a bottleneck |
| `Q-17-09` | What named scientific/security/release authorities are required beyond the sponsor? | Before sensitive block clearance | Assign people/services; defer profiles | Preserve logical roles and active blocks | No production admission |
| `Q-17-10` | Can authoritative Synapse provider/model/token/price/reliability evidence be supplied? | Before any Synapse capacity/cost estimate | Supply and admit; scope out; remain unavailable | Remain `EVIDENCE_BLOCKED` | No provider call/budget |

## Requirements-traceability updates

| Requirement | Stage 17 evidence | Remaining acceptance evidence |
|---|---|---|
| `ARK-FR-002/003` | Push/object data-rate, layer amplification and storage-growth formulas; `BM-17-03` | Source/release volume, policy, benchmark |
| `ARK-FR-004/005/006` | Per-operation request/response/eligibility and capability workload dimensions | Approved release definitions, limits and target profiles |
| `ARK-FR-007/008` | Queue/concurrency/backlog and sync-latency formulas; `BM-17-01/02` | Measured operation policies and objectives |
| `ARK-FR-009` | Per-capability training/inference/model resource and provider formulas | ADR-007 profile re-entry plus benchmark evidence |
| `ARK-FR-010/011` | Conditional event/delivery fan-out, attempt, storage, bandwidth and cost model | Named admitted subscriber/workflow and block exits |
| `ARK-FR-012` | LAB evidence-package storage/transfer/human-cost categories | LAB operating contract and authority |
| `ARK-NFR-001/005` | Tenant/fairness and security-control resource measurements stay mandatory | ADR-008 exit evidence |
| `ARK-NFR-002/006` | Lineage/audit/usage/telemetry storage and cost formulas | Retention, price and completeness measurements |
| `ARK-NFR-004` | Retry/recovery amplification and safe-concurrency model | Measured failure distributions and policies |
| `ARK-NFR-007`, `SC-02-12` | Symbol register, formulas, benchmarks, sensitivity, triggers and capacity-admission record | Approved numeric target/workload/environment/cost profile |
| `ARK-CON-004/005` | PostgreSQL/object placement and DB-queue measurement gates | Benchmark results; no product change now |
| `ARK-CON-007` | Independent measured gates for every specialized component/purchase | Sponsor approval if a trigger later proposes commitment |

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Every source capacity dimension covered | PASS | Source-instruction coverage and symbolic model |
| No fabricated precision | PASS | Unknown inputs remain explicit symbols/statuses; no server size, target, rate or price invented |
| Every estimate has a formula | PASS | Request, job, storage, model, event and cost matrices |
| Every formula records input status | PASS | Symbol register and per-matrix status/sensitivity columns |
| Sensitivities explicit | PASS | Per-model columns and sensitivity register |
| Bottlenecks explicit | PASS | Per-model bottleneck columns and benchmark plan |
| Scale triggers explicit | PASS | Scaling/build-buy ladder |
| Measurements required before commitment explicit | PASS | `BM-17-01` through `BM-17-12`; production admission record |
| Platform and data/ML specialist reviews reconciled | PASS | Both final read-only reviews reported no unresolved critical, high, or required medium defect and recommended `PASS` |
| Workspace structure and source integrity | PASS | Exact read-only PowerShell equivalent found 0 missing required files, 25 numbered stages, and 0 checksum failures; Bash remains unavailable under the recorded WSL access limitation |
| Purchase/build approval gate | PASS — NOT INVOKED | No purchase/build commitment is proposed |
| Production blocks preserved | PASS | Assumption/block, capability, cost and decision sections |
| Stage 18 not executed | PASS | Scope and stop condition |

**Gate result: PASSED AND APPROVED.** Every requested capacity dimension is covered without fabricated precision; every estimate provides a formula, explicit input status, sensitivity, bottleneck, and scale trigger. Dimensional-unit, four-layer data, feedback/drift/retraining, network, cost-driver, per-capability, and anti-overengineering findings from both specialists were reconciled. Their final read-only reviews reported no unresolved critical, high, or required medium defect and recommended `PASS`. The sponsor explicitly approved Stage 17 on 2026-08-13. No purchase/build commitment is proposed. All production blocks remain active. Stage 18 alone is authorized.

## Downstream consequences

- Stage 18 must index accepted ADR-009 and confirm that Stage 17 made no hidden technology, vendor, capacity, SLO, or purchase decision requiring a new ADR.
- Stage 19 diagrams may show logical measurement and scaling gates but must not draw unselected products or multi-node topology as deployed.
- Stage 20 must sequence instrumentation, benchmark fixtures, target/workload discovery, sponsor-run operating measurements, block clearance, and evidence-triggered infrastructure decisions without invented dates or budget.
- Stage 21/23 must publish formulas and unresolved input registers rather than a false production bill of materials.
- Stage 22 must use Stage 17 formulas when analyzing runtime placement and concurrency.
- Stage 24 must treat missing production workload/target/environment/cost evidence as an explicit unresolved production-readiness limitation, not an architecture-completeness omission.

## Exact next-stage inputs and stop condition

Stage 17 is approved and Stage 18 alone is authorized. Do not execute Stage 19.

Stage 18 must read:

1. Approved `outputs/stages/00-source-audit.md` through `outputs/stages/17-capacity-cost.md`
2. Accepted ADR-000 through ADR-009 and `decisions/README.md`
3. `sources/normalized/system-design-prompt.md` section **17. Architecture decisions**
4. `stages/18-architecture-decisions.md`, `templates/stage-output.md`, and `templates/adr.md`
5. Every recorded contradiction, assumption expiry, supersession, unresolved decision, and material recommendation requiring ADR coverage

Execute Stage 18 only after explicit sponsor authorization. Do not begin Stage 19.
