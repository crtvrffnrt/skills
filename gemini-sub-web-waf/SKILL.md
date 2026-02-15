---
name: gemini-sub-web-waf
description: Use when users ask for WAF-aware testing and payload adaptation while preserving high-confidence vulnerability validation.
---


# Gemini WAF-Aware Exploitation Optimizer

## 1. Mission
Detect filtering controls, adapt payload delivery safely, and preserve high-signal vulnerability verification.

## 2. Scope
### In Scope
- Passive/active WAF detection.
- Payload shape/encoding/pacing adaptation.
- Verification quality under filtering constraints.

### Out of Scope
- Reporting bypass alone as vulnerability without exploit impact.

## 3. Required Inputs
- Baseline responses and block responses.
- Target vulnerability class and payload families.

## 4. Workflow
1. Identify WAF/control signatures.
2. Probe low-impact payload variants.
3. Apply controlled adaptation strategy.
4. Re-verify exploit condition with controls comparisons.
5. Separate control weakness from underlying vulnerability.

## 5. Evidence Standard
- Bypass must result in confirmed exploit behavior to be security finding.
- Include before/after request evidence.

## 6. Output Contract
1. WAF detection summary.
2. Blocking pattern.
3. Adaptation applied.
4. Resulting finding (if confirmed).
5. Evidence, confidence, recommendation.

## 7. Handoff Rules
- Return tuned payloads to originating specialist.
- Escalate confirmed exploit paths to Chain specialist.

## 8. Constraints
- Keep test volume low.
- Avoid automated bypass loops with no new signal.

## 9. Results Persistence Protocol
This module MUST persist findings to `./results/Results-gemini-sub-web-waf.md` within the current active working directory.

### Required Behavior
1. Before any new analysis or testing, check whether `./results/Results-gemini-sub-web-waf.md` exists in the current active working directory.
2. If it exists, read it first and produce a short internal summary of current known findings.
3. Use that prior knowledge to avoid redundant work and only pursue net-new or higher-confidence validation.
4. If it does not exist, create it at end of run using the required template below.
5. At end of run, merge new results into `./results/Results-gemini-sub-web-waf.md` using the merge rules below.

### Merge Rules (Idempotent)
1. Treat **Known Findings** as canonical.
2. If a finding already exists, update or replace that finding subsection instead of duplicating it.
3. Append only genuinely new, relevant findings for the current approach.
4. Always update the **Last Updated** timestamp and append one concise entry under **Run Log**.
5. Keep the file compact and readable; do not dump raw tool logs.

### Required Results File Template
```markdown
# Results: gemini-sub-web-waf

- Module ID: `gemini-sub-web-waf`
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
- This module MUST write to `./results/Results-gemini-sub-web-waf.md` relative to the current active working directory.
- It is acceptable to run commands and maintain state within the `/root` directory.
- Run-log entries SHOULD include a Unix timestamp for lightweight chronology.
