### ARK **Project assumptions**

> **ARK — Consolidated architectural assumptions**
>
> I treated repeated recommendations and declared decisions as the
> current baseline. I excluded examples, vendor research, implementation
> alternatives, and unresolved questions.
>
> **Product and architecture**

1.  **ARK is a multi-tenant AI capability platform**, not merely a
    > collection of models behind APIs. Capabilities should be
    > independently consumable, versioned, observable, metered, and
    > potentially billable. Centra_Organized \_version_1.docx (page 1)

2.  **The initial architecture is a microservice-ready modular
    > monolith:** one repository, coordinated releases, and initially
    > one PostgreSQL cluster, while API, scheduler, and capability
    > workers may run as separate runtime roles.

3.  **Subservices/capabilities are independent business modules.** Each
    > owns its domain logic, configuration, contracts, persistence,
    > migrations, model lifecycle, tests, monitoring rules, and
    > runbooks. A capability must not import another capability’s
    > internals, write its tables, or depend on its database models.

4.  **Shared technical infrastructure is acceptable; shared business
    > ownership is not.** Database pools, tracing libraries,
    > object-storage adapters, and similar utilities may be shared
    > behind interfaces.

5.  **A module becomes a separate microservice only when justified** by
    > measured scaling, hardware, deployment, ownership, reliability, or
    > compliance needs—not merely for architectural style.
    > Centra_Organized \_version_1.docx (page 4)

6.  **The management/control plane and execution/data plane remain
    > distinct.** The former handles tenants, subscriptions,
    > permissions, quotas, configuration, auditing, and billing; the
    > latter performs ingestion, eligibility evaluation, ML execution,
    > and result production.

> **Integration and contracts**

7.  **ARK’s core is platform-neutral and adapterless.** Direct, Whatson,
    > POS, and future platforms translate their terminology and data
    > into ARK contracts in adapters outside the capability core.

8.  **The API gateway handles edge concerns only:** authentication,
    > routing, throttling, API versions, request-size limits, and
    > request IDs. It does not contain normalization, scientific
    > eligibility, or workflow logic. Centra_Organized \_version_1.docx
    > (page 9)

9.  **All capability requests share an operational envelope and
    > lifecycle**, including tenant/caller context, request and
    > idempotency IDs, execution mode, dataset references, callback
    > configuration, job status, standard errors, and metering. Inputs,
    > options, and outputs remain capability-specific.

10. **ARK uses small, bounded, versioned domain contracts and
    > datasets**, rather than one enormous universal customer object.
    > Contract, dataset, feature-schema, model, code, and execution
    > versions are tracked independently for reproducibility.
    > Centra_Organized \_version_1.docx (page 15)

11. **Every capability publishes a machine-readable definition**
    > describing supported operations, required and optional inputs,
    > thresholds, execution modes, outputs, dependencies, and available
    > fallbacks.

12. **Dataset readiness and capability eligibility are different
    > checks.**

    - Ingestion determines whether data is contract-valid, normalized,
      > fresh, policy-compliant, and usable.

    - ARK’s platform layer checks subscription, quota, dataset
      > availability, and active model/version.

    - Each capability owns its scientific thresholds, model readiness,
      > cold-start behavior, training permission, degradation, and
      > fallback rules.

    - ARK must explicitly return eligible, degraded, fallback, or
      > ineligible outcomes; it must not silently invent unavailable
      > data.

> **Ingestion and the ARK data lake**

13. **Subscription, data ingestion, and capability execution are
    > separate interactions.** Enabling Recommendation does not itself
    > ingest data or run Recommendation. Centra_Organized
    > \_version_1.docx (page 17)

14. **Push is the default ingestion approach.**

    - Push API for small incremental changes and micro-batches.

    - Direct object-storage upload for initial loads, backfills, and
      > large datasets.

    - Event streaming only when volume or latency genuinely requires it.

    - Standard pull, federation/query-in-place, or external connectors
      > are exceptions for platforms that cannot push or where residency
      > rules prevent copying.

    - Direct shared-database access is not a supported product
      > integration. Centra_Organized \_version_1.docx (page 20)

15. **ARK will have a data lake.** At minimum, it provides:

    - An immutable raw landing zone preserving original payloads/files.

    - Versioned canonical/curated datasets.

    - Service-owned derived data, features, results, models, and
      > artifacts.

    - Lineage, quality reports, freshness, retention, and
      > dataset-version metadata.

    - PostgreSQL stores operational metadata, registry records, jobs,
      > cursors, and state—not large historical payloads.

16. **Raw data is retained before normalization**, so failed
    > transformations are reproducible and auditable. Data reaches
    > capabilities only after authentication, registration, validation,
    > normalization, quality assessment, policy enforcement, and
    > publication of a ready immutable dataset version. Centra_Organized
    > \_version_1.docx (page 34)

17. **Ingestion is asynchronous and independently scalable.** It
    > supports idempotency, duplicate handling, incremental changes,
    > upserts, corrections, deletions/tombstones, reconciliation,
    > watermarks/cursors, backpressure, freshness, and staleness.

18. **Every dataset, artifact, storage path, and ingestion record
    > carries tenant, source, dataset, version, and ingestion-run
    > identity.** Large request inputs and results are passed by
    > reference; only small payloads may be inline.

> **Execution, orchestration, and proactive operation**

19. **ARK has one durable platform-level job manager**, not a separate
    > lifecycle implementation per capability. Capabilities own their
    > workers and computation, while the shared job layer owns state,
    > retries, scheduling, cancellation, progress, idempotency, result
    > locations, auditing, and notifications. Centra_Organized
    > \_version_1.docx (page 38)

20. **PostgreSQL is initially the job system’s durable source of
    > truth.** Capability/resource-specific worker pools prevent
    > training, backfills, or GPU workloads from blocking interactive
    > work. A broker or Temporal may be introduced later when scale or
    > workflow complexity justifies it.

21. **Synchronous execution is reserved for short, predictable
    > operations.** Training, ingestion, backfills, large inference
    > runs, scheduled work, and anything requiring retries execute as
    > durable jobs. Workers assume at-least-once delivery and make side
    > effects idempotent.

22. **The scheduler creates jobs; it does not execute capability
    > pipelines.** Cross-capability workflows create and observe child
    > jobs through the job manager rather than invoking capability
    > internals directly. Capability-internal pipelines remain private
    > to their capability. Centra_Organized \_version_1.docx (page 65)

23. **ARK supports permissioned proactive operation.** A platform may
    > issue a standing authorization for subscribed tasks, defining:

    - Permitted capability or workflow.

    - Tenant and data scope.

    - Execution interval or time window.

    - Thresholds and triggering conditions.

    - Capability-specific configuration.

    - Quotas, cooldowns, validity period, and notification destination.

24. **Proactive execution follows a governed flow:**

> ML capability detects a condition → ARK validates the standing
> permission, threshold, freshness, quota, and deduplication rules → ARK
> creates an auditable job/workflow → authorized task runs →
> event/webhook is sent to the platform
>
> ARK performs only the actions explicitly included in the grant;
> otherwise it reports the finding without acting.
>
> **Security, ownership, and operations**

25. **Tenant identity comes from the authenticated principal**, never an
    > untrusted request field. Tenant isolation applies to database
    > rows, object paths, datasets, models, jobs, events, caches,
    > quotas, audit records, and observability. PostgreSQL row-level
    > security is defense in depth. Centra_Organized \_version_1.docx
    > (page 42)

26. **The initially shared database is logically partitioned by
    > module-owned schemas.** Every table has exactly one authoritative
    > writer. Other modules use public APIs, approved read models/views,
    > or events—never cross-module writes or unrestricted SQL joins.
    > Centra_Organized \_version_1.docx (page 45)

27. **Internal events and external notifications are different
    > mechanisms.** Events coordinate work inside ARK; signed webhooks
    > or outward-facing events notify platforms. Reliable publication
    > eventually uses a transactional outbox.

28. **Audit, observability, lineage, secrets management, usage metering,
    > and cost tracking are platform-wide concerns.** Every output
    > should be traceable to its tenant, source contract, dataset,
    > feature schema, model, code version, and execution.

29. **ARK minimizes unnecessary PII.** Capabilities operate on
    > tenant-scoped opaque identifiers where possible; names, phones,
    > and presentation data remain with the consuming platform unless
    > explicitly required.

> Two document inconsistencies are now resolved by this baseline:

- Push—not pull—is the default ingestion model.

- One shared job manager owns job lifecycle; each capability owns its
  > worker and business logic, not a separate job-management system.
