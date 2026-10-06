#!/usr/bin/env python3
"""Fetch Red Hat support case subject(s) by case number(s) via the Red Hat API."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error

TOKEN_URL = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token"
CASE_API_URL = "https://api.access.redhat.com/support/v3/cases"
ENV_VAR = "RH_OFFLINE_TOKEN"


def get_access_token(offline_token):
    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "client_id": "rhsm-api",
        "refresh_token": offline_token,
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data)
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
        return result["access_token"]
    except urllib.error.HTTPError as e:
        print(f"Error: Failed to obtain access token: {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)
    except KeyError:
        print("Error: Unexpected token response — 'access_token' not found.", file=sys.stderr)
        sys.exit(1)


def fetch_case(token, case_number):
    url = f"{CASE_API_URL}/{case_number}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": f"{e.code} {e.reason}"}


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Red Hat support case subject by case number.",
        epilog=f"Set {ENV_VAR} env var or use --token to provide your offline token.",
    )
    parser.add_argument("cases", nargs="+", metavar="CASE_NUMBER",
                        help="One or more case numbers (e.g. 01234567)")
    parser.add_argument("--token", "-t", default=None,
                        help="Red Hat offline token (or set RH_OFFLINE_TOKEN env var)")
    parser.add_argument("--full", "-f", action="store_true",
                        help="Show full case details (JSON)")
    parser.add_argument("--fields", default=None,
                        metavar="FIELD1,FIELD2,...",
                        help="Comma-separated fields to display "
                             "(e.g. status,severity,product,isClosed,caseType)")
    args = parser.parse_args()

    offline_token = args.token or os.environ.get(ENV_VAR)
    if not offline_token:
        print(f"Error: Provide offline token via --token or {ENV_VAR} env var.", file=sys.stderr)
        print(f"Generate one at: https://access.redhat.com/management/api", file=sys.stderr)
        sys.exit(1)

    access_token = get_access_token(offline_token)

    for case_number in args.cases:
        data = fetch_case(access_token, case_number)

        if "error" in data:
            print(f"{case_number}: ERROR — {data['error']}")
            continue

        if args.full:
            print(json.dumps(data, indent=2, ensure_ascii=False))
            continue

        summary = data.get("summary", "N/A")
        output = f"{case_number}: {summary}"

        if args.fields:
            extras = []
            for field in args.fields.split(","):
                val = data.get(field, "N/A")
                extras.append(f"{field}={val}")
            output += f"  ({', '.join(extras)})"

        print(output)


if __name__ == "__main__":
    main()
