# ADR-006 — Governed proactive action and delivery boundary

Status: `ACCEPTED`

Date: 2026-08-12

Decision owner: ARK design sponsor (user approval)

## Context and requirements

ARK must support permissioned proactive evaluation and notification without allowing capability enablement, an ML result, an event, a webhook, or the Synapse campaign verifier to become authority for external action. The design must cover schedules and conditional event triggers; standing authorizations; thresholds, freshness, quotas, cooldowns, deduplication, expiry, and policy; typed job/workflow submission; internal event contracts; external delivery; retry, dead-letter, acknowledgement, replay, ordering, and audit.

Approved ADR-003 keeps event-driven behavior conditional and separates control authority, internal coordination, and external notification. ADR-004 makes polling authoritative and webhooks conditional. ADR-005 owns durable jobs and permits event handlers only to map approved events to typed commands. No named proactive workflow, consumer delivery SLO, concrete grant roles, production trust/signature protocol, numeric policy values, or broker-scale evidence is available.

Evidence: `sources/normalized/ark-assumptions.md — Execution, orchestration, and proactive operation`; `— Security, ownership, and operations`; `outputs/stages/02-system-definition.md — ARK-FR-010/011`; `outputs/stages/05-end-to-end-architecture.md — C05-04, C05-12, C05-18, C05-21, C05-22`; `outputs/stages/07-api-integration.md — Callback/webhook contract`; `outputs/stages/08-execution-orchestration.md — Conditional event-triggered execution`; `outputs/stages/09-events-proactive-actions.md`.

## Decision

ARK will use this governed proactive-action and delivery boundary:

1. Capability subscription, proactive subscription, event subscription, endpoint registration, standing authorization, immutable insight, control-plane action decision, authorized ARK task/workflow, internal domain event, external notification intent, and delivery attempt are separate versioned records with separate authoritative owners.
2. Proactive evaluation and any post-insight task/notification use a two-phase fail-closed gate. Before evaluation and again before task/notification creation, ARK verifies the applicable authenticated tenant, active subscriptions, exact standing authorization, registered destination where applicable, data scope/readiness/freshness, threshold, deterministic policy, quota, cooldown, deduplication, expiry, and mandatory audit evidence. The executing/delivery owner rechecks time-sensitive evidence before an irreversible external effect. A failed or unavailable mandatory check creates no action.
3. A capability result or actionable insight is eligible for governed review only. It is never a grant or command. The Synapse campaign verifier remains advisory under `A-03-SYNAPSE` and cannot be the sole policy or authorization authority.
4. Scheduled evaluation through the approved scheduler and PostgreSQL job lifecycle is the first supported independent trigger. Explicit evaluation is an ordinary authenticated command. Dataset/result/external event triggers remain inactive until an exact event contract, subscriber, handler, trust rule, and reliable-publication policy are approved.
5. No named proactive workflow or direct customer-channel action is activated. ARK may evaluate, report, submit an exact grant-listed ARK task, and notify a registered consuming platform. It does not claim that a notification caused or completed a downstream business action.
6. Internal business/domain events are immutable facts, not commands. If a named internal subscriber is activated, the source transaction also creates a producer-owned outbox/publication record; a shared publisher delivers at least once to an idempotent typed handler. Direct ports and jobs remain preferred when temporal decoupling is unnecessary.
7. External webhooks are optional at-least-once notifications over pre-registered tenant-scoped endpoints and exact event subscriptions. The control decision and promised notification/outbox intent commit without a crash gap. Polling/resource APIs remain authoritative. A stable logical `event_id` identifies the notification; each attempt has a distinct `delivery_id`. Delivery failure, dead-letter, expiry, or replay never reruns capability computation, changes the action decision, or consumes action quota twice.
8. Default event/delivery ordering is unspecified. An event type may add per-key ordering only with an explicit ordering key, sequence, gap/late policy, and serialized scope. HTTP 2xx acknowledges transport receipt only; business acknowledgement requires a separate authenticated idempotent contract.
9. Retry uses a versioned bounded exponential-backoff/jitter policy. Exhausted/permanent delivery becomes explicit PostgreSQL `DEAD_LETTERED` or `EXPIRED` state. Authorized replay creates a new attempt for the same logical fact/notification and preserves actor, reason, original occurrence time, and audit history.
10. No event broker, event backbone, continuous processor, SSE/public event feed, generic workflow engine, separate DLQ product, or direct campaign sender is selected. A broker requires ADR-005's measured trigger and a separate approved ADR.

No new temporary assumption is introduced. Concrete authorization roles, signature/trust controls, policy values, named workflows, retention periods, delivery targets, and operating owners remain activation-blocking inputs at their governing later stages.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| Capability-owned automation from result to action | Minimal coordination | Conflates science with authority, tenant policy, quota, audit, and delivery | Rejected | Never without a superseding security/product-boundary decision |
| One generic proactive-event/workflow object | Fewer record types | Hides authority, truth, retries, revocation, and failure ownership | Rejected | Only if independent invariants can be preserved explicitly |
| Separate records plus two-phase gate, scheduler/jobs first | Preserves authority and failure truth using approved mechanisms | More explicit state, version checks, and reconciliation | Selected | Reassess mechanics after measured evidence, not the fail-closed invariants |
| Event backbone/broker now | Native fan-out/replay | Unsupported operations, ordering, retention, security, and dual-truth burden | Rejected now | ADR-005 broker trigger passes |
| Webhook as result/action truth | Simple push-only consumer experience | Delivery ambiguity changes business truth and invites duplicate effects | Rejected | Never; transport may evolve but authoritative resources remain |
| General workflow engine/direct campaign sender | More automation | No named workflow, action authority, ownership, or complexity evidence; expands product boundary | Rejected now | Explicit sponsor scope/authority plus workflow-engine gate |

## Rationale

The selected boundary is the smallest implementation that satisfies the source's permissioned proactive flow while preserving accepted modular ownership and PostgreSQL-first execution. It prevents the most dangerous collapses: subscription into execution, insight into authorization, event into command, notification into result truth, retry into recomputation, and verifier output into policy enforcement.

Using schedules and ordinary jobs first avoids infrastructure that has no named subscriber or measured requirement. Conditional transactional outbox publication preserves a safe evolution path when an internal event boundary becomes real.

## Consequences and trade-offs

- Proactive work has explicit versioned authority, evidence, reasons, and revocation behavior.
- Some insights remain report-only even when scientifically strong because control evidence is absent or fails.
- Implementers must maintain separate control, decision, task, event, notification, and delivery identities plus reconciliation tooling.
- Webhook consumers must deduplicate logical events and use polling/resource APIs for recovery.
- Missing roles, trust controls, numeric policies, or audit availability block activation rather than being defaulted.
- Internal events/outbox add no first-version operational burden until a named subscriber is approved.
- Direct customer-channel automation and Synapse proactive use remain unavailable.

## Implementation constraints

- Tenant authority comes only from trusted context; every record and route is tenant-scoped and cross-tenant existence is concealed.
- Active standing authorizations are immutable except through a new version or audited state transition. Subscription configuration cannot create or broaden authority.
- Phase B rechecks authority/freshness/policy after insight computation and before any task or notification intent; execution/delivery rechecks time-sensitive evidence before irreversible effect.
- Mandatory audit must commit before a grant mutation, authorized task, or external notification intent becomes effective.
- The control decision, quota/cooldown/dedupe reservation, mandatory audit evidence, and producer-owned typed command/notification intents commit without a crash gap through owner module ports; intent handlers submit to the job manager/integration owner idempotently and never cross-write their tables.
- Capability-owned thresholds define scientific meaning; tenant configuration may select only supported values/ranges.
- Every task, event, notification, attempt, replay, quota/cooldown reservation, and audit record has a distinct stable identity and exact version references.
- Internal event creation occurs only from a committed authoritative fact. The outbox/broker owns delivery state only.
- External payloads are minimal/reference-oriented and contain no secrets, raw PII, arbitrary callback URLs, or large results.
- Retry/replay cannot silently re-evaluate policies, rerun models, create new action decisions, or consume quota twice.
- Numeric backoff, retry, rate, quota, cooldown, expiry, and retention values are required before activation but are not selected by this ADR.
- No direct campaign/channel integration, broker, workflow engine, stream processor, SSE/public feed, or per-capability event service follows from this decision.

## Validation evidence

- User approval dated 2026-08-12: “I approve Stage 09 and ADR-006 as written. Record the approval and execute only Stage 10.”
- `outputs/stages/09-events-proactive-actions.md` maps every governing Stage 09 requirement and supplies resource contracts, two-phase check order, identities, versioned internal/webhook schemas, routing, delivery state, failure/replay rules, audit fields, traceability, and gate evidence.
- The Stage 09-authorized read-only `platform_architect` delivery review is reconciled in that artifact.
- Required verification includes no-action negative tests for every mandatory gate; revocation/time-of-check races; cross-tenant routing/replay; duplicate triggers/events/deliveries; consumer timeout ambiguity; dead-letter/replay without recomputation; schema incompatibility; and audit-unavailable failure.

## Reconsideration trigger

- A concrete first-release proactive workflow/action and authoritative grant/consumer contract is approved.
- Stage 12 supplies named security roles, segregation, purpose/consent, signature, destination, and replay controls.
- Stage 13/17 supplies measured delivery/recovery/rate/retention targets and evidence the PostgreSQL mechanism cannot meet them.
- An internal subscriber requires independent fan-out/replay/ordering or a broker trigger in ADR-005 passes.
- The ARK product boundary expands to own a customer-channel action through an explicit superseding decision.
- Authoritative Synapse evidence changes its current interface-only/advisory status.

## Supersedes / superseded by

This ADR refines the conditional event/proactive boundaries of accepted ADR-003, ADR-004, and ADR-005. It does not supersede ADR-000 through ADR-005. Superseded by: none.
