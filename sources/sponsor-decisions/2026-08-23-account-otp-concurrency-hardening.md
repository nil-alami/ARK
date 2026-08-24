# Sponsor implementation addendum — Account OTP concurrency hardening

Date: 2026-08-23

Status: `AUTHORITATIVE SPONSOR-SUPPLIED IMPLEMENTATION UPDATE — REQUIRES PUBLICATION RECONCILIATION AND RE-ASSURANCE`

Source: explicit sponsor report in the Codex task, corroborated by the current
working tree of the sibling `ark` implementation repository.

This addendum supplements, and does not rewrite,
`sources/sponsor-decisions/2026-08-23-account-registration-redesign-implementation.md`.

## Implemented concurrency behavior

1. OTP challenge creation is serialized with a PostgreSQL advisory transaction
   lock before the resend decision and replacement write. Registration uses a
   phone-scoped lock; login/profile verification uses a purpose-and-phone-scoped
   lock.
2. While holding that transaction lock, a replacement challenge invalidates
   every previous live challenge in the same scope before inserting the new
   challenge. Concurrent resend requests therefore cannot leave two usable OTPs.
3. Attempt accounting no longer performs a separate eligibility read followed
   by an increment. Account reserves one attempt with a single conditional
   database update that simultaneously requires the challenge to be unconsumed,
   not invalidated, unexpired, and below its maximum-attempt limit.
4. Registration, login, and profile confirmation consume only a still-live
   challenge. Login and profile consumption explicitly reject challenges whose
   `invalidated_at` value is set.

## Delivery and persistence hardening

1. OTP challenge state is committed before the SMS delivery boundary is called.
2. Delivery success or failure is recorded on the persisted challenge.
3. A recorded delivery failure preserves pending state and permits an immediate,
   safe retry; the normal resend delay still applies after a recorded send.

## Database integrity guard

Migration `apps/backend/migrations/versions/20260823_06_otp_challenge_guards.py`
adds the `ck_otp_hash_length` constraint to `account."OtpChallenges"`. Every
stored `OtpHash` must be exactly 32 bytes, matching the HMAC-SHA-256 persistence
contract.

## Evidence boundaries and required reconciliation

- The implementation evidence includes the Account PostgreSQL store, table
  metadata, migration `20260823_06`, and Account authentication tests.
- Advisory locking is a PostgreSQL implementation mechanism inside the accepted
  modular-monolith deployment direction; it does not select a new component.
- This hardening does not select a production SMS provider, prove distributed
  abuse-control sufficiency, or clear `CRYPTO_SECRETS_BLOCKED`,
  `EXTERNAL_DELIVERY_BLOCKED`, or any other production-admission block.
- The pending identity/Account ADR and affected publication reliability,
  security, interface, execution-flow, testing, and data-contract text must
  reconcile these invariants before Stage 24 re-assurance can pass.
