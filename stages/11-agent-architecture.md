# Stage 11 — Agent architecture only if justified

Governing source: `system-design-prompt.md` section **10. Agent architecture, only if justified**.

Inputs: Stages 03, 08–10 and agentic-use-case evidence.

## Work

- Evaluate each proposed agent against the need for autonomous planning, tool selection, dynamic execution, or multi-step reasoning.
- Prefer deterministic workflow/rules/ML service where autonomy is unnecessary.
- For every justified agent, define the complete contract required by the source section, including permissions, limits, approval, evaluation, observability, injection, and exfiltration controls.
- Decide REST, gRPC, events, MCP, A2A, or other interfaces from actual interaction needs.
- Have `data_mlops_architect` propose and `assurance_reviewer` challenge each justification.

Output: `outputs/stages/11-agent-architecture.md`.

Gate: user approval is required for any production agent. “No agent justified” is a valid passing result.
