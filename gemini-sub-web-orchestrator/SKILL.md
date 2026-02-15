---
name: gemini-sub-web-orchestrator
description: Use when users request coordinated web pentesting across specialties with deduped findings and consolidated reporting.
---


# Gemini Web Orchestrator

## 1. Mission
Coordinate specialized web pentest sub-agents, enforce common evidence quality, and produce one consolidated exploitability-first output.

## 2. Scope
### In Scope
- Routing tasks by vulnerability class and attack surface.
- Deduplicating findings and sequencing chain validation.
- Normalizing confidence and severity output.

### Out of Scope
- Deep single-class testing that belongs to a specialist sub-agent.

## 3. Required Inputs
- Application map, auth context, and discovered signals.
- Operator priorities and time/impact constraints.

## 4. Workflow
1. Classify signals by attack domain.
2. For domains that may trigger non-shell outbound target traffic (SSRF, XXE, CSRF/XSS beacons), run BrowserCatch preflight:
   - `PUBLIC_IP=$(curl -s ipinfo.io/ip)`
   - `PORT=$(shuf -i 40000-50000 -n 1)`
   - `python3 /root/Tools/Browser-Fingerprint-Collector/browsercatch.py --host 0.0.0.0 --port "$PORT" --public-url "http://$PUBLIC_IP:$PORT" --stdout-json --quiet`
3. For reverse-shell-capable RCE/injection paths, run Penelope preflight before dispatch:
   - `ps -aux | grep '[p]enelope'`
   - `PUBLIC_IP=$(curl -s ipinfo.io/ip)`
   - `PENELOPE_PORT=$(ps -aux | grep '[p]enelope' | sed -n 's/.*-p[[:space:]]*\\([0-9,]*\\).*/\\1/p' | head -n1 | cut -d, -f1)`
   - If no active listener is found: `python3 /root/Tools/penelope/penelope.py -p 1988 -i eth0`
4. BrowserCatch listener port MUST be in `40000-50000`; callback token/URL and active `PUBLIC_IP:PENELOPE_PORT` MUST be shared with relevant sub-agents.
5. Route each domain to the best-fit sub-agent.
6. Enforce mandatory evidence checks.
7. Merge confirmed findings and remove duplicates.
8. Trigger chain analysis for compatible confirmed findings.

## 5. Evidence Standard
- No finding without execution-grade proof.
- Require controls comparison for high-impact claims.
- Reject status-only claims.

## 6. Output Contract
1. Confirmed Findings (deduplicated, prioritized).
2. Strong Hypotheses (next minimal test).
3. Exploit Chains (confirmed-only).
4. Fix Priorities by trust boundary.

## 7. Handoff Rules
- Route per specialty and avoid overlapping runs unless required for validation.
- Use `gemini-sub-web-chain` only when at least one confirmed finding exists.

## 8. Constraints
- Maintain low noise and avoid redundant probes.
- Keep all outputs machine-parseable and section-stable.

## 9. Results Persistence Protocol
This module MUST persist findings to `./results/Results-gemini-sub-web-orchestrator.md` within the current active working directory.

### Required Behavior
1. Before any new analysis or testing, check whether `./results/Results-gemini-sub-web-orchestrator.md` exists in the current active working directory.
2. If it exists, read it first and produce a short internal summary of current known findings.
3. Use that prior knowledge to avoid redundant work and only pursue net-new or higher-confidence validation.
4. If it does not exist, create it at end of run using the required template below.
5. At end of run, merge new results into `./results/Results-gemini-sub-web-orchestrator.md` using the merge rules below.

### Merge Rules (Idempotent)
1. Treat **Known Findings** as canonical.
2. If a finding already exists, update or replace that finding subsection instead of duplicating it.
3. Append only genuinely new, relevant findings for the current approach.
4. Always update the **Last Updated** timestamp and append one concise entry under **Run Log**.
5. Keep the file compact and readable; do not dump raw tool logs.

### Required Results File Template
```markdown
# Results: gemini-sub-web-orchestrator

- Module ID: `gemini-sub-web-orchestrator`
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
- This module MUST write to `./results/Results-gemini-sub-web-orchestrator.md` relative to the current active working directory.
- It is acceptable to run commands and maintain state within the `/root` directory.
- Run-log entries SHOULD include a Unix timestamp for lightweight chronology.
