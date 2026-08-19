# ARK entities

The current identity and access entities are `Users`, `Organizations`, `Roles`,
`Permissions`, `Members`, and `APIKeys`. `AuditEvents` records immutable security
and business effects.

## What happens during an API-key request?

1. Read the non-secret API-key prefix and secret from the request.
2. Find the API-key record by its unique prefix.
3. Verify the secret against `key_hash` using a constant-time comparison.
4. Reject a revoked, expired, or inactive API key.
5. Load the API key's Member and reject a suspended or revoked membership.
6. Verify that the Member and API key belong to the same active Organization.
7. Resolve the Member's one predefined Role and its predefined Permissions.
8. For a business operation, verify that the Business belongs to the Organization.
9. Build a trusted request context; request fields never create organization or business authority.
10. Append the required audit event before any high-impact effect.

## IAM schema

IAM owns Users, the system-managed Role/Permission catalog, and API-key hashes.
The Organizations schema owns Organizations, Members, and Businesses. Each Member
has exactly one Role and may have multiple API keys.

```sql
CREATE SCHEMA IF NOT EXISTS iam;
CREATE SCHEMA IF NOT EXISTS organizations;
CREATE SCHEMA IF NOT EXISTS audit;
```

### `users`

`users.id` is the stable identifier for a human user. ARK does not store raw
passwords in this table. The approved human sign-in trust mechanism remains a
separate deployment/security decision.

```sql
CREATE TABLE iam.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(200) NOT NULL,
    phone VARCHAR(16),
    phone_verified_at TIMESTAMPTZ,
    email VARCHAR(320),
    email_verified_at TIMESTAMPTZ,
    city_id CHAR(2),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_users_name
        CHECK (LENGTH(BTRIM(full_name)) > 0),

    CONSTRAINT chk_users_phone_e164
        CHECK (
            phone IS NULL
            OR phone ~ '^\+[1-9][0-9]{7,14}$'
        ),

    CONSTRAINT chk_users_phone_verification
        CHECK (
            phone_verified_at IS NULL
            OR phone IS NOT NULL
        ),

    CONSTRAINT chk_users_email_verification
        CHECK (
            email_verified_at IS NULL
            OR email IS NOT NULL
        ),

    CONSTRAINT chk_users_status
        CHECK (status IN ('ACTIVE', 'SUSPENDED', 'CLOSED'))
);
```

### `roles`, `permissions`, and `role_permissions`

Roles and Permissions are defined and versioned by ARK developers. Organization
owners may select an active Role for a Member, but cannot create Roles, change
Permissions, or edit Role-to-Permission mappings. A new permission set creates a
new Role version; it does not silently change the meaning of a Role already
referenced by a Member.

```sql
CREATE TABLE iam.roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_code VARCHAR(100) NOT NULL,
    name VARCHAR(200) NOT NULL,
    version BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    retired_at TIMESTAMPTZ,

    CONSTRAINT uq_roles_code_version
        UNIQUE (role_code, version),

    CONSTRAINT chk_roles_code
        CHECK (role_code ~ '^[A-Z][A-Z0-9_]{1,99}$'),

    CONSTRAINT chk_roles_name
        CHECK (LENGTH(BTRIM(name)) > 0),

    CONSTRAINT chk_roles_version
        CHECK (version >= 1),

    CONSTRAINT chk_roles_status
        CHECK (status IN ('ACTIVE', 'RETIRED')),

    CONSTRAINT chk_roles_retirement
        CHECK (
            (status = 'ACTIVE' AND retired_at IS NULL)
            OR (status = 'RETIRED' AND retired_at IS NOT NULL)
        )
);

CREATE UNIQUE INDEX uq_roles_one_active_version
    ON iam.roles (role_code)
    WHERE status = 'ACTIVE';

CREATE TABLE iam.permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    permission_code VARCHAR(150) NOT NULL,
    description VARCHAR(500) NOT NULL,
    version BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    retired_at TIMESTAMPTZ,

    CONSTRAINT uq_permissions_code_version
        UNIQUE (permission_code, version),

    CONSTRAINT chk_permissions_code
        CHECK (permission_code ~ '^[a-z][a-z0-9_.]{1,149}$'),

    CONSTRAINT chk_permissions_description
        CHECK (LENGTH(BTRIM(description)) > 0),

    CONSTRAINT chk_permissions_version
        CHECK (version >= 1),

    CONSTRAINT chk_permissions_status
        CHECK (status IN ('ACTIVE', 'RETIRED')),

    CONSTRAINT chk_permissions_retirement
        CHECK (
            (status = 'ACTIVE' AND retired_at IS NULL)
            OR (status = 'RETIRED' AND retired_at IS NOT NULL)
        )
);

CREATE UNIQUE INDEX uq_permissions_one_active_version
    ON iam.permissions (permission_code)
    WHERE status = 'ACTIVE';

CREATE TABLE iam.role_permissions (
    role_id UUID NOT NULL,
    permission_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (role_id, permission_id),

    CONSTRAINT fk_role_permissions_role
        FOREIGN KEY (role_id)
        REFERENCES iam.roles (id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_role_permissions_permission
        FOREIGN KEY (permission_id)
        REFERENCES iam.permissions (id)
        ON DELETE RESTRICT
);
```

Example predefined Role:

```text
DATA_INGESTOR
├── source.register
├── upload.create
├── upload.commit
├── ingestion.submit
└── ingestion.status.read
```

A Role grants permission to attempt an operation. It does not enable a capability;
organization pattern, business state, entitlement, quota, and production-admission
checks remain separate.

### `organizations`

```sql
CREATE TABLE organizations.organizations (
    organization_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_by_user_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version BIGINT NOT NULL DEFAULT 1,

    CONSTRAINT fk_organizations_created_by_user
        FOREIGN KEY (created_by_user_id)
        REFERENCES iam.users (id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_organizations_name
        CHECK (LENGTH(BTRIM(name)) > 0),

    CONSTRAINT chk_organizations_status
        CHECK (status IN ('ACTIVE', 'SUSPENDED', 'CLOSED')),

    CONSTRAINT chk_organizations_version
        CHECK (version >= 1),

    CONSTRAINT uq_organizations_id
        UNIQUE (organization_id)
);
```

### `members`

A Member connects one User to one Organization and carries exactly one Role.
The same User may have Member records in multiple Organizations, but may have
only one Member record in a given Organization. The composite
`UNIQUE (user_id, organization_id)` constraint enforces that boundary.

```sql
CREATE TABLE organizations.members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    organization_id UUID NOT NULL,
    role_id UUID NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    suspended_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ,
    row_version BIGINT NOT NULL DEFAULT 1,

    CONSTRAINT fk_members_user
        FOREIGN KEY (user_id)
        REFERENCES iam.users (id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_members_organization
        FOREIGN KEY (organization_id)
        REFERENCES organizations.organizations (organization_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_members_role
        FOREIGN KEY (role_id)
        REFERENCES iam.roles (id)
        ON DELETE RESTRICT,

    -- A User can join many Organizations, but only once per Organization.
    CONSTRAINT uq_members_user_organization
        UNIQUE (user_id, organization_id),

    -- Supports organization-safe composite references from API keys and audit.
    CONSTRAINT uq_members_id_organization
        UNIQUE (id, organization_id),

    CONSTRAINT chk_members_status
        CHECK (status IN ('ACTIVE', 'SUSPENDED', 'REVOKED')),

    CONSTRAINT chk_members_version
        CHECK (row_version >= 1),

    CONSTRAINT chk_members_suspension
        CHECK (suspended_at IS NULL OR suspended_at >= joined_at),

    CONSTRAINT chk_members_revocation
        CHECK (revoked_at IS NULL OR revoked_at >= joined_at),

    CONSTRAINT chk_members_status_timestamps
        CHECK (
            (status = 'ACTIVE'
                AND suspended_at IS NULL
                AND revoked_at IS NULL)
            OR
            (status = 'SUSPENDED'
                AND suspended_at IS NOT NULL
                AND revoked_at IS NULL)
            OR
            (status = 'REVOKED'
                AND revoked_at IS NOT NULL)
        )
);

CREATE INDEX ix_members_user
    ON organizations.members (user_id);

CREATE INDEX ix_members_organization_status
    ON organizations.members (organization_id, status);
```

### `businesses`

```sql
CREATE TABLE organizations.businesses (
    business_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    name VARCHAR(200) NOT NULL,
    external_ref VARCHAR(200), -- Identifier used by Direct, POS, Whatson or another external platform.
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version BIGINT NOT NULL DEFAULT 1,

    CONSTRAINT fk_businesses_organization
        FOREIGN KEY (organization_id)
        REFERENCES organizations.organizations (organization_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_businesses_name
        CHECK (LENGTH(BTRIM(name)) > 0),

    CONSTRAINT chk_businesses_status
        CHECK (
            status IN (
                'ACTIVE',
                'SUSPENDED',
                'CLOSED'
            )
        ),

    CONSTRAINT chk_businesses_external_ref
        CHECK (
            external_ref IS NULL
            OR LENGTH(BTRIM(external_ref)) > 0
        ),

    CONSTRAINT chk_businesses_version
        CHECK (version >= 1),

    -- Required for composite foreign keys from scope tables.
    CONSTRAINT uq_businesses_id_organization
        UNIQUE (business_id, organization_id)
);
```

### `api_keys`

An API key is assigned to exactly one Member of one Organization. The
`organization_id` is retained for tenant-scoped lookup and indexing, and the
composite foreign key prevents it from disagreeing with the Member's Organization.
Only the non-secret prefix and a keyed SHA-256 digest of the high-entropy secret
are stored. The raw API key is displayed once and never persisted.

```sql
CREATE TABLE iam.api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    member_id UUID NOT NULL,
    organization_id UUID NOT NULL,
    name VARCHAR(200) NOT NULL,
    key_prefix VARCHAR(32) NOT NULL,
    key_hash BYTEA NOT NULL,
    rotated_from_api_key_id UUID,
    last_used_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'active',

    CONSTRAINT fk_api_keys_member_organization
        FOREIGN KEY (member_id, organization_id)
        REFERENCES organizations.members (id, organization_id)
        ON DELETE RESTRICT,

    -- Required for same-Member/same-Organization rotation lineage.
    CONSTRAINT uq_api_keys_rotation_context
        UNIQUE (id, member_id, organization_id),

    CONSTRAINT fk_api_keys_rotated_from
        FOREIGN KEY (
            rotated_from_api_key_id,
            member_id,
            organization_id
        )
        REFERENCES iam.api_keys (
            id,
            member_id,
            organization_id
        )
        ON DELETE RESTRICT,

    CONSTRAINT uq_api_keys_prefix
        UNIQUE (key_prefix),

    CONSTRAINT uq_api_keys_hash
        UNIQUE (key_hash),

    CONSTRAINT chk_api_keys_name
        CHECK (LENGTH(BTRIM(name)) > 0),

    CONSTRAINT chk_api_keys_prefix
        CHECK (key_prefix ~ '^ark_[A-Za-z0-9]{8,28}$'),

    CONSTRAINT chk_api_keys_hash_length
        CHECK (OCTET_LENGTH(key_hash) = 32),

    CONSTRAINT chk_api_keys_status
        CHECK (status IN ('active', 'revoked')),

    CONSTRAINT chk_api_keys_expiration
        CHECK (expires_at > created_at),

    CONSTRAINT chk_api_keys_last_used
        CHECK (last_used_at IS NULL OR last_used_at >= created_at),

    CONSTRAINT chk_api_keys_rotation
        CHECK (
            rotated_from_api_key_id IS NULL
            OR rotated_from_api_key_id <> id
        ),

    CONSTRAINT chk_api_keys_revocation
        CHECK (
            (status = 'active' AND revoked_at IS NULL)
            OR
            (status = 'revoked'
                AND revoked_at IS NOT NULL
                AND revoked_at >= created_at)
        )
);

CREATE UNIQUE INDEX uq_api_keys_single_rotation_successor
    ON iam.api_keys (rotated_from_api_key_id)
    WHERE rotated_from_api_key_id IS NOT NULL;

CREATE INDEX ix_api_keys_member_status
    ON iam.api_keys (member_id, status);

CREATE INDEX ix_api_keys_organization_status
    ON iam.api_keys (organization_id, status);
```

An API key is usable only when `status = 'active'`, `revoked_at IS NULL`,
`expires_at > NOW()`, and its Member, Organization, Role, and requested Business
all pass their current checks. Suspending or revoking a Member therefore disables
all of that Member's API keys without rewriting the API-key rows. `last_used_at`
is operational metadata and may be updated asynchronously or at a throttled rate;
it is never authorization truth. The application must advance `updated_at` on
every API-key mutation.

### `audit_events`

Audit events are append-only. `actor_id` is intentionally text because it stores
a User UUID string for `USER`, an API-key UUID string for `API_KEY`, or a stable
workload code such as `JOB_WORKER` for `SYSTEM`. Actor references are historical
snapshots and are validated by the application before insertion rather than by a
polymorphic foreign key.

```sql
CREATE TABLE audit.audit_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actor_type TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    organization_id UUID,
    member_id UUID,
    business_id UUID,
    action TEXT NOT NULL,
    target_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    result TEXT NOT NULL,
    request_id UUID NOT NULL,
    details JSONB NOT NULL DEFAULT '{}'::jsonb,

    CONSTRAINT fk_audit_member_organization
        FOREIGN KEY (member_id, organization_id)
        REFERENCES organizations.members (id, organization_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_audit_business_organization
        FOREIGN KEY (business_id, organization_id)
        REFERENCES organizations.businesses (business_id, organization_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_audit_actor_type
        CHECK (actor_type IN ('USER', 'API_KEY', 'SYSTEM')),

    CONSTRAINT chk_audit_actor_context
        CHECK (
            actor_type = 'SYSTEM'
            OR (member_id IS NOT NULL AND organization_id IS NOT NULL)
        ),

    CONSTRAINT chk_audit_actor_id
        CHECK (LENGTH(BTRIM(actor_id)) > 0),

    CONSTRAINT chk_audit_action
        CHECK (action ~ '^[a-z][a-z0-9_.]{1,149}$'),

    CONSTRAINT chk_audit_target_type
        CHECK (target_type ~ '^[A-Z][A-Z0-9_]{1,99}$'),

    CONSTRAINT chk_audit_target_id
        CHECK (LENGTH(BTRIM(target_id)) > 0),

    CONSTRAINT chk_audit_result
        CHECK (result IN ('SUCCESS', 'ACCEPTED', 'DENIED', 'FAILED')),

    CONSTRAINT chk_audit_details_object
        CHECK (jsonb_typeof(details) = 'object')
);

CREATE INDEX ix_audit_events_organization_time
    ON audit.audit_events (organization_id, occurred_at DESC);

CREATE INDEX ix_audit_events_request
    ON audit.audit_events (request_id);

CREATE INDEX ix_audit_events_actor
    ON audit.audit_events (actor_type, actor_id, occurred_at DESC);

CREATE INDEX ix_audit_events_target
    ON audit.audit_events (target_type, target_id, occurred_at DESC);
```

Runtime database grants must deny `UPDATE` and `DELETE` on `audit.audit_events`.
Sensitive fields and raw API-key material must never be copied into `details`.

An organization owner is an active Member whose selected predefined Role is
`ORG_OWNER`. The User, Member, Role, API keys, and audit records remain separate
and are connected by immutable IDs.

# Interactions
## `Organization onboarding`
- Register or resolve an authenticated User through the approved human trust boundary.
- Collect and verify only the approved User profile fields.
- Create the User record if it does not already exist.
- Create an Organization for the User.
- Create an active Member linking the User to the Organization.
- Select the predefined `ORG_OWNER` Role for that Member.
- Issue the first API key only through an approved bootstrap flow and display it once.
- Append audit events for every mutation.
  
- Create the organization’s billing account.
- Create the first business.
- Derive access from the active Member and the Organization-to-Business relationship.

## `Member administration`
- Add an existing User as a Member.
- Suspend, reactivate, or revoke a Member.
- Change the Member's one selected predefined Role and increment `row_version`.
- Transfer organization ownership by selecting `ORG_OWNER` for the new Member before changing or revoking the old owner's Member record.
- Issue, rotate, revoke, or expire API keys independently.
- Audit every permission change.
- The last active organization owner should not be removable until another active owner exists.

## `Business administration`
Supported operations:
Create a business under an organization.
Update non-authoritative metadata such as display name.
Link an upstream external business reference.
Activate, suspend, reactivate, or close the business.
Grant members access to the business.
Read the business’s subscriptions, entitlements, usage, data, and jobs through the organization administration APIs.
Suspending a business should prevent new ingestion and capability execution without deleting historical evidence.

## `API-key operations`
Supported operations:
Issue an API key for an active Member.
Rotate an API key while preserving same-Member/same-Organization lineage.
Revoke or expire an API key.
Disable all API keys by suspending or revoking their Member.
Verify an API key and create:
AuthContext {
  actor_type,
  actor_id,
  user_id,
  api_key_id,
  member_id,
  organization_id,
  business_id,
  role_id,
  role_version,
  permissions,
  authenticated_at
}
Organization and business scope come from the verified API key, active Member,
and stored Organization-to-Business relationship—not arbitrary request fields.

## `Internal workload identity`

`SYSTEM` is an audit actor type, not an authentication mechanism. In the initial
modular monolith, schedulers and workers run under distinct least-privilege
deployment-managed service identities. A trusted scheduler supplies an internal
context that callers cannot create or broaden:

```text
WorkloadContext {
  workload_id,
  organization_id,
  business_id,
  originating_member_id,
  job_id,
  attempt_id,
  fencing_token,
  purpose,
  issued_at,
  expires_at
}
```

The worker revalidates job, attempt, tenant, purpose, and fencing state before an
effect. If a worker is later deployed as a separate service, that service receives
its own deployment-managed identity; no `system_user` or `system_member` row is
created merely for audit attribution.

# Subscription, entitlement, and configuration interactions
## `Enable a capability`
Authenticate an organization administrator.
Verify organization status.
Select an existing ARK capability definition.
Create or activate the organization subscription.
Grant selected businesses entitlements to specific operations.
Attach quota policies.
Optionally create versioned business settings.
Record audit evidence.
This operation must not ingest data or execute the capability.
## `Disable a capability`
Suspend or cancel the subscription.
Revoke or suspend its business entitlements.
Reject new operation admission.
Decide through policy whether existing jobs finish or cancel.
Preserve historical jobs, usage, results, and audit records.
## `Change capability configuration`
Authenticate an authorized administrator.
Read the current version and ETag.
Validate the proposed configuration against the capability definition.
Write a new settings version using If-Match.
Audit old/new version references.
Do not mutate capability-private model/scientific state directly.

# Credit and billing interactions
## `Add credits`
Authorize a billing administrator/operator.
Append a positive ledger entry.
Update the cached account balance/version if one is maintained.
Record the adjustment reason and effect ID.
Append an audit event.
## `Reserve credits before work`
Resolve organization billing account.
Verify account is active.
Evaluate subscription, entitlement, and quota.
Estimate required units using the versioned meter policy.
Check available credits.
Create an idempotent reservation.
Return reservation_id to job admission.
Create the job referencing that reservation.
If reservation fails, no job should be created.
## `Successful completion`
Capability finishes and commits its result.
Write one immutable usage record.
Calculate actual charge using the recorded meter version.
Settle the reservation.
Append the debit ledger entry.
Release unused reserved credits.
Link result, job, usage, reservation, and ledger effect.
Audit settlement when required.
## `Failure or cancellation`
Depending on the approved commercial policy:
release the complete reservation;
charge only consumed units and release the remainder;
create a compensating refund after settlement.
The exact pricing and failure-charge policy is still unresolved. It should be versioned rather than hard-coded.
## `Reconciliation`
Periodically or through maintenance:
find expired reservations;
find completed jobs without usage records;
find usage without settlement;
find duplicate effect IDs;
compare cached balance against ledger-derived balance;
release or correct using explicit compensating entries;
never silently edit ledger history.

# Data-ingestion interaction
Verify an API key or trusted internal WorkloadContext.
Resolve its active Member context when the request originated from a User or API key.
Resolve exactly one Organization and one Business from trusted stored relationships.
Verify business is active.
Check source-write entitlement and quota.
Reserve credits only if ingestion is a billed operation.
Resolve exact registered source-contract version.
Register upload or accept bounded inline data.
Store immutable raw bytes and checksum.
Create an ingestion run idempotently.
Submit a durable validation job.
Run light validation.
Run deep validation.
Build canonical customer/transaction data.
Publish a new immutable READY dataset version.
Record usage and settle/release any reservation.
Append audit/lineage evidence.

# Capability-execution interaction
Verify an API key or trusted internal WorkloadContext and derive one Organization and Business.
Verify organization and business are active.
Verify subscription is active.
Verify the business entitlement for the requested operation.
Check quota and rate limits.
Resolve the exact READY dataset version.
Run capability-specific scientific eligibility.
Reserve credits if chargeable.
Create a durable job with the reservation, dataset, operation, configuration, and idempotency references.
Worker claims the job using a lease and fencing token.
Capability executes without accessing sibling internals.
Commit result.
Record usage.
Settle or release credit reservation.
Append audit and trace evidence.
Return result metadata or an opaque result reference.
These checks are intentionally separate:
Subscription enabled
    ≠ data ingested
    ≠ dataset READY
    ≠ capability scientifically eligible
    ≠ capability executed

# Examples
```text
User:
    U_ALI → Ali
    U_SARA → Sara

Member:
    M_ALI_AFE  → U_ALI belongs to ORG_AFE with Role ORG_OWNER
    M_ALI_ACME → U_ALI also belongs to ORG_ACME with Role DATA_VIEWER
    M_SARA_AFE → U_SARA belongs to ORG_AFE with Role DATA_INGESTOR

API key:
    K_ALI_AFE_1  → assigned to M_ALI_AFE
    K_ALI_AFE_2  → rotated successor of K_ALI_AFE_1
    K_SARA_AFE_1 → assigned to M_SARA_AFE

Role:
    ORG_OWNER
    ADMIN
    BILLING_MANAGER
    DATA_INGESTOR
    DATA_VIEWER

Permission examples for ORG_OWNER:
    organization.manage
    members.invite
    billing.manage
    credits.purchase
    data.ingest
    data.read

System audit actor:
    JOB_WORKER → internal worker operating under a trusted WorkloadContext
```

The example shows that one User may belong to multiple Organizations through
different Member records, while every Member has one Role and its own API keys.

# relation to "Billing"
- `organization_id` in `reservations` to enforce organization boundaries.
- `reservation_id` and `usage_record_id` in ledger entries to enforce settlement uniqueness.



## `Billing`
```sql
CREATE TABLE billing.billing_accounts (
    billing_account_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    currency_or_credit_unit VARCHAR(32) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    cached_available_balance NUMERIC(20, 6) NOT NULL DEFAULT 0, -- Performance cache, not the authoritative financial record.
    version BIGINT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_billing_accounts_organization
        FOREIGN KEY (organization_id)
        REFERENCES organizations.organizations (organization_id)
        ON DELETE RESTRICT,

    CONSTRAINT uq_billing_accounts_organization_unit
        UNIQUE (organization_id, currency_or_credit_unit),

    CONSTRAINT uq_billing_accounts_id_organization
        UNIQUE (billing_account_id, organization_id),

    CONSTRAINT chk_billing_accounts_status
        CHECK (
            status IN (
                'ACTIVE',
                'SUSPENDED',
                'CLOSED'
            )
        ),

    CONSTRAINT chk_billing_accounts_unit
        CHECK (
            currency_or_credit_unit ~ '^[A-Z][A-Z0-9_]{1,31}$'
        ),

    CONSTRAINT chk_billing_accounts_version
        CHECK (version >= 1)
);
```


## `Credit reservations`
```sql
CREATE TABLE billing.credit_reservations (
    reservation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    billing_account_id UUID NOT NULL,
    organization_id UUID NOT NULL,
    business_id UUID NOT NULL,
    operation_id VARCHAR(100) NOT NULL, -- Capability operation code, such as recommendation.generate.
    requested_units NUMERIC(20, 6) NOT NULL,
    reserved_amount NUMERIC(20, 6) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'RESERVED',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    idempotency_key VARCHAR(200) NOT NULL,
    request_fingerprint BYTEA NOT NULL,  -- SHA-256 hash of the canonical request content.
    version BIGINT NOT NULL DEFAULT 1,

    CONSTRAINT fk_credit_reservations_account
        FOREIGN KEY (billing_account_id, organization_id)
        REFERENCES billing.billing_accounts (
            billing_account_id,
            organization_id
        )
        ON DELETE RESTRICT,

    CONSTRAINT fk_credit_reservations_business
        FOREIGN KEY (business_id, organization_id)
        REFERENCES organizations.businesses (
            business_id,
            organization_id
        )
        ON DELETE RESTRICT,

    CONSTRAINT uq_credit_reservation_id_context
        UNIQUE (
            reservation_id,
            organization_id,
            business_id,
            operation_id
        ),

    CONSTRAINT uq_credit_reservation_idempotency
        UNIQUE (
            organization_id,
            business_id,
            operation_id,
            idempotency_key
        ),

    CONSTRAINT chk_credit_reservation_units
        CHECK (requested_units > 0),

    CONSTRAINT chk_credit_reservation_amount
        CHECK (reserved_amount > 0),

    CONSTRAINT chk_credit_reservation_expiration
        CHECK (expires_at > created_at),

    CONSTRAINT chk_credit_reservation_fingerprint
        CHECK (OCTET_LENGTH(request_fingerprint) = 32),

    CONSTRAINT chk_credit_reservation_status
        CHECK (
            status IN (
                'RESERVED',
                'SETTLED',
                'RELEASED',
                'EXPIRED',
                'PARTIALLY_REFUNDED',
                'REFUNDED'
            )
        ),

    CONSTRAINT chk_credit_reservation_version
        CHECK (version >= 1)
);
```

## `Usage records`
produced by the [metering system]
```sql
CREATE TABLE billing.usage_records (
    usage_record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    business_id UUID NOT NULL,
    operation_id VARCHAR(100) NOT NULL,
    job_id UUID,  -- Opaque reference to the job module.
    reservation_id UUID NOT NULL,
    measured_units NUMERIC(20, 6) NOT NULL,
    charge_amount NUMERIC(20, 6) NOT NULL,
    meter_version VARCHAR(100) NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_usage_records_business
        FOREIGN KEY (business_id, organization_id)
        REFERENCES organizations.businesses (
            business_id,
            organization_id
        )
        ON DELETE RESTRICT,

    CONSTRAINT fk_usage_records_reservation
        FOREIGN KEY (
            reservation_id,
            organization_id,
            business_id,
            operation_id
        )
        REFERENCES billing.credit_reservations (
            reservation_id,
            organization_id,
            business_id,
            operation_id
        )
        ON DELETE RESTRICT,

    -- One usage result for each reservation.
    CONSTRAINT uq_usage_records_reservation
        UNIQUE (reservation_id),

    CONSTRAINT chk_usage_records_measured_units
        CHECK (measured_units >= 0),

    CONSTRAINT chk_usage_records_charge
        CHECK (charge_amount >= 0),

    CONSTRAINT chk_usage_records_meter_version
        CHECK (LENGTH(BTRIM(meter_version)) > 0)
);
```
The ledger uses signed amounts:
- Positive amount: adds credits.
- Negative amount: removes credits.
```sql
CREATE TABLE billing.credit_ledger_entries (
    ledger_entry_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    billing_account_id UUID NOT NULL,
    entry_type VARCHAR(30) NOT NULL,
    amount NUMERIC(20, 6) NOT NULL,
    effect_id UUID NOT NULL, -- Unique identifier of the logical financial effect.
    reservation_id UUID,
    usage_record_id UUID,
    reason_code VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by_actor_type TEXT NOT NULL,
    created_by_actor_id TEXT NOT NULL,
    audit_event_id UUID NOT NULL,

    CONSTRAINT fk_ledger_billing_account
        FOREIGN KEY (billing_account_id)
        REFERENCES billing.billing_accounts (billing_account_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_ledger_reservation
        FOREIGN KEY (reservation_id)
        REFERENCES billing.credit_reservations (reservation_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_ledger_usage_record
        FOREIGN KEY (usage_record_id)
        REFERENCES billing.usage_records (usage_record_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_ledger_audit_event
        FOREIGN KEY (audit_event_id)
        REFERENCES audit.audit_events (id)
        ON DELETE RESTRICT,

    -- Replaying the same logical effect cannot create another charge.
    CONSTRAINT uq_ledger_account_effect
        UNIQUE (billing_account_id, effect_id),

    CONSTRAINT chk_ledger_actor_type
        CHECK (created_by_actor_type IN ('USER', 'API_KEY', 'SYSTEM')),

    CONSTRAINT chk_ledger_actor_id
        CHECK (LENGTH(BTRIM(created_by_actor_id)) > 0),

    CONSTRAINT chk_ledger_entry_type
        CHECK (
            entry_type IN (
                'CREDIT',
                'SETTLEMENT',
                'REFUND',
                'ADJUSTMENT_CREDIT',
                'ADJUSTMENT_DEBIT'
            )
        ),

    CONSTRAINT chk_ledger_signed_amount
        CHECK (
            (
                entry_type IN (
                    'CREDIT',
                    'REFUND',
                    'ADJUSTMENT_CREDIT'
                )
                AND amount > 0
            )
            OR
            (
                entry_type IN (
                    'SETTLEMENT',
                    'ADJUSTMENT_DEBIT'
                )
                AND amount < 0
            )
        ),

    CONSTRAINT chk_ledger_effect_references
        CHECK (
            (
                entry_type = 'SETTLEMENT'
                AND reservation_id IS NOT NULL
                AND usage_record_id IS NOT NULL
            )
            OR
            (
                entry_type = 'REFUND'
                AND reservation_id IS NOT NULL
            )
            OR
            entry_type IN (
                'CREDIT',
                'ADJUSTMENT_CREDIT',
                'ADJUSTMENT_DEBIT'
            )
        ),

    CONSTRAINT chk_ledger_reason_code
        CHECK (LENGTH(BTRIM(reason_code)) > 0)
);
```


## `Credit ledger`

# Notes
-- Users, Roles, Permissions and API-key hashes are owned by IAM.
-- Organizations, Members and Businesses are owned by the Organizations module.
-- Cross-schema foreign keys shown here protect the initial modular-monolith database;
-- a future service extraction must replace them with explicit public contracts.
--
-- Never store raw passwords, bearer tokens, raw API keys, client secrets, or
-- private keys in these tables. Never place secrets in logs or audit details.

-- Runtime grants are intentionally absent. Deployment must create narrowly
-- scoped LOGIN/NOLOGIN roles, transfer schema ownership as approved, and grant
-- only the IAM module writer/reader privileges for that environment.
