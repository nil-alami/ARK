# ADR-015 — REST/JSON externally and typed ports internally; no gRPC requirement

Status: `ACCEPTED`

Date: 2026-08-13

Decision owner: ARK design sponsor; explicitly approved with Stage 18 on 2026-08-13

## Context and requirements

The governing decision section requires an explicit REST-versus-gRPC decision. ARK initially has consumer-facing request/response contracts, polling resources, optional webhooks, in-process modular coordination, and separately runnable roles from one coordinated codebase. No independently deployed low-latency streaming RPC boundary or non-HTTP consumer requirement is evidenced.

## Decision

Use versioned REST/JSON for the external platform API and documented Synapse adapter boundaries. Use typed in-process module ports for local coordination and typed durable job commands/resources for long work. Do not select gRPC as a baseline internal or external protocol. If a module is later extracted, its transport is chosen from measured consumer, latency, streaming, compatibility, security, and operating requirements without changing the logical contract or tenant authority.

The legacy-coexistence/cutover portion of `A-07-INTEGRATION` expired at Stage 16 and is not extended. Replace it with `CONSUMER_CUTOVER_BLOCKED`: no legacy dual-running, consumer migration, compatibility bridge, or cutover may be activated until the named consumer inventory, current and target contract versions, mapping/ownership boundary, reconciliation and rollback procedure, acceptance authority, cutover window, and Stage 16 contract/E2E evidence are approved. Bounded adapters do not constitute an approved migration plan.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| REST/JSON external, typed ports/jobs internal | Broad consumer compatibility, explicit schemas, simple operations, no internal network tax | Serialization overhead; requires contract governance | Selected | Measured protocol requirement emerges |
| gRPC for all internal module calls | Typed RPC and streaming | Turns logical boundaries into network contracts; tooling/proxy/debug/version burden | Rejected now | Extracted service has measured RPC/streaming need |
| gRPC external API | Efficient typed clients/streaming | Consumer/browser/gateway compatibility and generated-client burden without need | Rejected now | Named consumers require it and compatibility/security gates pass |
| Schema-free generic HTTP execute endpoint | Few routes | Erases capability contracts and limits | Rejected | No trigger under typed-operation requirements |

## Rationale

REST/JSON matches current consumer and interface evidence. In-process ports preserve modular boundaries without distribution. Durable jobs solve lifetime and reliability rather than using a faster RPC protocol for unsuitable work.

## Consequences and trade-offs

- One versioned public API and schema governance are required.
- Internal modules do not gain independent deployment by protocol convention.
- A later service may use gRPC without changing business ownership, but needs a dedicated extraction/transport decision.
- Polling remains authoritative and webhooks remain conditional.

## Implementation constraints

- Typed capability/version/operation schemas; no universal schema-free executor.
- Tenant authority only from trusted context across all transports.
- Large data/results remain by reference, not oversized JSON or RPC payloads.
- gRPC, SSE, public event feed, MCP and A2A are not inferred from module or LLM boundaries.
- `CONSUMER_CUTOVER_BLOCKED` remains fail-closed until its evidence and approval packet is complete; indefinite legacy coexistence is not a temporary default.

## Validation evidence

- Sponsor approval of Stage 07 and ADR-004 on 2026-08-11.
- Sponsor approval of Stage 11's interface disposition on 2026-08-12.
- Approved Stages 15–17 provide placement, tests and measured protocol triggers.

## Reconsideration trigger

A named consumer or extracted service has a measured low-latency, high-frequency, binary-schema, bidirectional/streaming, or interoperability need that REST/JSON, in-process ports, and jobs cannot meet; the proposal passes ADR-003 extraction, compatibility, security, observability, reliability, ownership, benchmark, and cost gates.

## Supersedes / superseded by

Records and refines accepted ADR-004's protocol decision and Stage 11 interface disposition and replaces the expired legacy-coexistence/cutover portion of `A-07-INTEGRATION` with the explicit fail-closed disposition above. Superseded by: none.
