# ARK account, organization, and business function contract

## 1. Function notation

Every function follows this abstract contract:

`function_name(RequestContext, FunctionInput) -> OperationResult<FunctionOutput>`

these are **boundary contracts** that define how every module communicates safely.

### 1.1 RequestContext
"Who is calling, under what authority, and in what scope?"\
```text
someone calls : reserve_credits( RequestContext, ReservationRequest)
Now the reservation service does not ask: "Who are you?" The context(RequestContext) already answers.
```

| Field | Type | Required | Contract                                                                              |
|---|---|---:|---------------------------------------------------------------------------------------|
| `request_id` | `RequestId` | Yes | Unique correlation ID for one request <br/> used by tracing,logs, audit and debugging |
| `idempotency_key` | `IdempotencyKey` | Mutations | Same key plus same fingerprint returns the original result                            |
| `actor_type` | `USER \| API_KEY \| SYSTEM \| ANONYMOUS` | Yes | Trusted actor class                                                                   |
| `actor_id` | `ActorId` | Except anonymous | Stable actor identifier                                                               |
| `member_id` | `MemberId?` | Organization-scoped calls | Active Member used for authorization                                                  |
| `organization_id` | `OrganizationId?` | Organization-scoped calls | Derived Organization scope                                                            |
| `business_id` | `BusinessId?` | Business-scoped calls | Derived Business tenant scope                                                         |
| `role_id` | `RoleId?` | Member calls | Selected Role snapshot                                                                |
| `role_version` | `Version?` | Member calls | Role version used for the decision                                                    |
| `authenticated_at` | `Instant?` | Authenticated calls | Time authentication was established                                                   |

Application callers MUST NOT construct trusted actor fields themselves. An edge
adapter or trusted internal scheduler creates this context. (the client is not allowed to tell ARK who they are.)
Instead, the client sends its authentication proof (APIKEY)

### 1.2 OperationResult
"What happened as a result of this operation?"\

| Field | Type | Required | Contract |
|---|---|---:|---|
| `request_id` | `RequestId` | Yes | Echoes the request correlation ID |
| `data` | Operation output | On success | Exact output defined by the function |
| `audit_event_id` | `AuditEventId?` | Mutations | Audit event associated with the effect |
| `resource_version` | `Version?` | Resource mutation | Version after the effect |
| `replayed` | `boolean` | Yes | True when returned from a matching idempotent replay |
| `error` | `ContractError?` | On failure | Structured failure; no partial success is hidden |

### 3.3 ContractError

| Field | Type | Required | Contract |
|---|---|---:|---|
| `code` | `ErrorCode` | Yes | Stable machine-readable code |
| `message` | `string` | Yes | Safe human-readable summary |
| `field_errors` | `map<string,string>` | No | Input validation details |
| `current_version` | `Version` | Version conflict | Current resource version |
| `retryable` | `boolean` | Yes | Whether an unchanged retry can succeed |
| `request_id` | `RequestId` | Yes | Correlation ID |

Errors MUST NOT disclose raw keys, tokens, verification codes, hashes, User
existence during login, or resources outside the actor's authorized scope.

### 3.4 Shared scalar types

| Type | Meaning |
|---|---|
| `Instant` | UTC timestamp with timezone |
| `Version` | Positive optimistic-concurrency version |
| `PageSize` | Integer from 1 through 100 |
| `PageToken` | Opaque continuation token |
| `Status` | Resource-specific lifecycle status |
| `SecretOnce` | Sensitive value returned once and never retrievable |



## 11. Audit read functions

Audit writes are internal mandatory effects of mutation functions. Developers
MUST NOT expose a general client-callable `add_audit_event` function.

### 11.1 `list_audit_events`

Signature: `list_audit_events(RequestContext, ListAuditEventsInput) -> OperationResult<ListAuditEventsOutput>`

Authorization: `audit.read` in the Organization.

Input: `organization_id`, optional `business_id`, optional `member_id`, optional
`actor_type`, optional `action`, optional `target_type`, optional `target_id`,
optional `occurred_from`, optional `occurred_to`, `page_size`, and `page_token`.

Output: `events: Page<AuditEventView>`.

Errors: `ORGANIZATION_NOT_FOUND`, `FORBIDDEN`, `INVALID_PAGE_TOKEN`,
`VALIDATION_FAILED`.

### 11.2 `get_audit_event`

Signature: `get_audit_event(RequestContext, GetAuditEventInput) -> OperationResult<GetAuditEventOutput>`

Authorization: `audit.read` in the event's Organization.

Input: `organization_id`, `audit_event_id`.

Output: `event: AuditEventView` with secrets and restricted fields redacted.

Errors: `AUDIT_EVENT_NOT_FOUND`, `FORBIDDEN`.


## 14. Audit requirements

Every mutation records at least:

| Field | Contract |
|---|---|
| `actor_type`, `actor_id` | Trusted actor identity |
| `organization_id`, `member_id`, `business_id` | Applicable derived scope |
| `action` | Stable function/effect code |
| `target_type`, `target_id` | Mutated resource |
| `result` | `SUCCESS`, `ACCEPTED`, `DENIED`, or `FAILED` |
| `request_id` | Correlation ID |
| `before_version`, `after_version` | Mutation lineage when applicable |
| `reason` | Required lifecycle/privileged-action reason |
| `occurred_at` | Server timestamp |

Raw secrets, hashes, authentication assertions, verification codes, tokens, and
unredacted sensitive profile values MUST NOT enter audit details.

## 15. Stable error-code catalog

| Category | Codes |
|---|---|
| Validation | `VALIDATION_FAILED`, `INVALID_PAGE_TOKEN`, `INVALID_STATE_TRANSITION` |
| Authentication | `AUTHENTICATION_FAILED`, `SESSION_NOT_FOUND`, `SESSION_EXPIRED`, `SESSION_REVOKED`, `VERIFICATION_REQUIRED` |
| Verification | `CHALLENGE_NOT_FOUND`, `CHALLENGE_EXPIRED`, `CHALLENGE_CONSUMED`, `VERIFICATION_FAILED`, `CHANNEL_NOT_SUPPORTED`, `DELIVERY_UNAVAILABLE` |
| Authorization | `FORBIDDEN`, `LAST_ORGANIZATION_OWNER` |
| User | `USER_NOT_FOUND`, `USER_NOT_ACTIVE`, `USER_ALREADY_EXISTS` |
| Organization | `ORGANIZATION_NOT_FOUND`, `ORGANIZATION_NOT_ACTIVE`, `ORGANIZATION_NOT_CLOSABLE` |
| Member | `MEMBER_NOT_FOUND`, `MEMBER_NOT_ACTIVE`, `MEMBER_ALREADY_EXISTS` |
| API key | `API_KEY_NOT_FOUND`, `API_KEY_STATE_CONFLICT`, `SECRET_ALREADY_DELIVERED` |
| Authorization catalog | `ROLE_NOT_FOUND`, `ROLE_NOT_ACTIVE`, `PERMISSION_NOT_FOUND` |
| Capability pattern | `CAPABILITY_NOT_FOUND`, `CAPABILITY_PATTERN_NOT_FOUND` |
| Business | `BUSINESS_NOT_FOUND`, `BUSINESS_NOT_ACTIVE`, `BUSINESS_TYPE_NOT_FOUND`, `EXTERNAL_REF_CONFLICT` |
| Concurrency | `VERSION_CONFLICT`, `IDEMPOTENCY_CONFLICT` |
| Operations | `RATE_LIMITED`, `IN_FLIGHT_WORK_EXISTS`, `AUDIT_UNAVAILABLE`, `TRUST_PROFILE_UNAVAILABLE` |
