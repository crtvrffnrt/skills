---
name: gemini-api
description: Use when users request authorized API security testing (REST/GraphQL/gRPC/SOAP), including auth, authz, and abuse-path validation.
---


# Gemini API Security Profile

## 1. Mission
Perform authorized offensive API testing across REST, GraphQL, gRPC, OData, SOAP, WebSockets, and custom RPC interfaces.

## 2. Scope
### In Scope
- API surface discovery, authn/authz, object/function access control, mutation abuse, and execution paths.
- Protocol-specific parser and transport abuse that leads to real impact.

### Out of Scope
- Static-only issues without runtime abuse path.
- Unapproved data extraction and destructive operations.

## 3. Required Inputs
- API endpoints, schemas/contracts, and identity/role contexts.
- Tenant and environment boundaries.
- Allowed load and rate constraints.
- Outbound callback listener details from `/root/Tools/Browser-Fingerprint-Collector/browsercatch.py` for webhook/SSRF/blind execution validation.
- Reverse shell listener details from `/root/Tools/penelope/penelope.py` for shell-capable API RCE paths.

## 4. Workflow
1. Enumerate schema and endpoint surface.
2. Validate authentication and token handling.
3. Test object/function authorization boundaries.
4. For outbound-callback-capable non-shell tests, run BrowserCatch preflight and use tokenized callback URLs:
   - `PUBLIC_IP=$(curl -s ipinfo.io/ip)`
   - `PORT=$(shuf -i 40000-50000 -n 1)`
   - `python3 /root/Tools/Browser-Fingerprint-Collector/browsercatch.py --host 0.0.0.0 --port "$PORT" --public-url "http://$PUBLIC_IP:$PORT" --stdout-json --quiet`
5. For reverse-shell-capable API execution paths, run Penelope preflight before payload dispatch:
   - `ps -aux | grep '[p]enelope'`
   - `PUBLIC_IP=$(curl -s ipinfo.io/ip)`
   - `PENELOPE_PORT=$(ps -aux | grep '[p]enelope' | sed -n 's/.*-p[[:space:]]*\\([0-9,]*\\).*/\\1/p' | head -n1 | cut -d, -f1)`
   - If no active listener is found: `python3 /root/Tools/penelope/penelope.py -p 1988 -i eth0`
6. Probe mutation and execution surfaces (mass assignment, action endpoints).
7. Stress control surfaces (rate limits, batching, complexity) within approved limits.
8. Chain confirmed primitives for impact.

## 5. Evidence Standard
- Include minimal request/response proof pairs.
- Distinguish hypothesis from confirmed capability.
- Show trust boundary broken and resulting attacker capability.

## 6. Output Contract
1. Confirmed API findings with severity and confidence.
2. Exploitation path from entry point to impact.
3. Minimal reproducible commands and payloads.
4. Specific remediation guidance.

## 7. Handoff Rules
- Reuse web auth/authz/injection sub-agents for shared API attack surfaces.
- Use `gemini-sub-web-chain` for multi-step impact chaining.

## 8. Constraints
- Keep requests deterministic and low-noise.
- Preserve service availability.
- Redact tokens and secrets in report output by default.

## 9. Results Persistence Protocol
This module MUST persist findings to `./results/Results-gemini-api.md` within the current active working directory.

### Required Behavior
1. Before any new analysis or testing, check whether `./results/Results-gemini-api.md` exists in the current active working directory.
2. If it exists, read it first and produce a short internal summary of current known findings.
3. Use that prior knowledge to avoid redundant work and only pursue net-new or higher-confidence validation.
4. If it does not exist, create it at end of run using the required template below.
5. At end of run, merge new results into `./results/Results-gemini-api.md` using the merge rules below.

### Merge Rules (Idempotent)
1. Treat **Known Findings** as canonical.
2. If a finding already exists, update or replace that finding subsection instead of duplicating it.
3. Append only genuinely new, relevant findings for the current approach.
4. Always update the **Last Updated** timestamp and append one concise entry under **Run Log**.
5. Keep the file compact and readable; do not dump raw tool logs.

### Required Results File Template
```markdown
# Results: gemini-api

- Module ID: `gemini-api`
- Last Updated: <ISO-8601 timestamp>

## Known Findings
- <finding-id>: <short statement>

## Evidence / Notes
- <concise supporting evidence>

## Open Questions / Next Steps
- <next validation target>

## Run Log
- <timestamp>: <what changed, added, or refined>
```

### Path Scope Note
- Skills are maintained and read from `/root/.gemini/skills/`.
- The active working directory WILL NOT contain a `.gemini` folder.
- All tool outputs, logs, findings, and temporary files MUST be written to the current active working directory or a designated project-specific temporary directory.
- This module MUST write to `./results/Results-gemini-api.md` relative to the current active working directory.
- It is acceptable to run commands and maintain state within the `/root` directory.
- Run-log entries SHOULD include a Unix timestamp for lightweight chronology.
