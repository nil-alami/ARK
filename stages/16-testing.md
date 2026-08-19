# Stage 16 — Testing strategy

Governing source: `system-design-prompt.md` section **15. Testing strategy**.

Inputs: Stages 02–15.

## Work

- Define unit, contract, integration, end-to-end, data-quality, model, event-delivery, load, resilience, security, tenant-isolation, and agent evaluations if applicable.
- Map tests to requirements, risks, interfaces, and deployment gates.
- Identify production-blocking scenarios and test data/fixture needs.
- Distinguish tests owned by each capability, shared platform, adapters, and LAB.
- Use `assurance_reviewer` to identify missing high-risk coverage.

Output: `outputs/stages/16-testing.md`.

Gate: every critical risk and contract has at least one test level, owner, environment, pass criterion, and release consequence.
