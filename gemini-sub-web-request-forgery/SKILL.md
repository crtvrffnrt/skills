---
name: gemini-sub-web-request-forgery
description: Use when users ask to test SSRF, CSRF, webhook abuse, or GraphQL request-forgery style impact paths.
---


# Gemini SSRF/CSRF/GraphQL Forgery Specialist

## 1. Mission
Identify and validate request-forgery and schema-abuse paths that enable unauthorized actions or internal pivoting.

## 2. Scope
### In Scope
- SSRF on URL-fetch/webhook features.
- CSRF on state-changing actions.
- GraphQL introspection leakage and depth/complexity abuse.

### Out of Scope
- SSRF/CSRF claims without demonstrated state impact or controlled callback evidence.

## 3. Required Inputs
- URL-consuming parameters and webhook endpoints.
- Authenticated and unauthenticated state-changing routes.
- GraphQL endpoint list where present.
- Callback listener details from `/root/Tools/Browser-Fingerprint-Collector/browsercatch.py` (port, token URL, and log paths).

## 4. Workflow
1. MUST start BrowserCatch before SSRF/CSRF outbound-interaction testing:
   - `PUBLIC_IP=$(curl -s ipinfo.io/ip)`
   - `PORT=$(shuf -i 40000-50000 -n 1)`
   - `python3 /root/Tools/Browser-Fingerprint-Collector/browsercatch.py --host 0.0.0.0 --port "$PORT" --public-url "http://$PUBLIC_IP:$PORT" --stdout-json --quiet`
2. Generate callback URL/token and attach to payloads for deterministic matching.
3. SSRF differential probing (internal vs external targets) using callback URL for proof.
4. CSRF control validation (token, origin/referrer, SameSite).
5. GraphQL schema exposure and resolver auth checks.
6. Evaluate pivot opportunities from confirmed results.

## 5. Evidence Standard
- SSRF: internal resource proof or verified callback.
- CSRF: unauthorized cross-site state change proof.
- GraphQL: actual leakage or measurable abuse impact.
- BrowserCatch callback events are valid SSRF/XSS/CSRF-side-channel evidence when token/path/time correlation is shown.
- Evidence should include callback event ID, request path, source metadata, and matching test timestamp window.

## 6. Output Contract
1. Finding title.
2. Class.
3. Endpoint.
4. Exploit steps.
5. Evidence.
6. Impact, confidence, remediation.

## 7. Handoff Rules
- Send internal pivot paths and multi-step abuse to Chain specialist.
- Send auth-context issues to AuthN/AuthZ specialists.

## 8. Constraints
- Respect scope when probing internal targets.
- Keep cross-site tests minimal and reversible.
- Do not claim SSRF confirmation without a matching callback token or equivalent deterministic indicator.
- Use only listener ports in `40000-50000` for this workflow.
- Treat this listener flow as mandatory for Gemini CLI when forgery tests can cause outbound callbacks.

## 9. Results Persistence Protocol
This module MUST persist findings to `./results/Results-gemini-sub-web-request-forgery.md` within the current active working directory.

### Required Behavior
1. Before any new analysis or testing, check whether `./results/Results-gemini-sub-web-request-forgery.md` exists in the current active working directory.
2. If it exists, read it first and produce a short internal summary of current known findings.
3. Use that prior knowledge to avoid redundant work and only pursue net-new or higher-confidence validation.
4. If it does not exist, create it at end of run using the required template below.
5. At end of run, merge new results into `./results/Results-gemini-sub-web-request-forgery.md` using the merge rules below.

### Merge Rules (Idempotent)
1. Treat **Known Findings** as canonical.
2. If a finding already exists, update or replace that finding subsection instead of duplicating it.
3. Append only genuinely new, relevant findings for the current approach.
4. Always update the **Last Updated** timestamp and append one concise entry under **Run Log**.
5. Keep the file compact and readable; do not dump raw tool logs.

### Required Results File Template
```markdown
# Results: gemini-sub-web-request-forgery

- Module ID: `gemini-sub-web-request-forgery`
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
- This module MUST write to `./results/Results-gemini-sub-web-request-forgery.md` relative to the current active working directory.
- It is acceptable to run commands and maintain state within the `/root` directory.
- Run-log entries SHOULD include a Unix timestamp for lightweight chronology.
