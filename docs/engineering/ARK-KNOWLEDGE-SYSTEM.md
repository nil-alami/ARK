# ARK knowledge system implementation

Status: `IMPLEMENTATION GUIDANCE — DOES NOT SUPERSEDE ACCEPTED ADRS`

Source basis: `sources/original/ARK knowledge system.docx` and its normalized working copy at `sources/normalized/ark-knowledge-system.md`.

## Purpose

The ARK knowledge system gives developers, reviewers, tools, and coding agents a small, deterministic route to the architecture information relevant to a task. It complements source files, accepted ADRs, approved stage outputs, and executable contracts; it does not replace their authority.

## Authority and safety rules

1. Existing source precedence and accepted ADR supersession rules remain controlling.
2. Generated indexes and resolver output are navigation aids, never authoritative truth.
3. A `MODULE.md` describes current identity and links to contracts; it is not the canonical schema.
4. A `module.yaml` contains discoverable structural facts; it is never runtime authorization, tenant, entitlement, model-assignment, or production-admission truth.
5. Illustrative technologies and names in the source document do not select products or add capabilities.
6. Missing or contradictory evidence fails visibly. The resolver must not invent a path, dependency, contract, owner, or ADR relationship.

## Artifact model

| Artifact | Scope | Required when | Canonical responsibility |
|---|---|---|---|
| `ARK.md` | Whole implementation | A production implementation repository is created | System purpose, boundaries, flows, invariants, links |
| `CONTEXT.md` | Major architectural area | The area groups several meaningful modules | Membership, interactions, dependency constraints |
| `MODULE.md` | Logical module | The entity owns behavior, contracts, or state | Human-readable identity and boundaries |
| `COMPONENT.md` | Important subcomponent | It has a substantial independent responsibility | Local boundary and consequences |
| `module.yaml` | Logical module | Tooling must discover the module | Machine-readable facts and links |
| Pattern document | Module family | More than one module shares an implementation convention | Required structure and dependency rules |
| ADR | Material decision | Alternatives and durable consequences exist | Decision rationale and supersession |
| `DEVELOPMENT_OVERRIDES.md` | One module | The module has a justified local exception | Narrow deviation, reason, scope, and exit condition |

Do not create identity files for ordinary classes, repositories, helpers, or packages.

## Repository placement

```text
ARK.md
architecture/
├── contexts/
├── decisions/
└── patterns/

src/ark/modules/<module>/
├── MODULE.md
├── module.yaml
├── contracts/
└── implementation...

tooling/architecture/context_resolver/
```

In this design repository, accepted ADRs remain under `decisions/`, implementation patterns live under `docs/engineering/patterns/`, reusable identity templates live under `templates/`, and the project skill lives under `.codex/skills/ark-context-resolver/`.

## Minimum `MODULE.md` contract

Every module identity must state:

- purpose;
- responsibilities and non-responsibilities;
- public/versioned contracts;
- allowed dependencies and forbidden direct access;
- state, schema, object, result, or artifact ownership;
- tenant and authorization scope;
- core execution flows;
- events produced and consumed;
- failure, retry, idempotency, and audit obligations;
- governing pattern and local overrides;
- related accepted ADRs;
- unresolved gaps and activation status.

Use `templates/module-identity.md`.

## Minimum `module.yaml` contract

Use `templates/module-manifest.yaml`. Required fields are `id`, `name`, `kind`, `tenant_scope`, `pattern`, and `identity`. Collection fields should be present as empty lists when intentionally empty so absence is distinguishable from omission.

Additional constraints:

- `id` is globally unique and stable.
- Paths are repository-relative or module-relative as declared by the schema.
- `depends_on` lists module IDs, not Python packages or product names.
- `owns_data` names logical state sets; it does not grant access to foreign state.
- `related_adrs` uses actual repository ADR IDs.
- `status` records implementation/admission state but cannot clear a block.
- Secrets, credentials, personal data, tenant IDs, endpoints, and mutable environment values are prohibited.

## Resolver contract

The resolver accepts a repository root, target module ID, and optional task description. It performs these steps:

1. Discover manifests and reject duplicate IDs.
2. Resolve the target identity.
3. Resolve its implementation pattern.
4. Resolve declared contracts and ADRs.
5. Resolve relevant dependency identities.
6. Use task terms to rank optional context without suppressing mandatory authority.
7. Return paths, artifact types, and inclusion reasons.
8. Report missing or contradictory references separately.

The first implementation returns a context manifest; it does not concatenate every file. The consuming agent reads only the returned artifacts required for the task.

## Dependency and context rules

- Always include the target manifest and identity.
- Include the selected pattern for implementation, refactoring, or review work.
- Include target contracts for API, schema, event, compatibility, or integration work.
- Include dependency identities when the task crosses a declared boundary.
- Include related ADRs for architecture, ownership, tenancy, security, state, or decision-rationale work.
- Include broader system/context documents only when the target package cannot resolve the question.
- Never include unrelated capability internals merely because they share a pattern.

## Generated registry

A future `architecture-registry.json` may be generated from validated manifests for dependency graphs, indexes, diagrams, context routing, and linting. It must be reproducible and excluded from manual maintenance. The source manifests remain its input; the registry does not become a second ownership record.

## Change workflow

| Change | Required updates |
|---|---|
| Module behavior | Code, tests, `MODULE.md`; manifest only if structural facts change |
| Public contract | Versioned contract, consumers/tests, module identity, manifest contract link |
| Architecture decision | New/superseding ADR, affected identities/manifests, downstream impact record |
| Shared implementation convention | Pattern document and migration guidance |
| Local exception | `DEVELOPMENT_OVERRIDES.md` with reason and exit condition |
| User-visible history | Appropriate changelog or release evidence |

## Implementation sequence

1. Adopt the identity and manifest templates for one pilot module.
2. Validate the pilot with the context-resolver skill and script.
3. Add the concrete capability pattern only to modules that use it.
4. Add architecture linting for duplicate IDs, missing paths, unresolved dependencies, and forbidden imports.
5. Generate indexes or diagrams only after manifests are validated.
6. Expand to other module families when at least two real modules share a stable convention.

## Acceptance criteria

- A target module resolves to one identity, one manifest, one pattern, declared contracts, declared dependencies, and actual ADR paths.
- Duplicate IDs and broken references fail deterministically.
- Resolver output explains every included artifact.
- Unrelated module internals are excluded.
- Generated output is reproducible from committed source artifacts.
- No metadata file can change runtime authorization, tenant scope, admission, or production status.

