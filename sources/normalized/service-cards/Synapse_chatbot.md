
# ML SERVICE CARD
===============

**Service name:** Chatbot  
**Service ID/version:** `AgentController_callChatbotAgent_v1` / API `1.0.0`  
**Owner:**

## INFRASTRUCTURE CLASSIFICATION

1. **Request-driven or proactive?**  
   Request-driven through an authenticated HTTP request. No proactive execution or event emission is defined.

2. **Stateless or stateful?**  
   The API contract can operate statelessly because the caller supplies conversation history on every request. Server-side session or conversation persistence is not described.

3. **Synchronous or asynchronous?**  
   Synchronous request/response API. No job ID, callback, polling, or asynchronous result contract is defined.

4. **Online or batch-oriented?**  
   Online, one conversational request at a time.

5. **Raw data or derived data?**  
   Consumes caller-supplied query text, message history, and optional customer context. No required server-side dataset is declared.

# 1. PURPOSE

- Provide an LLM-generated chatbot response to a customer query.
- Accept conversation history and optional customer/business context.
- Return generated text, request cost, the caller’s reference ID, and metadata.
- The result is intended for the calling customer-facing channel or platform.

# 2. TRIGGER / EXECUTION MODE

- **Mode:** authenticated HTTP API.
- **Endpoint:** `POST /dev/v1/agent/chatbot`
- **Content type:** `application/json`
- **Execution:** synchronous request/response.
- **Can initiate work proactively?** No proactive trigger is defined.
- **Authentication:** API key in the `authorization` header.
- The Swagger does not specify whether the header contains a raw key, bearer token, or another format.

# 3. INPUT CONTRACT

## API inputs

### Required inputs

- `query: string`
  - Customer query sent to the agent.
- `businessId: number`
  - Business identifier.
- `customerId: number`
  - Customer identifier.
- `history: MessageDto[]`
  - Required array; no minimum item count is specified.
  - Each message requires:
    - `source: "customer" | "agent"`
    - `content: string`
- `referenceId: number`
  - Request reference returned unchanged in the response.

### Optional inputs

- `channel: string`
  - Allowed values:
    - `sms`
    - `social-media`
    - `push`
  - Default: `social-media`
- `metadata: ChatbotMetadataDto`
  - All metadata properties are optional:
    - `address: string`
    - `phone: string`
    - `viewedProducts: MetadataProductDto[]`
      - Each product requires:
        - `id: string`
        - `title: string`
    - `basket: MetadataBasketDto[]`
      - Each basket item requires:
        - `id: string`
        - `title: string`
        - `quantity: number`, minimum `1`

## Required datasets

## Minimum data requirements

- All required request properties must be present.
- Each history entry must contain a valid `source` and `content`.
- Basket quantities, when supplied, must be at least `1`.
- `channel`, when supplied, must match the declared enumeration.

## Input schema/version

- Schema: `CallChatbotAgentDto`
- API path version: `v1`
- OpenAPI service version: `1.0.0`

# 4. OUTPUT CONTRACT

## Primary output

A JSON object conforming to `CallChatbotAgentResponseDto`.

## Output schema

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `cost` | number | Yes | Token-usage cost summed across all LLM calls in the request, in dollars |
| `referenceId` | number | Yes | Reference ID associated with the request |
| `response` | string | Yes | Generated chatbot response |
| `metadata` | object | Yes | Chatbot metadata using `ChatbotMetadataDto` |

The response metadata object can contain:

- `address: string`
- `phone: string`
- `viewedProducts: [{id, title}]`
- `basket: [{id, title, quantity}]`

No properties inside `metadata` are individually required, although the metadata object itself is required in the response.

## Scores/confidence

## Possible statuses

## HTTP responses

- `200`: chatbot agent response.
- `400`: validation error.
  - Error response body schema is not defined.

# 5. HIGH-LEVEL WORKFLOW

```text
CallChatbotAgentDto
  ↓
API authentication and request validation
  ↓
LLM chatbot processing
  ↓
CallChatbotAgentResponseDto
```

# 6. ELIGIBILITY / PRECONDITIONS

- Valid API authentication.
- Required request fields must be present.
- Enumerated values and numeric minimums must be valid.

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
**Expected dataset size:** One query and one conversation-history array per request  
**CPU:**  
**RAM:**  
**GPU:**  
**Parallelizable?:**  
**Timeout considerations:**

# 10. CONFIGURATION

- Default channel: `social-media`
- Supported channels:
  - `sms`
  - `social-media`
  - `push`
- LLM provider:
- LLM model/version:
- Temperature:
- Maximum output tokens:
- System prompt/version:
- Context-window limit:
- Conversation-history limit:
- Tenant-specific parameters:

# 11. FAILURE / FALLBACK

## Possible failures

- Request validation failure: HTTP `400`.

**Retryable?:**  
**Fallback:**  
**Partial-result behavior:**

# 12. INTEGRATION

**API:** `POST /dev/v1/agent/chatbot`  
**Authentication:** API key in `authorization` header  
**Request schema:** `CallChatbotAgentDto`  
**Response schema:** `CallChatbotAgentResponseDto`  
**Events emitted:**  
**Events consumed:**  
**Job type:**  
**Result retrieval:** Immediate HTTP response  
**Idempotency:**  
**Versioning:** `/v1`; OpenAPI service version `1.0.0`

`referenceId` is echoed by the response, but the Swagger does not define it as an idempotency key.

# 13. OBSERVABILITY

## Operational metrics

## Data metrics

## LLM metrics

- Per-request LLM cost is exposed in the response as `cost`.

# 14. OWNERSHIP / ISOLATION

## Owns

- Chatbot request and response API contract.
- Generated chatbot response.

## May access

## Must NOT directly access

---