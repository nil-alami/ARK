# Sponsor decision — owner billing account and organization credit policies

Date received: 2026-08-15

Authority: explicit ARK sponsor decision supplied in the active Codex task after ADR-017.

## Sponsor-provided product facts

- Credits belong to an owner/customer billing account, not to organizations.
- One commercial customer may operate several organizations. The shared billing account prevents constant movement of money or credits between organization wallets.
- Organizations receive consumption policies, not balances. ARK must not create multiple organization wallets beneath the owner account.
- Example: one billing account has 500,000 credits. Organization A has a 100,000 monthly policy, Organization B has a 250,000 monthly policy, and Organization C has an unlimited organization policy. All still consume from the same 500,000-credit pool.
- Credits flow through `owner billing account → organization spending policy → business usage → capability usage → job`.
- A debit must identify who paid, which organization consumed it, which business tenant caused it, which AI capability caused the charge, and which job/usage/pricing version produced it.

## Required debit attribution

```text
{
  billing_account_id
  organization_id
  business_id
  capability
  job_id
  usage_event_id
  pricing_version
  amount
}
```

## Organization credit policy

```text
OrganizationCreditPolicy
------------------------
organization_id
billing_account_id
monthly_limit
daily_limit
per_job_limit
hard_limit
warning_threshold
effective_from
effective_to
```

An explicit `NULL` limit may mean that the organization consumes from the owner's shared pool without an organization-specific ceiling.

## Required request-gate order

```text
Request
  → Authentication
  → Resolve business
  → Resolve organization
  → Authorization for the business
  → Organization capability pattern
  → Dataset validation
  → Capability eligibility
  → Organization credit policy
  → Owner billing-account balance
  → Reserve credits
  → Execute
```

There are two separate financial checks, and both must pass: the organization policy check and the owner billing-account balance check.

## Still unspecified by the sponsor

- How credits are purchased, granted, refunded, expired, adjusted, or converted from money.
- Exact pricing formulas, units, rounding, currency/tax/accounting treatment, and who approves pricing versions.
- Daily/monthly window boundaries and time zone.
- Exact meaning and type of `hard_limit` when it is not enforcing a denial, and exact warning-delivery behavior.
- Charging rules for cancellation, partial execution, failed jobs, retries, provider ambiguity, or actual cost above reservation.
- Whether one commercial customer may ever require multiple billing accounts or whether organizations may transfer between billing accounts.

Architectural interpretations, fail-closed defaults, reservation/settlement constraints, and production-admission consequences are recorded in ADR-018.
