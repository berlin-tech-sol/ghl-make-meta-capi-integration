"""Send one test Lead event straight to the Meta Conversions API.

Use it to check a dataset and access token without Make. If this works but
the Make scenario fails, the problem is in Make's connection.

Setup:
    1. Events Manager -> your dataset -> Settings -> Conversions API ->
       Generate access token.
    2. Copy .env.example to .env and fill in the values, or export them.
    3. python scripts/send_test_event.py --email you@example.com --phone +923001234567

Needs Python 3.8+ and no extra packages.
"""

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request


def load_env(path=".env"):
    """Read KEY=VALUE lines from a .env file into os.environ if present."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def sha256(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalize_phone(phone):
    """Meta wants digits only, including the country code."""
    return "".join(ch for ch in phone if ch.isdigit())


def build_event(args):
    now = int(time.time())
    user_data = {
        "em": [sha256(args.email.strip().lower())],
        "ph": [sha256(normalize_phone(args.phone))],
    }
    if args.first_name:
        user_data["fn"] = [sha256(args.first_name.strip().lower())]
    if args.last_name:
        user_data["ln"] = [sha256(args.last_name.strip().lower())]

    return {
        "event_name": "Lead",
        "event_time": now,
        "event_id": f"script-test-{now}",
        "action_source": "website",
        "event_source_url": args.source_url,
        "user_data": user_data,
    }


def main():
    load_env()

    parser = argparse.ArgumentParser(description="Send a test Lead to the Meta Conversions API")
    parser.add_argument("--email", required=True)
    parser.add_argument("--phone", required=True, help="With country code, e.g. +923001234567")
    parser.add_argument("--first-name", default="")
    parser.add_argument("--last-name", default="")
    parser.add_argument("--source-url", default=os.environ.get("EVENT_SOURCE_URL", "https://example.com/form"))
    args = parser.parse_args()

    dataset_id = os.environ.get("META_DATASET_ID")
    token = os.environ.get("META_ACCESS_TOKEN")
    test_code = os.environ.get("META_TEST_EVENT_CODE")
    api_version = os.environ.get("GRAPH_API_VERSION")

    missing = [name for name, val in [
        ("META_DATASET_ID", dataset_id),
        ("META_ACCESS_TOKEN", token),
        ("GRAPH_API_VERSION", api_version),
    ] if not val]
    if missing:
        sys.exit(f"Missing settings: {', '.join(missing)}. See .env.example.")

    payload = {"data": [build_event(args)]}
    if test_code:
        payload["test_event_code"] = test_code

    url = f"https://graph.facebook.com/{api_version}/{dataset_id}/events?access_token={token}"
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            print(json.dumps(json.load(response), indent=2))
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", errors="replace")
        print(f"HTTP {err.code}")
        print(body)
        if '"code":190' in body.replace(" ", ""):
            print("\nError 190: the access token is invalid, expired or revoked. "
                  "Generate a new one in Events Manager.")
        sys.exit(1)


if __name__ == "__main__":
    main()
