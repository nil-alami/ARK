# ARK implementation roadmap — ADR-017/018 publication revision

Status: `POST-PUBLICATION REVISION — ADR-017/018 ACCEPTED; INDEPENDENT RE-ASSURANCE PENDING`

## Phase 1 — non-production proof of architecture

Implement one synthetic REC-shaped async request through the real ARK boundaries, ADR-017 account/organization/business control model, and ADR-018 shared owner credit gate. Required roles: `api`, `worker-general`, one-shot maintenance/migration. Required stores: real PostgreSQL semantics and behavior-compatible object storage. Required handler: deterministic `POA_FIXTURE_ONLY`. Scheduler, providers, publisher, webhook, workflow, model training/cache, payment processing, production billing and production trust are absent.

### Ordered backlog

1. Establish one Python release, module dependency rules and role entrypoints.
2. Add module-owned PostgreSQL schemas/migrations and immutable object-reference adapter.
3. Implement test-only trusted context with one owner/admin account, at least two organizations, and multiple isolated business tenants per organization.
4. Implement account-profile, organization, membership, business-registry, and versioned organization capability-pattern records in existing owned schemas/ports.
5. Implement one synthetic owner billing account shared by the organizations, versioned organization credit policies, append-only credit ledger, balance/headroom projections, and reservation/settlement/release records—never organization wallets.
6. Publish immutable fixture capability/operation and pricing definitions and make discovery the intersection of release visibility and the effective organization pattern.
7. Implement push/reference synthetic ingestion, raw preservation, structural and semantic validation, and readiness publication for exactly one derived business tenant per operation.
8. Implement separated pattern eligibility, subscription, entitlement, grant, quota, organization credit-policy and shared owner-balance decisions.
9. Implement submit/poll/cancel, canonical idempotency and one durable job atomically paired with a credit reservation and pinned to organization, membership, business tenant, pattern, credit-policy and pricing versions.
10. Implement attempts, leases, fences, heartbeats, reaper, execution-time pattern/credit recheck, handler compatibility, exactly-once usage settlement and unused-reservation release.
11. Implement capability eligibility and deterministic fixture result commit.
12. Implement `FINALIZING`, lineage, usage and mandatory audit obligations, including pattern/policy old-new audit and full charge attribution.
13. Add correlation, PII-safe telemetry and truthful health.
14. Add fault hooks for crash, response loss, lease expiry, cancellation, pattern/policy change, reservation/settlement race, ledger outage and audit outage.
15. Add cross-organization/business, unscoped-business, inactive-role, pattern inheritance/override, policy-vs-balance denial, shared-pool concurrency, duplicate-charge, invalid/stale/duplicate/corrupt fixture tests against real stores.
16. Produce immutable evidence manifest and sponsor-operable start/stop/retry/reconcile/reset runbook.

Exit proves logical architecture only and clears no admission block.

## Phase 2 — one selected validation slice

Entry requires the sponsor to select exactly one consumer, one source-contract family, one capability operation and one business outcome. Named data/source, capability-scientific, security and integration authorities must exist for exercised decisions. Replace only the Phase 1 fixture/trust/source pieces needed for that slice; remediate the exact ADR-007 profile; admit the concrete ADR-011 contract; complete evaluation/reproduction and consumer/LAB evidence. Phase 2 is not automatically production.

## Phase 3 — production hardening and admission

Production admission is a join, not a phase checkbox. Clear every applicable capability, data-contract, ADR-008 security, ADR-018 credit/billing, deployment, capacity and cutover/delivery/provider block independently through its recorded evidence and named authority. Approve workload/SLO/RPO/RTO/retention/cost/pricing profiles; rehearse release, migration, backup, restore, credit reconciliation, recovery, rollback and incident runbooks; preserve zero unresolved Critical/High defects. This is the earliest point a production claim may be considered.

## Phase 4 — scale-driven improvements

Use measurements in this order:

1. correct algorithms, queries, serialization and indexes;
2. bound payloads, batches, checkpoints and backpressure;
3. vertical resource sizing;
4. tune concurrency and split same-release runtime roles;
5. add simple replicas/second host or managed store only when justified;
6. consider broker, GPU, Rust, additional data platform, Kubernetes or module extraction independently only when their exact trigger persists.

Every material change requires before/after correctness/security/performance evidence, owner/runbook, TCO including sponsor time, and a new/superseding ADR when it changes an accepted decision.

## Phase 5 — optional capabilities

Additional capability profiles, schedules, proactive action, event/webhook delivery, named workflows, Synapse/provider integration, feature-store/streaming/vector or agent work each require a named release requirement and its cumulative re-entry gate. No optional seam is an implied destination.

## Gate summary

| Phase | Entry | Exit | Production meaning |
|---|---|---|---|
| 1 | Approved architecture, ADR-017/018, and sponsor Phase 1 authority | 16 backlog items pass in clean/fault lanes | None |
| 2 | Selected slice, contracts, named affected authorities | Slice-specific evidence accepted in validation | None unless Phase 3 also passes |
| 3 | Authoritative environment/policy/workload/owner evidence | Every applicable block explicitly cleared and runbooks rehearsed | First possible production admission |
| 4 | Admitted workload with repeatable measured target failure | Change proves benefit and preserves invariants | Improves only affected admitted scope |
| 5 | Named optional requirement and re-entry packet | Exact path independently admitted | Only that path/profile |

## Complete phase contracts

| Phase | Scope | Tasks | Deliverables | Dependencies | Acceptance criteria | Major risks | Deliberate postponements |
|---|---|---|---|---|---|---|---|
| 1 | Synthetic, non-production async REC-shaped proof through ADR-017 hierarchy and ADR-018 credit gate | Execute the 16 ordered backlog items; exercise clean, crash, retry, cancellation, audit/ledger-outage, pattern/policy/reservation races, cross-organization and cross-business paths | Runnable `api`, `worker-general`, maintenance role; hierarchy/pattern/billing-policy/credit-ledger records and ports; migrations; fixture contract/handler/pricing; tests; evidence manifest; sponsor-operable runbook | Approved Stages 02–23 baseline, ADR-016/017/018 sponsor decisions, supported local tools, disposable PostgreSQL/object semantics | Organization-wide admin and uniform pattern behave correctly; every business operation has one derived tenant; organizations share one balance without wallets; policy+balance reservation is atomic with job acceptance and settlement is fully attributed/retry-safe; deterministic result, raw-first readiness, fencing, isolation, fail-closed audit and correlation pass; every production block remains active | Organization scope or billing account spoofing; shared-pool overspend/double charge; fixture mistaken for science/pricing; mocks hide store behavior; sponsor burden | Viewer/tester; ownership/business/billing transfer; real pricing/funding/accounting; cross-business aggregates; scheduler; real data/model/provider; webhooks/events/proactive; workflow; production environment; scale products |
| 2 | Exactly one sponsor-selected consumer/source-contract/capability-operation/business-outcome validation slice | Admit its source contract; remediate only its capability profile; replace affected fixture adapters; produce evaluation/reproduction, consumer and LAB evidence | Scope record; admitted contract packet; versioned capability evidence; integration result; evidence package; release candidate manifest | Phase 1; explicit scope; named data/scientific/security/integration authorities; ADR-011 and applicable ADR-007/008 evidence | Named flow passes Stage 16 suites and its evidence is accepted by the proper authorities; status changes are recorded; no test alone clears a block | All-seven scope creep; prototype values promoted; LAB treated as authority; hidden consumer coupling | Other six capabilities; unrelated provider/delivery blocks; scale mechanisms |
| 3 | Production hardening and admission for the selected release only | Clear applicable blocks independently; select environment/trust/secrets mechanisms; approve numeric profiles; rehearse release/migrate/backup/restore/reconcile/rollback/incident procedures | Environment/trust/governance/capacity profiles; supply-chain manifest; named owner/runbook set; restore/load/security evidence; production admission record | Phase 2 candidate; authoritative policy/environment/workload/cost evidence; named security/release/production-operations authorities | Every applicable block exit explicitly approved; zero unresolved Critical/High; sponsor/operator can reproduce runbooks; single-server lane is not called HA | Partial gate mistaken for total admission; AI treated as approver/operator; rollback layers conflated; one host overstated | Non-applicable capability/provider/delivery/cutover paths remain blocked |
| 4 | Evidence-triggered optimization or scaling of an admitted workload | Measure; apply simpler code/query/batch remedies; then evaluate vertical sizing, role split, replica/store/product/extraction independently | Before/after benchmark; correctness/security evidence; TCO including sponsor time; updated placement/runbook; ADR if material | Admitted workload; approved objective; repeatable bottleneck; Stage 17 trigger; accountable owner | Change resolves the approved need without weakening tenant/authority/recovery contracts and without clearing unrelated gates | Premature distribution; bundled scale stack; mean-only sizing; new unowned failure domains | Every mechanism whose individual trigger has not passed |
| 5 | Optional additional capabilities, schedules, proactive/delivery, named workflow, Synapse, data products or agent work | Apply the exact cumulative re-entry/admission contract for one named requirement; implement and evaluate only that bounded path | Capability/path-specific scope, contract, evidence, owner/runbook and ADR where material | Named release requirement plus applicable ADR-007/008/011/013/015 and Stage 11 gates | Only the named path/profile is admitted by its authorities; deterministic action gates remain outside models/agents | Optional seam mistaken for destination; verifier gains authority; fashionable platform addition | All unnamed optional paths and generic platforms |

## Source provenance

`outputs/stages/20-roadmap.md — Roadmap at a glance`; `— Phase 1 — Walking skeleton / proof of architecture`; `— First implementation milestone — engineering-ready backlog`; `— Phase 2 — MVP: first admitted vertical slice`; `— Phase 3 — Production hardening and admission`; `— Phase 4 — Scale-driven improvements`; `— Phase 5 — Optional future capabilities and mechanisms`; accepted ADR-016, ADR-017 and ADR-018; both 2026-08-15 sponsor-decision sources.
