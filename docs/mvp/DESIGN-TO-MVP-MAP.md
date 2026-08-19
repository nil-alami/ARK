# ARK design-to-Reference-MVP map

Status: `PLANNED`

> **ADR-017/018 notice:** this mapping describes the earlier direct-tenant/unpriced fixture. Both impact documents are mandatory: ADR-017 adds organization/business authorization and pattern rows; ADR-018 adds shared owner balance, organization policy, reservation/settlement and charge-attribution rows. The current code has not implemented them.

## Mapping rule

This document maps the assured architecture to one bounded demonstration. “Demonstrated” means the local behavior is observable and testable; it does not mean the related production requirement, authority, scale, science, or admission block has passed.

## Required flow mapping

| Required MVP step | Approved ARK boundary | MVP realization | Class | Principal evidence | What is not claimed |
|---:|---|---|---|---|---|
| 1. Run initialization | Request/correlation/idempotency identities | `POST /demo/v1/runs` creates `run_id`, correlation, scenario, release/config, and immutable status | real implementation | `run.initialized` | A new production aggregate or workflow engine |
| 2. Tenant context | Principal-derived `AuthContext` before tenant lookup | Test credential resolves immutable tenant/subject; context flows through every port | simplified implementation | `tenant.context.derived`; cross-tenant tests | Production IAM/trust admission |
| 3. Data receipt | Push-first raw-first ingestion | Bounded synthetic transactions/catalog/inventory accepted and immutable raw object/digest stored before parse | real implementation | `data.received` with ref/digest/counts | A production source/canonical contract |
| 4. Schema validation | Structural authority | Pydantic/envelope and row validators produce versioned report and reason counts | real implementation | `schema.validation.completed` | Complete domain/data-governance validation |
| 5. Invalid-row quarantine | Invalid data preserved but excluded | Rejected row refs and codes stored in quarantine owner schema; safe aggregate shown in UI | real implementation | `row.quarantined`, quarantine API | Production privacy/retention policy |
| 6. Normalization | Semantic validation then readiness publication | Deterministic canonical transform, fixture referential rules, dataset digest, immutable `READY/NOT_READY` state | simplified implementation | `normalization.completed`, `dataset.readiness.published` | Authoritative business semantics |
| 7. Capability eligibility | Readiness and science remain distinct | Fixture-only sufficiency rule evaluates normalized history/catalog after READY | simplified implementation | `capability.eligibility.evaluated` | REC scientific eligibility or profile clearance |
| 8. Job creation/execution | PostgreSQL job/attempt/lease/fence lifecycle | One job is committed, worker claims fenced attempt, executes/retries, and finalizes | real implementation | job/attempt rows and lifecycle events | Production throughput, concurrency, or exactly-once execution |
| 9. Feature generation | Capability-owned versioned transformations | Deterministic recency/frequency/value and item-affinity fixture features | simplified implementation | `feature.generation.completed` with feature-set ref | Approved feature science or feature store |
| 10. Candidate generation | Capability-owned candidate stage | Eligible sellable catalog items become bounded candidates | simplified implementation | `candidate.generation.completed` | Learned retrieval, personalization quality, or scale |
| 11. Ranking/business rules | Deterministic ML/rules boundary | Stable fixture score/tie-break, inventory filter, dedupe, top-k, empty-result truth | simplified implementation | `ranking.completed`, `business_rules.applied` | Production thresholds, policy, or trained ranker |
| 12. Result persistence | Owner result before job finalization | Immutable result object/ref/digest committed once, then evidence linked and job succeeds | real implementation | `result.persisted`, `job.finalizing`, `job.succeeded` | Production retention or scientific validity |
| 13. Result delivery | Polling authoritative; delivery separate | Gradio polls result; optional no-network emulator records delivery success/failure separately | polling real; external delivery simulated | `result.polled`; `delivery.attempt.failed` where selected | Activated webhook/publisher or cleared delivery block |

## Architecture element disposition

| Assured design element | MVP use | MVP class | Mapping / constraint |
|---|---|---|---|
| Boundary-enforced modular monolith | Used | real implementation | Modules expose typed ports; architecture tests reject private imports and owner cross-writes |
| REST/JSON public contract | Used | real implementation | FastAPI routes; Gradio is API-only consumer |
| Typed in-process ports | Used | real implementation | API/worker call public module ports, not repositories owned by other modules |
| Shared PostgreSQL with owned schemas | Used | real implementation | Separate schemas/tables for demo run, control, catalog, job, capability result, evidence, delivery simulation |
| Provider-neutral object contract | Used | simplified implementation | Digest-addressed local adapter; DB carries tenant-scoped refs |
| Test-only trusted context | Used | simplified implementation | Two credentials/two tenants; impossible outside demo profile |
| Subscription/entitlement/grant/quota/policy separation | Partly used | simplified implementation | One immutable fixture decision object; denial scenarios prove no job |
| Raw-first ingestion | Used | real implementation | Raw commit precedes any parse event |
| Structural/semantic/readiness/scientific layers | Used | mixed | Structural/quarantine real; normalization/readiness/eligibility fixture semantics simplified |
| Durable job state machine | Used | real implementation | MVP subset retains legal transitions, attempts, lease/fence, retry, finalization, terminal truth |
| Scheduler | Not used | postponed | Explicit user submission; no named schedule |
| Event/outbox publisher | Not used | postponed | No named committed-fact subscriber |
| Worker role separation | Used | real implementation | `worker-general` is a same-release separate process/entrypoint |
| Seven capability definitions | Contract awareness only | simplified implementation | Only CAP-REC fixture is executable; inventory/profile blocks remain visible |
| Real capability implementations | Not used | postponed | No profile is admitted |
| Capability-owned features/results | Used | simplified + real | Fixture transforms/ranking simplified; result ownership/persistence real |
| Model/artifact lifecycle | Not used | postponed | No training, registry promotion, assignment, load, cache, canary, or rollback |
| Polling result delivery | Used | real implementation | Universal UI recovery path |
| Webhook delivery | Not used | postponed | Local simulator demonstrates failure isolation without network egress |
| Audit/lineage/usage | Used in bounded form | simplified implementation | Required local evidence refs and finalization checks; no compliance claim |
| Observability | Used in bounded form | simplified implementation | Structured trace plus health; diagnostic backend/export postponed |
| Maintenance/migration | Used | real implementation | Additive bootstrap and scope-checked demo reset |
| Release/build identity | Used in bounded form | simplified implementation | Version/digest recorded; production supply-chain block remains |
| Proactive Phase A/B/effect | Not used | postponed | No approved action/channel/authority packet |
| Named workflow coordinator | Not used | postponed | One direct bounded job; no graph |
| Agent architecture | Not used | not applicable | Deterministic flow; no agent/runtime/tools/memory/MCP/A2A |

## Requirements and decisions preserved

| Source requirement / decision | MVP evidence | Residual or active block |
|---|---|---|
| `ARK-FR-001` control separation | Fixture control decision and denial/no-job tests | Production policy roles/values unavailable |
| `ARK-FR-002/003` ingestion and raw-to-ready | Raw, report, quarantine, dataset version, lineage events | `DATA_CONTRACT_ADMISSION_BLOCKED` |
| `ARK-FR-004/005` versioned capability contract/envelope | CAP-REC fixture definition and strict request schemas | Real capability remains blocked |
| `ARK-FR-006` distinct acceptance layers | Layer-specific states/reason codes/scenarios | Fixture semantics only |
| `ARK-FR-007/008` durable async lifecycle | Job/attempt/fence/retry/finalization/poll tests | Capacity/production operation unproved |
| `ARK-FR-009` lifecycle separation | Negative assertion: no training/promotion/assignment/model load | CAP-REC `MIGRATION_BLOCKED` |
| `ARK-FR-010/011` proactive/delivery separation | Result truth survives simulated delivery failure | Real proactive/event/webhook paths absent/blocked |
| `ARK-FR-012` evidence package | Trace export and scenario evidence manifest | LAB authority/acceptance undefined |
| `ARK-NFR-001` tenant isolation | Two-tenant collision, forged tenant, cross-resource tests | `EXTERNAL_TRUST_BLOCKED`; production assurance absent |
| `ARK-NFR-002/006` identity, lineage, evidence | Correlation across run/data/job/attempt/result/events | Production governance/telemetry unresolved |
| `ARK-NFR-003` bounded neutral contracts | FastAPI/Pydantic schemas and API-only UI | Consumer/cutover not selected |
| `ARK-NFR-004` at-least-once/one logical result | Fail-once retry and stale-fence tests | No end-to-end exactly-once claim |
| `ARK-CON-001/002` modular monolith ownership | Dependency and owned-schema tests | No extraction decision |
| `ARK-CON-004/005` object refs and PostgreSQL jobs | Real local semantics | Production storage/environment/capacity blocked |
| ADR-011 push-first | Inline bounded synthetic push | No production source admission |
| ADR-012 feature management first | Versioned fixture feature set, no product | No feature-store claim |
| ADR-013 no agent | Build/dependency absence assertion | Full re-entry required for future agent |
| ADR-014 build/buy conditional | Commodity libraries only, owned contracts | No vendor/purchase decision |
| ADR-016 authority | Sponsor reviews plan/evidence; AI non-authoritative | Later specialist/production authorities unassigned |

## Parts of the final design that this MVP cannot meaningfully demonstrate

| Final-design concern | Why a single synthetic Recommendation demonstration is insufficient | MVP disposition |
|---|---|---|
| Scientific REC correctness and business value | No authoritative production feature/candidate/ranking semantics, thresholds, feedback, baselines, or scientific owner | postponed; fixture outputs carry no quality claim |
| Other six capability contracts at runtime | One-capability flow cannot validate distinct data, model/provider, safety, output, or operating profiles | definitions/block states only; execution postponed |
| Training/evaluation/promotion/assignment/rollback | No admitted model, evaluation policy, promotion authority, or environment assignment exists | negative absence tests only |
| Production identity, workload trust, delegation, and revocation | Two hard-coded fixture tenants cannot establish provider, credential, assurance, network, or incident behavior | test contract only; `EXTERNAL_TRUST_BLOCKED` |
| Production data governance | Synthetic rows cannot validate consent, purpose, classification, residency, retention, deletion, legal hold, backups, or derived-model impact | `DATA_GOVERNANCE_BLOCKED` retained |
| Secrets/crypto/supply chain | Local configuration and dependency lock do not prove key lifecycle, encryption, signing, separation, revocation, or vulnerability policy | blocks retained |
| External delivery and ambiguous real effects | A no-network emulator cannot prove endpoint ownership, DNS/SSRF, signing, egress, receiver idempotency, or network ambiguity | simulator only; real path postponed |
| Scheduled/event-triggered/proactive flows | No named schedule, source fact, subscriber, grant, action, channel, or owner exists | postponed |
| Named multi-capability workflows | No approved graph or admitted child capabilities exist | postponed |
| Production topology, HA, DR, capacity, cost, and SLOs | A local run has one failure domain and no authoritative workload/targets | characterization may be collected later; no claim |
| Backup/restore and full recovery epoch | A disposable demo can test restart/retry but not governed backups, deletion obligations, cross-store restore, or external-effect reconciliation | only worker restart/fence demonstrated |
| Consumer adapters, coexistence, and cutover | Gradio is a demo client, not a named consumer or legacy estate | `CONSUMER_CUTOVER_BLOCKED` retained |
| LAB evidence authority | No LAB contract, environment, rubric, or acceptance authority is supplied | local evidence export only |
| Agent execution | Current design explicitly finds no justified agent need | not applicable, not postponed implementation |

## Trace to planning artifacts

- Scenario truth: `docs/mvp/SCENARIOS.md`
- Event/schema truth: `docs/mvp/EXECUTION-TRACE-CONTRACT.md`
- Implementation choices and interfaces: `docs/mvp/TECHNICAL-PLAN.md`
- Ordered vertical slices: `implementation/MVP-BACKLOG.md`
- Current state: `implementation/MVP-STATUS.md`
- Requirement-to-slice/test/event trace: `implementation/MVP-TRACEABILITY.md`
