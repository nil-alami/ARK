# ARK system-design controller

This repository exists to produce one complete, implementable ARK system design from the authoritative sources in `sources/`.

## Mandatory startup

Before architecture work, read in full:

1. `WORKFLOW.md`
2. `STATUS.md`
3. `SOURCE_MANIFEST.md`
4. `stages/STAGE-CONTRACT.md`

Then execute only the next incomplete stage in `WORKFLOW.md`. Read that stage file and every input it names. Never skip, merge, or reorder stages.

## Source authority

Use this precedence when sources conflict:

1. Explicit user decisions recorded in `decisions/` after this package was created.
2. `sources/normalized/ark-assumptions.md` for declared ARK decisions.
3. `sources/normalized/system-design-prompt.md` for process, required analysis, and deliverable shape.
4. Individual files in `sources/normalized/service-cards/` for capability-specific facts.
5. Temporary assumptions, always labeled and recorded.

Never silently resolve a conflict. Record it in `outputs/stages/00-source-audit.md` or the current stage's contradiction section. Preserve source wording and cite `path + section heading` for material facts and decisions.

Do not modify files under `sources/original/` or `sources/normalized/`. New evidence belongs in a new source file plus an updated manifest.

## Sequential workflow rules

- Stage outputs are durable project state, not disposable notes.
- A later stage must consume approved earlier outputs; it must not regenerate them from memory.
- Each stage must pass its completion gate before `STATUS.md` advances.
- If a blocking decision requires the user, stop after writing the question, alternatives, effect, and recommended temporary assumption.
- If the user cannot answer, use a clearly labeled temporary assumption only when the system-design prompt permits it.
- Never claim the ARK design is complete while a required capability lacks a service card unless the user has explicitly marked that capability out of scope or approved assumption-based treatment.
- Do not invent traffic, tenant counts, SLOs, budget, compliance duties, availability targets, or deployment constraints.
- Separate facts, assumptions, recommendations, approved decisions, and unresolved questions in every output.
- Apply the anti-overengineering test to every proposed component. Completeness means every required concern was evaluated, not that every possible product was added.

## Subagent policy

Use project-scoped agents in `.codex/agents/` only when `WORKFLOW.md` or the current stage authorizes them.

- Subagents are read-only evidence gatherers and reviewers.
- The primary agent is the only writer of authoritative stage outputs, ADRs, status, and final documents.
- Parallelize only independent analyses. Preserve sequential dependencies between stages.
- Give each subagent a bounded task, required inputs, required return structure, and explicit exclusions.
- Wait for all requested subagents, reconcile disagreements against source evidence, and record the resolution.
- Do not ask two agents to produce competing full-system designs.

## Output discipline

Every stage output must use `templates/stage-output.md` and include:

- stage purpose and source coverage;
- facts, assumptions, recommendations, decisions, contradictions, and open questions;
- requirement-to-design traceability updates;
- completeness-gate evidence;
- downstream consequences;
- exact next-stage inputs.

Record material architectural decisions using `templates/adr.md`. Do not overwrite an accepted decision without a superseding ADR.

The final design must be assembled from stage outputs and must contain all artifacts required by the source prompt, including concrete contracts, execution order, runtime placement, critical paths, failure behavior, diagrams, roadmap, and the anti-overengineering classification.

Before publication, run `scripts/validate_workspace.sh --final` and complete `quality/final-acceptance-checklist.md`. A final-review agent must report no unresolved critical defects.

## Default user command

When asked to “continue the ARK design,” execute only the next incomplete stage, update durable files, summarize the result, and stop wherever the workflow requires approval.
