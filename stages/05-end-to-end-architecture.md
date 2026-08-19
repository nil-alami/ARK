# Stage 05 — End-to-end architecture

Governing source: `system-design-prompt.md` section **4. End-to-end architecture**.

Inputs: approved Stage 04 plus Stages 02–03.

## Work

- Evaluate every component named in the governing section; include only justified components and explicitly reject unnecessary ones.
- For each included component, complete `templates/component-spec.md`.
- Define control-plane, data-plane, capability, integration, and operational boundaries.
- Ask `platform_architect` and `data_mlops_architect` for independent non-overlapping analyses; reconcile them.
- Produce a component inventory classified as required now, useful soon, scale-triggered, optional, or unjustified.

Output: `outputs/stages/05-end-to-end-architecture.md`.

Gate: every proposed component has responsibility, interfaces, ownership, failure behavior, scaling, security, monitoring, simplest implementation, and requirement traceability.
