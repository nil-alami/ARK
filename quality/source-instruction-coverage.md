# Source-instruction coverage matrix

Update `Status` to `Covered`, `Not applicable — reason`, or `Blocked — question`. Stage 24 may not pass while any row is `Pending` or unjustifiably blocked.

This file is the section-level controller. The literal one-instruction-per-ID mapping is `quality/source-instruction-atomic-coverage.md`; its IDs cover every working rule, capability-contract field, component field, design bullet, runtime-analysis field, required artifact, closing deliverable, and anti-overengineering question. A section-level `Covered` status is valid only while its atomic rows have exact destination evidence and no `Pending` entry.

| Source prompt section | Owning stage | Primary artifact | Status |
|---|---:|---|---|
| Project information | 01 | Discovery baseline | Covered |
| Working rules 1–15 | All | `quality/source-instruction-atomic-coverage.md — Working rules and process order` | Covered — each rule and nested recommendation field has a stable atomic ID and exact destination; Stage 24 independently revalidated them |
| 1. System definition | 02 | System definition | Covered |
| 2. Capability and service inventory | 03 | Capability inventory | Covered |
| 3. Architecture drivers and style | 04 | Style analysis + ADR | Covered |
| 4. End-to-end architecture | 05 | Component architecture | Covered |
| 5. Data architecture | 06 | Data architecture | Covered |
| 6. API and integration design | 07 | API/integration contracts | Covered |
| 7. Execution and orchestration | 08 | Execution design | Covered |
| 8. Event and proactive-action architecture | 09 | Event/proactive design | Covered |
| 9. ML and MLOps architecture | 10 | MLOps design | Covered |
| 10. Agent architecture, only if justified | 11 | Agent decision/contracts | Covered — no agent justified by current evidence; future re-entry contract and protocol gates recorded |
| 11. Security, privacy, and governance | 12 | Security/governance design | Covered — logical gate passed; production admission blocks remain explicit |
| 12. Reliability and failure design | 13 | Failure matrices | Covered — logical gate passed; numeric reliability/DR targets and named production owners remain explicit activation inputs |
| 13. Observability and evaluation | 14 | Observability/evaluation | Covered — logical gate passed; numeric SLOs, thresholds, retention, products and named owners remain explicit production inputs |
| 14. Deployment and infrastructure | 15 | Deployment design | Covered — approved provisional Python/PostgreSQL/one-Linux-server target; concrete production fitness remains `DEPLOYMENT_ENVIRONMENT_BLOCKED` pending environment/runbook evidence |
| 15. Testing strategy | 16 | Test strategy | Covered — logical gate passed; all production-admission blocks, missing numeric targets, and named-authority requirements remain active |
| 16. Capacity, performance, and cost | 17 | Capacity/cost model | Covered — symbolic gate passed; production sizing, targets, prices, budget, and purchases remain evidence/approval blocked |
| 17. Architecture decisions | 18 | ADR index/files | Covered — all ten named comparisons, alternatives, risks, trade-offs, statuses, supersessions, and reconsideration triggers recorded; ADR-010–015 were accepted on 2026-08-13 and ADR-016 later narrowed the Stage-20 ownership treatment |
| 18. Seven required diagrams | 19 | Diagram set | Covered — context, logical architecture, synchronous, asynchronous, proactive delivery, data lifecycle, and deployment diagrams complete |
| 19. Implementation roadmap | 20 | Roadmap | Covered — five evidence-ordered phases, engineering-ready first milestone, dependencies, acceptance evidence, risks, and postponements complete |
| 20. Ten final deliverables | 21/23 | Final publication | Covered — `DEL-01` through `DEL-10` have exact destinations in the atomic register and `outputs/final/ARK-requirements-traceability.md — Ten closing deliverables map`; Stage 24 assurance passed |
| Runtime placement: usage and placement | 22 | Runtime analysis | Covered — every significant element has trigger, placement, owner/state/contract, criticality and removal/movement effect |
| Runtime placement: execution/dependencies | 22 | Runtime analysis | Covered — exact ordering, bounded concurrency, fan-in, races, consistency, timeout/cancel and retry boundaries recorded |
| Runtime placement: critical/supporting paths | 22 | Runtime analysis | Covered — business/result/effect, background, telemetry, mandatory audit and delivery paths separated per use case |
| Runtime placement: four artifacts for eight use cases | 22 | Execution-flow package | Covered — all eight packages contain usage/dependency tables, narrative and Mermaid; agentic flow is explicit N/A under Stage 11 |
| Anti-overengineering test | 23 | Component classification and revisions | Covered — every included and deferred element answers the six governing questions through explicit current need, simpler outcome, burden, ADR-016 ownership capacity, classification and measurable re-entry trigger; independent Stage 23 component challenge applied |
