# Stage 11 — Agent architecture only if justified

Status: `APPROVED`

## Purpose and scope

Determine whether any current ARK use case requires an AI agent rather than a deterministic rule, bounded ML/LLM service, durable job, or named workflow. Test every plausible candidate against the governing requirement for autonomous planning, dynamic tool selection, adaptive execution, or genuinely open-ended multi-step reasoning. Decide the appropriate interaction mechanisms and define an exact re-entry gate for any future agent proposal.

This stage does not design a production agent, agent runtime, planner, memory subsystem, tool registry, vector store, MCP server, A2A protocol, new workflow, or Stage 12 security architecture. The sponsor accepted ADR-007, approved Stage 10 as written, and authorized Stage 11 only on 2026-08-12. On 2026-08-12 the sponsor explicitly approved Stage 11's “no agent justified by current evidence” result and authorized execution of Stage 12 only.

## Inputs read in full

- `AGENTS.md` — all sections
- `AGENT-ROSTER.md` — all sections
- `WORKFLOW.md` — all sections
- `STATUS.md` — all sections after recording Stage 10/ADR-007 approval
- `SOURCE_MANIFEST.md` — all sections
- `stages/STAGE-CONTRACT.md` — all sections
- `stages/11-agent-architecture.md` — all sections
- `templates/stage-output.md` — all sections
- `sources/normalized/system-design-prompt.md` — **Project information**, **Working rules**, and **10. Agent architecture, only if justified** exactly
- `sources/normalized/ark-assumptions.md` — all sections
- `outputs/stages/03-capability-inventory.md` — all sections
- `outputs/stages/08-execution-orchestration.md` — all sections
- `outputs/stages/09-events-proactive-actions.md` — all sections
- `outputs/stages/10-mlops.md` — all sections after approval
- `decisions/ADR-002-stage-03-capability-evidence-disposition.md` through accepted `decisions/ADR-007-versioned-ml-lifecycle-and-production-admission.md` — all sections
- `sources/normalized/service-cards/Synapse_chatbot.md` — all sections
- `sources/normalized/service-cards/synapse_message_generator.md` — all sections
- `sources/normalized/service-cards/synapse_campaign_verifier.md` — all sections
- Repository-wide agentic-use-case search over agent, planning, tool, memory, autonomy, MCP, and A2A references

The Stage 11-authorized `data_mlops_architect` performed a bounded read-only proposal review of every plausible agent candidate and its deterministic alternative. The Stage 11-authorized `assurance_reviewer` independently challenged the evidence threshold, candidate conclusions, protocol selection, and re-entry gate after a coherent draft existed. Their findings are reconciled below; the primary agent remains the sole writer.

## Source-instruction coverage

| Source requirement | Addressed in | Status/evidence |
|---|---|---|
| Prove agent need through planning/tool selection/dynamic execution/multi-step reasoning | Agent qualification test and candidate matrix | Addressed; no candidate passes |
| Prefer deterministic workflow/rules/ML service | Candidate matrix and recommended target forms | Addressed for every candidate |
| Goal | Per-agent contract | Not applicable — no agent proposed; required by re-entry gate |
| Reason it must be an agent | Agent qualification test | No evidenced reason; deterministic alternatives suffice |
| Tools | Per-agent contract | Not applicable — no tools or dynamic selection are evidenced |
| Available context | Synapse/candidate evidence assessment | Caller payload/history or immutable references only; no agent context contract |
| Memory and state | Agent qualification test | No autonomous/server-side memory requirement evidenced |
| Planning boundaries | Agent qualification test | No planning loop proposed |
| Permissions | Existing deterministic authority boundary | Stage 09 grants/policy remain authoritative; no agent permission surface |
| Human approval points | Existing deterministic authority boundary | No agent actions; future proposal must enumerate approvals |
| Termination criteria | Per-agent contract | Not applicable — bounded service/workflow termination already exists |
| Maximum steps, time, and cost | Per-agent contract | No agent loop; numeric service/job policies remain separate unresolved inputs |
| Output contract | Candidate matrix | Existing capability/job/result contracts remain; no agent output invented |
| Evaluation | Future re-entry gate | Deterministic-baseline comparison and agent safety evaluation required before proposal |
| Observability | Future re-entry gate | Full plan/tool/approval/action trace required if reconsidered |
| Failure/fallback | Deterministic alternatives and re-entry gate | Existing service/job fail-closed paths; future agent needs deterministic fallback |
| Prompt-injection and exfiltration controls | No-agent security consequence and re-entry gate | No agent tool/memory surface admitted; future proposal must pass dedicated controls |
| REST/gRPC/events/MCP/A2A decision | Interface disposition | Each mechanism explicitly dispositioned |

## Facts

1. The governing prompt says agents are permitted only where genuinely useful and requires proof of autonomous planning, tool selection, dynamic execution, or multi-step reasoning; otherwise the component is a normal deterministic or ML service. `sources/normalized/system-design-prompt.md — Working rules`, items 8–9.
2. Churn, RFM, NPT, and REC are bounded ML/data capabilities. Their work is represented by typed immediate or durable operations, explicit model lifecycle, and capability-owned results; no tool-use or autonomy contract exists. `outputs/stages/03-capability-inventory.md — CAP-CHURN through CAP-REC`; `outputs/stages/08-execution-orchestration.md — Execution-mode disposition`.
3. The Synapse evidence documents three synchronous request/response LLM interfaces. It documents no tools, planning loop, autonomous memory, adaptive execution, proactive initiation, event emission, or external-action authority. `sources/normalized/service-cards/Synapse_chatbot.md — INFRASTRUCTURE CLASSIFICATION`; `synapse_message_generator.md — INFRASTRUCTURE CLASSIFICATION`; `synapse_campaign_verifier.md — INFRASTRUCTURE CLASSIFICATION`.
4. `AgentController` and `config[].agent` are identifier/field names, not architectural evidence. Accepted source and capability decisions explicitly prohibit inferring agent behavior from them. `decisions/ADR-002-stage-03-capability-evidence-disposition.md — Implementation constraints`; `outputs/stages/03-capability-inventory.md — C-03-06`.
5. The approved proactive path is a deterministic two-phase authorization/policy algorithm that submits one typed grant-listed task and separates insight, decision, work, event, and notification. No named workflow or direct campaign action is active. `outputs/stages/09-events-proactive-actions.md — Two-phase fail-closed decision order`; `— Decisions`.
6. The approved conditional workflow uses an immutable named graph of public typed operations with declared branches, failure, fallback, and compensation. It is inactive because no named workflow is evidenced. `outputs/stages/08-execution-orchestration.md — Conditional named-workflow contract`.
7. Accepted ADR-007 makes all three Synapse profiles `EVIDENCE_BLOCKED` and explicitly says no provider/model, prompt, retrieval, tool, memory, agent, state, proactive, or external-action behavior may be inferred. `decisions/ADR-007-versioned-ml-lifecycle-and-production-admission.md — Decision`, item 3.
8. Accepted ADR-003 rejected agentic architecture as the starting style and permits reconsideration only when a bounded evidenced need cannot be satisfied by a deterministic workflow. `decisions/ADR-003-architecture-style.md — Options considered`.
9. LAB is an external validation consumer/platform, not an ARK capability or documented agent. `SOURCE_MANIFEST.md — Expected capability-card coverage`.

## Assumptions

Stage 11 introduces no new temporary assumption and does not extend an expired assumption.

| ID | Assumption | Why needed | Architectural effect | Risk | Validation/expiry |
|---|---|---|---|---|---|
| `A-01-BUS` | ARK remains behind consuming platforms and does not own customer-channel delivery | Product boundary remains unresolved | No agent is invented to contact customers or send campaigns | Later scope may expand | B-01 through B-05 or superseding product decision |
| `A-01-SEC` | Least privilege, deterministic policy-before-action, tenant binding, and audit remain mandatory | Exact security role/policy evidence is incomplete | A future agent cannot become authorization authority | Later policy may be stricter | Stage 12 and authoritative evidence |
| `A-01-SCALE` | Traffic, latency, step/time/cost, and resource targets remain unknown | Prevent invented agent loop limits or protocol claims | No production agent profile can be sized | Future agent proposal plus Stage 17 |
| `A-01-OPS` | Support, recovery, and operating targets remain unknown | Agent loops add ambiguous recovery/on-call burden | No agent runtime/operator is introduced | Stages 13–15/20 or authoritative evidence |
| `A-04-OWNERSHIP` | Logical owner roles suffice for design; named accountable owners remain unresolved | Agent goal/tool/safety/runbook ownership cannot be invented | Any future agent remains production-blocked until names exist | Actual role separation may differ | Before Stage 20/production |
| `A-07-INTEGRATION` | Typed REST/JSON, durable job resources/polling, registered webhook condition, and external adapters remain the baseline | Interface choices must preserve approved contracts | Agent protocols cannot bypass current API/notification authority | Consumer needs may differ | Existing per-portion expiry |

Accepted ADR-007's `MIGRATION_BLOCKED` and `EVIDENCE_BLOCKED` profiles are decisions, not assumptions. This stage neither lifts nor weakens them.

## Analysis and recommendations

### Agent qualification test

A component is an ARK agent only if a named use case requires an ARK-controlled execution loop that constructs or revises a plan from observations, selects among multiple authorized tools at runtime, performs dependent steps whose safe sequence cannot be enumerated as a bounded workflow, or adapts/replans within explicit authority. Using an LLM, accepting conversation history, executing several fixed steps, reacting to state-machine transitions, or carrying “Agent” in a name does not pass.

Every proposed agent must answer all five questions affirmatively with evidence:

1. Is there a named business goal and success/failure measure?
2. Does execution require runtime planning, tool selection, adaptive dependent steps, or equivalent autonomy?
3. Has the simplest deterministic rule, typed workflow, or bounded ML/LLM operation been shown insufficient?
4. Can permissions, termination, maximum steps/time/cost, approvals, evaluation, observability, injection/exfiltration protection, and deterministic fallback be bounded before execution?
5. Do named product, security/policy, operations, and runbook authorities approve the production risk?

A “no” or missing evidence yields `NOT_JUSTIFIED`; an under-evidenced Synapse candidate also remains `EVIDENCE_BLOCKED`.

### Candidate evaluation

| Candidate | Evidenced behavior | Planning/tool/adaptation test | Deterministic target | Verdict |
|---|---|---|---|---|
| Churn | Versioned tenant scoring/training target | Fixed feature/model pipeline; no tools or plan | Typed batch inference and explicit lifecycle jobs | `NOT_JUSTIFIED`; remains `MIGRATION_BLOCKED` |
| RFM | Versioned segmentation target | Fixed transform/optional clustering/mapping; no tools or plan | Typed batch segmentation and explicit lifecycle/rules profile | `NOT_JUSTIFIED`; remains `MIGRATION_BLOCKED` |
| NPT | Versioned classifier/survival forecast target | Fixed compatible bundle and routing policy; no tools or plan | Typed batch prediction and lifecycle jobs | `NOT_JUSTIFIED`; remains `MIGRATION_BLOCKED` |
| REC | Candidate generation/ranking/fallback target | Multiple algorithms and branches are predetermined, not runtime tool choice | Versioned ranking pipeline with explicit degraded sources | `NOT_JUSTIFIED`; remains `MIGRATION_BLOCKED` |
| Synapse Chatbot | One request with query, caller-supplied history/context; one response | No server-side memory, tools, plan, autonomy, or adaptive loop evidenced | Bounded conversational response-generation service | `NOT_JUSTIFIED` and `EVIDENCE_BLOCKED` |
| Synapse Message Generator | One constrained churn/occasion request; one Persian text response | No tools, plan, memory, proactive trigger, or action evidenced | Bounded content-generation service plus deterministic validation | `NOT_JUSTIFIED` and `EVIDENCE_BLOCKED` |
| Synapse Campaign Verifier | One opaque payload/reference/config request; advisory status | No tool selection or planning; `config[].agent` is untyped caller data | Deterministic policy authority plus optional bounded advisory assessment | `NOT_JUSTIFIED` and `EVIDENCE_BLOCKED` |
| Proactive monitoring/action | Schedule/request/conditional fact through ordered checks to typed task/notification | Multi-step but completely specified; dynamic authority is prohibited | Stage 09 two-phase evaluator + Stage 08 job/intent handlers | `NOT_JUSTIFIED`; no named action/workflow active |
| Optional generate-and-verify campaign flow | Possible generation then verification in governing example, not approved scope | Known sequence/branches; no evidence that plan synthesis is needed | Named deterministic parent/child workflow if later approved | `NOT_JUSTIFIED`; remains inactive |
| ML lifecycle/operations | Train, evaluate, promote, assign, monitor, rollback | Explicit state/approval graph; adaptation cannot bypass authority | Stage 08 jobs + Stage 10 registry/decision/assignment records | `NOT_JUSTIFIED`; no autonomous promotion/remediation |
| LAB validation | External consumer validates services | No ARK agent behavior or tool contract evidenced | External test/evaluation integration | `NOT_JUSTIFIED`; not an ARK capability |

An LLM may perform opaque internal reasoning inside a bounded generation request. That is a model-serving concern governed by Stage 10 evidence and evaluation, not proof of an ARK agent loop.

### R-11-01 — Retain bounded capability services and deterministic orchestration

**Requirement/where:** source Working rules 7–9; capability, proactive, workflow, and lifecycle execution. **Why now:** treating LLM or multi-step labels as agents would add tool, memory, planning, authorization, recovery, and safety surfaces without a requirement. **Simplest implementation:** retain typed module/REST operations, Stage 08 durable jobs, deterministic Stage 09 control decisions, and an inactive named-workflow seam. **Alternative:** agent framework or generic agent loop. **Why rejected:** no goal requires runtime plan/tool adaptation, and all current behavior is bounded or unevidenced. **Trade-off:** future genuinely dynamic work requires a new decision rather than ad hoc autonomy. **Reconsideration:** every item in the agent re-entry gate below passes.

### R-11-02 — Keep LLM generation separate from agency and authority

**Requirement/where:** Synapse interfaces, `ARK-FR-010`, ADR-007 profiles. **Why now:** free-form text and advisory labels are probabilistic outputs but do not imply tool use or permission. **Simplest implementation:** a bounded generation/assessment handler with exact prompt/model/policy evidence, deterministic input/output validation, and no direct effect. **Alternative:** chatbot/message/verifier agent with tools or memory. **Why rejected:** those internals are absent and production-blocked. **Trade-off:** less autonomous user experience, but smaller injection/exfiltration and unauthorized-action surface. **Reconsideration:** authoritative Synapse evidence plus a named use case proves deterministic response generation insufficient and passes all re-entry gates.

### R-11-03 — Do not select MCP or A2A without a real relationship

**Requirement/where:** source section 10 interface decision; future integration design. **Why now:** protocol choice can accidentally establish dynamic tool or peer-agent authority. **Simplest implementation:** approved REST/module/job contracts and conditional events. **Alternatives:** MCP for tools, A2A for peer agents, gRPC for internal calls. **Why rejected:** no justified agent, tool server, peer agent, or measured RPC need exists. **Trade-off:** no generic discovery/interoperability layer now. **Reconsideration:** MCP only for a justified agent that must interact with independently governed interoperable tool servers; A2A only for at least two justified independently governed agents whose peer delegation cannot be expressed by typed jobs/workflows; gRPC only after a measured transport requirement.

### Interface disposition

| Mechanism | Status now | Appropriate use / reason |
|---|---|---|
| In-process typed module port | Required default inside the modular monolith | Short local calls while preserving public module boundaries |
| REST/JSON | Required external baseline | Documented Synapse and approved ARK capability/control/job/resource interfaces |
| Durable job command + polling | Required for long/retryable work | Training, batch inference, ingestion, scheduled work, and named workflow children |
| Events | Conditional | Only an approved committed-fact subscriber requiring temporal decoupling; not an agent protocol |
| Webhook | Conditional external notification | Reports existing resources/facts; never tool invocation or action authority |
| gRPC | Not justified | No independently deployed high-throughput/streaming/latency need exists |
| MCP | Not justified | No justified agent-to-tool relationship, dynamic tool selection, or tool-server boundary exists |
| A2A | Not justified | No production agent is currently justified or selected, let alone independently governed peer agents |
| Vector store/retrieval layer | Not justified | No approved governed corpus, semantic retrieval need, or quality/latency target exists |
| Agent framework/runtime | Not justified | No current candidate passes qualification; existing state machines/workflows suffice |

### Future agent re-entry gate

A future proposal must provide and gain approval for all of the following before an agent is added:

1. Named business goal, tenant/purpose/data scope, accountable owner, measurable success/failure, and explicitly prohibited outcomes.
2. Comparative evidence that a deterministic rule, typed workflow, or bounded ML/LLM operation cannot meet the use case safely or effectively.
3. Concrete runtime need for plan construction/revision, selection among multiple versioned tools, dependent steps that cannot be safely enumerated, or bounded adaptive recovery.
4. Complete agent contract: goal; agent necessity; exact tools and schemas; available context; memory/state model and retention; planning boundaries; permissions; human approval points; termination; maximum steps, time, and cost; output; evaluation; observability; failure/fallback; injection and exfiltration controls.
5. Tenant lifecycle and ownership: principal-derived tenant, purpose-bound context/memory, tenant-isolated tool credentials/state/audit/cache/output, owner-writer boundaries, correction/export/deletion, and named product/security/operations/runbook authorities.
6. Independent versions for agent contract, model/deployment, prompts, context assembly, memory schema, tool schemas/adapters, planner, safety policy, evaluator, code, and execution, with immutable trace of observations, plan transitions, tool calls/results, approvals, usage/cost, and output.
7. Evaluation against the deterministic baseline for task success, plan boundedness, tool choice/arguments/results, hallucination, unauthorized action, approval compliance, injection, exfiltration, privacy, recovery, latency, and cost across relevant tenant/use-case/adversarial slices.
8. First deployment in shadow/no-effect mode, explicit bounded canary only after Stage 12–17 gates, deterministic fallback, assignment rollback, no runtime self-learning/prompt/tool mutation, and no automatic permission expansion or model promotion.
9. Execution and effect safety: long-running/retryable agent execution uses the Stage 08 durable job, attempt, lease, and fencing contract; every tool effect is a typed authorized command with stable effect/idempotency identity; stale attempts cannot act; ambiguous external effects are reconciled without blind retry; deadlines, checkpoints, cancellation safe points, and deterministic failure/fallback are explicit.
10. Authority preservation: an agent may propose but cannot own, reorder, or bypass entitlement, standing authorization, deterministic policy, quota, cooldown, dedupe, mandatory audit, action authority, model promotion, or deployment assignment. Stage 09 Phase A, Phase B, and execution-time/at-effect rechecks remain outside the agent and authoritative; Stage 10 exact approved deployment assignment remains mandatory.
11. Explicit interface proof: MCP only for actual agent-to-tool interoperability across a governed tool-server boundary; A2A only for two or more independently governed justified agents needing peer delegation that typed commands/jobs/events cannot satisfy.
12. Explicit sponsor approval, as required by the Stage 11 gate, before any production agent.

Until every item passes, the disposition is `NOT_JUSTIFIED`; use the named deterministic alternative.

### No-agent security and operations consequence

No agent-specific planner, autonomous memory, dynamic tool credential, tool-call execution, delegation, or agent trace surface is admitted. This reduces but does not eliminate LLM risk: Synapse remains `EVIDENCE_BLOCKED`, and its eventual bounded model calls still require Stage 12 prompt-injection, data-exfiltration, provider-transfer, tenant, content-safety, secrets, and abuse controls plus Stages 13–16 reliability/observability/testing evidence. A no-agent result must not be misread as a Synapse security approval.

## Decisions

- **No production agent is justified.** Therefore the user-approval gate for a proposed production agent is not triggered.
- Churn, RFM, NPT, and REC remain normal ML/data capabilities; their `MIGRATION_BLOCKED` status is unchanged.
- Synapse Chatbot, Message Generator, and Campaign Verifier remain interface-only and `EVIDENCE_BLOCKED`; no ARK agent is currently justified or selected from admitted evidence, and their undocumented internal behavior remains unresolved.
- Proactive evaluation, campaign composition if ever named, ML lifecycle, and cross-capability coordination use deterministic policy/state machines and typed workflows/jobs.
- REST/JSON, in-process module ports, durable job commands/polling, and conditional events/webhooks remain the appropriate interfaces. gRPC, MCP, A2A, an agent framework/runtime, autonomous memory, and a vector store are not selected.
- No new ADR is required: this stage confirms accepted ADR-003's rejection/reconsideration gate and ADR-007's Synapse evidence boundary without choosing a new architecture component.

## Contradictions and dangerous assumptions

| ID | Tension/hazard | Treatment | Consequence |
|---|---|---|---|
| `C-11-01` | Synapse paths/types contain “Agent” | Identifier only; no planning/tool/memory/autonomy inference | Normal bounded interface, still evidence-blocked |
| `C-11-02` | Chat history may be called agent memory | Caller-supplied request context; server state/retention are undocumented | No memory subsystem or persistence inferred |
| `C-11-03` | LLM internal reasoning may be called a planning loop | One bounded inference call is model behavior, not ARK-controlled iterative execution | Govern through MLOps/evaluation, not an agent runtime |
| `C-11-04` | A multi-step workflow appears agentic | Fixed named nodes/branches are deterministic orchestration | Use Stage 08 coordinator first |
| `C-11-05` | Proactive operation appears autonomous | Exact grant, schedule, policy, typed command, and rechecks bound every step | No self-chosen goal/task/tool/action |
| `C-11-06` | Verifier `accepted` appears to authorize action | Advisory only; deterministic policy and standing authorization remain authoritative | No probabilistic authority |
| `C-11-07` | MCP is treated as a generic internal API | MCP requires an actual justified agent-to-tool interoperability need | Typed module/REST/job contract remains simpler |
| `C-11-08` | A2A is treated as generic workflow messaging | A2A requires justified independently governed agents | Jobs/workflows/events remain authoritative |
| `C-11-09` | “No agent” could imply “no LLM risk” | LLM safety/provider/prompt evidence is independently missing | Synapse remains blocked; Stage 12 controls still required |
| `C-11-10` | Future unknown needs are used to prebuild agent infrastructure | Re-entry gate preserves evolution without deployment | No speculative framework, memory, vector store, or protocol |

## Open questions

| ID | Question | Blocking? | Options | Recommended temporary assumption | Effect |
|---|---:|---|---|---|---|
| `Q-11-01` | Is there a named business goal that demonstrably cannot be satisfied by a deterministic workflow or bounded model call? | Before any agent proposal | Supply evaluated use case; remain deterministic | No such need is evidenced | No agent component |
| `Q-11-02` | Does any future use case need runtime-selected tools, plan revision, or adaptive dependent steps? | Before tool/planner design | Evidence and bounded tool set; fixed workflow | Treat absent | No tool registry/MCP |
| `Q-11-03` | Can authoritative Synapse provider/prompt/tool/memory/state/safety evidence be supplied? | Before Synapse re-entry | Supply evidence; scope out; remain blocked | Preserve accepted `EVIDENCE_BLOCKED` state | No Synapse production/agent claim |
| `Q-11-04` | Is a named generate/verify or other cross-capability workflow actually in release scope? | Before workflow activation | None; deterministic named workflow; later agent proposal | Keep inactive | No workflow engine or agent |
| `Q-11-05` | Which named authorities would own a future agent goal, tool policy, approvals, evaluation, security, and on-call? | Before production proposal | Assign roles/people and segregation | Remain unresolved under `A-04-OWNERSHIP` | Production agent blocked |

## Requirements-traceability updates

| Requirement | Stage 11 design response | Verification direction |
|---|---|---|
| `ARK-FR-004/005/006` | Capability schemas/readiness/outcomes remain bounded; agent naming changes no contract | Contract and outcome matrix tests |
| `ARK-FR-007/008/009` | Existing immediate/durable execution and explicit ML lifecycle remain; no agent owns retry/training/promotion | State/lifecycle negative tests |
| `ARK-FR-010` | No LLM/verifier/agent-like output authorizes work/action | No-action and authorization-bypass tests |
| `ARK-FR-011` | Commands, events, insights, notifications, workflows, and future tool calls remain distinct | Contract/authority boundary tests |
| `ARK-FR-012` | Future agent requires plan/tool/action/safety evaluation; current evaluation remains model/service-level | Re-entry evidence checklist |
| `ARK-NFR-001/005` | No new memory/tool/context surface; tenant/privacy constraints remain mandatory | Cross-tenant/provider/payload tests |
| `ARK-NFR-002/003/006` | Future agent version/trace axes specified but not instantiated | Manifest/trace completeness if reopened |
| `ARK-NFR-004/007` | Deterministic jobs/recovery retained; no unsupported autonomy/cost/scale claims | Failure/anti-overengineering tests |
| `ARK-CON-001/002/005` | Modular-monolith ports, PostgreSQL jobs, and conditional events remain | Dependency/state-authority tests |
| `ARK-CON-007` | Agent runtime/framework, MCP, A2A, vector store, and agent memory rejected without evidence | Component inventory/re-entry gate review |
| `SC-02-04/05/06/08/09/10/11/12` | Failure, recovery, isolation, no-action, ownership, target blocks, and acceptance evidence preserved | Stage 12–16 suites and future agent approval |

`quality/source-instruction-coverage.md` marks source prompt section 10 covered by this artifact after the completion gate passes. “Covered” means every candidate and required contract concern was dispositioned; it does not approve any production agent or lift any capability block.

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Every plausible current agent candidate evaluated | PASS | Eleven-candidate matrix covers all named capabilities, proactive/workflow/lifecycle/LAB paths |
| Agent threshold applied to planning/tool/dynamic/multi-step need | PASS | Five-question qualification test and evidence citations |
| Deterministic alternative preferred where sufficient | PASS | One target form per candidate and R-11-01/02 |
| Synapse names/context/history not mistaken for agency | PASS | Facts and C-11-01 through C-11-03 |
| Proactive and multi-step workflows not mistaken for agency | PASS | C-11-04/05 and approved Stage 08/09 state machines |
| Complete source-section contract dispositioned | PASS / NOT APPLICABLE | No agent proposed; every field is mandatory in the future re-entry gate |
| REST/gRPC/events/MCP/A2A decision explicit | PASS | Interface disposition and R-11-03 |
| MCP/A2A introduced only for actual relationship | PASS | Both rejected; exact future triggers recorded |
| Prompt-injection/exfiltration responsibility preserved | PASS | No-agent security consequence and re-entry gate |
| Production-agent approval gate | NOT TRIGGERED | No production agent proposed |
| Anti-overengineering applied | PASS | No agent framework/runtime, memory, vector store, MCP, A2A, or speculative workflow |
| Authorized specialist proposal reconciled | PASS | `data_mlops_architect` confirmed no candidate passes and supplied deterministic alternatives/re-entry evidence |
| Authorized assurance challenge reconciled | PASS | Final read-only review reported no critical or high defects after evidence-qualified wording and Stage 08/09/10 authority corrections |
| Stage 12 not executed | PASS | No Stage 12 artifact or decision created |

**Gate result: PASSED AND APPROVED.** No production agent is justified or selected from currently admitted evidence. Every plausible candidate has a simpler deterministic form, Synapse unknowns remain `EVIDENCE_BLOCKED`, protocol choices are explicitly dispositioned, and the complete future re-entry gate preserves Stage 08 execution/effect safety and Stage 09/10 authority. The authorized final assurance review reported no unresolved critical or high defects. Because no production agent is proposed, the Stage 11 user-approval gate for an agent was not triggered. The sponsor explicitly approved the result on 2026-08-12 and authorized Stage 12 only.

## Downstream consequences

- Stage 12 must secure bounded LLM/provider/prompt/context interfaces but must not invent agent tools, memory, permissions, or delegation controls as active architecture. It should retain the future-agent threat requirements as conditional.
- Stage 13 must analyze model/provider/job/workflow failures, not agent-loop failures, unless new evidence reopens Stage 11.
- Stage 14 evaluates Synapse as bounded LLM capabilities and other capabilities as ML/data services; agent execution traces are not applicable unless Stage 11 is superseded.
- Stage 15 must not place an agent runtime, MCP server, A2A gateway, vector store, or agent memory tier.
- Stage 16 must verify no endpoint name, verifier output, proactive result, or workflow state bypasses deterministic authority; any future agent needs the re-entry evaluation suite.
- Stage 17 assigns no agent step/time/cost capacity because no ARK agent is currently justified or selected; current service/job/provider costs remain applicable.
- Stage 18 should index this stage's no-agent decision; no ADR is created unless later evidence supersedes ADR-003/Stage 11.
- Stage 19's agentic workflow diagram is explicitly not applicable unless a production agent is later justified.
- Stage 20 must not place agent implementation in the roadmap; it may list the re-entry gate as a conditional future decision.

## Exact next-stage inputs

Stage 11 is approved and Stage 12 is authorized. Stage 12 must read:

1. Approved `outputs/stages/01-discovery-and-questions.md` through `outputs/stages/11-agent-architecture.md`
2. Accepted `decisions/ADR-000-temporary-source-evidence-disposition.md` through `decisions/ADR-007-versioned-ml-lifecycle-and-production-admission.md`
3. `sources/normalized/system-design-prompt.md` section **11. Security, privacy, and governance**
4. `sources/normalized/ark-assumptions.md`
5. All seven service cards under accepted production-admission restrictions
6. `stages/12-security-governance.md`, `templates/stage-output.md`, and any directly referenced security templates

Execute Stage 12 only. Do not execute Stage 13 until Stage 12 passes its gate and the sponsor explicitly authorizes continuation under the active stop condition.
