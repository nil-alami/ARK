# Stage 19 — Diagrams

**Status:** APPROVED  
**Completed:** 2026-08-13  
**Stage owner:** Primary architecture agent  
**Specialist support:** None required; Stage 19 permits but does not require specialist review

## Purpose and scope

Provide the seven readable Mermaid diagrams required by `sources/normalized/system-design-prompt.md — 18. Diagrams`, using the stable component names, authority boundaries, failure semantics, deployment roles, and accepted ADRs from approved Stages 04–18. These diagrams visualize the approved design; they do not select products, clear production blocks, or begin the Stage 20 roadmap.

## Inputs read in full

- `WORKFLOW.md`
- `STATUS.md`
- `SOURCE_MANIFEST.md`
- `stages/STAGE-CONTRACT.md`
- `stages/19-diagrams.md`
- `sources/normalized/system-design-prompt.md — 18. Diagrams`
- Approved `outputs/stages/04-architecture-style.md` through `outputs/stages/18-architecture-decisions.md`
- Accepted `decisions/ADR-003-architecture-style.md` through `decisions/ADR-015-rest-json-and-typed-ports-before-grpc.md`
- `outputs/stages/05-end-to-end-architecture.md — Component inventory; End-to-end logical architecture`
- `outputs/stages/06-data-architecture.md — Four-layer acceptance model; Zone and authoritative-writer matrix; Lineage and provenance graph`
- `outputs/stages/07-api-integration.md — External resource and operation surface; Internal application-port contracts`
- `outputs/stages/08-execution-orchestration.md — Internal job state machine; Durable execution flow`
- `outputs/stages/09-events-proactive-actions.md — Two-phase fail-closed decision order; External delivery state and semantics`
- `outputs/stages/12-security-governance.md — Security invariants; Tenant-bearing asset control matrix`
- `outputs/stages/15-deployment-infrastructure.md — Conditional starting deployment; Deployable runtime-role matrix; Network, trust, and secrets placement`

## Source-instruction coverage

| Required diagram | Section | Result |
|---|---|---|
| System context | Diagram 1 | Covered |
| Logical container/component architecture | Diagram 2 | Covered |
| One synchronous request flow | Diagram 3 | Covered |
| One asynchronous job flow | Diagram 4 | Covered |
| One proactive ML event-delivery flow | Diagram 5 | Covered |
| Data lifecycle | Diagram 6 | Covered |
| Deployment architecture | Diagram 7 | Covered |
| Readability and consistency | Diagram conventions and validation | Covered; details split across seven views |

## Confirmed facts

1. ARK is a boundary-enforced modular monolith with separately runnable roles from one coordinated Python release, not a service-per-capability system. `ADR-003 — Decision`; `ADR-009 — Decision`.
2. Stable logical component names are `C05-01` through `C05-22`. A component is not automatically a process, container, service, database, or product. `outputs/stages/05-end-to-end-architecture.md — Component inventory`.
3. External contracts use REST/JSON; internal coordination uses typed module ports and PostgreSQL-backed durable jobs. No gRPC, broker, agent runtime, MCP, A2A, Kubernetes, or standalone feature store is selected. ADR-005, ADR-012, ADR-013, and ADR-015.
4. Tenant authority derives from trusted principal/workload context. Body tenant values, object paths, model output, event payload, or delivery destination never create authority. `ADR-008 — Decision`.
5. All production-admission states remain cumulative and active, including four `MIGRATION_BLOCKED`, three `EVIDENCE_BLOCKED`, eight ADR-008 security blocks, `DEPLOYMENT_ENVIRONMENT_BLOCKED`, `CAPACITY_ADMISSION_BLOCKED`, `DATA_CONTRACT_ADMISSION_BLOCKED`, `CONSUMER_CUTOVER_BLOCKED`, and `A-04-OWNERSHIP`. Approved Stage 18.

## Assumptions and diagram conventions

- Solid arrows show an approved logical call, command, data/reference movement, or state transition. They do not imply a network hop.
- Dashed arrows show supporting telemetry, optional/conditional delivery, or a path that remains admission-blocked.
- PostgreSQL and object storage are logical infrastructure contracts. The exact production providers and placement remain unresolved.
- “One Linux server” is the provisional implementation/benchmark target, not a production availability or topology claim.
- Component labels retain their `C05-*` identities so later stages can trace every edge to the component inventory.

## Diagram 1 — System context

```mermaid
flowchart LR
    Consumer["Consumer applications / operators\nC05-01 adapters"]
    Sources["Authoritative tenant data sources"]
    LAB["LAB\nexternal evidence consumer"]
    IdP["Identity / trust provider contract\nEXTERNAL_TRUST_BLOCKED"]
    Provider["Synapse / external LLM provider\nEVIDENCE_BLOCKED + LLM_PROVIDER_BLOCKED"]
    Destination["Approved webhook destination\nEXTERNAL_DELIVERY_BLOCKED"]

    subgraph ARK["ARK boundary-enforced modular monolith"]
        API["REST/JSON platform boundary\nC05-02 / C05-03 / C05-05"]
        Control["Tenant control, grants, policy, quota\nC05-04"]
        Data["Ingestion, catalog, jobs and schedules\nC05-06–C05-10"]
        Cap["Seven capability modules and registry\nC05-11 / C05-16"]
        Delivery["Results and conditional delivery\nC05-12 / C05-21"]
        Evidence["Audit, lineage, usage, observability\nC05-18 / C05-19"]
    end

    Consumer -->|"authenticated REST/JSON; polling"| API
    Sources -.->|"push / referenced bulk only after contract admission"| API
    API --> Control
    API --> Data
    Data --> Cap
    Cap --> Delivery
    Control --> Evidence
    Data --> Evidence
    Cap --> Evidence
    Delivery --> API
    Evidence -->|"minimized immutable evidence package"| LAB
    IdP -.->|"identity contract; production blocked"| API
    Cap -.->|"documented interface only; no production call"| Provider
    Delivery -.->|"signed at-least-once delivery after admission"| Destination
```

**Boundary reading:** Sources and consumers remain authoritative for their own data and presentation. ARK owns platform state and evidence. LAB consumes evidence but has no implicit promotion authority. External providers and delivery are visibly blocked, not depicted as active production dependencies.

## Diagram 2 — Logical container/component architecture

```mermaid
flowchart TB
    subgraph Edge["Integration and edge boundary"]
        C01["C05-01 Consumer adapter"]
        C02["C05-02 Logical edge/API"]
        C03["C05-03 AuthN/AuthZ + tenant context"]
        C05["C05-05 Capability and job API"]
        C12["C05-12 Result / notification delivery"]
    end

    subgraph Control["Control plane"]
        C04["C05-04 Entitlement / quota / grant / policy"]
        C17["C05-17 Secrets and technical config"]
        C20["C05-20 Admin / operations interfaces"]
    end

    subgraph Data["Data and execution plane"]
        C06["C05-06 Ingestion / validation / publication"]
        C07["C05-07 Dataset catalog / readiness"]
        C08["C05-08 Durable job manager"]
        C09["C05-09 Scheduler"]
        C10["C05-10 Worker runtime roles"]
    end

    subgraph Capability["Capability plane"]
        C11["C05-11 Seven capability modules"]
        C15["C05-15 Capability feature / result / state"]
        C16["C05-16 Model / artifact registry"]
        C22["C05-22 Named workflow coordinator\nconditional and not deployed"]
    end

    subgraph Stores["Shared infrastructure; owned namespaces and writers"]
        C13[("C05-13 PostgreSQL\nmodule-owned schemas")]
        C14[("C05-14 Object storage\ntenant/owner/version namespaces")]
    end

    subgraph Evidence["Operational and evidence plane"]
        C18["C05-18 Audit / lineage / usage ledger"]
        C19["C05-19 Observability"]
        C21["C05-21 Reliable publication adapter\nconditional"]
    end

    C01 --> C02 --> C03 --> C05
    C03 --> C04
    C05 --> C07
    C05 --> C08
    C05 --> C11
    C09 --> C08 --> C10
    C10 --> C06
    C10 --> C11
    C06 --> C07
    C07 --> C11
    C11 --> C16
    C11 --> C15
    C11 --> C12 --> C01
    C06 --> C14
    C15 --> C14
    C16 --> C14
    C04 --> C13
    C07 --> C13
    C08 --> C13
    C15 --> C13
    C16 --> C13
    C17 --> C03
    C17 --> C10
    C20 -->|"typed owner commands only"| C04
    C20 -->|"typed owner commands only"| C08
    C04 --> C18
    C06 --> C18
    C08 --> C18
    C11 --> C18
    C12 --> C18
    C18 -.-> C19
    C21 -.-> C12
    C22 -.-> C08
```

**Ownership reading:** The shared PostgreSQL cluster is physical infrastructure, not shared write authority. Every schema, object namespace, state transition, and command has one logical owner. Conditional `C05-21` and `C05-22` do not imply a broker or workflow engine.

## Diagram 3 — Synchronous request flow

```mermaid
sequenceDiagram
    autonumber
    actor U as Consumer / C05-01
    participant E as Edge + AuthContext / C05-02,03
    participant P as Control policy / C05-04
    participant A as Capability API / C05-05
    participant D as Catalog readiness / C05-07
    participant C as Capability / C05-11
    participant R as Registry / C05-16
    participant S as Owned stores / C05-13,14,15
    participant X as Audit / C05-18

    U->>E: Versioned REST request + idempotency/correlation
    E->>E: Authenticate, derive tenant from principal, validate limits
    alt Trust or request invalid
        E-->>U: Typed denial, zero execution/effect
    else Trusted request
        E->>P: Authorize operation, entitlement, quota, grant
        P-->>E: Versioned allow or reasoned denial
        alt Denied or ambiguous
            E-->>U: Typed ineligible/unauthorized response
        else Allowed
            E->>A: Validate capability/version and synchronous eligibility
            A->>D: Resolve exact READY dataset/context
            D-->>A: Versioned readiness result
            A->>C: Typed public-port command with immutable AuthContext
            C->>R: Resolve exact approved assignment/artifact
            R-->>C: Exact bundle reference or blocked reason
            C->>S: Read authorized inputs, commit owned result
            C->>X: Commit lineage, usage and mandatory audit evidence
            C-->>A: Bounded result/status with exact identities
            A-->>U: REST result or stable reference
        end
    end
```

**Failure reading:** Long or unpredictable work is rejected as synchronous and submitted through the durable-job path. No synchronous call trains, promotes, activates, bypasses blocked profiles, or treats telemetry as authoritative evidence.

## Diagram 4 — Asynchronous durable-job flow

```mermaid
sequenceDiagram
    autonumber
    actor U as Consumer / scheduler
    participant A as Capability and job API / C05-05
    participant J as Job manager / C05-08
    participant DB as PostgreSQL job schemas / C05-13
    participant W as Worker / C05-10
    participant P as Policy + readiness / C05-04,07
    participant C as Capability or data handler / C05-06,11
    participant O as Owned result/object stores / C05-14,15
    participant E as Audit + usage / C05-18
    participant D as Result delivery / C05-12

    U->>A: Submit typed operation with idempotency key
    A->>P: Admission checks
    alt Admission fails
        A-->>U: Typed denial, no job created
    else Admission passes
        A->>J: Create or replay one logical job
        J->>DB: Atomic job + occurrence/idempotency state
        J-->>U: 202 + stable job reference
        W->>DB: Claim eligible job attempt with lease/fence
        DB-->>W: Attempt identity, deadline and scoped context
        W->>P: Recheck current authority, readiness and assignment
        alt Revoked, stale, blocked or incompatible
            W->>DB: Terminal/held outcome with exact reason
        else Executable
            W->>C: Invoke versioned public handler
            C->>O: Write candidate/result under attempt fence
            C-->>W: Candidate reference + evidence
            W->>DB: FINALIZING compare-and-set
            W->>E: Commit required audit/lineage/usage evidence
            W->>DB: Commit terminal result exactly once logically
            D-->>U: Polling exposes authoritative result/status
        end
        Note over W,DB: Crash or lease expiry creates a new attempt, stale fences cannot finalize
        Note over C,O: Ambiguous external effects are reconciled, never blindly retried
    end
```

**State reading:** Attempts are at least once; the logical job/result/effect is idempotent. PostgreSQL owns job truth. Worker process death, response loss, or lease expiry cannot fabricate success or authorize a stale attempt.

## Diagram 5 — Proactive ML insight and event-delivery flow

```mermaid
flowchart TD
    Trigger["Versioned schedule or approved explicit trigger"]
    PhaseA{"Phase A admission\nsubscription + grant + entitlement + quota + freshness"}
    Job["Durable evaluation job\nC05-08 / C05-10"]
    Cap["Capability evaluation\nC05-11\nblocked profiles remain unavailable"]
    Insight["Immutable insight/result\nmodel or verifier is advisory"]
    PhaseB{"Phase B decision\npolicy + threshold + cooldown + dedupe + destination"}
    Audit{"Mandatory audit commit available?"}
    Intent["Typed task or notification intent\nstable effect identity"]
    EffectCheck{"At-effect recheck\ncurrent authority + destination + expiry"}
    Outbox["Conditional PostgreSQL publication/delivery state\nC05-21; no broker selected"]
    Receiver["Approved external receiver"]
    Poll["Authoritative polling / insight API"]
    Stop["REPORT_ONLY / suppressed / blocked\nreason recorded; zero external effect"]
    Ambiguous["AMBIGUOUS / retry / reconcile / dead-letter\noriginal insight remains true"]

    Trigger --> PhaseA
    PhaseA -->|"deny / ambiguous"| Stop
    PhaseA -->|"allow"| Job
    Job --> Cap
    Cap --> Insight
    Insight --> Poll
    Insight --> PhaseB
    PhaseB -->|"deny / stale / quota / dedupe"| Stop
    PhaseB -->|"allow"| Audit
    Audit -->|"unavailable"| Stop
    Audit -->|"committed"| Intent
    Intent --> EffectCheck
    EffectCheck -->|"revoked / expired / invalid destination"| Stop
    EffectCheck -.->|"admitted delivery path only"| Outbox
    Outbox -.->|"signed at-least-once attempt"| Receiver
    Receiver -.->|"timeout or lost acknowledgement"| Ambiguous
    Ambiguous -.-> Outbox
```

**Authority reading:** Capability, ML, LLM, verifier, insight, event, and transport never grant permission. Phase A, Phase B, mandatory audit, and the at-effect recheck are ordered and fail closed. Delivery retry never reruns capability work or changes result truth.

## Diagram 6 — Data lifecycle

```mermaid
flowchart LR
    Source["Authoritative source + approved source contract"]
    Block{"DATA_CONTRACT_ADMISSION_BLOCKED cleared?"}
    Stage["Upload staging\nnot evidence / never ready"]
    Raw["Immutable raw landing\nreceipt + checksum"]
    Structural{"1. Structural validity\ningestion authority"}
    Quarantine["Quarantine + reason report\nnever ready"]
    Validated["Validated source-aligned version"]
    Semantic{"2. Semantic validity\ndomain authority"}
    Canonical["Immutable canonical candidate"]
    Ready{"3. Dataset readiness\ndata-platform authority"}
    Catalog["READY catalog version\nlineage + policy + quality"]
    Eligible{"4. Capability eligibility\ncapability authority"}
    Feature["Versioned feature / label materialization\ncapability-owned"]
    Model["Exact model / artifact assignment\nMIGRATION or EVIDENCE blocks still apply"]
    Result["Authoritative prediction / result"]
    Feedback["Attributed feedback / outcomes\nmissing is not negative"]
    Revoke["Correction / tombstone / deletion / revocation manifest"]
    Evidence["Audit + lineage + usage evidence"]

    Source --> Block
    Block -->|"no"| Quarantine
    Block -->|"yes: push / referenced bulk"| Stage --> Raw --> Structural
    Structural -->|"fail"| Quarantine
    Structural -->|"pass"| Validated --> Semantic
    Semantic -->|"fail"| Quarantine
    Semantic -->|"pass"| Canonical --> Ready
    Ready -->|"NOT_READY / STALE / REVOKED"| Quarantine
    Ready -->|"READY"| Catalog --> Eligible
    Eligible -->|"INELIGIBLE / DEGRADED / FALLBACK"| Evidence
    Eligible -->|"ELIGIBLE"| Feature --> Model --> Result --> Feedback
    Raw --> Evidence
    Catalog --> Evidence
    Feature --> Evidence
    Model --> Evidence
    Result --> Evidence
    Feedback --> Evidence
    Revoke --> Raw
    Revoke --> Catalog
    Revoke --> Feature
    Revoke --> Model
    Revoke --> Result
```

**Lifecycle reading:** Structural validity, semantic validity, dataset readiness, and capability eligibility are four independent owner decisions. Published content is immutable but may be superseded, revoked, or deleted through an authoritative lineage-driven workflow. No generic `valid` or `ready` flag collapses these gates.

## Diagram 7 — Provisional deployment architecture

```mermaid
flowchart TB
    Internet["Approved consumer ingress"]
    Admin["Sponsor/operator administrative boundary\nstronger auth + audit"]
    CI["Build/release evidence\nimmutable Python release"]

    subgraph Host["Provisional one Linux server / one failure domain\nDEPLOYMENT_ENVIRONMENT_BLOCKED"]
        API["api role\nC05-02,03,04,05,12"]
        Scheduler["scheduler role\nC05-09"]
        Worker["worker-general role\nC05-10"]
        DataWorker["worker-data role\nconditional split"]
        MLWorker["worker-ml role\nconditional; profiles blocked"]
        Maintenance["maintenance-migration\none-shot privileged role"]
        Publisher["publisher-delivery role\nnot deployed until admitted"]
        Workflow["workflow-coordinator role\nnot deployed until named"]
    end

    PG[("Environment-provided PostgreSQL contract\nshared cluster; owned schemas")]
    Obj[("Environment-provided object-storage contract\nprovider/production placement unresolved")]
    Trust["Identity / secrets / config contracts\nsecurity blocks active"]
    Telemetry["Audit and telemetry contracts\nconcrete sinks/retention unresolved"]
    Egress["Exact approved provider/destination egress\ndeny by default"]

    Internet -->|"authenticated encrypted REST/JSON"| API
    Admin --> Maintenance
    CI --> API
    CI --> Scheduler
    CI --> Worker
    API --> PG
    API --> Obj
    Scheduler --> PG
    Worker --> PG
    Worker --> Obj
    DataWorker -.-> PG
    DataWorker -.-> Obj
    MLWorker -.-> PG
    MLWorker -.-> Obj
    Maintenance --> PG
    Maintenance --> Obj
    Trust --> API
    Trust --> Scheduler
    Trust --> Worker
    API --> Telemetry
    Scheduler --> Telemetry
    Worker --> Telemetry
    Publisher -.-> Egress
    Workflow -.-> PG
```

**Placement reading:** Roles may be supervised processes or optional simple containers from the same release. Conditional role boxes are not initially deployed. The drawing makes no HA, RPO/RTO, server-size, provider, network-product, or production-fitness claim; Kubernetes remains unselected.

## Analysis and recommendations

### R-19-01 — Keep diagram edges at logical-contract granularity

**Requirement/where:** source Section 18 readability; Stages 19, 21, and 23. **Why now:** the approved design has many contracts but few initial deployment units. **Simplest implementation:** show stable `C05-*` boundaries, owner stores, trust boundaries, and critical transitions without expanding every schema or operation. **Alternative:** one exhaustive diagram. **Why rejected:** it would obscure authority and failure order. **Trade-off:** readers consult the written stages for field-level detail. **Reconsideration:** a later deliverable requires a bounded use-case-specific execution diagram.

### R-19-02 — Show unavailable and conditional paths without depicting them as active

**Requirement/where:** ADR-007/008/011/015 and Stage 19 accuracy. **Why now:** conventional diagrams can falsely imply that providers, webhooks, publishers, ML workers, or cutovers are deployed. **Simplest implementation:** dashed arrows and explicit block labels. **Alternative:** omit blocked paths. **Why rejected:** omission would hide intended seams and safety conditions. **Trade-off:** legends must be read. **Reconsideration:** a block is explicitly cleared and the path becomes part of an admitted release.

### R-19-03 — Preserve authority separately from transport and placement

**Requirement/where:** ADR-003/005/006/010; every flow. **Why now:** a shared cluster, HTTP call, job, or event can be mistaken for ownership. **Simplest implementation:** label owner components and authoritative commits; treat arrows as logical contracts. **Alternative:** diagram only physical runtime nodes. **Why rejected:** physical placement cannot express policy/scientific/data authority. **Trade-off:** deployment and logical views must be read together. **Reconsideration:** none; authority remains explicit under any topology.

## Decisions

- Adopt the seven diagrams above as the Stage 19 visual representation of the approved architecture baseline.
- Use `C05-*` component names and accepted ADR terminology as the canonical visual vocabulary.
- Treat dashed paths as conditional, blocked, or supporting exactly as labeled; they are not production admission.
- Create no new ADR because Stage 19 introduces no material mechanism, topology, product, protocol, or authority decision.
- Do not begin Stage 20 without the user's next explicit instruction.

## Contradictions and dangerous assumptions

| ID | Finding | Resolution | Consequence |
|---|---|---|---|
| `C-19-01` | Mermaid arrows can look like network calls | Diagram convention says logical contract unless a trust/deployment boundary is explicit | Modules are not silently converted into services |
| `C-19-02` | Shared PostgreSQL can look like shared ownership | Diagram 2 labels owned schemas/writers and typed owner commands | No cross-module write/join authority |
| `C-19-03` | Provider/webhook/publisher paths can look enabled | Dashed paths carry explicit active block labels | No external call or delivery is authorized |
| `C-19-04` | The deployment diagram can look production-ready | Host is labeled provisional, single failure domain, and deployment-blocked | No HA, RPO/RTO, sizing, or production claim |
| `C-19-05` | Proactive “ML event” can imply model authority | Diagram 5 places deterministic gates and audit outside capability output | Model/verifier remains advisory |
| `C-19-06` | A data pipeline can collapse four acceptance decisions | Diagram 6 gives each gate its own owner/outcome | Readiness never implies scientific eligibility |
| `C-19-07` | Retry can look exactly-once | Diagram 4 distinguishes at-least-once attempts from one logical result/effect | Stale attempts and ambiguous effects remain explicit |

## Open questions

| ID | Question | Blocking effect | Current disposition |
|---|---|---|---|
| `Q-19-01` | Which capability and consumer form the first implementation slice? | Blocks roadmap specificity, not these diagrams | Stage 20 must keep sequencing conditional unless evidence answers it |
| `Q-19-02` | What exact production hosting, identity, secrets, object storage, telemetry, backup, and network mechanisms apply? | Blocks concrete production deployment diagram | Preserve ADR-008/009 and deployment blocks |
| `Q-19-03` | Which source contracts, consumers, webhooks, workflows, and external providers are admitted? | Blocks activation of dashed paths | Preserve data-contract, cutover, delivery, provider, and ownership blocks |
| `Q-19-04` | What numeric workload, SLO, recovery, retention, and cost profiles apply? | Blocks sizing and production topology | Preserve `CAPACITY_ADMISSION_BLOCKED` and Stage 17 benchmark process |

## Requirements-traceability updates

| Requirement/decision | Diagram evidence |
|---|---|
| `ARK-CON-001/002/003`, ADR-003/010 | Diagrams 1, 2, and 7 show modular boundaries and owned shared infrastructure |
| `ARK-FR-002/003`, ADR-011 | Diagrams 1 and 6 show push/bulk intake and source-contract admission |
| `ARK-FR-004–008`, ADR-004/005/015 | Diagrams 3 and 4 show sync versus durable job execution |
| `ARK-FR-009`, ADR-007/012 | Diagrams 2 and 6 show capability-owned features, registry, exact assignment, and blocks |
| `ARK-FR-010/011`, ADR-006/013 | Diagram 5 shows deterministic proactive authority and advisory ML/LLM |
| `ARK-NFR-001/005`, ADR-008 | All diagrams preserve principal-derived tenant and fail-closed boundaries |
| `ARK-NFR-004`, ADR-005/006 | Diagrams 4 and 5 show retries, fences, audit, ambiguity, and delivery separation |
| `ARK-NFR-007`, ADR-009/014 | Diagram 7 shows the provisional minimal deployment without production-fitness claims |
| Prompt Section 18 | Seven numbered Mermaid diagrams above |

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| All seven required diagrams present | PASS | Diagrams 1–7 |
| Stable component names | PASS | `C05-*` labels match Stage 05 inventory |
| Trust and tenant boundary visible | PASS | Context, sync, logical, and deployment diagrams |
| Async job authority/retry visible | PASS | Diagram 4 |
| Proactive ordering and delivery separation visible | PASS | Diagram 5 |
| Four data acceptance gates visible | PASS | Diagram 6 |
| Conditional/blocked paths not represented as active | PASS | Dashed-arrow convention and explicit labels |
| No later-stage roadmap or product choice introduced | PASS | Decisions and open questions |
| Mermaid fence and structural validation | PASS | Seven `mermaid` fences; balanced blocks and supported diagram types checked by workspace validation |
| Visual render validation | PASS | All seven diagrams rendered successfully with the local Mermaid renderer; no syntax error |

**Gate result: PASS.** All seven required Mermaid diagrams render, use stable names, preserve ownership and trust/async boundaries, and agree with the approved contracts. Stage 19 is complete. Stage 20 remains unstarted.

## Downstream consequences

- Stage 20 must reference these diagrams when defining the walking skeleton, MVP, hardening, and scale-triggered phases; it must not turn dashed/blocked paths into committed scope.
- Stage 21 may reuse these diagrams provisionally but must preserve labels, blocks, and traceability.
- Stage 22 must add the required use-case runtime/execution views without changing component ownership or deployment admission.
- Stage 23 must publish the final diagram artifact from approved stage outputs and reapply the anti-overengineering test.
- Stage 24 must independently verify diagram-to-contract consistency.

## Exact next-stage inputs

Stage 19 is complete. Do not execute Stage 20 until explicitly instructed.

When authorized, Stage 20 must read:

1. Approved `outputs/stages/00-source-audit.md` through `outputs/stages/19-diagrams.md`
2. Accepted ADR-000 through ADR-015 and the Stage 18 effective decision register
3. `sources/normalized/system-design-prompt.md — 19. Implementation roadmap`
4. `stages/20-roadmap.md`
5. All active production-admission blocks, unresolved ownership/scope questions, and measurable ADR reconsideration triggers

Stage 20 must produce only `outputs/stages/20-roadmap.md` and stop before Stage 21.

## Approval record

The sponsor explicitly approved Stage 19 as written on 2026-08-13 and authorized execution of Stage 20 only.
