# Agent Skills

<p align="center">
  <img src="logo.png" alt="Agent Skills logo" width="360">
</p>

<p align="center">
  <strong>Reusable Agent Skills for defensive incident response, authorized security assessment,Penetration Tests, Azure operations and security research workflows.</strong>
</p>

<p align="center">
  <a href="https://github.com/crtvrffnrt/skills"><img src="https://img.shields.io/badge/Skills-crtvrffnrt%2Fskills-2563EB?style=for-the-badge" alt="Skills repository"></a>
  <a href="https://github.com/crtvrffnrt/AGENTS.md"><img src="https://img.shields.io/badge/Profiles-AGENTS.md-111827?style=for-the-badge" alt="AGENTS.md profiles"></a>
  <a href="https://agentskills.io/"><img src="https://img.shields.io/badge/Format-Agent%20Skills-0F766E?style=for-the-badge" alt="Agent Skills format"></a>
</p>

This repository contains task-specific `SKILL.md` instructions for AI coding agents. The skills are designed to pair with the instruction profiles in [`crtvrffnrt/AGENTS.md`](https://github.com/crtvrffnrt/AGENTS.md), but they can also be installed independently in agents that support the [Agent Skills](https://agentskills.io/) format.

The goal is predictable routing: a broad profile such as `AGENTS-CORE-BLUE.md` or `AGENTS-CORE-RED.md` defines the operating posture, then the matching skill provides the focused workflow, evidence standard, tool usage, and output shape for the current task.

## Intro

The repository is organized around two main work modes:

- **Incident response skills** support defensive Microsoft security investigations, BEC and AiTM analysis, public-IP enrichment, and report writing.
- **Pentest skills** support authorized security assessment workflows from reconnaissance through validation, exploit proof, and final reporting.

Several helper skills provide environment-specific execution or research support:

- **Azure/Microsoft operator support** through the current Azure CLI session.
- **HTB and lab support** for private training environments.
- **HackTricks and CVE research support** for targeted methodology and vulnerability intelligence lookups.

Use the skills as specialized modules. Do not load every skill at once unless the agent runtime handles skill routing automatically.

## Skill Map

### Incident Response Skills

| Skill | Purpose | Typical inputs | Key dependencies |
| --- | --- | --- | --- |
| `incident-response-main` | General IR triage for Microsoft Entra ID, Microsoft 365, Defender, identity, mailbox, endpoint, and mixed incidents | UPN, host, alert ID, incident ID, UTC time window, exported logs | `az rest`, Microsoft telemetry, `vpnchecker.sh`, `ipir.sh`, optional `scripts/extract_entities.py` |
| `incident-response-bec` | BEC, AiTM, session theft, mailbox abuse, suspicious forwarding, OAuth consent, and secondary phishing analysis | UPN, incident window, sign-in evidence, mailbox evidence, phishing message IDs | Microsoft Graph or equivalent mailbox telemetry, `vpnchecker.sh`, `ipir.sh` |
| `incident-response-report` | Decision-ready incident report, timeline, containment record, remediation plan, and executive handoff | Mature investigation notes, timeline, confirmed facts, IoCs, containment actions | Prior enrichment and telemetry collection from IR workflow |

### Pentest Skills

| Skill | Purpose | Typical inputs | Relationship |
| --- | --- | --- | --- |
| `pentest-recon-surface-analysis` | Reconnaissance, endpoint discovery, asset inventory, service mapping, and control-plane surface analysis | Target scope, domains, hosts, URLs, auth state | Usually first phase; hands precise targets to mapper, authz, input, XSS, or CVE skills |
| `pentest-web-application-logic-mapper` | Workflow mapping, hidden API discovery, and state-machine analysis | Crawl data, API docs, workflow descriptions | Bridges recon into business-logic or access-control testing |
| `pentest-authentication-authorization-review` | Authentication, session, token, MFA, IDOR, BOLA, BFLA, privilege, and tenant isolation review | Role matrix, session tokens, resource IDs, expected permissions | Core auth/authz validator; overlaps with advanced access-control auditor |
| `pentest-advanced-access-control-auditor` | Focused authorization failure analysis for IDOR, BFLA, vertical and horizontal privilege escalation | Target URL, role matrix, resource map | Specialized access-control workflow; currently stored as `SKILLS.md` instead of strict `SKILL.md` |
| `pentest-input-protocol-manipulation` | Injection, parser differential testing, request smuggling, method tampering, header confusion, and payload mutation | Requests, parsers, protocol surfaces, payload hypotheses | Use when the primary question is input handling, not business logic or authz |
| `pentest-xss` | Reflected, stored, DOM, blind XSS, CSP bypass, WAF bypass, and payload context analysis | URLs, parameters, headers, proxy traffic, browser evidence | Uses OOB skill when blind XSS needs callback proof |
| `pentest-business-logic-abuse` | Workflow bypass, race condition, replay, quota abuse, state transition, and delegated execution testing | Workflow model, state transitions, reversible test sequence | Use after mapper or recon identifies a meaningful workflow |
| `pentest-outbound-interaction-oob-detection` | SSRF callbacks, blind XSS beacons, XXE/OOB, webhook delivery, DNS/HTTP callback correlation | Hypothesis, payload vector, callback listener, timing window | Evidence helper for blind or asynchronous findings |
| `pentest-cve-vulnerability-research-helper` | CVE lookup, exploit maturity, affected product validation, and applicability analysis | CVE IDs, product names, versions, CPE guesses, exploit artifacts | Research phase; informs validation and exploit planning |
| `pentest-exploit-execution-payload-control` | Deterministic exploit execution from already validated primitives | Confirmed primitive, preconditions, payload goal, safety guardrails | Late phase only; proves impact with bounded execution |
| `pentest-evidence-structuring-report-synthesis` | Evidence deduplication, severity ranking, remediation, executive summary, and final deliverables | Confirmed findings, proof artifacts, impact notes | Final phase; does not perform live testing |

### Operator and Research Helpers

| Skill | Purpose | Typical dependencies |
| --- | --- | --- |
| `pentest-gemini-az` | Azure, Microsoft 365, Microsoft Graph, and Entra operator workflow using the current Azure CLI login context | Azure CLI, active `az login`, `az rest` |
| `pentest-htb-lab-specialist` | Hack The Box, CTF, and private lab workflows from recon to foothold and privilege escalation | Lab target, private scope, standard local testing tools |
| `pentest-hacktricks-finder` | Targeted HackTricks lookup for payloads, bypasses, techniques, prerequisites, and caveats | Web search, access to `book.hacktricks.wiki` |

## Relationship To AGENTS.md

This repository is the companion skill layer for the instruction profiles in `crtvrffnrt/AGENTS.md`.

| AGENTS.md profile | Recommended skills |
| --- | --- |
| `AGENTS-CORE-BLUE.md` | `incident-response-main`, `incident-response-bec`, `incident-response-report` |
| `AGENTS-CORE-RED.md` | Pentest skills for recon, mapping, authz, input/protocol testing, XSS, OOB validation, CVE research, exploit proof, and report synthesis |
| `AGENTS-SUB-HTB.md` | `pentest-htb-lab-specialist`, plus recon, CVE, input, authz, and exploit skills as needed |
| `AGENTS-SUB-RECON.md` | `pentest-recon-surface-analysis`, `pentest-web-application-logic-mapper`, `pentest-hacktricks-finder` |
| `AGENTS-SUB-EXPLOIT.md` | `pentest-exploit-execution-payload-control`, `pentest-cve-vulnerability-research-helper`, `pentest-outbound-interaction-oob-detection` |
| `AGENTS-KQL.md` or `AGENTS-entra.md` | `incident-response-main`, `incident-response-bec`, `pentest-gemini-az` depending on whether the task is defensive investigation or Azure/Microsoft operations |

The intended routing pattern is:

1. Use the AGENTS.md profile to set the global behavior and boundaries.
2. Select one primary skill for the current phase.
3. Add a secondary skill only when it materially improves evidence handling or the next step.
4. Preserve the distinction between facts, indicators, hypotheses, and recommendations.

## Workflow Routing

### Defensive Workflow

```text
Alert or artifact
  -> incident-response-main
  -> incident-response-bec when mailbox abuse, AiTM, session theft, forwarding, or OAuth consent is central
  -> incident-response-report when the investigation is ready for handoff
```

Use `incident-response-main` as the default defensive entry point. It contains references for identity analysis, endpoint triage, true-positive indicators, a report skeleton, and the `extract_entities.py` helper.

### Authorized Assessment Workflow

```text
Scope or target
  -> pentest-recon-surface-analysis
  -> pentest-web-application-logic-mapper
  -> focused validation skill:
       auth/authz, advanced access control, input/protocol, XSS, business logic, OOB, or CVE research
  -> pentest-exploit-execution-payload-control only after a primitive is validated
  -> pentest-evidence-structuring-report-synthesis for final reporting
```

Use the narrowest validation skill that matches the actual hypothesis. For example, use `pentest-input-protocol-manipulation` for parser and request-layer behavior, but use `pentest-business-logic-abuse` for workflow state manipulation.

## Dependencies

### Skill Format

Most directories follow the standard layout:

```text
skill-name/
  SKILL.md
```

One directory currently uses a non-standard filename:

```text
pentest-advanced-access-control-auditor/
  SKILLS.md
```

If your skill installer requires strict Agent Skills layout, rename or copy that file to `SKILL.md` before packaging.

One directory also has a directory/name mismatch:

```text
pentest-gemini-sub-htb/SKILL.md
  name: pentest-htb-lab-specialist
```

Use the metadata name when the runtime routes by front matter. Use the directory name when installing or referencing the local path.

### Defensive Tooling

The incident-response skills expect these local workstation tools when public IPs are present:

```bash
/root/Tools/IncidentResponseScripts/vpnchecker.sh <ip>
/root/Tools/IncidentResponseScripts/ipir.sh <ip>
```

The repo also includes:

```bash
incident-response-main/scripts/extract_entities.py
```

That helper normalizes users, hosts, IP addresses, hashes, domains, and URLs from incident exports.

Threat-intelligence enrichment may depend on API keys stored outside this repository, commonly in:

```bash
~/Tools/apikeys.txt
```

For Microsoft cloud investigations, the skills prefer Azure CLI and Microsoft Graph through:

```bash
az account show -o json
az rest --method get --url "https://graph.microsoft.com/v1.0/..."
```

### Pentest Tooling

The pentest skills are tool-aware rather than hard-bound. Install only the tools needed for the assessment phase.

Common local tools:

```bash
curl wget git jq nmap dnsutils whois python3 python3-pip pipx golang nodejs npm chromium
ffuf feroxbuster seclists nuclei httpx-toolkit dnsx katana interactsh-client
```

Key skill-specific dependencies:

| Dependency | Used by | Notes |
| --- | --- | --- |
| `az` and `az rest` | `pentest-gemini-az`, IR skills | Requires an active Azure CLI login and correct tenant/subscription context |
| `interactsh-client` | `pentest-outbound-interaction-oob-detection`, blind XSS workflows | Required for DNS/HTTP/HTTPS callback correlation |
| `vulnx` | `pentest-cve-vulnerability-research-helper` | Requires `PDCP_API_KEY`; if unavailable, the skill falls back to web research |
| `ffuf` | `pentest-recon-surface-analysis` | Used for vhost and endpoint fuzzing examples |
| Burp Suite or another proxy | `pentest-xss` | Useful for match-and-replace payload injection and traffic evidence |
| Web search | `pentest-hacktricks-finder`, CVE helper, HTB lab skill | Required for current technique and vulnerability research |

Example base install on Kali-style systems:

```bash
sudo apt update && sudo apt install -y \
  curl wget git jq nmap dnsutils whois python3 python3-pip pipx golang nodejs npm chromium \
  ffuf feroxbuster seclists nuclei httpx-toolkit dnsx katana interactsh-client
```

Some ProjectDiscovery tools are commonly installed through `pdtm`, Go, or upstream release packages when they are not available from the OS repository.

## Install

Install the skills into an Agent Skills-compatible runtime with:

```bash
npx skills add crtvrffnrt/skills
```

For local development, clone the repository and point your agent runtime at the repository root or at individual skill directories:

```bash
git clone https://github.com/crtvrffnrt/skills.git
cd skills
```

## Repository Layout

```text
.
|-- README.md
|-- logo.png
|-- incident-response-main/
|   |-- SKILL.md
|   |-- assets/summary_report.md
|   |-- references/endpoint_triage.md
|   |-- references/identity_analysis.md
|   |-- references/tp_indicators.md
|   `-- scripts/extract_entities.py
|-- incident-response-bec/
|-- incident-response-report/
|-- pentest-*/
`-- pentest-xss/
    |-- examples/match-and-replace-examples.md
    `-- resources/blind-xss-guide.md
```

## Usage Guidance

Use one primary skill per phase:

- Start broad defensive cases with `incident-response-main`.
- Switch to `incident-response-bec` when mailbox abuse, AiTM, token replay, forwarding, or consent abuse is the central question.
- Use `incident-response-report` only when the investigation is ready to become a report.
- Start authorized assessments with `pentest-recon-surface-analysis`.
- Move to focused validation skills only after there is a concrete surface or hypothesis.
- Use `pentest-exploit-execution-payload-control` only after a vulnerability primitive is validated.
- Use `pentest-evidence-structuring-report-synthesis` for final deliverables, not live testing.

## Safety Boundaries

These skills are written for defensive operations, authorized assessments, and lab environments.

- Do not use the pentest skills against systems without explicit authorization.
- Do not run destructive payloads unless the scope explicitly permits them.
- Preserve raw evidence before containment, cleanup, or session revocation.
- Keep public-IP, CVE, and exploit conclusions tied to reproducible evidence.
- Treat missing telemetry as an investigation gap, not proof that activity is benign.

## Maintenance Notes

Keep skill changes additive and explicit. A useful skill should define:

- When it should activate.
- When it should not activate.
- Required or preferred inputs.
- Expected outputs.
- Tooling assumptions.
- Evidence standards.
- Handoff relationships to upstream or downstream skills.
