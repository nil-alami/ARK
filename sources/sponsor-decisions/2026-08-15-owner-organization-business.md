# Sponsor decision — owner, organization, business, capability pattern, and admin scope

Date received: 2026-08-15

Authority: explicit ARK sponsor decision supplied in the active Codex task after the original design package was completed.

## Sponsor-provided product facts

- A person registers in ARK as an owner/admin profile. The profile includes at least full name and phone number; additional registration fields were not specified.
- One owner can define one or multiple organizations.
- An organization contains businesses.
- The owner defines one ARK service pattern for an organization's businesses. The same enabled service set applies to all businesses in that organization.
- Example capability patterns include `{RFM, NPT, REC}` and `{RFM, Churn}`.
- Example: Andrew owns the Direct organization. Direct is an SMS marketing platform hosting data for approximately 1,000 businesses such as shops, restaurants, and cafés. Andrew can configure Direct's businesses to use RFM and Churn.
- Authorization is intended to support organization roles or privileges such as admin, viewer, and tester. At present, only the admin role is usable and implemented.

## Clarifications explicitly approved on 2026-08-15

- An organization admin may change the organization's ARK service pattern, for example from `{RFM, Churn}` to `{RFM, Churn, REC}`.
- The admin role is organization-scoped. An admin of Direct can access all Direct businesses.

## Still unspecified by the sponsor

- The complete registration-field set represented by “and ...”, the concrete authentication provider/credential mechanism, and phone verification/uniqueness rules.
- Whether an organization may have multiple organization owners, how ownership transfer works, and whether an admin may appoint or remove other admins.
- Exact permission mappings and activation rules for viewer and tester.
- Business transfer between organizations and cross-business aggregate/export contracts.

This source records the sponsor's words and decisions. Architectural interpretations and implementation constraints are recorded separately in ADR-017.
