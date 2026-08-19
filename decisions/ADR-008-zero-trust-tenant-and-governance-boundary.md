# ADR-008 — Zero-trust tenant and governance boundary

Status: `ACCEPTED`

Date: 2026-08-12

Decision owner: ARK sponsor (human user), by explicit approval on 2026-08-12; security, privacy/data-governance, IAM, key/secret, audit, provider, supply-chain, and operations authorities remain unassigned

## Context and requirements

ARK is a multi-tenant AI capability platform whose data may include PII/pseudonymous identifiers, behavioral/transactional history, purchase values, campaign content, and model outputs. Accepted decisions already require principal-derived tenant scope, owned state, immutable data/model/job identities, fail-closed proactive authority, and blocked production capability profiles.

At Stage 12, the temporary trust portion of `A-07-INTEGRATION` reaches its decision point while the IdP, credential types, issuer/audience/tenant claim binding, revocation, workload identity, role matrix, cryptographic/key/secrets environment, compliance/residency/retention rules, webhook security, Synapse provider terms, and named authorities remain unknown. Those gaps cannot be silently extended or filled by convention.

## Decision

ARK adopts the Stage 12 security and governance boundary in `outputs/stages/12-security-governance.md`:

1. Tenant and actor authority comes only from a registered, validated trust profile and immutable trusted context. Request fields, paths, object names, event payloads, model outputs, and telemetry never establish or broaden tenant or permission scope.
2. Authentication is provider-neutral at design time but fail-closed at activation. Each human or workload credential class requires approved trust anchor/issuer, validation, audience, tenant-binding, lifetime/revocation, assurance, permission mapping, owner, and tests.
3. Authorization is deny-by-default at the edge and again at the authoritative owner module. The owner verifies exact action, resource tenant/state, purpose, data class, and policy version. Infrastructure policy and PostgreSQL RLS are defense in depth, not substitutes.
4. Each separately runnable role has a distinct least-privilege workload identity. Background work requires both workload authority and a non-forgeable tenant/job/attempt/fence/handler/purpose execution context. Delegation may narrow but never replace tenant authority.
5. The Stage 12 tenant-bearing asset matrix is normative. Every tenant-bearing asset must define identity source, authorization rule, isolation mechanism, and audit behavior before implementation or activation.
6. Secrets are opaque, scoped, versioned, rotated/revoked, and audit-accessed through a managed interface. Sensitive network traffic and stored databases, objects, backups, models/artifacts, audit, and retained telemetry require approved encryption. Exact products, algorithms, keys, regions, and tenant-key topology remain evidence-dependent.
7. Every data/model/LLM asset resolves to classification, purpose/consent policy where applicable, residency, retention/deletion/legal-hold, owner, and lineage. Unknown classification is treated as restricted and unavailable for external transfer. Deletion uses immediate access revocation plus policy-driven purge/impact handling; generic model unlearning is not claimed.
8. High-impact security/control/model/data/delivery/release actions require immutable audit before effect and distinct permissions. Exact role combinations, stronger-auth, dual-control, emergency access, and named authorities must be approved before activation.
9. Synapse remains `EVIDENCE_BLOCKED`; external LLM/provider processing is denied until provider/data-use/retention/residency, prompt/context, injection/exfiltration, safety, secret/egress, cost, audit, failure, and ownership evidence passes its re-entry gates. The verifier remains advisory. No agent/tool architecture is active.
10. Abuse protection and supply-chain provenance are production requirements: bounded inputs and resources, registered destinations/egress, tenant quotas/rates/cost, dependency locks/SBOM/provenance/scans, isolated builds, digest/signature verification, and separated build/promotion/assignment permissions. Concrete values/tools remain later evidence.
11. The following negative production-admission states remain until their exit evidence is approved: `EXTERNAL_TRUST_BLOCKED`, `DATA_GOVERNANCE_BLOCKED`, `CRYPTO_SECRETS_BLOCKED`, `PRIVILEGED_ACTION_BLOCKED`, `EXTERNAL_DELIVERY_BLOCKED`, `LLM_PROVIDER_BLOCKED`, `SUPPLY_CHAIN_BLOCKED`, and `MODEL_CACHE_BLOCKED`.
12. This ADR explicitly refines accepted ADR-007's local cache implementation constraint to resolve a material Stage 06/10 conflict. Authorization and cache identity include tenant, owner/capability, purpose, exact deployment assignment/version, and bundle digest. A lower-level immutable byte cache may reuse content by digest alone only when an approved classification declares the artifact globally/shareably identical; tenant-specific assignment, authorization, metadata, results, audit, and revocation remain isolated. Until this refinement is accepted and tested, model/artifact cache loading is `MODEL_CACHE_BLOCKED`.

This decision replaces the Stage 12 trust/security-policy deferral portions of `A-07-INTEGRATION` and `A-01-SEC` with explicit controls and negative admission states. It does not enable production, select a provider/product/vendor/algorithm/region/compliance regime, clear ADR-007 capability blocks, or authorize Stage 13.

## Options considered

| Option | Benefits | Costs/risks | Fit now | Reconsideration condition |
|---|---|---|---|---|
| Continue temporary security/trust assumptions | Avoids a decision | Violates expiry and risks accidental production trust | Rejected | Not applicable |
| Select concrete IdP, IAM, KMS, secrets, WAF, SIEM, DLP, region, and compliance stack now | Implementation specificity | No environment/legal/owner evidence; vendor and operational overcommitment | Rejected | Stage 15 receives authoritative requirements and approvals |
| Provider-neutral contracts plus explicit production-admission blocks | Preserves implementability and fail-closed safety without invention | Production remains unavailable until substantial evidence and ownership arrive | Selected | Clear each block only by its recorded exit evidence |
| Treat gateway authentication/RLS/encryption-at-rest as sufficient | Small control set | Misses owner authorization, non-database assets, delegated work, privacy lifecycle, provider, and supply-chain threats | Rejected | Never unless a superseding decision proves equivalent controls |

## Rationale

The selected option is the narrowest implementable security architecture consistent with current evidence. It turns expired uncertainty into testable denial states, preserves the approved logical architecture, and prevents a successful login, shared database role, model registry row, LLM response, or webhook registration from becoming unintended authority.

## Consequences and trade-offs

- No external caller, separately deployed role, production data onboarding, privileged action, webhook, Synapse/provider call, or production release is security-admitted yet.
- Implementers can build against stable trusted-context, owner-authorization, tenant-asset, audit, data-policy, secret, model, and supply-chain contracts without selecting vendors.
- Repeated authorization and audit checks add latency and implementation effort; they preserve ownership and reduce confused-deputy risk.
- Shared PostgreSQL/object infrastructure remains viable, but it requires module/tenant roles, RLS/storage policy defense, scoped references, and cross-tenant tests.
- Privacy deletion may require derived-data/model impact decisions; it cannot be solved by silently retaining everything or promising generic unlearning.
- Later environment/policy evidence may require stronger isolation or service extraction through ADR-003, but does not weaken these invariants.

## Implementation constraints

- No default trust profile, role binding, tenant claim, provider, endpoint, key, retention period, data-transfer authority, or abuse threshold.
- No body/header tenant authority; no caller-selected object/provider/callback/tool/model path.
- No owner-module authorization bypass for in-process calls, jobs, maintenance, or administrative access.
- No broad shared workload credential or database/object-storage access.
- No secret/plain PII in source, images, artifacts, prompts by default, logs, metrics, traces, errors, IDs, or event envelopes.
- No privileged/security-sensitive effect before required audit evidence.
- No production model load without exact approved assignment, digest, compatibility, revocation, tenant/capability namespace, and permission checks.
- No digest-only cache lookup as authorization or tenant/capability selection. Any byte-level cross-tenant deduplication requires an explicit shared-artifact classification and is subordinate to tenant-specific assignment, authorization, revocation, and audit.
- No external LLM/provider or webhook egress without approved destination, data/purpose policy, credentials, and audit.
- No dependency/model/build artifact admission without provenance and integrity evidence.
- No new security product or service boundary without a traced requirement, owner, operational model, and anti-overengineering review.

## Validation evidence

- User approval dated 2026-08-12: “I approve Stage 12 and accept ADR-008, including its narrow supersession of ADR-007’s local model-cache key clause. Record the approval and execute only Stage 13.”
- `outputs/stages/12-security-governance.md` maps every governing source requirement, defines the normative asset matrix and threat model, and records all unresolved production blocks.
- The Stage 12-authorized read-only `assurance_reviewer` identified the accepted cache-key contradiction; it was reconciled through the Stage 12 matrix, contradiction/admission records, and this ADR's Decision 12 and narrow supersession clause. The final pass reported no critical or high defects and recommended `PASS`.
- Future verification includes cross-tenant negative tests for every matrix row; trust/role/delegation tests; audit-unavailable tests; provider/prompt injection/exfiltration tests; webhook SSRF/signature/replay tests; deletion-impact tests; and supply-chain provenance/integrity tests.

## Reconsideration trigger

- Authoritative identity, credential, role, compliance, residency, retention/deletion, key/secret, provider, delivery, deployment, or supply-chain evidence.
- Named accountable owner assignments.
- A release-applicable security-admission block supplies all exit evidence.
- A new service/compliance boundary satisfies ADR-003 extraction criteria.
- New Synapse or future-agent evidence reopens ADR-007 or Stage 11.

## Supersedes / superseded by

This ADR replaces only the Stage 12 trust/security-policy deferral portions of `A-07-INTEGRATION` and `A-01-SEC`, and narrowly supersedes ADR-007's “local caches ... keyed by exact bundle digest” implementation constraint with the tenant/capability/purpose/assignment-aware rule in Decision item 12. It preserves the API/adapter/polling/cutover portions of ADR-004, all accepted ADR-003/005/006 authority and effect-safety controls, every ADR-007 capability block and lifecycle decision outside that cache-key clause, and Stage 11's no-agent result. Superseded by: none.
