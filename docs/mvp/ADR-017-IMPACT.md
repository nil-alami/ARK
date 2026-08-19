# ADR-017 impact on the ARK Reference MVP

Status: `DOCUMENTED GAP — IMPLEMENTATION NOT YET REVISED`

Date: 2026-08-15

ADR-017 was accepted after the current Reference MVP was implemented and evidenced. The runnable code still uses a simplified direct credential→`tenant_id` fixture and therefore does not demonstrate the newly approved product hierarchy or authorization behavior. Existing smoke/visual evidence remains valid only for the pre-ADR-017 fixture behavior.

## Required MVP revision

The next implementation change must add, inside the existing trust/context and control boundaries:

1. An `AccountProfile` fixture with at least full name and phone number, kept out of logs/telemetry/capability payloads.
2. At least two organizations and multiple businesses per organization.
3. Active organization memberships with `admin` implemented; `viewer` and `tester` fail closed.
4. Business as the effective tenant/data-isolation key on every existing run/job/object/result/event record.
5. One versioned capability pattern per organization, uniformly inherited by current and newly created businesses.
6. Owner/admin pattern updates with canonical capability IDs, ETag/CAS, idempotency, old/new audit, and effective version.
7. Submit-time and pre-execution pattern checks, without clearing any existing capability or production block.
8. Positive proof that a Direct admin can administer every Direct business and change Direct's pattern.
9. Negative proof for cross-organization access, forged organization/business IDs, unscoped business data operations, per-business pattern overrides, inactive viewer/tester, implicit cross-business aggregation/export, concurrent pattern changes, and capability removal before execution.

## Explicit non-goals

- No production registration, IdP, phone verification, credentials, recovery, or IAM product.
- No implementation of viewer/tester permissions.
- No admin-managed admin membership, ownership/business transfer, or cross-business data product.
- No new microservice, policy engine, or hierarchy service.
- No real RFM, Churn, NPT, REC, or Synapse production admission.

## Evidence effect

The current application may continue to run as a historical pre-ADR-017 demo, but it must not be cited as evidence that ADR-017 is implemented. `implementation/MVP-STATUS.md` remains `REVISION_REQUIRED` until the new schema/contracts/tests and browser-visible evidence pass. The revised publication's independent assurance is a separate documentation gate and cannot be satisfied by MVP tests alone.
