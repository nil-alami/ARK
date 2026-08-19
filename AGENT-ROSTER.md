# Agent roster and coordination model

The primary Codex agent is the workflow controller, sole authoritative writer, decision reconciler, and final editor.

| Agent | Used for | May run in parallel with | Must not do |
|---|---|---|---|
| `source_auditor` | Source inventory, contradictions, missing facts | Other read-only audits | Design or resolve conflicts silently |
| `capability_analyst` | One service card per agent | Analysts for other service cards | Infer unprovided capabilities or edit outputs |
| `platform_architect` | Platform boundaries, APIs, jobs, events, control plane | `data_mlops_architect` on independent concerns | Become the final writer |
| `data_mlops_architect` | Ingestion, data lake, ML lifecycle, agent justification | `platform_architect` on independent concerns | Add fashionable infrastructure without evidence |
| `assurance_reviewer` | Independent gate review after a coherent draft exists | Other non-overlapping assurance checks | Rewrite artifacts or approve its own draft |

## Coordination rules

1. Stages remain sequential because later work depends on approved earlier outputs.
2. Inside a stage, only independent read-heavy analysis may be parallelized.
3. Every delegation names inputs, output fields, and exclusions.
4. The primary agent waits for all requested findings, resolves disagreement using source precedence, and writes one coherent stage output.
5. No subagent edits shared files. This avoids concurrent-write conflict and fragmented architecture ownership.
6. The assurance reviewer is used after synthesis, not as a co-author of the same draft it reviews.
