---
name: ms-incident-response
description: Microsoft incident-response skill for Entra ID, Microsoft 365, Defender for Endpoint, Defender for Identity, and Defender for Office investigations. Use when triaging suspicious sign-ins, user compromise, mailbox rules or forwarding, token replay, impossible travel, consent abuse, endpoint compromise, or when you need TP/FP classification, scoping, containment, and reporting. Requires a UPN, host name, or incident identifier when available.
---

# Microsoft Incident Response

## Use when
- The user reports a suspicious Microsoft alert, compromised account, mailbox abuse, endpoint compromise, or mixed identity plus endpoint activity.
- The task is to classify a potential true positive, scope impact, contain active compromise, or write an incident summary.

## Required inputs
- Preferred inputs: `UPN`, device/host name, alert or incident ID, and a UTC time window.
- If the user principal name or host is missing, ask for it before querying Microsoft data.

## Workflow
1. Classify the alert.
   - Start with [references/tp_indicators.md](references/tp_indicators.md).
   - Decide whether the event is identity-led, mailbox-led, endpoint-led, or mixed.
2. Build the timeline.
   - Use [scripts/extract_entities.py](scripts/extract_entities.py) to pull users, hosts, IPs, hashes, and domains from alert exports.
   - Normalize all timestamps to UTC and keep first-seen and last-seen ordering.
3. Investigate identity.
   - Follow [references/identity_analysis.md](references/identity_analysis.md).
   - Review sign-ins, risk events, MFA context, app consent, and post-authentication activity.
4. Investigate mailbox and collaboration activity.
   - Check inbox rules, forwarding, sent items, and Office audit events that show mailbox access or exfiltration.
5. Investigate endpoint activity.
   - Follow [references/endpoint_triage.md](references/endpoint_triage.md).
   - Review process trees, persistence, network destinations, downloads, and host isolation needs.
6. Contain and eradicate.
   - Revoke sessions, reset passwords, remove malicious rules or forwarding, remove suspicious OAuth consent, and isolate hosts when active malware or C2 is present.
7. Report.
   - Draft the final incident summary with [assets/summary_report.md](assets/summary_report.md).

## Microsoft Graph and `az rest`
- Prefer `az rest` for Microsoft Graph and Entra queries.
- Scope every query by `UPN`, host, incident ID, or a narrow UTC window.
- Use `v1.0` when it exposes the required data; use `beta` only when the needed field is unavailable elsewhere.
- Preserve raw evidence before making destructive changes such as session revocation or account blocking.

## Operating rules
- Do not assume MFA means the account is safe.
- Do not alert the user before initial scoping if that could tip off an attacker.
- Treat missing telemetry as a limitation, not as proof of innocence.
- State clearly when a conclusion is an inference from partial logs.

## Practical outputs
- A concise scope summary.
- A timeline of suspicious events.
- Containment actions already taken.
- Remaining gaps and recommended next checks.
