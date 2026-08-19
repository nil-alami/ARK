# ADR-009 — Provisional Python, PostgreSQL, and single-Linux-server target

Status: `ACCEPTED`

Date: 2026-08-13

Decision owner: ARK design sponsor (explicit user approval)

## Context and requirements

Stage 15 defined a portable role-based deployment baseline but required a sponsor decision because the implementation target and operating capacity were unknown. The sponsor clarified that ARK will be implemented primarily in Python with PostgreSQL, initially target one Linux server, and be operated by the sponsor with AI assistance without an assumed 24/7 operations team. Containers remain optional; Kubernetes is not selected; Rust or additional data-lake infrastructure requires later evidence.

Evidence: user approval dated 2026-08-13; `outputs/stages/15-deployment-infrastructure.md`; accepted `decisions/ADR-003-architecture-style.md`.

## Decision

1. The provisional implementation language is Python.
2. PostgreSQL remains the initial authoritative relational and durable-job store under the accepted module-owned schema/writer contracts.
3. The provisional deployment target is one Linux server and one coordinated application release with separately runnable API, scheduler, worker, and one-shot maintenance/migration roles.
4. The sponsor is the accountable human operator and may use AI assistance for implementation, deployment preparation, diagnosis, documentation, and runbook execution. No staffed platform team or 24/7 response commitment is assumed.
5. Containers are optional. If used, they follow Stage 15’s immutable OCI-compatible packaging contract; otherwise supervised Linux processes preserve the same artifact, identity, configuration, secret, health, shutdown, and isolation contracts.
6. Kubernetes is not selected. It remains available only through Stage 15’s measured admission gate and proof that its added operational burden is justified and supportable.
7. A data lake remains a logical object-storage/data-lifecycle concern already defined by Stage 06. Additional data-lake infrastructure and Rust components are not selected. Rust may be introduced only for a measured performance, dependency, safety, hardware, or systems-integration need with owned interfaces and build/operational support.
8. The one-server target is not a high-availability, zero-downtime, multi-zone, disaster-recovery, RPO/RTO, capacity, security-compliance, or production-readiness claim.
9. `DEPLOYMENT_ENVIRONMENT_BLOCKED` narrows to unresolved production placement and operating details: hosting provider/site, network and ingress/egress controls, certificates/DNS, concrete identity/secrets/backup/telemetry mechanisms, resource sizing, recovery objectives, patching/maintenance, alert routing, and tested runbooks. All ADR-007 and ADR-008 blocks remain active.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| Python/PostgreSQL on one Linux server with optional containers | Lowest implementation/operations burden; matches sponsor knowledge and coordinated modular-monolith baseline | Single failure domain; sponsor availability; limited isolation/capacity; no inherent HA | Selected provisionally | Measured scale, availability, recovery, security, dependency or team evidence |
| Mandatory container platform | Reproducible role isolation | Adds a required runtime the sponsor has not selected | Optional only | Confirmed preference/environment standard |
| Kubernetes | Scheduling/rollout ecosystem | Excess operational burden without evidence or team | Rejected now | Stage 15 Kubernetes gate passes |
| Rust implementation or separate data-lake platform now | Potential performance/systems benefits | Additional language/tooling/runtime/storage burden before need | Rejected now | Measured bottleneck or required integration/safety constraint |
| Multi-server/multi-zone production topology | Availability and isolation potential | Sizing, consistency, networking, recovery, cost and operation unknown | Deferred | Approved SLO/RPO/RTO, workload and operating evidence |

## Rationale

The decision minimizes operational surface for a single human operator while preserving the accepted module, role, security, job, data, recovery, and observability contracts. Python/PostgreSQL/Linux is sufficient to begin implementation and testing without making unsupported production guarantees. Optional containers preserve portability without making Kubernetes a prerequisite.

## Consequences and trade-offs

- Implementation and early validation can target a concrete, simple environment.
- API, scheduler, and workers remain separate runtime roles even if they share one server.
- The server is a shared failure and resource domain; Stage 17 must measure capacity and cost before production sizing.
- The sponsor must have documented, testable deployment, backup/restore, patching, secret rotation, monitoring, and incident procedures before production.
- AI assistance does not replace human authorization, access accountability, incident ownership, or external availability guarantees.
- Later Rust or infrastructure additions require measurable evidence, compatible contracts, ownership, CI/CD, security, observability, and a recorded decision when material.

## Implementation constraints

- Preserve the Stage 15 coordinated immutable release and role-entrypoint contracts.
- Use Python dependency locking, reproducible builds, supported interpreter/runtime policy, supply-chain evidence, and explicit native/system dependency inventory.
- Keep PostgreSQL schemas/migrations owner-qualified; no direct cross-module writes.
- Treat object storage as a provider-neutral interface. A local filesystem may be used only for developer/test fixtures; it is not automatically the production data lake.
- Do not co-locate production secrets or unrestricted data in source, images, local developer tooling, or AI prompts.
- Server supervision, service accounts, file permissions, firewall/egress, TLS, backups, telemetry, disk/resource bounds, and restart/upgrade procedures require concrete implementation before production.
- Preserve every capability and security production-admission block.

## Validation evidence

- Sponsor statement dated 2026-08-13: “I approve Stage 15 with the provisional implementation target of Python, PostgreSQL, and one Linux server, operated by me with AI assistance and without an assumed 24/7 operations team. Containers remain optional, Kubernetes is not selected, and Rust or data-lake infrastructure requires later evidence.”
- Approved Stage 15 contains the role, release, migration, model, backup, rollback, and environment contracts.
- Stage 16 must make the baseline testable; Stage 17 must measure capacity/cost; Stage 20 must define the sponsor-operated runbooks and responsibility plan.

## Reconsideration trigger

Measured failure to meet approved performance, availability, recovery, security, compliance, isolation, delivery, or cost objectives; incompatible ML/native dependencies or accelerator needs; introduction of additional staffed operators; an authoritative hosting/platform mandate; or a justified Rust/data-lake/Kubernetes/service-extraction need.

## Supersedes / superseded by

Operationalizes accepted ADR-003 and resolves Stage 15’s sponsor decision without superseding ADR-003 through ADR-008. It narrows the deployment uncertainty but preserves `DEPLOYMENT_ENVIRONMENT_BLOCKED` for production details. Not superseded.
