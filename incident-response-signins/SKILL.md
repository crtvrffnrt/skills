# SKILL: incident-response-signins

## PURPOSE

Analyze Microsoft Entra ID interactive and non-interactive sign-in logs to determine whether there is evidence of user account compromise.

This skill performs structured, evidence-based identity threat detection using normalized log analysis, behavioral baselining, and correlation logic across authentication events.

---

## INPUTS

The skill expects two log files in the working directory:

- interactive_signins.json
- noninteractive_signins.json

Both must be exported from Microsoft Entra ID Sign-In Logs.

---

## OBJECTIVE

Determine whether a user account shows evidence of compromise.

All conclusions must be:
- Evidence-based
- Log-supported
- Explicitly classified by confidence level

---

## EXECUTION MODEL

### STEP 1 — INGESTION & NORMALIZATION

Parse both datasets and normalize into a unified schema:

- TimeGenerated
- UserPrincipalName
- AppDisplayName
- IPAddress
- Location (Country, City)
- ClientAppUsed
- DeviceDetail (OS, Browser, DeviceId)
- ConditionalAccessStatus
- Status (Success / Failure + ErrorCode)
- RiskLevelDuringSignIn
- RiskState
- AuthenticationRequirement

Tag each record:
- Interactive
- NonInteractive

---

### STEP 2 — BASELINE CONSTRUCTION

For each user:

Establish behavioral baseline:
- Known IP ranges / ASN / Geo
- Typical devices and user agents
- Common applications
- Normal sign-in time patterns

Mark deviations from baseline.

---

### STEP 3 — DETECTION LOGIC

Evaluate the following detection categories:

#### A. Geographic Anomalies
- Impossible travel (time-distance violation)
- First-time country or region
- High-risk geolocation (TOR, VPS, anonymizers)

#### B. IP Patterns
- Hosting provider / VPN IPs
- Shared IP across multiple users
- Burst authentication patterns

#### C. Authentication Anomalies
- Multiple failed logins followed by success
- Error codes:
  - 50126 (invalid credentials)
  - 50053 (account locked)
- Success after brute-force pattern

#### D. Non-Interactive Abuse
- Sudden spike in non-interactive logins
- Access via unfamiliar apps (Graph API, PowerShell)
- Legacy authentication usage

#### E. Device / Client Anomalies
- Unknown device identifiers
- Suspicious user agents
- New OS / browser combinations

#### F. Conditional Access / MFA
- Missing MFA where expected
- Conditional Access not applied
- Token issuance without strong authentication

#### G. Risk Signals
- Elevated RiskLevelDuringSignIn
- Risk detections:
  - Anonymous IP
  - Atypical travel
  - Malware-linked IP

---

### STEP 4 — CORRELATION

Correlate across both datasets:

- Failed interactive → successful non-interactive
- Token reuse patterns
- Session chaining or persistence behavior

---

### STEP 5 — TIMELINE GENERATION

For each suspicious user:

Construct a timeline:
- First anomaly
- Escalation events
- Last observed activity

Highlight pivot points.

---

### STEP 6 — CLASSIFICATION

Assign one of the following:

- CONFIRMED_COMPROMISE
- HIGHLY_SUSPICIOUS
- BENIGN

Each classification must include justification.

---

### STEP 7 — OUTPUT

Generate structured HTML report.

#### Required Sections:

1. Executive Summary
2. Scope & Data Sources
3. Key Findings (per user)
4. Timeline of Suspicious Activity
5. Indicators of Compromise (IoCs)
6. Behavioral Deviations
7. Confidence Assessment
8. Appendix (Raw Events)

---

## CONSTRAINTS

- No speculation without log evidence
- Clearly separate anomaly vs compromise
- Highlight missing data or blind spots
- Prioritize accuracy over completeness

---

## ENRICHMENT (OPTIONAL)

- IP → ASN / Hosting provider mapping
- TOR / Proxy detection
- Geo-risk classification

---

## MITRE ATT&CK MAPPING

Map findings where applicable:

- T1078 — Valid Accounts
- T1550 — Use of Authentication Tokens
- T1110 — Brute Force

---

## OUTPUT FORMAT

Primary output:

- HTML report (default)

Optional:
- JSON structured findings
- CSV IoC export

---

## SUCCESS CRITERIA

The skill is successful if:

- Suspicious users are clearly identified
- Evidence is traceable to raw logs
- Timeline reconstruction is coherent
- Output is SOC-ready and actionable

---

## FAILURE CONDITIONS

- Missing input files
- Unparseable JSON
- Insufficient data for baseline

In such cases:
- Abort analysis
- Return structured error message

---

## NOTES

- Treat non-interactive logins as high-risk indicators when correlated with anomalies
- Emphasize token-based persistence patterns
- Prefer deterministic logic over heuristic-only scoring
