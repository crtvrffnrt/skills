# User Account Compromise Analysis

Use this guide when investigating a suspicious Microsoft identity event.

## 1. Initial scoping
- Confirm the `UPN`.
- Pull recent alerts, risky sign-ins, and identity protection events for the user.
- Record the first suspicious time and the current incident window.

## 2. Authentication review
- Check source IP, geo, ASN, device, browser, and client app.
- Compare the sign-in against the user’s normal pattern.
- Look for MFA prompts, repeated denials, claim-based MFA satisfaction, or token replay indicators.
- Identify all applications accessed in the same session.

## 3. Post-authentication activity
- Review mailbox and audit events for mailbox reads, search activity, inbox rule creation, forwarding, or message sending.
- Check collaboration workloads for file downloads, sharing changes, or unusual consent.
- Look for role assignment, group membership changes, or privileged app consent.

## 4. Containment
- Revoke sessions once the suspicious activity is scoped.
- Reset the password if compromise is confirmed or suspected.
- Disable or block the account if active abuse is continuing.
- Remove malicious rules, forwarding, and unauthorized app consent.

## 5. Evidence to preserve
- Suspicious IPs, user agents, device IDs, session IDs, and timestamps.
- Mailbox rule definitions and forwarding targets.
- Any delegated permissions, app consent, or group/role changes.
- The exact reason the event was marked TP or FP.
