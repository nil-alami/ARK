# Stage 09 — Event and proactive-action architecture

Governing source: `system-design-prompt.md` section **8. Event and proactive-action architecture**.

Inputs: Stages 05–08 and proactive-operation assumptions.

## Work

- Define evaluation triggers, standing authorizations, schedule/threshold/channel configuration, insight-to-event conversion, subscriptions, delivery, retries, DLQ, deduplication, ordering, expiry, throttling, acknowledgement, replay, and audit.
- Provide versioned example event and webhook schemas.
- Distinguish internal technical events, domain events, commands, notifications, and actionable ML insights.
- State when an insight is reported versus when ARK may act.
- Ask `platform_architect` for delivery-semantics review.

Output: `outputs/stages/09-events-proactive-actions.md`.

Gate: proactive action cannot bypass subscription, explicit authorization, data freshness, thresholds, policy, quota, cooldown, deduplication, or audit.
