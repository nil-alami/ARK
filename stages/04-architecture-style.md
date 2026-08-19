# Stage 04 — Architecture drivers and style

Governing source: `system-design-prompt.md` section **3. Architecture drivers and style**.

Inputs: Stages 02–03 and assumptions.

## Work

- Compare the listed architecture styles against actual drivers, team maturity, and known scale.
- Recommend one starting style and define module boundaries, acceptable coupling, mandatory isolation, shared infrastructure, forbidden sharing, and extraction triggers.
- Treat the declared microservice-ready modular monolith as baseline evidence; surface any reason to supersede it.
- Ask `platform_architect` for an independent fit analysis.
- Create the architecture-style ADR.

Output: `outputs/stages/04-architecture-style.md` and `decisions/ADR-001-architecture-style.md`.

Gate: explicit user approval of the starting style and boundary principles.
