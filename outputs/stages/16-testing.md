# Stage 16 — Testing strategy

**Status:** APPROVED  
**Completed:** 2026-08-13  
**Stage owner:** Primary architecture agent  
**Authorized specialist:** `assurance_reviewer` (read-only high-risk coverage challenge)

## Purpose and scope

Define an executable, ownership-aware testing strategy for every approved ARK requirement, critical contract, critical path, production-admission block, and provisional deployment boundary. The strategy covers unit, contract, integration, end-to-end, data-quality, model-evaluation, event-delivery, load, resilience, security, tenant-isolation, migration/release, restore/reconciliation, and LAB-facing evidence.

The provisional implementation target is Python, PostgreSQL, and one Linux server operated by the sponsor with AI assistance and no assumed 24/7 team. Containers remain optional. Tests therefore prove correctness and expose operating limits; they do not claim high availability, capacity, RPO/RTO, SLOs, security compliance, or production readiness without the missing evidence. Stage 17 is not executed.

## Inputs read in full

- `WORKFLOW.md`
- `STATUS.md`
- `SOURCE_MANIFEST.md`
- `stages/STAGE-CONTRACT.md`
- `stages/16-testing.md`
- `templates/stage-output.md`
- `templates/requirements-traceability.md`
- `sources/normalized/system-design-prompt.md` — **15. Testing strategy**
- Approved `outputs/stages/02-system-definition.md` through `outputs/stages/15-deployment-infrastructure.md`
- Accepted `decisions/ADR-000-temporary-source-evidence-disposition.md` through `decisions/ADR-009-provisional-python-postgresql-linux-target.md`
- All seven service cards selected by `SOURCE_MANIFEST.md`, including their input, output, failure, observability, and current-gap evidence
- `quality/source-instruction-coverage.md`

## Specialist reconciliation

The Stage 16-authorized `assurance_reviewer` performed a bounded read-only challenge of high-risk coverage, contract/risk traceability, environments, fixtures, owners, pass criteria, release consequences, capability blocks, security blocks, critical paths, deployment constraints, LAB boundaries, and agent-evaluation applicability. The review required explicit per-asset tenant-isolation coverage, separate current-negative and future-exit suites for every admission block, conditional-versus-runnable event tests, the absence of agent runtime/authority, and an explicit warning that a one-server test run cannot establish production fitness. The primary agent incorporated those findings below and remains the sole authoritative writer.

## Source-instruction coverage

| Governing requirement | Addressed in | Status/evidence |
|---|---|---|
| Unit tests | Test-level contract; ownership matrix | Covered |
| Contract tests | Contract/risk matrix and interface compatibility suite | Covered |
| Integration tests | PostgreSQL/object/identity/secrets/telemetry/adapters matrix | Covered |
| End-to-end tests | CP-13-01 through CP-13-08 matrix | Covered |
| Data-quality tests | Four-layer data matrix and capability suites | Covered |
| Model-evaluation tests | Seven-capability admission matrix | Covered; blocked profiles preserved |
| Event-delivery tests | Conditional publication/delivery suite | Covered without activation |
| Load tests | Measurement plan for Stage 17; no invented targets | Covered |
| Resilience tests | Stage 13 path matrix and deployment/recovery suite | Covered |
| Security tests | ADR-008 block matrix | Covered |
| Tenant-isolation tests | Cross-asset negative matrix | Covered |
| Agent evaluations if applicable | Not applicable now; future re-entry suite defined | Covered as N/A |
| Highest-risk pre-production scenarios | Production-blocking invariant register | Covered |

## Confirmed facts

1. ARK has 26 stable Stage 02 requirements and 12 success criteria whose acceptance evidence already names contracts, isolation, lineage, jobs, failures, evaluation, and operating targets. `outputs/stages/02-system-definition.md — Requirements`; `— Success criteria`.
2. The architecture contains 22 logical Stage 05 components, three foundational flows, eight Stage 13 current/conditional critical paths, and product-neutral Stage 14 signal contracts. Approved Stages 05, 13, and 14.
3. The job system assumes at-least-once attempts with idempotent/fenced effects; external ambiguity must be reconciled. Accepted ADR-005 and approved Stage 13.
4. Data acceptance has structural, semantic, readiness, and capability-eligibility layers. Immutable raw/candidates and atomic owner publication are distinct. Approved Stage 06.
5. Model training, evaluation, promotion, deployment assignment, inference, rollback, and reproduction are separate authorized operations with exact identities. Accepted ADR-007.
6. Four profiles remain `MIGRATION_BLOCKED`; three Synapse profiles remain `EVIDENCE_BLOCKED`; eight ADR-008 security-admission blocks and `DEPLOYMENT_ENVIRONMENT_BLOCKED` remain active. Tests provide evidence but do not clear a block without its accountable decision.
7. No agent is justified or selected. Approved Stage 11.
8. The provisional implementation target is Python/PostgreSQL on one Linux server with optional containers, operated by one human sponsor with AI assistance and no assumed 24/7 support. Accepted ADR-009.
9. Numeric quality, performance, capacity, SLO, RPO/RTO, alert, retention, and cost targets are not approved. Tests measure distributions and invariant correctness; target-based pass criteria remain blocked until their versioned policies exist.

## Assumptions and constraints

| ID | Classification | Testing effect | Expiry/evidence |
|---|---|---|---|
| `A-01-SCALE` | Retained temporary assumption | Load/soak tests characterize curves and failure points; no production threshold invented | Stage 17 target evidence |
| `A-04-OWNERSHIP` | Accepted temporary assumption | Logical test owners are named; sponsor is human release authority, but capability/security specialist assignments remain required for production | Stage 20/production |
| `DEPLOYMENT_ENVIRONMENT_BLOCKED` | Accepted Stage 15 disposition | Linux integration baseline can be tested; provider/network/TLS/secrets/backup/telemetry production implementation cannot pass yet | Concrete environment/runbooks |
| `A-07-INTEGRATION` | Retained integration disposition | Polling tests are required; webhook/event tests remain contract/fault suites without production activation | Consumer/delivery admission |

AI may generate code, fixtures, cases, mutations, analyses, and reports. AI output is untrusted until reviewed and reproduced by the test pipeline. AI cannot approve its own code, change expected results, waive a failing gate, hold production credentials, or serve as the sole release/security/scientific authority.

## Testing principles

1. **Test owner truth, not mocks alone.** PostgreSQL owner state, immutable object references, audit, lineage, usage, evaluation reports, and assignments decide pass/fail for integration and E2E suites.
2. **Negative paths are first-class.** Denied, invalid, not-ready, ineligible, unavailable, cancelled, degraded, partial, suppressed, ambiguous, dead-lettered, and failed are distinct expected results.
3. **Every retry test asserts one logical effect.** Attempts may multiply; results, reservations, assignments, tasks, notifications, and charges do not.
4. **Every security test proves both denial and non-effect.** A rejected request must not leave unauthorized rows, objects, jobs, cache entries, audit omissions, provider calls, or external effects.
5. **Version compatibility is executable.** Current and supported previous contracts/handlers/schemas coexist only through declared ranges and immutable fixtures.
6. **Determinism is bounded honestly.** Exact reproduction is required where promised; approved tolerances and provenance are required where platform/library/provider nondeterminism exists.
7. **Blocked means blocked.** A test may prove a re-entry condition, but only the recorded owner/approval transition changes admission state.
8. **No production data in ordinary tests.** Use synthetic or governed de-identified data; sensitive evidence remains protected and purpose-bound.
9. **Failures are injected at authority boundaries.** Crash/timeout tests cover before, during, and after candidate, owner, audit, usage, delivery, and response commits.
10. **A green test suite is necessary, not sufficient.** Missing target, owner, policy, environment, or external evidence remains a production blocker.

## Test levels and execution lanes

| Level/lane | Purpose | Typical scope | Environment | Default owner | Release consequence |
|---|---|---|---|---|---|
| Unit/property | Pure logic, invariants, parsers, policy functions, state transitions, transforms | One module/function; deterministic dependencies | Local/CI | Owning module/capability | Failure blocks merge |
| Module/component | Public port with owned persistence adapter; state/reason behavior | One logical module plus ephemeral PostgreSQL/object fixture | CI | Module owner | Failure blocks merge/candidate |
| Contract/schema | Request/response/error, job, event, dataset, model, config and evidence schemas; compatibility | Producer/consumer fixtures and generated cases | CI/shared validation | Contract owner + consumers | Breaking/unsupported change blocks release |
| Integration | Real PostgreSQL semantics, object adapter, transactions, locks, migrations, identity/secrets/telemetry adapters | Multiple owned adapters without full system | CI/shared Linux validation | Platform/data/security owners | Failure blocks release candidate |
| End-to-end | Consumer/source through owner result/evidence and polling/delivery | Deployed coordinated candidate roles | Shared isolated Linux validation | Platform + participating owners | Failure blocks release |
| Data-quality | Four-layer validation, lineage, corrections, freshness/readiness | Synthetic/golden datasets and mutation generators | CI/shared validation | Data/source/capability owner | Failure blocks dataset/profile release |
| Model/evaluation | PIT/leakage, training/reproduction, quality/safety, assignment/load | Immutable datasets/artifacts/reports | Isolated evaluation/LAB lane | Capability scientific + release owner | Failure keeps capability blocked/no promotion |
| Security/isolation | Authn/z, tenant/assets, secrets, egress, audit, supply chain, abuse | All assets/trust boundaries | CI plus isolated security lane | Security + affected owner | Any invariant failure blocks release; incident if production-like data involved |
| Resilience/recovery | Crash, timeout, dependency loss, retry, poison, restore/reconcile, disk/resource failure | Deployed roles and real owner stores | Disposable isolated Linux/recovery lane | Platform/data/operations | Failure blocks production/recovery approval |
| Load/soak | Curves, saturation, backlog/fairness, leaks, resource/cost evidence | Representative operation mixes | Isolated performance lane | Platform + capability/data | Results inform Stage 17; invariant breach blocks release; missing numeric targets prevent capacity approval |
| Release acceptance | Provenance, migrations, config, smoke, evidence manifest, rollback readiness | Exact candidate digest and environment revision | Shared validation/pre-production | Sponsor/release authority | Failure blocks deployment |

Coverage percentage alone is not a gate. Risk/contract/scenario coverage, mutation/property evidence where useful, deterministic failure reproduction, and absence of untested production-critical paths are the criteria.

## Test ownership matrix

| Owner | Owns test evidence for | Does not own/approve |
|---|---|---|
| Shared platform | Envelope, jobs, scheduler, state machines, correlation, usage, API/public errors, deployment roles | Capability scientific truth or external consumer mappings |
| Data platform/source owner | Source contracts, raw/validation/canonical/readiness/lineage, corrections, storage reconciliation | Capability model thresholds |
| Capability owner | Scientific eligibility, private transforms/features, result schema, fallbacks, model/recommendation evaluation, reproduction | Grants, cross-capability writes, production security approval |
| Security/governance | Trust, authorization, isolation, secrets/egress, audit, privacy, retention/deletion and supply-chain negative evidence | Scientific promotion alone |
| Integration/adapter owner | Consumer mapping, webhook endpoint/receiver behavior, dedupe/ack/replay | Capability core schema ownership |
| Operations/release | Build/deploy/migrate/backup/restore/rollback/runbook and environment evidence | Waiving security/scientific failures |
| Sponsor | Approves requirements, unresolved target/policy decisions, release disposition under named authority | Treating AI-generated assertion as evidence |
| AI assistant | Generates/reviews proposed tests, fixtures, fault cases and reports under human scope | Production credentials, unilateral approval, expected-result mutation, incident accountability |
| LAB | Consumes release-scoped contract/isolation/reproduction/evaluation/failure evidence under future operating contract | Automatic promotion/veto until authority is explicitly approved |

## Contract and critical-risk verification matrix

Every row names at least one level, owner, environment, pass criterion, and release consequence.

| Risk/contract | Test level(s) | Logical owner | Environment/fixtures | Pass criterion | Release consequence |
|---|---|---|---|---|---|
| Public envelope, definitions, errors and versioning | Unit/property, contract, E2E | Platform contract + capability owners | Generated valid/invalid schemas; current/supported/unknown versions | Machine-readable bounded contracts; no consumer terminology; exact outcome/error classes; incompatible versions rejected | Blocks merge/release; affected capability unavailable |
| Authenticated tenant and resource authorization | Unit, integration, security, E2E | Security/control + resource owner | Tenant A/B/C, forged body/header/path IDs, stale/revoked credentials | Tenant derives only from trusted principal; unauthorized read/write/effect absent and concealment policy correct | Blocks all production release; security incident |
| Subscription/entitlement/quota/grant/config separation | Unit/property, integration, E2E | Control owner | State-transition/race fixtures and CAS conflicts | Enablement creates no ingestion/execution; exact decision/reason/version; one reservation/effect | Blocks control/proactive release |
| Push/bulk ingestion and raw-first publication | Contract, integration, E2E, data-quality | Data/source owner | Valid, truncated, duplicate, malformed, incompatible, late/corrected files/records | Raw preserved once; invalid quarantined; no ready version before full owner evidence; exact lineage | Blocks ingestion/data release |
| Four-layer validity/readiness/eligibility | Unit, data-quality, E2E | Data + capability owner | Independently failing structural, semantic, readiness and scientific cases | Each layer produces its exact reason and no later-layer/fabricated result | Blocks affected dataset/capability |
| Object/reference integrity and atomic publication | Integration, resilience, recovery | Data/storage/result owner | Crash at multipart/candidate/catalog/result points; checksum corruption | Candidate unreferenced until owner commit; missing/orphan classified; no false readiness/success | Blocks storage/data/capability release |
| Durable job lifecycle | Unit/property, integration, E2E, resilience | Job platform | Every state/attempt transition, restart, lease expiry, duplicate, cancel/finalize race | Only legal CAS transitions; public state truthful; stale fence rejected; one logical result | Blocks async operations/platform release |
| Scheduler occurrences and misfire | Unit/property, integration, resilience | Scheduler/control | Time-controlled due/missed/duplicate/expired, `SKIP/RUN_ONCE/RUN_EACH` policies | One logical occurrence/job; expired work does not execute late; grant rechecked | Blocks scheduled/proactive release |
| Synchronous classification and timeout | Contract, E2E, resilience | Platform + capability | Short/long operations; timeout before/during/after commit; lost response | No silent background conversion; same-key reconciliation; one result/effect | Blocks synchronous operation |
| Idempotency and ambiguous effects | Property, integration, resilience | Platform/effect owner | Concurrent same/different hash; webhook/provider timeout after send; response loss | Same key/hash replays; conflict on changed hash; ambiguity reconciled before repeat | Blocks effecting path |
| Partial/degraded/fallback semantics | Unit, contract, E2E | Capability owner | Partition/source/model loss under each operation policy | Default failure; only approved public `SUCCEEDED` + domain `DEGRADED` manifest; never ordinary full success | Blocks affected operation |
| Model lifecycle and no implicit training | Unit, integration, E2E, model evaluation | Capability + registry/release | Missing/invalid artifact; inference with no model; unauthorized training/promotion | Inference never trains/promotes; exact approved assignment only; blocks preserved | Keeps profile blocked/no deployment |
| Reproduction and exact lineage | Integration, evaluation, E2E | Capability + data/registry | Original manifests; missing/corrupt refs; reconstructed environment/PIT snapshot | Complete immutable report; exact or approved tolerance; every output resolves required versions | Blocks promotion/release evidence |
| Proactive Phase A/Phase B/at-effect order | Unit/property, integration, E2E, security, resilience | Control + capability + effect owner | Revocation/staleness/quota/audit races at every boundary | No job before Phase A; no intent before Phase B; no effect after failed recheck; one reservation/effect | Blocks proactive path; remains inactive |
| Event/outbox/delivery contract | Contract, integration, E2E, resilience | Producer/integration/consumer | Duplicate, out-of-order, poison/schema mismatch, crash gap, endpoint 429/5xx/timeout, lost ack | Source truth unchanged; at-least-once transport, deduped logical effect, dead-letter/replay preserves identity | Blocks conditional activation |
| Privileged admin/replay/recovery/deletion | Security, integration, recovery | Security/governance + target owner | Missing step-up/audit; stale/broad/cross-tenant commands; partial deletion/restore | Denied without exact authority; manifests truthful; no resurrected deleted data or blind replay | Blocks production/admin role |
| Mandatory audit/lineage/usage versus telemetry | Integration, E2E, resilience | Audit/usage/observability owners | Each writer/exporter independently unavailable; duplicate usage | Mandatory evidence failure blocks/holds effect; diagnostic loss degrades only; one usage effect | Blocks protected path or release |
| Deployment artifact/config/migration compatibility | Contract, integration, release, resilience | Release/platform/module owners | Previous/current Python artifact, DB schema, config, handler, optional container/process modes | Same digest/config identities; expand/contract compatibility; no secret; rollback/forward-fix safe | Blocks candidate deployment |
| Backup/restore/recovery epoch | Recovery/E2E/security | Operations/data/security | Isolated PostgreSQL/object backups, mismatched recovery points, old worker/process | Trusted restore order; old fences invalid; missing/orphan/ambiguous effects reconciled; tenant isolation intact | Blocks production recovery approval |
| Observability/health/redaction | Unit, contract, integration, resilience | Operations + module/security owners | Missing exporter/context; cardinality burst; PII/secret canaries; clock skew | Safe fields/correlation complete; no authority from telemetry; bounded outage; unsafe export stopped | Blocks release for redaction/authority gaps; other gaps per policy |
| Linux single-server operating baseline | Integration, resilience, release | Sponsor/operations | Process and optional-container modes; reboot; disk/memory/process/DB failure; patch/redeploy | Roles restart safely; durable truth survives; limits measured; runbook reproducible by sponsor | Failure blocks production use; does not imply HA |
| Architecture boundaries/no forbidden infrastructure | Static, contract, release | Architecture/module owners | Dependency graph, imports, schemas, manifests/IaC | No private cross-module imports/writes, hidden scheduler, unapproved broker/Kubernetes/Rust/provider | Blocks merge/release; material change requires decision |

## Stage 13 critical-path test matrix

| Path | Test levels | Owner | Environment | Minimum pass criterion | Release consequence |
|---|---|---|---|---|---|
| `CP-13-01` synchronous request | Contract, integration, E2E, resilience, security | API/control/capability/audit | Shared isolated Linux candidate | Every failure boundary returns truthful outcome; lost response reconciles; no duplicate or unaudited result | Blocks sync operation/release |
| `CP-13-02` durable execution | Property, integration, E2E, load, resilience | Job/scheduler/worker/capability | Ephemeral DB CI + deployed Linux candidate | All states/races/crashes/duplicates/cancels/finalization obey fence and one-effect rules | Blocks async platform |
| `CP-13-03` ingestion/publication | Contract, data-quality, integration, E2E, resilience | Source/data/catalog/storage | Synthetic golden/mutated datasets | Raw-first, quarantine, exact correction/version, atomic readiness and orphan recovery | Blocks data onboarding |
| `CP-13-04` ML lifecycle | Data/model evaluation, integration, E2E, resilience, security | Capability/data/registry/release | Isolated evaluation/LAB lane | PIT/leakage/quality/reproduction/integrity/assignment/load gates all pass; exact blocked state transition authorized | Keeps capability blocked/no promotion |
| `CP-13-05` proactive action | Property, integration, E2E, resilience, security | Scheduler/control/capability/effect | Time-controlled isolated lane | Exact Phase A/B/effect order; every revocation/race produces no unauthorized action | Path remains inactive on failure |
| `CP-13-06` delivery | Contract, integration, E2E, resilience, security | Producer/integration/consumer | Receiver emulator; no real egress | Crash-safe intent, dedupe, ambiguity, dead-letter/replay, SSRF/destination controls pass | Delivery remains blocked |
| `CP-13-07` privileged/recovery | Security, integration, recovery | Security/governance/operations | Isolated clone/recovery lane | Strong auth/separation/audit; exact scope; truthful deletion/restore; no cross-tenant mutation | Blocks admin/production |
| `CP-13-08` named workflow | Property, contract, integration, resilience | Workflow/job/child owners | Inactive contract harness | Deterministic graph, one child/node, restart, partial/residual/compensation truth | Workflow remains unactivated until named contract passes |

## Data-quality test matrix

| Layer | Fixture/mutation families | Pass criterion | Owner/environment | Consequence |
|---|---|---|---|---|
| Structural | Unknown schema, malformed encoding/compression, missing/extra fields, type/bounds/cardinality, truncated/checksum mismatch | Exact reject/quarantine reason; raw evidence protected; no canonical/ready state | Source/data; CI/shared validation | Blocks source contract |
| Semantic | Currency/unit/time-zone, referential/catalog/inventory, consent/purpose, duplicates/conflicts, correction/order/cursor gaps | No ambiguous truth accepted; explicit semantic/reconciliation result | Domain/data governance | Blocks dataset version |
| Readiness | Missing partition/object/lineage/policy/quality, stale/revoked/tombstoned, candidate without catalog | No `READY`; previous version only if current policy explicitly permits | Catalog/data; integration/E2E | Blocks use/publication |
| Scientific eligibility | Insufficient history/population/features/catalog/model/config, incompatible versions | Explicit ineligible/unavailable; no fabricated score/rank/segment | Capability; CI/evaluation | Blocks capability execution |
| Corrections/reprocessing | Duplicate, late, tombstone, backfill interruption, mixed versions | New immutable version/impact manifest; deterministic resume; no overwrite/mixing | Data/capability; resilience | Blocks publication/reprocessing |

## Capability production-admission test matrix

Passing these suites is necessary but never silently changes the recorded profile state.

| Capability/current state | Required test families | Pass criteria before re-entry decision | Owner/environment | Failure consequence |
|---|---|---|---|---|
| Churn — `MIGRATION_BLOCKED` | Intended schema/outcome; PIT labels/features; forced-score removal/policy; temporal evaluation/calibration; artifact/load/persist; retry/idempotency; tenant/debug isolation; reproduction | Exact approved semantics and thresholds; no inference training; no forced/fabricated score; full lineage and deterministic/toleranced replay | Churn scientific + data/release; isolated evaluation/LAB | Remains blocked |
| RFM — `MIGRATION_BLOCKED` | R/F/M definitions/direction/currency/window; deterministic/non-model or trained lifecycle; cluster stability; semantic mapping/version; weights; population/fallback; persistence/tenant | Stable approved labels/algorithm profile; no per-run ungoverned remapping/refit; evaluation and reproduction pass | RFM scientific/data/release | Remains blocked |
| NPT — `MIGRATION_BLOCKED` | Calendar/horizon/label/censoring; PIT snapshots; CLF/RSF/routing bundle; schema signature; temporal evaluation/calibration; served/output contract; load/persist/retry | No leakage or `_x/_y` defects; exact compatible bundle; approved event floors/thresholds are policy, not prototype constants; truthful result | NPT scientific/data/release | Remains blocked |
| REC — `MIGRATION_BLOCKED` | Transaction/catalog/inventory/availability; candidate/ranker/fallback; unavailable item and empty output; temporal ranking/baseline/ablation; feedback idempotency/attribution; tenant/debug | Exact top-k/constraint semantics; no unavailable item; partial/empty truth; reproducible ranking under seed/tie policy; governed feedback | REC scientific/data/integration/release | Remains blocked |
| Synapse Chatbot — `EVIDENCE_BLOCKED` | Interface contract only now; future provider/model/prompt/context/privacy/safety/refusal/injection/cost/failure/reproduction/adversarial suites | Authoritative evidence and owners; bounded tenant/purpose data; output validation; no tools/actions; measured sync fit | Synapse owner/security/LAB; isolated provider stub then admitted sandbox | No provider call; remains blocked |
| Synapse Message Generator — `EVIDENCE_BLOCKED` | Interface now; future Persian quality, context/offer fidelity, length/channel, claims, safety/refusal/bias, prompt/provider/cost, no-delivery tests | Approved rubric/corpus and exact versions; generated text cannot authorize/send | Synapse/security/policy/LAB | Remains blocked |
| Synapse Campaign Verifier — `EVIDENCE_BLOCKED` | Interface now; future policy/reference completeness, false accept/reject, explanation, injection, safety, advisory-authority negatives | `accepted` never grants permission; deterministic policy remains authority; exact evidence/report | Synapse/policy/security/LAB | Remains blocked/no action |

## Security-admission and tenant-isolation matrix

| Block/area | Required tests | Assets/fixtures | Pass criterion | Owner/environment | Release consequence |
|---|---|---|---|---|---|
| `EXTERNAL_TRUST_BLOCKED` | Credential validation/revocation/rotation, issuer/audience/time/replay, workload mutual trust, body-tenant forgery | Human/workload/consumer identities, expired/stolen/malformed tokens | Only configured trust profiles accepted; tenant immutable; revocation timely under approved policy | Security; isolated trust integration | Block all external/production access |
| `DATA_GOVERNANCE_BLOCKED` | Classification, purpose/consent, residency/retention/deletion/legal hold, backups/model derivatives | Every data class; deletion manifests and restored backups | Unknown policy fails closed; complete truthful manifest; no resurrection/access | Governance/data/security recovery lane | Block production data onboarding |
| `CRYPTO_SECRETS_BLOCKED` | In-transit/at-rest config evidence, secret reference/access/rotation/revocation, no plaintext/log/image | Secret canaries, role identities, backups/artifacts | Least privilege; values never leak; dependent role fails closed and recovers | Security/platform | Block production deployment |
| `PRIVILEGED_ACTION_BLOCKED` | Strong auth, role combinations/separation, approval, audit, race/replay, break-glass | Promotion/grant/deletion/export/recovery commands | Unauthorized/unaudited/stale action has zero effect; required approvals immutable | Security/governance/release | Block privileged operations/production |
| `EXTERNAL_DELIVERY_BLOCKED` | Endpoint ownership/SSRF/DNS/rebinding, signature/secret/replay, rate/retry/dedupe/egress | Local receiver emulator and malicious endpoints | Only registered approved destination; one logical event; no secret/body leak | Integration/security isolated lane | Delivery remains disabled |
| `LLM_PROVIDER_BLOCKED` | Provider identity/terms/config/egress, input minimization, injection/exfiltration, output safety/schema, retention/cost | Adversarial synthetic prompts/context; provider stub | No real call until admission; future sandbox meets all exact controls | Security/Synapse/LAB | Synapse remains disabled |
| `SUPPLY_CHAIN_BLOCKED` | Locked Python dependencies, provenance/SBOM/signature, secret scan, vulnerability/license policy, build isolation/reproducibility | Source/build/image/artifact/model manifests | Candidate digest reproducible/verified; prohibited issue/secret absent; promotion by digest | Release/security CI | Block artifact promotion |
| `MODEL_CACHE_BLOCKED` | Tenant/capability/purpose/assignment/digest key isolation, shared-byte classification, revocation/eviction, collision/concurrency | Tenant A/B assignments and identical/different artifacts | No unauthorized selection/read; revoked/stale entry unusable; bytes never become authority | Capability/security integration | Cached model loading disabled |
| Cross-asset tenant isolation | Matrix across rows, objects, datasets, models, jobs, events, caches, quotas, audit, telemetry, usage, endpoints, backups | At least two tenants with colliding resource/idempotency names | Tenant A cannot observe/influence B through direct, inferred, timing/listing, retry, restore, or admin paths | Security + all owners | Any failure blocks production and triggers incident |
| `DEPLOYMENT_ENVIRONMENT_BLOCKED` | Linux role identity, process/container parity, firewall/egress, TLS/DNS, patching, backups, disk/resource, telemetry, runbook | Exact selected server/environment when supplied | All concrete controls and sponsor-run recovery/deploy procedure pass | Sponsor/operations/security | No production deployment until passed |

### Tenant-bearing asset isolation coverage

Every row below runs with at least tenants A and B, colliding public/resource/idempotency identifiers, valid and forged principals, workload identity plus delegated context, concurrency, listing/inference probes, and restore/replay variants. Passing one row never substitutes for another.

| Asset class | Required adversarial assertions | Owner/environment | Pass criterion and consequence |
|---|---|---|---|
| PostgreSQL business and control rows | Forged body/header/path tenant; IDOR; owner-module access; in-process and job paths; database roles/RLS defense; bulk/list/count inference | Security + row/control owner; real PostgreSQL isolation lane | Principal-derived scope only; zero cross-tenant read/write/inference; any failure blocks production |
| Raw, canonical, curated and feature objects/datasets | Prefix/reference traversal; signed-reference scope; catalog indirection; correction/backfill; orphan discovery; deletion/restore | Data/storage/security; object-compatible recovery lane | No cross-tenant reference, byte access, publication or resurrection; blocks data onboarding |
| Capability state, results and debug artifacts | Foreign customer/result/job correlation IDs; debug/explanation fields; partial/fallback outputs | Capability/security; integration/E2E | Only exact tenant-owned eligibility and result visible; blocks affected capability |
| Model registry, assignments, bundles and caches | Cross-tenant assignment/digest collision; capability/purpose mismatch; revoked/stale cache; shared-byte deduplication | Registry/capability/security; model integration lane | Bytes never grant authority; exact tenant/capability/purpose/assignment required; keeps model loading blocked |
| Jobs, attempts, schedules and checkpoints | Forged tenant submit/status/cancel; worker delegated scope; occurrence/key collision; lease/fence theft; replay | Job/scheduler/security; concurrency/resilience lane | One tenant cannot enqueue, observe, claim, cancel or resume another tenant's work; blocks async runtime |
| Events, outbox, notifications and delivery state | Topic/filter/destination confusion; handler/delivery dedupe collisions; wrong-tenant replay/dead letter | Producer/integration/security; receiver emulator | No cross-tenant publication, subscription, destination or effect; delivery remains blocked |
| Grants, quotas, reservations and policy/config | Cross-tenant grant/config/version lookup; reservation races; administrative scope | Control/security; state-machine and integration lane | Exact scoped authority and accounting only; blocks control/proactive operation |
| Secrets and external endpoint registrations | Secret-reference enumeration; workload access; endpoint ownership; rotation/revocation; SSRF/redirect/DNS variants | Security/integration; isolated secret/egress lane | No value or endpoint use outside exact principal/purpose; keeps secrets/delivery blocks active |
| Audit, lineage, usage and cost evidence | Foreign query/export; missing tenant/correlation; duplicate attribution; privileged access | Evidence owners/security; integration lane | Complete immutable tenant attribution and authorized access only; blocks protected path/release |
| Logs, metrics, traces and health | Identifier/PII canaries; labels/cardinality; tenant dashboard/query access; exporter/buffer failure | Observability/security; telemetry fault lane | Redacted bounded signals; no cross-tenant access or inference; unsafe export stops and blocks release |
| Backups, restores, deletion and recovery manifests | Tenant-scoped restore; old backup after deletion/revocation; recovery epoch; stale writers; replay | Operations/data/governance/security; disposable recovery lane | No unauthorized resurrection or cross-tenant recovery; blocks production recovery approval |
| Exports and LAB evidence packages | Purpose/tenant/release scope; minimization; immutable digest; access expiry; audit; attempted onward use | Sponsor/security/evidence owner; isolated evidence-consumer lane | LAB sees only approved minimized package and gains no promotion authority; blocks LAB acceptance/export |

## Event-delivery test suite

Schema, producer-authority, no-publisher/no-egress, and unit/contract tests always run. Delivery integration, acknowledgement-loss, retry, dead-letter, and replay tests run only in an isolated receiver-emulator or later approved receiver lane; the production publisher remains absent while delivery is blocked. No broker is introduced by this strategy.

- producer fact and intent transaction crash points;
- duplicate publisher/handler/delivery attempts and stable `event_id`/`delivery_id` dedupe;
- ordering where declared, out-of-order handling where not guaranteed, handler-version compatibility;
- malformed/unsupported schema and deterministic poison isolation/dead-letter;
- endpoint timeout before/after receive, lost acknowledgement, 429/5xx, circuit and bounded retry;
- endpoint revocation/secret rotation/expiry during retry; SSRF, redirect, DNS rebinding and wrong-tenant endpoint attempts;
- authorized replay generation retains original fact/time/hash/version and does not recompute/re-authorize;
- polling remains authoritative and result/action truth is unchanged by delivery outcome.

Pass means one logical downstream effect where the receiver contract supports it, truthful ambiguity where it does not, no unauthorized egress, and complete audit/trace/evidence. Any failure keeps `EXTERNAL_DELIVERY_BLOCKED`.

## Load, performance, and resource-characterization plan

Stage 16 defines workloads and invariants; Stage 17 supplies measured targets and capacity/cost decisions.

| Workload family | Variables measured | Invariants under load | Environment/consequence |
|---|---|---|---|
| API/control/polling | request mix, latency distribution, DB pool/query, errors, memory/CPU | Tenant/auth/outcome/idempotency truth; bounded payloads; no resource leak | Isolated Linux lane; invariant failure blocks release, curves feed Stage 17 |
| Job/scheduler | submissions, queue age/depth, claim/finalize, retries, tenant/pool fairness, DB contention | No lost/duplicate job/effect; deadlines/status truthful; backpressure | Same |
| Ingestion/backfill | object/row/entity sizes, validation stages, DB/object I/O, orphan cleanup | Raw-first, no partial readiness, bounded memory/disk, resumable work | Same; no production sizing claim |
| Training/evaluation/reproduction | dataset/artifact sizes, stage time, memory/CPU/disk, cost, concurrency impact | No implicit promotion; exact identities/evidence; interactive isolation | Profiles remain blocked; informs role split/Rust need |
| Batch inference/REC | customers/items/candidates/partitions, artifact load, result commit | Deterministic/approved tolerance, no unavailable item, partial truth, one result | Same |
| Telemetry/audit/usage | signal volume/cardinality/export lag, audit/ledger write load | Mandatory evidence complete; diagnostic backpressure bounded; no PII | Redaction/authority failure blocks release |

The first test on one Linux server establishes saturation/failure curves, not capacity approval. A Rust rewrite, additional server, Kubernetes, broker, or data-lake product is justified only if a measured bottleneck persists after simpler Python/PostgreSQL/query/batch/pool remedies and the operational burden is accepted.

Each load or resilience run consumes a versioned operation profile covering deadlines, attempts, leases/heartbeats, backlog/admission/fairness, partial/fallback behavior, retention, and recovery targets. If any required target is absent, the run may characterize behavior but cannot pass activation, capacity, or production admission.

## Resilience, migration, release, and recovery suite

- Kill/restart API, scheduler, each worker role, migration command, PostgreSQL connection, object adapter and telemetry exporter at every Stage 13 commit boundary.
- Simulate reboot and old process return; advance recovery epoch; prove stale leases/fences/effects fail.
- Exhaust disk, file descriptors, memory budget, DB connections and worker concurrency in isolated lanes; assert backpressure/truthful failure and no corruption.
- Apply migrations from clean and every supported prior schema; interrupt/retry; exercise mixed current/next handlers; verify expand/contract and forward-fix/rollback limits.
- Deploy previous/current immutable Python artifact in supervised-process and optional-container modes; compare contract/state behavior and secret/config isolation.
- Verify a locked, reproducible Python dependency/build manifest; one coordinated release identity across API, scheduler, worker and maintenance entry points; and proof that publisher and named-workflow roles are absent by default.
- Corrupt/remove object/model/config references and restore mismatched PostgreSQL/object recovery points; classify missing/orphan/ambiguous state and reconcile.
- Restore deletion/legal-hold cases and prove deleted data is not silently accessible or reintroduced.
- Exercise release plan, dry run, backup checkpoint, apply order, health/owner-state smoke tests, abort, layer-specific rollback, audit and closeout using sponsor-run documentation.

Production release remains blocked until the sponsor can reproduce required deploy/backup/restore/rollback/incident runbooks in the selected environment without relying on hidden AI memory or credentials.

## Test data and fixture strategy

| Fixture family | Required properties | Prohibited |
|---|---|---|
| Tenant/control | Multiple tenants, colliding IDs/keys, varied grants/quotas/config versions, revoked/stale states | Real credentials or one-tenant-only happy path |
| Transaction/customer | Synthetic event histories with time zones, currencies, refunds, duplicates, gaps, corrections, late/tombstone, insufficient and large cohorts | Raw production phone/history in repository/logs/prompts |
| Catalog/inventory | Sellable/unavailable, duplicate/family/category, sparse metadata, changing inventory/effective times | Assuming catalog completeness |
| Model/artifact | Tiny deterministic artifacts, corrupt/missing/incompatible/revoked bundles, exact/tolerance reproduction references | Production proprietary model unless governed |
| LLM | Local deterministic stubs and adversarial synthetic prompt/context/output corpus | Real provider calls while blocked; treating stub quality as provider evidence |
| Delivery | Local receiver emulator with dedupe/query/failure modes and malicious URL/DNS fixtures | Internet egress/arbitrary destination |
| Time/concurrency | Controllable clock, deterministic seeds, barriers/latches, transaction/crash hooks | Wall-clock sleeps as the only race proof |
| Backup/recovery | Disposable encrypted test backups, mismatched snapshots, deleted/legal-hold manifests | Production restore into shared test or uncontrolled copies |

Golden fixtures are versioned with schema, generator seed/code, expected owner state/evidence, and privacy classification. Property/mutation generators record a minimal reproducible failing case. Tests never relax expected results automatically because an implementation changed.

## Production-blocking invariant scenarios

Any failure below blocks the affected release—and most block all production—regardless of coverage percentage or performance:

1. Cross-tenant read, write, inference, cache, job, event, audit, usage, backup, telemetry, or external effect.
2. Caller/body/trace data broadens tenant, role, resource, destination, model, or provider authority.
3. Invalid/incomplete/stale/revoked data becomes `READY` or produces a fabricated successful result.
4. Duplicate/retried/stale attempts create more than one logical result, reservation, charge, task, notification, assignment, or external effect.
5. Long/retryable work depends on HTTP/process lifetime or bypasses the durable job lifecycle.
6. Inference trains, promotes, activates, selects `latest`, or uses an unapproved/blocked model/provider.
7. A capability output/verifier/telemetry signal authorizes proactive or privileged action.
8. Mandatory audit, lineage, usage, policy, secret, or identity failure is bypassed or backfilled after effect.
9. Public success precedes required owner result/evidence finalization or hides an unapproved partial/degraded outcome.
10. Migration/rollback/restore resurrects revoked/deleted authority/data, accepts an incompatible version, or lets pre-recovery workers act.
11. Secrets, direct identifiers, prompts/history, customer data, or unsafe object/endpoint paths leak into source, image, logs, telemetry, test artifacts, or AI context.
12. A production-admission block is cleared by test execution without the required evidence owner and explicit decision.
13. The one-server process/container release cannot be deployed, restarted, backed up, restored, patched, or diagnosed by the sponsor using durable runbooks.

## Agent evaluation disposition

Agent evaluations are **not applicable** because no agent is justified or selected. Current tests must prove:

- no agent runtime/framework/MCP/A2A/vector-memory dependency appears in build/deployment manifests;
- `agent` labels or LLM outputs do not create planning/tool/action authority;
- proactive and workflow behavior remains deterministic, bounded, typed, and governed.
- advisory LLM/verifier output has no entitlement, grant, policy, quota, promotion, deployment, notification, or external-effect authority.

All twelve items of the approved Stage 11 future-agent re-entry gate remain cumulative prerequisites. If Stage 11 re-entry later approves an agent, Stage 16 must be revised before production to cover goal/task success versus deterministic baseline; plan/step/time/token/tool/cost bounds; tool choice/arguments/results; permissions and human approvals; memory tenant/retention/deletion; injection/exfiltration; hallucination/unsafe action; cancellation/recovery/idempotency/fencing; full plan/tool/action trace; and red-team/adversarial suites. Long or retryable runs must use Stage 08 job/attempt/fence semantics, and every tool effect remains subordinate to Stage 09 authorization and at-effect rechecks. A future agent cannot inherit a passing “N/A.”

## Test automation and evidence manifest

Each candidate release emits an immutable test-evidence manifest containing release/source/build/config/migration/handler identities; test suite and fixture/generator versions; environment/IaC revision; database/object/model fixture digests; executed levels/scenarios; results and quarantined/flaky tests; coverage by requirement/risk/contract/block; performance distributions without invented targets; security/data classifications; reproduction links; exceptions/waivers with owner/expiry; and signer/approval evidence. LAB packages are minimized, tenant/purpose/release scoped, access-controlled, audited, retention-bound evidence projections; LAB remains a consumer and never becomes an implicit test owner or promotion authority.

Flaky tests are failures until isolated with owner, issue, risk classification, expiry, and compensating release block. Quarantine cannot hide a production-critical scenario. Retries distinguish infrastructure noise from deterministic product failure and retain every attempt.

## Release and block transition gates

| Gate | Required evidence | Decision authority | Failure/missing evidence |
|---|---|---|---|
| Merge | Unit/module/contract/static/security scans for changed risks | Code/module reviewer under repository policy | No merge |
| Coordinated candidate | Full integration, migration, boundary, tenant and supply-chain suite | Release owner/sponsor | No candidate promotion |
| Shared validation | E2E CP-01..08 applicable paths, resilience, telemetry/evidence, consumer/LAB contract | Sponsor + logical owners | No deployment approval |
| Capability re-entry | Profile-specific data/model/safety/reproduction suite and immutable evidence | Named scientific/release/security/operations authorities | Remains `MIGRATION_BLOCKED`/`EVIDENCE_BLOCKED` |
| Security block clearance | Exact ADR-008 evidence and negative/race/fault suite | Named security/governance authority + affected owner | Block remains |
| Delivery/workflow activation | Contract, authority, security, reliability, receiver/consumer and runbook suite | Integration/control/security owner + sponsor | Role/path remains undeployed |
| Production environment | Linux target controls, load targets, backup/restore, runbooks, identities/secrets/network/telemetry | Sponsor + named security/operations roles as required | `DEPLOYMENT_ENVIRONMENT_BLOCKED` remains |
| Production release | All applicable gates, zero unresolved critical/high defects, approved targets and acceptance manifest | Sponsor and required separated authorities | No production release |

No waiver may bypass tenant isolation, mandatory audit, unauthorized effect, data/model integrity, secret leakage, or an active production-admission block. Other waivers require owner, reason, scope, expiry, compensating control, and sponsor approval.

## Requirements-to-test traceability

| Requirement group | Primary suites | Owner | Pass/release effect |
|---|---|---|---|
| `ARK-FR-001` | Control separation, decision/race, usage/audit tests | Control/security | Failure blocks platform/proactive release |
| `ARK-FR-002/003` | Ingestion contracts, four-layer data, raw/publication/reprocessing E2E | Data/source | Failure blocks data onboarding |
| `ARK-FR-004/005/006` | Definition/envelope/version/outcome contracts and capability eligibility suites | Platform + capability | Failure blocks affected capability/API |
| `ARK-FR-007/008` | Job state/property/restart/duplicate/cancel/sync lifetime suites | Execution/platform | Failure blocks runtime |
| `ARK-FR-009` | Lifecycle/negative inference/promotion/assignment/reproduction suites | Capability/release | Profile remains blocked |
| `ARK-FR-010/011` | Phase A/B/effect, event/delivery/adapter/dedupe/replay suites | Control/integration | Path remains inactive |
| `ARK-FR-012` | LAB evidence manifest, contract/isolation/reproduction/failure E2E | Sponsor/platform/LAB | No release acceptance claim |
| `ARK-NFR-001/005` | Cross-asset isolation, PII/secret minimization, environment separation | Security/all owners | Any failure blocks production |
| `ARK-NFR-002/006` | Lineage/reproduction/correlation/audit/usage/cost completeness | Data/platform/capability | Failure blocks result/release evidence |
| `ARK-NFR-003` | Schema lint/bounds/neutrality/version compatibility | Contract owners | Breaking change blocks release |
| `ARK-NFR-004` | At-least-once, fence/idempotency, timeout/ambiguity/recovery | Platform/effect owners | Failure blocks effecting runtime |
| `ARK-NFR-007` | Load/soak/recovery measurements and target-register presence | Sponsor/platform/capability | Missing targets block production/capacity approval |
| `ARK-CON-001/002/003` | Dependency/import/schema/migration/adapter ownership checks | Architecture/module owners | Violation blocks merge/release |
| `ARK-CON-004/005/006` | Object-reference/PostgreSQL-job/source-authority/no-identity-merge suites | Data/platform | Violation blocks architecture release |
| `ARK-CON-007` | Build/IaC/dependency inventory rejects unapproved infrastructure/language/platform | Architecture/release | Material change requires evidence/decision |
| `SC-02-01..12` | Combined contract, E2E, isolation, lineage, proactive, LAB, evaluation and target suites above | Sponsor + logical owners | Each unmet criterion remains visible and blocks its claimed acceptance |

## Anti-overengineering assessment

| Testing component/pattern | Disposition | Reason |
|---|---|---|
| Shared Python test harness, fixtures and contract schemas | Required | Matches approved implementation and coordinated repository |
| Ephemeral PostgreSQL and object-compatible integration dependencies | Required where semantics matter | Mocks cannot prove transactions, locks, constraints, migrations, references |
| Property/state-machine and fault-injection hooks | Required for critical invariants | Race/retry/fence behavior cannot rely on happy-path examples |
| Separate test repository/platform per capability | Rejected | Shared harness with capability-owned suites preserves ownership without duplication |
| Full permanent staging/performance/security fleet | Not required | Lanes may be ephemeral/created when evidence requires them |
| Real external provider/webhook in ordinary CI | Rejected while blocked | Local deterministic stubs/emulators plus admitted sandbox only later |
| Kubernetes-specific test platform | Rejected | Kubernetes is unselected; test process/container parity instead |
| Rust test stack/data-lake product | Rejected now | No Rust/data-lake implementation evidence; add only with the component decision |
| AI-only test approval | Rejected | AI assists; human/owner and reproducible pipeline evidence remain authoritative |

## Recommendations

### R-16-01 — Make risk/contract coverage the release unit

**Requirement/where:** source Section 15; all requirements and blocks. **Why now:** line/branch coverage cannot prove tenant, authority, job, model, or recovery semantics. **Simplest implementation:** stable risk/contract IDs mapped to scenarios, fixtures, owners, environments, criteria, and evidence manifests. **Alternative:** generic test pyramid and percentage target. **Why rejected:** gaps remain invisible and numeric target is unsupported. **Trade-off:** matrix maintenance. **Reconsideration:** tools may automate mapping; the trace remains mandatory.

### R-16-02 — Test real PostgreSQL/object authority boundaries early

**Requirement/where:** jobs, data publication, model registry, audit/usage, migrations and restore. **Why now:** transactions, uniqueness, locks, fencing, and cross-store reconciliation are central risks. **Simplest implementation:** ephemeral real PostgreSQL and object-compatible fixtures in CI/shared validation plus deterministic crash hooks. **Alternative:** mocks until E2E. **Why rejected:** false confidence in the most critical semantics. **Trade-off:** slower setup and fixture lifecycle. **Reconsideration:** optimize parallelization, not semantic fidelity.

### R-16-03 — Treat every admission block as an executable negative suite

**Requirement/where:** ADR-007/008 and Stage 15. **Why now:** architecture blocks are otherwise easy to bypass during implementation. **Simplest implementation:** default-deny tests assert blocked operations are unavailable and re-entry suites emit evidence without changing status. **Alternative:** checklist-only governance. **Why rejected:** configuration/code drift can enable paths silently. **Trade-off:** gates require maintained fixtures and authorities. **Reconsideration:** never remove default denial; update exact evidence with superseding decisions.

### R-16-04 — Optimize automation for a single human operator without delegating authority to AI

**Requirement/where:** accepted ADR-009; CI/CD, recovery and release gates. **Why now:** one sponsor cannot rely on manual broad regression or 24/7 observation. **Simplest implementation:** one-command reproducible suites, deterministic fixtures, machine-readable evidence, actionable failure summaries, and rehearsed runbooks; AI may assist analysis. **Alternative:** manual testing or AI self-approval. **Why rejected:** neither is reproducible/accountable. **Trade-off:** upfront automation work. **Reconsideration:** additional team may split ownership, but evidence/approval separation remains.

## Decisions

- Adopt this level, ownership, fixture, contract/risk, critical-path, data, capability, security, delivery, load, resilience, and release-gate strategy as the Stage 16 testing baseline, subject to sponsor approval.
- No new ADR is proposed: Stage 16 operationalizes accepted requirements, blocks, architecture, deployment, and evidence decisions without changing them.
- Keep every `MIGRATION_BLOCKED`, `EVIDENCE_BLOCKED`, ADR-008 block, and `DEPLOYMENT_ENVIRONMENT_BLOCKED` active until its exact test evidence and accountable approval exist.
- Record agent evaluations as not applicable now and mandatory re-entry work for any future approved agent.
- Keep Stage 17 unstarted until Stage 16 passes its gate and the sponsor explicitly authorizes continuation.

## Contradictions and dangerous assumptions

| ID | Finding | Resolution | Consequence |
|---|---|---|---|
| `C-16-01` | Existing prototype tests/logs/CSVs may look like target acceptance evidence | Treat as migration inputs only; target suites use approved contracts and immutable evidence | Profiles remain blocked |
| `C-16-02` | Passing tests can be mistaken for automatic block clearance | Test evidence and accountable approval are separate transitions | No silent production admission |
| `C-16-03` | One Linux server can make destructive fault/load tests unsafe | Run in disposable isolated clones/lanes; never fault-inject shared production | Production integrity preserved |
| `C-16-04` | AI coding/testing can be mistaken for independent assurance or operations | AI is an assistant; pipeline reproduction and human/owner decisions are authoritative | No AI self-approval or hidden runbook state |
| `C-16-05` | Service-card constants (for example NPT event floors) can look like approved targets | Test current migration behavior separately; target thresholds require versioned scientific approval | No prototype constant becomes production gate silently |
| `C-16-06` | Mocks can pass while PostgreSQL/object/receiver semantics fail | Use real compatible integration dependencies for authority behavior | More CI burden, credible evidence |
| `C-16-07` | Load tests without targets can appear to pass capacity | Report curves/saturation/invariant behavior only; Stage 17 owns targets | No production sizing claim |
| `C-16-08` | LAB suite can imply release veto/promotion authority | LAB remains evidence consumer until operating contract is approved | Sponsor/owners retain decision authority |
| `C-16-09` | Agent N/A can become a permanent loophole | Future agent requires Stage 11 and Stage 16 revision | No inherited agent approval |

## Open questions

| ID | Question | Blocking? | Options | Recommended temporary disposition | Effect |
|---|---:|---|---|---|---|
| `Q-16-01` | Which Python versions/dependency/build/test tools and PostgreSQL versions are supported? | Before implementation/release | Select supported matrix from environment | Keep contracts/tool-neutral; test chosen matrix once approved | No runtime/tool claim |
| `Q-16-02` | What numeric quality, performance, freshness, availability, recovery, security-alert and cost targets apply? | Before production | Versioned per-operation/profile targets | Measure distributions; invariant-only gates now | Stage 17/owners required |
| `Q-16-03` | What selected Linux host, networking, TLS, secrets, backup, telemetry and patching implementation will be tested? | Before production | Supply environment evidence | Keep `DEPLOYMENT_ENVIRONMENT_BLOCKED` | No production deployment approval |
| `Q-16-04` | Who are the named scientific, security, data, release and incident approvers besides the sponsor where separation is required? | Before block clearance/production | Assign people/services under policy | Logical owners only | Sensitive gates remain blocked |
| `Q-16-05` | What LAB test data, interface, execution environment, thresholds and release authority apply? | Before LAB acceptance | Advisory; required evidence; veto | Evidence consumer only | No LAB promotion claim |
| `Q-16-06` | Which first-release capabilities/consumers and conditional paths are in scope? | Before release acceptance | One vertical slice; subset; all | Test all contracts; activate none without scope/admission | Runtime suite/sizing remains broad |
| `Q-16-07` | What retention/quarantine/waiver policy applies to test evidence and flaky tests? | Before governed release | Policy by evidence class | Immutable manifest; critical tests cannot be waived | Storage/governance unresolved |

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Every source-requested test type covered | PASS | Source-instruction and test-level tables |
| Critical risks/contracts have a test level | PASS | Contract and critical-risk matrix |
| Critical risks/contracts have a logical owner | PASS | Same matrix and ownership table |
| Critical risks/contracts have an environment/fixture | PASS | Same matrix plus fixture strategy |
| Critical risks/contracts have a pass criterion | PASS | Same matrix and production invariants |
| Critical risks/contracts have a release consequence | PASS | Same matrix and gate-transition table |
| Every Stage 13 critical path covered | PASS | CP-13-01 through CP-13-08 matrix |
| All seven capabilities and admission states covered | PASS | Capability production-admission matrix |
| Eight ADR-008 blocks and deployment block covered | PASS | Security/isolation matrix |
| Every Stage 12 tenant-bearing asset class covered | PASS | Tenant-bearing asset isolation coverage |
| Highest-risk production scenarios explicit | PASS | 13 production-blocking invariants |
| Test data/fixtures and ownership boundaries explicit | PASS | Fixture and ownership sections |
| Load tests avoid unsupported targets | PASS | Measurement plan and `C-16-07` |
| Agent evaluations correctly dispositioned | PASS — NOT APPLICABLE | Current negative tests plus future re-entry suite |
| Authorized assurance review reconciled | PASS | Final read-only review reported no unresolved critical/high defect and recommended `PASS` |
| Workspace structure and source integrity | PASS | Existing Bash validator could not launch under Windows WSL access policy; an exact read-only PowerShell equivalent found 0 missing required files, 25 numbered stages, and 0 checksum failures |
| Stage 17 not executed | PASS | Scope, decisions and stop condition |

**Gate result: PASSED AND APPROVED.** Every material requirement, risk, contract, Stage 13 path, capability profile, security/deployment block, and Stage 12 tenant-bearing asset class has a test level, logical owner, environment, deterministic pass criterion, and release consequence. The authorized assurance reviewer reported no unresolved critical or high defect and recommended `PASS`. The sponsor explicitly approved Stage 16 on 2026-08-13. Passing this logical design gate clears no production-admission block and makes no one-server production-fitness claim. Stage 17 alone is authorized.

## Downstream consequences

- Stage 17 must turn load/resource/usage/cost curves into a capacity model and may propose targets or purchases only with evidence and the workflow gate.
- Stage 18 must index accepted ADR-009 and verify every material testing-related decision is represented without manufacturing an ADR for test mechanics.
- Stage 20 must sequence test automation, fixtures, migrations, recovery drills, block clearance and named owner/runbook work for a single-human/AI-assisted implementation model.
- Stage 21/23 evidence packages must link requirement/risk/block IDs to immutable test manifests; no “tested” claim without results.
- Stage 24 assurance must treat quarantined critical tests, active blocks, missing targets/owners and unexercised recovery as unresolved defects.

## Exact next-stage inputs and stop condition

Stage 16 is approved and Stage 17 alone is authorized. Do not execute Stage 18.

Stage 17 must read:

1. Approved `outputs/stages/00-source-audit.md` through `outputs/stages/16-testing.md`
2. Accepted ADR-000 through ADR-009
3. `sources/normalized/system-design-prompt.md` section **16. Capacity, performance, and cost**
4. Measured workload/resource/cost evidence if available
5. `stages/17-capacity-cost.md`, `templates/stage-output.md`, and directly referenced capacity templates

Execute Stage 17 only after explicit sponsor authorization. Do not begin Stage 18.
