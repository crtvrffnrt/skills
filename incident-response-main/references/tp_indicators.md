# True Positive Indicators

Use this reference when deciding whether a Microsoft alert is a real incident or likely noise.

## Identity
- Impossible travel with successful sign-ins from geographically distant locations in a short interval.
- Unfamiliar properties such as a new device, browser, ASN, or geo for the user.
- Risky sign-ins, leaked credentials, or repeated MFA prompts followed by success.
- Session reuse from an unexpected IP after a normal interactive sign-in.

## Mailbox and collaboration
- New inbox rules that delete, hide, forward, or move messages away from the inbox.
- External forwarding enabled on the mailbox or transport rules that redirect mail.
- Mail access followed by suspicious sent items, mass search, or unusual mailbox traversal.
- New OAuth consent, app registration, or privilege grant that the user did not approve.

## Endpoint
- Office or browser processes spawning script engines, LOLBins, or encoded commands.
- Persistence through Run keys, services, scheduled tasks, startup folders, or WMI consumers.
- Network beacons to rare domains, cloud VPS hosts, or non-standard ports.
- File execution from user-writable paths such as `TEMP`, `APPDATA`, or public folders.

## Common false positives
- VPN, proxy, or roaming mobile network changes that match approved user behavior.
- Administrative scripts, software deployment, or vulnerability scanner activity.
- Known corporate sync tools or sanctioned mailbox forwarding rules.
- Device changes that align with reset, reimage, or enrollment activity.
