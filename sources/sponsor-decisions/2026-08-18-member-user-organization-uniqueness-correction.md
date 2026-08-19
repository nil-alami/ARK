# Sponsor correction — Member uniqueness within an Organization

Date: 2026-08-18

Status: `AUTHORITATIVE SPONSOR CORRECTION — REQUIRES ARCHITECTURE RECONCILIATION`

Source: explicit sponsor instruction in the Codex task to add
`UNIQUE (user_id, organization_id)` to Members and the related documentation.

## Corrected decision

1. `organizations.members` MUST enforce `UNIQUE (user_id, organization_id)`.
2. A User may still belong to multiple Organizations because each Organization
   has a different `organization_id`.
3. The constraint prevents more than one Member row for the same User in the same
   Organization, regardless of Member lifecycle status.
4. Duplicate and concurrent `add_member` requests for the same pair MUST resolve
   to the stable `MEMBER_ALREADY_EXISTS` contract error.

## Supersession and consequence

- This correction supersedes only Decision 5 of
  `sources/sponsor-decisions/2026-08-18-user-member-api-key-identity.md`.
- With the current terminal `REVOKED` state, a revoked User cannot be enrolled in
  the same Organization by inserting another Member row. A future re-enrollment
  workflow requires an explicitly approved restore or replacement-membership
  contract.
- This correction clears no production-admission block.
