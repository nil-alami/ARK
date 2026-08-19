# ARK knowledge system implementation guide

Source: `sources/original/ARK knowledge system.docx`

Normalization date: 2026-08-16

## Normalization and authority note

This working copy preserves the implementation concepts supplied by the sponsor. It is implementation guidance, not an instruction to the reader and not, by itself, an accepted architecture decision. Examples such as Kafka, Redis, Celery, NBA, TTS, Direct, POS, WhatsOn, and sample ADR numbers illustrate the proposed knowledge-system mechanics; they do not select technologies, add capabilities, identify production consumers, or supersede accepted ADRs.

## Purpose

The ARK knowledge system should let humans and tools answer four different questions without searching or loading the entire architecture corpus:

1. What is this architectural entity?
2. What structured facts should tools know about it?
3. How should this family of entities be implemented?
4. Why was the governing architectural choice made?

The proposed artifacts are identity documents, small structured manifests, implementation patterns, ADRs, and a task-aware context resolver.

## Identity documents

Identity documents live close to the entity they describe. Not every directory receives one; only architecturally meaningful systems, contexts, modules, and substantial subcomponents do. Ordinary classes, repositories, helpers, and packages should normally explain themselves through code and ordinary documentation.

| Level | Artifact | Example |
|---|---|---|
| System | `ARK.md` | ARK as a whole |
| Architectural context | `CONTEXT.md` | Platform, Capabilities, Data, Execution |
| Module | `MODULE.md` | Recommendation, Jobs, IAM |
| Important subcomponent | `COMPONENT.md` | Recommendation Ranking |

The documents share a recognizable structure: purpose, responsibilities, non-responsibilities, public contracts, dependencies, state/data ownership, tenant scope, important flows, events, invariants, and related ADRs.

Documentation references executable or versioned contracts; it does not redefine those contracts. In particular, `MODULE.md` links to request, response, event, and storage contracts rather than becoming their canonical schema.

### System identity

`ARK.md` explains ARK's purpose, major boundaries, architectural style, major contexts, major flows, global invariants, system-wide rules, and major ADRs.

### Context identity

`CONTEXT.md` represents a major architectural area. Candidate views include Platform, Capabilities, Data, Execution, Integration/API, and Observability. It records the area's purpose, member modules, responsibility boundary, module interactions, cross-context dependencies, and important rules.

### Module identity

`MODULE.md` is a module's human-readable identity card. The Recommendation example describes:

- its purpose: produce ranked product recommendations for a business;
- responsibilities: accept recommendation requests, establish execution requirements, generate candidates, rank, apply Recommendation-owned policies, and return results;
- non-responsibilities: authentication, tenant ownership, organization permissions, direct credit debit, platform ingestion, and durable job infrastructure;
- versioned request and result contracts;
- dependencies on dataset, eligibility, entitlement, job, metering, and observability boundaries;
- owned runs and results, and explicitly unowned organization, business, credit, and dataset state;
- the core validation-to-result flow;
- business tenant scope;
- produced completion/failure events;
- related ADRs.

### Component identity

`COMPONENT.md` is reserved for a substantial internal concept with its own responsibility boundary. It is not required for every internal package or class.

## Structured module manifest

Each architecturally meaningful module may carry a deliberately small `module.yaml`. The manifest exists for automation; it is not another prose document and is not runtime authorization truth.

Minimum useful fields from the supplied example are:

```yaml
id: recommendation
name: Recommendation
kind: capability
parent: capabilities
tenant_scope: business
pattern: capability-module-v1

identity: MODULE.md

provides_contracts:
  - contracts/RecommendationRequestV1
  - contracts/RecommendationResultV1

depends_on:
  - datasets
  - eligibility
  - entitlements
  - jobs
  - metering

owns_data:
  - recommendation_runs
  - recommendation_results

emits:
  - RecommendationCompletedV1
  - RecommendationFailedV1

related_adrs:
  - ADR-004
```

Tools should be able to answer which modules depend on a boundary, which modules are business-scoped, which implementation pattern governs a module, which contracts it provides, and which events it emits without asking an LLM to infer those facts from prose.

A global architecture registry may later be generated from module manifests. It must not be maintained manually in parallel with the manifests.

## Architecture decision records

An ADR records why a significant architectural choice exists, the alternatives considered, and its consequences. Identity documents state the current truth and link to the ADR; they do not reproduce the ADR's rationale.

The supplied examples illustrate business as the tenant/data-isolation boundary and capability-owned, consumer-neutral versioned contracts. Example numbering and wording must be reconciled with the repository's actual accepted ADR inventory rather than copied as new decisions.

## Implementation patterns

Patterns describe how a family of ARK modules should be built. A module selects its governing pattern in `module.yaml`. Shared conventions belong in the pattern; module-specific business logic remains in the module identity and code.

Candidate pattern families include platform modules, capability modules, worker/execution modules, orchestration modules, and integration modules. Only a pattern with concrete requirements should be created; unusual modules should use a local `DEVELOPMENT_OVERRIDES.md` rather than causing a new pattern for every exception.

### Capability module pattern v1

The supplied capability pattern proposes this structure:

```text
capability/
├── domain/
├── application/
├── contracts/
├── infrastructure/
├── api/
├── tests/
├── MODULE.md
└── module.yaml
```

The domain contains entities, policies, value objects, and domain services. It must not import transport, ORM, task-queue, or HTTP-client frameworks.

The application layer contains use cases, commands, queries, orchestration, and ports/interfaces. Contracts contain versioned externally visible request, response, and event schemas. Infrastructure implements external dependencies such as repositories, publishers, caches, and model clients when those products and adapters are actually selected. API code translates transport requests into application calls and contains no business logic.

The dependency direction is:

```text
API -> Application -> Domain
Infrastructure -> application/domain ports
```

Domain never depends on infrastructure. The pattern does not select a capability algorithm or model.

## ARK Context Resolver

The Context Resolver is a small architecture-aware search/router in the repository tooling layer. Given a task and target module, it identifies the minimum architecture knowledge required and returns a context package rather than the complete ARK corpus.

For a target module, the base package contains:

- entity identity (`MODULE.md`);
- structured metadata (`module.yaml`);
- the selected implementation pattern;
- related versioned contracts;
- identities/public contracts of relevant dependencies;
- applicable ADRs.

Task-aware routing then narrows or expands that package. For example, an eligibility change in Recommendation needs Recommendation identity, Eligibility identity, the relevant dataset contract, the capability pattern, dependency rules, and governing ADRs. It does not need unrelated Synapse, TTS, NPT-internal, or gateway implementation documents.

The resolver should return paths and reasons before content is loaded. Missing manifests, duplicate module IDs, unresolved dependencies, missing contracts, or missing ADR links should fail visibly rather than be guessed.

## Change workflow

When module behavior changes, update the implementation and tests plus `MODULE.md`; update `module.yaml` only when structured facts change.

When an architectural decision changes, create or supersede an ADR and then update affected identity documents and manifests to represent the new current truth.

When a shared implementation convention changes, update the applicable pattern. Do not edit every module unless its implementation must migrate.

When one module requires an exception, create or update its `DEVELOPMENT_OVERRIDES.md`.

User-visible or historical changes belong in the appropriate changelog.

## Agent consumption

The normal flow is:

```text
Task + target
  -> ARK Context Resolver
  -> identity + manifest + pattern + contracts + dependencies + ADRs
  -> coding agent
```

The manifest is a fast index, not a substitute for authoritative contracts or ADRs. The resolver determines which deeper artifacts are needed for the task. It must preserve source and decision precedence, must not treat generated indexes as authoritative, and must not use documentation metadata to grant runtime authority or production admission.

