# Stage 18 — Architecture decisions

**Status:** APPROVED  
**Completed:** 2026-08-13  
**Stage owner:** Primary architecture agent  
**Authorized specialist:** `assurance_reviewer` (read-only missing-alternative, supersession, and unsupported-choice challenge)

## Purpose and scope

Create the complete ARK architecture-decision register required by the governing prompt, verify that every material implementation constraint is either recorded in a dedicated ADR or deliberately remains a stage-level operational specification, and make partial supersessions, assumption expiries, production blocks, alternatives, risks, and measurable reconsideration triggers explicit.

Stage 18 does not redesign or reopen approved decisions. ADR-010 through ADR-015 formalize material comparisons whose underlying dispositions were approved in Stages 04, 06, 07, 10, 11, 15, and 17 but lacked dedicated ADR files. ADR-011 and ADR-015 also replace two temporary treatments that passed their recorded expiry points with explicit fail-closed admission states. The sponsor explicitly approved Stage 18 and ADR-010 through ADR-015, including both blocks, on 2026-08-13.

## Inputs read in full

- `WORKFLOW.md`
- `STATUS.md`
- `SOURCE_MANIFEST.md`
- `stages/STAGE-CONTRACT.md`
- `stages/18-architecture-decisions.md`
- `templates/stage-output.md`
- `templates/adr.md`
- `sources/normalized/system-design-prompt.md` — **17. Architecture decisions**
- Approved `outputs/stages/00-source-audit.md` through `outputs/stages/17-capacity-cost.md`
- `decisions/ADR-000-temporary-source-evidence-disposition.md` through `decisions/ADR-015-rest-json-and-typed-ports-before-grpc.md`
- `decisions/README.md`
- `quality/source-instruction-coverage.md`

## Specialist reconciliation

The Stage 18-authorized `assurance_reviewer` independently challenged the complete decision inventory, alternatives, reasons, risks, trade-offs, statuses, supersession claims, temporary-assumption lifecycle, production blocks, and all ten comparisons explicitly named by the source. Its initial review identified missing dedicated records, two expired temporary treatments, stale effective-status descriptions, historical drafting residue, and the ADR-005 authored/accepted date distinction. After reconciliation, its final review reported **PASS — no unresolved Critical, High, or material defects**. The primary agent remained the sole authoritative writer.

## Source-instruction coverage

| Governing requirement | Addressed in | Status/evidence |
|---|---|---|
| Decision | Complete ADR register | Covered |
| Context | Complete ADR register and each ADR | Covered |
| Chosen option | Complete ADR register and each ADR | Covered |
| Alternatives | Complete ADR register and each ADR's options table | Covered |
| Reason | Complete ADR register and each ADR rationale | Covered |
| Trade-offs | Complete ADR register and each ADR consequences | Covered |
| Risks | Complete ADR register and open/block registers | Covered |
| Status | Effective-status and supersession registers | Covered |
| Reconsideration trigger | Complete ADR register and dedicated ADR sections | Covered |
| Ten named comparisons | Comparison coverage matrix | Covered by dedicated ADRs |

## Confirmed facts

1. The sponsor explicitly approved every architecture stage through Stage 17 and accepted ADR-000 through ADR-009. `STATUS.md — Approved decisions`.
2. Accepted ADRs are immutable historical records. Later changes must be recorded by a superseding/refining ADR rather than overwriting history. `decisions/README.md`.
3. ADR-008 narrowly supersedes ADR-007's local digest-only model-cache clause; it does not supersede ADR-007's lifecycle or blocked capability profiles. Accepted ADR-008.
4. ADR-007 replaces the Stage 10 portions of ADR-002's `A-03-ML-MIGRATION` and `A-03-SYNAPSE` treatments with durable negative production-admission states. Accepted ADR-007.
5. Several accepted stage decisions were material and implementation-constraining but were intentionally not assigned ADR files when authored. Stage 18 is the prescribed point for the complete ADR set. Approved Stages 06, 10, 11, 15, and 17; workflow Stage 18.
6. No current evidence clears any capability, security, deployment, capacity, source-contract, or consumer-cutover production block. No current decision selects Kubernetes, a broker, a feature store, an agent runtime, gRPC, Rust, a GPU platform, or a vendor/managed service.
7. Approval authority comes from `STATUS.md` and recorded user evidence. Pre-approval words such as “proposed,” “recommend,” or “pending sponsor review” that remain inside an approved stage artifact are historical drafting residue and do not override the stage's recorded approval.
8. ADR-005 was authored on 2026-08-11 and explicitly accepted on 2026-08-12. The immutable ADR header retains its authored date; `STATUS.md` retains the acceptance date.

## Complete ADR register

The status column distinguishes the immutable file status from its current effective scope. “Partial replacement” does not erase the historical ADR.

| ADR | Decision | Context | Chosen option | Main alternatives | Reason | Trade-offs | Principal risks | Effective status | Reconsideration trigger |
|---|---|---|---|---|---|---|---|---|---|
| `ADR-000` | Temporary source-evidence disposition | Six normalized-only cards lack originals; Synapse internals sparse | Admit exact checksum-pinned files temporarily; Synapse interface facts only | Wait for originals; permanent authority; scope out | Continue without inventing provenance/internals | Revalidation burden; unresolved Synapse | Originals may conflict; provenance unknown | Accepted; active | Original/better evidence, checksum mismatch, scope decision |
| `ADR-001` | Stage 01 requirements baseline | Forty discovery questions and eight temporary assumptions | Approve baseline and time-bounded assumptions | Stop; answer all; infer conventional values | Smallest reversible path under missing evidence | Later stages conditional; expiry management | Assumptions may become stale | Accepted; portions replaced/dispositioned below | Any assumption expiry or authoritative answer |
| `ADR-002` | Capability evidence disposition | Prototype defects and Synapse evidence gaps at Stage 03 | Logical owners temporarily TBD; prototypes migration-only; Synapse interface-only | Supply evidence; scope out; infer details | Preserve inventory without granting readiness | Production unavailable; later re-entry decisions | Temporary treatment can be misread as approval | Accepted historical; ownership replaced by ADR-003, ML/Synapse Stage-10 portions by ADR-007 | New evidence, scope or owner assignment |
| `ADR-003` | Starting architecture style | Multiple capabilities but unknown scale/team/topology | Boundary-enforced modular monolith with durable-job/data-pipeline patterns and extraction gate | Microservices; SOA/ESB; event platform; whole-system pipeline; agentic; undisciplined monolith | Lowest distributed burden with enforceable evolution seams | Coordinated releases; boundary enforcement work | Shared-code/state erosion | Accepted; active | Specific extraction criterion passes |
| `ADR-004` | API/integration boundary | Need one platform-neutral API and durable lifecycle | Versioned REST/JSON namespace, typed operations, polling/jobs, conditional webhook, consumer adapters outside cores | Generic execute; API/service per capability; workflow API; push-only; concrete IdP | Common lifecycle without erasing capability contracts | Polling burden; contract governance; later adapter work | Temporary trust/cutover portions can overstay | Accepted; trust portion replaced by ADR-008; other `A-07` portions retain named expiries | Consumer/trust/delivery/cutover evidence or extraction |
| `ADR-005` | PostgreSQL-first job state machine | Durable async work without evidenced broker/workflow product | PostgreSQL jobs/attempts/leases/fences, at-least-once attempts, one logical effect | In-memory; external broker; workflow engine; per-capability queues; exactly once | Existing authority gives atomic lifecycle/idempotency at lowest burden | Critical DB code/tuning/recovery; handler idempotency | Queue contention or stale/ambiguous effects | Accepted; active | Measured broker/workflow/continuous-processing/extraction trigger |
| `ADR-006` | Governed proactive action and delivery | Need permissioned proactive evaluation without model/event authority | Separate records, deterministic two-phase gate plus at-effect recheck, schedules/jobs first, conditional outbox/webhook | Capability automation; generic workflow/event object; broker; push truth; direct sender | Preserve authority and truthful failure | More records/rechecks/reconciliation; blocked activation | Revocation races, ambiguous external effects | Accepted; active | Named workflow/action/consumer, security and measured event evidence |
| `ADR-007` | Versioned ML lifecycle and production admission | Prototype lifecycle defects and Synapse evidence expiry | Separate train/evaluate/promote/assign/infer; exact bundles; 4 `MIGRATION_BLOCKED` + 3 `EVIDENCE_BLOCKED` profiles; basic feature management | Continue assumptions; accept prototypes; remove capabilities; block workflow; full MLOps suite | Fail closed while keeping all capabilities and re-entry paths | No production capability; more metadata/approval work | Block status may be bypassed or mistaken for readiness | Accepted; active except local cache clause narrowed by ADR-008 | Per-profile evidence/owner/test gate or scope change |
| `ADR-008` | Zero-trust tenant/governance boundary | Trust, policy, crypto, provider and authority details absent at expiry | Provider-neutral fail-closed contracts plus 8 explicit security blocks; tenant-aware cache authorization | Extend assumptions; select products; minimal gateway/RLS controls | Implementable denial boundary without inventing vendors/policy | Production unavailable; repeated checks/control work | Missing named authorities or concrete mechanisms | Accepted; active; narrowly supersedes ADR-007 cache clause | Exact block-exit evidence, owners, new provider/agent/boundary evidence |
| `ADR-009` | Provisional implementation target | Sponsor clarified implementation/operation preference | Python, PostgreSQL, one Linux server; sponsor + AI assistance; optional containers; no Kubernetes/Rust/lake product yet | Mandatory containers; Kubernetes; Rust/lake platform; multi-server | Lowest sponsor-operable implementation burden | One failure/resource domain; no HA/fitness claim | Single-operator and shared-host limits | Accepted; active provisional target | Measured target, environment/team mandate, dependency/security need |
| `ADR-010` | Shared vs separate databases | Need operational transactions and large immutable storage with module ownership | Shared PostgreSQL cluster with owned schemas/writers; object storage by reference | Unrestricted shared DB; database per module; polyglot stores | Simple coordinated operation while preserving logical ownership | Shared failure/contention; discipline required | Cross-write/join erosion; cross-store reconciliation | Accepted; formalizes approved Stages 04/06/15 | Extraction, persistent contention, or mandated physical boundary |
| `ADR-011` | Push vs pull ingestion and source-contract admission | Upstreams authoritative; volume/cadence unknown; `A-01-DATA` expired | Push/micro-batch plus referenced bulk; pull/federation/CDC/streaming conditional; `DATA_CONTRACT_ADMISSION_BLOCKED` | Pull; shared DB; streaming default; federation; extend expired assumption | Clear source ownership and replayable raw-first contract without silently extending unknown semantics | Upstream delivery burden; no generic real-time promise; concrete contracts remain blocked | Source correction/order/identity ambiguity | Accepted; formalizes Stage 06 and replaces expired `A-01-DATA` | Named source proves push/object path cannot meet approved need; each contract separately admitted |
| `ADR-012` | Basic feature management vs feature store | Need PIT/version/reproduction without shared online feature evidence | Capability-owned transforms/manifests/immutable feature datasets on existing stores | Full feature store; shared mutable tables; ad-hoc recomputation | Required invariants do not require a new product | Explicit reuse/governance work; no online serving claim | Skew or duplication may emerge later | Accepted; formalizes approved Stage 10 | Governed reuse/skew/latency/scale trigger passes |
| `ADR-013` | Rules/ML service vs AI agent | No admitted autonomous planning/tool/memory need | Deterministic rules/workflows/jobs and bounded ML/LLM interfaces; no agent selected | General agent; multi-agent/A2A; infer agent from Synapse names | All current needs are expressible deterministically with less risk | Less open-ended autonomy; future re-entry work | “No agent now” misread as permanent/unknown internals absent | Accepted; formalizes explicit Stage 11 approval | Full evidence-bounded Stage 11 re-entry gate passes |
| `ADR-014` | Build vs buy | ARK must own domain contracts; vendor/budget/workload evidence absent | Build ARK-owned logic/contracts; use replaceable built/managed adapters; select/buy only from evidence and approval | Build all; buy suite now; open-source-only | Avoid reinvention and premature procurement simultaneously | Interface/evaluation discipline; later selection work | Sponsor labor or vendor lock-in hidden | Accepted; formalizes approved Stages 15/17 | Concrete requirement, benchmark, TCO, owner, budget and approval packet |
| `ADR-015` | REST vs gRPC and consumer cutover | External HTTP consumers and in-process modules; no RPC/streaming need; cutover treatment expired | REST/JSON externally, typed ports internally, jobs for durable work; no baseline gRPC; `CONSUMER_CUTOVER_BLOCKED` | Internal/external gRPC; generic HTTP execute; indefinite legacy coexistence | Match evidence and avoid network services or unapproved migration | JSON/HTTP overhead; schema governance; explicit cutover packet later | Protocol inertia, oversized payloads, or indefinite adapters | Accepted; formalizes Stages 07/11 and replaces expired cutover treatment | Named consumer/extracted service proves protocol need; approved cutover packet clears block |

## Required named-comparison coverage

| Required comparison | Dedicated decision(s) | Chosen disposition | Completeness |
|---|---|---|---|
| Modular monolith versus microservices | `ADR-003` | Boundary-enforced modular monolith; extraction only by measured gate | Complete |
| Shared versus separate databases | `ADR-010`, constrained by `ADR-003/008` | Shared PostgreSQL infrastructure with owned schemas/writers; separate DB conditional | Complete |
| Push versus pull ingestion | `ADR-011` | Push/micro-batch and referenced bulk default; pull/CDC/streaming exceptions | Complete |
| Synchronous versus asynchronous processing | `ADR-004`, `ADR-005` | Sync only for measured short/predictable operations; otherwise durable jobs | Complete |
| Queue versus event broker | `ADR-005`, `ADR-006` | PostgreSQL job/outbox state first; broker only by measured dispatch/fan-out gate | Complete |
| Scheduled versus event-driven execution | `ADR-005`, `ADR-006`, `ADR-011` | Versioned schedules/jobs first; named event/source triggers conditional | Complete |
| REST versus gRPC | `ADR-015`, refines `ADR-004` | REST/JSON external, typed ports/jobs internal; gRPC conditional | Complete |
| Build versus buy | `ADR-014`, constrained by `ADR-009` and Stage 17 | Own ARK contracts; no purchase now; evaluate concrete adapters/services by TCO | Complete |
| Rules/ML service versus AI agent | `ADR-013`, refines `ADR-003/007` | Deterministic rules/workflows and bounded ML/LLM; no agent currently justified | Complete |
| Basic feature management versus feature store | `ADR-012`, refines `ADR-007` | Versioned capability-owned transforms/materializations; no standalone store | Complete |

## Supersession and refinement register

| Earlier record/scope | Later record | Exact effect | Preserved scope |
|---|---|---|---|
| ADR-001 `A-01-ML` Stage-03 portions | ADR-002 | Replaced ML-01/04/05/06 temporary treatment at Stage 03 | Historical baseline and unrelated discovery assumptions |
| ADR-002 `A-03-OWNERSHIP` | ADR-003 `A-04-OWNERSHIP` | Replaced ownership deferral at Stage 04 with tighter production/extraction expiry | Capability evidence findings |
| ADR-001 `A-01-INT` Stage-07 boundary portions | ADR-004 `A-07-INTEGRATION` | Replaced adapter/API/delivery default treatment with named per-portion expiries | Unrelated requirements |
| ADR-002 `A-03-ML-MIGRATION` and Stage-10 Synapse portion | ADR-007 | Replaced temporary assumptions with 4 durable migration blocks and 3 evidence blocks | Historical evidence, source restrictions and advisory-verifier boundary |
| ADR-004/ADR-001 trust/security deferrals | ADR-008 | Replaced trust and security-policy uncertainty with provider-neutral controls and 8 blocks | Adapter placement, polling, delivery/cutover portions of ADR-004 |
| ADR-007 local digest-keyed cache clause | ADR-008 Decision 12 | Narrowly superseded with tenant/capability/purpose/assignment-aware authorization; byte reuse only by classified digest | All lifecycle, profile, assignment and other cache constraints |
| ADR-001 `A-01-OPS` at Stage 15 | ADR-009 + `DEPLOYMENT_ENVIRONMENT_BLOCKED` | Retired broad deployment deferral; selected provisional target and explicit unresolved production environment block | Concrete unanswered OPS requirements remain open evidence |
| Approved stage decisions without dedicated ADR | ADR-010 through ADR-015 | Formalizes the approved baseline; accepted with Stage 18 | Original approved stage artifacts remain authoritative detail |
| Expired ADR-001 `A-01-DATA` | ADR-011 `DATA_CONTRACT_ADMISSION_BLOCKED` | Replaces the unusable temporary treatment with per-contract fail-closed admission | Stage 06 logical contract design remains approved |
| Expired ADR-004 `A-07-INTEGRATION` legacy coexistence/cutover portion | ADR-015 `CONSUMER_CUTOVER_BLOCKED` | Replaces the unusable temporary cutover treatment with an evidence/approval gate | ADR-004 REST, adapter, polling and conditional-delivery decisions remain |

No accepted ADR file is deleted or rewritten to conceal its historical state. The effective register above is authoritative for later assembly.

## Temporary-assumption lifecycle

| Assumption | Current disposition | Effective constraint/expiry |
|---|---|---|
| `A-00-01` / ADR-000 temporary normalized-only evidence | Active | Revalidate when originals/provenance arrive or checksum changes |
| `A-00-02` / ADR-000 Synapse interface-only evidence | Active | Until authoritative Synapse evidence or scope change |
| `A-01-BUS` | Active | Product/MVP/channel/CDP answers B-01–B-05 or superseding scope decision |
| `A-01-DATA` | **Expired; replaced** | Accepted ADR-011 replaces it with `DATA_CONTRACT_ADMISSION_BLOCKED`; no concrete source/canonical contract is activatable without its recorded gate |
| `A-01-ML` | Dispositioned, not silently active | ADR-002/007/013 and explicit blocked profiles now govern ML-01–06; numeric quality/authority inputs remain unresolved gates, not defaults |
| `A-01-INT` | Replaced for Stage-07 boundary | `A-07-INTEGRATION`, ADR-006 and ADR-008 govern; no body tenant or unapproved action |
| `A-01-SCALE` | Active | Measured S-01–S-04 targets and approved operation/release profiles; Stage 17 formulas alone do not expire it |
| `A-01-SEC` | Dispositioned at Stage 12 | ADR-008 controls and blocks replace security-policy deferral |
| `A-01-OPS` | Dispositioned at Stage 15 | ADR-009 plus `DEPLOYMENT_ENVIRONMENT_BLOCKED`; unresolved OPS evidence remains required |
| `A-01-TEAM` | Partially active | TEAM-04 resolved by ADR-003; TEAM-01/02 remain until roster/Stage 20; TEAM-03 remains until budget/procurement evidence or before commitment |
| `A-03-OWNERSHIP` | Replaced | `A-04-OWNERSHIP` governs |
| `A-03-ML-MIGRATION` | Replaced | Four ADR-007 `MIGRATION_BLOCKED` profiles govern |
| `A-03-SYNAPSE` | Replaced for Stage-10 production admission | ADR-000 interface restriction plus ADR-007 `EVIDENCE_BLOCKED`, ADR-008 provider block, and ADR-013 no-agent decision govern |
| `A-04-OWNERSHIP` | Active | Named assignments or before Stage 20 approval, extraction, or production readiness—whichever comes first |
| `A-07-INTEGRATION` | Partially replaced; cutover portion **expired and replaced** | Trust portion replaced by ADR-008; proactive authority by ADR-006; accepted ADR-015 replaces expired coexistence/cutover with `CONSUMER_CUTOVER_BLOCKED`; remaining adapter ownership, polling and conditional-delivery portions retain their named evidence gates |

## Production-admission decision register

| Decision state | Count/scope | Clearing authority/evidence | Current effect |
|---|---|---|---|
| `MIGRATION_BLOCKED` | Churn, RFM, NPT, REC | Per-capability scientific, data, release, security/operations owners; remediation, evaluation, reproduction, assignment, rollback and Stage 16 evidence; explicit decision | No production execution |
| `EVIDENCE_BLOCKED` | Synapse Chat, Message, Verifier | Authoritative provider/model/prompt/data/state/safety/reliability/evaluation evidence; affected stage review; explicit decision | Interface inventory only; no production call |
| ADR-008 blocks | 8 named security blocks | Exact Stage 12 exit evidence and named authorities; explicit decision | No external trust/data/secret/privileged/delivery/LLM/supply-chain/cache admission |
| `DEPLOYMENT_ENVIRONMENT_BLOCKED` | Production Linux environment | Exact hosting/network/TLS/identity/secrets/backup/telemetry/sizing/recovery/patch/runbook evidence and approval | Benchmark target only; no production fitness |
| `CAPACITY_ADMISSION_BLOCKED` | Each production release/profile lacking Stage 17 packet | Workload, objectives, environment, price, benchmarks, headroom, runbooks, blocks and sponsor approval | No production sizing/purchase claim |
| `DATA_CONTRACT_ADMISSION_BLOCKED` | Every concrete source/canonical contract while identifiers, semantics, correction rules or owners are unresolved | ADR-011 evidence packet, Stage 06/16 validation and named source/data authority approval | No source/canonical contract activation; approved logical schemas are not admission evidence |
| `CONSUMER_CUTOVER_BLOCKED` | Legacy coexistence, compatibility bridge, dual running and consumer migration | ADR-015 consumer/version inventory, mapping, reconciliation, rollback, window, tests and named acceptance approval | No cutover or assumption-based indefinite coexistence |
| `A-04-OWNERSHIP` block | Production promotion/extraction/operations | Named accountable owners and runbook/on-call authority | Logical design only |

These states are cumulative. Passing one test or selecting a managed product clears none automatically.

## Stage-level decisions that do not require another ADR

| Stage decision | Why it remains stage-level | Governing ADRs |
|---|---|---|
| Stage 02 system boundary and 26 requirements | Requirements baseline/traceability, not a new mechanism choice | ADR-001/002 |
| Stage 03 per-capability target contracts/gaps | Detailed application of evidence disposition; production states later in ADR-007 | ADR-000/002/007 |
| Stage 05 component inventory and flows | Logical decomposition applying selected style | ADR-003 |
| Stage 06 four acceptance layers and data schemas | Contract detail; storage/ingestion comparisons now recorded by ADR-010/011 | ADR-003/010/011 |
| Stage 08 job transition tables | Implementable detail of PostgreSQL job decision | ADR-005 |
| Stage 09 event schemas and gate ordering | Implementable detail of proactive boundary | ADR-006 |
| Stage 10 manifests/evaluation profiles | Implementable detail of lifecycle and blocks | ADR-007/012 |
| Stage 12 asset/threat/admission matrices | Implementable detail of zero-trust boundary | ADR-008 |
| Stages 13–14 failure/observability matrices | Operationalization of existing authority and lifecycle decisions | ADR-004–008 |
| Stage 15 release/migration/backup mechanics | Operationalization of provisional target; products remain blocked | ADR-009/014 |
| Stage 16 test matrix | Verification strategy, not a technology choice | All applicable ADRs |
| Stage 17 symbolic formulas/benchmarks | Measurement strategy; no numeric/purchase choice | ADR-009/014 |

Any later material choice that changes these mechanisms, ownership boundaries, production block states, selected technology, protocol, product, topology, or purchase must create a new ADR or explicitly refine/supersede an existing one.

## Major recommendations

### R-18-01 — Use the effective register, not filename status alone

**Requirement/where:** prompt Section 17; all downstream assembly. **Why now:** historical ADR files can correctly remain `ACCEPTED` while portions are later replaced. **Simplest implementation:** publish immutable ADR files plus this explicit scope-level supersession register. **Alternative:** edit old files to `SUPERSEDED`. **Why rejected:** partial replacement and historical approval would be obscured. **Trade-off:** readers must consult the effective register. **Reconsideration:** a future decision fully supersedes an ADR, in which case its new ADR and index status state that explicitly.

### R-18-02 — Require dedicated ADRs only for material implementation constraints

**Requirement/where:** Stage contract and ADR completeness. **Why now:** too few ADRs hide choices; an ADR per table/field makes history unusable. **Simplest implementation:** record style, ownership, protocol, storage, execution, data, ML/agent, security, deployment, and build/buy choices; keep schemas/matrices as governed detail. **Alternative:** ADR for every recommendation. **Why rejected:** duplicates stage outputs and creates approval noise. **Trade-off:** judgment is required when a detail becomes material. **Reconsideration:** a stage detail changes component/product/owner/authority/topology/protocol or irreversible cost.

### R-18-03 — Treat negative and provisional decisions as real decisions

**Requirement/where:** risks/status/reconsideration; implementation safety. **Why now:** “not selected” or “blocked” can disappear from conventional ADR summaries. **Simplest implementation:** retain explicit negative decisions, exact re-entry evidence, and cumulative block register. **Alternative:** list only selected technologies. **Why rejected:** later implementers could silently add agents, brokers, stores, providers, or enable capabilities. **Trade-off:** the register is longer. **Reconsideration:** only through its measurable trigger and explicit approval.

## Decisions

- Adopt this complete effective ADR register, named-comparison coverage, supersession map, assumption lifecycle, production-admission register, and stage-level-versus-ADR boundary as the approved Stage 18 decision package.
- Recognize ADR-000 through ADR-009 as the previously accepted historical records. Submit ADR-010 through ADR-015 for explicit Stage 18 sponsor approval: they formalize approved stage-level comparisons, while ADR-011 and ADR-015 additionally establish the fail-closed replacements for expired data-contract and cutover assumptions.
- Do not alter or reopen any accepted baseline decision.
- Create no ADR for reliability matrices, observability schemas, test mechanics, or symbolic capacity formulas because they operationalize existing decisions and do not select a new material mechanism.
- Preserve all production-admission blocks and unresolved evidence.
- Keep Stage 19 unstarted until the sponsor explicitly approves Stage 18 and authorizes continuation.

## Contradictions and dangerous assumptions

| ID | Finding | Resolution | Consequence |
|---|---|---|---|
| `C-18-01` | ADR-002 says “not superseded,” while ADR-007 later replaces two scoped treatments | Treat ADR-002 as accepted history with explicit partial replacement in the effective register | No false full supersession or stale assumption |
| `C-18-02` | ADR-004 says “superseded by none,” while ADR-008 later replaces its trust deferral | Record scope-level replacement; preserve API/adapter/polling/cutover decisions | Trust cannot rely on stale bearer assumption |
| `C-18-03` | ADR-007 says digest-keyed local cache, while ADR-008 narrows it | ADR-008 Decision 12 is authoritative for cache identity/authorization | `MODEL_CACHE_BLOCKED` remains |
| `C-18-04` | Approved stages said no new ADR while containing material named comparisons | Stage 18 creates ADR-010–015 using explicit historical approval evidence | Durable coverage without reopening decisions |
| `C-18-05` | `ACCEPTED` can be mistaken for production admitted | Separate decision acceptance from capability/security/deployment/capacity states | No accepted ADR clears production blocks |
| `C-18-06` | “No agent” or “no gRPC” can be read as permanent prohibition | Every negative decision has a measurable/evidence re-entry trigger | Evolution remains possible without speculative implementation |
| `C-18-07` | Build-versus-buy can be read as “build everything” | ADR-014 separates owned domain contracts from replaceable infrastructure adapters | No reinvention or unauthorized procurement |
| `C-18-08` | Shared database can be read as shared state ownership | ADR-010 makes schemas/writers/ports/roles mandatory | Shared infrastructure never broadens authority |
| `C-18-09` | Stage 17 `CAPACITY_ADMISSION_BLOCKED` could be mistaken for a new global architecture component | Treat as release/profile admission state, cumulative with existing blocks | No unnecessary ADR/component or sizing claim |
| `C-18-10` | `A-01-DATA` passed its “before Stage 06 approval” expiry but was still described as active | Mark it expired and unusable; ADR-011 establishes `DATA_CONTRACT_ADMISSION_BLOCKED` | No source/canonical activation from stale assumptions |
| `C-18-11` | The legacy coexistence/cutover portion of `A-07-INTEGRATION` passed its Stage 16 expiry | Mark it expired and unusable; ADR-015 establishes `CONSUMER_CUTOVER_BLOCKED` | Bounded adapters cannot masquerade as an approved cutover plan |
| `C-18-12` | Approved stage files retain pre-approval words such as “proposed” or “pending sponsor review” | Treat `STATUS.md` and recorded user evidence as approval authority; preserve old artifacts as historical drafts | No retrospective rewrite or false reopening |
| `C-18-13` | ADR-005 header date is 2026-08-11 while its acceptance evidence is 2026-08-12 | Record 2026-08-11 as authored date and 2026-08-12 as acceptance date | Historical file remains immutable and provenance is unambiguous |

## Open questions and decisions requiring future approval

| ID | Question | Blocking? | Options | Recommended temporary disposition | Effect |
|---|---:|---|---|---|---|
| `Q-18-01` | Which capabilities, consumers and workflows are first-release scope? | Before roadmap/release | One vertical slice; subset; phases | Keep all product-scoped; activate none without admission | Stage 20 sequencing remains conditional |
| `Q-18-02` | Who are the named product/data/platform/scientific/security/integration/release/operations owners? | Before Stage 20 approval/production/extraction | Assign people/services and separation | Keep `A-04-OWNERSHIP` | No production/extraction approval |
| `Q-18-03` | What concrete operation targets, retention/governance, environment, recovery, budget and deadline apply? | Before production/commitments | Supply versioned policies/profiles | Preserve explicit blocks/unknowns | No production fitness or purchase |
| `Q-18-04` | Can originals and authoritative Synapse/provider evidence be supplied? | Before permanent source authority/Synapse enablement | Supply; scope out; remain unavailable | Preserve ADR-000/007/008/013 restrictions | No Synapse production call |
| `Q-18-05` | What LAB operating contract and acceptance authority apply? | Before LAB release gate | Advisory; required evidence; veto with authority | Evidence consumer only | No implicit promotion authority |

## Requirements-traceability updates

| Requirement | Decision coverage | Remaining evidence |
|---|---|---|
| `ARK-CON-001/002/003` | ADR-003, ADR-010 | Boundary/schema ownership and extraction tests |
| `ARK-CON-004/005` | ADR-005, ADR-010, ADR-011 | Storage/job benchmarks and production environment |
| `ARK-CON-007` | All ADR triggers; ADR-014 | Explicit decision before new infrastructure/purchase |
| `ARK-FR-002/003` | ADR-010/011 | Source contracts, policy and implementation evidence |
| `ARK-FR-004–008` | ADR-004/005/015 | Operation profiles, limits and tests |
| `ARK-FR-009` | ADR-007/012 | Per-profile re-entry evidence |
| `ARK-FR-010/011` | ADR-006/013 | Named grants/workflows/consumers and security admission |
| `ARK-NFR-001/005` | ADR-008/010 | Exact security block exits |
| `ARK-NFR-002/006` | ADR-007/008/010 | Retention/owner/environment evidence |
| `ARK-NFR-004` | ADR-005/006 | Operation policies and failure tests |
| `ARK-NFR-007`, `SC-02-12` | ADR-009/014 plus Stage 17 | Approved workload/target/environment/cost packet |
| Prompt Section 17 named comparisons | ADR-003–015 comparison matrix | None at logical decision level; implementation evidence remains gated |

## Completion-gate evidence

| Gate item | Result | Evidence |
|---|---|---|
| Complete ADR table has all ten required fields | PASS | Complete ADR register |
| All ten named comparisons have dedicated decisions | PASS | Named-comparison coverage |
| One file per material decision | PASS | ADR-000 through ADR-015 inventory |
| Alternatives and unsupported choices challenged | PASS | ADR option tables plus authorized assurance review |
| Superseded/refined scopes linked without deletion | PASS | Supersession register and ADR sections |
| Temporary assumptions have truthful lifecycle | PASS | Expired `A-01-DATA` and cutover treatment are replaced by accepted fail-closed dispositions |
| Production blocks remain explicit | PASS | Production-admission register |
| No approved decision reopened | PASS | ADR-010 through ADR-015 preserve and formalize the approved baseline |
| Authorized assurance review reconciled | PASS | Final reviewer result: no unresolved Critical, High, or material defect |
| Explicit Stage 18 user-approval gate | PASS | Sponsor approved Stage 18 and ADR-010 through ADR-015 on 2026-08-13 |
| Stage 19 not executed | PASS | Scope and stop condition |

**Gate result: PASSED AND APPROVED.** The decision audit, authorized assurance review, and explicit sponsor gate all passed. ADR-010 through ADR-015 are accepted; Stage 19 is authorized and no later stage is authorized.

## Downstream consequences

- Stage 19 must diagram only selected logical mechanisms and clearly label conditional/unselected alternatives and active blocks.
- Stage 20 must use ADR triggers and the assumption/block register when sequencing implementation; it cannot silently add products or enable profiles.
- Stage 21/23 must publish this effective register and preserve partial supersessions rather than copying stale per-file status alone.
- Stage 22 must map runtime placement to ADR-003/005/009/010/015 without turning roles into services.
- Stage 24 must challenge every implementation component against its ADR/requirement/trigger and verify no accepted decision is contradicted.

## Exact next-stage inputs and stop condition

Stage 18 is approved. Stage 19 is the only authorized next stage.

After validation passes and the sponsor explicitly approves Stage 18, ADR-010 through ADR-015, and continuation, Stage 19 must read:

1. Approved `outputs/stages/00-source-audit.md` through `outputs/stages/18-architecture-decisions.md`
2. Accepted ADR-000 through ADR-009, sponsor-approved ADR-010 through ADR-015, and the Stage 18 effective register
3. `sources/normalized/system-design-prompt.md` section **18. Diagrams**
4. `stages/19-diagrams.md`, diagram templates/assets if any, and the approved component/data/API/execution/event/ML/security/deployment flows
5. Every active production block and conditional/unselected mechanism that must be labeled visually

Execute Stage 19 only after explicit sponsor authorization. Do not begin Stage 20.
