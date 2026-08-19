# Stage 03 — Capability and service inventory

Governing source: `system-design-prompt.md` section **2. Capability and service inventory**.

Inputs: Stage 02, all service cards, assumptions.

## Work

- Run one `capability_analyst` per available service card; parallelize only across separate cards.
- Produce the full compact contract required by the governing section for every named ML/AI capability.
- Separate current implementation facts from the intended ARK contract and migration work.
- Separate shared platform responsibilities from capability-owned responsibilities.
- Mark each missing card as blocked, explicitly out of scope, or assumption-based with user approval.

Output: `outputs/stages/03-capability-inventory.md` using `templates/service-contract.md`.

Gate: no named capability is silently omitted. A complete-ARK claim is blocked until all cards are present or explicitly dispositioned by the user.
