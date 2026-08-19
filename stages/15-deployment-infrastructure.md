# Stage 15 — Deployment and infrastructure

Governing source: `system-design-prompt.md` section **14. Deployment and infrastructure**.

Inputs: Stages 04–14 and known environment constraints.

## Work

- Recommend the simplest adequate deployment model and compare Kubernetes with simpler approaches.
- Define environments, configuration, containers, CI/CD, migrations, model deployment, IaC, secrets, scaling, backups, rollback, releases, and developer/test environments.
- Map modular ownership to deployable runtime roles without pretending each module is a microservice.
- Provide deployment alternatives and measurable extraction/scaling triggers.
- Use `platform_architect` for operational-fit review.

Output: `outputs/stages/15-deployment-infrastructure.md`.

Gate: unknown hosting constraints remain explicit; the recommended starting deployment can be operated by the known team or is clearly conditional on team confirmation.
