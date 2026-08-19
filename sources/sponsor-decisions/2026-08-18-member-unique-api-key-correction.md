# Sponsor correction — One current API key per Member

Date: 2026-08-18

Status: `AUTHORITATIVE SPONSOR DECISION — REQUIRES ARCHITECTURE RECONCILIATION`

Source: explicit sponsor correction in the Codex task following
`sources/sponsor-decisions/2026-08-18-user-member-api-key-identity.md`.

## Correction

The relationship `Member 1 ── N APIKey` is not the intended logical contract.
Each active Member has exactly one current active API key.

Rotation may retain revoked predecessor rows for immutable audit and
`rotated_from_api_key_id` lineage, but those historical rows are not additional
usable API keys. At most one API-key row for a Member may have `status = 'active'`.
Activation creates the Member and first API key as one application transaction.
Rotation atomically revokes the predecessor and inserts its successor. An active
key may otherwise be removed without replacement only when the Member is
suspended or revoked.

## Supersession

This correction supersedes only Decision 7 of
`sources/sponsor-decisions/2026-08-18-user-member-api-key-identity.md`, where it
said that each Member may have multiple API keys. All other decisions and
unresolved boundaries in that source remain unchanged.

This correction clears no production-admission block.
