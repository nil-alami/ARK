# ARK Reference MVP

> **ADR-017/018 implementation notice:** the architecture documents now define account→organization→business hierarchy, uniform organization capability patterns, organization-scoped admin access, one shared owner billing balance, and organization credit policies with job-linked reservation/settlement. The current runnable MVP predates those decisions and is not conformant. See [ADR-017-IMPACT.md](docs/mvp/ADR-017-IMPACT.md), [ADR-018-IMPACT.md](docs/mvp/ADR-018-IMPACT.md), and [MVP-STATUS.md](implementation/MVP-STATUS.md).

This repository contains a local, non-production architectural hypothesis for one ARK Recommendation run. A deterministic synthetic retail fixture crosses ARK's important runtime boundaries while a Gradio dashboard renders the structured execution trace emitted by the run.

## Run locally

Python 3.12 is recommended.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\run.ps1
```

The launcher binds to all local network interfaces. Open `http://127.0.0.1:7860` on the host machine, or `http://<host-LAN-IP>:7860` from another device on the same trusted network. Select one of the two scenarios and choose **Start Run**. This workspace also carries a local `.vendor` dependency directory so the included `run.ps1` works in the Codex desktop runtime without a separate package installation.

The MVP has no authentication. Use it only on a trusted local network; do not expose port 7860 to the public internet.

Run the smoke tests with:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## What the demo executes

The app provides exactly two scenarios:

- **Successful Recommendation**: all 216 submitted rows are valid and the run completes.
- **Invalid rows -> quarantine + degraded execution**: four deliberately invalid rows are quarantined; the 216-row valid subset continues with warnings.

Every run performs initialization, fixture submission, tenant resolution, entitlement evaluation, receipt, Pydantic schema validation, quarantine, normalization, readiness and Recommendation eligibility checks, job queueing, worker execution, feature generation, candidate generation, ranking and business rules, SQLite result persistence, result delivery, and final audit/trace closure. The result contains three ranked unseen products for each of 24 customers.

Pipeline cards, activity history, progress, warnings, row counts, branch decisions, masked before/after samples, and stage details are derived from persisted `TraceEvent` records. Runs, jobs, quarantine records, trace events, and result payloads are stored in `.data/ark_mvp.db`.

## Implementation boundary

Functional in this MVP: deterministic data transformation, validation, quarantine, normalization, aggregate feature computation, candidate generation, ranking/rules, job-state transitions, SQLite persistence, replayable event history, and result retrieval.

Deliberately simplified: tenant context, entitlement, data receipt, readiness/eligibility thresholds, queue/worker separation, audit, and result delivery. These are explicit seams inside one Python process, not production implementations or production decisions.

Excluded: production IAM, external connectors, distributed workers, Kafka, Kubernetes, production workflow infrastructure, model training/serving, multi-capability orchestration, production SLOs, and scientific validation. See [DEFERRED.md](DEFERRED.md) for the concrete follow-on list and `docs/mvp/` for the design-to-MVP mapping.

## Architecture knowledge system

The implementation guidance for module identity documents, machine-readable manifests, shared patterns, ADR links, and task-aware agent context is in [ARK-KNOWLEDGE-SYSTEM.md](docs/engineering/ARK-KNOWLEDGE-SYSTEM.md). Reusable templates live under `templates/`, and the project-scoped resolver skill lives under `.codex/skills/ark-context-resolver/`. These artifacts guide implementation and navigation; they do not change production admission or activate illustrative technologies and capabilities.
