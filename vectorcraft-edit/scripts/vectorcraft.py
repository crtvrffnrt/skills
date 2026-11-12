#!/usr/bin/env python3
"""Call a live MCP tool; never fall back to a headless document."""
import json
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    binary = shutil.which("vectorcraft-cli")
    if not binary or str(Path(binary).resolve()).startswith("/tmp/"):
        raise RuntimeError("Install vectorcraft-cli persistently as described in skill.md")
    tool = sys.argv[1] if len(sys.argv) > 1 else "inspect_document"
    arguments = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {"depth": 0}
    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be a JSON object")
    messages = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {},
            "clientInfo": {"name": "local-vectorcraft", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
            "name": tool, "arguments": arguments}},
    ]
    result = subprocess.run(
        [binary, "mcp", "--connect", "127.0.0.1:7979"],
        input="".join(json.dumps(message) + "\n" for message in messages),
        capture_output=True, text=True, timeout=60,
    )
    for line in result.stdout.splitlines():
        response = json.loads(line)
        if response.get("id") == 2:
            print(json.dumps(response, indent=2))
            return int(bool(response.get("error") or response.get("result", {}).get("isError")))
    raise RuntimeError(result.stderr.strip() or "MCP server returned no tool response")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
