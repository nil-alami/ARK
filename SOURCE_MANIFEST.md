# Source manifest

## Authority and integrity

The original files are immutable evidence. The normalized files are searchable working copies. If wording appears ambiguous, inspect the corresponding original before deciding.

| Source | Working copy | Purpose | Authority/provenance | Date received | Status |
|---|---|---|---|---|---|
| `sources/original/System_design_Prompt.docx` | `sources/normalized/system-design-prompt.md` | Governing design process and deliverables | Original evidence with normalized working copy | Unknown (present when package was created) | Present; recorded checksums verified 2026-08-11 |
| `sources/original/ARK Project assumptions.docx` | `sources/normalized/ark-assumptions.md` | Consolidated ARK decisions and baseline | Original evidence with normalized working copy | Unknown (present when package was created) | Present; recorded checksums verified 2026-08-11 |
| `sources/original/683b67c3-d20d-4e43-8c09-f5ae9c6be574.md` | `sources/normalized/service-cards/churnobyl.md` | Churn/Churnobyl capability facts | Original evidence with normalized working copy | Unknown (present when package was created) | Present; recorded checksums verified 2026-08-11 |
| Not supplied | `sources/normalized/service-cards/RFM.md` | Customer segmentation/RFM capability facts | Normalized-only evidence admitted temporarily by `decisions/ADR-000-temporary-source-evidence-disposition.md`; original pending | Unknown | Temporary evidence approved 2026-08-11; checksum-pinned |
| Not supplied | `sources/normalized/service-cards/next_purchase_prediction.md` | Next-purchase prediction/NPT capability facts | Normalized-only evidence admitted temporarily by `decisions/ADR-000-temporary-source-evidence-disposition.md`; original pending | Unknown | Temporary evidence approved 2026-08-11; checksum-pinned |
| Not supplied | `sources/normalized/service-cards/recommender.md` | Recommendation/REC capability facts | Normalized-only evidence admitted temporarily by `decisions/ADR-000-temporary-source-evidence-disposition.md`; original pending | Unknown | Temporary evidence approved 2026-08-11; checksum-pinned |
| Not supplied | `sources/normalized/service-cards/Synapse_chatbot.md` | Synapse LLM chatbot interface facts | Normalized-only, interface-contract-only evidence admitted temporarily by `decisions/ADR-000-temporary-source-evidence-disposition.md`; original pending | Unknown | Temporary interface evidence approved 2026-08-11; undocumented internals unresolved |
| Not supplied | `sources/normalized/service-cards/synapse_message_generator.md` | Synapse LLM message-generator interface facts | Normalized-only, interface-contract-only evidence admitted temporarily by `decisions/ADR-000-temporary-source-evidence-disposition.md`; original pending | Unknown | Temporary interface evidence approved 2026-08-11; undocumented internals unresolved |
| Not supplied | `sources/normalized/service-cards/synapse_campaign_verifier.md` | Synapse campaign-policy-verifier interface facts | Normalized-only, interface-contract-only evidence admitted temporarily by `decisions/ADR-000-temporary-source-evidence-disposition.md`; original pending | Unknown | Temporary interface evidence approved 2026-08-11; undocumented internals unresolved |
| Sponsor decision in Codex task | `sources/sponsor-decisions/2026-08-15-owner-organization-business.md` | Account/organization/business hierarchy, uniform organization capability pattern, and organization-wide admin scope | Explicit sponsor decision after the original package; interpreted by accepted ADR-017 | 2026-08-15 | Present; checksum recorded below |
| Sponsor decision in Codex task | `sources/sponsor-decisions/2026-08-15-owner-billing-credit-management.md` | Shared owner billing account, organization credit policies, debit attribution, and dual financial request gate | Explicit sponsor decision after ADR-017; interpreted by accepted ADR-018 | 2026-08-15 | Present; checksum recorded below |
| Sponsor decision in Codex task | `sources/sponsor-decisions/2026-08-18-user-member-api-key-identity.md` | Concrete User/Member/Role/Permission/API-key identity model and removal of physical principal/generic-credential tables | Explicit sponsor decision after ADR-017/018; architecture reconciliation and a later ADR are required | 2026-08-18 | Present; checksum recorded below; does not clear any production block |
| Sponsor correction in Codex task | `sources/sponsor-decisions/2026-08-18-member-user-organization-uniqueness-correction.md` | One Member row per User and Organization through `UNIQUE (user_id, organization_id)` | Explicit sponsor correction to Decision 5 of the earlier 2026-08-18 identity source; multi-Organization membership remains allowed | 2026-08-18 | Present; checksum recorded below; architecture reconciliation required; clears no production block |
| Sponsor correction in Codex task | `sources/sponsor-decisions/2026-08-18-member-unique-api-key-correction.md` | Exactly one current active API key per active Member, with revoked predecessors retained only for rotation history | Explicit sponsor correction to Decision 7 of the earlier 2026-08-18 identity source; architecture reconciliation remains required | 2026-08-18 | Present; checksum recorded below; does not clear any production block |
| Sponsor decision in Codex task | `sources/sponsor-decisions/2026-08-18-organization-wide-member-business-and-capability-scope.md` | Organization-wide Role-limited Member reach to all Businesses and one capability pattern for all current/future Businesses | Explicit sponsor decision resolving the per-Business Member-access question and preserving ADR-017's uniform capability-pattern rule | 2026-08-18 | Present; checksum recorded below; architecture reconciliation required; clears no production block |
| `sources/original/ARK knowledge system.docx` | `sources/normalized/ark-knowledge-system.md` | Implementation knowledge model: identity documents, module manifests, implementation patterns, ADR linking, change workflow, and task-aware context routing | Sponsor-supplied implementation guidance; examples are illustrative and do not select products, add capabilities, supersede ADRs, or clear admission blocks | 2026-08-16 | Present; original and normalized checksums recorded below; implementation guidance only |

## Expected capability-card coverage

The system-design prompt names these initial capabilities:

| Capability | Card status | Completion effect |
|---|---|---|
| Churn/Churnobyl | Present | Evidence-based capability design allowed |
| Customer segmentation/RFM | Present; temporary normalized-only evidence approved | Temporary evidence-based analysis allowed; revalidate when original/provenance arrives |
| Next-purchase prediction/NPT | Present; temporary normalized-only evidence approved | Temporary evidence-based analysis allowed; revalidate when original/provenance arrives |
| Recommendation/REC | Present; temporary normalized-only evidence approved | Temporary evidence-based analysis allowed; revalidate when original/provenance arrives |
| Synapse LLM chatbot | Present; temporary interface-contract-only evidence approved | Use documented interface facts only; keep every undocumented internal unresolved and reapply the Stage 03 evidence gate |
| Synapse LLM message generator | Present; temporary interface-contract-only evidence approved | Use documented interface facts only; keep every undocumented internal unresolved and reapply the Stage 03 evidence gate |
| Synapse campaign-policy verifier | Present; temporary interface-contract-only evidence approved | Use documented interface facts only; keep every undocumented internal unresolved and reapply the Stage 03 evidence gate |
| LAB validation platform | Not a capability card | Treat as external validation consumer/platform per current prompt |

## SHA-256 checksums

```text
e1c4dfe9eef2fe23c0cab28ab69382693f76aa86646bb9e77e99181f64a9e47e  sources/original/683b67c3-d20d-4e43-8c09-f5ae9c6be574.md
870189df6c614b2b8e669d713ca7034847ed2b463cfad9f0895107cf5c0fa801  sources/original/ARK Project assumptions.docx
4aafa51af886449fd989a027e123eceee8a74fb3143e4a91a2375e0c2cddb6e6  sources/original/System_design_Prompt.docx
8535d1b5092d81aa7113d1bb409242cba044598d3b21b0d51fe6b1d0bdcf679a  sources/normalized/ark-assumptions.md
f302e97845dbb08cab38fcae05143a8377ed241ccca6c503549ed901bf1f436c  sources/normalized/system-design-prompt.md
d119c7d99d7fc4551b1a8df2be56b6599d95c81a33211ca2e3608440e57fc109  sources/normalized/service-cards/churnobyl.md
d17f34fdda65b174952c980d59c97ff095bbe34dc92583cd2061fc72bf5f862d  sources/normalized/service-cards/next_purchase_prediction.md
7cb992506e92317ed9e6dcdc166b157608c2ae8035790d1fa4cddff8cf5f542e  sources/normalized/service-cards/recommender.md
6634c6d2d87df1394b0917129c8fe66e687d115052e829257d4b9549719bf2ca  sources/normalized/service-cards/RFM.md
28b78fe6b83062745c8e39cfb4b426feb56b89573c4ac26af67a08ec3a219560  sources/normalized/service-cards/synapse_campaign_verifier.md
a6b5d73db5383e9f11dcf4614320242f7a6c6d1ca886a57989ba140545b6a54e  sources/normalized/service-cards/Synapse_chatbot.md
afcad912d74e31bb0d54ae8f179b04e7921432b529d10af3bb1ff79ea8e03950  sources/normalized/service-cards/synapse_message_generator.md
0ee7f8b5cb407f52dab9d1a4db721b784f5f060e9af3cfe61d96f95e3c0d1924  sources/sponsor-decisions/2026-08-15-owner-organization-business.md
49676e5a0ce6b20bdeb1aa734814759e75fde5184c9ceab1895e9e37f9a3f999  sources/sponsor-decisions/2026-08-15-owner-billing-credit-management.md
4e30e9ea9d5100401eb1f39d52c9919fe124287038d04fb7f9fcc766897055e1  sources/sponsor-decisions/2026-08-18-user-member-api-key-identity.md
29338b87e546345394c7b8050a162ad1c14b6f0f4522c740d9b0852f036d7d14  sources/sponsor-decisions/2026-08-18-member-user-organization-uniqueness-correction.md
cfe19b175eafd11948c8547fc4312d9b96f6e303e7a392a3a6f71495fb420d57  sources/sponsor-decisions/2026-08-18-member-unique-api-key-correction.md
2bd49d0bd817248b7e1b75ee9cd00d07b930fefd8ad7ebf8f4e5fdb9bc59c5e6  sources/sponsor-decisions/2026-08-18-organization-wide-member-business-and-capability-scope.md
a98c292cd67dcea9bbb23aa96e36a0a88e39806786cdabe759ec0b7ce4a71818  sources/original/ARK knowledge system.docx
37269a1dd4bd5d93d63aec8398e6e6553403007e937e8b941d204ec4915bc63a  sources/normalized/ark-knowledge-system.md
```

The Stage 00 hashes pin the exact files discovered during the original audit. The 2026-08-15 sponsor-decision hashes pin the later decision sources interpreted by ADR-017 and ADR-018. The four 2026-08-18 sponsor-decision hashes pin the concrete identity-model revision, its Member uniqueness and one-current-API-key corrections, and the Organization-wide Member/Business/capability scope decision; all still require architecture reconciliation and an ADR. The 2026-08-16 hashes pin the supplied ARK knowledge-system DOCX and its searchable normalization; they do not turn its examples into accepted decisions. A matching hash proves file identity, not provenance. Temporary-use approval is recorded in `decisions/ADR-000-temporary-source-evidence-disposition.md`.

When adding a source, record its filename, purpose, authority, capability coverage, date received, and checksum. Never replace evidence without preserving the earlier version.
