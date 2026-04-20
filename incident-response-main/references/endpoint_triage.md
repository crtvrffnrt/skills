# Defender for Endpoint Triage

Use this guide when the incident includes a workstation or server alert.

## 1. Confirm the alert
- Identify the parent process, child process, and command line.
- Check whether the binary is signed, expected, and launched from a normal path.
- Compare the alert time to any identity or mail activity from the same incident window.

## 2. Review behavior
- Look for script engines, LOLBins, PowerShell, WMI, scheduled tasks, services, or startup persistence.
- Check network destinations, ports, and bytes transferred.
- Inspect file drops, archive extraction, browser downloads, and suspicious child processes.
- For any material public destination IP, run `/root/Tools/IncidentResponseScripts/vpnchecker.sh <ip>` and `/root/Tools/IncidentResponseScripts/ipir.sh <ip>` and keep the raw output with the case notes.

## 3. Scope the host
- Determine whether the activity is isolated to one host or appears across multiple machines.
- Capture hashes, file paths, process trees, and notable registry or task artifacts.
- Note any signs of credential theft, lateral movement, or remote execution.

## 4. Containment
- Isolate the host if there is active malware, C2, or destructive behavior.
- Run an approved full scan and collect live response artifacts when available.
- Remove malicious persistence only after evidence is captured.

## 5. Remediation
- Patch the host, remove malicious files, and validate that persistence is gone.
- Reimage if the compromise is extensive or confidence in cleanup is low.
- Document whether the alert was a true positive, a benign admin action, or a false positive.
