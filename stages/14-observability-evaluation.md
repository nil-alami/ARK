# Stage 14 — Observability and evaluation

Governing source: `system-design-prompt.md` section **13. Observability and evaluation**.

Inputs: Stages 02–13.

## Work

- Define logs, metrics, traces, correlation, health, dashboards, alerts, audit, tenant usage, model/data quality, cost, and agent traces if applicable.
- Identify essential inline instrumentation versus asynchronous export.
- Separate operational observability from mandatory audit and compliance records.
- Define SLIs; propose SLOs only where evidence is sufficient, otherwise define measurement plans.
- Use platform and data/ML specialists for non-overlapping signal sets.

Output: `outputs/stages/14-observability-evaluation.md`.

Gate: every component and critical workflow has owner-relevant signals, correlation fields, alert conditions, and failure behavior for telemetry outages.
