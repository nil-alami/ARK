# ADR-000 — Temporary source-evidence disposition

Status: `ACCEPTED`

Date: 2026-08-11

Decision owner: ARK design sponsor (user approval)

## Context and requirements

Stage 00 discovered six capability cards under `sources/normalized/service-cards/` that were absent from the original manifest and have no corresponding immutable evidence under `sources/original/`. Their exact current contents were checksum-pinned. The three Synapse cards contain usable HTTP interface facts but leave material internal, operational, policy, ownership, and safety fields undocumented.

The Stage 00 approval gate required explicit disposition before these sources could be used downstream. Evidence: `outputs/stages/00-source-audit.md — Open questions`, Q-00-01 and Q-00-02.

## Decision

The user approved the following on 2026-08-11:

> Approve the six checksum-pinned cards as temporary evidence pending originals. Treat Synapse as interface-contract-only evidence, with all undocumented internals unresolved.

Therefore:

1. The exact checksum-pinned RFM, NPT, REC, Synapse chatbot, Synapse message-generator, and Synapse campaign-verifier files may be used as temporary capability evidence.
2. This approval admits the files for workflow use; it does not verify their provenance or turn their recommendations into approved architecture decisions.
3. Only explicitly documented Synapse interface facts may be treated as facts. Blank or undocumented internals remain unresolved and must not be inferred.
4. New originals or authoritative implementation evidence must be compared with the pinned files. Conflicts must be recorded and affected downstream work invalidated or revised.
5. Stage 03 may still stop if its complete capability-contract gate cannot be met from the admitted Synapse interface evidence.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| Supply and register originals before proceeding | Strongest provenance and fidelity | Blocks progress until originals are available | Preferred long-term, unavailable now | Originals are received |
| Treat pinned working copies as permanently authoritative | Fast and simple | Conceals provenance risk | Rejected | Explicit permanent authority decision |
| Use pinned working copies as temporary evidence | Preserves progress and exact traceability | Requires provisional labeling and later revalidation | Chosen | Originals or better evidence arrive |
| Scope affected capabilities out | Removes evidence dependency | Changes stated product scope | Rejected | Explicit product-scope decision |

## Rationale

The chosen option is the narrowest approval that lets the sequential workflow continue without inventing evidence or silently claiming provenance. Restricting Synapse to its documented interface prevents conventional LLM-service assumptions from becoming unsupported facts.

## Consequences and trade-offs

- Later stages may cite the six files, but must preserve their temporary-evidence status where material.
- Source-card recommendations remain recommendations unless separately approved.
- Synapse ownership, models, prompts, state, persistence, dependencies, failure behavior, policy authority, security controls, SLOs, and observability remain unresolved unless explicitly documented.
- Provenance risk remains visible until originals are supplied.
- Stage 00 can pass; Stage 01 becomes the next incomplete stage.

## Implementation constraints

- Do not modify the pinned files under `sources/normalized/`.
- Verify their hashes against `sources/SHA256SUMS` before relying on this decision after a restart.
- Do not fill blank Synapse card sections by inference.
- Do not describe a Synapse component as an agent solely because its API identifier contains “Agent.”
- Record newly received originals as new immutable evidence and update `SOURCE_MANIFEST.md` and `sources/SHA256SUMS`.

## Validation evidence

- All 12 entries in `sources/SHA256SUMS` matched their current files on 2026-08-11.
- The admitted files and hashes are listed in `SOURCE_MANIFEST.md — SHA-256 checksums`.
- The approval text is the user's explicit response to Stage 00 Q-00-01 and Q-00-02.

## Reconsideration trigger

- Receipt of any missing original or authoritative provenance record.
- Receipt of Synapse implementation, OpenAPI, configuration, policy, safety, or operational evidence.
- Any checksum mismatch in an admitted working copy.
- A user decision to change capability scope or grant permanent source authority.

## Supersedes / superseded by

Supersedes no prior ADR. Superseded by: none.
