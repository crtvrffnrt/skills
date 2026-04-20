---
name: incident-response-bec
description: Blue team skill for Business Email Compromise and AiTM investigations focused on suspicious sign-ins, mailbox abuse, forwarding, session theft, consent abuse, and secondary phishing. Requires a UPN when available.
---

# Business Email Compromise and AiTM Analysis

## Mission
Determine whether a Microsoft identity and mailbox event is consistent with BEC, AiTM session theft, or another compromise pattern. Keep the assessment advisory; final decision belongs to the human analyst.

## Use when
- Suspicious sign-ins are paired with mailbox forwarding, inbox rules, or unexpected sent mail.
- A user reports phishing, strange mailbox behavior, or external recipients the user did not send to.
- The incident includes suspected session theft, token replay, or unauthorized app consent.
- The same workflow applies to non-Microsoft cases when equivalent sign-in and mailbox evidence exists.

## Required context
- Preferred inputs: UPN, incident window, alert or incident ID, and any phishing message identifiers.
- If UPN is missing and Microsoft telemetry is required, ask for it before querying.

## Investigation flow
1. Confirm the compromise hypothesis
   - identify the first suspicious sign-in or mailbox event
   - note source IP, geo, ASN, device, client app, and MFA context
2. Extract all IPs from the prompt, phishing artifacts, logs, and mailbox evidence and enrich every unique public IP
   - classify each IP as public or non-public before enrichment
   - run `/root/Tools/IncidentResponseScripts/vpnchecker.sh <ip>` and `/root/Tools/IncidentResponseScripts/ipir.sh <ip>` for every public IP
   - keep the raw outputs and use them in the verdict
3. Review authentication
   - look for impossible travel, session reuse, token replay, claim-based MFA satisfaction, repeated MFA prompts, or suspicious non-interactive activity
4. Review mailbox and collaboration activity
   - check inbox rules, forwarding, transport rules, sent items, deleted items, search behavior, delegated access, and OAuth consent
   - look for MailItemsAccessed or equivalent mailbox access evidence when available
5. Review downstream actions
   - identify secondary phishing, data exfiltration, file sharing changes, role or group changes, and privileged app consent
6. Contain and preserve
   - preserve the suspicious events, then revoke sessions, reset credentials, remove malicious rules, disable forwarding, and remove unauthorized consent
   - isolate the host if endpoint evidence shows active malware or credential theft

## Public IP rule
- If a public IP is present anywhere in the prompt or evidence, enrichment is required before closing the assessment.
- `vpnchecker.sh` is the fast VPN and provider signal.
- `ipir.sh` is the deeper multi-source reputation and infrastructure scoring pass.
- A VPN, proxy, or datacenter result alone is not enough to call the IP malicious.
- Use the enrichment results together with sign-in behavior, mailbox activity, and timeline context.
- If the tools cannot be executed, state the limitation explicitly in the analyst note.

## Microsoft Graph guidance
- Use `az rest` or the best available Microsoft telemetry path.
- Scope every query to the user and time window under investigation.
- Do not rely on the last sign-in date alone.
- Treat MFA as one control signal, not proof of safety.
- Do not alert the user before initial scoping if doing so could tip off an attacker.

## Evidence to preserve
- IPs, user agents, device IDs, session IDs, timestamps, and app IDs
- mailbox rule definitions, forwarding targets, and transport rule changes
- OAuth consents, delegated permissions, role changes, and group changes
- phishing message details or sender infrastructure when available

## Assessment output
- State whether the incident is confirmed, suspected, likely benign, or inconclusive.
- Separate facts from indicators and hypotheses.
- Explain whether the likely path is AiTM or session theft, mailbox compromise, or another access path.
- Include public IP enrichment results for every material public IP.
- List immediate containment actions and remaining gaps.
