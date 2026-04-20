# SKILL: incident-response-signins

## PURPOSE

Analyze Microsoft Entra ID interactive and non-interactive sign-in logs to determine whether there is evidence of user account compromise.

This skill performs structured, evidence-based identity threat detection using normalized log analysis, behavioral baselining, and correlation logic across authentication events.
It also enriches every related public source IP with dedicated threat-intelligence tooling before assigning an IP verdict or an incident verdict.

---

## INPUTS

The skill expects two log files in the working directory:

- interactive_signins.json
- noninteractive_signins.json

Both must be exported from Microsoft Entra ID Sign-In Logs.

---

## OBJECTIVE

Determine whether a user account shows evidence of compromise.
Determine whether each related public source IP is `CLEAN`, `SUSPICIOUS`, or `MALICIOUS`.

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

### STEP 1B — PUBLIC SOURCE IP EXTRACTION

Extract all source IPs from both datasets and build a deduplicated enrichment set.

For each IP:
- Classify it as public, private, loopback, link-local, multicast, or reserved
- Exclude non-public IPs from external threat-intelligence lookups
- Preserve the full raw IP set in the report for auditability

For every unique public source IP, run both of the following local enrichment scripts before final classification:
- `/root/Tools/IncidentResponseScripts/vpnchecker.sh`
- `/root/Tools/IncidentResponseScripts/ipir.sh`

Use `vpnchecker.sh` as the fast VPN signal cross-check.
Use `ipir.sh` as the richer threat-intelligence and scoring pass.
Capture the raw outputs and the normalized fields from both tools.

Normalize the IP enrichment into a table with, at minimum:
- IPAddress
- VPN status from `vpnchecker.sh`
- VPN/provider flag from `vpnchecker.sh`
- `ipir.sh` score
- `ipir.sh` infrastructure flags
- `ipir.sh` threat-intelligence hits
- ASN / organization
- country / region
- final IP verdict

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
- Public source IPs must be enriched through both local scripts before a verdict is assigned

#### C. Public Source IP Threat Intelligence
- `vpnchecker.sh` flags showing VPN usage are strong risk indicators, but not by themselves proof of compromise
- `ipir.sh` scoring, AbuseIPDB, VirusTotal, OTX, CrowdSec, Kaspersky, ThreatFox, Hybrid Analysis, and blacklist hits should be combined into a single IP reputation assessment
- Datacenter, proxy, TOR, and mobile indicators should be treated as context for risk, not as standalone proof
- A public IP can be `CLEAN` only when both scripts return no meaningful risk and there is no supporting behavioral anomaly
- A public IP is `SUSPICIOUS` when there are one or more risk indicators but not enough evidence to call it malicious
- A public IP is `MALICIOUS` when multiple independent TI sources agree or when high-confidence malicious indicators are present

#### D. Authentication Anomalies
- Multiple failed logins followed by success
- Error codes:
  - 50126 (invalid credentials)
  - 50053 (account locked)
- Success after brute-force pattern

#### E. Non-Interactive Abuse
- Sudden spike in non-interactive logins
- Access via unfamiliar apps (Graph API, PowerShell)
- Legacy authentication usage

#### F. Device / Client Anomalies
- Unknown device identifiers
- Suspicious user agents
- New OS / browser combinations

#### G. Conditional Access / MFA
- Missing MFA where expected
- Conditional Access not applied
- Token issuance without strong authentication

#### H. Risk Signals
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

Also assign a per-public-IP verdict:
- CLEAN
- SUSPICIOUS
- MALICIOUS

IP verdicts must be justified with the combined output of `vpnchecker.sh`, `ipir.sh`, and the surrounding sign-in behavior. A VPN flag alone is not enough to call an IP malicious.

---

### STEP 7 — OUTPUT

Generate structured HTML report.

#### Required Sections:

1. Executive Summary
2. Scope & Data Sources
3. Key Findings (per user)
4. Timeline of Suspicious Activity
5. Public Source IP Threat Intel
6. Indicators of Compromise (IoCs)
7. Behavioral Deviations
8. Confidence Assessment
9. Appendix (Raw Events and Script Output)

---

## CONSTRAINTS

- No speculation without log evidence
- Clearly separate anomaly vs compromise
- Highlight missing data or blind spots
- Prioritize accuracy over completeness

---

## THREAT INTEL ENRICHMENT

- IP → ASN / Hosting provider mapping
- TOR / Proxy detection
- Geo-risk classification
- Run `vpnchecker.sh` on every unique public source IP
- Run `ipir.sh` on every unique public source IP
- Include the raw and normalized outputs from both scripts in the report
- Treat `ipir.sh` as the broader TI decision aid when deciding whether a public IP is clean, suspicious, or malicious

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
- Public source IPs are fully enriched through both local scripts
- Each public source IP receives a defensible clean / suspicious / malicious verdict
- Output is SOC-ready and actionable

---

## FAILURE CONDITIONS

- Missing input files
- Unparseable JSON
- Insufficient data for baseline
- Unable to enrich related public source IPs with the required local scripts

In such cases:
- Abort analysis
- Return structured error message

---

## NOTES

- Treat non-interactive logins as high-risk indicators when correlated with anomalies
- Emphasize token-based persistence patterns
- Prefer deterministic logic over heuristic-only scoring
