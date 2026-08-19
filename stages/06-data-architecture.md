# Stage 06 — Data architecture

Governing source: `system-design-prompt.md` section **5. Data architecture**.

Inputs: Stages 02–05, assumptions, capability data needs.

## Work

- Design all ingestion options and select defaults/exceptions from evidence.
- Define canonical contracts, schema versioning, validation layers, tenant isolation, data zones, ownership, retention, lineage, PII controls, quality, backfill, reprocessing, duplicate, and late-data behavior.
- Explicitly distinguish structural validity, semantic validity, dataset readiness, and capability eligibility.
- Include one concrete data lifecycle with identities and version fields at each transition.
- Use `data_mlops_architect` for independent review.

Output: `outputs/stages/06-data-architecture.md`.

Gate: lifecycle is implementable, storage purpose and authoritative writer are explicit, and large payloads/results are passed by reference where required.
