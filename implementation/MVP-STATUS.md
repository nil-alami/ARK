# ARK Reference MVP status

Overall state: `IMPLEMENTED PRE-ADR-017 — REVISION_REQUIRED`

Last updated: 2026-08-15

Decision authority remains the human ARK sponsor under accepted ADR-016. This status records implementation evidence only; it does not approve the MVP for production or clear any existing admission block.

ADR-017 and ADR-018 were accepted after the implementation evidence below was produced. The code still uses a simplified direct credential→tenant fixture and does not implement account→organization→business membership, uniform capability patterns, organization-scoped admin behavior, a shared owner credit pool, organization credit policies, or reservation/settlement. See `docs/mvp/ADR-017-IMPACT.md` and `docs/mvp/ADR-018-IMPACT.md`. Existing evidence remains historical and must not be used as conformance evidence for either ADR.

## Current implementation

- Local Python/Gradio Blocks application: implemented.
- Deterministic synthetic retail fixture, seed 42: implemented.
- Single-process runtime with explicit module boundaries: implemented.
- SQLite runs, jobs, quarantine rows, trace events, and results: implemented.
- Event-driven vertical pipeline, activity timeline, metrics, stage drill-down, and final results: implemented.
- Successful Recommendation scenario: implemented and smoke-tested.
- Invalid-row quarantine with degraded continuation: implemented and smoke-tested.
- Browser-rendered happy-path and degraded-path visual checks: passed.

The latest implementation mandate intentionally narrowed the runnable demo to exactly two scenarios. The previously planned hard-ineligibility, retry, delivery-failure, and stored-replay UI scenarios remain unimplemented and are recorded in `DEFERRED.md`.

## Verification evidence

| Check | Result |
|---|---|
| Python compile check | pass |
| Smoke suite | 3 tests passed |
| Successful scenario | 216 input, 216 valid, 0 quarantined, 72 recommendations, 54 events |
| Degraded scenario | 220 input, 216 valid, 4 quarantined, 72 recommendations, 54 events |
| Persisted job state | `succeeded`, one attempt |
| Result persistence | one stored result payload per run |
| UI startup | `http://127.0.0.1:7860` served successfully |
| Visual/interaction QA | both scenarios and validation-stage drill-down passed |

## Classification boundary

Functional: deterministic transformation, schema validation, quarantine, normalization, feature/candidate/ranking logic, job transitions, SQLite persistence, trace history, and persisted-result retrieval.

Simplified: tenant context, entitlement, data receipt, readiness/eligibility policies, queue/worker separation, Recommendation science, audit closure, and UI delivery.

Postponed: production trust and IAM, external ingestion/delivery, distributed execution, real model lifecycle, multi-capability flows, production observability, scale, resiliency, deployment, and scientific validation.

Required revision: account/organization/membership/business fixture records, business-level tenant propagation, versioned uniform capability pattern, organization-wide admin/pattern change behavior, inactive viewer/tester denial, cross-scope/pattern-race tests, and updated UI/evidence.

Additional ADR-018 revision: one synthetic shared owner balance, organization policies rather than wallets, immutable pricing, dual financial gate, atomic reservation+job acceptance, idempotent settlement/release, complete charge attribution, concurrency/recovery tests, and explicit `CREDIT_BILLING_ADMISSION_BLOCKED` labeling.

## Active blocks

All production and migration blocks in the final design remain active. The MVP uses the explicit fixture-only marker `POA_FIXTURE_ONLY`; it is an executable architectural hypothesis, not a production decision.
