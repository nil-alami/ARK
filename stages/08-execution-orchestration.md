# Stage 08 — Execution and orchestration

Governing source: `system-design-prompt.md` section **7. Execution and orchestration**.

Inputs: Stages 05–07 and capability execution profiles.

## Work

- Design immediate inference, durable inference, training, schedules, batch, events, continuous processing only if justified, and multi-capability workflows.
- Specify cancellation, retries, timeouts, partial failure, compensation, priority, concurrency, duplicates, and delivery semantics.
- Distinguish API gateway, job manager, scheduler, queue, worker, workflow orchestrator, event broker, event handler, and notification delivery.
- State PostgreSQL-first job semantics and measurable triggers for a broker or workflow engine.

Output: `outputs/stages/08-execution-orchestration.md`.

Gate: state machine, retry/idempotency boundary, ownership, and worker routing are implementable; no vague “event system” remains.
