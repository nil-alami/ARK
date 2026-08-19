# Stage 06 — Data architecture

Status: `APPROVED`

## Purpose and scope

Define an implementable, tenant-isolated data path from source registration through immutable raw preservation, validation, canonical publication, capability-owned derivation, prediction/result production, audit, deletion, and reproducible replay. This stage refines the approved `C05-06`, `C05-07`, `C05-13`, `C05-14`, `C05-15`, `C05-16`, and `C05-18` responsibilities without changing their ownership boundaries.

This stage defines logical contracts, states, owners, and failure behavior. It does not select a database/object-storage vendor, encryption algorithm, key topology, numeric retention/freshness/quality threshold, stream/broker product, feature-store product, capacity, or physical deployment topology. Those choices require later evidence in Stages 10, 12, 15, and 17.

The sponsor explicitly approved Stage 05 and its outputs on 2026-08-11. Per the sponsor's instruction, Stage 06 stops after its completion gate for approval before Stage 07.

## Inputs read in full

- `AGENTS.md` — all sections
- `WORKFLOW.md` — all sections
- `STATUS.md` — all sections, including recorded Stage 05 approval
- `SOURCE_MANIFEST.md` — all sections
- `stages/STAGE-CONTRACT.md` — all sections
- `stages/06-data-architecture.md` — all sections
- `templates/stage-output.md` — all sections
- `sources/normalized/system-design-prompt.md` — **5. Data architecture** exactly
- `sources/normalized/ark-assumptions.md` — all sections
- `outputs/stages/02-system-definition.md` — all sections
- `outputs/stages/03-capability-inventory.md` — all sections, including all seven capability data needs and evidence restrictions
- `outputs/stages/04-architecture-style.md` — all sections
- `outputs/stages/05-end-to-end-architecture.md` — all sections after approval was recorded
- `decisions/ADR-000-temporary-source-evidence-disposition.md` through `decisions/ADR-003-architecture-style.md` — all sections

The Stage 06-authorized `data_mlops_architect` completed a bounded independent review of required coverage, defaults/exceptions, implementability risks, and the stage-specific gate. The primary agent reconciled its findings into the four-layer validity model, writer matrix, lifecycle identity set, versioning rules, training/serving compatibility, evaluation/feedback treatment, and completion-gate evidence, and remains the sole writer.

## Source-instruction coverage

| Governing requirement | Addressed in | Status/evidence |
|---|---|---|
| Data-source integration | Integration-mode policy; source contract | Addressed |
| Push, pull, file upload, CDC, batch, streaming | Integration-mode policy | Every mode selected, deferred, or rejected with an evidence trigger |
| Canonical data contracts | Canonical contract families; contract envelope | Addressed without a universal customer object |
| Schema versioning | Version and compatibility policy | Addressed across source, canonical, feature, model, code, and execution identities |
| Technical validation | Four-layer acceptance model | Addressed as structural validation |
| Semantic validation | Four-layer acceptance model | Addressed separately from structure and capability eligibility |
| Tenant isolation | Tenant and access-isolation rules | Addressed for rows, objects, contracts, datasets, jobs, models, results, audit, and caches |
| Raw, validated, processed, feature, prediction, audit data | Zone and authoritative-writer matrix | Storage purpose and writer explicit |
| Storage ownership | Zone and authoritative-writer matrix | Addressed with one authoritative writer per state set |
| Retention and deletion | Retention, correction, and deletion model | Logical workflow defined; durations remain unresolved |
| Lineage and provenance | Lineage graph and minimum evidence | Addressed end to end |
| PII handling | PII minimization and classification | Addressed; Synapse transfer remains prohibited without evidence |
| Encryption | Encryption-control contract | Required in transit/at rest; product/algorithm/key topology deferred |
| Data-quality monitoring | Quality dimensions and ownership | Addressed without invented thresholds |
| Backfills and reprocessing | Replay/backfill protocol | Addressed with new run/version publication |
| Duplicate and late-arriving data | Incremental-change semantics | Addressed with idempotency, corrections, tombstones, watermarks, and impact manifests |
| Structural vs semantic vs sufficient | Four-layer acceptance model | Explicitly distinguished, including dataset readiness and capability eligibility |
| Example data lifecycle | Concrete lifecycle | Implementable transitions and identity/version fields included |

## Facts

1. ARK is not the source of record for customer, transaction, catalog, inventory, consent, campaign, or feedback data. Source platforms remain authoritative under active `A-01-DATA`. `outputs/stages/02-system-definition.md — System boundary`; `decisions/ADR-001-stage-01-requirements-baseline.md — Decision`.
2. Push is the approved default: API push for small increments/micro-batches and direct object upload for initial loads, backfills, and large datasets. Pull and federation are exceptions; streaming is evidence-triggered; direct shared-database integration is unsupported. `sources/normalized/ark-assumptions.md — Ingestion and the ARK data lake`.
3. Raw source evidence is preserved before normalization, and only a ready immutable dataset version reaches a capability. `sources/normalized/ark-assumptions.md — Ingestion and the ARK data lake`; `outputs/stages/02-system-definition.md — ARK-FR-003`.
4. PostgreSQL initially owns bounded operational metadata, registry records, jobs, cursors, and state; object storage owns large historical payloads, derived datasets, results, and artifacts. `sources/normalized/ark-assumptions.md — Ingestion and the ARK data lake`; `outputs/stages/05-end-to-end-architecture.md — C05-13`, `— C05-14`.
5. Every data object and execution must carry tenant, source, dataset, version, and ingestion-run identity; contract, dataset, feature-schema, model, code, and execution versions are independent. `sources/normalized/ark-assumptions.md — Integration and contracts`; `— Ingestion and the ARK data lake`.
6. Churn, RFM, NPT, and REC need transaction-derived data; REC additionally needs catalog/inventory/product metadata and optional feedback; NPT needs explicit time/horizon/calendar semantics. Exact schemas and thresholds remain unresolved. `outputs/stages/03-capability-inventory.md — CAP-CHURN`, `— CAP-RFM`, `— CAP-NPT`, `— CAP-REC`.
7. The three Synapse cards evidence request interfaces only. Their internal data access, state, persistence, provider transfer/retention, and safety behavior are unresolved and non-production-eligible under `A-03-SYNAPSE`. `decisions/ADR-000-temporary-source-evidence-disposition.md — Decision`; `decisions/ADR-002-stage-03-capability-evidence-disposition.md — Decision`.
8. Tenant authority comes from the authenticated principal, never a body `businessId`, phone, or other untrusted field. Isolation applies to every data and metadata class. `sources/normalized/ark-assumptions.md — Security, ownership, and operations`.

## Assumptions

Stage 06 introduces no new temporary assumption and does not extend an existing expiry. The following accepted assumptions constrain the design.

| ID | Assumption | Why needed | Architectural effect | Risk | Validation/expiry |
|---|---|---|---|---|---|
| `A-01-DATA` | Upstreams remain systems of record and supply stable tenant-scoped opaque IDs | No authoritative source/identity decision has superseded it | Canonical data preserves source identity; no probabilistic identity merge | Upstreams may not supply adequate identifiers/semantics | D-01 through D-05 |
| `A-01-SCALE` | Volumes, rates, latency, freshness, availability, recovery, and cost targets are unknown | Prevents speculative topology | Push/batch/object paths are the baseline; CDC/streaming/products remain triggered | Baseline may need measured evolution | S-01 through S-04 |
| `A-01-SEC` | Least privilege, tenant binding, PII minimization, auditable authority, and policy-before-action are mandatory | Legal/provider specifics are absent | Fail-closed access and data minimization; no unapproved Synapse transfer | Authoritative duties may require stronger boundaries | SEC-01 through SEC-06 |
| `A-01-OPS` | Environment, recovery, support, and numeric observability targets remain unknown | Avoids vendor/topology claims | Logical backup/recovery evidence required later; no product chosen | Production operability not yet proven | OPS-01 through OPS-05 |
| `A-04-OWNERSHIP` | Logical owner roles are sufficient for design; named people remain TBD | Required to assign authoritative writers without inventing teams | Data-platform and capability roles own contracts/state; production promotion remains blocked | Actual organization may group roles differently | Named assignments or before Stage 20/extraction/production readiness |
| `A-03-ML-MIGRATION` | Detailed prototypes are migration evidence, not target production contracts | Prevents defective prototype semantics becoming canonical | Canonical and feature contracts use intended meanings; prototype thresholds/fields are not approved | Compatibility work remains unresolved | Per capability at Stage 10/16 approval |
| `A-03-SYNAPSE` | Synapse remains interface-only and non-production-eligible | Internals and data behavior are undocumented | Only bounded caller-supplied context contracts may be modeled; hidden stores/provider transfers are not inferred | Product scope may change when evidence arrives | Relevant Stage 10/12/14/15 or enablement decision |

## Analysis and recommendations

### Data boundaries and invariants

The following invariants apply at every transition:

- `tenant_id` is derived from the authenticated principal or durable job authority and cannot be overridden by payload data.
- A source record is never silently reinterpreted: `source_contract_id`, `source_contract_version`, `source_record_id` or file identity, and source event/effective time remain traceable.
- Large bytes move through scoped immutable object references; APIs/jobs carry metadata and references, not duplicated bulk data.
- Publication is atomic at the metadata boundary: incomplete/orphaned objects are not discoverable as ready datasets or successful results.
- Published dataset, feature, prediction, and artifact versions are immutable. Corrections, late data, reprocessing, and policy changes produce a new version and lineage edge.
- Each state set has one authoritative writer. Shared infrastructure supplies storage interfaces, not shared business ownership.
- Dataset readiness is data-platform authority; capability eligibility is capability authority; entitlement/model/action authority remains separate.

### R-06-01 — Integration-mode policy

| Mode | Classification now | Contract and simplest viable implementation | Failure/operational burden | Reconsideration trigger |
|---|---|---|---|---|
| Push API | Default, required now | Authenticated, tenant-bound versioned source contract; small increments/micro-batches submitted inline and converted to a durable ingestion run | Backpressure, idempotency, bounded payload validation, and retry-safe acknowledgements | Keep default unless an authoritative source cannot push |
| File/direct object upload | Default for large/initial/backfill data | ARK issues or accepts a scoped upload registration; caller uploads, then commits an object reference plus checksum, media type, size, contract/version, and source identity | Partial/orphan cleanup, checksum verification, scoped access | Always use when request/result size exceeds the later approved inline limit |
| Batch | Required execution mode | One or more registered objects/increments processed by a durable job into an immutable candidate version | Long-running retry, checkpoint, cancellation, and resource isolation | Remains required for initial load, backfill, training preparation, and large inference |
| Pull/connector | Exception | A source-specific adapter reads from an approved endpoint using a durable cursor and writes through the same raw-registration contract | Credential rotation, rate limits, source change, polling lag, duplicate pages | Source cannot push and an accountable owner accepts connector/runbook burden |
| Federation/query in place | Exception | Read-only bounded adapter produces a versioned snapshot/reference and lineage manifest without making a shared database authoritative to ARK | Source availability can break reproducibility; residency/policy and query limits | Authoritative residency/copy restriction makes controlled federation necessary |
| CDC | Scale/integration-triggered | Source-approved change log mapped through the same source contract, sequence/cursor, raw evidence, and idempotent ingestion states | Ordering, tombstones, schema drift, retention, connector operations | Measured increment volume/freshness cannot be met by push/micro-batch and source exposes authoritative CDC |
| Streaming | Scale/latency-triggered | Versioned tenant-qualified events land raw before validation and are compacted into immutable dataset versions; no capability reads unvalidated stream state as ready data | Broker, ordering, replay, watermark, poison, schema-registry, and on-call burden | Approved latency/volume target cannot be met by micro-batch after simpler tuning |
| Direct shared database | Unjustified/prohibited | No supported product integration | Bypasses ownership, tenant, lineage, schema, and replay controls | Only a superseding ADR could change this constraint |

**Requirement/where:** `ARK-FR-002/003/007`, `ARK-NFR-004`, `ARK-CON-004/006`; ingestion and reprocessing in Stages 06/08/15. **Why now:** every source must enter one lifecycle regardless of transport. **Alternative rejected:** a connector/streaming platform as the universal ingestion plane; no source inventory or measured target justifies it. **Trade-off:** source adapters may require individual mapping work, but the core lifecycle remains small and auditable.

### Source-registration and canonical contract envelope

Every accepted source integration registers a bounded contract; ARK does not define one universal customer document.

| Field | Rule/purpose |
|---|---|
| `tenant_id` | Principal-derived immutable scope; never caller-selected authority |
| `source_id` | Registered source-system identity within tenant |
| `source_contract_id`, `source_contract_version` | Exact accepted wire/file/event schema and semantic declaration |
| `ingestion_run_id`, `attempt_id` | Durable processing and retry identity |
| `idempotency_key` | Tenant + source + operation scoped logical-submission identity |
| `source_batch_id` / `source_record_id` / `source_event_id` | Source-stable identity where supplied; absence is explicit |
| `source_sequence` / `cursor` | Optional ordered incremental position; source semantics registered |
| `event_time`, `effective_time`, `observed_at`, `received_at` | Distinct time meanings; required/optional per domain contract |
| `object_ref`, `content_length`, `media_type`, `checksum` | Required for files/large data; reference is tenant-scoped and opaque |
| `classification`, `purpose`, `consent_policy_ref` | Data handling and allowed-use evidence; exact values require policy authority |
| `schema_ref` | Machine-readable structural schema and compatibility declaration |
| `correlation_id`, `actor_ref` | Cross-system trace and privacy-safe submitter identity |

Canonical records add `canonical_contract_id/version`, stable tenant-scoped opaque domain identifiers, `source_record_ref`, normalization/code version, validity/effective intervals where applicable, and correction/tombstone status. Units, currency, time zone, identifier namespace, nullability, enumerations, and authoritative field sources are contract semantics, never inferred from column names.

### R-06-02 — Bounded canonical contract families

Stage 06 establishes contract families, not their unresolved business field lists:

| Canonical family | Minimum semantic concerns | Consumers evidenced now | Authoritative contract writer |
|---|---|---|---|
| Customer/reference identity | Tenant-scoped opaque customer ID, source namespace, lifecycle/effective state; no probabilistic merge | Churn, RFM, NPT, REC; Synapse only if later authorized | Data-platform canonical owner with upstream source authority |
| Transaction/purchase | Transaction and line IDs, customer/product references, event/effective time, amount, currency/unit, correction/refund/deletion semantics | Churn, RFM, NPT, REC | Data-platform canonical owner |
| Catalog/product | Opaque product ID, attributes with source/version, lifecycle state | REC | Data-platform canonical owner; upstream catalog remains source of record |
| Inventory/availability | Product/location scope, quantity or availability semantics, effective/as-of time | REC | Data-platform canonical owner; upstream inventory remains source of record |
| Interaction/feedback | Subject/item/action, event time, channel/context, idempotency/source authority, consent/purpose | REC learning/evaluation if approved | Data-platform canonical owner for source-aligned facts; REC owns derived learning state |
| Calendar/reference | Calendar/event/occasion ID, locale/time-zone scope, effective interval/version | NPT; message generation only if later authorized | Data-platform reference-data owner |
| Consent/policy reference | Subject/scope/purpose/channel, authority, version/effective interval/revocation | Eligibility and outward-action governance | Control/policy owner, exposed as a bounded read contract |
| Campaign/offer context | Campaign/offer identity, authorized facts, scope, effective interval, policy reference | Synapse interfaces only after evidence/authorization | Upstream/control authority; not Synapse |

Capability-owned feature schemas remain separate: churn feature set; RFM recency/frequency/monetary semantics; NPT labels/horizons/censoring/calendar binding; REC candidate/ranking/feedback features. Their owners consume canonical references and publish immutable feature versions without expanding the shared canonical kernel.

**Requirement/where:** `ARK-NFR-002/003`, `ARK-CON-002/003`, capability needs from Stage 03; ingestion, training, inference, and lineage. **Why now:** consumers need stable data meaning without importing prototype schemas. **Simplest implementation:** machine-readable schemas and semantic metadata stored with relational catalog records and immutable objects. **Alternative rejected:** a universal customer/profile contract; it centralizes ownership and creates sparse, unstable coupling. **Trade-off:** more explicit mappings and version joins; clearer ownership and independent evolution. **Reconsideration:** add or split a contract family only when a release-scoped capability/source proves a bounded need.

### Version and compatibility policy

| Version identity | Owner | Change rule |
|---|---|---|
| Source contract version | Source adapter/data platform | Exact parser and declared semantics; incompatible change registers a new version |
| Canonical contract version | Canonical contract owner | Published immutable; additive or incompatible classification is explicit; no silent reinterpretation |
| Dataset version | Dataset catalog | Immutable snapshot/delta-set identity bound to source/canonical versions, run, quality, policy, and code |
| Feature-schema version | Capability | Immutable names/types/units/null/transform semantics |
| Label/horizon/mapping/ranking version | Capability | Independent from feature/model version; must be explicit when applicable |
| Model/artifact bundle version | Capability + registry | Exact immutable artifact set and evaluation/promotion evidence |
| Configuration/policy version | Owning control or capability module | Effective interval and authority recorded; execution binds the exact version |
| Code/transformation version | Build/data/capability owner | Reproducible identifier for normalization/derivation/execution |
| Execution/result version | Job/capability owner | Exact job/attempt plus all referenced versions; result is immutable or superseded, never overwritten |

Readers declare supported contract-version ranges. A producer may publish a new version only after structural schema checks, mapping/semantic tests, compatibility classification, and consumer impact are recorded. Incompatible versions coexist during an explicit migration window; the length is unresolved. “Latest” is not a reproducible selector: admission resolves exact versions before work begins.

### Four-layer acceptance model

| Layer | Authority | Question | Representative checks | Outcome |
|---|---|---|---|---|
| 1. Structural validity | Ingestion validator | Can the bytes/record be safely parsed as the declared source contract? | Media type, checksum, decompression/parser success, schema/version known, required fields, types, bounds, enum/cardinality, object integrity | `STRUCTURALLY_VALID` or quarantined with reason report |
| 2. Semantic validity | Domain normalizer/validator | Do values mean a coherent, source-authoritative domain fact? | Tenant/source identity, referential integrity, units/currency/time-zone, event/effective ordering, duplicates/corrections, catalog/inventory consistency, consent/purpose, business invariants | `SEMANTICALLY_VALID` or quarantined/rejected with reason |
| 3. Dataset readiness | Dataset catalog/data-platform owner | Is an immutable version safe and usable under its declared general purpose? | Required partitions/contracts present, lineage complete, quality/freshness/policy evidence evaluated, no unresolved publication error, object integrity | `READY`, `NOT_READY`, `STALE`, or `REVOKED`, with reasons |
| 4. Capability eligibility/sufficiency | Individual capability | Is this ready version scientifically sufficient for this exact operation and active bundle? | Required feature coverage/history/population/variance, label/horizon compatibility, catalog availability, model/config applicability, cold-start/fallback rules | `ELIGIBLE`, `DEGRADED`, `FALLBACK`, or `INELIGIBLE`, with reasons |

Structurally valid data can still be semantically invalid (for example, a valid timestamp string after a transaction's correction time, or a valid product ID unknown to the tenant catalog). Semantically valid data can still produce a not-ready dataset (for example, a required partition is absent or freshness policy failed). A ready transaction dataset can still be insufficient for NPT if its approved history/horizon requirements are not met, while it may remain sufficient for RFM. No generic `valid=true` flag can replace these four decisions.

### Zone and authoritative-writer matrix

| Zone/state class | Purpose and mutability | Physical placement rule | Authoritative writer | Allowed readers / publication rule |
|---|---|---|---|---|
| Upload staging | Incomplete multipart/object transfer; not evidence yet | Object storage, non-public namespace | Upload/ingestion adapter | Ingestion only; expires/cleans by later policy; never ready |
| Raw landing | Exact accepted bytes/payload plus receipt metadata; immutable | Object storage; metadata in ingestion schema | Ingestion module (`C05-06`) | Restricted data-platform/replay access; no capability reads |
| Quarantine/validation report | Rejected/untrusted record/object and machine-readable reasons | Object storage for large evidence; metadata in PostgreSQL | Ingestion/validator | Data steward/operator only; never ready |
| Validated source-aligned | Structurally and semantically accepted, still source-shaped; immutable version | Object storage | Data-platform normalizer | Canonical builders; not a universal capability input |
| Canonical/processed | Bounded normalized domain datasets; immutable published versions | Object storage; catalog metadata in PostgreSQL | Canonical data-platform owner | Authorized capabilities through dataset references after readiness |
| Feature/derived | Capability-specific transformations/features/labels; immutable versions | Capability namespace in object storage; bounded metadata/state in owned schema | Owning capability (`C05-15`) | That capability and approved evaluation/training paths; no cross-write |
| Prediction/result | Bounded result rows or immutable large result object | Inline only when bounded/small; otherwise capability result namespace + reference | Owning capability | Result API/authorized adapters; publication only after authoritative commit |
| Model/artifact/evaluation | Immutable model bundles, scalers, mappings, prompts only if evidenced, evaluation reports | Capability object namespace; registry metadata in PostgreSQL | Capability owns bytes/evidence; registry owns common metadata/status (`C05-16`) | Exact activated reference only; no mutable “latest” lookup |
| Dataset/catalog/readiness metadata | Contract/version/object/quality/freshness/policy/lineage and publication state | Data-platform PostgreSQL schema | Dataset catalog (`C05-07`) | Authorized modules via public query contract |
| Operational ingestion/job/cursor state | Runs, attempts, cursors, watermarks, leases, idempotency | Module-owned PostgreSQL schemas | Ingestion/job owner | Narrow public interfaces; not historical payload store |
| Audit/lineage/usage evidence | Append/supersede evidence of authority and transitions | PostgreSQL for bounded records; large evidence by object reference | Audit/lineage owner (`C05-18`); source owner supplies facts | Restricted authorized trace/LAB export; not diagnostic logs |
| Deletion/correction/tombstone manifests | Scope, authority, reason, affected versions/objects/results, completion evidence | Governance/data PostgreSQL plus object manifests | Data governance workflow; each storage owner executes its scope | Readers must honor revoked/superseded state |

Authority and persistence remain distinct when a common registry is used. A capability owner makes and signs the scientific promotion/rollback decision; the common model registry is the sole writer of common registry metadata and applies that authorized command. Likewise, the data-platform publisher decides that its validated candidate is ready for publication, while the dataset catalog is the sole writer of catalog publication state. Audit records evidence an owner's decision but do not become the underlying business authority.

### Tenant and access-isolation rules

1. PostgreSQL: every tenant-owned row includes `tenant_id`; module-owned schemas, least-privilege roles, one writer, and row-level security as defense in depth. Cross-module reads use public APIs or explicitly approved read models, not unrestricted joins.
2. Object storage: path/key structure includes an opaque tenant partition plus owner namespace, data class, dataset/artifact/result identity, version, and run. Authorization derives path scope from the principal/job, never from caller path text. Raw objects are never public URLs.
3. Catalog/registry: uniqueness and lookup keys start with tenant and owner scope. A reference resolving under another tenant returns not-found/denied without metadata leakage.
4. Jobs/caches/telemetry: tenant and exact version are part of idempotency/cache keys and trace context. A cache is never authority and cannot contain unbounded raw PII.
5. Worker access: a claimed job grants only the referenced tenant/source/dataset/capability namespaces and expires with job authority; workers cannot enumerate other tenants.
6. Cross-tenant aggregate or model training is prohibited unless a future explicit product, privacy, and ownership decision defines it. No such requirement exists now.

### Retention, correction, and deletion model

- Numeric retention periods are unresolved and must not be invented. A production data class cannot be onboarded until an accountable owner records its purpose, classification, retention, deletion SLA, backup/copy coverage, legal-hold behavior, residency, and downstream derived-data treatment.
- “Immutable” means published content is not edited in place; it does not mean undeletable. Correction creates a superseding source fact and new dataset version. Deletion creates an authoritative tombstone/revocation workflow and may physically purge objects according to policy.
- A deletion request is tenant- and subject/source-scoped, authenticated, idempotent, audited, and expanded through lineage to raw, validated, canonical, feature, prediction/result, artifact/evaluation (when affected), cache, export, and backup/copy obligations.
- Each authoritative storage owner records `PENDING`, `IN_PROGRESS`, `COMPLETED`, `FAILED`, or `EXEMPT/HELD` with reason and evidence. The governance workflow aggregates status but does not directly mutate another owner's store.
- Catalog and result readers must honor revoked/deleted/superseded versions immediately according to policy, even when deferred physical purge remains in progress.
- Legal hold, statutory retention, consent withdrawal, subject erasure applicability, and model-unlearning requirements are unresolved and belong to Stage 12 policy authority. Stage 06 supplies the traceable mechanism, not a legal conclusion.

### Lineage and provenance graph

Every published result must resolve backward and forward across:

`source registration/contract → source object/event/checksum → ingestion run/attempt → validation report → validated source version → canonical contract/dataset version → feature/label version → model/artifact bundle + evaluation + activation → configuration/policy/code version → job/execution/attempt → prediction/result → projection/notification/audit`

Minimum lineage edges contain tenant, producer/owner, input reference/version, output reference/version, transformation/code version, run/attempt, event/processing time, decision/outcome, and correlation. An edge is appended or superseded, not silently overwritten. A missing mandatory edge prevents readiness, activation, or authoritative result success as appropriate.

### PII minimization and classification

- Prefer tenant-scoped opaque customer/product/campaign identifiers. Names, phone numbers, addresses, message presentation fields, and raw free text remain upstream unless an approved capability contract proves necessity.
- Source contracts classify sensitive fields and allowed purpose before ingestion. Raw/quarantine access is stricter than canonical access; normalizers drop, tokenize, or separate presentation fields when not needed.
- Logs, metrics, traces, idempotency keys, object keys, and error text must not expose raw PII or secrets. Audit uses privacy-safe actor/subject references and controlled evidence links.
- Capability features/results contain only fields required by their declared purpose. External projectors resolve presentation data outside capability cores.
- Synapse request fields currently include business/customer IDs, history, address, phone, payloads, references, and opaque metadata. These interface facts do not authorize ARK storage or external-provider transfer. Until Stage 12 receives authoritative implementation, provider, retention, consent, and safety evidence, Synapse remains non-production-eligible and no hidden data access is designed.

### Encryption-control contract

Data is encrypted in transit across trust boundaries and at rest in PostgreSQL, object storage, backups, and exported evidence. Application and operator access uses workload/principal identity, least privilege, auditable key/secret references, rotation/version support, and fail-closed behavior. Keys/secrets never enter datasets, logs, contracts, or object paths. Exact algorithms, providers, key hierarchy, tenant-specific keys, regional placement, rotation interval, and backup-key design remain Stage 12/15 decisions because environment and compliance evidence are absent.

### Data-quality monitoring and ownership

| Dimension | Examples | Owner/action |
|---|---|---|
| Contract conformance | Parse/schema/type/bound/cardinality errors, unknown versions | Source adapter + data platform; quarantine/reject |
| Completeness | Required fields/partitions/source coverage, null rates | Canonical data owner; affects readiness by declared policy |
| Uniqueness/duplicate | Duplicate event/record/batch IDs, collision rate | Ingestion owner; dedupe/reconcile |
| Validity/consistency | Units, currency, time order, range, referential/catalog/inventory rules | Canonical domain owner; semantic failure or quality signal |
| Freshness/latency | Source event lag, last complete partition, watermark delay | Data platform; ready/stale outcome under policy |
| Volume/change | Record/byte deltas, missing partitions, unexpected source distribution | Source/data owner; investigate, no invented fixed threshold |
| Distribution/drift | Canonical/feature distribution shift, category emergence | Data owner for canonical; capability owner for feature/scientific impact |
| Lineage/integrity | Missing edge, checksum/reference failure, orphan object | Catalog/lineage owner; block publication or result |
| Capability sufficiency | History/population/variance/coverage/model applicability/fallback rate | Individual capability; eligibility outcome, not dataset rewrite |

Every metric is tenant-, source-, contract-, dataset-, version-, and run-scoped. Numeric thresholds and alert routes require named owners and measured baselines; absent thresholds remain visible, not defaulted. Failed quality policy does not delete raw evidence and cannot silently publish a ready version.

### Training, evaluation, serving, and feedback consistency

- Training, evaluation, and inference must resolve compatible canonical-contract, dataset, feature-schema/transformation, label/horizon/mapping, configuration, and code versions. Inference additionally binds the exact activated model/artifact bundle and execution version. No path selects an ambiguous “latest” version.
- A training dataset and an evaluation dataset are immutable dataset references with purpose/split policy, observation/as-of boundary, label-availability boundary, and complete lineage. Evaluation reports are immutable capability-owned evidence linked to the exact dataset, feature, model bundle, code, configuration, and execution versions.
- The registry records compatibility and activation metadata but cannot invent scientific approval. Inference never fits preprocessing, trains, promotes, or activates an artifact.
- Feedback/outcome data is admitted through a bounded source contract, not a universal event stream. It carries tenant/entity/result linkage, source authority, event time, observation/ingestion time, idempotency identity, consent/purpose, and applicable schema/policy versions.
- Delayed labels and feedback are late-arriving facts: they create new evaluation/training dataset versions and may trigger an explicitly authorized evaluation or retraining job. They do not rewrite the dataset or model evidence used by an earlier result.
- REC currently evidences capability-owned learning feedback. Other predictive outcome/label contracts are added only when a release-scoped capability defines their authority and semantics. Feedback alone does not justify a broker or streaming platform.

### Incremental changes, duplicates, corrections, and late data

1. Submission dedupe uses tenant + source + contract + operation + idempotency key. Content checksum detects identical file/object retries; source event/record ID and sequence provide record-level identity where authoritative.
2. An exact duplicate maps to the existing logical ingestion/result and records a duplicate observation; it does not create a second logical side effect.
3. An update/correction retains the prior source fact and adds a superseding fact with authority/effective time. Domain-specific merge/upsert rules live in the bounded canonical contract, not generic “last write wins.”
4. A deletion is represented by an authoritative tombstone even when physical purge follows later. Tombstones participate in canonical publication and lineage.
5. Cursors/watermarks are source-contract state. Cursor advancement is committed only with durable receipt/raw registration; failed processing can replay raw evidence without rereading the source.
6. Late data is evaluated against event/effective time and the last published version. It creates a new candidate dataset version and an impact manifest identifying affected partitions, feature versions, models/evaluations, and results. No published version is mutated.
7. Recomputing features/predictions after late/corrected data is an explicit authorized job. Prior results remain reproducible and may be marked superseded/revoked; external redelivery is a separate policy decision.
8. Conflicting events, missing source identities, cursor gaps, or sequence regressions become reconciliation exceptions. They are never silently accepted as newest truth.

### Backfill and reprocessing protocol

1. Authorized operator/workflow submits a durable backfill/reprocess request with tenant, source/dataset scope, immutable input references, target contract/transformation versions, reason, and idempotency key.
2. The job reuses registered raw evidence when policy permits; rereading a source creates a new source receipt/run and does not rewrite the old one.
3. Transformations write a new validated/canonical candidate namespace and quality/lineage evidence. They cannot overwrite a published dataset.
4. Catalog publication uses an atomic compare-and-publish command, binds all exact versions, and yields a new immutable dataset version or explicit rejection.
5. Capability feature/result recomputation is separately scheduled against the new dataset version. It binds exact feature/model/config/code versions and publishes a new result identity.
6. Impact, supersession, deletion, and external-notification consequences are explicit and audited. Replay is at-least-once safe; cancellation before publication leaves unreferenced candidates for controlled cleanup.

### Concrete data lifecycle — transaction file to recommendation result

| Step/state | Identity and version fields present | Authoritative writer/storage | Transition and failure behavior |
|---:|---|---|---|
| 1. Register upload | `tenant_id`, `source_id`, `source_contract_id/version`, `ingestion_run_id`, `idempotency_key`, expected media/size/checksum, `correlation_id` | Ingestion schema in PostgreSQL | Auth/entitlement/contract failure creates no upload authority |
| 2. Upload/commit raw | Above + `object_ref`, actual checksum/length, `received_at`, `source_batch_id` | Ingestion writer; raw object namespace | Partial/mismatched object remains staging/quarantine; no dataset candidate |
| 3. Structural validation | Above + validator/code version, validation report ID | Ingestion/validator; report metadata + large evidence ref | Unknown schema, parse/type/bound failure → quarantined; raw retained |
| 4. Semantic normalization | `canonical_contract_id/version`, opaque customer/product/transaction IDs, event/effective times, currency/unit, source-record refs, normalization version | Canonical data writer; validated/canonical candidate object | Referential/unit/time/correction ambiguity → semantic failure; no ready version |
| 5. Quality/readiness publication | `dataset_id/version`, candidate object refs/checksums, run, quality/freshness/policy versions, lineage graph | Dataset catalog in PostgreSQL; canonical object storage | Atomic publication yields exact `READY` version; otherwise `NOT_READY/STALE/REVOKED` with reasons |
| 6. REC capability admission | Tenant/job, dataset refs/versions for transactions + catalog/inventory + optional feedback, active feature/ranking/model/config versions | REC public port reads catalog/control/registry | Data ready but inadequate cold-start/availability/model applicability → `DEGRADED/FALLBACK/INELIGIBLE`, not fabricated success |
| 7. Feature/candidate generation | `feature_schema_version`, transformation/code version, input dataset versions, execution/attempt | REC writer; capability feature namespace | Retry writes same logical version or an unpublishable attempt; no cross-capability write |
| 8. Rank/filter and commit result | `result_id/version`, as-of/context, ranking/config/model versions, availability snapshot, job/execution/attempt, lineage | REC result writer; small bounded rows or large immutable object by reference | Empty/unavailable items produce truthful no-result/fallback; terminal success only after authoritative commit |
| 9. Retrieve/audit | Tenant-bound result reference, job/correlation, actor, usage and full lineage | Result API reads REC state; audit/lineage appends evidence | Cross-tenant/expired/revoked access denied; large result uses scoped reference, never copied into job/API metadata |
| 10. Late correction | New source receipt/run and dataset version; impact/supersession manifest | Ingestion/catalog, then explicit REC recompute job | Prior version/result remains reproducible and is marked superseded/revoked only by policy; no in-place mutation |

The same source-to-ready lifecycle serves Churn, RFM, and NPT, but each capability independently declares its feature, history, label/horizon, model, and fallback sufficiency. Synapse is excluded from this production lifecycle until its data access/provider evidence is authoritative.

### Anti-overengineering classification

| Component/product | Disposition | Reason |
|---|---|---|
| PostgreSQL catalog/operational metadata + object-storage interface | Required now | Approved baseline and minimum implementable ownership split |
| Machine-readable schema/contract tooling | Required now | Needed for structural validation/version compatibility; may be code/repository metadata, not a separate product |
| Dedicated data catalog/lakehouse platform | Unjustified now | Relational catalog + immutable object namespaces satisfy current requirements |
| Streaming platform/broker | Scale-triggered | No approved latency/volume evidence |
| CDC platform | Integration/scale-triggered | No authoritative CDC sources or measured need supplied |
| Generic connector/ETL suite | Optional/exception | Add only for evidenced source that cannot use default contracts |
| Standalone feature store | Unjustified now | No proven online/offline consistency, cross-capability reuse, or latency need; capability-owned schemas/namespaces suffice |
| Vector store, agent memory, MCP, or A2A data plane | Unjustified now | No evidenced retrieval, autonomy, memory, or inter-agent data contract; Synapse interface names prove none |
| Data warehouse/query engine | Optional/scale-triggered | No analytics workload or performance target supplied |
| Universal customer/profile model | Rejected | Violates bounded contracts, source authority, and module ownership |
| Probabilistic identity graph | Rejected under active assumption | `A-01-DATA` requires stable opaque upstream identities; no merge mandate |

## Decisions

- Stage 06 applies accepted ADR-003 and the authoritative ingestion/data-lake baseline; it does not introduce a separate deployable service or new ADR.
- The data-platform module is authoritative for source registration, raw/validated/canonical publication, dataset readiness, and catalog/lineage metadata. Each capability is authoritative for its derived features, scientific eligibility, artifacts/evaluations, and predictions/results.
- Push/micro-batch and referenced object upload/batch are the default paths. Pull/federation are exceptions; CDC/streaming require evidence; direct shared-database integration remains prohibited.
- Immutable publication, four distinct validation/readiness/eligibility layers, exact independent version identities, and by-reference large payload/result handling are mandatory logical contracts.
- Numeric policy values and physical products remain unresolved; this output is not a production data-governance approval.

These are Stage 06 design recommendations pending the sponsor's requested approval. No accepted ADR is superseded.

## Contradictions and dangerous assumptions

| ID | Tension/hazard | Treatment | Consequence |
|---|---|---|---|
| `C-06-01` | Prototype fields/thresholds appear concrete but are not approved target semantics | Canonical/feature contracts use intended bounded meanings; exact fields remain release-scoped and versioned under `A-03-ML-MIGRATION` | No prototype schema is silently standardized |
| `C-06-02` | Shared PostgreSQL/object infrastructure can look like shared ownership | Module schemas/namespaces, public interfaces, and one authoritative writer remain mandatory | Infrastructure sharing cannot authorize cross-writes/joins |
| `C-06-03` | Immutable evidence appears to conflict with deletion duties | Immutability prohibits in-place change; tombstone/revocation plus policy-driven physical purge remains possible | Retention/deletion policy can be applied without destroying lineage silently |
| `C-06-04` | “Valid” is often used for structure, semantics, readiness, and ML sufficiency | Four independent authorities/states are mandatory | No capability runs on a generic validity flag |
| `C-06-05` | Event streaming may appear required for incremental data | Push micro-batch is the authoritative default; streaming requires measured latency/volume evidence | No broker/stream processor is selected |
| `C-06-06` | Synapse request schemas contain PII/context fields | Interface presence is not data-access, retention, or provider-transfer authority | Synapse remains non-production-eligible and hidden internals unresolved |
| `C-06-07` | Late/corrected data may tempt in-place dataset/result updates | New dataset/result versions plus impact/supersession manifests | Prior results remain reproducible |
| `C-06-08` | Retention/encryption wording could imply concrete compliance controls | Logical control contract is defined; durations, algorithms, keys, region, and legal duties remain unresolved | Stage 12/15 must supply authoritative policy/environment decisions |

## Open questions

| ID | Question | Blocking? | Options | Recommended temporary treatment | Effect |
|---|---:|---|---|---|---|
| `Q-06-01` | Which source systems and bounded contract families are in the first release? | Before implementation/roadmap | One vertical slice; per-capability subset; all | Keep families logical; implement only release-scoped source/capability contracts | No unsupported connector/schema work |
| `Q-06-02` | What are authoritative transaction, catalog, inventory, identity, feedback, calendar, consent, campaign, and offer semantics? | Before each contract is accepted | Source-owned definitions; governed mapping | Require source owner + canonical owner approval; do not infer | Exact field schemas remain unresolved |
| `Q-06-03` | What quality/freshness/readiness and capability-sufficiency thresholds apply? | Before production admission | Per source/dataset/capability approved policies | Record explicit no-threshold state and fail/not-admit where a threshold is mandatory | No numeric target invented |
| `Q-06-04` | What retention, erasure, legal hold, residency, consent, and backup-copy duties apply per data class? | Before production data onboarding | Jurisdiction/tenant policy register | Require accountable policy before onboarding; mechanism remains as defined | Production governance remains blocked |
| `Q-06-05` | Which correction/upsert/tombstone/sequence semantics does each source guarantee? | Before incremental ingestion | Source-specific event semantics | Contract must declare them; ambiguous changes quarantine/reconcile | Generic last-write-wins prohibited |
| `Q-06-06` | Does any source require pull, federation, CDC, or streaming? | Before those components | Default push; source exception; measured scale path | Keep conditional classifications | Avoids speculative integration products |
| `Q-06-07` | What encryption/key topology and secret facility does the environment require? | Stage 12/15 and production | Platform-managed; tenant-specific; regional | Logical encryption/least-privilege contract only | No vendor/algorithm invented |
| `Q-06-08` | May corrected data trigger automatic feature/result recomputation and redelivery? | Before operational policy | Manual/authorized job; scoped automatic workflow | Explicit authorized job; no automatic external redelivery | Prevents surprising side effects |
| `Q-06-09` | Can authoritative Synapse implementation/provider/data-access/retention evidence be supplied? | Relevant Stage 10/12/14/15 or enablement | Supply evidence; scope out; remain unavailable | Continue `A-03-SYNAPSE` | No Synapse production data path |
| `Q-06-10` | Who are the named data-contract, data-quality, privacy/governance, storage, and per-capability owners? | Before production and Stage 20 expiry | Assign roster | Continue accepted `A-04-OWNERSHIP` constraints | Logical design valid; operations/promotion blocked |

## Requirements-traceability updates

| Requirement | Stage 06 design response | Verification direction |
|---|---|---|
| `ARK-FR-002` | Default push/micro-batch and object-reference bulk; pull/federation exceptions; CDC/stream triggered; direct DB rejected | Contract tests for every admitted mode and exception gate |
| `ARK-FR-003` | Raw-first lifecycle, structural/semantic validation, immutable canonical publication, catalog readiness | Failed transform retains raw and publishes no ready version |
| `ARK-FR-006` | Four-layer acceptance model and separate authorities | Scenario matrix proves readiness cannot replace capability eligibility |
| `ARK-FR-007` | Durable ingestion/backfill/reprocess and explicit job/run/attempt identities | Restart, replay, cancel-before-publish, idempotency tests |
| `ARK-FR-009` | Capability-owned immutable features/artifacts and exact activation references | Inference cannot train/activate; lineage bundle test |
| `ARK-FR-010` | Consent/policy references and Synapse advisory/data restrictions | Missing/stale/ambiguous policy produces no action |
| `ARK-FR-012` | Queryable end-to-end data/result lineage and quality evidence | LAB trace reconstruction and fault scenarios |
| `ARK-NFR-001` | Tenant keys/paths/roles/RLS and worker/reference scoping | Cross-tenant negative suite for every zone and registry |
| `ARK-NFR-002` | Independent contract/dataset/feature/model/config/code/execution versions | Reproduce result from exact immutable references |
| `ARK-NFR-003` | Bounded canonical families and explicit compatibility declarations | Consumer compatibility and no-universal-model checks |
| `ARK-NFR-004` | At-least-once-safe dedupe, correction, late-data, replay and publication | Duplicate/cursor-gap/late-arrival/fault injection tests |
| `ARK-NFR-005` | Opaque IDs, classification/minimization, restricted raw/quarantine, no hidden Synapse transfer | PII inventory, logs/object-path scans, provider-transfer denial |
| `ARK-NFR-006` | Lineage/audit/quality/version evidence at each transition | Trace completeness and missing-edge failure tests |
| `ARK-NFR-007` | No invented volumes/thresholds/products; conditional scale paths | Target register required before CDC/stream/warehouse/product commitments |
| `ARK-CON-002` | Data-platform/capability schema and namespace ownership; one writer | Dependency, migration, DB role, object-prefix tests |
| `ARK-CON-004` | Large data/results/artifacts in object storage by reference; bounded metadata in PostgreSQL | Size-class/reference integrity/orphan tests |
| `ARK-CON-005` | PostgreSQL job/run/cursor truth; streaming/broker not baseline | Recovery tests and evidence gate before replacement |
| `ARK-CON-006` | Upstream source authority and opaque identities retained | Reject unregistered source/body tenant/probabilistic merge |
| `SC-02-02/04/06/07/09/12` | Lifecycle, independent validity/eligibility, isolation, lineage, ownership, and unresolved policy targets | Acceptance suites named above |

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Every governing data-architecture bullet addressed | PASS | Source-instruction coverage maps all bullets |
| All ingestion modes dispositioned | PASS | Integration-mode policy includes push, file, batch, pull, federation, CDC, streaming, and direct DB |
| Structural, semantic, readiness, and capability sufficiency are distinct | PASS | Four-layer acceptance model with separate authorities/outcomes |
| Canonical contracts are bounded/versioned | PASS | Contract envelope, seven families, independent version policy; universal object rejected |
| Storage purpose and authoritative writer explicit | PASS | Zone and authoritative-writer matrix |
| Lifecycle implementable | PASS | Ten-step transaction-to-REC lifecycle plus retry/failure/late-correction behavior |
| Large payloads/results passed by reference where required | PASS | Upload contract, zone matrix, lifecycle steps 2/8/9, `ARK-CON-004` trace |
| Tenant, PII, encryption, retention, deletion, lineage, quality controls addressed | PASS WITH POLICY INPUTS OPEN | Logical mechanisms explicit; unsupported numeric/legal/environment values remain unresolved |
| Backfill, reprocessing, duplicates, corrections, tombstones, cursors, and late data addressed | PASS | Dedicated protocols and impact/supersession rules |
| Anti-overengineering applied | PASS | No speculative catalog/lakehouse/CDC/stream/feature-store/warehouse product |
| Independent authorized specialist review | PASS | `data_mlops_architect` independently confirmed the evidence-backed defaults, four-layer model, writer matrix, identity/version set, and by-reference gate; training/serving, evaluation/feedback, writer-authority, and unresolved-policy findings were incorporated |
| Stage 07 not executed | PASS | No Stage 07 artifact created or decision made |
| Sponsor-requested approval | **PASS** | Sponsor explicitly approved Stage 06 and its outputs on 2026-08-11 |

**Gate result: PASSED AND APPROVED.** The independent review is reconciled and the lifecycle is implementable, every storage purpose has an authoritative writer, and bulk inputs/large datasets/features/results/artifacts/evidence use tenant-scoped references while PostgreSQL retains bounded operational metadata. The sponsor explicitly approved Stage 06 and its outputs on 2026-08-11, authorizing Stage 07 to begin.

## Downstream consequences

- Stage 07 must express the source-registration, upload-commit, dataset-reference, result-reference, version, error, idempotency, pagination, and tenant-context fields without changing data authority.
- Stage 08 must implement durable ingestion/backfill/reprocess jobs, cursor ownership, cancellation before publication, retries, and result/reference lifecycle.
- Stage 09 must keep internal data-change coordination separate from external notification and introduce reliable publication only when a named path requires it.
- Stage 10 must bind feature/label/model/config/evaluation versions, exact capability sufficiency, and prototype remediation to the Stage 06 lineage graph.
- Stage 12 must resolve authoritative classification, consent, retention/deletion, legal hold, erasure/model-unlearning, provider transfer, encryption/key, and audit-access policies.
- Stage 13 must define storage/catalog availability, backup/recovery, orphan cleanup, partial publication, and reconciliation runbooks.
- Stage 14 must set measurable quality/drift/lineage monitoring and LAB evidence without conflating telemetry with audit truth.
- Stage 15 must select actual PostgreSQL/object/encryption/backup placement only from deployment/residency evidence.
- Stage 17 must measure whether CDC, streaming, warehouse/query, catalog, feature-store, or storage extraction triggers are met.
- Stage 20 cannot authorize production data onboarding until named owners and the unresolved policy register are supplied.

## Exact next-stage inputs

Approved inputs for Stage 07:

1. Approved `outputs/stages/02-system-definition.md`
2. Approved `outputs/stages/03-capability-inventory.md`
3. Approved `outputs/stages/04-architecture-style.md`
4. Approved `outputs/stages/05-end-to-end-architecture.md`
5. Approved `outputs/stages/06-data-architecture.md`
6. Accepted `decisions/ADR-000-temporary-source-evidence-disposition.md` through `decisions/ADR-003-architecture-style.md`
7. `sources/normalized/ark-assumptions.md`
8. All seven service cards under their ADR-000/ADR-002 evidence restrictions
9. `stages/07-api-integration.md`, `templates/stage-output.md`, and exact governing prompt section **6. API and integration design**

Stage 06 approval is recorded; Stage 07 may consume this artifact.
