# Deferred from the ARK Reference MVP

The following work is intentionally outside this single-process, single-capability demonstration. Nothing here is silently decided by the MVP implementation.

- Real tenant identity, authorization, policy enforcement, secrets, and production IAM.
- ADR-017 MVP conformance: account/organization/membership/business records, uniform versioned organization capability pattern, organization-wide admin/pattern mutation, inactive viewer/tester denial, and cross-scope/pattern-race evidence. See `docs/mvp/ADR-017-IMPACT.md`.
- ADR-018 MVP conformance: shared owner credit pool, organization policy-not-wallet records, immutable synthetic pricing, dual financial gate, atomic reservation+job acceptance, retry-safe settlement/release, full debit attribution, and concurrency/recovery evidence. See `docs/mvp/ADR-018-IMPACT.md`.
- External ingestion connectors, durable object storage, data contracts beyond the sample schema, and operational quarantine workflows.
- Distributed job dispatch, leases, heartbeats, cancellation, concurrency control, worker isolation, and production retry/dead-letter behavior.
- Production databases, event streaming, observability backends, retention policies, disaster recovery, high availability, and SLO enforcement.
- Recommendation model training, registry and serving, online features, experiment management, explainability validation, drift monitoring, and scientific approval.
- Production-grade readiness and eligibility policies; the MVP uses explicit fixture-oriented thresholds only.
- Multi-capability routing and execution for RFM, NPT, Churn, and Synapse capabilities.
- Real downstream delivery channels, callbacks, idempotent delivery retries, and consumer authentication.
- Stored-run replay controls in the UI. Event history is durable in SQLite, but the current time-boxed interface exposes only the newly executed run.
- Remaining planned scenarios beyond the two required here, including hard ineligibility, worker retry, delivery failure, and replay demonstrations.
- Deployment packaging, containers, Kubernetes, Kafka, cloud infrastructure, and production operations.

The authoritative production direction remains the completed ARK design and ADR set. Promoting any MVP shortcut requires explicit architecture review and an accepted decision record.
