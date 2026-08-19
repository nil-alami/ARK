# Stage 23 — Anti-overengineering test and publication

Governing source: `system-design-prompt.md` section **Anti-overengineering test**.

Inputs: all completed stages, ADRs, traceability, diagrams, and runtime analysis.

## Work

- Challenge every proposed component using every question in the governing section.
- Classify each component as required now, useful soon, scale-triggered, optional, or unjustified.
- Remove unjustified elements and repair every affected stage, diagram, contract, ADR, flow, roadmap, and traceability entry.
- Ask `assurance_reviewer` for an independent component challenge before publishing.
- Assemble the eight required files listed in `WORKFLOW.md` from approved durable artifacts.
- Complete `quality/source-instruction-coverage.md` and `quality/final-acceptance-checklist.md` provisionally.

Output: the complete set under `outputs/final/`.

Gate: explicit user approval of the publishable design; no “final” claim until Stage 24 independently passes.
