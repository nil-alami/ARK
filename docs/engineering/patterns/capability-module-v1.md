# Capability module pattern v1

Status: `PROPOSED IMPLEMENTATION PATTERN`

## Applies to

Capability modules that own a versioned operation contract and capability-specific behavior. Applying this pattern does not activate a capability or establish scientific or production readiness.

## Required structure

```text
<capability>/
├── domain/
├── application/
├── contracts/
├── infrastructure/
├── api/
├── tests/
├── MODULE.md
├── module.yaml
└── DEVELOPMENT_OVERRIDES.md      # only when a local exception exists
```

Small modules may use files instead of empty directories, but the responsibility and dependency boundaries remain the same.

## Responsibilities by layer

### Domain

Own capability entities, value objects, policies, domain services, and scientific/business eligibility rules. Do not import FastAPI, SQLAlchemy, task queues, HTTP clients, or infrastructure implementations.

### Application

Own use cases, commands, queries, orchestration, and ports. Coordinate the capability's work without bypassing platform authority or writing another module's state.

### Contracts

Own versioned capability-specific request, response/result, and event schemas. Consumer-specific translation remains outside the capability core.

### Infrastructure

Implement declared ports for capability-owned persistence, objects, models, providers, or publication. An example technology in documentation is not permission to add that product.

### API

Translate an admitted transport request into an application call. Keep authentication derivation, generic tenant resolution, billing, job lifecycle, and transport error mapping in their owning platform boundaries.

### Tests

Cover domain behavior, contract compatibility, dependency direction, tenant/state isolation, idempotency, failures, and the capability's current admission state.

## Dependency rule

```text
API -> Application -> Domain
Infrastructure -> declared application/domain ports
```

The domain never depends on infrastructure. A capability never imports another capability's internals, writes another module's tables, or selects/activates another capability's model.

## Required declarations

`MODULE.md` states responsibilities, non-responsibilities, contracts, data ownership, tenant scope, flow, dependencies, events, operational obligations, admission status, and actual ADR links.

`module.yaml` declares the stable module ID, `kind: capability`, tenant scope, `pattern: capability-module-v1`, identity path, contracts, dependencies, owned data, events, ADRs, and status.

## Local exceptions

Record a justified deviation in `DEVELOPMENT_OVERRIDES.md` with scope, reason, consequence, tests, owner, and removal trigger. Do not create a new shared pattern for one unusual module.

