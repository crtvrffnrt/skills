---
name: intune
description: Manage and inspect Microsoft Intune resources using Microsoft Graph and an Azure CLI service principal. Use for Intune policies, configuration profiles, devices, apps, assignments, and related administrative tasks.
---

# Intune with Azure CLI

Use this skill together or alongside with `pentest-gemini-az` for Azure CLI and Microsoft Graph operations. Follow the user's requested scope; a configured credential does not authorize unrelated changes.

## Authentication and context

Authenticate Azure CLI as the configured service principal using `AZURE_CLIENT_ID` and `AZURE_CLIENT_SECRET` from the environment. For the root user, these are configured in `/root/.zshrc`; if they are not inherited, load them in the command shell without printing their values. Use tenant `f8f1547f-48cd-40d8-addc-fc7bd12dc44f` for this configured application, unless the user explicitly specifies a different confirmed tenant. Never print, copy into artifacts, or commit the secret. Do not create or rotate credentials unless requested. If credentials are absent, expired, or lack permissions, report the issue and the required permission; do not silently change consent or permissions.

Use `az login --service-principal` with the configured client ID and tenant, and `--allow-no-subscriptions` when needed. Supply the secret through Azure CLI's password prompt or another supported secure input mechanism, never as a command argument; do not enable tracing or expose credentials in output. Preserve existing CLI state and configuration as required by the runtime; use an isolated configuration directory only when permitted. Confirm the resulting tenant and service-principal identity before querying, and run subsequent `az rest` calls in that same authenticated context. Do not fall back silently to an interactive user account. Azure CLI login may briefly fail immediately after a newly created secret; retry only for a short propagation delay.

## Graph operations

Use `az rest` and the existing `pentest-gemini-az` workflow. Prefer Microsoft Graph `v1.0`; use `beta` when the required Intune resource or fields are unavailable in `v1.0`, and identify beta results as such. Check current Microsoft documentation when selecting endpoints or permissions. Follow every `@odata.nextLink` for complete listings.

Configuration profiles span different collections: Settings Catalog policies are under `/deviceManagement/configurationPolicies` (use beta if unavailable in v1.0), while classic device configuration profiles are under `/deviceManagement/deviceConfigurations`. Query both when the request calls for all configuration profiles; report failures or permission gaps separately rather than presenting partial results as complete. Other Intune policy types may use separate collections; clarify the scope in the result.

List or inspect resources by default. Make changes only when requested, preserve unrelated settings, and verify the result. Report the tenant, resource names and IDs as relevant, endpoint versions, permissions failures, and validation performed. Never include credential values in output.
