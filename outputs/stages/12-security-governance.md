# Stage 12 — Security, privacy, and governance

Status: `APPROVED`

## Purpose and scope

Define the minimum implementable trust, authorization, tenant-isolation, privacy, data-governance, model/LLM, abuse-prevention, and software-supply-chain controls for ARK. The design applies to the approved modular monolith and its separately runnable API, scheduler, ingestion, worker, publisher, and delivery roles without turning those roles into services.

This stage defines logical security contracts and production-admission blocks. It does not select an identity provider, cloud, secrets product, key-management product, encryption algorithm, region, compliance regime, retention duration, recovery behavior, deployment topology, or numeric abuse/rate threshold. It does not enable any capability, Synapse interface, webhook, proactive action, or production agent. Stage 13 is not executed.

The sponsor explicitly approved Stage 11's “no agent justified by current evidence” result on 2026-08-12 and authorized Stage 12 only. On 2026-08-12 the sponsor explicitly approved Stage 12 and accepted ADR-008, including its narrow supersession of ADR-007's local model-cache key clause, and authorized execution of Stage 13 only.

## Inputs read in full

- `AGENTS.md` — all sections
- `WORKFLOW.md` — all sections
- `STATUS.md` — all sections after recording Stage 11 approval
- `SOURCE_MANIFEST.md` — all sections
- `stages/STAGE-CONTRACT.md` — all sections
- `stages/12-security-governance.md` — all sections
- `templates/stage-output.md` and `templates/adr.md` — all sections
- `sources/normalized/system-design-prompt.md` — **11. Security, privacy, and governance** exactly
- `sources/normalized/ark-assumptions.md` — all sections
- Approved `outputs/stages/01-discovery-and-questions.md` through `outputs/stages/11-agent-architecture.md` — all sections
- Accepted `decisions/ADR-000-temporary-source-evidence-disposition.md` through `decisions/ADR-007-versioned-ml-lifecycle-and-production-admission.md` — all sections
- `sources/normalized/service-cards/churnobyl.md`, `RFM.md`, `next_purchase_prediction.md`, `recommender.md`, `Synapse_chatbot.md`, `synapse_message_generator.md`, and `synapse_campaign_verifier.md` — all sections, subject to ADR-000/ADR-007 evidence restrictions

The Stage 12-authorized `assurance_reviewer` performed a bounded, read-only adversarial review of the trust boundaries, tenant-bearing assets, threats, controls, unresolved production blocks, and completion gate. Its initial challenge identified the material Stage 06/ADR-007 model-cache contradiction. The primary agent reconciled that finding through both cache matrix rows, `C-12-11`, `SEC-ADM-08`, and proposed ADR-008's Decision 12 and narrow supersession clause. The final reviewer pass reported no critical or high defects and recommended `PASS`. The primary agent remains the sole writer.

## Source-instruction coverage

| Source requirement | Addressed in | Status/evidence |
|---|---|---|
| Tenant isolation | Tenant-bearing asset control matrix | Every required asset has identity source, authorization, isolation, and audit behavior |
| Identity and access management | Identity, authentication, and authorization contract | Principal and permission model defined; concrete IdP/credential profiles remain production-blocking |
| Service-to-service authentication | Workload identity and delegated execution | Distinct workload identities and non-forgeable execution context required |
| Least privilege | Authorization and privilege-separation rules | Deny by default, narrow permissions, owner-module enforcement, no ambient cross-module access |
| Secrets handling | Secrets and key-control contract | No source/config/log secret material; versioned scoped delivery and rotation/revocation required |
| Encryption in transit and at rest | Encryption and integrity controls | Mandatory control intent; products/algorithms/key topology remain environment inputs |
| PII protection | Classification, minimization, and provider-transfer controls | Opaque identifiers by default; raw PII excluded from telemetry and external LLM use |
| Data residency | Residency and location-policy contract | Policy-bound placement/processing; no production onboarding without authoritative rules |
| Auditability | Security audit contract | Privileged/security effects require immutable correlated audit evidence |
| Consent and permission handling | Purpose, consent, and action-authority controls | Versioned effective policy references and fail-closed rechecks |
| Retention and deletion | Lifecycle governance | Logical revocation plus policy-driven purge across every copy/derivative; durations unresolved |
| Model access controls | Model/artifact and deployment controls | Exact approved assignment, digest, tenant/capability namespace, and distinct lifecycle permissions |
| Prompt/tool security for agents | LLM/provider boundary and conditional future-agent controls | No active agent/tools; bounded LLM controls required; Stage 11 future gate retained conditionally |
| Abuse prevention | Abuse and resource-exhaustion controls | Layered bounded admission, quotas, payload/content limits, destination restrictions, and audit |
| Dependency and supply-chain risks | Software/model supply-chain controls | Provenance, integrity, review, scanning, and least-privilege release path required |
| Concise realistic threat model | Threat model | Trust boundaries, realistic threats, mitigations, residual blocks |

## Facts

1. ARK is multi-tenant and may process PII or pseudonymous identifiers, behavioral and transactional histories, purchase values, campaign content, and model outputs. `outputs/stages/01-discovery-and-questions.md — Workload and sensitivity facts`.
2. Tenant identity comes from the authenticated principal, never a request-body tenant/business/customer value. Isolation applies to rows, objects, datasets, models, jobs, events, caches, quotas, audit, logs, metrics, and traces; PostgreSQL row-level security is defense in depth. `sources/normalized/ark-assumptions.md — Security, ownership, and operations`, item 25.
3. ARK minimizes PII and uses tenant-scoped opaque identifiers where possible; presentation data remains in consuming platforms unless explicitly required. `sources/normalized/ark-assumptions.md — Security, ownership, and operations`, item 29.
4. The edge is responsible for authentication and coarse admission, but owner modules retain semantic authorization. The API contract currently uses a temporary bearer presentation and immutable `AuthContext`; issuer, token format, client flow, optional mTLS, and IdP are unresolved at the Stage 12 expiry of the trust portion of `A-07-INTEGRATION`. `outputs/stages/07-api-integration.md — A-07-INTEGRATION`; `decisions/ADR-004-api-contract-boundary.md — Decision`.
5. Control-plane authority, dataset readiness, capability scientific eligibility, job lifecycle, model promotion/deployment assignment, proactive action, and external delivery are distinct authoritative decisions. `outputs/stages/05-end-to-end-architecture.md — Boundary map`; accepted ADR-005 through ADR-007.
6. PostgreSQL initially stores bounded operational state and object storage holds large immutable raw/curated/derived/result/model evidence. Shared infrastructure does not grant shared business ownership. `outputs/stages/06-data-architecture.md — Zone and authoritative-writer matrix`; accepted ADR-003.
7. Stage 08 uses durable jobs, immutable admitted handler/version, attempt leases and fencing; a worker or stale attempt cannot broaden tenant scope or commit an effect without the current fence. `decisions/ADR-005-postgresql-job-state-machine.md — Decision`.
8. Stage 09 requires Phase A, Phase B, and execution-time rechecks of subscription, grant, freshness, policy, quota, cooldown, deduplication, and audit before any permitted action or notification. An LLM/verifier output is never authority. `decisions/ADR-006-governed-proactive-action-and-delivery.md — Decision`.
9. All seven capability production profiles are blocked under accepted ADR-007. The three Synapse profiles remain interface-only and `EVIDENCE_BLOCKED`; provider, model, prompt, storage, data use, retention, safety, and reliability evidence is absent. `decisions/ADR-007-versioned-ml-lifecycle-and-production-admission.md — Decision`.
10. No production agent is justified or selected. Agent tools, memory, planner, MCP, A2A, and autonomous effect paths are not active architecture. `outputs/stages/11-agent-architecture.md — Decisions`.
11. Authoritative compliance duties, residency, retention/deletion periods, identity provider, role bindings, secret/key environment, webhook security profile, and named security/on-call authorities remain unknown. `outputs/stages/01-discovery-and-questions.md — SEC-01 through SEC-06`; `STATUS.md — Known blockers`.
12. Accepted Stage 06 requires tenant and exact version in cache identity, while accepted ADR-007 says a local model cache is keyed by exact bundle digest. Digest-only byte lookup can conflict with tenant/capability authorization unless shared-byte reuse is explicitly classified and kept behind tenant-specific assignment checks. This material contradiction was identified by the Stage 12 assurance review and is not silently resolved. `outputs/stages/06-data-architecture.md — Tenant and access-isolation rules`; `decisions/ADR-007-versioned-ml-lifecycle-and-production-admission.md — Implementation constraints`.

## Assumptions

Stage 12 introduces no temporary assumption and does not silently extend an expired one.

| ID | Assumption/status | Stage 12 effect | Risk | Validation/expiry |
|---|---|---|---|---|
| `A-01-SCALE` | Numeric traffic, quota, abuse, storage, latency, and cost targets remain unknown | Control semantics are defined; concrete activation values remain required | Production denial-of-service and cost fitness are unproven | Authoritative measurements and Stage 17 |
| `A-01-OPS` | Deployment, recovery, support, and environment remain unknown | Logical identities, encryption, secrets, and audit interfaces are portable; product/topology is deferred | Environment may impose stricter controls | Stages 13–15 and authoritative environment |
| `A-04-OWNERSHIP` | Logical owner roles suffice; named authorities remain absent | Every control has a logical owner; production, promotion, grants, and extraction stay blocked | Separation and on-call feasibility are unproven | Named assignments or existing earlier expiry |
| `A-07-INTEGRATION` non-trust portions | Adapter ownership, polling baseline, conditional webhook, and cutover treatments retain their existing expiries | Consumer translation remains outside cores; polling remains authoritative | Consumer constraints may differ | Existing per-portion expiries |

The Stage 12 trust portion of `A-07-INTEGRATION` and the security-policy questions covered by `A-01-SEC` are not extended. Proposed ADR-008 replaces them with explicit target controls and fail-closed production-admission blocks.

## Analysis and recommendations

### Security invariants

1. Every request, command, job, event, delivery, model operation, and storage access has one authenticated actor/workload identity and one server-derived tenant scope. Missing, ambiguous, expired, revoked, or conflicting identity is denied.
2. A caller-supplied ID is a lookup key only. The owner loads the resource, verifies its stored tenant and policy scope against trusted context, and conceals cross-tenant existence.
3. Edge authentication and coarse scope checks never replace owner-module authorization at the command/query/effect boundary.
4. Authority can only narrow across delegation. API → job → attempt → owner effect and parent → child flows retain the original actor/tenant/purpose and add a distinct workload/execution principal; they cannot substitute a new tenant.
5. Shared code, cluster, connection pools, telemetry libraries, or object-storage adapters never imply shared data access. Each module/state set has one writer and explicit read grants.
6. Privileged or externally consequential effects are fail-closed when required authorization, policy, consent/purpose, audit, exact version, or owner evidence is unavailable.
7. Security audit is authoritative evidence; logs, metrics, and traces are supporting telemetry and may not become permission or tenant sources.
8. No mutable alias (`latest`, arbitrary path, caller-selected provider/config/tool) can select a model, artifact, policy, secret, endpoint, or executable behavior.

### R-12-01 — Identity, authentication, and authorization contract

ARK uses a provider-neutral trust-profile registry. A production-enabled credential class must identify a registered issuer/trust anchor, validation mechanism, audience, credential type, tenant-binding rule, subject type, allowed scopes/attributes, lifetime/revocation behavior, and responsible owner. Validation produces immutable trusted context:

```text
AuthContext {
  subject_id, actor_type, tenant_id,
  permissions[], roles_or_attributes[],
  credential_id, trust_profile_id, issuer_id,
  audience, authenticated_at, expires_at,
  delegation_chain?, assurance_level?, correlation_id
}
```

The field set is a logical contract, not a token schema. Claims are accepted only from the configured validator; request headers/bodies cannot add or broaden them. Every non-health external endpoint authenticates. Privileged human operations require an approved stronger-authentication/step-up policy; exact mechanism and assurance levels remain unresolved and block activation.

Authorization is deny-by-default and permission-based. Coarse edge checks reject obviously unauthorized routes; the authoritative owner module checks the exact action, resource tenant, resource state, purpose, data class, capability/operation, and policy version immediately before effect. Logical permissions include tenant control, ingestion, dataset access, capability invocation, job read/cancel, training, evaluation, promotion, deployment assignment, grant request/approval/revocation, delivery administration, audit access, and retention/deletion execution. Exact role-to-permission bindings and prohibited combinations are policy inputs, not inferred team structure.

- **Requirement/where:** IAM, least privilege, principal-derived tenant; every Stage 07 API and internal port.
- **Simplest implementation:** one authentication adapter and shared immutable context type plus owner-module policy functions and database roles/RLS as defense in depth.
- **Alternative rejected:** gateway-only authorization or a body tenant header; it creates confused-deputy and cross-tenant bypass paths.
- **Trade-off:** repeated owner checks and a policy registry add implementation work; authority remains visible and testable.
- **Reconsideration:** a concrete policy engine/product only when rule complexity, independent administration, or measured evaluation burden exceeds typed policies and a dedicated ADR approves it.

### Workload identity and delegated execution

- Each independently runnable API, scheduler, ingestion, worker-pool, publisher, delivery, maintenance, and build/release role receives a distinct non-human identity. Shared credentials and long-lived embedded API keys are prohibited.
- A workload proves its own identity to infrastructure. It receives only the database schema/commands, object prefixes, secret references, provider endpoints, and queues/handler types required for its role.
- A worker acts only when the job manager supplies a signed or internally non-forgeable execution context bound to `tenant_id`, `job_id`, `attempt_id`, fence, handler/version, purpose, and exact input/data/model/config references. Workload identity authorizes the worker role; the execution context authorizes the particular tenant work. Neither alone is sufficient.
- In-process calls still pass immutable trusted context and invoke public owner ports. Separately deployed roles require mutually authenticated encrypted transport under the later deployment environment; process separation never weakens owner authorization.
- Delegation chains and child jobs retain origin actor, causation, tenant, and narrowed scope for audit. Impersonation is an explicit privileged operation, never an ordinary field mutation.

### Tenant-bearing asset control matrix

| Asset/trust surface | Authoritative identity source | Authorization rule | Isolation mechanism | Mandatory audit behavior |
|---|---|---|---|---|
| PostgreSQL business/control rows | `AuthContext.tenant_id` or fenced job context; stored `tenant_id` | Owner-module command/query permission; resource tenant must match; DB role cannot bypass owner | Tenant key on every row, module-owned schema/writer, restricted DB roles, parameterized access, RLS defense in depth | Mutations, privileged reads/exports, denials, policy/version and actor/correlation |
| Idempotency, schedule, quota, cooldown, grant, subscription, and configuration records | Original authenticated command plus stored tenant | Exact control permission; ETag/state/version checks; grants require approved role policy | Tenant-qualified unique keys, owner schema, CAS transitions, no caller priority/scope broadening | Create/change/revoke/deny, old/new refs, approver/requester, reason, policy version |
| Object paths: raw, quarantine, curated, features, results, artifacts, reports, backups | Server-generated tenant-scoped object reference from trusted context | Owner issues bounded read/write/delete capability for exact namespace/object/purpose | Non-guessable opaque ref, enforced tenant prefix/bucket policy, short-lived scoped access, checksum, no caller path | Authority issuance/use for sensitive objects, publication/deletion, checksum failure, denied cross-scope access |
| Source contracts, ingestion runs, datasets, quality and lineage | Authenticated source/job tenant plus catalog-owned stored tenant | Registered source and data permission; dataset purpose/readiness/policy check | Immutable tenant-qualified IDs, owned catalog writer, by-reference objects, no unregistered source | Registration, receipt, quarantine, readiness/revocation, access/export, lineage change, policy refs |
| Capability feature/state/result rows and objects | Trusted invocation/job tenant and capability owner | Entitlement + operation permission + exact dataset/config/model authorization; owner-only write | Capability-owned schema/prefix, tenant namespace, immutable published versions, no cross-capability writes | Invocation/outcome/result access, fallback/ineligibility, sensitive export, version lineage |
| Model/artifact/experiment/evaluation registry | Trusted lifecycle command/job tenant | Separate train/evaluate/promote/assign/load permissions; exact approved assignment required and rechecked before cache use | Tenant/capability namespace, immutable digest/version, owner writer; model cache identity is `{tenant, capability, purpose, exact assignment/version, bundle digest}`; no `latest`; digest-only byte reuse requires a later explicit shared-artifact decision | Register/evaluate/promote/reject/assign/rollback/revoke/load/cache denial with actors/evidence |
| Jobs, attempts, leases, checkpoints, concurrency scopes | Authenticated submission tenant; job-manager-created attempt/fence | Submit/read/cancel by operation/resource permission; workers only typed handlers and current fence | Tenant row keys, job-manager sole lifecycle writer, fenced effects, tenant/pool concurrency leases, scoped checkpoints | Submission/replay/conflict, claim, state/retry/cancel/fence rejection, result/evidence linkage |
| Internal events/outbox/handlers | Producer's committed tenant fact | Producer may emit approved schema; named consumer permission and exact schema/filter; handler maps to typed command only | Tenant-qualified event/outbox row, authorized producer/consumer, minimal refs, dedupe/version checks | Publish/attempt/consume/reject/replay/dead-letter, causation, schema and decision refs |
| External notifications, endpoints, subscriptions, deliveries | Authenticated registration tenant plus source resource tenant | Endpoint/event-subscription permission; exact registered endpoint; Stage 09 authority recheck; no arbitrary URL | Tenant-scoped endpoint/subscription/secret, destination validation, signed minimal payload, stable event ID | Register/verify/rotate/disable, intent, attempt/response class, replay/dead-letter, no raw secret/body logging |
| Caches and local worker/model caches | Trusted request/job tenant plus exact immutable source identity | Same authorization as authoritative source, rechecked before lookup/use; cache never grants access or selects an assignment | Tenant, owner/capability, purpose, exact assignment/version, and digest in model-cache identity; tenant partition for other caches; encrypted where sensitive; bounded TTL/eviction; no cross-tenant value visibility; digest-only byte reuse requires a later explicit shared-artifact decision | Configuration/flush, shared-artifact classification, security anomaly and authorization denial; access telemetry without sensitive keys or high-cardinality IDs |
| Secrets, credentials, keys, provider and webhook signing material | Workload/human identity and registered secret metadata tenant/owner | Exact role/purpose/environment/version; no general list/read; separation for administration/use | Managed secret interface, encryption, versioning, rotation/revocation, no source/config/artifact/log plaintext | Create/rotate/revoke/access/use denial with secret reference, never value |
| Audit ledger | Original trusted actor/workload/tenant plus evidence writer | Append by approved owners; restricted tenant/security read; no mutation by audited component | Append-only owner schema/object evidence, integrity/version checks, tenant partition, separate access roles | Audit access/export/configuration and integrity verification are themselves audited |
| Application/security logs | Trusted instrumentation context; tenant only from trusted context | Operational/security read by approved scope; no business authority | Structured allowlist fields, opaque IDs, redaction, tenant/environment access partitions, bounded retention | Access/export/config changes and redaction failures; ordinary log emission is correlated, not recursively audited |
| Metrics | Server instrumentation; tenant dimension only from trusted context | Aggregate operational access; per-tenant visibility policy | No raw PII/secrets/object paths; bounded labels; tenant label only where necessary and access-controlled | Dashboard/export/config/alert-rule changes; security counters correlate to audit refs |
| Traces | Server-generated trace context plus trusted tenant/correlation | Approved operational access; trace context never authorizes | Sanitize attributes/baggage, no credentials/payloads, tenant partition/access filter, sampling policy | Trace export/access/config changes; security-sensitive spans link audit IDs |
| Usage, metering, cost, and rate/abuse state | Trusted API/job/provider adapter tenant and operation identity | Control/metering writer only; tenant can read only its approved view; caller cannot set usage | Tenant-qualified counters/reservations, idempotent effect IDs, bounded provider-cost evidence | Reservation/commit/release/adjustment, override, threshold denial, reconciliation |
| Administrative exports and LAB evidence packages | Authenticated requester tenant/scope plus source record tenants | Explicit export/LAB permission, purpose, data-class ceiling, expiry; cross-tenant aggregation requires separate authority | New immutable package/ref in scoped namespace, minimization/redaction, manifest and expiry | Request/approve/create/download/expire/delete with included sources and purpose |

The matrix is normative: adding a tenant-bearing asset requires these four fields before implementation or activation.

### R-12-02 — Secrets, encryption, and integrity

- Secrets enter through a managed secret-delivery interface and are referenced by opaque ID/version. They are never committed to source, embedded in images/models/notebooks, accepted in business payloads, written to result objects, or logged/traced.
- Secret access is granted to a distinct workload/purpose/environment and supports rotation, revocation, overlap where required, access audit, and emergency invalidation. Provider and webhook credentials are separate by tenant/endpoint where policy requires; no unscoped platform master credential reaches capability code.
- All external network traffic and any inter-process traffic carrying credentials, tenant data, control commands, results, or telemetry uses authenticated encryption in transit. PostgreSQL, object data, backups, artifacts/models, audit, and retained telemetry use approved encryption at rest.
- Key ownership, algorithm/cipher versions, rotation, tenant-specific or customer-managed keys, hardware boundary, and regional key placement require authoritative environment/compliance evidence. Missing values block production activation; Stage 12 does not choose them.
- Checksums/digests and signatures provide integrity/provenance, not confidentiality. Object/model/build digests are verified before publication/load; mutable aliases cannot bypass verification.

### R-12-03 — Data classification, PII, residency, consent, retention, and deletion

Every source contract, dataset/object, feature/result, prompt/context, feedback record, audit/export, and model evidence record carries or resolves to a versioned classification, purpose, policy/consent reference where applicable, residency policy, retention policy, and owner. Unknown classification defaults to the most restrictive admitted handling and cannot be sent externally.

Data classes are registry-defined rather than invented here. At minimum the registry must distinguish public/non-sensitive, internal operational, tenant confidential, personal/pseudonymous, secrets/credentials, and restricted raw/quarantine material; exact legal categories are authoritative policy inputs.

- Use tenant-scoped opaque subject/item IDs. Names, phone numbers, free-form presentation data, and raw customer content remain outside ARK unless a release-scoped contract proves necessity and policy authority.
- Sensitive values do not appear in URLs, object names, idempotency keys, correlation IDs, event payloads, logs, metric labels, trace baggage, or error messages.
- Purpose and consent are effective-dated/versioned. Ingestion preserves source authority; use-time checks verify allowed purpose, channel/data scope, validity, and revocation. A proactive grant cannot replace consent or policy authority.
- Residency policy constrains ingest, storage, processing, backup, telemetry export, model/provider transfer, and administrative access. Every physical copy/processor must be locatable from metadata. Stage 15 may choose placement only after these policies exist.
- Retention is per tenant/data class/purpose/record type, not one global duration. No duration is guessed. Expiry removes ordinary access and schedules an authorized deletion workflow.
- Deletion/erasure uses immediate logical revocation/tombstoning plus policy-driven physical purge from operational rows, objects, caches, search/read models, features/results, exports, provider copies, and backups according to the approved policy. Immutable historical identifiers/evidence retain only the minimum lawful non-content proof.
- A deletion-impact manifest traces affected datasets, features, experiments, models, results, notifications, and exports. Policy decides whether a derived artifact remains lawful, requires retraining, is revoked, or needs provider deletion; ARK does not claim generic “model unlearning.” Legal hold overrides purge only through an authorized, time-bounded, audited record.

Before production onboarding, accountable policy owners must approve classification, purpose/consent authority, residency, retention, erasure, legal-hold, backup-copy, audit-retention, and derived/model handling for every release data class.

### R-12-04 — Audit, privileged operations, and governance separation

The audit ledger records actor and workload identity, tenant, action, target/ref, old/new immutable versions or state transition, authorization/policy/consent evidence, decision and reason, request/correlation/causation/job/execution IDs, timestamp, outcome, and code/config versions. It stores no secret value or unnecessary raw PII.

Mandatory-audit operations fail closed before effect: identity/trust/profile administration; role/permission and privileged access changes; tenant/subscription/quota/grant/policy changes; sensitive export/access; source/dataset readiness or revocation; secret/key/endpoint changes; retention/deletion/legal hold; model promotion/assignment/rollback/revocation; proactive task/notification authorization; administrative retry/replay/override; and release/provenance decisions. Audit writer outage cannot be bypassed by logging locally and acting first.

Training, scientific recommendation, promotion approval, deployment assignment, security/policy approval, grant request/approval, and operations recovery remain distinct permissions. Exact human role bindings, dual-control requirements, emergency access, session rules, and named authorities are unresolved; high-impact operations remain disabled until an approved matrix names who may hold which combinations. Emergency access, if later required, must be time-bounded, purpose-bound, independently approved where policy requires, and reviewed from immutable audit.

### Model, LLM, prompt, and conditional agent controls

#### Model and artifact access

- Registry presence is not authority. Training, evaluation, promotion, assignment, loading, inference, rollback, and revocation use separate permissions and exact immutable evidence.
- Workers load only the assignment-authorized tenant/capability/operation bundle after tenant namespace, digest, schema/preprocessor/handler/runtime compatibility, promotion state, revocation, and purpose checks.
- Model caches are bounded and keyed by the full authorization identity `{tenant, owner/capability, purpose, exact assignment/version, bundle digest}`; cache hits rerun current assignment, purpose, compatibility, promotion, and revocation authorization and cannot broaden assignment. A lower-level immutable byte cache may deduplicate by digest only after an explicit shared-artifact classification, and it never becomes selection, metadata, or access authority.
- Training/evaluation data and artifacts inherit classification/residency/retention. Cross-tenant training, shared models, protected-attribute use, and data export are absent unless a later explicit source/policy/decision authorizes them.

#### Bounded LLM/Synapse security gate

Synapse remains `EVIDENCE_BLOCKED` and no production request may be sent to a provider. Re-entry requires authoritative provider/model and processor identity; data-use/training/retention/deletion/residency/subprocessor terms; approved egress destination; input/output schemas and size/content bounds; prompt/context/policy versions; secret separation; tenant/purpose/data-class controls; injection and exfiltration tests; content-safety/refusal policy; output validation; usage/cost limits; audit/telemetry redaction; failure/fallback; and named security/operations owners.

When admitted, external content is untrusted data, not instructions or authority. Context assembly allowlists registered sources, minimizes data, separates instructions from content, records provenance, and never includes secrets. Outputs are untrusted until schema/content/policy validation and cannot directly modify state, choose a tenant/provider/tool, authorize a campaign, or trigger an irreversible effect. The verifier remains advisory.

No agent or tool execution exists. Stage 11's prompt/tool/memory/delegation/approval controls remain conditional re-entry requirements only. If Stage 11 is ever superseded, per-tool authorization, tenant-isolated credentials/memory, injection/exfiltration controls, bounded steps/time/cost, Stage 08 fencing/idempotency, and Stage 09 external authority rechecks are mandatory before an agent can act.

### R-12-05 — Abuse, confused-deputy, and egress prevention

- Enforce request schema/size/content-type limits at the edge and again at the owner; use registered object references for bulk content.
- Apply authenticated principal/tenant/operation rate policy, quota reservation, concurrent-job/worker limits, storage/object limits, provider-cost limits, and fixed policy-owned priority. Exact values are mandatory activation inputs and remain for Stage 17.
- Deny arbitrary callback URLs, object paths, provider endpoints, prompt templates, model aliases, tool names, workflow graphs, SQL/filter expressions, and caller-defined priorities. Resolve only registered tenant-owned/versioned references.
- Webhook destinations require ownership verification, allowed scheme/port/network policy, DNS/IP revalidation at effect time, redirect restrictions, signed payloads, secret rotation, replay protection, bounded response handling, and delivery quotas before activation. Exact signing and replay policy remain unresolved.
- Validate archive/file types, checksums, declared sizes, parser limits, and quarantine behavior; workers process untrusted inputs with least privilege and bounded resources.
- Use explicit egress allowlists for providers, webhooks, telemetry exporters, dependency/build fetches, and administrative exports. A capability or model cannot initiate arbitrary network access.
- Security-relevant denials, anomaly/rate decisions, endpoint/provider changes, and administrative overrides are auditable; automated responses must not leak cross-tenant existence or sensitive policy detail.

### R-12-06 — Software, model, and build supply chain

The simplest viable supply-chain contract is one controlled build/release path with:

1. reviewed source changes and module ownership;
2. pinned/locked direct and transitive dependencies plus license/vulnerability policy;
3. isolated least-privilege builds with no production data and tightly scoped dependency egress;
4. secret scanning and prohibition of secrets in source, images, notebooks, model bundles, logs, and test fixtures;
5. generated software bill of materials and provenance linking source, dependencies, build environment, tests, and immutable artifact/image/model digest;
6. malware/unsafe-deserialization and dependency/model artifact scanning before registry admission;
7. signature/digest verification at promotion, deployment assignment, worker load, and rollback;
8. separate build, promotion, assignment, and production-use permissions with immutable audit;
9. approved base-image/runtime/dependency update and revocation process; and
10. test data that is synthetic or explicitly authorized, tenant-scoped, minimized, and deleted by policy.

A new commercial supply-chain platform is not selected. Concrete CI/CD, artifact repository, scanner, signing service, and remediation timelines depend on Stage 15/16 environment and policy evidence.

### Concise threat model

| Trust boundary / asset | Realistic threat | Required mitigation | Residual/blocking evidence |
|---|---|---|---|
| Consumer/adapter → ARK edge | Forged/stolen credential, body-tenant override, IDOR, oversized/replayed request | Registered trust profile, immutable AuthContext, owner resource check, no tenant header, idempotency, schema/size/rate limits, concealed denial | IdP/credential/revocation/assurance profile unresolved; external production blocked |
| Edge/control → module owner | Gateway compromise or confused deputy broadens scope | Owner-module deny-by-default authorization; exact resource/purpose/version check; narrow immutable context; audit | Role/permission matrix and named owners unresolved |
| API/scheduler → job/worker → effect | Forged job, stale attempt, cross-tenant checkpoint/result, privilege escalation | Job-manager-only transitions, workload identity, exact tenant/job/handler context, leases/fencing, scoped storage/secrets, at-effect recheck | Workload credential mechanism/placement unresolved |
| PostgreSQL/object/data lake | SQL/RLS bypass, object-prefix traversal, shared credential, exfiltration, deletion failure | Module DB roles/writers, RLS defense, server-generated opaque refs, scoped access, encryption, classification/residency/retention/deletion manifests | Concrete keys, residency, retention, erasure/legal-hold policy unresolved |
| Model/artifact registry and cache | Tampered artifact, `latest` substitution, unauthorized model/tenant load, poisoned dependency | Immutable digest/provenance, exact assignment, distinct lifecycle permissions, compatibility/revocation check, tenant cache key | Capability profiles already production-blocked; authority matrix absent |
| Proactive control/event/delivery | Verifier output or stale grant authorizes action; duplicate/replayed delivery; SSRF | Stage 09 Phase A/B/at-effect checks, deterministic policy, transactional intent/audit, registered verified endpoint, signature/replay/dedupe | Roles, destination/signing/replay policies and named workflow absent; activation blocked |
| ARK → external LLM/provider | PII/secret exfiltration, provider retention/training, prompt injection, unsafe output, cost abuse | Egress allowlist, approved processor terms, minimization/classification, prompt provenance/separation, no tools, output validation, quota/audit | All Synapse profiles `EVIDENCE_BLOCKED`; no production transfer |
| Logs/metrics/traces/audit/export | PII/secret leakage, high-cardinality tenant leakage, unauthorized operator access, audit tampering | Allowlisted/redacted fields, access partition, immutable audit, export purpose/expiry, access auditing | Retention/access policy and named operators unresolved |
| Build/dependency/model supply chain | Compromised package/image/model, leaked CI secret, unauthorized release | Locks/SBOM/provenance/scans, isolated build, digest/signature verification, separation of build/promote/assign | Environment/tooling and policy thresholds unresolved |
| Privileged human/insider | Excess privilege, self-approval, unaudited override, bulk export | Least privilege, high-impact permission separation, stronger auth, time-bounded emergency access, immutable audit/review | Concrete role combinations, dual control, named authorities unresolved |
| Resource/cost boundary | Tenant exhausts DB/workers/storage/provider budget and affects others | Admission/rate/quota/concurrency/storage/cost controls, fixed priority, resource pools, backpressure | Numeric targets/limits unresolved under `A-01-SCALE`; production profile blocked |

### Production security-admission register

These are explicit negative readiness states, not temporary assumptions and not claims that logical design is blocked:

| ID | State | Scope | Exit evidence |
|---|---|---|---|
| `SEC-ADM-01` | `EXTERNAL_TRUST_BLOCKED` | Public callers and separately deployed internal roles | Approved trust profiles, tenant-claim binding, credential lifecycle/revocation, human assurance, workload authentication, authorization/role matrix, named owners, and cross-tenant tests |
| `SEC-ADM-02` | `DATA_GOVERNANCE_BLOCKED` | Production onboarding/storage/processing of tenant data | Approved classification, purpose/consent, residency, retention, erasure/legal hold, backup/telemetry/export/model-derivative policies and owners |
| `SEC-ADM-03` | `CRYPTO_SECRETS_BLOCKED` | Production credentials, databases, objects, backups, artifacts, callbacks, providers | Approved encryption/key/secret architecture, rotation/revocation, access/audit, environment placement, and tests |
| `SEC-ADM-04` | `PRIVILEGED_ACTION_BLOCKED` | Grants, proactive notification/action, model promotion/assignment, sensitive export/deletion, emergency recovery | Named authorities, allowed role combinations/separation, stronger-auth policy, immutable audit availability, and negative/race tests |
| `SEC-ADM-05` | `EXTERNAL_DELIVERY_BLOCKED` | Webhook activation | Consumer contract, endpoint ownership/SSRF rules, signature/secret/replay policy, egress controls, rate/retry policy, and owner/runbook |
| `SEC-ADM-06` | `LLM_PROVIDER_BLOCKED` | Synapse/external model data transfer and execution | ADR-007 re-entry evidence plus provider/data-use/retention/residency, prompt/injection/exfiltration/safety, secrets/egress/cost, audit, and named owners |
| `SEC-ADM-07` | `SUPPLY_CHAIN_BLOCKED` | Production build/release/model load | Approved repository/build/artifact provenance, dependency/SBOM/scan/signature policy, least-privilege CI/CD identities, release separation, revocation, and test evidence |
| `SEC-ADM-08` | `MODEL_CACHE_BLOCKED` | Any cached model/artifact load | Sponsor acceptance of ADR-008's narrow ADR-007 refinement plus tests proving tenant/capability/purpose/assignment authorization precedes lookup/load; digest-only byte reuse allowed only for an explicitly shared artifact classification |

No entry can be cleared by file existence, registry presence, a successful prototype call, or telemetry alone. Exit requires authoritative evidence, tests, named accountable authority, and a recorded decision. Accepted ADR-007 capability blocks remain independently necessary.

### Anti-overengineering findings

- Use typed authorization policies, module/database roles, RLS defense, object-prefix policy, a narrow secret interface, immutable audit, and existing PostgreSQL/object-storage metadata first.
- Do not add a service mesh, standalone policy engine, SIEM/SOAR product, DLP platform, HSM, customer-managed key service, separate audit database, private certificate authority, WAF product, secrets product, or data-governance suite without environment/compliance/scale evidence and an accountable owner.
- Logical controls are mandatory even if implemented initially by framework middleware, database roles/policies, storage access policy, build tooling, and owned tables.
- No agent-specific runtime, tool sandbox, memory store, MCP/A2A security gateway, or agent trace product is justified.

## Decisions

- Propose `decisions/ADR-008-zero-trust-tenant-and-governance-boundary.md` to record the Stage 12 trust, tenant, governance, model/LLM, and production-admission boundary.
- The authenticated principal/trust profile and owner-stored resource tenant are authoritative. Request fields, paths, object names, event payloads, model outputs, and logs cannot create tenant or permission authority.
- Authentication is provider-neutral but not unspecified at activation: no external or workload credential class is production-enabled until its registered trust profile and tests are approved.
- Authorization is deny-by-default at both edge and authoritative owner module. Workload identity and delegated execution context are distinct and both required for background effects.
- Tenant isolation and audit behavior in the asset matrix are mandatory across all state and telemetry. RLS and infrastructure policy are defense in depth, not substitutes for owner checks.
- Accepted ADR-007's digest-only local model-cache wording conflicts with Stage 06 tenant cache identity. Proposed ADR-008 narrows it: authorization and cache identity include tenant, owner/capability, purpose, exact assignment/version and digest. A lower-level immutable byte cache may deduplicate by digest only after an explicit shared-artifact classification, and never becomes selection, metadata, or access authority. Until sponsor acceptance and tests, `MODEL_CACHE_BLOCKED` applies.
- Purpose/consent, classification, residency, retention/deletion/legal hold, encryption/key/secrets, privileged-role separation, webhook security, and supply-chain profiles are mandatory production inputs. Their absence is recorded as explicit blocked admission, not filled by convention.
- Synapse remains `EVIDENCE_BLOCKED` and `LLM_PROVIDER_BLOCKED`; no external LLM data transfer or execution is approved. No active agent/tool controls are introduced.
- No vendor, product, numeric threshold, compliance claim, production enablement, or Stage 13 reliability decision is made.

## Contradictions and dangerous assumptions

| ID | Evidence/tension | Treatment | Consequence |
|---|---|---|---|
| `C-12-01` | `A-07-INTEGRATION` temporarily presents bearer credentials but the issuer, token format, tenant binding, and revocation are unresolved at Stage 12 | Replace the trust portion with provider-neutral trust-profile requirements and `EXTERNAL_TRUST_BLOCKED`; do not extend bearer as production authority | API design remains implementable; external activation is denied |
| `C-12-02` | Immutable raw/versioned evidence conflicts with erasure and legal-hold duties | Preserve immutable identity/lineage while policy drives access revocation and physical purge; retain only lawful minimum audit proof | No blanket “immutable forever” or invented deletion promise |
| `C-12-03` | Shared PostgreSQL/object infrastructure can be mistaken for shared tenant/module access | Owner-module checks, distinct DB/storage roles, tenant keys/prefixes, one writer, RLS/policy defense | Shared infrastructure does not broaden authority |
| `C-12-04` | A workload service identity can be mistaken for tenant authority | Require both workload identity and immutable delegated job/request context; worker cannot choose tenant | Prevents confused-deputy background effects |
| `C-12-05` | Logs/traces often propagate arbitrary headers/baggage | Tenant only from trusted context; allowlist/redact telemetry fields | Observability cannot become an exfiltration or authority channel |
| `C-12-06` | Synapse API keys and request fields look like an acceptable trust/data-transfer contract | Treat only as legacy interface evidence; block production provider use until full security evidence | No provider/LLM call is security-approved |
| `C-12-07` | “No agent” can be misread as “no prompt injection/exfiltration risk” | Apply bounded LLM input/context/output/provider controls independently; retain conditional agent gate | Stage 11 conclusion does not waive LLM security |
| `C-12-08` | Audit availability can be treated as eventual logging for high-impact effects | Mandatory audit commits before/effectively with privileged decisions/intents; fail closed | Logs cannot backfill missing authority evidence |
| `C-12-09` | Encryption language can imply an approved algorithm/key topology/compliance state | Define control objective and admission evidence only; defer concrete environment choice | No unsupported compliance or crypto claim |
| `C-12-10` | Model registry presence can be mistaken for access/promotion authority | Exact approved assignment, digest, compatibility, revocation and separate permissions remain mandatory | No artifact file or alias activates a model |
| `C-12-11` | Stage 06 requires tenant/version cache keys, while accepted ADR-007 permits an exact-digest-keyed local model cache | Do not overwrite ADR-007 silently. Proposed ADR-008 explicitly refines the cache contract: tenant/capability/purpose/assignment authorization and identity wrap any byte-level digest reuse; digest-only reuse requires an approved shared-artifact classification | Model/artifact cache loading remains `SEC-ADM-08 MODEL_CACHE_BLOCKED` until ADR-008 is accepted and isolation tests pass |

## Open questions

| ID | Question | Blocking? | Options | Recommended temporary treatment | Effect |
|---|---:|---|---|---|---|
| `Q-12-01` | What IdP/trust anchors, credential types, issuer/audience validation, tenant-claim binding, credential lifetimes/revocation, human assurance, and workload authentication are authoritative? | Yes before external/internal production activation | Federated human/workload identities; opaque introspection; signed tokens; mTLS/workload identity; approved combination | No production trust profile; `SEC-ADM-01` remains blocked | No credential is assumed production-valid |
| `Q-12-02` | What exact permissions, role bindings, prohibited combinations, stronger-auth, dual-control, emergency-access, and session policies apply? | Yes before privileged operations | Sponsor/security-approved matrix | Deny all high-impact operations not explicitly assigned | `SEC-ADM-01/04` remain blocked |
| `Q-12-03` | Which legal, contractual, privacy, residency, breach, audit, and data-subject obligations apply by tenant/data class/jurisdiction? | Yes before production data onboarding | Supply authoritative policy register; explicitly declare non-applicability where lawful | Make no compliance claim; most restrictive handling and no external transfer | `SEC-ADM-02` remains blocked |
| `Q-12-04` | What classifications, purposes, consent authorities, retention periods, erasure/legal-hold/backup/model-derivative rules apply? | Yes before onboarding/processing | Per-class/tenant policies | Require policy refs; unknown class is restricted and unavailable | Data lifecycle cannot be production-configured |
| `Q-12-05` | What encryption/key ownership/rotation, secret store/delivery, certificate, tenant-key, and regional key requirements apply? | Yes before production/Stage 15 | Platform keys; tenant keys; customer-managed keys; environment combination | Keep logical controls only; no product/algorithm assumption | `SEC-ADM-03` remains blocked |
| `Q-12-06` | Which Synapse/provider/model, processor terms, data use/training, retention/deletion, residency/subprocessors, egress, prompt/safety, and cost controls are approved? | Yes before any Synapse production request | Approved provider; self-hosted evidence; scope out; remain unavailable | Remain `EVIDENCE_BLOCKED` and `LLM_PROVIDER_BLOCKED` | No external LLM transfer/execution |
| `Q-12-07` | Which consumers require webhook and what endpoint verification, network/redirect, signing, replay, secret-rotation, and authorization profile applies? | Yes before webhook activation | Polling only; per-consumer approved webhook | Polling only; webhook disabled | `SEC-ADM-05` remains blocked |
| `Q-12-08` | Who are the named security, privacy/data-governance, IAM, key/secret, audit, incident, data/model, provider, delivery, and supply-chain owners/on-call authorities? | Yes before production/Stage 20 | Assign accountable roster and runbooks | Logical roles under `A-04-OWNERSHIP`; no activation | All production admission remains blocked |
| `Q-12-09` | What audit/log/metric/trace/export retention, access, integrity, redaction, and tenant-reporting policies apply? | Yes before production observability/governance | Per record class and purpose | Minimize and restrict; no numeric period | Stage 14 cannot finalize evidence policy |
| `Q-12-10` | What request/job/storage/provider cost limits, abuse thresholds, lockout/challenge/escalation, and tenant fairness policies apply? | Yes before activation | Measured per operation/plan/resource | Require configured policy; no numeric defaults | `A-01-SCALE` and Stage 17 remain active |
| `Q-12-11` | What dependency, license, SBOM, provenance, signing, vulnerability, base-image/model-source, remediation, and release-separation policies apply? | Yes before production release | Organization-approved software/model supply-chain standard | Require evidence contract; no tool/vendor selected | `SEC-ADM-07` remains blocked |

## Requirements-traceability updates

| Requirement | Stage 12 design response | Verification direction |
|---|---|---|
| `ARK-FR-001` | Tenant/control/grant/quota/config permissions and mandatory audits are separate from execution | Unauthorized enablement/grant/quota mutation and no-side-effect tests |
| `ARK-FR-002/003` | Authenticated registered source, restricted raw/quarantine, classification/purpose/residency, immutable refs, deletion impact | Cross-source/tenant, malicious file, raw-access, policy and purge-manifest tests |
| `ARK-FR-004/005` | Entitled definitions and typed operations use immutable AuthContext and owner authorization | Scope/schema/IDOR/body-tenant/credential tests |
| `ARK-FR-006` | Data readiness, platform authority, scientific eligibility, model assignment, and security admission remain independent | Denial/outcome matrix and missing-policy tests |
| `ARK-FR-007/008` | Workload identity plus fenced delegated context; no background authority from process identity alone | Forged/stale/cross-tenant job and worker tests |
| `ARK-FR-009` | Separate lifecycle permissions and exact approved model assignment/digest | Unauthorized train/promote/assign/load/rollback tests |
| `ARK-FR-010` | Consent/purpose plus Stage 09 deterministic two-phase/at-effect authority; verifier remains advisory | Grant/revocation/audit/LLM bypass and race tests |
| `ARK-FR-011` | Authorized producers/consumers, minimal events, registered destinations, webhook SSRF/signature/replay gate | Cross-tenant route, arbitrary URL, replay and dedupe tests |
| `ARK-FR-012` | LAB evidence package is scoped, minimized, immutable, purpose-bound, and audited | Unauthorized export and evidence-integrity tests |
| `ARK-NFR-001` | Normative tenant-bearing asset matrix with four required controls | Exhaustive cross-tenant negative suite across all matrix rows |
| `ARK-NFR-002/003` | Security/policy/trust/model/supply-chain versions join existing lineage identities | Reproduction and incompatible-policy/version tests |
| `ARK-NFR-004` | Identity/authorization preserved across retry/replay; idempotency/fencing cannot be bypassed | Duplicate, stale-fence, replay, ambiguous-effect security tests |
| `ARK-NFR-005` | Opaque IDs, classification/minimization, telemetry redaction, controlled provider/export/deletion | PII/secret/path/log/trace/provider scans and subject-request tests |
| `ARK-NFR-006` | Immutable security audit correlated with request/job/result/event/delivery/model evidence | Audit completeness, tamper, access and unavailable-audit tests |
| `ARK-NFR-007` | Security production blocks expose missing numeric/environment/policy evidence | Admission-register and Stage 15/17 evidence review |
| `ARK-CON-001/002` | Same-codebase roles retain public owner checks, schema roles, one writer and workload least privilege | Dependency/DB-role/object-policy tests |
| `ARK-CON-003` | Consumer trust/translation stays outside capability cores; no legacy trust inheritance | Adapter and body-tenant negative tests |
| `ARK-CON-004/005` | Scoped object refs and PostgreSQL state enforce tenant/purpose; job context fenced | Reference traversal and durable authorization tests |
| `ARK-CON-006` | Upstream identity remains data, not tenant authority; no probabilistic identity privilege | Source/identity spoofing tests |
| `ARK-CON-007` | No unsupported security platform, agent runtime, provider, compliance, key topology, or product | Anti-overengineering and decision-evidence review |
| `SC-02-06/08/09/10/12` | Isolation, no-action authority, owner boundaries, LAB evidence, and production target blocks are concrete | Stage 12 negative suites plus Stages 13–17 evidence |

`quality/source-instruction-coverage.md` may mark source prompt section 11 `Covered` only after the assurance review and gate pass. Coverage does not clear any production-admission block.

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Every governing security/privacy/governance bullet addressed | PASS | Source-instruction coverage |
| Authenticated principal is authoritative tenant source | PASS | Security invariants and R-12-01 |
| Every required tenant-bearing asset has identity, authorization, isolation, and audit | PASS | Tenant-bearing asset control matrix; final assurance pass |
| IAM and service identity implementable without invented provider | PASS | Trust-profile/AuthContext and delegated workload contract |
| Least privilege and privilege separation explicit | PASS WITH ACTIVATION INPUTS OPEN | Owner-module authorization and governance separation; role bindings remain blocked |
| Secrets and encryption controls explicit | PASS WITH ENVIRONMENT INPUTS OPEN | R-12-02 and `SEC-ADM-03` |
| PII, residency, consent, retention/deletion and legal hold addressed | PASS WITH POLICY INPUTS OPEN | R-12-03 and `SEC-ADM-02` |
| Audit behavior and fail-closed sensitive effects explicit | PASS | R-12-04 and asset matrix |
| Model access and LLM/provider/prompt security explicit | PASS; PRODUCTION BLOCKED | Model/LLM section, ADR-007, `SEC-ADM-06` |
| Agent tool security correctly conditional | PASS | No active agent; Stage 11 re-entry controls retained |
| Abuse and supply-chain controls explicit | PASS WITH ACTIVATION INPUTS OPEN | R-12-05/06 and `SEC-ADM-07` |
| Threat model concise and realistic | PASS | Threat-model table; final assurance pass |
| Missing policies become explicit blocks rather than invented assumptions | PASS | Production security-admission register |
| Accepted boundaries preserved; no Stage 13 design or product selection | PASS | Decisions and anti-overengineering findings |
| Authorized assurance review reconciled | PASS | Initial cache contradiction reconciled; final review reported no critical or high defects |
| Proposed ADR recorded | PASS | `decisions/ADR-008-zero-trust-tenant-and-governance-boundary.md` |

**Gate result: PASSED AND APPROVED.** Every governing concern is dispositioned, every required tenant-bearing asset has an authoritative identity source, authorization rule, isolation mechanism, and audit behavior, and the concise threat model covers the realistic trust boundaries. The authorized final assurance review reported no critical or high defects after the cache contradiction was explicitly reconciled. The logical design remains intentionally fail-closed: all missing trust, governance, cryptographic, privileged-action, delivery, LLM-provider, supply-chain, and model-cache evidence appears in explicit production-admission blocks. The sponsor explicitly approved Stage 12 and accepted ADR-008 on 2026-08-12, authorizing Stage 13 only.

## Downstream consequences

- Stage 13 must define failure/recovery behavior for identity dependencies, audit, secret/key access, policy stores, PostgreSQL/object controls, provider calls, and webhook security without weakening fail-closed authority.
- Stage 14 must instrument authentication/authorization denials, privileged actions, cross-tenant attempts, provider/egress decisions, deletion progress, artifact/provenance checks, and security-admission status while keeping telemetry non-authoritative and privacy-safe.
- Stage 15 must select physical identity, network, secret/key, database/object, backup, egress, telemetry, region, and build placement only after the relevant Stage 12 policy inputs are authoritative.
- Stage 16 must implement exhaustive security tests for every asset-matrix row, trust profile, owner authorization, delegation/fence, webhook/provider boundary, deletion flow, artifact provenance, and privileged-action race.
- Stage 17 must supply measured abuse/rate/quota/concurrency/storage/provider-cost limits before production activation.
- Stage 18 must index ADR-008 and all inherited security constraints without claiming that blocked profiles are accepted production controls.
- Stage 20 cannot admit production work until named security/governance/operations owners and every release-applicable `SEC-ADM-*` exit gate are satisfied.
- Stage 22 must carry trusted identity and tenant/purpose context through every runtime flow and show where authorization/audit/effect rechecks occur.

## Exact next-stage inputs

Stage 12 and ADR-008 are approved and Stage 13 is authorized. Stage 13 must read:

1. Approved `outputs/stages/01-discovery-and-questions.md` through `outputs/stages/12-security-governance.md`
2. Accepted `decisions/ADR-000-temporary-source-evidence-disposition.md` through `decisions/ADR-007-versioned-ml-lifecycle-and-production-admission.md`
3. Proposed/accepted `decisions/ADR-008-zero-trust-tenant-and-governance-boundary.md`, according to sponsor disposition
4. `sources/normalized/system-design-prompt.md` section **12. Reliability and failure design**
5. `sources/normalized/ark-assumptions.md`
6. `stages/13-reliability.md`, `templates/stage-output.md`, and directly referenced failure templates

Execute Stage 13 only. Do not execute Stage 14 until Stage 13 passes its gate and the sponsor explicitly authorizes continuation.
