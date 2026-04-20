# Agent Skills

A collection of offensive, defensive, and trading skills for AI coding agents.

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Available Trading Skills (NeonTrade)

- **ib_trade-osint**: OSINT intelligence cycle and prefilter.
- **ib_trade-analysis**: AI-supercycle stock analysis and strategy.
- **ib_trade-execution**: Risk and trade execution.

## Available Pentest Skills

- **pentest-authentication-authorization-review**: Security assessment skill for authentication and authorization controls.
- **pentest-business-logic-abuse**: Security assessment skill for business workflow abuse and state-machine flaws.
- **pentest-evidence-structuring-report-synthesis**: Security assessment skill for structuring evidence and producing decision-ready reports.
- **pentest-exploit-execution-payload-control**: Security assessment skill for deterministic exploit execution from validated primitives.
- **pentest-gemini-az**: Azure, Microsoft 365, and Entra ID companion that uses the current Azure CLI session.
- **pentest-gemini-sub-htb**: Hack The Box compromise workflows from recon to privilege escalation.
- **pentest-input-protocol-manipulation**: Security assessment skill for input validation abuse and protocol-level manipulation.
- **pentest-outbound-interaction-oob-detection**: Security assessment skill for outbound interaction and out-of-band validation.
- **pentest-recon-surface-analysis**: Security assessment skill for reconnaissance and attack-surface mapping.

## Available Incident Response Skills

- **incident-response-main**: Defensive incident-response companion for Entra ID, Microsoft 365, Defender, mixed identity or endpoint incidents, sign-in triage, and public-IP enrichment.
- **incident-response-bec**: BEC and AiTM analysis for mailbox abuse, forwarding, token theft, and secondary phishing.
- **incident-response-report**: Decision-ready incident report drafting and post-compromise writeups.

## Usage

Each skill is a directory containing a `SKILL.md` file that defines its behavior, triggers, and instructions. These can be used by AI agents to perform specialized tasks in a structured and reproducible manner.
