# Stage 18 — Architecture decisions

Governing source: `system-design-prompt.md` section **17. Architecture decisions**.

Inputs: Stages 02–17 and existing ADRs.

## Work

- Create the complete ADR table required by the prompt.
- Ensure dedicated decisions cover every comparison explicitly named in the governing section.
- Create one file per material decision from `templates/adr.md`; link superseded decisions rather than deleting them.
- Include status and measurable reconsideration trigger.
- Ask `assurance_reviewer` to challenge missing alternatives and unsupported choices.

Output: `outputs/stages/18-architecture-decisions.md` and files under `decisions/`.

Gate: explicit user approval of decisions that constrain implementation; provisional decisions remain visibly provisional.
