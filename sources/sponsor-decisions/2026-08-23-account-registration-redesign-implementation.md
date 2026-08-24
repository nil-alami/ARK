# Sponsor implementation update — Account registration redesign

Date: 2026-08-23

Status: `AUTHORITATIVE SPONSOR-SUPPLIED IMPLEMENTATION UPDATE — REQUIRES PUBLICATION RECONCILIATION AND RE-ASSURANCE`

Source: explicit sponsor report in the Codex task, corroborated by the current
working tree of the sibling `ark` implementation repository.

## Module identity

The module is named **Account**. Earlier references to the same module as **IAM**
are legacy terminology and must not be used as the current module name. Historical
source quotations and accepted ADR rationale may retain the old term where changing
it would rewrite history.

## Implemented registration controls

| Control | Implemented behavior |
|---|---|
| OTP expiry | 5 minutes |
| Resend delay | 60 seconds; immediate retry after a recorded delivery failure |
| Request limits | 5 per phone per 15 minutes; 100 per requester IP per 15 minutes |
| Attempt limit | 5; exhaustion sets `OTP_EXHAUSTED` while the registration remains resumable |
| Single use | OTP consumption and activation occur atomically |
| OTP storage | Only a challenge-scoped HMAC-SHA-256 digest is stored; plaintext is never persisted |

## Implemented registration behavior

1. Registration validates and normalizes full name, phone, email, city,
   registration type, and invitation fields.
2. Registration does not accept a password.
3. No `User` row is stored until the OTP succeeds.
4. Authoritative registration data remains server-side. The browser stores only
   an opaque, tab-scoped registration-session ID.
5. SMS delivery failure is recorded while registration remains pending and
   resumable.
6. An identical pending registration is reused after a lost API response.
7. Starting a newer registration for a phone supersedes the older attempt and
   invalidates its OTP.
8. One transaction creates or resolves the User, verifies the phone, consumes
   the OTP, completes the registration, and issues the first session.
9. A newly created User has `PasswordHash = NULL`. Account exposes a dedicated
   authenticated password setup/change form and endpoint.
10. Normal profile editing treats phone as read-only; a future phone-change flow
    must separately prove the new number.
11. Expired and terminal temporary registration records are cleaned up.

## Evidence boundaries and required reconciliation

- The sponsor-supplied implementation state is represented by the Account
  migration, application/store code, API contracts, frontend registration-session
  handling, automated tests, `docs/adr/0006-pending-registration-activation.md`,
  and `docs/domain/user-authentication-workflows.md` in the implementation repository.
- This update supersedes registration/password-at-registration behavior in the
  earlier Phase 1 Account/IAM documentation. It does not supersede unrelated
  User, Member, Role, Permission, API-key, Organization, or audit decisions.
- Recording implemented behavior does not select a production SMS provider,
  approve production secret management, clear abuse-control gaps, or clear any
  accepted ADR-008 production-admission block.
- The pending identity ADR and the eight publication artifacts must reconcile
  the Account name, human registration trust flow, temporary-state ownership,
  activation transaction, profile phone immutability, password-null lifecycle,
  failure behavior, tests, and diagrams before Stage 24 re-assurance can pass.
