---
name: incident_response-bec
description: "Blue teaming skill for analyzing a compromised user hit by a Business Email Compromise (BEC) resulting from an AiTM (Adversary-in-the-Middle) phishing attack. Focuses on identifying malicious sign-ins, unauthorized mailbox rules, data exfiltration, and secondary phishing attempts. Requires a User Principal Name (UPN)."
---

# Business Email Compromise (BEC) & AiTM Analysis

This skill is designed for incident responders to analyze a user account suspected of being compromised via an Adversary-in-the-Middle (AiTM) phishing attack. These attacks often bypass MFA by stealing session cookies, leading to unauthorized mailbox access and further malicious activity.

## Activation Triggers (Positive)
- `bec`
- `business email compromise`
- `aitm`
- `adversary-in-the-middle`
- `phishing investigation`
- `compromised user`
- `unauthorized mail forwarding`
- `suspicious sign-in`

## Exclusion Triggers (Negative)
- `pentest`
- `exploit development`
- `vulnerability research`
- `network service scan`

## Instructions
1. **Identify the Target**: Ensure you have the User Principal Name (UPN) of the affected user. All following commands require this.
2. **Verify Session**: Confirm you are logged in with an account that has sufficient permissions (e.g., Global Reader, Security Reader) using `az account show`.
3. **Analyze Sign-in Logs**: Use `az rest` to query Microsoft Graph for recent sign-ins for the UPN. Look for unusual IP addresses, locations, or "MFA satisfied by claim in token" from new locations.
   ```bash
   az rest --method get --url "https://graph.microsoft.com/v1.0/auditLogs/signIns?\$filter=userPrincipalName eq '{UPN}'"
   ```
4. **Audit Mailbox Rules**: Check for newly created or suspicious inbox rules (e.g., "Delete" or "Move to RSS Feed") often used by attackers to hide their activity.
   ```bash
   az rest --method get --url "https://graph.microsoft.com/v1.0/users/{UPN}/mailFolders/inbox/messageRules"
   ```
5. **Trace Sent Items**: Identify if the attacker sent further phishing emails or exfiltrated data by checking the user's sent items.
   ```bash
   az rest --method get --url "https://graph.microsoft.com/v1.0/users/{UPN}/messages?\$filter=isDraft eq false"
   ```
6. **Check Forwarding Addresses**: Verify if the attacker enabled SMTP forwarding to an external address.
   ```bash
   az rest --method get --url "https://graph.microsoft.com/v1.0/users/{UPN}/mailboxSettings"
   ```

## Tip 1: Detecting AiTM Session Theft
In AiTM attacks, the attacker proxies the authentication process. Look for sign-ins where the `User-Agent` is consistent but the `IP Address` changes mid-session, or where the sign-in location is a known VPN/Cloud provider (like DigitalOcean, AWS, or Azure) while the user normally signs in from a residential/corporate range.

## Should Do
- Use the `az rest` command to interact directly with Microsoft Graph APIs for granular data.
- Correlate the timing of the suspected phishing email with the first "unusual" sign-in.
- Document all suspicious IP addresses and forwarding rules discovered.
- Always check for "MailItemsAccessed" events if Log Analytics is available for more detailed exfiltration analysis.

## Should Not Do
- Do not assume MFA means the account is safe; AiTM attacks specifically target MFA-protected accounts.
- Do not alert the user until the initial scoping is complete to avoid tipping off the attacker.
- Do not rely solely on the "Last Signed In" date; audit the full log for concurrent sessions.
