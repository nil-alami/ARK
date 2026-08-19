# ARK system-design workflow

The order below mirrors `sources/normalized/system-design-prompt.md`. Stages are executed sequentially. The source prompt remains authoritative; stage files route and validate it but do not replace it.

## Global execution rules

- Execute the lowest-numbered incomplete stage only.
- Read `stages/STAGE-CONTRACT.md` and the named stage file in full.
- Consume all required earlier outputs.
- Save one durable stage artifact at the exact path listed below.
- Update `STATUS.md` only after the gate passes.
- Approval gates require explicit user approval or explicit authorization to proceed under documented temporary assumptions.
- Subagents return analysis to the primary agent; the primary agent alone writes authoritative files.

## Ordered stages

| Stage | Governing source section | Required output | Specialist support | Approval gate |
|---:|---|---|---|---|
| 00 | Source manifest and all inputs | `outputs/stages/00-source-audit.md` | `source_auditor` | If required source is missing or contradictory |
| 01 | Project information + Working rules | `outputs/stages/01-discovery-and-questions.md` | `source_auditor` | Yes |
| 02 | 1. System definition | `outputs/stages/02-system-definition.md` | Optional `platform_architect` | No |
| 03 | 2. Capability and service inventory | `outputs/stages/03-capability-inventory.md` | One `capability_analyst` per card | If a named capability lacks evidence |
| 04 | 3. Architecture drivers and style | `outputs/stages/04-architecture-style.md` + ADR | `platform_architect` | Yes |
| 05 | 4. End-to-end architecture | `outputs/stages/05-end-to-end-architecture.md` | `platform_architect`, `data_mlops_architect` | No |
| 06 | 5. Data architecture | `outputs/stages/06-data-architecture.md` | `data_mlops_architect` | No |
| 07 | 6. API and integration design | `outputs/stages/07-api-integration.md` | `platform_architect` | No |
| 08 | 7. Execution and orchestration | `outputs/stages/08-execution-orchestration.md` | `platform_architect` | No |
| 09 | 8. Event and proactive-action architecture | `outputs/stages/09-events-proactive-actions.md` | `platform_architect` | No |
| 10 | 9. ML and MLOps architecture | `outputs/stages/10-mlops.md` | `data_mlops_architect` | No |
| 11 | 10. Agent architecture, only if justified | `outputs/stages/11-agent-architecture.md` | `data_mlops_architect`, `assurance_reviewer` | If any agent is proposed |
| 12 | 11. Security, privacy, and governance | `outputs/stages/12-security-governance.md` | `assurance_reviewer` | No |
| 13 | 12. Reliability and failure design | `outputs/stages/13-reliability.md` | `assurance_reviewer` | No |
| 14 | 13. Observability and evaluation | `outputs/stages/14-observability-evaluation.md` | `platform_architect`, `data_mlops_architect` | No |
| 15 | 14. Deployment and infrastructure | `outputs/stages/15-deployment-infrastructure.md` | `platform_architect` | If deployment environment remains blocking |
| 16 | 15. Testing strategy | `outputs/stages/16-testing.md` | `assurance_reviewer` | No |
| 17 | 16. Capacity, performance, and cost | `outputs/stages/17-capacity-cost.md` | `platform_architect`, `data_mlops_architect` | If a purchase/build commitment is proposed |
| 18 | 17. Architecture decisions | `outputs/stages/18-architecture-decisions.md` + ADRs | `assurance_reviewer` | Yes |
| 19 | 18. Diagrams | `outputs/stages/19-diagrams.md` | Optional specialist review | No |
| 20 | 19. Implementation roadmap | `outputs/stages/20-roadmap.md` | `platform_architect` | No |
| 21 | 20. Final deliverables | `outputs/stages/21-provisional-final-deliverables.md` | Primary agent | No; provisional only |
| 22 | Runtime placement and execution-flow analysis | `outputs/stages/22-runtime-execution-analysis.md` | `platform_architect`, `data_mlops_architect` | No |
| 23 | Anti-overengineering test + publication | files under `outputs/final/` | `assurance_reviewer` for component challenge | Yes |
| 24 | Independent final assurance | `outputs/stages/24-final-assurance.md` | `assurance_reviewer` | Final pass required |

## Final publication set

Stage 23 assembles, and Stage 24 validates:

1. `outputs/final/ARK-system-design.md`
2. `outputs/final/ARK-diagrams.md`
3. `outputs/final/ARK-interface-contracts.md`
4. `outputs/final/ARK-execution-flows.md`
5. `outputs/final/ARK-implementation-roadmap.md`
6. `outputs/final/ARK-requirements-traceability.md`
7. `outputs/final/ARK-architecture-decisions.md`
8. `outputs/final/ARK-risks-and-open-questions.md`

The word “final” is prohibited in user-facing status until Stage 24 passes.

## Restart behavior

On any restart, trust source files, accepted ADRs, completed stage outputs, and `STATUS.md` over conversation memory. Re-open the current stage's required inputs in full. Never redo accepted stages unless a new source or superseding decision invalidates them; in that case, record the invalidation and all downstream stages that require revision.
