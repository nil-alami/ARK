# Sponsor decision — User, Member, Role, Permission, and API-key identity model

Date: 2026-08-18

Status: `AUTHORITATIVE SPONSOR DECISION — REQUIRES ARCHITECTURE RECONCILIATION`

Source: explicit sponsor decisions in the Codex task that requested revision of
`tests/phase_1_docs/level_1.md`.

## Decisions

1. The current identity/access entity set is `Users`, `Organizations`, `Roles`,
   `Permissions`, `Members`, and `APIKeys`.
2. There is no physical `principals` table and no generic `credentials` table in
   this model. Existing Phase 1 references to those tables/concepts are to be
   removed. This does not remove the requirement for a trusted actor context.
3. The former `owners` table is replaced by `users`; each User has an immutable
   `id`.
4. A Member links a User to an Organization and contains `user_id`,
   `organization_id`, and exactly one `role_id`.
5. The sponsor explicitly declined a database uniqueness constraint on
   `(user_id, organization_id)`. A User may have Member records associated with
   multiple Organizations.
6. Roles and Permissions are predefined and managed by ARK developers. They are
   versioned. Organization owners may select an available Role for a Member but
   cannot define Roles or edit their Permission mappings.
7. An API key is assigned to one Member of one Organization. One Organization may
   have multiple Members and each Member may have multiple API keys.
8. API-key records include immutable identity and organization/member binding,
   non-secret lookup material, a stored hash rather than the raw key, rotation
   lineage, usage/expiry/revocation timestamps, lifecycle status, integrity
   constraints, and indexes required for lookup and administration.
9. Audit events distinguish `USER`, `API_KEY`, and `SYSTEM` actors and record the
   applicable organization/member context, action, target, result, and request.

## Explicit boundary and unresolved item

- Removing a physical `principals` table does not authorize caller-supplied actor,
  organization, Member, or Business identifiers. The runtime must still derive a
  trusted actor and tenant context.
- The exact authentication mechanism for human Users remains unresolved.
- The exact deployment-managed identity mechanism for schedulers and workers
  remains unresolved. `SYSTEM` audit attribution alone is not authentication.
- This decision does not clear `EXTERNAL_TRUST_BLOCKED`,
  `CRYPTO_SECRETS_BLOCKED`, `PRIVILEGED_ACTION_BLOCKED`, or any other accepted
  production-admission block.

## Required reconciliation

The accepted architecture and publication artifacts that use `principal`, generic
credential, account/owner, membership, role-assignment, trusted-context, workload
identity, or audit terminology must be checked against this decision before the
pending independent assurance can pass. A later ADR must state whether legacy
`principal` language is renamed to this concrete entity model or retained only as
an abstract actor term.
