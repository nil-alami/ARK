# ADR-018 — Owner billing account, organization credit policy, and reservation

Status: `ACCEPTED`

Date: 2026-08-15

Decision owner: ARK sponsor (human user), through `sources/sponsor-decisions/2026-08-15-owner-billing-credit-management.md`

## Context and requirements

ADR-017 established an account/organization/business hierarchy with business-level tenant isolation and organization-wide capability configuration. The sponsor now requires a different hierarchy for credits: one commercial owner/customer billing account holds the shared balance, while each organization receives a consumption policy rather than a wallet. Every charge must trace payer, organization, business tenant, capability, job, usage event, pricing version, and amount.

This design must prevent four failures: organization subwallets that require manual transfers, concurrent overspending of the shared balance or organization limits, retries that charge twice, and a credit check that accidentally replaces authorization, capability-pattern, data, scientific, or production-admission gates.

The owner/customer billing account is a commercial payer boundary. It is not the human `AccountProfile`, organization owner role, ARK sponsor, module owner, or production/scientific/security authority.

## Decision

1. ARK adds a stable `OwnerCustomerAccount` commercial boundary with one active `OwnerBillingAccount` in the initial design. Multiple organizations may reference that billing account. Human principals act through separately authorized account/membership records.
2. Credits exist only in the owner billing account's append-only balance/ledger model. Organizations and businesses have no balance, wallet, transferable credit allocation, or child account.
3. Every organization linked to a billing account has one effective, versioned `OrganizationCreditPolicy`. The policy contains `organization_id`, `billing_account_id`, `monthly_limit`, `daily_limit`, `per_job_limit`, `hard_limit`, `warning_threshold`, `effective_from`, and `effective_to` plus immutable policy/version/audit identity.
4. An explicit `NULL` for a daily, monthly, or per-job ceiling means no organization-specific ceiling for that dimension; consumption still requires an effective policy record and sufficient shared owner balance. Missing policy, ambiguous window, expired policy, organization/billing-account mismatch, or invalid policy version fails closed. Zero is a zero ceiling, not unlimited.
5. The initial request gate is ordered: authenticate → resolve stored business → resolve stored organization → authorize the principal for that business → check effective organization capability pattern → validate dataset/readiness → evaluate capability eligibility and all other admission blocks → check organization credit policy → check shared owner available balance → reserve credits → durably accept/execute the job.
6. Both financial decisions must pass independently. Organization-policy approval cannot spend an insufficient owner balance, and a sufficient owner balance cannot override an organization ceiling.
7. Credit admission uses reservation, settlement, and release records. A reservation reduces both available owner balance and the applicable organization policy headroom for concurrency purposes. Successful priced usage settles exactly once; unused reservation is released; a failed acceptance creates no lasting debit.
8. In the initial same-PostgreSQL modular-monolith placement, the credit reservation and durable job acceptance are committed in one coordinated transaction through the billing/control and job-owner public ports. Each owner writes only its own tables. If that atomic boundary is later removed, a separately approved recoverable reservation/job-intent protocol is required before extraction.
9. Every immutable debit/settlement includes at least `billing_account_id`, `organization_id`, `business_id`, canonical `capability_id` (and operation/version where priced), `job_id`, globally stable `usage_event_id`, immutable `pricing_version`, and non-negative `amount`. It also carries reservation, policy version/window, actor/correlation, timestamps, and reversal/adjustment references where applicable.
10. `usage_event_id` and the priced logical effect are idempotency identities. A job retry or replay cannot create a second charge for the same priced usage event. Adjustments/refunds are new append-only ledger entries linked to the original; settled history is never edited or deleted in place.
11. The amount reserved must be derived from an immutable pricing version and bounded request inputs before execution. If actual usage can exceed the reservation, execution must either obtain an atomic incremental reservation before exceeding it or stop/fail according to the approved pricing contract. ARK may not silently create a negative balance or bypass an organization hard ceiling.
12. Only an authorized owner/customer billing administrator may fund/adjust the billing account or change organization credit policies initially. ADR-017 organization-wide admin authority does not grant billing/policy mutation by implication. Exact billing roles and separation of duties remain unresolved and fail closed.
13. Warning thresholds produce advisory state/evidence only and do not create authority. A hard policy denial, insufficient shared balance, missing pricing version, unavailable ledger/audit truth, or failed reservation produces no executable job/effect.
14. Credit policy/balance checks are additional control-plane admission gates. They do not clear or replace `MIGRATION_BLOCKED`, `EVIDENCE_BLOCKED`, data readiness, capability eligibility, model assignment, security/governance, environment, capacity, or another production block.
15. Production credit charging remains `CREDIT_BILLING_ADMISSION_BLOCKED` until authoritative pricing/units/rounding, credit issuance/funding/expiry/refund/adjustment, policy-window/time-zone, partial/failure/cancellation/provider-ambiguity, reconciliation/accounting, access/audit, named authority, and concurrency/recovery evidence are approved.
16. Every credit-consuming execution has a durable logical `job_id`, even if a future transport waits synchronously for its result. Until a priced synchronous contract explicitly preserves reservation, cancellation, timeout and job/result truth, `:invoke` is limited to unpriced/zero-credit operations and priced work uses durable submission.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| One wallet/balance per organization | Simple local balance view | Manual transfers, stranded credits, multiple ledgers, contradicts sponsor decision | Rejected | Only a superseding sponsor decision with commercial/accounting evidence |
| Shared owner balance plus organization policies | Flexible shared pool, explicit consumption controls, full attribution | Requires atomic shared-balance/policy concurrency and precise ledger recovery | Selected | Revisit physical mechanism only on measured scale/ownership need |
| Shared owner balance with no organization policies | Minimal records | Cannot bound organization consumption or implement sponsor controls | Rejected | Never while organization policy is required |
| Separate billing/ledger microservice or vendor now | Independent scaling/product features | Network consistency, reconciliation, vendor/accounting burden without environment evidence | Rejected initially | ADR-003 extraction trigger or approved financial/provider requirement |

## Rationale

The selected model represents the commercial requirement without introducing organization wallets. It reuses the existing control, usage/metering, audit, and PostgreSQL durable-state boundaries. Policy headroom plus reserved owner balance provides a concurrency-safe admission decision, while immutable settlement attribution supplies the exact payer→organization→business→capability→job trail required by the sponsor.

## Consequences and trade-offs

- The control plane gains commercial customer, billing account, credit policy, reservation, settlement/release, and balance-projection records but no new deployable component.
- Shared balance creates a contention scope across all organizations on the billing account; correctness takes priority over maximum parallelism, with optimization allowed only after measurement.
- Organization limits are policies, not earmarked money. Unused Organization A policy capacity does not reserve credits away from B, and B may still fail if the owner pool is exhausted.
- Jobs pin policy and pricing versions and link one or more priced usage events. Retry safety now includes financial idempotency and reconciliation.
- Financial policy changes and manual adjustments are privileged audited operations. Existing privileged-action and trust blocks remain active.
- Exact commercial/accounting semantics remain unresolved and are made an explicit production block rather than invented.

## Implementation constraints

- Minimum logical records: `OwnerCustomerAccount`, `OwnerBillingAccount`, append-only `CreditLedgerEntry`, `OrganizationCreditPolicy`, `CreditReservation`, and `CreditUsageEvent`/settlement; balance and policy-consumption totals are reconstructable projections, not mutable unaudited truth.
- Unique identities prevent more than one effective policy per organization/time range, duplicate reservation per priced request/effect, or duplicate settlement per `usage_event_id`/pricing version.
- Available balance equals admitted credits minus settled debits minus active reservations plus append-only approved credits/adjustments, under one defined invariant. Exact funding/expiry/refund formulas remain blocked until supplied.
- Policy consumption includes settled usage plus active reservations in the applicable approved window so parallel requests cannot pass against stale headroom.
- Resolution uses stored relationships: business→organization→billing account. Caller fields never choose a payer, organization, pricing version, balance, policy, or amount.
- Ledger, reservation, policy, and privileged mutation evidence is tenant-safe and access-controlled; full name, phone, payment data, secrets, and raw business inputs never appear in usage events by default.
- Do not add per-organization wallets, a credit-transfer workflow, a distributed ledger, billing microservice, payment processor, or financial data warehouse solely for this requirement.

## Validation evidence

- Hierarchy tests: several organizations share one billing account; every business charge resolves through its stored organization; forged payer/organization/business IDs are denied.
- Policy tests: daily/monthly/per-job ceilings, explicit null/unlimited dimensions, zero, effective interval, missing/expired/mismatched policy, warning threshold, version race, and owner-only mutation.
- Balance/concurrency tests: organization policy passes but balance fails; balance passes but policy fails; both pass; parallel requests across organizations cannot overspend shared balance or organization headroom.
- Job/reservation tests: atomic reservation+job acceptance, crash at each boundary, cancellation, rejection, release, settlement, incremental reservation, finalization, reconciliation, and restore epoch.
- Idempotency tests: duplicate submit, retry, replay, response loss, worker retry, and usage-event redelivery produce one logical charge; adjustment/refund is linked append-only evidence.
- Attribution tests: every debit traces billing account, organization, business tenant, capability/operation, job, usage event, pricing version, amount, reservation/policy versions, actor, and correlation.
- Block tests: a funded account and permissive organization policy cannot execute a blocked capability or bypass authorization/data/science/security/environment gates.

## Reconsideration trigger

Reconsider when authoritative payment/funding/accounting policy arrives, multiple billing accounts per customer are required, organization billing transfer is required, actual concurrent load makes serialized balance/policy reservation a measured bottleneck, an external billing/ledger product is mandated, or a service-extraction trigger under ADR-003 passes.

## Supersedes / superseded by

ADR-018 refines ADR-017's hierarchy by adding a commercial owner/customer billing boundary above organizations while preserving business as the data tenant and organization as the capability/policy scope. It refines ADR-008/Stage 12 usage, quota, audit, and privileged-action contracts and C05-04/C05-18 without weakening any block or adding a deployable. It does not authorize payment processing, production billing, or organization wallets. Superseded by: none.
