# ADR-001 — Stage 01 requirements baseline

Status: `ACCEPTED`

Date: 2026-08-11

Decision owner: ARK design sponsor (user approval)

## Context and requirements

Stage 01 assembled the known requirements baseline, forty architecture-driving questions across the eight required discovery groups, and eight temporary assumptions for unanswered matters. The Stage 01 completion gate required explicit approval of the baseline and authorization of temporary assumptions before Stage 02 could begin.

The sponsor stated: “Approve the Stage 01 requirements baseline and authorize A-01-BUS, A-01-DATA, A-01-ML, A-01-INT, A-01-SCALE, A-01-SEC, A-01-OPS, and A-01-TEAM as temporary assumptions until their stated expiry points.”

## Decision

The requirements baseline in `outputs/stages/01-discovery-and-questions.md` is approved.

The following temporary assumptions are authorized and active until the validation or expiry condition stated for each assumption in that artifact:

- `A-01-BUS`
- `A-01-DATA`
- `A-01-ML`
- `A-01-INT`
- `A-01-SCALE`
- `A-01-SEC`
- `A-01-OPS`
- `A-01-TEAM`

Unanswered discovery questions remain unresolved requirements and must be revisited no later than their stated expiry points. New authoritative evidence or an explicit user decision supersedes a conflicting temporary assumption and must be recorded durably.

This approval does not convert recommendations in service cards or the Stage 01 artifact into approved architecture decisions. It does not select a deployment platform, vendor, broker, workflow engine, service mesh, feature store, vector database, agent framework, capacity value, SLO, availability or recovery target, compliance regime, budget, deadline, or MVP sequence. Synapse evidence remains restricted by `ADR-000` to explicit interface-contract facts; every undocumented internal remains unresolved.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| Answer every discovery question before continuing | Maximum early certainty | Requires unavailable business, operational, security, and measured workload evidence | Not selected | Use whenever owners can supply authoritative answers |
| Approve the baseline and authorize the eight temporary assumptions | Preserves traceability and lets system-boundary work proceed without invented facts | Later work remains conditional and assumptions require expiry management | Selected | Replace each assumption when its stated validation evidence becomes available |
| Halt the workflow pending all missing evidence | Avoids conditional design | Prevents useful reversible architecture work | Not selected | Reconsider if a later stage cannot pass safely under its authorized assumptions |
| Infer conventional scale, SLO, platform, compliance, and staffing values | Produces superficially concrete design inputs | Violates source rules and risks unjustified commitments | Rejected | Never without authoritative evidence or explicit approval |

## Rationale

The selected option is the smallest reversible decision that satisfies the Stage 01 completion gate. It preserves unknowns as unknowns, makes their architectural effects visible, and permits Stage 02 to define the system without committing to unsupported implementation or operating targets.

## Consequences and trade-offs

- Stage 01 passes and Stage 02 becomes the next incomplete stage.
- Later outputs that depend on an active assumption remain conditional until the assumption is validated or replaced.
- The forty discovery questions remain tracked; approval defers them but does not answer them.
- Stage 03 must still apply its evidence gate, including the Synapse restrictions established by `ADR-000`.
- Production sizing, SLO, recovery, compliance, procurement, and delivery commitments remain unavailable until their required evidence is supplied.

## Implementation constraints

- Cite the applicable `A-01-*` identifier wherever a later recommendation materially depends on a temporary assumption.
- Revalidate an assumption at or before its stated expiry point; do not silently extend it.
- Preserve the modular-monolith and platform-neutral baseline unless a later approved decision supersedes it.
- Do not infer undocumented Synapse internals from endpoint names, “Agent” identifiers, or conventional LLM designs.
- Record any conflicting user answer or new evidence as a superseding decision before relying on it.

## Validation evidence

- User approval dated 2026-08-11, quoted in this ADR.
- `outputs/stages/01-discovery-and-questions.md` — assumptions, open questions, decision timing, and completion-gate evidence.
- `decisions/ADR-000-temporary-source-evidence-disposition.md` — temporary evidence and Synapse restrictions.
- `outputs/stages/00-source-audit.md` — approved source inventory and provenance state.

## Reconsideration trigger

Any stated assumption expiry, authoritative answer to a covered discovery question, new source evidence, or downstream gate finding that an assumption is unsafe or insufficient.

## Supersedes / superseded by

Supersedes no prior ADR. Not superseded.
