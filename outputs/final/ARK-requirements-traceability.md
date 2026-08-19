# ARK requirements traceability — ADR-017/018 publication revision

Status: `POST-PUBLICATION REVISION — ADR-017/018 ACCEPTED; INDEPENDENT RE-ASSURANCE PENDING`

## Forward trace

| Requirement | Design realization | Verification / admission effect |
|---|---|---|
| `ARK-FR-001` | Separate control module for subscriptions, entitlements, grants, quota, policy, audit and usage | Contract/negative tests; denial creates no ingestion/job/effect |
| `ARK-FR-002` | Push/micro-batch and referenced bulk ingestion; pull/federation/streaming conditional | Ingestion contract tests; source exceptions require new evidence |
| `ARK-FR-003` | Raw-first structural→semantic→readiness publication | Invalid input never READY; lineage and correction tests |
| `ARK-FR-004` | Seven versioned capability definitions and independently owned schemas | Definition coverage/schema tests; blocked fields remain explicit |
| `ARK-FR-005` | Common trusted envelope plus capability-specific payload | Tenant/envelope/version/idempotency contract tests |
| `ARK-FR-006` | Readiness, platform control and capability eligibility remain distinct | Layer-by-layer outcome scenarios |
| `ARK-FR-007` | PostgreSQL job/attempt/lease/fence/cancel/finalize lifecycle | State, restart, duplicate, cancellation and reconciliation suites |
| `ARK-FR-008` | Sync is opt-in; long/retryable work durable | Operation-profile tests; missing targets default to async/unavailable |
| `ARK-FR-009` | Explicit lifecycle job, evaluation, promotion and assignment | No inference-time train/promote tests; exact reproduction/rollback evidence |
| `ARK-FR-010` | Phase A, immutable insight, Phase B and at-effect recheck | Negative grant/revocation/stale/quota/dedupe/audit/effect suites |
| `ARK-FR-011` | Internal fact transport, result polling and external delivery state separated | Event/webhook contract and idempotency tests; delivery remains blocked |
| `ARK-FR-012` | Minimized immutable LAB evidence package | Isolation/reproduction/evaluation suite; LAB is not authority |
| `ARK-FR-013` | Registered account can own multiple organizations; each organization contains business tenants | Account/organization/business cardinality, opaque-ID, lifecycle and ownership-boundary tests |
| `ARK-FR-014` | One versioned organization capability pattern applies uniformly to all current and future businesses | Inheritance/no-override, canonical-ID, ETag/idempotency, version-pin/recheck and audit tests |
| `ARK-FR-015` | Organization admin can access every business in the organization and change its capability pattern | Positive organization-wide admin tests plus cross-organization, unscoped-business and cross-business-combination denials |
| `ARK-FR-016` | Admin is active; viewer/tester are reserved but unavailable until exact mappings are approved | Role-policy tests fail closed for inactive roles and unauthorized admin-membership mutation |
| `ARK-FR-017` | Credits belong to one shared owner/customer billing account; organizations receive policies, never balances or subwallets | Shared-pool hierarchy, no-wallet/no-transfer schema and ownership tests |
| `ARK-FR-018` | Every request must pass both organization credit-policy headroom and shared owner available-balance checks | Policy-pass/balance-fail, balance-pass/policy-fail, both-pass and both-fail admission tests |
| `ARK-FR-019` | Credit reservation is atomic with durable job acceptance and settles/releases idempotently | Crash/concurrency/retry/replay/cancel/finalize/restore reconciliation tests; no job on failed reservation |
| `ARK-FR-020` | Every charge attributes payer, organization, business tenant, capability/operation, job, usage event, pricing version and amount | Immutable ledger completeness, lineage, duplicate-charge and authorized-read tests |
| `ARK-NFR-001` | Principal plus stored membership derives organization scope; stored business parent derives the tenant on every row/object/dataset/model/job/event/cache/evidence asset | Cross-organization/business, forged-scope, cross-asset, restore/replay/deletion concurrency suite |
| `ARK-NFR-002` | Independent source/data/feature/model/code/policy/job/result identities | End-to-end lineage and reproduction query |
| `ARK-NFR-003` | Bounded platform-neutral REST/JSON and typed ports | Schema lint, compatibility and consumer-neutral dependency tests |
| `ARK-NFR-004` | At-least-once attempts plus logical effect idempotency/fencing | Crash, duplicate, stale attempt and ambiguous-effect tests |
| `ARK-NFR-005` | Opaque tenant-scoped refs and PII minimization | Classification/schema/log/provider-transfer negative tests |
| `ARK-NFR-006` | Correlation, audit, lineage, usage and cost evidence | Trace-completeness and redaction/export-degradation tests |
| `ARK-NFR-007` | Versioned operation profiles before production acceptance | Missing numeric workload/SLO/RPO/RTO/cost keeps capacity/environment blocked |
| `ARK-NFR-008` | Organization administration remains separate from business-level tenant/data isolation | Every business asset carries one derived business tenant; organization membership alone cannot authorize unscoped or combined business data |
| `ARK-NFR-009` | Shared-balance and organization-policy concurrency is fail-closed, append-only, reconstructable and retry-safe | Parallel multi-organization reservation, unique usage identity, ledger outage, negative-balance, hard-limit, reconciliation and recovery suites |
| `ARK-CON-001` | One repository/coordinated release/modular monolith | Boundary/import/release tests; extraction requires ADR-003 gate |
| `ARK-CON-002` | Capability-owned logic/state/schema/migrations/tests/runbooks | Dependency and one-writer tests |
| `ARK-CON-003` | Consumer mapping outside capability cores | Adapter/core dependency and conformance tests |
| `ARK-CON-004` | Object refs for large immutable data; PostgreSQL for bounded operational state | Placement/size/reference/missing-object tests |
| `ARK-CON-005` | PostgreSQL initial job truth | Recovery/load tests; broker/engine requires measured ADR |
| `ARK-CON-006` | Source master-data authority and no probabilistic identity merging | Identity/readiness negative tests; unresolved identity blocks affected source-contract activation and publication of a READY dataset/capability use, not architecture publication |
| `ARK-CON-007` | Evidence-triggered component admission | Stage 23 six-question classification; no unsupported product/number |

## Reverse trace from Phase 1 required elements

| Element | Requirement(s) | Evidence |
|---|---|---|
| `C05-01` Consumer adapter boundary | FR-004/005/007/011; CON-003 | Test client uses public schemas only; import/contract tests prohibit consumer mappings in capability cores |
| `C05-02` Logical edge/API | FR-004/005/007/008; NFR-003/006 | Route/schema/correlation/size/deadline tests; no business authority at transport boundary |
| `C05-03` Auth and tenant context | FR-001/004/005/008/013/015/016; NFR-001/005/008 | Test trust profile, active membership, organization→business derivation, forged IDs, cross-organization/business, inactive roles and delegation negative suites |
| `C05-04` Control/eligibility/policy/billing | FR-001/006/010/013/014/015/016/017/018/019; NFR-001/004/008/009 | Organization/business/pattern/billing ownership, no subwallet, dual financial denial/no-job, exact membership/pattern/credit/pricing versions, ETag/idempotency, shared-balance/policy CAS and reservation-race tests |
| `C05-05` Capability/job API | FR-004/005/007/008; NFR-003/004 | Versioned invoke/submit/job/result/error/idempotency contract tests |
| `C05-06` Ingestion/validation/publication | FR-002/003/006; NFR-002/005; CON-006 | Raw-first, structural/semantic rejection, correction and no-false-READY tests |
| `C05-07` Dataset catalog/readiness | FR-003/006; NFR-002/003; CON-004/006 | Immutable version, lineage, readiness-authority and cross-tenant reference tests |
| `C05-08` PostgreSQL job manager | FR-007/008/019; NFR-004/006/009; CON-005 | Atomic reservation+job acceptance, duplicate submit, claim/lease/fence, retry/cancel/finalization, release/settlement and restart evidence |
| `C05-10` Worker runtime | FR-007/008/009; NFR-004 | Exact admitted handler, delegated context, cancellation, stale-fence and resource-bound tests |
| `C05-11a` Seven capability definitions/contracts | FR-004/005/006/009/012; NFR-002/003 | Definition-schema and blocked-profile assertions for all seven capabilities |
| `C05-11b` Deterministic fixture capability port | FR-004–008; CON-002 | `POA_FIXTURE_ONLY`, exact eligibility, cross-tenant and deterministic-result tests; zero scientific/production claim |
| `C05-12a` Polling result delivery | FR-007/011; NFR-003/004 | Response-loss, authorization and repeatable authoritative result retrieval |
| `C05-13` Operational PostgreSQL | FR-001/003/007/008/012; CON-005 | Owned-schema/role, migration, transaction, recovery and no-cross-writer tests |
| `C05-14` Object-storage contract | FR-002/003/007/009; NFR-002/005; CON-004 | Opaque tenant-scoped refs, checksum, missing-object, traversal, lifecycle and reconciliation tests |
| `C05-15` Capability feature/result/state namespaces | FR-006/007/009; NFR-001/002 | Owner-only write, tenant/version isolation, immutable publication and retention tests |
| `C05-16a` Minimal artifact/release identity | FR-009/012; NFR-002/003/006 | Immutable release/digest/provenance/compatibility and fixture-evidence-manifest tests |
| `C05-17` Secret/config delivery interface | NFR-001/005/007; CON-007 | No secret in source/request/log; test adapter isolation; production mechanism remains blocked |
| `C05-18` Audit/lineage/usage/credit ledger | FR-001/012/019/020; NFR-002/005/006/009 | Fail-closed audit/ledger, complete charge attribution, unique usage settlement, append-only adjustment, lineage/correlation, balance reconstruction, integrity and access tests |
| `C05-19` Observability interfaces | NFR-006/007 | Signal schema, redaction, bounded-buffer/export-outage and truthful-health tests |
| `C05-20` Admin/operations interfaces | FR-013/014/015/016/017/020; NFR-004/005/006/008/009; CON-001/002 | Organization-wide admin/pattern operations, owner-only billing-policy/ledger views, role-separation and cross-scope denials, credit reconciliation, bootstrap/interruption/reconcile, least-privilege, mandatory-audit and production-denial tests |

## Decision trace

| Decision family | Requirements governed |
|---|---|
| ADR-003/010/014 | CON-001/002/004/007; NFR-003/004 |
| ADR-004/015 | FR-004/005/008/011; NFR-001/003; CON-003 |
| ADR-005 | FR-007/008; NFR-004/006; CON-005 |
| ADR-006 | FR-010/011; NFR-001/004/006 |
| ADR-007/012 | FR-004/006/009/012; NFR-002/004/006/007 |
| ADR-008 | FR-001/010/011/012; NFR-001/005/006 |
| ADR-009 | NFR-004/006/007; CON-001/004/007 |
| ADR-011 | FR-002/003/006; NFR-002/005; CON-004/006 |
| ADR-013 | CON-007 and Stage 11 agent qualification |
| ADR-016 | Phase-specific accountability for every requirement gate |
| ADR-017 | FR-013/014/015/016; NFR-001/005/008; refines ADR-008 tenant/interface context without clearing blocks |
| ADR-018 | FR-017/018/019/020; NFR-006/009; refines ADR-017/008 control/usage context and creates `CREDIT_BILLING_ADMISSION_BLOCKED` |

## Ten closing deliverables map

| Required item | Publication location |
|---:|---|
| 1. Recommended starting architecture | `ARK-system-design.md — Binding architecture baseline` |
| 2. Minimal component list for first version | `ARK-system-design.md — Runtime roles and actual first placement`; `ARK-implementation-roadmap.md — Phase 1` |
| 3. Components explicitly postponed | `ARK-system-design.md — Stage 23 anti-overengineering classification — deferred or rejected mechanisms`; `ARK-risks-and-open-questions.md — Decisions safely deferred` |
| 4. Top ten unresolved questions | `ARK-risks-and-open-questions.md — Top ten unresolved questions` |
| 5. Top ten risks | `ARK-risks-and-open-questions.md — Top ten risks` |
| 6. First implementation milestone | `ARK-implementation-roadmap.md — Phase 1` |
| 7. Decisions that must be made now | `ARK-risks-and-open-questions.md — Decisions required now` |
| 8. Decisions that can safely wait | `ARK-risks-and-open-questions.md — Decisions safely deferred` |
| 9. Architecture completeness checklist | `ARK-requirements-traceability.md — Publication completeness checklist` |
| 10. Non-technical executive summary | `ARK-system-design.md — Non-technical executive summary` |

## Publication completeness checklist

| Concern | Final status / remaining activation gate |
|---|---|
| Sources, system boundary, seven capability inventory | Covered; normalized-only provenance remains explicit under ADR-000; post-publication hierarchy and credit-management sponsor sources are recorded in the manifest and ADR-017/018 |
| Requirements, components, data, API, execution, events, ML | Covered by approved Stages 02–10 and publication artifacts |
| Agent decision, security, reliability, observability | Covered logically; activation blocks remain |
| Deployment, testing, capacity | Covered as provisional/symbolic contracts; production evidence absent |
| ADRs, diagrams, roadmap, runtime analysis | Covered through Stage 22 |
| Anti-overengineering and publication assembly | Original Stage 23 approved; ADR-017/018 reuse C05-03/C05-04/C05-08/C05-18/C05-20 and add no component/product/deployable or organization wallet |
| Independent assurance | Original Stage 24 PASS remains historical evidence; independent re-assurance of the ADR-017/018 revision is pending |

## Provenance

`outputs/stages/02-system-definition.md — Functional requirements`; `— Non-functional requirements`; `— Constraints`; `outputs/stages/16-testing.md — Contract and critical-risk verification matrix`; `outputs/stages/18-architecture-decisions.md — Complete ADR register`; `outputs/stages/21-provisional-final-deliverables.md — Source-instruction coverage`; `outputs/stages/22-runtime-execution-analysis.md — Requirements-traceability updates`; both 2026-08-15 sponsor-decision sources; accepted ADR-017 and ADR-018.
