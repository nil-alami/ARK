# ARK Reference MVP traceability

Status: `PLAN BASELINE`

> **ADR-017/018 notice:** this matrix covers earlier implementation evidence. No row demonstrates the accepted organization/business hierarchy, uniform pattern/admin behavior, shared owner credit pool, organization policy, reservation/settlement, or charge attribution. Add both impact-document requirements/tests before returning MVP status to evidence-ready.

## Traceability rules

- A row is covered only when its named slice has passed the named tests and emitted the required durable evidence. Planning text alone is not implementation evidence.
- `MVP-*` identifiers are Reference MVP planning IDs, not new ARK production requirements.
- “Pass” proves the bounded local behavior only. It cannot clear an active block without the governing authority/evidence decision.
- Implementation evidence references are `TBD` until a slice runs; no fabricated pass state is recorded.

## Objective-to-slice trace

| ID | Required demonstrated behavior | Design owner/boundary | Slice | Scenario | Required trace evidence | Minimum tests | Current evidence |
|---|---|---|---|---|---|---|---|
| `MVP-FLOW-01` | Run initialization | demo run owner | 01 | S-01..05 | `run.initialized` | contract, PostgreSQL integration, idempotency, E2E | TBD |
| `MVP-FLOW-02` | Tenant context | trust/context owner | 01 | all | `tenant.context.derived` | forged tenant, two-tenant collision, foreign-ref E2E | TBD |
| `MVP-FLOW-03` | Data receipt | ingestion/object owner | 01 | S-01..05 | `data.received` | raw-first, digest/ref, crash, cross-tenant object | TBD |
| `MVP-FLOW-04` | Schema validation | ingestion validation owner | 01/02 | S-01..03 | validation start/completed | schema/property/mutation, unknown fields, E2E | TBD |
| `MVP-FLOW-05` | Invalid-row quarantine | quarantine owner | 02 | S-02 | `row.quarantined`, `quarantine.completed` | uniqueness, accepted-only lineage, redaction, tenant isolation | TBD |
| `MVP-FLOW-06` | Normalization | ingestion/catalog owner | 01/02 | S-01..05 | `normalization.completed`, readiness publication | deterministic transform, semantic/ref integrity, no false READY | TBD |
| `MVP-FLOW-07` | Capability eligibility | REC fixture owner | 01/03 | S-01..05 | eligibility event, optional `run.ineligible` | layer separation, threshold property, zero-effect ineligible | TBD |
| `MVP-FLOW-08` | Job creation/execution | job manager/worker | 01/04 | S-01/02/04/05 | job/attempt/recheck/retry/finalization events | state property, idempotency, lease/fence, crash/restart, E2E | TBD |
| `MVP-FLOW-09` | Feature generation | REC fixture owner | 01 | eligible scenarios | feature event/ref | deterministic golden, exact input/version lineage | TBD |
| `MVP-FLOW-10` | Candidate generation | REC fixture owner | 01 | eligible scenarios | candidate event/ref | catalog/inventory/property, bounded set | TBD |
| `MVP-FLOW-11` | Ranking and business rules | REC fixture owner | 01 | eligible scenarios | rank/rules events | stable tie-break, availability, dedupe, top-k, empty truth | TBD |
| `MVP-FLOW-12` | Result persistence | result/evidence/job owners | 01/04 | eligible scenarios | result/finalizing/evidence/succeeded | owner-before-success, one result, finalization recovery | TBD |
| `MVP-FLOW-13` | Result delivery | API/result owner; demo delivery owner | 01/05 | S-01/S-05 | `result.polled`, simulated delivery events | polling auth/recovery; state separation; no network/recompute | TBD |
| `MVP-FLOW-14` | Stored replay | evidence/query owner | 06 | S-06 | replay access after snapshot | snapshot/order/hash, zero effect, tenant concealment | TBD |

## Scenario-to-acceptance trace

| Scenario | Principal acceptance requirement | Slice | Test/evidence families | Forbidden evidence/behavior |
|---|---|---|---|---|
| S-01 eligible | One run/job/attempt/result; deterministic available top-k; full trace/poll | 01 | clean E2E, golden rank, idempotency, owner-state/event reconciliation | Science/production claim; model/provider call |
| S-02 partial invalid | Exact raw/accepted/rejected reconciliation; invalid rows never normalize; result from accepted set | 02 | mutation/quarantine/lineage/crash/E2E | Raw invalid row in trace/UI/result |
| S-03 ineligible | READY then fixture INELIGIBLE; zero job/compute/result | 03 | layer boundary, negative-effect DB assertion, E2E | Failed/succeeded job or fabricated recommendation |
| S-04 retry | One job, two fenced attempts, one result; stale attempt rejected | 04 | state/concurrency/kill/lease/finalization/E2E | Second logical result or unpinned retry |
| S-05 delivery failure | Job/result succeed; simulated delivery fails; no recompute/network | 05 | state-separation, no-network, row/event diff, E2E | Publisher/webhook/URL/egress or result failure |
| S-06 replay | Stored snapshot reconstructs exact history; zero new effect; tenant authorized | 06 | hash/order/snapshot/diff/cross-tenant/UI E2E | Resubmission, new attempt/result/delivery |

## Slice completeness trace

Every row is a mandatory gate for the slice.

| Slice | E2E behavior | Acceptance criteria | Required tests | Structured events | README | Shortcut/decision distinction | State |
|---|---|---|---|---|---|---|---|
| 01 | S-01 | defined | defined | defined | create/update required | defined | planned |
| 02 | S-02 | defined | defined | defined | update required | defined | planned |
| 03 | S-03 | defined | defined | defined/prohibited set | update required | defined | planned |
| 04 | S-04 | defined | defined | defined | update required | defined | planned |
| 05 | S-05 | defined | defined | defined | update required | defined | planned |
| 06 | S-06 and full regression | defined | defined | defined/no historical mutation | finalize required | defined | planned |

Definitions are in `implementation/MVP-BACKLOG.md`. No slice may be split into a foundation-only increment that lacks its named E2E behavior.

## ARK requirement/decision trace

| ARK source ID / decision | Reference MVP realization | Slice(s) | Evidence/test gate | Limit / preserved block |
|---|---|---:|---|---|
| `ARK-FR-001` | Fixture control decision distinct from enablement/execution | 01/03 | deny/no-job and decision-version tests | Not production policy administration |
| `ARK-FR-002` | Bounded synthetic push | 01 | request/raw receipt contracts | Pull/streaming not selected |
| `ARK-FR-003` | Raw → validation/quarantine → normalization/readiness | 01/02 | raw-first/no-false-READY/correction-free fixture tests | `DATA_CONTRACT_ADMISSION_BLOCKED` |
| `ARK-FR-004` | One immutable CAP-REC fixture definition | 01 | schema/compatibility/blocked inventory assertions | Other definitions not executable; CAP-REC blocked |
| `ARK-FR-005` | Common strict envelope + fixture payload | 01 | contract/unknown-field/version tests | Demo subset only |
| `ARK-FR-006` | Structural/readiness/eligibility separation | 01/02/03 | scenario layer assertions | Fixture eligibility not science |
| `ARK-FR-007` | Job/attempt/lease/fence/retry/finalization | 01/04 | state/property/restart/fence tests | No capacity/exactly-once claim |
| `ARK-FR-008` | Async submit/poll; no sync inference | 01 | 202/idempotency/poll/result E2E | Only demo operation |
| `ARK-FR-009` | Negative assertion: no training/promotion/assignment/load | all | build/dependency/runtime absence tests | CAP-REC `MIGRATION_BLOCKED` |
| `ARK-FR-010` | Not exercised; no proactive action | all | absence/no-effect manifest assertion | postponed |
| `ARK-FR-011` | Poll result truth separated from delivery simulation | 01/05 | state separation/no recompute | `EXTERNAL_DELIVERY_BLOCKED` |
| `ARK-FR-012` | Local trace/evidence export | 06 | immutable evidence manifest | No LAB authority |
| `ARK-NFR-001` | Tenant on rows/objects/jobs/results/events and owner auth | all | cross-asset A/B collision suite | Production trust remains blocked |
| `ARK-NFR-002` | Distinct run/data/job/attempt/result/event/version refs | 01/04/06 | lineage and replay queries | Bounded MVP identities only |
| `ARK-NFR-003` | REST/Pydantic and API-only Gradio | 01 | contract/architecture tests | No consumer/cutover admission |
| `ARK-NFR-004` | At-least-once attempts; one logical result | 04 | retry/stale fence/result uniqueness | No exactly-once claim |
| `ARK-NFR-005` | Synthetic-only, safe refs, trace redaction | all | canary/property/redaction tests | Governance block remains |
| `ARK-NFR-006` | Correlated stored trace and bounded evidence | all | completeness/hash/owner-state reconciliation | Not production telemetry/audit |
| `ARK-NFR-007` | No numeric production target | all | warning/config classification | Capacity/environment blocks remain |
| `ARK-CON-001/002` | One release, hard modules, owned schemas/writers | 01 | dependency/repository/migration tests | No microservice extraction |
| `ARK-CON-003` | Gradio external API client | 01 | no core imports/consumer terms | No real adapter/cutover |
| `ARK-CON-004` | Object refs for payloads, PostgreSQL for bounded truth | 01 | object/ref/digest/size tests | Local adapter not production data lake |
| `ARK-CON-005` | PostgreSQL job authority | 01/04 | real-store concurrency/recovery tests | No broker |
| `ARK-CON-006` | Synthetic source identities only; no identity merge | 01/02 | stable ID/ref tests | No real source admission |
| `ARK-CON-007` | Forbidden-component and dependency manifest | all/06 | architecture/release absence test | Evidence-triggered additions only |
| ADR-003 | Modular monolith/runtime roles | 01 | module/process architecture evidence | No extraction |
| ADR-004/015 | REST/JSON, typed ports, polling | 01 | API/port/consumer-neutral tests | Cutover block active |
| ADR-005 | PostgreSQL state machine | 01/04 | lifecycle/fence/finalization evidence | Broker/engine absent |
| ADR-006 | Result/delivery authority separation | 05 | delivery failure isolation | Proactive/external path inactive |
| ADR-007/012 | Blocked REC and basic feature management | 01 | fixture label, no-model, versioned feature-set evidence | No profile re-entry |
| ADR-008 | Trusted context/tenant/block preservation | all | two-tenant/adversarial/default-deny suite | All eight blocks active |
| ADR-009/010 | Python/PostgreSQL/simple local role baseline | 01 | reproducible local evidence | No production topology claim |
| ADR-011 | Push-first/raw-first | 01/02 | receipt/quarantine/readiness tests | Contract admission blocked |
| ADR-013 | No agent | all/06 | build/runtime absence assertion | Agent N/A |
| ADR-014 | Owned contracts, conditional products | all | dependency/forbidden-platform inventory | No vendor purchase |
| ADR-016 | Sponsor accepts evidence; AI non-authoritative | each/closure | explicit sponsor record | Later authorities unassigned |

## Trace contract coverage

| Trace concern | Implemented by | Test gate | Evidence state |
|---|---|---|---|
| Strict envelope/version/unknown fields | Slice 01 | schema contract suite | TBD |
| Per-run monotonic sequence under concurrency | Slice 01/04 | PostgreSQL concurrent insertion | TBD |
| Owner transition + required event atomicity | Slice 01/02/04 | fault injection at owner commits | TBD |
| Required event taxonomy/order | all slices | per-scenario completeness/prohibited-event assertions | TBD |
| Implementation class and shortcut flags | all slices | schema/value/UI rendering tests | TBD |
| Causation/resource/version integrity | Slice 01/04/05 | graph/ref reconciliation tests | TBD |
| Tenant isolation/concealment | all slices | A/B collision and foreign-ref suite | TBD |
| Sensitive field prohibition | all slices | property/canary/redaction suite | TBD |
| Poll cursor/terminal behavior | Slice 01 | API/UI polling tests | TBD |
| Delivery state separation | Slice 05 | no-recompute/no-network suite | TBD |
| Replay snapshot/hash/zero effect | Slice 06 | snapshot/integrity/database diff suite | TBD |

## Components not meaningfully validated

These rows ensure absence is not mistaken for coverage.

| Concern | Reference MVP evidence | Status |
|---|---|---|
| Real REC science/business value | None; deterministic fixture only | not validated / postponed |
| Other six capabilities | Block-state/inventory assertion only | not validated / postponed |
| Model lifecycle/cache | Absence tests only | not validated / postponed |
| Production IAM/governance/secrets/crypto/supply chain | Default-deny and no-leak demo tests only | not validated / blocked |
| Real webhook/provider/network effect | No-network simulator only | not validated / blocked |
| Scheduler/event/proactive/workflow | Absence tests only | not validated / postponed |
| Production HA/DR/SLO/capacity/cost | No claim; local behavior only | not validated / blocked |
| Consumer cutover/LAB authority | Gradio/local evidence only | not validated / blocked |
| Agent | Absence assertion consistent with N/A decision | not applicable |

## Evidence manifest fields required at closure

The eventual immutable Reference MVP evidence manifest must contain:

- source commit/workspace/release/config/dependency/migration identities;
- Python/PostgreSQL and selected package versions;
- fixture contract/generator/dataset/object digests;
- scenario/run/job/attempt/result/event identifiers;
- executed tests, results, environment, failures/retries, and quarantines;
- per-row mapping to this traceability file;
- shortcut classifications and active block assertions;
- forbidden component/dependency/runtime-role inventory;
- README/runbook reproduction reference;
- AI contribution declaration;
- explicit human sponsor evidence-acceptance decision or unresolved defects.

No implementation row in this file may change from `TBD`/planned to passed based only on code existence, AI assertion, UI appearance, or an unrecorded manual run.
