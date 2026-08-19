# ML SERVICE CARD
===============

**Service name:** Campaign Verifier  
**Service ID/version:** `AgentController_callCampaignVerifierAgent_v1` / API `1.0.0`  
**Owner:**

## INFRASTRUCTURE CLASSIFICATION

1. **Request-driven or proactive?**  
   Request-driven through an authenticated HTTP request. No proactive campaign-monitoring process is defined.

2. **Stateless or stateful?**  
   The API contract can operate statelessly because the complete payload, references, configuration, and metadata are supplied in each request. Server-side persistence is not described.

3. **Synchronous or asynchronous?**  
   Synchronous request/response. No job ID, callback, or polling contract is defined.

4. **Online or batch-oriented?**  
   Online/request-oriented. A request can contain multiple references, configuration entries, and metadata entries, but it represents one verification operation.

5. **Raw data or derived data?**  
   Consumes caller-supplied opaque payload data, reference data and tags, agent configuration, and metadata. No required server-side dataset is declared.

# 1. PURPOSE

- Verify a campaign or campaign-related payload using an LLM.
- Evaluate the supplied payload against references, tags, agent configuration, settings, and metadata.
- Return one of:
  - `accepted`
  - `rejected`
  - `failed`
- Return a description, error string, and token-usage cost.
- The intended consumer is the platform or campaign workflow requesting a verification decision.

# 2. TRIGGER / EXECUTION MODE

- **Mode:** authenticated HTTP API.
- **Endpoint:** `POST /dev/v1/agent/campaign-verifier`
- **Content type:** `application/json`
- **Execution:** synchronous request/response.
- **Can initiate work proactively?** No proactive trigger is defined.
- **Authentication:** API key in the `authorization` header.

# 3. INPUT CONTRACT

## Required inputs

The request must contain all four top-level fields:

- `payload: CampaignVerifierPayloadDto`
- `references: CampaignVerifierReferenceDto[]`
- `config: CampaignVerifierConfigDto[]`
- `metadata: CampaignVerifierMetadataItemDto[]`

No minimum array lengths are declared.

## Payload schema

```json
{
  "data": {}
}
```

- `data: object` is required.
- Internal properties are not defined.

## Reference schema

Each `references` entry requires:

```json
{
  "data": {},
  "tags": ["string"]
}
```

- `data: object`
- `tags: string[]`

No tag enumeration or minimum tag count is defined.

## Configuration schema

Each `config` entry requires:

```json
{
  "agent": "string",
  "settings": {}
}
```

- `agent: string`
- `settings: object`

Allowed agent names and the internal settings schema are not defined.

## Metadata schema

Each `metadata` entry contains:

```json
{
  "tag": "string",
  "value": {}
}
```

- `tag: string` is required.
- `value: object` is optional.
- Allowed metadata tags and value schemas are not defined.

## Optional inputs

- `value` inside each metadata entry.

## Required datasets

## Minimum data requirements

- All four top-level request fields must be present.
- `payload.data` must be present.
- Every reference must contain `data` and `tags`.
- Every configuration entry must contain `agent` and `settings`.
- Every metadata entry must contain `tag`.

## Input schema/version

- Schema: `CampaignVerifierRequestDto`
- API path version: `v1`
- OpenAPI service version: `1.0.0`

# 4. OUTPUT CONTRACT

## Primary output

A campaign-verification decision conforming to `CampaignVerifierResponseDto`.

## Output schema

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `cost` | number | Yes | LLM request cost |
| `status` | string enum | Yes | Verification outcome |
| `description` | string | Yes | Description of the verification result |
| `error` | string | Yes | Error information |

Allowed `status` values:

- `accepted`
- `rejected`
- `failed`

The `error` field is required even for accepted/rejected responses; the Swagger does not define whether it should be an empty string when no error exists.

## Scores/confidence

## Possible statuses

- `accepted`
- `rejected`
- `failed`

The generic statuses `SUCCESS`, `PARTIAL`, `FAILED`, and `NOT_ELIGIBLE` are not defined as a separate service/job envelope.

## HTTP responses

- `200`: campaign verifier agent response.
- `400`: validation error.
  - Error response body schema is not defined.

# 5. HIGH-LEVEL WORKFLOW

```text
CampaignVerifierRequestDto
  ↓
API authentication and request validation
  ↓
LLM campaign verification
  ↓
accepted / rejected / failed
  ↓
CampaignVerifierResponseDto
```

# 6. ELIGIBILITY / PRECONDITIONS

- Valid API authentication.
- All required request structures must be supplied.
- Entries in `references`, `config`, and `metadata` must satisfy their schemas.

- Minimum references:
- Minimum configuration entries:
- Minimum metadata entries:
- Required agent values:
- Tenant entitlement/configuration:
- Campaign eligibility rules:

# 7. DEPENDENCIES

## Internal

## External

- LLM service/model.

## Data

## Model/artifact

# 8. STATE & STORAGE

## Reads

## Writes

## Persistent state

## Cache

## Intermediate artifacts

# 9. EXECUTION PROFILE

**Typical runtime:**  
**Expected dataset size:** One payload plus arrays of references, configuration entries, and metadata  
**CPU:**  
**RAM:**  
**GPU:**  
**Parallelizable?:**  
**Timeout considerations:**

# 10. CONFIGURATION

## Request-level configuration

- `config[].agent`
- `config[].settings`

## Service-level configuration

**Decision thresholds:**  
**Required references:**  
**Verification policy version:**  
**LLM provider:**  
**LLM model/version:**  
**Temperature:**  
**Maximum output tokens:**  
**Prompt version:**  
**Schedule:**  
**Tenant-specific parameters:**

# 11. FAILURE / FALLBACK

## Possible failures

- Request validation failure: HTTP `400`.
- A completed HTTP `200` response may contain `status: "failed"`.

**Retryable?:**  
**Fallback:**  
**Partial-result behavior:**

No structured error response is defined for HTTP `400`. For HTTP `200`, failure information is returned through the required `status`, `description`, and `error` fields.

# 12. INTEGRATION

**API:** `POST /dev/v1/agent/campaign-verifier`  
**Authentication:** API key in `authorization` header  
**Request schema:** `CampaignVerifierRequestDto`  
**Response schema:** `CampaignVerifierResponseDto`  
**Events emitted:**  
**Events consumed:**  
**Job type:**  
**Result retrieval:** Immediate HTTP response  
**Idempotency:**  
**Versioning:** `/v1`; OpenAPI service version `1.0.0`

# 13. OBSERVABILITY

## Operational metrics

## Data metrics

## LLM metrics

- Per-request cost is returned in `cost`.
- Verification outcome is returned in `status`.

# 14. OWNERSHIP / ISOLATION

## Owns

- Campaign-verification request and response contract.
- Verification outcome and description.

## May access

## Must NOT directly access