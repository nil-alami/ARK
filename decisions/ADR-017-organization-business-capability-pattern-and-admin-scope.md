# ADR-017 — Organization/business hierarchy, capability pattern, and admin scope

Status: `ACCEPTED`

Date: 2026-08-15

Decision owner: ARK sponsor (human user), through the explicit decisions recorded in `sources/sponsor-decisions/2026-08-15-owner-organization-business.md`

## Context and requirements

The completed ARK design used one opaque `tenant_id` for tenant-bearing assets but intentionally left the concrete customer hierarchy and role bindings unresolved. The sponsor has now supplied a product hierarchy: a registered owner can create multiple organizations, each organization contains businesses, and one organization-wide ARK capability pattern applies to all of its businesses. The sponsor also approved organization-wide admin access and authorized an organization admin to change that pattern.

The design must preserve ADR-008's principal-derived, deny-by-default tenant isolation. In particular, an organization-wide administrator must not turn a caller-supplied business identifier into authority, accidentally authorize unbounded cross-business data access, or make an enabled but production-blocked capability executable.

The product term **organization owner** is distinct from an ARK **module/state owner**, the human **ARK sponsor**, and named security/data/scientific/operations authorities. An organization owner receives no architectural approval or production-admission authority by implication.

## Decision

1. ARK uses the hierarchy `account → organization membership → organization → business`.
2. A registered account profile stores at least full name and phone number. Additional profile fields, verification, uniqueness, credentials, recovery, and identity-provider behavior remain unresolved and production trust remains `EXTERNAL_TRUST_BLOCKED`.
3. An account may own one or more organizations. An organization owns zero or more businesses while being configured; every active business belongs to exactly one organization at a time.
4. A business is ARK's tenant/data-isolation unit. Its opaque `business_id` is the effective `tenant_id` on datasets, jobs, results, models/assignments, objects, events, usage, audit, and other business-bearing assets. An organization is the administrative and entitlement container; it is not a shared business-data namespace.
5. Organization membership is the authority source for organization actions. The authenticated subject and stored active membership are validated before ARK derives an organization scope. For a business operation, ARK additionally loads the business, verifies that it belongs to the authorized organization, and derives the business tenant scope. A request path/body/header ID remains a lookup key and never establishes authority.
6. Each organization has one versioned capability pattern containing the enabled capability allowlist. The same pattern applies to every current and future business in that organization; there are no per-business capability exceptions in the initial design.
7. An organization admin may read and change the organization's capability pattern. Pattern mutation requires canonical capability IDs, optimistic version/ETag protection, idempotency, immutable audit of old/new patterns and actor, and a new pattern version/effective time.
8. Capability admission checks both organization pattern eligibility and every existing platform, data, scientific, model, environment, policy, quota, and production-admission gate. Adding RFM, Churn, NPT, REC, or another capability to a pattern grants no scientific or production admission and clears no block.
9. New submissions pin the effective pattern version. A removed capability is denied for new work and rechecked before an unstarted attempt executes. Previously committed results are not erased; accepted/running work follows the existing cancellation, finalization, and reconciliation contracts.
10. The implemented admin role is organization-scoped: an admin of Direct is authorized across all Direct businesses. Each business-data command/query still carries one explicit derived business scope. Cross-business aggregation, bulk export, or combined datasets require a separately typed, authorized, audited contract and are not implied by the admin role.
11. `viewer` and `tester` are reserved role names only. They remain unavailable/fail-closed until exact permissions, prohibited combinations, tests, and activation authority are approved. Whether admins may manage other admin memberships remains unresolved; until decided, only an organization owner may grant or revoke admin membership.
12. Direct is the canonical example: Andrew's account owns the Direct organization; Direct may register approximately 1,000 business tenants; one Direct capability pattern such as `{RFM, Churn}` governs all of them; a Direct admin may change that pattern and has organization-wide administrative reach without receiving implicit cross-business data-combination authority.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| Organization is the tenant and businesses are unisolated children | Smallest apparent context | Weakens business isolation and makes one compromised business context expose all organization data | Rejected | Only a sponsor decision plus data/security evidence proving business isolation unnecessary |
| Business is the tenant; organization supplies administration and uniform entitlement | Preserves existing tenant controls and supports Direct's 1,000 businesses | Requires validated organization→business derivation and explicit cross-business contracts | Selected | Revisit only if a different authoritative tenancy model is approved |
| Per-business capability overrides | Flexible exceptions | Contradicts the sponsor's same-pattern rule and adds precedence/audit complexity | Rejected initially | Sponsor explicitly requires exceptions and approves precedence semantics |
| Separate organization/IAM/policy microservice now | Physical isolation and independent administration | Adds deployment, failure, migration, and operating burden without evidence | Rejected | ADR-003 extraction trigger or measured policy administration burden |

## Rationale

The selected hierarchy is the smallest refinement that represents the sponsor's product model while preserving the already accepted security boundary. Existing trust/context and control modules can own accounts, memberships, organizations, businesses, and capability-pattern records in their owned PostgreSQL schemas. Business-level tenant keys continue to protect computation and data assets; organization membership supplies only the administrative scope needed to reach those tenants.

## Consequences and trade-offs

- `AuthContext` gains organization membership/scope and an optional derived business scope; background jobs remain bound to exactly one business tenant.
- The control plane gains versioned account, organization, membership, business, and capability-pattern contracts, but no new deployable component.
- Organization-wide administration requires efficient business listing and negative tests across organizations, while avoiding generic cross-business reads.
- Full name and phone number are now explicitly required account PII. They require classification, minimization, access, audit, retention/deletion, and redaction policies; unspecified registration fields cannot be invented.
- Capability discovery and invocation become organization-pattern aware. A pattern is entitlement, not capability readiness or production admission.
- Existing production blocks remain active. This decision does not activate a real capability, external caller, source contract, or production environment.

## Implementation constraints

- Minimum logical records: `AccountProfile`, `Organization`, `OrganizationMembership`, `Business`, and `OrganizationCapabilityPattern` with immutable IDs, status, versions, timestamps, and audit references.
- Enforce one active organization membership identity per subject/organization relationship and one active organization parent per business. Business moves require a future explicit transfer contract; direct parent mutation is prohibited.
- Pattern contents use registered immutable capability IDs, never display names. Unknown, unavailable, or blocked capabilities may be represented for configuration visibility but must fail execution admission with a precise reason.
- Organization control operations use `organization_id`; business data/execution operations require a derived `business_id`/`tenant_id`. Background delegation pins subject origin, organization, business tenant, membership/pattern versions, job/attempt/fence, and purpose.
- Pattern changes and admin grants/revocations require mandatory audit before effect. If membership, pattern, or audit truth is unavailable, the action fails closed.
- Do not add an IAM product, policy engine, microservice, hierarchy service, or cross-business data mart solely for this decision.

## Validation evidence

- Contract tests: create multiple organizations for one account; register many businesses; apply one pattern to current and newly created businesses; reject per-business pattern overrides.
- Authorization tests: an admin can list and administer every business in its organization and change its pattern; the same admin cannot access another organization or derive authority from forged IDs.
- Isolation tests: every capability/data/job/result/object operation resolves to exactly one business tenant; organization-wide membership alone cannot run an unscoped business-data operation or aggregate/export businesses.
- Pattern tests: canonical IDs, ETag/CAS, idempotent replay, concurrent update conflict, old/new audit, removal before execution, pinned version lineage, and blocked-capability denial.
- Role tests: admin is active and organization-scoped; viewer/tester and admin-membership management by admins remain denied until separately approved.
- PII tests: full name/phone never enter logs, telemetry, object keys, capability inputs, or business tenant identity by default.

## Reconsideration trigger

Reconsider when the sponsor requires business-specific capability exceptions, cross-business datasets/analytics, business transfer, multiple organization owners/ownership transfer, admin-managed admin membership, active viewer/tester semantics, or a measured scale/ownership/security trigger qualifies a separate service or policy product.

## Supersedes / superseded by

ADR-017 narrows and refines ADR-008's single `tenant_id` context into an organization-membership administrative scope plus a business-level tenant/data scope. It preserves ADR-008's principal-derived authority, owner-module checks, isolation, audit, and every production block. It refines ADR-004/015 interface context without changing REST/JSON or typed-port choices, and refines C05-03/C05-04/C05-20 without adding a component. It does not supersede ADR-016's architecture-accountability limits. Superseded by: none.
