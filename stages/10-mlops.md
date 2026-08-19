# Stage 10 — ML and MLOps architecture

Governing source: `system-design-prompt.md` section **9. ML and MLOps architecture**.

Inputs: Stages 03, 05–09 and service-card ML facts.

## Work

- Define experiment, dataset, feature, training, evaluation, promotion, registry, deployment, inference, loading, rollout, rollback, drift, feedback, retraining, explainability, reproducibility, fairness, and safety flows.
- Make contract, dataset, feature-schema, model, code, and execution versions independently traceable.
- Decide whether a full feature store is justified; if not, define the simpler consistency controls.
- Separate platform MLOps services from capability-owned model lifecycle.
- Use `data_mlops_architect` for independent review.

Output: `outputs/stages/10-mlops.md`.

Gate: every capability can reproduce a prediction and training result from versioned evidence; model promotion and rollback have accountable gates.
