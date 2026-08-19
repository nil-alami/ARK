# ADR-013 — Deterministic rules, workflows, and ML; no agent justified by current evidence

Status: `ACCEPTED`

Date: 2026-08-13

Decision owner: ARK design sponsor; explicitly approved with Stage 18 on 2026-08-13

## Context and requirements

The governing decision section requires an explicit rules/ML-service-versus-AI-agent decision. The seven capability cards, proactive flow, named-workflow seam, ML lifecycle, and capacity evidence show bounded model/data operations and deterministic authority. Synapse internals remain undocumented. No admitted use case requires autonomous goal decomposition, dynamic tool selection, adaptive multi-step execution, durable agent memory, or agent-to-agent delegation.

## Decision

Use ordinary ML/data capabilities, deterministic policy/state machines, typed named workflows where later approved, in-process public ports, REST/JSON, durable jobs/polling, and conditional events/webhooks. No ARK production agent, agent framework/runtime, autonomous tool execution, agent memory, vector store, MCP, or A2A is selected from current evidence. Synapse remains interface-only and `EVIDENCE_BLOCKED`; unknown internals are not asserted absent.

LLM/verifier output is advisory and cannot own entitlement, grant, policy, quota, scientific promotion, deployment, notification, or external-effect authority.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| Deterministic rules/workflows plus bounded ML/LLM calls | Testable authority, reproducibility and recovery; matches evidence | Less open-ended autonomy | Selected | A bounded use case proves irreducible autonomy need |
| General agent runtime | Adaptive planning/tool use | Nondeterminism, injection/exfiltration, authority, recovery, cost and evaluation burden | Rejected now | Full Stage 11 re-entry gate passes |
| Multiple agents/A2A | Specialized delegation | Additional identity, handoff, conflict and task-state complexity | Rejected | At least two independently justified governed agents exist |
| Treat Synapse `Agent` labels as proof | Quick classification | Unsupported inference from names | Rejected | Authoritative implementation evidence arrives and passes re-entry |

## Rationale

Automatic, proactive, multi-step, or LLM-backed does not itself mean agentic. Every admitted current need can be expressed with fixed contracts, deterministic gates, versioned jobs, and bounded model calls. This is safer and simpler while retaining an explicit future re-entry path.

## Consequences and trade-offs

- No agent-specific runtime, memory, tool protocol, security or observability stack is built now.
- Stage 09 action gates and Stage 08 fencing remain outside any future agent and authoritative.
- A future agent proposal reopens affected capability, security, reliability, evaluation, testing, deployment and capacity stages.
- The conclusion is evidence-bounded, not a permanent assertion that ARK can never use agents.

## Implementation constraints

- Build/deployment manifests contain no agent framework, MCP/A2A, autonomous tool role or vector-memory dependency without a superseding ADR.
- Named workflows are immutable deterministic graphs over typed public jobs.
- No LLM/model result directly performs or authorizes an irreversible effect.
- Future long/retryable agent execution must use job/attempt/fence and effect-idempotency contracts.

## Validation evidence

- Sponsor approval on 2026-08-12: “I approve Stage 11’s ‘no agent justified by current evidence’ result.”
- `outputs/stages/11-agent-architecture.md` evaluates all current candidates and records the full future-agent re-entry gate.
- Stage 11 authorized specialists ultimately reported no unresolved critical/high defect.
- Approved Stages 12–17 preserve the no-agent security, reliability, observability, testing and capacity consequences.

## Reconsideration trigger

A sponsor-approved bounded goal and scenario proves that deterministic rules, one model call, a fixed pipeline, or a named workflow cannot satisfy the need; the exact autonomy/tools/memory/permissions/limits/effects are evidenced; the full Stage 11 re-entry contract and downstream gates pass; and the sponsor explicitly approves the agent proposal.

## Supersedes / superseded by

Records the approved Stage 11 decision and refines ADR-003's agentic-architecture rejection and ADR-007's Synapse evidence boundary. Supersedes none. Superseded by: none.
