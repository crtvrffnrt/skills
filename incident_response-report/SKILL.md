# Incident Response Report Skill (incident_reponse-report)

## Mission
To produce high-fidelity, professional, and visually consistent Post-Compromise Incident Reports. This skill ensures every report follows the Senior SOC Analyst and Incident Responders standard, providing a clear narrative from initial access to full containment.

## Operating Style
- **Tone:** Professional, direct, senior-level SOC analysis.
- **Priority:** High-signal technical evidence (KQL/Audit) and actionable remediation.
- **Structure:** Modular, allowing for licensing-dependent depth.

## Visual Formatting Standard
Use consistent blocks and emojis for readability:
- 🛡️ **Executive Summary**
- 📊 **Incident Classification**
- 👤 **Involved Entities**
- ⏳ **Timeline (UTC+X)**
- 🕵️ **Detailed Analysis**
- 🛠️ **Actions Taken**
- 📝 **Recommendations**
- ⚠️ **Limitations**

---

## Report Template (Drafting Workflow)

### 1. Executive Summary (Zusammenfassung)
*A 1-2 paragraph summary of the incident, impact, and current status.*

### 2. Incident Classification & Scope
| Category | Value |
| :--- | :--- |
| **Severity** | ☒ High / ☐ Medium / ☐ Low |
| **Involved Users** | `user@domain.com` |
| **Permissions** | e.g., Standard User, AVD Access, Global Admin |
| **Status** | Resolved / Ongoing |

### 3. Timeline (UTC+X)
*Ordered chronologically (Earliest to Latest).*
- **[Timestamp]** - **Initial Access:** Vector identified (e.g., AiTM Phishing).
- **[Timestamp]** - **Persistence:** MFA Registered / Inbox Rule created.
- **[Timestamp]** - **Action on Objectives:** Malicious emails sent / Files accessed.
- **[Timestamp]** - **Containment:** Password reset / Sessions revoked.

### 4. Technical Deep Dive
#### Identity & MFA Analysis
- **Source IPs:** List malicious IPs with reputation (e.g., ExpressVPN).
- **MFA Methods:** Documentation of unauthorized methods (e.g., Authenticator, SMS).
- **Token Correlation:** Evidence of AiTM/Token-Replay using `SessionId` and `UniqueTokenIdentifier`.

#### Mail & Collaboration
- **Inbox Rules:** Configuration details (e.g., "Move to Conversation History").
- **Exfiltration/Outbound:** Recipient counts, subject lines, and volume of data.
- **SPO/OneDrive/Teams:** List of accessed/downloaded files (or "Worst-Case" if logs are absent).

### 5. Containment & Remediation (Actions Taken)
*Detailed list of actions performed by the analyst or technician.*
- [Timestamp] Account Disabled.
- [Timestamp] Sessions Revoked (including MFA).
- [Timestamp] Malicious Rules/MFA Methods removed.

### 6. Limitations (Einschränkungen)
*Document missing telemetry.*
- e.g., "Entra ID P1 license limits sign-in log retention to 30 days."
- e.g., "Lack of Defender for Office 365 P2 prevents Advanced Hunting URL click analysis."

### 7. Recommendations (Empfehlungen)
- **Identity:** Conditional Access (CA), MFA enforcement, Token Protection.
- **Email:** Safe Links, Safe Attachments, Phishing Simulation.
- **Governance:** User awareness training on lookalike domains.

---

## Technical Procedures: AiTM & Token Analysis
When analyzing suspected Session Hijacking (AiTM):
1. **Identify suspicious Sign-In:** Check for unusual IPs/Countries.
2. **Extract Identifiers:**
   - `SessionId` (sid): Links interactive sessions.
   - `UniqueTokenIdentifier` (uti): Fingerprint for a specific token.
3. **Correlate across Workloads:**
   - Map `SessionId` from Sign-In logs to `AppAccessContext.AADSessionId` in Audit logs (SharePoint/Exchange).
   - **Evidence of Replay:** Same `UniqueTokenIdentifier` seen from different IP ranges or User-Agents.

## KQL Patterns for Correlation
```kql
// Correlate Sign-In with Office Activity via SessionId
let targetSession = "YOUR_SESSION_ID_HERE";
OfficeActivity
| where AppAccessContext has targetSession
| project TimeGenerated, Operation, ClientIP, UserId, OfficeWorkload, AppAccessContext
| sort by TimeGenerated asc
```

## Quality Checklist
- [ ] Timeline is in chronological order.
- [ ] Timezone is explicitly stated.
- [ ] External IPs are enriched with reputation data.
- [ ] Worst-case assumptions are clearly marked where logs are missing.
- [ ] All remediation steps include precise timestamps.
- [ ] Report is signed by a SOC Manager before delivery.
