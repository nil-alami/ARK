# ADR-018 impact on the ARK Reference MVP

Status: `DOCUMENTED GAP — IMPLEMENTATION NOT YET REVISED`

Date: 2026-08-15

The runnable Reference MVP has no owner billing account, organization credit policy, pricing version, credit reservation, or append-only charge ledger. Its existing entitlement/usage seams are not ADR-018 conformance evidence.

## Required MVP revision

After the ADR-017 hierarchy revision, the next bounded implementation must add:

1. One synthetic owner/customer billing account shared by at least two fixture organizations.
2. A synthetic append-only credit ledger and reconstructable available-balance projection.
3. One effective versioned `OrganizationCreditPolicy` per organization, with explicit null, zero, daily/monthly/per-job, warning and hard-denial fixtures.
4. Immutable synthetic pricing versions and a bounded pre-execution reservation estimate.
5. Both organization-policy and shared owner-balance checks after pattern/data/capability admission.
6. One coordinated reservation+durable-job acceptance transaction; no reservation orphan and no executable unreserved job.
7. Exactly-once settlement by stable `usage_event_id`, unused-reservation release, append-only adjustment/reversal links, and full billing→organization→business→capability→job attribution.
8. Parallel multi-organization tests proving no shared-balance overspend and no organization-policy overspend.
9. Retry, replay, response-loss, crash, cancellation, finalization, ledger-outage, restore and reconciliation tests proving no duplicate charge.
10. Negative proof that a funded account/permissive policy cannot bypass authorization, capability pattern, readiness, eligibility, or any production block.

## Explicit non-goals

- No payment processor, real money, currency, tax, invoice, purchase flow, or accounting integration.
- No organization wallets, child balances, or credit transfer workflow.
- No invented production price, window time zone, funding/expiry/refund, partial-failure charge or billing-role policy.
- No billing microservice, distributed ledger or third-party billing product.

## Evidence effect

The current MVP may not display a real-looking balance or charge. All fixture credits/prices must be labeled synthetic and `POA_FIXTURE_ONLY`. `CREDIT_BILLING_ADMISSION_BLOCKED` remains active even after local tests pass; only authoritative commercial/accounting rules and named human authority can clear it.
