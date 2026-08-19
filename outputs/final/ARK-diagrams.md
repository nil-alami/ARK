# ARK architecture diagrams — ADR-017/018 publication revision

Status: `POST-PUBLICATION REVISION — ADR-017/018 ACCEPTED; INDEPENDENT RE-ASSURANCE PENDING`

Legend: solid paths are required logical contracts; dashed paths are conditional, blocked or supporting. A box is not necessarily a separately deployed service. Red/block labels mean unavailable, not planned work.

## 1. System context

```mermaid
flowchart LR
    Consumer["Consumer systems / adapters"] -->|REST/JSON invoke, submit, poll| ARK["ARK capability platform"]
    Source["Authoritative source platforms"] -->|push / referenced bulk| ARK
    Sponsor["Human ARK sponsor"] -->|Phase 1 decisions and review| ARK
    LAB["LAB evidence consumer"] -->|contracts and minimized evidence| ARK
    ARK -->|result resources / polling| Consumer
    ARK -. blocked conditional webhook .-> Consumer
    Provider["External LLM provider"] -. LLM_PROVIDER_BLOCKED .-> ARK
    Ops["Future named operations/security authorities"] -. unassigned .-> ARK
```

## 1a. Account, organization, business, and capability-pattern scope

```mermaid
flowchart LR
    Account["Andrew account"] -->|owns / active membership| Direct["Direct organization"]
    Admin["Direct admin membership"] -->|organization-scoped administration| Direct
    Direct --> Pattern["One versioned capability pattern: RFM + Churn"]
    Direct --> B1["Business A — tenant"]
    Direct --> B2["Business B — tenant"]
    Direct --> BN["Business 1000 — tenant"]
    Pattern -->|uniform eligibility| B1
    Pattern -->|uniform eligibility| B2
    Pattern -->|uniform eligibility| BN
    Admin -->|may change pattern| Pattern
    B1 -. "no implicit data combination" .-> B2
    B2 -. "no implicit data combination" .-> BN
```

An organization is the administrative/entitlement container; each business is an isolated tenant. Organization-wide admin scope permits access to every member business only through a separately derived one-business context. It does not authorize an untyped cross-business dataset, query, job, result, or export.

## 1b. Shared owner billing account and organization credit policies

```mermaid
flowchart TB
    Owner["Owner / customer account"] --> Billing["Shared billing account — 500,000 credits"]
    Billing --> OrgA["Organization A policy — 100k/month"]
    Billing --> OrgB["Organization B policy — 250k/month"]
    Billing --> OrgC["Organization C policy — no organization ceiling"]
    OrgA --> BA1["Business A1 — tenant"]
    OrgA --> BA2["Business A2 — tenant"]
    OrgB --> BB1["Business B1 — tenant"]
    OrgB --> BB2["Business B2 — tenant"]
    OrgC --> BC1["Business C1 — tenant"]
    BA1 --> Cap["Capability usage"]
    BA2 --> Cap
    BB1 --> Cap
    BB2 --> Cap
    BC1 --> Cap
    Cap --> Job["Durable job + credit reservation / usage event"]
```

Organizations have policy ceilings, not balances or wallets. Every admitted job must pass both its organization's effective policy and the owner's shared available-balance check. The numeric labels illustrate the sponsor example and are not ARK defaults.

## 2. Logical component architecture

```mermaid
flowchart TB
    subgraph API["API role"]
        Edge["Edge + organization membership + business AuthContext"]
        Control["Account / organization / business / pattern + billing / credit policy / reservation"]
        Contract["Capability + job API"]
        ResultAPI["Polling / result API"]
        Admin["Admin / operations interfaces"]
    end
    subgraph Core["Boundary-enforced modules"]
        Ingest["Ingestion + validation"]
        Catalog["Dataset catalog / readiness"]
        Jobs["Durable job manager"]
        Caps["Seven capability contracts"]
        CapState["Capability feature / result / state"]
        Registry["Artifact / evaluation / assignment registry"]
        Evidence["Audit / lineage / usage / credit ledger"]
        ResultDelivery["Result + conditional notification boundary"]
        Outbox["Reliable publication / outbox — conditional"]
    end
    subgraph Roles["Same-release runtime roles"]
        Worker["worker-general"]
        Scheduler["scheduler — outside Phase 1"]
        Publisher["publisher-delivery — absent"]
        Workflow["workflow coordinator — absent"]
        Maintenance["maintenance / migration"]
    end
    PG[("PostgreSQL — owned schemas")]
    Obj[("Immutable object-storage contract")]
    Config["Secrets + technical configuration contract"]
    Telemetry["Buffered diagnostic telemetry"]
    Edge --> Control --> Contract
    Contract --> Jobs
    Contract --> Catalog
    Contract --> Caps
    Contract --> ResultDelivery
    Jobs <--> Worker
    Worker --> Ingest
    Worker --> Caps
    Ingest --> Catalog
    Caps --> CapState
    Caps --> Registry
    Registry -->|exact assignment / authorized selection| Caps
    Catalog --> PG
    Jobs --> PG
    Control --> PG
    Registry --> PG
    Evidence --> PG
    CapState --> PG
    ResultDelivery --> PG
    Outbox --> PG
    Ingest --> Obj
    Caps --> Obj
    CapState --> Obj
    Registry --> Obj
    Contract --> ResultAPI
    ResultAPI --> ResultDelivery
    Admin --> Control
    Admin --> Jobs
    Admin --> Catalog
    Admin --> Registry
    Scheduler -. typed SubmitJob .-> Jobs
    Outbox -. admitted intent only .-> Publisher
    Publisher -. delivery state .-> ResultDelivery
    Workflow -. public child jobs only .-> Jobs
    Maintenance --> PG
    Config --> API
    Config --> Roles
    Control --> Evidence
    Jobs --> Evidence
    Ingest --> Evidence
    Catalog --> Evidence
    Caps --> Evidence
    Registry --> Evidence
    ResultDelivery --> Evidence
    API -. buffered .-> Telemetry
    Core -. buffered .-> Telemetry
```

## 3. Synchronous request flow — target contract only

```mermaid
sequenceDiagram
    actor Consumer
    participant API
    participant Auth as Auth + control
    participant Data as Catalog / assignment metadata
    participant Cap as Capability owner
    participant Audit as Mandatory evidence
    participant Result as Result owner
    Consumer->>API: typed :invoke
    API->>Auth: derive tenant and authorize
    par safe prerequisite reads
        API->>Data: exact READY dataset refs
        API->>Data: exact assignment/config if applicable
    end
    API->>Cap: scientific eligibility
    opt policy-classified sensitive work
        API->>Audit: commit pre-effect audit
    end
    API->>Cap: bounded execution
    Cap->>Result: commit immutable result
    Result->>Audit: verify completion obligations
    API-->>Consumer: authoritative response
```

No current capability profile is admitted to production synchronous execution. Under ADR-018, every credit-consuming execution requires a durable logical job/reservation identity; `:invoke` remains unpriced/zero-credit unless a later contract preserves the same job and financial truth.

## 4. Durable asynchronous flow

```mermaid
sequenceDiagram
    actor Consumer
    participant API
    participant Control
    participant Catalog as Dataset catalog/readiness
    participant Jobs as PostgreSQL job manager
    participant Worker
    participant Cap as Capability/result owner
    participant Registry as Assignment registry
    participant Credit as Organization policy + owner balance
    participant Evidence
    Consumer->>API: submit + idempotency key
    API->>Control: derive organization/business scope; check pattern and exact command/refs
    API->>Catalog: check exact dataset version is READY
    API->>Registry: check exact assignment/version and revocation
    API->>Cap: check capability eligibility
    API->>Credit: check organization policy + shared owner balance
    rect rgb(235, 245, 255)
        API->>Credit: create active credit reservation
        API->>Jobs: commit one logical job
    end
    Jobs-->>API: durable job id
    API-->>Consumer: 202 + polling URLs
    Worker->>Jobs: claim leases and fenced attempt
    Jobs-->>Worker: exact handler + fence
    Worker->>Control: recheck membership, business parent, pattern, entitlement, grant, policy and quota
    Worker->>Credit: recheck active reservation/current financial authority
    Worker->>Catalog: recheck exact dataset version is READY
    Worker->>Registry: recheck exact assignment/version and revocation
    Worker->>Cap: recheck capability eligibility for exact inputs
    opt sensitive work
        Worker->>Evidence: pre-effect audit
    end
    Worker->>Cap: execute public handler
    Cap->>Cap: commit owner result
    Cap-->>Jobs: result ref
    Worker->>Credit: settle unique usage + release unused reservation
    Jobs->>Evidence: link completion evidence
    Jobs->>Jobs: FINALIZING to SUCCEEDED
    Consumer->>API: poll
    API-->>Consumer: job/result truth
```

Only the synthetic `POA_FIXTURE_ONLY` Phase 1 path is immediately runnable, and only in validation.

## 5. Proactive insight and conditional delivery

```mermaid
flowchart TD
    Trigger["Schedule, explicit request, or admitted fact"] --> A{"Phase A: provenance, subscription, grant, data, quota, dedupe, audit"}
    A -->|deny| Stop["No evaluation job"]
    A -->|admit| Job["Durable evaluation job"]
    Job --> Insight["Immutable insight + lineage"]
    Insight --> B{"Phase B: current authority, freshness, threshold, policy, reservation, dedupe, audit"}
    B -->|report/suppress| Report["Queryable insight; no intent"]
    B -->|authorize| Intent["Typed decision + delivery intent"]
    Intent -. asynchronous .-> Recheck{"At-effect destination, policy, egress and secret recheck"}
    Recheck -->|fail| NoSend["Suppress/reconcile; zero send"]
    Recheck -->|pass| Hook["Signed webhook attempt"]
    Hook --> Outcome{"Confirmed or ambiguous"}
    Outcome --> Delivery["Separate delivery state / retry / dead-letter"]
```

The path is inactive and `EXTERNAL_DELIVERY_BLOCKED`; webhook outcome never changes insight/result truth.

## 6. Data lifecycle

```mermaid
flowchart LR
    Source["Registered source contract"] --> Raw["Immutable raw evidence"]
    Raw --> Structural{"Structural validation"}
    Structural -->|fail| Quarantine["Quarantine + report"]
    Structural -->|pass| Semantic{"Semantic validation"}
    Semantic -->|fail| Quarantine
    Semantic -->|pass| Candidate["Canonical candidate version"]
    Candidate --> Ready{"Dataset readiness publication"}
    Ready -->|fail| Hidden["Not READY / undiscoverable"]
    Ready -->|pass| Dataset["Immutable READY dataset version"]
    Dataset --> Eligibility{"Capability eligibility"}
    Eligibility -->|ineligible| Outcome["Explicit ineligible/degraded outcome"]
    Eligibility -->|eligible and admitted| Job["Capability job"]
    Job --> Result["Immutable result + lineage"]
    Result -. governed feedback .-> Feedback["Versioned feedback/outcome"]
    Feedback -. candidate trigger only .-> Train["Lifecycle admission"]
```

The synthetic Phase 1 contract does not clear `DATA_CONTRACT_ADMISSION_BLOCKED`.

## 7. Provisional deployment architecture

```mermaid
flowchart TB
    Internet["Approved ingress — production mechanism blocked"] --> API["api process"]
    subgraph Linux["One provisional Linux server / one failure domain"]
        API
        Worker["worker-general"]
        Scheduler["scheduler — activate only when selected"]
        Maint["one-shot maintenance/migration"]
        Publisher["publisher-delivery — not deployed"]
        Workflow["workflow coordinator — not deployed"]
    end
    API --> PG[("PostgreSQL contract")]
    Worker --> PG
    Scheduler --> PG
    Maint --> PG
    Worker --> Obj[("Object-storage contract")]
    API --> Config["Identity / secrets / config contracts"]
    Worker --> Config
    Linux -. buffered .-> Obs["Telemetry backend — mechanism unknown"]
    Backup["Backup / restore / recovery mechanism unknown"] -.-> PG
    Backup -.-> Obj
```

This diagram makes no HA, RPO/RTO, capacity, provider, network or production-fitness claim. Containers are optional and Kubernetes is not selected.

## Diagram provenance and validation

| Diagram | Exact approved basis |
|---|---|
| 1. System context | `outputs/stages/19-diagrams.md — Diagram 1 — System context`; `outputs/stages/02-system-definition.md — System boundary` |
| 1a. Account/organization/business scope | `sources/sponsor-decisions/2026-08-15-owner-organization-business.md`; accepted ADR-017 |
| 1b. Shared owner billing/organization credit policy | `sources/sponsor-decisions/2026-08-15-owner-billing-credit-management.md`; accepted ADR-018 |
| 2. Logical architecture | `outputs/stages/19-diagrams.md — Diagram 2 — Logical container/component architecture`; `outputs/stages/05-end-to-end-architecture.md — Component inventory`; `outputs/stages/22-runtime-execution-analysis.md — Runtime element usage and placement matrix` |
| 3. Synchronous request | `outputs/stages/19-diagrams.md — Diagram 3 — Synchronous request flow`; `outputs/stages/22-runtime-execution-analysis.md — UC-22-01 — Synchronous inference` |
| 4. Durable asynchronous job | `outputs/stages/19-diagrams.md — Diagram 4 — Asynchronous durable-job flow`; `outputs/stages/22-runtime-execution-analysis.md — UC-22-02 — Asynchronous inference or batch job` |
| 5. Proactive action | `outputs/stages/19-diagrams.md — Diagram 5 — Proactive ML insight and event-delivery flow`; `outputs/stages/09-events-proactive-actions.md — Two-phase fail-closed decision order`; `outputs/stages/22-runtime-execution-analysis.md — UC-22-05 — Proactive insight and webhook delivery` |
| 6. Data lifecycle | `outputs/stages/19-diagrams.md — Diagram 6 — Data lifecycle and ML feedback`; `outputs/stages/06-data-architecture.md — Concrete data lifecycle — transaction file to recommendation result`; `outputs/stages/06-data-architecture.md — Four-layer acceptance model` |
| 7. Deployment | `outputs/stages/19-diagrams.md — Diagram 7 — Provisional deployment architecture`; `outputs/stages/15-deployment-infrastructure.md — Deployable runtime-role matrix` |

The original seven assembled Mermaid charts rendered successfully on 2026-08-14 with Mermaid CLI 11.16.0. Stage 24 independently verified their visual-to-contract consistency after the asynchronous authority-order repair. Diagrams 1a/1b and the ADR-017/018 label/flow revisions were added after that assurance and require render verification plus independent re-assurance. The transferred Windows environment could not relaunch the CLI during the original closure; `outputs/stages/24-final-assurance.md — Accepted residual risks` records that historical tooling limitation.
