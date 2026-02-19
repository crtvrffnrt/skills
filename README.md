# Agent Skills

A nice collection of offensive skills for AI coding agents. Skills are instructions and scripts and stuff that extend agent capabilities.

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Available Pentest Skills

- **pentest-authentication-authorization-review**: Security assessment skill for authentication and authorization controls. Use when prompts include session handling, token abuse, MFA weaknesses, account takeover, IDOR/BOLA/BFLA, privilege escalation, tenant isolation, or identity boundary validation.
- **pentest-business-logic-abuse**: Security assessment skill for business workflow abuse, state-machine manipulation, and control-plane logic flaws. Use when prompts include workflow bypass, race condition, replay, quota abuse, order-of-operations flaws, delegated execution abuse, or unauthorized state transitions.
- **pentest-evidence-structuring-report-synthesis**: Security assessment skill for structuring evidence, deduplicating findings, and producing decision-ready security reports. Use when prompts include write report, consolidate findings, severity ranking, remediation guidance, executive summary, or technical appendix generation.
- **pentest-exploit-execution-payload-control**: Security assessment skill for deterministic exploit execution from validated primitives. Use when prompts include exploit implementation, payload hardening, chaining confirmed weaknesses, post-exploitation proof, or controlled impact demonstration.
- **pentest-gemini-az**: Use when users need an Azure, Microsoft 365, or Entra ID companion that reads, lists, changes, and manages resources using the current Azure CLI session, with `az rest` as the default execution path.
- **pentest-gemini-sub-htb**: Use when users ask for Hack The Box machine compromise workflows from recon to foothold and privilege escalation.
- **pentest-input-protocol-manipulation**: Security assessment skill for input validation abuse and protocol-level manipulation. Use when prompts include injection, parser differential testing, request smuggling, method tampering, header confusion, serialization abuse, or payload mutation for exploitability testing.
- **pentest-outbound-interaction-oob-detection**: Security assessment skill for outbound interaction and out-of-band (OOB) validation. Use when prompts include SSRF callback confirmation, blind XSS beacons, webhook abuse, XXE/OOB behavior, DNS/HTTP callback correlation, or asynchronous server-side interaction proof.
- **pentest-recon-surface-analysis**: Security assessment skill for reconnaissance, endpoint/service enumeration, and attack-surface mapping. Use when prompts include recon, enumerate, map endpoints, discover assets, inventory interfaces, fingerprint technologies, or identify control-plane surfaces.

## Usage

Each skill is a directory containing a `SKILL.md` file that defines its behavior, triggers, and instructions. These can be used by AI agents to perform specialized tasks in a structured and reproducible manner.
