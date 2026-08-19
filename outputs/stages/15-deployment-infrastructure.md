# Stage 15 — Deployment and infrastructure

**Status:** APPROVED  
**Completed:** 2026-08-13  
**Stage owner:** Primary architecture agent  
**Authorized specialist:** `platform_architect` (read-only operational-fit review)

## Purpose and scope

Recommend the simplest adequate, evidence-bounded deployment model for the approved ARK modular monolith; map logical ownership to runnable roles; and define portable contracts for environments, configuration, containers, delivery, migrations, models, infrastructure as code, secrets, scaling, backups, rollback, releases, and developer/test operation.

The sponsor approved Python, PostgreSQL, and one Linux server as the provisional implementation target. Cloud/provider/site, region, network, managed-service choices, identity/secrets products, CI/CD/IaC/observability tools, capacity, availability, RPO/RTO, and production-fitness evidence remain unknown. Containers are optional, Kubernetes is not selected, and no vendor or purchase is approved.

## Inputs read in full

- `WORKFLOW.md`
- `STATUS.md`
- `SOURCE_MANIFEST.md`
- `stages/STAGE-CONTRACT.md`
- `stages/15-deployment-infrastructure.md`
- `templates/stage-output.md`
- `templates/adr.md`
- `sources/normalized/system-design-prompt.md` — **14. Deployment and infrastructure**
- Approved `outputs/stages/04-architecture-style.md` through `outputs/stages/14-observability-evaluation.md`
- Accepted `decisions/ADR-003-architecture-style.md` through `decisions/ADR-008-zero-trust-tenant-and-governance-boundary.md`
- `outputs/stages/01-discovery-and-questions.md` — `S-01` through `S-04`, `OPS-01` through `OPS-05`, `TEAM-01` through `TEAM-04`

## Specialist reconciliation

The Stage 15-authorized `platform_architect` performed a bounded read-only operational-fit review covering portable placement, runtime roles, Kubernetes comparison, environments, containers, CI/CD, migrations, model deployment, IaC, secrets, scaling, backup/restore, rollback, release, developer/test operation, network/trust boundaries, team fit, and the workflow approval gate. It confirmed conditional `PASS` with hosting blocking concrete production topology. Its final artifact review found only two stale mechanical references left during removal of the redundant ADR-009 proposal; the live artifact now contains neither reference, and the reviewer stated no further review was needed after correction. No critical or high defect remains. The primary agent reconciled the findings and remains the sole authoritative writer.

## Source-instruction coverage

| Governing requirement | Addressed in | Status/evidence |
|---|---|---|
| Simplest adequate deployment model | Conditional baseline and option comparison | Covered; production target remains blocked |
| Environments | Environment model | Covered |
| Configuration | Configuration and release identity | Covered |
| Containers | Packaging contract | Covered; supervised-process compatibility retained |
| CI/CD | Coordinated delivery pipeline | Covered product-neutrally |
| Database migrations | Migration protocol | Covered |
| Model deployment | Model/artifact deployment protocol | Covered; profiles remain blocked |
| Infrastructure as code | IaC contract | Covered product-neutrally |
| Secrets | Workload/secrets placement | Covered; concrete provider remains blocked |
| Scaling | Scaling ladder and triggers | Covered without sizing |
| Backups | Backup/restore deployment contract | Covered without RPO/RTO |
| Rollback | Layer-specific rollback matrix | Covered |
| Release strategies | Coordinated release baseline and conditional strategies | Covered |
| Development/testing environments | Developer and validation environments | Covered |
| Kubernetes comparison | Alternatives matrix | Covered; not selected |
| Runtime-role mapping without service-per-module | Deployable role matrix | Covered |

## Confirmed facts

1. ARK’s accepted style is one repository, coordinated releases, boundary-enforced modules, one initially shared PostgreSQL cluster with module-owned schemas/writers, and optional separately runnable API, scheduler, ingestion, and worker roles. Accepted ADR-003.
2. PostgreSQL is authoritative for jobs, attempts, schedules, control/catalog/registry metadata, audit/usage records, and conditional outbox/delivery state. Object storage holds large immutable raw, datasets, features, results, artifacts, and evidence by reference. Approved Stages 05–10.
3. Long/retryable work requires durable job/attempt/lease/fence semantics independent of HTTP/process lifetime. Scheduler and workers may run separately without becoming microservices. Accepted ADR-005.
4. Each independently runnable role requires a distinct workload identity, least privilege, exact execution context, encrypted authenticated transport when crossing a process/network boundary, and no embedded/shared credential. Approved Stage 12; accepted ADR-008.
5. Recovery requires ordered restore and cross-store reconciliation, a new recovery epoch, stale worker isolation, and no blind replay. RPO/RTO/topology/failure domains remain unknown. Approved Stage 13.
6. Structured telemetry is product-neutral and diagnostic; audit/lineage/usage/evaluation remain authoritative records. Approved Stage 14.
7. Four capability profiles are `MIGRATION_BLOCKED`, three Synapse profiles are `EVIDENCE_BLOCKED`, and all eight ADR-008 security-admission blocks remain active. Deployment cannot clear them. Accepted ADR-007/008.
8. No current evidence justifies a broker, workflow engine, service mesh, feature store, vector store, agent runtime, service-per-capability topology, or Kubernetes. Approved Stages 04, 08, 11, 13, and 14.
9. Hosting target, cloud/on-premises constraints, regions, network boundaries, existing container platform, managed-service rules, team roster/skills/on-call, traffic, SLOs, capacity, recovery targets, compliance, budget, and deadline are absent. Approved Stage 01 and `STATUS.md`.

## Assumptions and explicit blocks

| ID | Classification | Statement | Architectural effect | Expiry/evidence |
|---|---|---|---|---|
| `A-01-SCALE` | Temporary assumption retained | Scale/capacity/SLO/cost values remain unknown | Scaling ladder and measurements only; no sizing | Stage 17 evidence |
| `A-04-OWNERSHIP` | Accepted temporary assumption retained | Logical owners exist; named delivery/on-call owners do not | Architecture can define roles; production/extraction blocked | Stage 20/production/extraction |
| `DEPLOYMENT_ENVIRONMENT_BLOCKED` | Accepted Stage 15 deployment disposition | Linux is selected provisionally, but provider/site, network, TLS/DNS, identity/secrets, backup/telemetry mechanisms, sizing, recovery targets, patching and tested runbooks are absent | No production-fitness or hosting approval; portable role model plus one-server test baseline only | Authoritative environment/operations evidence and sponsor decision |

Stage 01 `A-01-OPS` expired at Stage 15. It is not silently extended: its unresolved production-environment portion is replaced by accepted `DEPLOYMENT_ENVIRONMENT_BLOCKED`. Concrete workload identity, secrets/keys, supply chain, privileged release, governance, audit, cache, provider, and delivery remain governed by the existing accepted ADR-008 blocks rather than a redundant new Stage 15 security block.

### Approved sponsor disposition

On 2026-08-13 the sponsor approved Stage 15 with this provisional target: Python, PostgreSQL, one Linux server, sponsor-operated with AI assistance and no assumed 24/7 operations team; containers optional; Kubernetes unselected; Rust or additional data-lake infrastructure evidence-triggered. Accepted `decisions/ADR-009-provisional-python-postgresql-linux-target.md` records the material implementation and operating decision.

This approval resolves the Stage 15 workflow decision and selects a concrete implementation baseline. It does not claim production fitness. `DEPLOYMENT_ENVIRONMENT_BLOCKED` now applies to the unresolved provider/site, networking, ingress/egress, DNS/TLS, identity/secrets/backup/telemetry mechanisms, sizing, recovery targets, patching/maintenance, and tested runbooks. ADR-007/008 blocks remain unchanged.

## Conditional starting deployment

### R-15-01 — Coordinated Python role-based deployment from one release

**Requirement/where:** source Section 14; `ARK-CON-001/002/005`; all runtime paths. **Why now:** API, scheduler, durable workers, and maintenance have different process lifecycles, but no module qualifies for service extraction. **Simplest viable implementation:** one immutable Python release with role entrypoints; deploy `api`, `scheduler`, `worker`, and one-shot `maintenance/migration` roles on one Linux server under a process supervisor or optional simple container runtime. **Alternative:** service per module/capability. **Why rejected:** distributed deployment/ownership/compatibility burden without evidence. **Trade-off:** coordinated releases and one server form a shared failure/resource domain; role restart/resource policies can differ. **Reconsideration:** ADR-003 extraction gate, measured server limit, approved availability/recovery need, or recurrent incompatible runtime/hardware need.

The approved provisional starting profile is:

```text
approved ingress
    -> API role(s) [same ARK release]

Scheduler role [same release, PostgreSQL occurrence/lease truth]
Worker role(s) [same release, typed handler pools and fences]
Maintenance/migration role [one-shot, privileged and audited]

All roles -> environment-provided PostgreSQL contract
          -> environment-provided object-storage contract
          -> identity/secrets/config/audit/telemetry contracts
```

API, scheduler, and workers initially share one Linux server/failure domain but run as distinct supervised processes or optional containers. This is a packaging/implementation baseline, not a production availability claim. PostgreSQL is the approved initial durable store. Object storage remains a provider-neutral interface and may be local only for developer/test; a production data-lake mechanism requires later evidence and policy. Production placement details remain blocked.

## Deployable runtime-role matrix

| Role | Contains/logical responsibilities | Lifecycle/scaling | Required identity/access | Initial disposition |
|---|---|---|---|---|
| `api` | Edge/API facade, auth context adapter, control/query ports, sync-eligible capability calls, job/result APIs, health | Long-lived; stateless where possible; horizontal only after measurements | Public ingress; narrow owner ports; DB schemas through owner commands; no broad object access | Required runnable role |
| `scheduler` | Schedule/occurrence evaluation and typed job submission only | Long-lived; duplicate instances safe through PostgreSQL identity/lease; one effective owner | Schedule/job commands, policy/readiness checks, mandatory audit | Required logical role; may co-host |
| `worker-general` | Job claim/heartbeat/fenced public handlers for bounded general work | Long-lived; scale by declared pool/concurrency policy | Job/attempt context; exact handler and tenant-scoped storage | Required starting worker role |
| `worker-data` | Ingestion, validation, normalization, publication, backfill handlers | Split from general only for dependency/resource/isolation evidence | Raw/candidate/catalog namespaces and data-owner commands | Conditional separate role; handlers required |
| `worker-ml` | Training/evaluation/reproduction/batch inference handlers | Split for incompatible libraries, resource/accelerator need, or contention | Exact dataset/artifact/assignment scopes; no promotion authority | Conditional; profiles production-blocked |
| `publisher-delivery` | Conditional outbox/event handlers and external delivery | Activate only for named admitted subscriber/webhook; scale by delivery backlog | Named schema/consumer/destination/secret scopes | Not deployed initially |
| `workflow-coordinator` | Conditional deterministic parent/child workflow graph | Activate only for named workflow | Workflow/job public commands only | Not deployed initially |
| `maintenance-migration` | Schema/data migrations, reconciliation, restore, cleanup, privileged admin operations | One-shot/explicit schedule; never general worker; strong audit/approval | Exact environment/target/version; least privilege; time-bounded | Required operational entrypoint; production blocked pending roles/security |
| `developer-tools` | Local schema setup, fixtures, contract tools | Developer-only | No production credentials/data/network | Required locally; excluded from production artifact/runtime |

Logical routing pools inside Stage 08 are not automatically processes, containers, services, or queues. Combine them until measured contention, incompatible dependencies, hardware, or security policy requires role separation.

## Deployment alternatives and Kubernetes comparison

| Model | Operational fit | Benefits | Risks/burden | Disposition and trigger |
|---|---|---|---|---|
| Supervised processes on one VM/host | Fits one small team/environment without container support | Fewest layers; simple debugging | Packaging drift, weaker isolation, single failure domain, manual patch/release | Compatibility option; production only after explicit environment/team acceptance |
| Small container runtime on VM(s) or managed container execution | Best conditional fit | Reproducible artifacts, role health/restart/resource isolation, portable | Still requires platform/network/secrets/storage/backup expertise | Recommended conditional baseline; exact runtime/host count TBD |
| Kubernetes | No current fit evidence | Rich scheduling, rollout, policy, autoscaling, placement | Cluster/network/security/upgrades/controllers/storage/observability/on-call cost | Reject now; reconsider only after simpler runtime misses approved role scale, hardware, availability, policy, or fleet needs |
| Service-per-capability Kubernetes/microservices | Contradicts starting evidence | Independent deploy/scale | Multiplies services, APIs, state, pipelines, on-call; profiles not stable | Reject; only per-module ADR-003 extraction |
| Whole-platform serverless/functions | Poor fit for durable jobs/ML | Managed burst scaling | Runtime duration, leases, large dependencies, artifact/state/network limits | Reject as baseline; bounded stateless adapter may qualify later |
| Bespoke on-prem/bare metal | Unknown | Meets potential mandated control/hardware | Highest operational/capacity/patch/backup burden | Only on authoritative OPS-01 constraint |

### Kubernetes measurable admission gate

Kubernetes may be proposed only when the confirmed environment permits it, a staffed owner/runbook exists, and one or more measured needs persist after simple runtime/VM/container remedies:

- role/replica fleet size or release frequency makes supervisor/host management unsafe;
- approved availability/rollout objectives require automated rescheduling or progressive rollout unavailable otherwise;
- multiple worker hardware/resource/placement classes require scheduling;
- workload bursts exceed manual/static scaling and have measured safe autoscaling signals;
- network/policy/compliance controls mandate cluster-level enforcement;
- an existing organizational platform materially lowers rather than adds operational burden.

Even then, Kubernetes does not justify service-per-module, a mesh, a broker, or operator proliferation.

## Environment model

| Environment/lane | Purpose | Data/identity | Deployment characteristics | Promotion authority |
|---|---|---|---|---|
| Developer local | Fast module/contract/migration work | Synthetic/minimized fixtures; developer identity; no production secrets/data | Same role entrypoints; local process or container composition; ephemeral dependencies acceptable | None |
| Shared integration/validation | Cross-module API/job/data/security/recovery tests and consumer/LAB evidence | Synthetic or governed de-identified versioned fixtures; isolated tenant IDs/credentials | Coordinated candidate release; production-like interfaces; disposable/rebuildable | Test evidence only; LAB authority unresolved |
| Production | Approved tenant work only | Governed production identities/data/secrets/keys | **Not enabled** until all deployment/capability/security/ownership/target gates pass | Named release/security/scientific/operations authorities required |
| Optional staging/performance/security/recovery lanes | Only when release risk, scale measurement, security validation, consumer certification, or restore exercises require isolation | Governed representative/synthetic data by policy | Created from same IaC/config modules; not permanently required by architecture | Evidence-producing, not automatic promotion |

The simplest model has three conceptual tiers: local, shared validation, and production. Separate always-on development/test/staging/performance clusters are not assumed. Environment isolation applies to identity, credentials, database/object namespaces, keys, config, telemetry, audit, and IaC state.

## Configuration and release identity

- Build once; promote the same immutable application artifact digest across environments. Never rebuild source for production with hidden code changes.
- Configuration is external, typed, schema-versioned, environment-scoped, tenant-qualified where applicable, and validated before role readiness. Defaults cannot broaden security, tenant scope, model selection, retention, delivery, or fallback.
- Every role exposes release ID, source revision, build/provenance reference, configuration schema/version, supported handler/contract versions, and environment identity in safe health/telemetry evidence.
- Secrets are references, never configuration values, image layers, repository files, command arguments, logs, or telemetry.
- Application release, database migration set, object/data contract, model/artifact assignment, policy/config version, and IaC revision are independent identities. A release manifest records the intended compatible set.
- Feature flags/config switches may only select pre-approved behavior; they cannot clear production blocks, grant authority, promote models, or bypass migration/security gates.

## Container and artifact packaging contract

When containers are permitted:

- Use OCI-compatible immutable images built from pinned dependencies and a minimal runtime, with non-root user, explicit entrypoint/role, read-only root filesystem where practical, bounded writable scratch, no embedded credentials/data/models, and declared health/shutdown behavior.
- One base/application image may serve API/scheduler/general worker roles. A distinct ML/data worker image is justified only by incompatible libraries, accelerator/runtime needs, vulnerability/size isolation, or measured build/start burden; it still belongs to the coordinated release.
- Images and dependencies require source provenance, SBOM, vulnerability/license policy, digest/signature/attestation, restricted registry access, and promotion by digest. `SUPPLY_CHAIN_BLOCKED` remains until concrete controls and tests pass.
- Graceful shutdown stops admission/claims, relinquishes or lets leases expire safely, reaches cancellation/checkpoint boundaries, and cannot extend authority beyond the current fence/deadline.
- Resource requests/limits, filesystem/network policy, and replica counts remain environment/capacity inputs.

If containers are prohibited, supervised processes must preserve the same immutable artifact/version, non-privileged identities, config/secrets separation, role entrypoints, health, shutdown, and filesystem/network isolation contracts. “No container” is not permission for mutable servers or shared credentials.

## Coordinated CI/CD and release pipeline

| Phase | Required evidence/action | Failure behavior |
|---|---|---|
| Source admission | Reviewed change; dependency/module-boundary/CODEOWNERS-equivalent checks; issue/decision refs | No build candidate |
| Build | Reproducible artifact/image; pinned dependencies; SBOM/provenance/digest; no secrets/data | Candidate quarantined on mismatch/failure |
| Static/unit/contract | Formatting/static analysis, module dependency, public contract, migration, tenant/security tests | No promotion |
| Integration/validation | API/job/data/model-fixture, cross-role, recovery, telemetry, consumer/LAB suites in isolated environment | No promotion; evidence immutable |
| Security/supply chain | Vulnerability/license/secret/provenance/config/IaC policy and signing checks | `SUPPLY_CHAIN_BLOCKED`/security blocks remain |
| Release assembly | Immutable manifest binds app artifacts, migrations, supported handlers/contracts, config schema, IaC revision, and approved model assignments separately | Incomplete/incompatible release rejected |
| Deployment plan | Target diff, migration impact/locks, backups/restore checkpoint, capacity, rollout/rollback/runbook, approvals | Privileged deployment blocked |
| Apply | IaC/config, migration one-shot, roles in dependency order, readiness checks, bounded smoke/contract verification | Pause/rollback layer safely; no blind continuation |
| Observe/close | Verify owner truth, audit/lineage/usage, SLI signals, versions, queues/fences, security and reconciliation | Hold release; do not infer success from green process alone |

The pipeline is logical and product-neutral. Production branch rules, approval roles, release cadence/windows, artifact retention, and pipeline platform require OPS-02/TEAM evidence. CI workers never receive broad persistent production credentials; production apply uses a separately authorized workload/approval boundary.

## Database and data migrations

1. Each module owns its schema and ordered migration history; one release manifest orders only real cross-module prerequisites without granting cross-writes.
2. Default to expand → deploy compatible readers/writers → bounded backfill/reconcile → verify → contract after rollback/compatibility window. Old and new role versions may overlap only when the contract explicitly supports it.
3. A one-shot migration identity acquires an environment/release lock, records plan/dry-run, expected schema version, lock/time/data impact, backup/restore checkpoint, actor/approval/audit, and terminal evidence.
4. Migrations are idempotent or detect already-applied state. Long data backfills use Stage 08 jobs/checkpoints/fencing rather than holding a schema transaction.
5. Destructive/drop/rename/type changes require verified consumer compatibility, retention/deletion policy, backup implications, and explicit approval. Rollback normally uses a forward fix; database downgrade is not assumed safe.
6. Cross-store changes create immutable candidates first and publish through owner metadata; no migration claims atomic PostgreSQL/object-store commit.
7. Production migration remains blocked until target database capabilities, maintenance windows, backup/restore evidence, data policies, and named owner are confirmed.

## Model and capability deployment

- Application deployment registers supported handlers/runtime compatibility; it does not train, promote, assign, or activate a model.
- Model artifacts and evaluation reports remain immutable registry/object references. Promotion and deployment assignment are separate privileged audited operations with scientific, release, security, and operations evidence.
- Workers load only the exact environment/tenant/capability/operation assignment and digest after compatibility/revocation/purpose checks. ADR-008 cache identity applies; `MODEL_CACHE_BLOCKED` remains.
- Retain compatible worker artifact versions for admitted jobs or explicitly migrate/fail them. A code rollback cannot silently execute an old/new incompatible bundle.
- Model rollback creates a new assignment to a prior approved compatible bundle; past predictions are never rewritten.
- Shadow/canary model deployment is conditional on approved evaluation, tenant/purpose scope, comparison method, resource/cost limit, and no-action output. No current profile is production eligible.

## Infrastructure as code

IaC is required as a logical delivery discipline once an environment is selected. It must declare environment-scoped network/trust boundaries, runtime roles, workload identities/permissions, database/object/registry endpoints, secrets references, telemetry/audit integrations, backup policies, DNS/certificates where applicable, and protected outputs.

- Reusable modules separate common contracts from environment-specific values; environments have distinct state, credentials, approval, and drift detection.
- Plans are reviewed and policy/security checked; applies are serialized/authorized and auditable; state and sensitive outputs are encrypted/restricted/backed up.
- Manual emergency change requires the same privileged audit and later reconciliation; it does not become the desired state silently.
- No IaC tool, state backend, cloud module, region, or account/subscription layout is selected until OPS-01 and security evidence exist.

## Network, trust, and secrets placement

The portable logical zones are:

| Zone/boundary | Permitted flows | Prohibited assumptions |
|---|---|---|
| Ingress/consumer | Approved consumer/adapter → API over authenticated encrypted protocol | Direct database/object/worker access; body tenant authority |
| Application roles | API/scheduler/workers/maintenance → typed owner interfaces and least-privilege infrastructure endpoints | Flat mutual trust, shared credential, private module network API by default |
| Data/control | Role-specific PostgreSQL schemas/commands, object namespaces, registry/audit/usage | Public exposure, unrestricted joins/prefixes, direct capability cross-write |
| Administrative/build | CI/release/admin through separate stronger-auth, approval and audit boundary | Developer laptop or CI build credential as persistent production admin |
| Egress/provider/delivery | Deny by default; exact destination/provider/secret/purpose only after admission | Arbitrary outbound internet, caller URL, blocked Synapse/webhook |

Each role gets a distinct workload identity and only its required DB schemas/commands, object prefixes, secret refs, egress destinations, handlers, and telemetry permissions. Concrete identity, certificate, network policy, key/secrets provider, rotation, break-glass, and administrative access are `EXTERNAL_TRUST_BLOCKED`, `CRYPTO_SECRETS_BLOCKED`, and `PRIVILEGED_ACTION_BLOCKED` until admitted.

## Scaling ladder

Apply the lowest-cost measured remedy first:

1. Profile code/queries/serialization and remove waste; validate indexes and object transfer patterns.
2. Bound payloads, batch, checkpoint, enforce backpressure/concurrency/fairness, and separate sync from durable work.
3. Vertically size the simple host/role and database within approved limits.
4. Adjust worker concurrency and split general/data/ML/delivery roles only for measured contention/dependencies/hardware/security.
5. Add API/worker replicas under a simple container/VM runtime; scheduler duplicates remain logically safe through occurrence identity/leases.
6. Apply PostgreSQL connection/query/index/table lifecycle remedies and object-store multipart/parallelism only from measurements.
7. Reconsider Kubernetes for fleet/placement/rollout/policy needs, a broker for proven dispatch/fan-out limits, or module extraction through ADR-003 only after simpler remedies fail approved targets.

Autoscaling requires an approved safe signal (queue age/backlog/deadline/resource/latency), minimum/maximum bounds, cooldown, tenant fairness, database/provider/storage capacity, scale-to-zero compatibility, cost guard, and test evidence. None is numerically configured here.

## Backup, restore, and disaster-recovery deployment contract

| Asset | Backup/restore requirement | Verification |
|---|---|---|
| PostgreSQL owner schemas | Encrypted, access-controlled backups and transaction recovery capability appropriate to later RPO/RTO; schema/version manifest | Automated integrity plus periodic isolated restore and Stage 13 reconciliation |
| Object namespaces | Version/integrity inventory and backup/replication only per data class/residency/deletion policy | Digest/reference/orphan/missing-object verification |
| Registry/models/evaluations | Immutable artifact/report digests and metadata/assignment history | Reconstruct exact bundle/assignment; revoked artifacts remain revoked |
| Config/IaC/release manifests | Versioned repositories/state/backups with protected sensitive values | Rebuild environment plan and compare drift |
| Secrets/keys/identity | Provider-specific protected recovery/rotation under separation of duties | Recovery exercise without exposing values or restoring revoked authority |
| Audit/usage/lineage | Integrity-preserving retained evidence per policy | Completeness/tamper/access and effect reconciliation |

Stage 13 restore order, recovery epoch, stale worker isolation, cross-store mismatch classification, deletion/legal-hold behavior, external-effect reconciliation, cache invalidation, and bounded resume are mandatory. The deployment must prevent restored schedulers, workers, publishers, and webhooks from acting until reconciliation releases them.

Backup frequency, retention, RPO/RTO, replication, region/site, automatic failover, and disaster-recovery environment are not selected. Production remains `DEPLOYMENT_ENVIRONMENT_BLOCKED` until these are approved and exercised.

## Layer-specific rollback

| Layer | Rollback action | Preconditions/limits |
|---|---|---|
| Application role | Redeploy previous immutable artifact digest | Database/config/handler contracts remain compatible; in-flight jobs retain admitted handler or explicit migration/failure |
| Configuration/policy | New audited version restoring approved previous values | Current authority/security checks; no history overwrite |
| Database schema/data | Prefer forward fix; restore only under incident recovery; corrections create new versions | No blind down migration; reconcile cross-store/effects/deletion |
| Model/artifact | New deployment assignment to prior approved compatible bundle | Scientific/release/security/operations checks; no `latest`; past predictions unchanged |
| IaC | Reviewed corrective plan or prior desired revision | Provider state and destructive effects reconciled; no assumed reversal |
| Secret/key | Rotate/revoke/reissue through provider policy | Dependent roles restart/reload safely; audit mandatory |
| Delivery/external effect | Stop future attempts, reconcile ambiguity, compensate only by typed authorized operation | Cannot claim an external effect was undone |

## Release strategies

- **Default:** coordinated release with explicit dependency order and compatible schema/handler window. On a single simple host this may be stop/replace with an acknowledged outage; on a multi-instance/container runtime it may be rolling. The environment/SLO determines which—Stage 15 does not promise zero downtime.
- **Progressive canary:** justified only when traffic routing, tenant isolation, comparable telemetry, rollback safety, and approved blast-radius policy exist. It is not a default requirement.
- **Blue/green:** justified only when near-zero-downtime/fast-revert objectives and duplicate environment cost/state/migration constraints are approved.
- **Feature flags:** only for pre-approved reversible behavior; never for schema incompatibility, security bypass, production admission, or model promotion.
- **Model shadow/canary:** separate from application rollout and blocked until the specific capability profile passes evaluation/admission.

Every strategy has release ID, artifact/config/migration/handler/model compatibility manifest, health/SLI checks, observation window, abort/rollback rules, authority, audit, and post-deployment verification. Numeric percentages/windows are not invented.

## Developer and test environments

- The repository provides the same role commands, configuration schemas, migrations, and public contracts used elsewhere. Local execution may use process supervision or a container composition, but neither becomes a production topology decision.
- Developer dependencies are ephemeral/test instances implementing PostgreSQL/object/identity/secrets/provider interfaces. Fakes are allowed only for narrow unit tests; integration/contract tests use behavior-compatible real interfaces where semantics matter.
- Use synthetic or governed de-identified fixtures with stable tenant/source/dataset/model identities. Production snapshots, secrets, phone numbers, histories, prompts, or customer debug CSVs are prohibited.
- Migrations test from supported prior versions, clean bootstrap, retry/interruption, mixed-version application compatibility, and rollback/forward-fix behavior.
- Validation environments exercise API/jobs/data/model fixtures, workload identity/tenant isolation, failure/recovery, backup restore, telemetry/audit separation, and release manifests.
- LAB remains an external evidence consumer with unresolved promotion authority; connecting LAB does not grant production access or release veto automatically.
- Developer access never supplies broad production data/control/DB/object credentials. Break-glass and production debugging require the Stage 12 privileged contract.

## Anti-overengineering assessment

| Component/pattern | Disposition | Reason |
|---|---|---|
| One coordinated release with role entrypoints | Required now | Matches ADR-003 and actual lifecycle isolation |
| OCI-compatible containers | Recommended conditionally | Reproducibility/isolation with low platform burden; environment must permit them |
| Supervised-process compatibility | Required portability | Unknown target may prohibit containers; preserves same contracts |
| Separate API/scheduler/worker hosts | Optional/measurement-triggered | Roles differ, but host count/availability evidence is absent |
| Managed PostgreSQL/object/secrets/container services | Environment option only | May reduce burden, but managed-service/vendor restrictions are unknown |
| Kubernetes/service mesh/operators | Rejected now | No fleet/scale/availability/team evidence |
| Service per capability/database per service | Rejected | No extraction gate passed; profiles are not production ready |
| Broker/workflow engine | Rejected now | PostgreSQL jobs/outbox and deterministic coordination suffice |
| Permanent full environment fleet | Rejected now | Local/shared validation/production conceptual tiers suffice; extra lanes are evidence-triggered |
| Automatic multi-region active-active | Rejected | Failure domains, consistency, RPO/RTO, compliance, and budget unknown |

## Recommendations

### R-15-02 — Build once and promote immutable compatible manifests

**Requirement/where:** containers, CI/CD, config, migrations, models, rollback. **Why now:** rebuilding or selecting `latest` breaks provenance and recovery. **Simplest implementation:** immutable app artifact plus release manifest; external config/secrets; exact migration and assignment refs. **Alternative:** environment-specific builds and mutable servers. **Why rejected:** drift and untraceable behavior. **Trade-off:** compatibility and artifact retention discipline. **Reconsideration:** never weaken identity; tooling may change with environment.

### R-15-03 — Use environment contracts and explicit blocks instead of inventing hosting

**Requirement/where:** workflow Stage 15 approval gate; remaining OPS evidence. **Why now:** provider, network, recovery, and security constraints can reverse a production topology choice. **Simplest implementation:** the approved Python/PostgreSQL/one-Linux-server target with vendor-neutral interfaces plus `DEPLOYMENT_ENVIRONMENT_BLOCKED`, while preserving accepted ADR-008 blocks. **Alternative:** assume a typical cloud/Kubernetes stack. **Why rejected:** unsupported spend/operations/security. **Trade-off:** production fitness awaits environment and runbook evidence. **Reconsideration:** authoritative OPS-01/02/04 evidence or measured need.

### R-15-04 — Roll back each authority layer explicitly

**Requirement/where:** releases, DB/data, models, config, IaC, secrets, external effects. **Why now:** “rollback release” is not an atomic reversal across these truths. **Simplest implementation:** layer-specific versioned commands and Stage 13 reconciliation. **Alternative:** deploy previous application and declare recovery. **Why rejected:** can corrupt schemas, assignments, jobs, effects, or restored authority. **Trade-off:** more manifests/runbooks/tests. **Reconsideration:** none without preserving explicit layer ownership.

## Decisions

- Accept `decisions/ADR-009-provisional-python-postgresql-linux-target.md`, recording the sponsor-approved provisional language, database, server, operating-capacity, container, Kubernetes, Rust, and data-lake dispositions. It operationalizes ADR-003 and does not supersede ADR-003 through ADR-008.
- Use supervised Linux processes or optional containers with behavior-compatible entry points; neither packaging form is preferred or required by the approval. This does not select a vendor, region, availability tier, or production topology beyond the provisional single-server target.
- Keep Kubernetes, service-per-capability deployment, mesh, broker, workflow product, and multi-region active-active unselected until their measurable gates pass.
- Replace the expired Stage 01 deployment deferral with `DEPLOYMENT_ENVIRONMENT_BLOCKED`; do not extend `A-01-OPS` silently or duplicate accepted ADR-008 blocks.
- Preserve every ADR-007/008 block and `A-04-OWNERSHIP`. No capability or production environment becomes active.
- Stage 15 approval authorizes Stage 16 only; Stage 17 remains unstarted until separate sponsor approval.

## Contradictions and dangerous assumptions

| ID | Finding | Resolution | Consequence |
|---|---|---|---|
| `C-15-01` | The source asks for a deployment recommendation while the target environment is unknown | Select portable packaging/roles and compare placements; block concrete production topology | Workflow approval gate is required |
| `C-15-02` | “Microservice-ready” and separate roles can be misread as service-per-module | Roles share source/release/contracts and are not extracted modules | No distributed architecture drift |
| `C-15-03` | Containers can be mistaken for Kubernetes | OCI packaging works with simple runtime/VM/managed execution; Kubernetes has a separate gate | Lower operational burden |
| `C-15-04` | Single-host simplicity can be mistaken for production fitness/HA | Treat it as a failure-domain-explicit starting placement only | No availability/failover claim |
| `C-15-05` | App rollback can be mistaken for DB/data/model/effect rollback | Use the layer-specific matrix and recovery reconciliation | No unsafe down migration or hidden model/effect change |
| `C-15-06` | Managed services can reduce toil but may violate unknown restrictions/budget | Keep managed/self-hosted forms as options until OPS/TEAM/budget evidence | No purchase/vendor commitment |
| `C-15-07` | Local containers/test data can drift into a production blueprint | Same contracts/entrypoints, but environment identity/data/secrets/access remain isolated | Developer convenience cannot weaken controls |
| `C-15-08` | Deployment might be treated as clearing capability/security blocks | Release manifests surface block state; they cannot override it | No production enablement |

## Open questions and recorded human decision

| ID | Question | Blocking? | Options | Recommended temporary disposition | Effect |
|---|---:|---|---|---|---|
| `Q-15-01` | What target cloud/on-prem/hybrid environment, regions, networks, existing container platform, and managed-service restrictions apply? | Yes for production topology | VM/process; simple container runtime; managed container platform; Kubernetes; mandated on-prem | Approve portable conditional baseline only | `DEPLOYMENT_ENVIRONMENT_BLOCKED` remains |
| `Q-15-02` | What named specialist/security/release authorities, if any, will supplement the sponsor? | Yes where separation is required for production | Sponsor only during development; later people/services; managed operations | Sponsor operates with AI assistance and no assumed 24/7 team; logical roles remain | `A-04-OWNERSHIP` remains |
| `Q-15-03` | What availability, RPO/RTO, failure-domain, maintenance, backup retention, and restore obligations apply? | Yes for production | Best effort; single-site; multi-zone; multi-region | No HA/DR topology claim | Stage 13 logical recovery only |
| `Q-15-04` | What CI/CD platform, release approvals/windows/cadence, artifact retention, and change governance exist? | Before production delivery | Existing platform/process; build new; managed | Product-neutral pipeline contract | Implementation/tooling unresolved |
| `Q-15-05` | Which optional container runtime or managed database/object/secrets/registry/telemetry services, if any, will be used? | Before selecting those products | None; selected products; later decision | Containers optional; retain process compatibility | No product selection yet |
| `Q-15-06` | What data residency/key/network/egress/compliance constraints affect placement? | Yes for production | Supply policy; tenant-specific; mandated boundary | Deny production/egress until admitted | ADR-008 blocks remain |
| `Q-15-07` | Which capabilities/use cases and consumers form the first release? | Before actual role/image sizing and release | One vertical slice; subset; all | Do not deploy blocked profiles | Capacity/rollout remains conditional |

### Recorded approval decision

The sponsor approved the following bounded decision on 2026-08-13, as recorded by ADR-009:

> Adopt Python, PostgreSQL, and one Linux server as the provisional role-based coordinated implementation target; operation is by the sponsor with AI assistance and no assumed 24/7 team; containers are optional; Kubernetes is not selected; Rust or data-lake infrastructure requires later evidence; and `DEPLOYMENT_ENVIRONMENT_BLOCKED` plus all accepted ADR-007/ADR-008 production blocks remain until their exact evidence and approval gates pass.

Approval does **not** approve a cloud, vendor, production deployment, capability activation, SLO, capacity, budget, or Kubernetes exclusion forever.

## Requirements-traceability updates

| Requirement | Stage 15 design evidence | Validation evidence required later |
|---|---|---|
| `ARK-FR-001` | Control/config/usage roles and environment-scoped release/config identities | Config/permission/release isolation tests |
| `ARK-FR-002/003` | Data-worker/object/catalog placement and migration/backup contracts | Cross-environment ingestion/restore/integrity tests |
| `ARK-FR-004/005/006` | API/capability role packaging and exact compatible contracts | Image/role/contract/version tests |
| `ARK-FR-007/008` | Scheduler/worker/maintenance roles, leases/fences, handler compatibility | Restart/rolling/mixed-version/job recovery tests |
| `ARK-FR-009` | Separate model assignment and artifact deployment lifecycle | Registry/assignment/load/rollback tests |
| `ARK-FR-010/011` | Conditional publisher/delivery not deployed; egress denied until admission | Absence/activation and destination/secret tests |
| `ARK-FR-012` | Shared validation/LAB evidence lane without inferred promotion authority | Environment/evidence access and release-gate tests |
| `ARK-NFR-001/003/005` | Environment/role identities, network/data/secrets isolation, no prod data in dev | Cross-env/tenant/role/secret/egress negative tests |
| `ARK-NFR-002/006` | Immutable release/config/migration/model/IaC identities and evidence manifest | End-to-end deployed-version/lineage/audit trace |
| `ARK-NFR-004` | Process-independent PostgreSQL jobs, graceful shutdown, restart/fence/rollback | Kill/redeploy/stale-worker/rollback fault tests |
| `ARK-NFR-005` | Role/pool isolation and scaling ladder before service extraction | Resource/noisy-neighbor/load tests |
| `ARK-NFR-007` | No unsupported topology/capacity/SLO/cost claim; explicit blocks | Stage 17 evidence and sponsor target register |
| `ARK-CON-001/002` | Coordinated modular-monolith release with role separation, owned schemas/migrations | Build dependency/schema/role packaging tests |
| `ARK-CON-004/005` | Environment-provided object/PostgreSQL contracts; no broker/Kubernetes job authority | Storage/job deployment and recovery tests |
| `ARK-CON-007` | Kubernetes/vendor/microservices/multi-region deferred to measurable gates | Stage 23 anti-overengineering review |
| `SC-02-04/05/06/08/09/10/11/12` | Truthful role failure/recovery, isolation, no action, ownership, blocks, and release evidence | Stage 16 deployment/recovery/security suites |

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Simplest adequate model recommended | PASS CONDITIONALLY | Role-based coordinated release; simple container runtime preferred, process compatibility retained |
| Kubernetes compared, not automatic | PASS | Alternatives and measurable admission gate |
| Environments/config/containers/CI-CD/migrations/models/IaC/secrets/scaling/backups/rollback/releases/dev-test covered | PASS | Dedicated sections for every source bullet |
| Modular ownership mapped without service-per-module | PASS | Runtime-role matrix and ADR-003 preservation |
| Alternatives and extraction/scaling triggers explicit | PASS | Alternative/Kubernetes/scaling matrices |
| Unknown hosting constraints remain explicit | PASS — APPROVAL GATE ACTIVE | `DEPLOYMENT_ENVIRONMENT_BLOCKED`, open questions, exact decision request |
| Operability by known team | CONDITIONAL / NEEDS HUMAN CONFIRMATION | Team is unknown; simple baseline minimizes burden but makes no staffing claim |
| All capability/security blocks preserved | PASS | Facts, blocks, model/network sections and decisions |
| Authorized platform review reconciled | PASS | No critical/high defect; two stale references corrected; reviewer stated no further pass required |
| Stage 16 not executed | PASS | Scope, decisions and stop condition |

**Gate result: PASSED AND APPROVED.** The logical design covers every deployment concern and provides the simplest provisional baseline. The authorized platform review found no unresolved critical or high defect after two stale mechanical references were removed, workspace structure/source-integrity validation passed, and the sponsor explicitly approved Stage 15 on 2026-08-13 with Python, PostgreSQL, one Linux server, sponsor operation with AI assistance/no assumed 24/7 team, optional containers, no Kubernetes, and evidence-triggered Rust/data-lake infrastructure. Accepted ADR-009 records the decision. Remaining production environment details stay `DEPLOYMENT_ENVIRONMENT_BLOCKED`; Stage 16 alone is authorized.

## Downstream consequences

- Stage 16 must test artifact provenance, role/config/environment isolation, migrations, mixed-version compatibility, graceful shutdown/restart, fences, release manifests, rollback layers, backup/restore/reconciliation, secrets/egress, and conditional-role absence.
- Stage 17 must measure workload/resource/queue/database/object/model/telemetry costs and evaluate role sizing, replicas, autoscaling, managed-service or Kubernetes need without purchasing by default.
- Stage 20 must name platform/database/storage/security/release/incident/on-call owners and sequence environment/capability admission.
- Stage 22 must map eight use cases to these roles and physical placements after environment evidence, without treating each role/module as a service.
- Stage 23 must retain the rejection of Kubernetes, service-per-capability, mesh, broker, workflow engine, permanent environment sprawl, and multi-region active-active until triggers pass.

## Exact next-stage inputs and stop condition

Stage 15 and ADR-009 are approved and Stage 16 is authorized. Do not execute Stage 17.

Stage 16 must read:

1. Approved `outputs/stages/00-source-audit.md` through `outputs/stages/15-deployment-infrastructure.md`
2. Accepted ADR-000 through ADR-009
3. `sources/normalized/system-design-prompt.md` section **15. Testing strategy**
4. All service-card testing/current-gap sections selected through `SOURCE_MANIFEST.md`
5. `stages/16-testing.md`, `templates/stage-output.md`, and directly referenced test matrices

Execute Stage 16 only. Do not begin Stage 17 until Stage 16 passes its gate and the sponsor explicitly authorizes continuation.
