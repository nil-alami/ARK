# Stage 22 — Runtime placement and execution-flow analysis

Governing source: the complete **Runtime placement and execution-flow analysis** section of `system-design-prompt.md`.

Inputs: Stages 05–21.

## Work

- For every architecturally significant component and workflow operation, explain when, where, why, trigger, prerequisites, invoker, frequency, critical-path status, and removal/movement effect.
- Classify execution as sequential blocking, sequential async, parallel with fan-in, parallel non-blocking, event-triggered, scheduled, conditional, or out-of-band.
- Separate critical path, background operations, operational side effects, observability, audit, and delivery.
- Produce all four required artifacts for every major use case using `templates/execution-flow.md`.
- Cover all eight use cases listed by the prompt; mark agentic flow not applicable only if Stage 11 rejected agents.
- Ask platform and data/ML specialists to analyze independent flows, then reconcile naming and dependencies.

Output: `outputs/stages/22-runtime-execution-analysis.md`.

Gate: serial/parallel decisions are justified by dependencies and consistency, synchronization points are explicit, and every required flow has table, dependency map, narrative, and Mermaid diagram.
