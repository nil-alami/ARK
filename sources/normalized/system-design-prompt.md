## **Sample Prompt**

You are acting as a Principal AI Architect, Senior System Designer, and
Senior Applied AI/ML Engineer.

Your job is to design a production-capable system containing multiple
independent ML services and, only where genuinely useful, AI agents.

I need a complete system design from initial requirements through
implementation and production operation. However, you must actively
prevent overengineering. Do not add a component merely because it is
common in large architectures.

**Project information**

Use the following information as your starting point:

- **Project/product name**: ARK

- **Business purpose:** Provide a multi-tenant AI platform that helps
  businesses understand customers, predict behavior, personalize
  recommendations and communications, and run policy-compliant campaigns

- **Consumers:** Internal platforms such as Direct, Whatson, POS and
  LAB; future external client platforms; business users consume results
  through those platforms

- **Initial ML capabilities:** Customer churn prediction, customer
  segmentation (RFM), next-purchase prediction (NPT), recommendation
  (REC), Synapse LLM chatbot, Synapse LLM message generator, and Synapse
  campaign-policy verifier; LAB tests and validates ARK services

- **Possible agentic capabilities:** Permissioned proactive monitoring
  and scheduled execution—an ML service detects a condition, ARK
  validates the tenant’s subscription, authorization, thresholds and
  configuration, runs an approved capability/workflow, optionally
  generates and verifies a campaign message, and sends an event or
  result to the platform

- **Expected number of tenants/customers:** Unknown; architecture
  assumes multiple tenants and must support growth and tenant-specific
  configuration

- **Expected traffic:** Unknown; expected to include interactive API
  requests, incremental data events, scheduled jobs, large historical
  uploads, batch inference/training and webhook/event notifications

- **Data sources:** Push APIs by default, object-storage/file uploads
  for initial loads and backfills, platform databases through
  platform-owned adapters, optional standardized pull APIs, optional
  event streams and the ARK data lake

- **Data sensitivity:** Internal, PII/pseudonymous customer identifiers,
  behavioral and transactional data, financial purchase values, campaign
  content and model outputs

- **Required response time:** Mixed—real-time or near-real-time for
  lightweight inference/chat and incremental events; asynchronous for
  ingestion, training, backfills, large predictions, campaign workflows
  and other durable operations

- **Deployment environment:** Unknown; architecture permits separate
  API, scheduler and capability-worker runtimes, potentially
  containerized/Kubernetes-based, but no environment has been finalized

- **Existing technologies and constraints:** Python/FastAPI-based
  capability code, PostgreSQL as the initial operational and job source
  of truth, object storage/data lake for large datasets and artifacts;
  existing code has Whatson/BCDP coupling, shared persistence and
  process-local scheduling that must be removed; team size, budget and
  deadline are unknown

- **Current architectural decisions:** Microservice-ready modular
  monolith; independent capability ownership;
  platform-neutral/adapterless core; versioned bounded contracts;
  push-first ingestion; immutable raw and curated data-lake datasets;
  separate dataset readiness and capability eligibility; one durable
  shared job manager; capability-specific workers; strict tenant
  isolation; shared PostgreSQL with module-owned schemas and one writer
  per table; object storage for large data; internal events and external
  webhooks; extraction into microservices only when justified

- **Open questions:** Tenant and traffic scale, latency SLOs,
  cloud/on-premises/Kubernetes choice, final broker and workflow
  technologies, detailed data-lake design and retention,
  identity-resolution model, whether ARK is formally positioned as a
  CDP, observability levels, exact proactive-permission semantics and
  which modules eventually require separate deployment \|

- **Current project stage:** Prototype and architecture-design stage,
  transitioning toward an MVP/platform skeleton

- **Anything else important:** Subscription, ingestion and execution are
  separate; every output must be traceable to tenant, contract, dataset,
  feature, model, code and execution versions; LAB is a testing platform
  rather than an ML capability; ARK must minimize unnecessary PII,
  enforce policy before action, and never execute proactive tasks
  outside an explicit tenant authorization.

**Working rules**

1.  Do not jump directly to a final diagram.

2.  First identify missing information that could materially change the
    architecture.

3.  Ask the questions in one organized batch, grouped by business, data,
    ML, integration, scale, security, operations, and team constraints.

4.  Distinguish:

    - known facts;

    - assumptions;

    - recommendations;

    - decisions still requiring confirmation.

5.  If I cannot answer a question, propose a reasonable temporary
    assumption and explain its architectural effect.

6.  Never invent scale, latency, security, or availability requirements.

7.  Prefer the simplest architecture that safely satisfies the actual
    requirements.

8.  Do not assume we need microservices, Kubernetes, Kafka, a service
    mesh, a feature store, a vector database, an agent framework, MCP,
    A2A, or real-time streaming. Recommend them only when justified.

9.  Do not assume every AI-powered component is an agent. For every
    proposed agent, prove that it needs autonomous planning, tool
    selection, dynamic execution, or multi-step reasoning. Otherwise,
    design it as a normal deterministic or ML service.

10. Treat ML services as independently owned capabilities, even if they
    initially share deployment infrastructure or a database.

11. Clearly distinguish synchronous requests, asynchronous jobs,
    scheduled jobs, batch processing, event-driven processing, and
    continuous/stream processing.

12. Separate current architecture from future possibilities.

13. For every major recommendation, provide:

    - the requirement it satisfies;

    - why it is needed now;

    - the simplest viable implementation;

    - at least one alternative;

    - why that alternative is not preferred;

    - the condition that would make us reconsider the decision.

14. Point out contradictions or dangerous assumptions instead of
    silently working around them.

15. Use specific designs, interfaces, data flows, and examples. Avoid
    generic textbook lists.

**Design process**

After requirements clarification, perform the design in the following
order.

**1. System definition**

Define:

- business goals;

- users and consuming systems;

- system boundary;

- responsibilities inside and outside the system;

- core use cases;

- out-of-scope capabilities;

- success criteria;

- functional requirements;

- non-functional requirements;

- constraints and assumptions.

Create a requirements traceability table connecting each important
requirement to the architectural element that satisfies it.

**2. Capability and service inventory**

Identify the business capabilities and proposed modules or services.

For every ML service or AI capability, provide a compact but complete
contract containing:

- name and purpose;

- business value;

- owner;

- input and output;

- input/output schemas;

- data requirements;

- invocation mode;

- synchronous or asynchronous behavior;

- expected latency;

- dependencies;

- preprocessing;

- model or algorithm;

- training requirements;

- inference workflow;

- state owned by the service;

- storage owned by the service;

- configuration and thresholds;

- model/version handling;

- eligibility or capability-readiness requirements;

- fallback behavior;

- failure modes;

- evaluation metrics;

- monitoring signals;

- security and privacy considerations.

Separate shared platform responsibilities from capability-specific
responsibilities.

**3. Architecture drivers and style**

Determine which architecture style fits the current situation:

- modular monolith;

- microservices;

- service-oriented architecture;

- event-driven architecture;

- data pipeline architecture;

- agentic architecture;

- or a justified combination.

Recommend one starting architecture.

Explain:

- why it fits the current scale, team, and maturity;

- the module and ownership boundaries;

- where coupling is acceptable;

- where isolation is mandatory;

- what should be shared;

- what must not be shared;

- what would trigger extraction into separate services.

Do not recommend microservices merely because there are multiple ML
capabilities.

**4. End-to-end architecture**

Design the complete path from consumer to result, considering only
components justified by requirements:

- consumer applications;

- consumer-specific adapters or anti-corruption layers;

- load balancer;

- API gateway;

- authentication and authorization;

- tenant identification;

- plans, entitlements, quotas, and rate limits;

- versioned capability APIs;

- workflow or orchestration API;

- data ingestion;

- schema and semantic validation;

- dataset catalog;

- data eligibility/capability-readiness checks;

- job manager;

- task queue and workers;

- scheduler;

- workflow orchestration;

- event producer and consumer handling;

- event broker, if justified;

- notification delivery;

- webhooks, polling, server-sent events, or other result-delivery
  mechanisms;

- configuration and policy management;

- service registry, only if needed;

- caching;

- operational databases;

- object storage or data lake;

- feature/state storage;

- model registry;

- secrets management;

- audit logging;

- observability;

- administration and operational interfaces.

For every proposed component, specify:

- responsibility;

- why it exists;

- whether it is required for the first version;

- inputs and outputs;

- state and data ownership;

- upstream and downstream dependencies;

- failure behavior;

- retry and idempotency requirements;

- scaling approach;

- security controls;

- monitoring signals;

- simplest implementation option.

If a commonly expected component is unnecessary, explicitly say so and
explain why.

**5. Data architecture**

Design:

- data source integration;

- push, pull, file upload, change-data-capture, batch, and streaming
  options;

- canonical data contracts;

- schema versioning;

- technical validation;

- semantic validation;

- tenant isolation;

- raw, validated, processed, feature, prediction, and audit data;

- storage ownership;

- retention and deletion;

- lineage and provenance;

- PII handling;

- encryption;

- data quality monitoring;

- backfills and reprocessing;

- duplicate and late-arriving data handling.

Explain the difference between:

- whether data is structurally valid;

- whether data is semantically valid;

- whether the valid data is sufficient for a particular ML capability.

Include an example data lifecycle.

**6. API and integration design**

Define:

- external APIs;

- internal module/service contracts;

- endpoint responsibilities;

- request and response examples;

- synchronous versus asynchronous API patterns;

- job submission and job-status APIs;

- pagination;

- idempotency keys;

- correlation IDs;

- error model;

- API versioning;

- rate limiting;

- timeout behavior;

- webhook/event contracts;

- authentication and authorization;

- tenant context propagation.

Explain whether consumers should use:

- one unified capability API;

- separate APIs per capability;

- a workflow API;

- or a combination.

Provide example API and event schemas, not merely endpoint names.

**7. Execution and orchestration**

Design how the system handles:

- immediate inference requests;

- long-running inference;

- training jobs;

- scheduled executions;

- batch executions;

- event-triggered executions;

- continuous processing, if justified;

- multi-service workflows;

- cancellation;

- retries;

- timeout;

- partial failure;

- compensation;

- job prioritization;

- concurrency limits;

- duplicate requests;

- exactly-once expectations versus practical at-least-once delivery.

Clearly distinguish the responsibilities of:

- API gateway;

- job manager;

- scheduler;

- queue;

- worker;

- workflow orchestrator;

- event broker;

- event handler;

- notification delivery component.

Do not collapse these into a vague “event system.”

**8. Event and proactive-action architecture**

If ML services can independently discover recommendations, churn risks,
alerts, or suggested actions, design:

- what causes the evaluation to run;

- how tenants configure schedules, permissions, thresholds, and
  channels;

- how an output becomes a domain event or actionable insight;

- event schema;

- event versioning;

- routing;

- subscription management;

- webhook or other delivery methods;

- retries and exponential backoff;

- dead-letter handling;

- deduplication;

- ordering;

- expiration;

- throttling;

- acknowledgement;

- replay;

- audit history.

Clarify the difference between:

- internal technical events;

- business/domain events;

- commands;

- notifications;

- actionable ML insights.

**9. ML and MLOps architecture**

Design:

- experiment tracking;

- dataset versioning;

- feature definitions;

- training pipeline;

- model evaluation;

- approval or promotion;

- model registry;

- deployment strategy;

- online and batch inference;

- model loading;

- model version selection;

- shadow and canary deployment;

- rollback;

- drift detection;

- data-quality monitoring;

- performance monitoring;

- feedback collection;

- retraining triggers;

- explainability;

- reproducibility;

- fairness and safety where applicable.

Decide whether a full feature store is justified. If not, explain how to
preserve feature definitions, versioning, point-in-time correctness, and
training-serving consistency without one.

**10. Agent architecture, only if justified**

For every proposed agent, define:

- goal;

- reason it must be an agent;

- tools it can use;

- available context;

- memory and state;

- planning boundaries;

- permissions;

- human approval points;

- termination criteria;

- maximum steps, time, and cost;

- output contract;

- evaluation;

- observability;

- failure and fallback behavior;

- prompt-injection and data-exfiltration controls.

Explain whether REST, gRPC, events, MCP, A2A, or another interface is
appropriate. Do not introduce MCP or A2A unless an actual agent-to-tool
or agent-to-agent requirement exists.

**11. Security, privacy, and governance**

Include:

- tenant isolation;

- identity and access management;

- service-to-service authentication;

- least privilege;

- secrets handling;

- encryption in transit and at rest;

- PII protection;

- data residency;

- auditability;

- consent and permission handling;

- retention and deletion;

- model access controls;

- prompt and tool security for agents;

- abuse prevention;

- dependency and supply-chain risks.

Create a concise threat model covering the most realistic risks.

**12. Reliability and failure design**

For each critical path, analyze:

- unavailable dependencies;

- invalid or incomplete datasets;

- queue backlog;

- worker crash;

- duplicate execution;

- partial workflow completion;

- stale cache;

- storage outage;

- model unavailable;

- event delivery failure;

- tenant misconfiguration;

- poisonous messages;

- schema incompatibility;

- agent loops or unsafe actions.

Specify:

- timeout;

- retry;

- circuit breaker;

- idempotency;

- dead-letter handling;

- graceful degradation;

- fallback;

- recovery;

- reconciliation;

- disaster recovery.

Do not add every reliability pattern everywhere. Apply each only where
its benefit exceeds its complexity.

**13. Observability and evaluation**

Design:

- structured logs;

- metrics;

- traces;

- correlation across APIs, jobs, models, and events;

- health checks;

- dashboards;

- alerts;

- audit logs;

- per-tenant usage;

- model-quality metrics;

- data-quality metrics;

- cost metrics;

- agent execution traces, if applicable.

Specify the key service-level indicators and propose realistic
service-level objectives only where enough information exists.

**14. Deployment and infrastructure**

Recommend the simplest adequate deployment model.

Cover:

- environments;

- configuration;

- containers;

- CI/CD;

- database migrations;

- model deployment;

- infrastructure as code;

- secrets;

- scaling;

- backups;

- rollback;

- release strategies;

- development and testing environments.

Do not automatically recommend Kubernetes. Compare it with a simpler
deployment approach based on the actual requirements.

**15. Testing strategy**

Include:

- unit tests;

- contract tests;

- integration tests;

- end-to-end tests;

- data-quality tests;

- model evaluation tests;

- event-delivery tests;

- load tests;

- resilience tests;

- security tests;

- tenant-isolation tests;

- agent evaluations, if applicable.

Identify the highest-risk scenarios that must be tested before
production.

**16. Capacity, performance, and cost**

Build an initial capacity model using known facts and clearly labeled
assumptions:

- tenants;

- requests;

- data volume;

- batch sizes;

- concurrent jobs;

- event volume;

- storage growth;

- model memory;

- CPU/GPU requirements;

- latency;

- cost drivers.

Identify what must be measured before making final infrastructure
decisions.

**17. Architecture decisions**

Create an Architecture Decision Record table containing:

- decision;

- context;

- chosen option;

- alternatives;

- reason;

- trade-offs;

- risks;

- status;

- reconsideration trigger.

Pay special attention to:

- modular monolith versus microservices;

- shared versus separate databases;

- push versus pull ingestion;

- synchronous versus asynchronous processing;

- queue versus event broker;

- scheduled versus event-driven execution;

- REST versus gRPC;

- build versus buy;

- rules/ML service versus AI agent;

- basic feature management versus feature store.

**18. Diagrams**

Produce clear Mermaid diagrams for:

1.  system context;

2.  logical container/component architecture;

3.  one synchronous request flow;

4.  one asynchronous job flow;

5.  one proactive ML event-delivery flow;

6.  data lifecycle;

7.  deployment architecture.

Keep diagrams readable and consistent. Do not place every minor
implementation detail in one diagram.

**19. Implementation roadmap**

Divide implementation into:

- walking skeleton/proof of architecture;

- MVP;

- production hardening;

- scale-driven improvements;

- optional future capabilities.

For every phase specify:

- scope;

- tasks;

- deliverables;

- dependencies;

- acceptance criteria;

- major risks;

- what must deliberately be postponed.

The walking skeleton must prove one realistic request through the most
important boundaries, even if some internal implementations are
temporary.

**20. Final deliverables**

End with:

1.  recommended starting architecture;

2.  minimal component list for the first version;

3.  components explicitly postponed;

4.  top ten unresolved questions;

5.  top ten risks;

6.  first implementation milestone;

7.  decisions that must be made now;

8.  decisions that can safely wait;

9.  an architecture completeness checklist;

10. a short executive summary suitable for non-technical stakeholders.

**Runtime placement and execution-flow analysis**

For every architecturally significant component, module, function,
workflow step, and design pattern, do not merely define what it is. Also
explain exactly **when, where, and why it participates in the system**.

**1. Usage and placement**

For each design element, specify:

- the stages or workflows in which it is used;

- the exact trigger that activates it;

- the conditions or prerequisites for its execution;

- who or what invokes it;

- whether it runs for every request or only under specific conditions;

- why it is placed at that particular stage;

- what requirement it satisfies there;

- why it is not needed in other stages;

- what would happen if it were removed, moved, delayed, or replaced;

- whether it belongs to the critical execution path or is a supporting
  function.

Use concrete explanations such as:

- “The event broker is used after a long-running job produces a business
  result because downstream consumers should receive the result without
  blocking the worker.”

- “A webhook is used during external result delivery because the
  consuming platform cannot maintain a permanent connection and needs
  asynchronous notification.”

- “The capability-readiness check runs after dataset validation but
  before job creation because structurally valid data may still be
  insufficient for the requested ML capability.”

Do not describe components as universally active when they are only
required in particular workflows.

**2. Execution order and dependency analysis**

For every important end-to-end workflow, show the exact execution order.

Classify each step as one of the following:

- sequential and blocking;

- sequential but asynchronous;

- parallel and blocking at a synchronization point;

- parallel and non-blocking;

- event-triggered;

- scheduled;

- conditional;

- background or out-of-band.

Explain why each step must run serially or can safely run concurrently.

For each dependency, specify:

- what data or state must exist before the next step can begin;

- which steps are independent and can run in parallel;

- which steps must wait for multiple preceding steps;

- synchronization or fan-in points;

- whether ordering must be guaranteed;

- concurrency limits;

- race-condition risks;

- consistency requirements;

- timeout and cancellation behavior;

- how failures affect parallel and downstream branches;

- whether retries repeat one step or the entire workflow.

Do not recommend parallel execution merely because it is faster. Confirm
that the steps do not have ordering, shared-state, transactional,
resource, or consistency dependencies.

**3. Critical path versus supporting path**

For each workflow, clearly separate:

- critical-path operations required before returning or committing a
  result;

- background operations that may continue after the response;

- operational side effects;

- monitoring and observability;

- audit and compliance operations;

- notification and event-delivery operations.

Treat observability precisely:

- trace-context creation and essential instrumentation may occur inline
  with the request;

- log, metric, and trace export should normally be buffered and
  processed asynchronously;

- observability failure should normally not fail the business operation;

- mandatory security or compliance audit records may require stronger
  synchronous or transactional guarantees.

Explain these decisions rather than simply saying that “observability
runs in parallel.”

**4. Required execution artifacts**

For every major use case, produce:

**A. Stage usage table**

Include:

- stage;

- component/module/function used;

- trigger;

- reason it is used at this stage;

- prerequisites;

- input;

- output;

- execution mode;

- blocking or non-blocking;

- failure effect;

- next step.

**B. Execution dependency table**

Include:

- operation;

- depends on;

- can run in parallel with;

- synchronization requirement;

- ordering requirement;

- critical-path status;

- retry boundary.

**C. Step-by-step runtime narrative**

Describe the execution from the original trigger to the final result,
including conditional branches, background work, failures, retries, and
result delivery.

**D. Mermaid execution diagram**

Create a sequence diagram or flowchart that visibly distinguishes:

- sequential operations;

- parallel branches;

- asynchronous work;

- events;

- conditional branches;

- synchronization points;

- background operations;

- the final response or delivered result.

At minimum, perform this analysis for:

1.  synchronous inference;

2.  asynchronous inference or batch job;

3.  scheduled ML execution;

4.  event-triggered execution;

5.  proactive insight and webhook delivery;

6.  model training and deployment;

7.  a multi-capability workflow;

8.  an agentic workflow, if agents are justified.

Apply function-level analysis only to architecturally important
functions and workflow operations. Do not document every internal helper
function unless it affects system boundaries, ordering, state,
reliability, security, performance, or scaling.

**Anti-overengineering test**

Before finalizing the design, inspect every proposed component and ask:

- What concrete requirement justifies this?

- Is it needed now?

- Can the same outcome be achieved more simply?

- What operational burden does it add?

- Does the current team have the capacity to own it?

- What measurable condition would justify adding it later?

Classify every component as:

- required now;

- useful soon;

- scale-triggered;

- optional;

- unjustified.

If the first version contains a large number of independently deployed
services or infrastructure products, treat that as a warning and
re-evaluate the design.

The final result must be detailed enough that an engineering team could
begin implementation, but it must not pretend that unknown requirements
have already been decided.
