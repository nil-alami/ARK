# Stage 01 — Discovery and architecture-driving questions

Governing source: `system-design-prompt.md` sections **Project information** and **Working rules**.

Inputs: Stage 00, all assumptions, and source manifest.

## Work

- Restate known facts without changing their status.
- Ask one organized batch of material questions grouped by business, data, ML, integration, scale, security, operations, and team constraints.
- For each unanswered question, propose a temporary assumption and explain its architectural effect and risk.
- Identify contradictions or dangerous assumptions.
- Produce an initial decision-needed-now versus decision-can-wait split.

Output: `outputs/stages/01-discovery-and-questions.md`.

Gate: user approves the requirements baseline, answers questions, or explicitly authorizes the listed temporary assumptions. Do not advance automatically.
