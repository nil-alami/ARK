# Stage 17 — Capacity, performance, and cost

Governing source: `system-design-prompt.md` section **16. Capacity, performance, and cost**.

Inputs: Stages 02–16 and all known workload evidence.

## Work

- Build a symbolic or range-based capacity model when exact values are unknown.
- Cover tenants, requests, data, batches, jobs, events, storage, model memory, CPU/GPU, latency, and cost drivers.
- Separate measured facts, estimates, and assumptions.
- Define benchmarks and measurements required before infrastructure commitments.
- Use platform and data/ML specialists for independent workload dimensions.

Output: `outputs/stages/17-capacity-cost.md`.

Gate: no fabricated precision; every estimate shows formula, input status, sensitivity, bottleneck, and scale trigger.
