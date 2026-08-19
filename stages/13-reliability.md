# Stage 13 — Reliability and failure design

Governing source: `system-design-prompt.md` section **12. Reliability and failure design**.

Inputs: Stages 05–12.

## Work

- Analyze every critical failure named in the governing section against actual ARK flows.
- Apply timeout, retry, circuit breaker, idempotency, DLQ, degradation, fallback, recovery, reconciliation, and disaster recovery only where justified.
- Define partial-result and stale-data semantics explicitly.
- Define recovery ownership, replay boundaries, poison-message handling, and state reconciliation.
- Use `assurance_reviewer` for failure-path challenge.

Output: `outputs/stages/13-reliability.md`.

Gate: each critical path has a failure matrix with detection, containment, user-visible status, retry boundary, data consistency effect, recovery owner, and verification step.
