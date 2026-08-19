# Stage 00 — Source integrity and intake audit

Status: `APPROVED`

## Purpose and scope

Inventory and integrity-check every supplied source, map source authority and capability coverage, expose contradictions and dangerous assumptions, classify missing information, and request disposition of blocking source gaps. This stage does not design ARK.

## Inputs read in full

- `AGENTS.md` — all sections
- `WORKFLOW.md` — all sections
- `STATUS.md` — all sections
- `SOURCE_MANIFEST.md` — all sections
- `stages/STAGE-CONTRACT.md` — all sections
- `stages/00-source-audit.md` — all sections
- `templates/stage-output.md` — all sections
- `sources/SHA256SUMS` — complete checksum list
- `sources/normalized/system-design-prompt.md` — all sections
- `sources/normalized/ark-assumptions.md` — all sections
- `sources/normalized/service-cards/churnobyl.md` — all sections
- `sources/normalized/service-cards/RFM.md` — all sections
- `sources/normalized/service-cards/next_purchase_prediction.md` — all sections
- `sources/normalized/service-cards/recommender.md` — all sections
- `sources/normalized/service-cards/Synapse_chatbot.md` — all sections
- `sources/normalized/service-cards/synapse_message_generator.md` — all sections
- `sources/normalized/service-cards/synapse_campaign_verifier.md` — all sections

The configured `source_auditor` completed a bounded, read-only completeness and contradiction scan. Its findings agreed that manifest-listed hashes match, six cards are unregistered normalized-only sources, three Synapse cards are materially incomplete, and user disposition is required. The primary agent reconciled those findings against the source hierarchy and retained sole authorship of this artifact.

## Source-instruction coverage

| Source requirement | Addressed in | Status/evidence |
|---|---|---|
| Inventory every normalized source | Source inventory and capability coverage | Addressed; nine normalized files found and read |
| Verify files and checksums | Integrity results | Addressed; all three original files and all nine normalized files were hashed |
| Identify named capabilities and cards | Capability coverage | Addressed; seven named capabilities each have a physical card |
| Build authority map | Source authority map | Addressed |
| Expose contradictions | Contradictions and dangerous assumptions | Addressed |
| Classify missing information | Missing-information classification | Addressed |
| Do not design ARK | Entire artifact | Satisfied; no component or architecture selection is made |
| Ask user to disposition blocking missing sources | Resolved approval questions Q-00-01 and Q-00-02 | Pass; explicit approval recorded in `decisions/ADR-000-temporary-source-evidence-disposition.md` |

## Facts

### Source inventory and integrity results

| ID | Source | Physical state | Integrity/provenance result |
|---|---|---|---|
| F-00-01 | `sources/original/System_design_Prompt.docx` and `sources/normalized/system-design-prompt.md` | Both present | Recorded SHA-256 values match current files |
| F-00-02 | `sources/original/ARK Project assumptions.docx` and `sources/normalized/ark-assumptions.md` | Both present | Recorded SHA-256 values match current files |
| F-00-03 | `sources/original/683b67c3-d20d-4e43-8c09-f5ae9c6be574.md` and `sources/normalized/service-cards/churnobyl.md` | Both present | Recorded SHA-256 values match current files |
| F-00-04 | RFM, NPT, REC, and three Synapse working-copy cards | Six normalized files present | They were absent from the manifest/checksum inventory and have no corresponding file under `sources/original/`; Stage 00 has now checksum-pinned their exact contents |
| F-00-05 | `sources/original/` | Three files present | No original evidence exists in the repository for the six discovered working-copy cards |
| F-00-06 | `SOURCE_MANIFEST.md` and pre-audit `STATUS.md` | Present but stale | Both said six capability cards were missing although those working-copy files physically existed |

Exact added working-copy SHA-256 values are recorded in `SOURCE_MANIFEST.md — SHA-256 checksums` and `sources/SHA256SUMS`.

### Capability coverage

| Capability named by the governing prompt | Card | Evidence state | Intake disposition |
|---|---|---|---|
| Churn/Churnobyl | `sources/normalized/service-cards/churnobyl.md` | Detailed card; manifest-linked original exists; owner remains TBD | Available as capability evidence |
| Customer segmentation/RFM | `sources/normalized/service-cards/RFM.md` | Detailed normalized-only card; owner TBD | Approved as temporary evidence pending original |
| Next-purchase prediction/NPT | `sources/normalized/service-cards/next_purchase_prediction.md` | Detailed normalized-only card; production owner not explicit | Approved as temporary evidence pending original |
| Recommendation/REC | `sources/normalized/service-cards/recommender.md` | Detailed normalized-only card; owner TBD | Approved as temporary evidence pending original |
| Synapse LLM chatbot | `sources/normalized/service-cards/Synapse_chatbot.md` | Normalized-only public interface fragment; many required sections blank | Approved as temporary interface-contract-only evidence; undocumented internals unresolved |
| Synapse LLM message generator | `sources/normalized/service-cards/synapse_message_generator.md` | Normalized-only public interface fragment; many required sections blank | Approved as temporary interface-contract-only evidence; undocumented internals unresolved |
| Synapse campaign-policy verifier | `sources/normalized/service-cards/synapse_campaign_verifier.md` | Normalized-only public interface fragment; policy/configuration semantics and many required sections blank | Approved as temporary interface-contract-only evidence; undocumented internals unresolved |
| LAB | No capability card expected | The prompt classifies LAB as a testing/validation platform, not an ML capability | Treat as a consumer/platform in later discovery |

Evidence: `sources/normalized/system-design-prompt.md — Project information`; each card's `PURPOSE`, `INPUT CONTRACT`, `OUTPUT CONTRACT`, and operational sections; `SOURCE_MANIFEST.md — Expected capability-card coverage`.

### Source authority map

| Precedence | Source class | Stage 00 finding |
|---:|---|---|
| 1 | Explicit post-package user decisions in `decisions/` | `decisions/ADR-000-temporary-source-evidence-disposition.md` accepted; governs temporary admission and Synapse evidence limits |
| 2 | `sources/normalized/ark-assumptions.md` | Present; authoritative declared ARK baseline; manifest-linked original and matching recorded hashes |
| 3 | `sources/normalized/system-design-prompt.md` | Present; authoritative process and deliverable contract; manifest-linked original and matching recorded hashes |
| 4 | `sources/normalized/service-cards/` | Seven physical cards; Churn has linked original; six exact pinned cards are admitted temporarily; Synapse is interface-contract-only evidence |
| 5 | Temporary assumptions | A-00-01 and A-00-02 below are explicitly approved and expire on receipt of better evidence |

Evidence: `AGENTS.md — Source authority`; `SOURCE_MANIFEST.md — Authority and integrity`.

## Assumptions

| ID | Assumption | Why needed | Architectural effect | Risk | Validation/expiry |
|---|---|---|---|---|---|
| A-00-01 | The exact checksum-pinned RFM, NPT, REC, and three Synapse cards may be used as temporary evidence pending originals | Preserves workflow progress without claiming verified provenance | Later stages may cite explicit card content but must not elevate card recommendations into decisions | An eventual original may differ | Recheck on any checksum change or receipt of an original; invalidate affected downstream work if content conflicts |
| A-00-02 | Synapse evidence is limited to explicitly documented interface-contract facts; every undocumented internal remains unresolved | Prevents invented LLM, agent, policy, security, runtime, and operating claims | Stage 01 may discover requirements; Stage 03 must reapply its capability-evidence gate | Capability inventory may remain incomplete | Expires when authoritative Synapse implementation/configuration/policy evidence arrives or scope changes |

Approval: `decisions/ADR-000-temporary-source-evidence-disposition.md — Decision`.

## Analysis and recommendations

### R-00-01 — Require explicit provenance disposition for normalized-only cards

- Requirement satisfied: source integrity, visible conflicts, and explicit disposition of blocking missing evidence.
- Exact stage/workflow where used: completion of Stage 00 and evidence admission for Stages 01–24.
- Why needed now: the physical repository contradicts its manifest, and file hashes establish identity but not origin or authority.
- Simplest viable implementation: preferably supply and register the six originals/provenance; if unavailable, explicitly approve the exact checksum-pinned normalized files as temporary evidence.
- Alternative considered: silently treat every file under `sources/normalized/` as provenance-verified.
- Why the alternative is not preferred: it would erase a material source-integrity gap and violate the instruction not to silently resolve conflicts.
- Trade-offs and operational burden: supplying originals adds intake work but enables fidelity checks; temporary approval is low effort but retains provenance risk in every downstream citation.
- Measurable reconsideration trigger: receipt of original evidence or an explicit source-authority decision recorded under `decisions/`.

### R-00-02 — Keep incomplete Synapse evidence contract-only unless expanded or scoped out

- Requirement satisfied: do not invent missing capability facts; do not claim completeness for unsupported capability contracts.
- Exact stage/workflow where used: Stage 01 discovery and the Stage 03 capability-inventory gate; later security, reliability, agent-justification, and deployment stages.
- Why needed now: the three Synapse cards define request/response fragments but omit owners, internal dependencies, model/provider configuration, runtime limits, persistence, fallback, policy semantics, and most observability evidence.
- Simplest viable implementation: accept the published interface facts only, keep every blank field unresolved, and require additional evidence or explicit assumption authorization before Stage 03 completes.
- Alternative considered: infer conventional LLM-service internals.
- Why the alternative is not preferred: the governing prompt prohibits invented scale, security, availability, and unjustified agent architecture.
- Trade-offs and operational burden: preserves correctness but may block Stage 03; supplying OpenAPI, implementation/configuration, policy, and operating evidence removes that block.
- Measurable reconsideration trigger: new Synapse evidence, explicit scoping-out, or explicit approval of contract-only assumption treatment.

## Decisions

- `decisions/ADR-000-temporary-source-evidence-disposition.md` is `ACCEPTED`.
- The six exact checksum-pinned normalized-only cards are admitted as temporary evidence pending originals.
- Synapse is interface-contract-only evidence; every undocumented internal remains unresolved.
- This is a source-governance decision, not approval of any architecture recommendation contained in a card.

## Contradictions and dangerous assumptions

| ID | Type | Evidence | Precedence/resolution state | Consequence |
|---|---|---|---|---|
| C-00-01 | Source-inventory contradiction | `SOURCE_MANIFEST.md — Expected capability-card coverage` and pre-audit `STATUS.md — Known source inventory` said six cards were missing; six files exist under `sources/normalized/service-cards/` | Resolved for intake by `ADR-000`; provenance remains a tracked risk pending originals | Later stages may use pinned content temporarily and must revalidate against originals |
| C-00-02 | Target-versus-current integration gap | The baseline prohibits supported direct shared-database integration and requires platform-neutral adapters; RFM, NPT, REC, and Churn cards document direct database/BCDP access and shared persistence | Target baseline wins for future design; cards remain current-state evidence | Later stages must model migration, not normalize current coupling as the target (`sources/normalized/ark-assumptions.md — Integration and contracts`; cards — `OWNERSHIP / ISOLATION`) |
| C-00-03 | Target-versus-current execution gap | The baseline requires one durable platform job manager; Churn and RFM use a process-local daily scheduler and synchronous caller semantics, while NPT/REC are synchronous batches without active durable-job integration | Target baseline wins; current behavior is migration evidence | Later execution design must not treat current schedulers as an approved job lifecycle (`sources/normalized/ark-assumptions.md — Execution, orchestration, and proactive operation`; cards — `TRIGGER / EXECUTION MODE`) |
| C-00-04 | Security gap | Tenant identity must come from an authenticated principal; Churn and RFM cards report route declarations that do not enforce authentication or tenant authorization | Baseline security rule wins | Current endpoints are prototype risks, not approved target contracts (`sources/normalized/ark-assumptions.md — Security, ownership, and operations`; Churn/RFM cards — `INTEGRATION`) |
| C-00-05 | RFM semantic contradiction | RFM declares `Champions` the best-ranked cluster, but the card reports industry weights are not applied and recency is not inverted, so higher recency can improve rank | Current implementation contradicts intended semantic meaning | Stage 03 must separate intended labels from implemented ranking (`sources/normalized/service-cards/RFM.md — PURPOSE`; `OUTPUT CONTRACT`) |
| C-00-06 | Cross-contract inconsistency | RFM produces semantic enums `0–4`, while its documented downstream agent API accepts `0–5` | Unresolved; no higher-precedence source selects meaning for `5` | Must be resolved before an integrated public contract is accepted (`sources/normalized/service-cards/RFM.md — INTEGRATION`) |
| C-00-07 | Agent-label dangerous assumption | Synapse identifiers call components “Agent,” but the supplied cards describe synchronous request/response LLM endpoints and no autonomous planning, tool selection, dynamic execution, or multi-step control evidence | Naming is not justification; Stage 11 must decide only from evidence | Do not pre-approve an agentic architecture (`sources/normalized/system-design-prompt.md — Working rules`; Synapse cards — `INFRASTRUCTURE CLASSIFICATION`) |
| C-00-08 | REC implementation contradiction | REC describes low-data fallback sources, but its current top-level 200-transaction gate returns before those fallbacks execute | Current implemented behavior is authoritative as current-state evidence | Eligibility/fallback semantics require an explicit later contract (`sources/normalized/service-cards/recommender.md — PURPOSE`; `ELIGIBILITY / PRECONDITIONS`) |
| C-00-09 | NPT implementation contradiction | NPT model-output fields and final-output fields do not align, so predictions can be computed while `nostradamus.served=false` | Current readiness blocker, not silently repaired here | Stage 03 must distinguish intended from implemented output (`sources/normalized/service-cards/next_purchase_prediction.md — Current readiness assessment`; `OUTPUT CONTRACT`) |

## Resolved approval questions

| ID | Resolution | Decision evidence |
|---|---|---|
| Q-00-01 | Use the six checksum-pinned cards as temporary evidence pending originals | `decisions/ADR-000-temporary-source-evidence-disposition.md — Decision` |
| Q-00-02 | Treat Synapse as interface-contract-only evidence and keep every undocumented internal unresolved | `decisions/ADR-000-temporary-source-evidence-disposition.md — Decision` |

## Open questions

| ID | Question | Blocking? | Options | Recommended temporary assumption | Effect |
|---|---|---:|---|---|---|
| Q-00-03 | Who owns each capability and the shared platform boundaries? | No for Stage 00; architecture-affecting | Name accountable owners; approve temporary team-level owners; leave unresolved | Use “owner TBD” without inventing ownership | Affects service boundaries, escalation, deployment, and roadmap |
| Q-00-04 | What are the tenant/traffic scale, latency and availability objectives, deployment environment, team size, budget, and deadline? | No for Stage 00; architecture-affecting | Supply targets; authorize bounded temporary assumptions later; leave unknown | Keep unknown and measure before infrastructure commitments | Prevents premature Kubernetes, broker, capacity, SLO, or cost choices |
| Q-00-05 | What are the authoritative retention, residency, identity-resolution, consent, proactive-permission, and policy-verification semantics? | No for Stage 00; architecture-affecting | Supply policies; explicitly defer; authorize narrow temporary assumptions later | Keep unresolved and prohibit action beyond explicit grants | Affects data, security, governance, and proactive workflows |
| Q-00-06 | Does downstream segment value `5` have a meaning, or must consumers accept only RFM values `0–4`? | No for Stage 00; blocking before integrated contract approval | Remove `5`; define it; version an adapter mapping | Restrict ARK-owned RFM contract to evidenced values `0–4` | Prevents ambiguous segmentation behavior |

## Missing-information classification

### Blocking source/approval gaps

- None remain for Stage 00 or for starting Stage 01.
- The incomplete Synapse capability evidence may block Stage 03 unless authoritative evidence, explicit scoping, or a later approved assumption satisfies that stage's complete-contract gate.

### Architecture-affecting but deferrable

- Capability and platform ownership.
- Tenant scale, traffic mix/volume, latency SLOs, availability targets, team size, budget, and deadline.
- Deployment environment and constraints.
- Data retention, deletion, residency, consent, identity resolution, and CDP positioning.
- Exact proactive authorization, threshold, cooldown, notification, and campaign-policy semantics, including whether the verifier is advisory or enforcing.
- Observability depth and the RFM enum consumer mismatch.
- LAB validation responsibilities and acceptance interface beyond its classification as an external validation platform.

### Implementation detail

- Concrete broker/workflow product, if later justified.
- Exact container/orchestrator choice, cache, service-discovery mechanism, and deployment topology.
- LLM provider/model, temperature, token ceilings, prompt versions, timeouts, retry settings, and cache behavior, except where they affect residency, safety, or contract compatibility.
- Exact per-capability tuning values not already evidenced or approved.

## Requirements-traceability updates

| Trace ID | Requirement | Source | Current evidence/status | Downstream use |
|---|---|---|---|---|
| RT-00-001 | Preserve source authority and expose conflicts | `AGENTS.md — Source authority` | Authority map and contradiction register created; temporary source disposition approved in `ADR-000` | Every later stage |
| RT-00-002 | Cover all seven initial capabilities | `sources/normalized/system-design-prompt.md — Project information` | Seven physical cards admitted; six are temporary evidence; three Synapse cards remain interface-only and incomplete | Stages 01 and 03 |
| RT-00-003 | Treat LAB as validation platform, not ML capability | `sources/normalized/system-design-prompt.md — Project information` | Confirmed; no LAB capability card required | Stages 01, 02, 16, 20 |
| RT-00-004 | Do not invent unknown scale/security/availability facts | `sources/normalized/system-design-prompt.md — Working rules` | Unknowns classified and retained | Stages 01, 04, 12–17 |
| RT-00-005 | Use declared ARK baseline over lower-authority current implementations | `sources/normalized/ark-assumptions.md — Product and architecture`; `AGENTS.md — Source authority` | Current-target gaps identified without designing their solution | Stages 02–23 |

## Completion-gate evidence

| Gate item | Result |
|---|---|
| Every governing Stage 00 work item addressed | Pass |
| All normalized sources inventoried and read in full | Pass |
| Current hashes calculated; registered hashes verified | Pass |
| Named capability coverage explicit | Pass |
| Source conflicts and dangerous assumptions visible | Pass |
| Missing information classified | Pass |
| No ARK architecture designed | Pass |
| User explicitly approved disposition of blocking normalized-only/incomplete evidence | Pass — `decisions/ADR-000-temporary-source-evidence-disposition.md` accepted 2026-08-11 |

Stage 00 is `APPROVED`. `STATUS.md` advances to Stage 01, which is not executed as part of this stage.

## Downstream consequences

- No later stage may describe the six normalized-only cards as provenance-verified; they are temporary evidence under `ADR-000`.
- Later outputs may cite the pinned working copies while retaining their temporary/provisional label where material.
- If originals arrive and differ, the conflict must be recorded and any affected later work invalidated.
- Stage 01 may now begin as the next incomplete stage.
- Stage 03 must distinguish implemented behavior, intended behavior, and missing Synapse evidence, and may require another stop if required contract facts remain unsupported.
- Current prototype coupling, scheduling, authentication gaps, and internal card contradictions are migration evidence, not target decisions.

## Exact next-stage inputs

Stage 01 must read:

- `stages/01-discovery-and-questions.md`.
- `sources/normalized/system-design-prompt.md — Project information` and `Working rules`.
- `sources/normalized/ark-assumptions.md` in full.
- `outputs/stages/00-source-audit.md` in full.
- `decisions/ADR-000-temporary-source-evidence-disposition.md` in full.
- All capability cards admitted by that decision, preserving the Synapse interface-only constraint.
