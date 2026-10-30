---
name: intune
description: Manage and inspect Microsoft Intune resources using Microsoft Graph and an Azure CLI service principal. Use for Intune policies, configuration profiles, devices, apps, assignments, and related administrative tasks.
---

# Intune with Azure CLI

Use this skill together or alongside with `pentest-gemini-az` for Azure CLI and Microsoft Graph operations. Follow the user's requested scope; a configured credential does not authorize unrelated changes.

## Authentication and context

The local shell configuration may provide `INTUNE_TENANT_ID`, `INTUNE_CLIENT_ID`, `INTUNE_CLIENT_SECRET`, `INTUNE_APP_NAME`, `INTUNE_APP_OBJECT_ID` (app registration), and `INTUNE_SERVICE_PRINCIPAL_OBJECT_ID` (enterprise application). Read credentials from the environment or the user's local `~/.zshrc`; never print, copy into artifacts, or commit secrets. Do not create or rotate credentials unless requested. If credentials are absent, expired, or lack permissions, report the issue and the required permission; do not silently change consent or permissions.

Use an isolated Azure CLI configuration directory for service-principal authentication so the existing interactive login is preserved. Load the environment in the same shell as the commands, log in with `az login --service-principal --tenant "$INTUNE_TENANT_ID" --username "$INTUNE_CLIENT_ID" --password "$INTUNE_CLIENT_SECRET" --allow-no-subscriptions`, and remove the temporary configuration directory on exit. Avoid exposing credentials through tracing or command output. Confirm the resulting tenant before querying. Azure CLI login may briefly fail immediately after a newly created secret; retry only for a short propagation delay.

## Graph operations

Use `az rest` and the existing `pentest-gemini-az` workflow. Prefer Microsoft Graph `v1.0`; use `beta` when the required Intune resource or fields are unavailable in `v1.0`, and identify beta results as such. Check current Microsoft documentation when selecting endpoints or permissions. Follow every `@odata.nextLink` for complete listings.

Configuration profiles span different collections: Settings Catalog policies are under `/deviceManagement/configurationPolicies` (use beta if unavailable in v1.0), while classic device configuration profiles are under `/deviceManagement/deviceConfigurations`. Query both when the request calls for all configuration profiles; report failures or permission gaps separately rather than presenting partial results as complete. Other Intune policy types may use separate collections; clarify the scope in the result.

List or inspect resources by default. Make changes only when requested, preserve unrelated settings, and verify the result. Report the tenant, resource names and IDs as relevant, endpoint versions, permissions failures, and validation performed. Never include credential values in output.
