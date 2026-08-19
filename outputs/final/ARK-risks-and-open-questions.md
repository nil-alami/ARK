# ARK risks and open questions — ADR-017/018 publication revision

Status: `POST-PUBLICATION REVISION — ADR-017/018 ACCEPTED; INDEPENDENT RE-ASSURANCE PENDING`

## Top ten unresolved questions

| Rank | Question | Required by | Current fail-closed treatment |
|---:|---|---|---|
| 1 | Which consumer, capability operation and business outcome form Phase 2? | Phase 2 entry | Build Phase 1 only; REC fixture is not MVP selection |
| 2 | Which source/canonical contracts and stable opaque identifiers are authoritative? | Real data activation | Synthetic only; `DATA_CONTRACT_ADMISSION_BLOCKED` |
| 3 | Who is named data/source-contract authority? | First contract admission | Unassigned under ADR-016 |
| 4 | Who owns capability science, evaluation, promotion/assignment and thresholds? | Capability re-entry | All seven profiles blocked |
| 5 | What external/workload identity, network/TLS, secrets/keys and privileged mechanisms apply? | Validation/production boundary | ADR-008 trust/crypto/privileged blocks |
| 6 | What classification, consent/purpose, residency, retention, deletion/legal-hold and backup policy applies? | Real data onboarding | `DATA_GOVERNANCE_BLOCKED` |
| 7 | What production Linux/PostgreSQL/object/telemetry/backup/patching environment and runbooks exist? | Phase 3 | `DEPLOYMENT_ENVIRONMENT_BLOCKED` |
| 8 | What workload, latency, freshness, completion, availability, recovery, growth and cost targets are approved? | Production/capacity | `CAPACITY_ADMISSION_BLOCKED` |
| 9 | Who owns security, integration/cutover, release and production operations, and what support scope applies? | First affected decision/Phase 3 | Unassigned; no 24/7 assumption |
| 10 | What authority does LAB have and which business/scientific criteria determine acceptance? | Phase 2 evidence | Evidence consumer only; no implicit veto/promotion |

Original source provenance for six normalized-only cards, Synapse internals/provider behavior and the remaining discovery questions also remain open under ADR-000 and Stage 01.

### ADR-017 product-policy questions

The sponsor has closed the hierarchy, uniform-pattern, admin-pattern-change, and organization-wide admin-scope decisions. These narrower questions remain intentionally open and fail closed:

- What additional account-registration fields are required, and what phone verification/uniqueness, credential, recovery, retention, and deletion policies apply?
- May an organization have multiple owners, and how are ownership transfer and recovery authorized?
- May an admin appoint or remove other admins? Until approved, only an organization owner may do so.
- What exact permissions activate `viewer` and `tester`? Both roles remain unavailable.
- How may a business move between organizations? Direct parent mutation is prohibited until a transfer contract exists.
- Is any cross-business aggregation, combined dataset, job, analytics, or export required? Organization-wide admin scope does not imply it.

### ADR-018 credit-management questions

The shared owner balance, organization-policy-not-wallet rule, debit attribution, request order, and dual financial gate are decided. Production charging remains fail-closed until these questions are answered:

- How are credits purchased, granted, expired, refunded, reversed, or manually adjusted, and which commercial/accounting authority approves them?
- What are the immutable pricing units/formulas, rounding and currency/tax treatment, and who may approve a `pricing_version`?
- Which time zone and boundary rules define daily/monthly policy windows?
- What exact type/behavior does `hard_limit` have when false, and how/where are warning thresholds delivered?
- What is charged or released for cancellation, partial success, job failure, provider ambiguity, and actual usage beyond the initial reservation?
- Can a customer ever have multiple billing accounts, can an organization transfer billing accounts, and what reconciliation/approval contract governs either change?

## Top ten risks

| Rank | Risk | Consequence | Current mitigation / release effect |
|---:|---|---|---|
| 1 | Fixture mistaken for production capability | False scientific/release claim | `POA_FIXTURE_ONLY`; all profile and data-contract blocks remain |
| 2 | Organization-wide admin scope becomes unscoped or cross-business data authority | Exposure/influence across businesses or organizations | Stored membership→organization→business derivation, one-business execution scope, owner ports, namespace/RLS defense, no implicit aggregation/export, and adversarial suite |
| 3 | Shared PostgreSQL becomes shared business ownership | Boundary erosion and unsafe cross-writes | Owned schemas/migrations/writers and dependency tests |
| 4 | Retry/crash/lease/response loss duplicates or falsifies effect | Corrupt truth or external harm | Stable identity, CAS, fencing, finalization and ambiguity reconciliation |
| 5 | Prototype behavior copied as target science | Invalid/irreproducible output | Four `MIGRATION_BLOCKED` remediation gates |
| 6 | Synapse/provider internals inferred | Privacy/safety/cost/reliability failure | Interface-only evidence, three `EVIDENCE_BLOCKED`, `LLM_PROVIDER_BLOCKED` |
| 7 | Model/verifier/insight/event gains action authority | Unauthorized effect | Deterministic Phase A/B/at-effect policy outside models |
| 8 | One-server validation called production/HA | Outage/data-loss exposure | Deployment/capacity blocks and explicit single failure domain |
| 9 | Sponsor+AI treated as complete operating authority | Self-approval and unsafe operations | ADR-016 narrow scope; named later authorities mandatory |
| 10 | Scale products added by fashion | Complexity, cost and recovery burden | Stage 23 classifications and measured ADR triggers |

Additional ADR-018 financial risk: concurrent organizations could overspend the shared balance or duplicate charges during retry/recovery. The mitigation is atomic policy+balance reservation with durable job acceptance, active-reservation headroom, stable usage identities, append-only settlement/adjustment, and `CREDIT_BILLING_ADMISSION_BLOCKED` until exact semantics and evidence pass.

## Active blocks

Production remains unavailable under four `MIGRATION_BLOCKED`, three `EVIDENCE_BLOCKED`, eight ADR-008 blocks, `DEPLOYMENT_ENVIRONMENT_BLOCKED`, per-release/profile `CAPACITY_ADMISSION_BLOCKED`, `DATA_CONTRACT_ADMISSION_BLOCKED`, `CONSUMER_CUTOVER_BLOCKED`, `CREDIT_BILLING_ADMISSION_BLOCKED`, and the later authority gates preserved by ADR-016. ADR-017/018 clear none of them: configuring a capability or funding a shared account does not admit production execution. Each block clears independently through evidence plus recorded human authority; tests are necessary but insufficient.

## Decisions required now

For Phase 1 only:

- retain the Python/modular-monolith/PostgreSQL/object-contract baseline;
- retain synthetic, non-production, fixture-only scope;
- represent `account → organization membership → organization → business`, with business as the tenant/data-isolation unit;
- enforce one versioned capability pattern uniformly across every organization business and allow owner/admin pattern changes under ETag, idempotency, mandatory audit, and execution-time recheck;
- make admin organization-scoped while denying unscoped or implicit cross-business data operations and keeping viewer/tester inactive;
- represent one synthetic shared owner billing balance across organizations, organization policies rather than wallets, dual policy+balance admission, atomic reservation+job acceptance, and complete retry-safe debit attribution;
- use the sponsor’s ADR-016 authority and keep AI non-authoritative;
- choose and record reversible supported implementation tools for Python/dependency lock, package layout, migrations, local PostgreSQL/object adapter, REST/schema/test tooling, process supervision, build/config identity and safe synthetic reset.

No production, vendor, real capability, source, model, webhook, schedule or scale decision is required to begin Phase 1.

## Decisions safely deferred

| Decision | Deferral point / reason |
|---|---|
| Phase 2 slice | Before Phase 2; Phase 1 is reusable fixture plumbing |
| Capability algorithms and thresholds | Profile re-entry; science must not be invented by roadmap |
| Production IAM/network/secrets/governance mechanisms | Their validation/Phase 3 gates |
| Hosting/server size/containers/HA/DR | Production environment admission |
| Scheduler/webhook/event/proactive path | First named scheduled consumer/action requirement |
| Broker/streaming/CDC | Measured dispatch/fan-out/freshness failure after simpler remedies |
| Feature-store/MLOps/registry product | Proven reuse/skew/control/scale gap |
| Microservice/gRPC/Kubernetes | Specific extraction, transport or fleet trigger |
| GPU/Rust/lakehouse/vector | Repeatable workload/quality/TCO evidence |
| Agent/MCP/A2A | Full Stage 11 re-entry and explicit approval |
| Vendor purchase | Concrete need, benchmark, security/recovery fit, TCO/exit and budget authority |
| Remaining account/role/transfer/cross-business policy | Before the first affected endpoint is activated; ADR-017 records current fail-closed behavior |
| Pricing, credit funding/expiry/refund, policy-window, partial/failure charging, billing roles/accounting and multiple-account/transfer semantics | Before any production debit; ADR-018 keeps `CREDIT_BILLING_ADMISSION_BLOCKED` |

## Effective-assumption warnings

- ADR-011, not expired `A-01-DATA`, governs source activation.
- ADR-015, not expired cutover language in `A-07-INTEGRATION`, governs coexistence/cutover.
- ADR-008 governs trust/security and supersedes older deferrals/cache wording.
- ADR-016 governs Phase 1 accountability and does not qualify later owners.
- ADR-017 governs product organization ownership/admin scope; an organization owner/admin is not an ARK architectural, scientific, security, or production authority.
- ADR-018 governs shared owner credits and organization spending policies; an organization policy is not a wallet, and organization admin authority does not imply billing mutation.
- Business/KPI, scale/target, remaining team/authority and temporary source-provenance uncertainties remain open; no publication synthesis closes them.

## Provenance

`outputs/stages/01-discovery-and-questions.md — Prioritized discovery questions`; `outputs/stages/10-mlops.md — Capability ML profiles and production-admission gates`; `outputs/stages/12-security-governance.md — Production security-admission register`; `outputs/stages/17-capacity-cost.md — Production capacity-admission record`; `outputs/stages/20-roadmap.md — Cross-phase risk register`; `outputs/stages/21-provisional-final-deliverables.md — Top ten unresolved questions`; `— Top ten risks`; accepted ADR-011, ADR-015, ADR-016, ADR-017 and ADR-018; both 2026-08-15 sponsor-decision sources.
