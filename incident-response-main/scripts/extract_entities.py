#!/usr/bin/env python3
"""Extract common entities from Microsoft incident exports."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

EMAIL_RE = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}\b")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
URL_RE = re.compile(r"\bhttps?://[^\s\"'<>]+", re.IGNORECASE)
HASH_RE = {
    "MD5": re.compile(r"\b[a-fA-F0-9]{32}\b"),
    "SHA1": re.compile(r"\b[a-fA-F0-9]{40}\b"),
    "SHA256": re.compile(r"\b[a-fA-F0-9]{64}\b"),
}

USER_KEYS = ("user", "account", "upn", "principalname", "mail")
HOST_KEYS = ("host", "computer", "device", "machine", "hostname")


def add_if_present(target, value):
    if value is None:
        return
    text = str(value).strip()
    if text:
        target.add(text)


def extract_from_text(text, entities):
    for email in EMAIL_RE.findall(text):
        entities["Users"].add(email)
        entities["Domains"].add(email.split("@", 1)[1].lower())

    for ip in IP_RE.findall(text):
        entities["IPs"].add(ip)

    for label, pattern in HASH_RE.items():
        for match in pattern.findall(text):
            entities["Hashes"].add(match.lower())

    for url in URL_RE.findall(text):
        entities["URLs"].add(url)
        parsed = urlparse(url)
        if parsed.hostname:
            entities["Domains"].add(parsed.hostname.lower())


def extract_from_value(key, value, entities):
    lowered = (key or "").lower()

    if isinstance(value, str):
        if any(token in lowered for token in USER_KEYS):
            add_if_present(entities["Users"], value)
        if any(token in lowered for token in HOST_KEYS):
            add_if_present(entities["Hosts"], value)
        extract_from_text(value, entities)
    elif isinstance(value, (int, float, bool)):
        return
    elif isinstance(value, list):
        for item in value:
            extract_from_value(key, item, entities)
    elif isinstance(value, dict):
        for child_key, child_value in value.items():
            extract_from_value(child_key, child_value, entities)


def extract_entities_from_json(data):
    entities = defaultdict(set)
    for key in ("Users", "Hosts", "IPs", "Hashes", "Domains", "URLs"):
        entities[key]
    extract_from_value(None, data, entities)
    return {key: sorted(values) for key, values in entities.items() if values}


def extract_entities_from_csv(file_path):
    entities = defaultdict(set)
    for key in ("Users", "Hosts", "IPs", "Hashes", "Domains", "URLs"):
        entities[key]
    with open(file_path, mode="r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            for key, value in row.items():
                extract_from_value(key, value, entities)
    return {key: sorted(values) for key, values in entities.items() if values}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file_path", help="JSON or CSV export to inspect")
    args = parser.parse_args()

    path = Path(args.file_path)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    if path.suffix.lower() == ".json":
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        results = extract_entities_from_json(data)
    elif path.suffix.lower() == ".csv":
        results = extract_entities_from_csv(path)
    else:
        print("Unsupported file format. Please use .json or .csv.", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
