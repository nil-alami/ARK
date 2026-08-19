# Contract for every workflow stage

## Before execution

1. Confirm every dependency is complete in `STATUS.md`.
2. Read the governing section of `sources/normalized/system-design-prompt.md` exactly as written.
3. Read all required earlier outputs and relevant source files in full.
4. State what is known, what is assumed, and what remains missing.
5. If the stage authorizes subagents, give each a bounded read-only task and wait for all findings.

## Required stage output structure

Use `templates/stage-output.md`. Include source citations as `file path — section heading`; do not use unsupported claims.

For every major recommendation include:

- requirement satisfied;
- exact stage/workflow where used;
- why needed now;
- simplest viable implementation;
- alternative considered;
- why the alternative is not preferred;
- trade-offs and operational burden;
- measurable reconsideration trigger.

## Completion gate

A stage passes only when:

- every bullet in the governing source section is addressed or explicitly marked not applicable with a reason;
- every material statement is classified as fact, assumption, recommendation, decision, or unresolved question;
- contradictions are visible;
- traceability is updated;
- no later-stage decision is smuggled in without being labeled provisional;
- the output includes downstream consequences and exact next inputs;
- the stage-specific gate passes.

If the gate fails, keep the stage `IN_PROGRESS`; do not advance `STATUS.md`.

## After execution

1. Save the stage output.
2. Create or update ADRs for material decisions.
3. Update `STATUS.md` with completed stage, next stage, blockers, decisions, and invalidated downstream work.
4. Stop if `WORKFLOW.md` requires approval.
