# Sponsor correction — snake_case database table and column identifiers

Date: 2026-08-24

Status: `AUTHORITATIVE SPONSOR DECISION — DOCUMENTATION RECONCILED; IMPLEMENTATION MIGRATION REQUIRED`

Source: explicit sponsor correction in the Codex task following the Account
registration and OTP-hardening documentation updates.

## Decision

1. Physical PostgreSQL table names use lowercase `snake_case`, for example
   `users`, `registration_sessions`, and `otp_challenges`.
2. Physical PostgreSQL column names use lowercase `snake_case`, for example
   `user_id`, `registration_session_id`, and `otp_hash`.
3. PostgreSQL schema names remain lowercase module namespaces such as `account`,
   `organizations`, and `audit`.
4. Index, constraint, sequence, and other generated identifier names should also
   use lowercase `snake_case` and should not embed PascalCase table names.
5. Python fields, SQLAlchemy keys, public request/response fields, and physical
   database identifiers should use the same snake_case spelling where they name
   the same concept. A casing-only mapping boundary is not desired.
6. Current conceptual documentation must use snake_case identifiers. Historical
   ADR text and operational SQL for a not-yet-migrated legacy schema may retain
   quoted PascalCase only when clearly labeled as historical or legacy.

## Supersession and implementation boundary

- This decision supersedes the identifier convention selected by implementation
  ADR 0003 and any current documentation rule requiring PascalCase tables or
  columns.
- It does not retroactively alter the factual contents of earlier checksum-pinned
  implementation reports, which describe the working tree as it existed when
  recorded.
- The current `ark` SQLAlchemy metadata and Alembic history still use quoted
  PascalCase physical identifiers. This task changes documentation only. A
  coordinated forward migration must rename tables, columns, constraints,
  indexes, sequences, foreign-key references, and dependent SQL before the
  implementation conforms.
- Until that migration is implemented and verified, the snake_case convention is
  the target contract and the existing database schema is a documented legacy
  compatibility gap. Do not partially mix both conventions in a deployed schema.
- This correction adds no component and clears no production-admission block.
