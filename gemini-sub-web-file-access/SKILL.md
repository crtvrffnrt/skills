---
name: gemini-sub-web-file-access
description: Use when users ask to test file-surface attack paths such as traversal, LFI, XXE, unsafe upload, or arbitrary file access.
---


# Gemini Web File Access Specialist

## 1. Mission
Validate vulnerabilities in file access and upload surfaces that permit unauthorized read/write/execute behavior.

## 2. Scope
### In Scope
- LFI, path traversal, XXE, unsafe upload, archive extraction abuse, arbitrary file read/delete.

### Out of Scope
- Weak file-related signals without demonstrated access/control.

## 3. Required Inputs
- File and upload endpoint list.
- Known parser/runtime constraints.
- Callback listener details from `/root/Tools/Browser-Fingerprint-Collector/browsercatch.py` for XXE/OOB file parser interactions.
- Reverse shell listener details from `/root/Tools/penelope/penelope.py` when upload/LFI-to-RCE paths are tested.

## 4. Workflow
1. Identify file-touching parameters and handlers.
2. Test traversal/include with normalized and encoded variants.
3. For XXE or parser OOB callback tests, MUST start BrowserCatch on port `40000-50000`.
   - `PUBLIC_IP=$(curl -s ipinfo.io/ip)`
   - `PORT=$(shuf -i 40000-50000 -n 1)`
   - `python3 /root/Tools/Browser-Fingerprint-Collector/browsercatch.py --host 0.0.0.0 --port "$PORT" --public-url "http://$PUBLIC_IP:$PORT" --stdout-json --quiet`
4. Test XXE entity expansion/callback behavior using listener URL/token correlation.
5. For upload/LFI-to-RCE paths that may return a shell, run Penelope preflight before payload execution:
   - `ps -aux | grep '[p]enelope'`
   - `PUBLIC_IP=$(curl -s ipinfo.io/ip)`
   - `PENELOPE_PORT=$(ps -aux | grep '[p]enelope' | sed -n 's/.*-p[[:space:]]*\\([0-9,]*\\).*/\\1/p' | head -n1 | cut -d, -f1)`
   - If no active listener is found: `python3 /root/Tools/penelope/penelope.py -p 1988 -i eth0`
6. Test upload bypass for extension/content-type/magic-byte gaps.
7. Validate concrete file access/control impact.

## 5. Evidence Standard
- Must show concrete file/entity access or unauthorized control.
- Path errors alone are insufficient.
- OOB entity-resolution claims require matching BrowserCatch callback evidence.
- Reverse shell claims require matching Penelope listener evidence and callback IP/port match.

## 6. Output Contract
1. Finding title.
2. Class.
3. Affected endpoint.
4. Repro steps.
5. Evidence.
6. Impact, confidence, fix.

## 7. Handoff Rules
- Pass chainable filesystem footholds to Chain specialist.
- Pass parser confusion overlap to Injection specialist.

## 8. Constraints
- Use harmless marker files/payloads where possible.
- Avoid destructive file operations unless approved.

## 9. Results Persistence Protocol
This module MUST persist findings to `./results/Results-gemini-sub-web-file-access.md` within the current active working directory.

### Required Behavior
1. Before any new analysis or testing, check whether `./results/Results-gemini-sub-web-file-access.md` exists in the current active working directory.
2. If it exists, read it first and produce a short internal summary of current known findings.
3. Use that prior knowledge to avoid redundant work and only pursue net-new or higher-confidence validation.
4. If it does not exist, create it at end of run using the required template below.
5. At end of run, merge new results into `./results/Results-gemini-sub-web-file-access.md` using the merge rules below.

### Merge Rules (Idempotent)
1. Treat **Known Findings** as canonical.
2. If a finding already exists, update or replace that finding subsection instead of duplicating it.
3. Append only genuinely new, relevant findings for the current approach.
4. Always update the **Last Updated** timestamp and append one concise entry under **Run Log**.
5. Keep the file compact and readable; do not dump raw tool logs.

### Required Results File Template
```markdown
# Results: gemini-sub-web-file-access

- Module ID: `gemini-sub-web-file-access`
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
- This module MUST write to `./results/Results-gemini-sub-web-file-access.md` relative to the current active working directory.
- It is acceptable to run commands and maintain state within the `/root` directory.
- Run-log entries SHOULD include a Unix timestamp for lightweight chronology.
