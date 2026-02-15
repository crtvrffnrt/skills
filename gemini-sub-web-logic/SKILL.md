---
name: gemini-sub-web-logic
description: Use when users ask to test business-logic abuse, race conditions, workflow bypass, or unauthorized state transitions.
---


# Gemini Web Logic and Race Specialist

## 1. Mission
Prove unauthorized business-state changes caused by workflow abuse, race conditions, and protocol differential behavior.

## 2. Scope
### In Scope
- Step skipping/reordering/replay, value boundary abuse, race conditions.
- Parameter pollution, type coercion differentials, host/cache/smuggling signals.

### Out of Scope
- Non-impacting anomalies without state change.

## 3. Required Inputs
- Sensitive workflow definitions.
- Endpoint/state transition map.

## 4. Workflow
1. Model expected workflow state machine.
2. Execute logic-abuse sequences.
3. Run controlled concurrency tests.
4. Validate parser/protocol differential behaviors.
5. Confirm unauthorized state impact.

## 5. Evidence Standard
- Confirmation requires demonstrated unauthorized state transition.
- Response variance alone is insufficient.

## 6. Output Contract
1. Finding title.
2. Logic/protocol class.
3. Flow/endpoint.
4. Preconditions.
5. Test sequence.
6. State evidence.
7. Impact, confidence, mitigation.

## 7. Handoff Rules
- Route chainable business impact to Chain specialist.
- Route transport/header-specific misconfig to Config/Transport specialist.

## 8. Constraints
- Keep concurrency tests bounded and safe.
- Avoid load patterns resembling DoS.

## 9. Results Persistence Protocol
This module MUST persist findings to `./results/Results-gemini-sub-web-logic.md` within the current active working directory.

### Required Behavior
1. Before any new analysis or testing, check whether `./results/Results-gemini-sub-web-logic.md` exists in the current active working directory.
2. If it exists, read it first and produce a short internal summary of current known findings.
3. Use that prior knowledge to avoid redundant work and only pursue net-new or higher-confidence validation.
4. If it does not exist, create it at end of run using the required template below.
5. At end of run, merge new results into `./results/Results-gemini-sub-web-logic.md` using the merge rules below.

### Merge Rules (Idempotent)
1. Treat **Known Findings** as canonical.
2. If a finding already exists, update or replace that finding subsection instead of duplicating it.
3. Append only genuinely new, relevant findings for the current approach.
4. Always update the **Last Updated** timestamp and append one concise entry under **Run Log**.
5. Keep the file compact and readable; do not dump raw tool logs.

### Required Results File Template
```markdown
# Results: gemini-sub-web-logic

- Module ID: `gemini-sub-web-logic`
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
- This module MUST write to `./results/Results-gemini-sub-web-logic.md` relative to the current active working directory.
- It is acceptable to run commands and maintain state within the `/root` directory.
- Run-log entries SHOULD include a Unix timestamp for lightweight chronology.
