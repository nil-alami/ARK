# Sponsor decision — Organization-wide Member access and capability pattern

Date: 2026-08-18

Status: `AUTHORITATIVE SPONSOR DECISION — REQUIRES ARCHITECTURE RECONCILIATION`

Source: explicit sponsor clarification in the Codex task following the Phase 1
identity and function-contract work.

## Decisions

1. An active Member of an Organization is eligible, subject to the Member's one
   selected Role and its Permissions, to operate on every current and future
   Business belonging to that Organization.
2. ARK does not select or assign individual Businesses to Members in the initial
   design. There is no `MemberBusinessAccess` entity, grant, allowlist, or
   per-Business Member exception.
3. A Member receives no authority merely from supplying a Business identifier.
   Each operation must derive the Organization from trusted Member context, load
   the requested Business, and verify that the Business belongs to that
   Organization.
4. Role Permissions continue to constrain actions. Organization-wide Business
   reach does not grant `data.read`, `data.ingest`, `business.manage`, capability
   execution, billing, or any other action absent from the selected Role.
5. Every Business data or execution operation remains explicitly scoped to one
   Business. Organization-wide Member reach does not authorize cross-Business
   aggregation, combined datasets, bulk export, or unscoped reads.
6. Each Organization has one versioned enabled-capability pattern. The same
   pattern applies to every current and future Business in the Organization.
7. There are no per-Business capability enablement overrides, exceptions, or
   selected-Business entitlement grants in the initial design.
8. Adding a capability to the Organization pattern grants configuration
   eligibility only. It does not bypass Business status, Role Permission, quota,
   data readiness, scientific eligibility, model assignment, environment,
   security, or production-admission checks.
9. Removing a capability denies new submissions for every Business in the
   Organization. Accepted/running work follows the approved cancellation and
   finalization policy, and committed history remains preserved.

## Tradeoff explicitly accepted

The Organization is the administrative trust boundary for Member reach. A Role
Permission such as `data.read` or `data.ingest` therefore applies across all of
the Organization's Businesses. This intentionally simplifies administration but
increases compromise and misassignment blast radius as the Business count grows.
The Role catalog, one-Business-per-request scope, audit, and Organization-to-
Business validation are mandatory compensating controls.

## Supersession and reconciliation

This decision resolves the open Phase 1 question of whether ordinary Members
need per-Business grants: they do not. It preserves ADR-017's existing uniform
Organization capability pattern and makes the all-Business Member rule explicit
for every Role, not only the organization-admin example.

The decision clears no production-admission block. The pending identity ADR and
affected interface, authorization, testing, and publication artifacts must
reconcile it before independent assurance.
