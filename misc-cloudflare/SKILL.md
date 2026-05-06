s---
name: cloudflare-api-helper
description: Minimal Cloudflare operational helper for Codex/Gemini CLI. Use for Cloudflare DNS, zones, proxy settings, WAF/rulesets, cache/transform/origin rules, and account/zone inspection. Worker-specific tasks must use the locally authenticated Wrangler CLI instead of direct API calls.
---

# Cloudflare API Helper

This skill provides a minimal, safe operating pattern for Cloudflare tasks.

Use Cloudflare's REST API for non-Worker Cloudflare operations. Use local Wrangler for Worker-related operations.

## Required environment variables

The operator must provide these environment variables before using the skill:

```bash
export CODEX_CLOUDFLARE_TOKEN="<cloudflare-api-token>"
export CODEX_CLOUDFLARE_ACCOUNT="<cloudflare-account-id>"
```

Do not use hyphens in shell variable names. Shell variables like `CODEX-CLOUDFLARE-TOKEN` are invalid. Use `CODEX_CLOUDFLARE_TOKEN` and `CODEX_CLOUDFLARE_ACCOUNT`.

Never print, echo, log, commit, or write the token value to repository files.

## Mandatory first step: verify API token

Before performing any Cloudflare API operation, verify that the token is present and valid.

Run:

```bash
: "${CODEX_CLOUDFLARE_TOKEN:?Missing CODEX_CLOUDFLARE_TOKEN}"
: "${CODEX_CLOUDFLARE_ACCOUNT:?Missing CODEX_CLOUDFLARE_ACCOUNT}"

curl -X GET "https://api.cloudflare.com/client/v4/accounts/$CODEX_CLOUDFLARE_ACCOUNT/tokens/verify" \
     -H "Authorization: Bearer $CODEX_CLOUDFLARE_TOKEN"
```

The token is valid only if the JSON response contains:

```json
{
  "success": true
}
```

If validation fails, halt immediately. Do not attempt fallback authentication. Instruct the user to provide a valid Cloudflare API token with the required account and zone permissions.

Do not continue if any of these conditions are true:

```text
- CODEX_CLOUDFLARE_TOKEN is missing.
- CODEX_CLOUDFLARE_ACCOUNT is missing.
- The verify endpoint returns success=false.
- The request returns HTTP 401 or HTTP 403.
- The response cannot be parsed as successful Cloudflare API JSON.
```

## API request pattern

Use this pattern for Cloudflare REST API calls:

```bash
curl -fsS "https://api.cloudflare.com/client/v4/<endpoint>" \
  -H "Authorization: Bearer ${CODEX_CLOUDFLARE_TOKEN}" \
  -H "Content-Type: application/json"
```

For write operations, use explicit HTTP methods and JSON bodies:

```bash
curl -fsS -X PATCH "https://api.cloudflare.com/client/v4/<endpoint>" \
  -H "Authorization: Bearer ${CODEX_CLOUDFLARE_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"key":"value"}'
```

Never place the token in the URL. Never use query-string authentication.


## Worker handling

Do not use the REST API for Worker lifecycle operations when Wrangler is available locally.

For Worker-related tasks, first verify local Wrangler authentication:

```bash
wrangler whoami --json
```

Continue only if Wrangler returns valid authenticated account information. If Wrangler is not authenticated, halt and instruct the user to authenticate Wrangler locally.

Use Wrangler for Worker tasks such as:

```text
- Worker deploys
- Worker dev server
- Worker routes
- Worker secrets
- Worker KV/R2/D1 bindings through Wrangler project configuration
- Worker logs/tail
- Wrangler configuration validation
```

Examples:

```bash
wrangler whoami --json
wrangler deploy
wrangler dev
wrangler secret put SECRET_NAME
wrangler tail
```

Do not pass `CODEX_CLOUDFLARE_TOKEN` to Wrangler unless the user explicitly asks for token-based Wrangler execution. Prefer the existing local authenticated Wrangler session.

## REST API responsibilities

Use the REST API for non-Worker Cloudflare operations, including:

```text
- Account and zone discovery
- DNS record listing and changes
- Proxied/unproxied DNS state
- Zone settings
- WAF configuration
- Rulesets
- Cache rules
- Transform rules
- Origin rules
- SSL/TLS settings
- Security settings
```

Read before write. For every change request:

```text
1. Validate the token.
2. Resolve the target account or zone.
3. Read the current object/configuration.
4. Prepare the exact API change.
5. Execute the smallest possible change.
6. Read back the object/configuration and verify the result.
```

## Common endpoints

Token verification:

```text
GET /user/tokens/verify
```

Accounts:

```text
GET /accounts
GET /accounts/{account_id}
```

Zones:

```text
GET /zones
GET /zones/{zone_id}
GET /zones?name={zone_name}
```

DNS:

```text
GET    /zones/{zone_id}/dns_records
POST   /zones/{zone_id}/dns_records
GET    /zones/{zone_id}/dns_records/{dns_record_id}
PATCH  /zones/{zone_id}/dns_records/{dns_record_id}
PUT    /zones/{zone_id}/dns_records/{dns_record_id}
DELETE /zones/{zone_id}/dns_records/{dns_record_id}
```

Zone settings:

```text
GET   /zones/{zone_id}/settings
GET   /zones/{zone_id}/settings/{setting_id}
PATCH /zones/{zone_id}/settings/{setting_id}
```

Rulesets and WAF:

```text
GET   /zones/{zone_id}/rulesets
GET   /zones/{zone_id}/rulesets/{ruleset_id}
POST  /zones/{zone_id}/rulesets
PUT   /zones/{zone_id}/rulesets/{ruleset_id}
PATCH /zones/{zone_id}/rulesets/{ruleset_id}
DELETE /zones/{zone_id}/rulesets/{ruleset_id}

GET   /accounts/{account_id}/rulesets
GET   /accounts/{account_id}/rulesets/{ruleset_id}
POST  /accounts/{account_id}/rulesets
PUT   /accounts/{account_id}/rulesets/{ruleset_id}
PATCH /accounts/{account_id}/rulesets/{ruleset_id}
DELETE /accounts/{account_id}/rulesets/{ruleset_id}
```

## Safety rules

Do not perform destructive actions unless the user explicitly requested them.

Treat these as destructive or high-impact:

```text
- Deleting DNS records
- Changing proxied state for production records
- Changing nameservers
- Disabling SSL/TLS security features
- Disabling WAF or managed rules
- Replacing complete rulesets
- Deleting rulesets
- Deploying Workers to production
- Rotating or deleting secrets
```

For high-impact changes, prefer PATCH over PUT when supported. Preserve unrelated fields.

## Output format

When reporting results, include:

```text
- Target account or zone
- Operation performed
- Object changed
- Before/after summary
- Verification result
- Any Cloudflare API error code/message if applicable
```

Do not include bearer tokens, secret values, session cookies, or raw credential material in the response.

