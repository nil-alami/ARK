# Stage 12 — Security, privacy, and governance

Governing source: `system-design-prompt.md` section **11. Security, privacy, and governance**.

Inputs: Stages 02–11 and data-sensitivity facts.

## Work

- Define tenant isolation, IAM, service identity, least privilege, secrets, encryption, PII, residency, audit, consent, retention, model access, agent security, abuse prevention, and supply-chain controls.
- Make authenticated principal the authoritative tenant source.
- Cover isolation across rows, objects, datasets, models, jobs, events, caches, quotas, audit, logs, metrics, and traces.
- Create a concise realistic threat model with trust boundaries and mitigations.
- Use `assurance_reviewer` for adversarial review.

Output: `outputs/stages/12-security-governance.md`.

Gate: no trust boundary or tenant-bearing asset lacks identity source, authorization rule, isolation mechanism, and audit behavior.
