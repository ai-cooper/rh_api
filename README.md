# rh_case_subject.py

Fetch Red Hat support case subjects by case number using the Red Hat Support API v3.

## Prerequisites

- Python 3.6+
- A Red Hat offline API token (generate at https://access.redhat.com/management/api)

No external dependencies required (stdlib only).

## Setup

1. Generate an offline token at https://access.redhat.com/management/api
2. Set the environment variable:
   ```bash
   export RH_OFFLINE_TOKEN='your_offline_token_here'
   ```
   Add this line to your `~/.zshrc` or `~/.bashrc` to persist across sessions.

3. Make the script executable:
   ```bash
   chmod +x rh_case_subject.py
   ```

## Usage

```
./rh_case_subject.py [OPTIONS] CASE_NUMBER [CASE_NUMBER ...]
```

### Options

| Option | Description |
|--------|-------------|
| `--token`, `-t` | Red Hat offline token (overrides `RH_OFFLINE_TOKEN` env var) |
| `--full`, `-f` | Show full case details as JSON |
| `--fields FIELD1,FIELD2,...` | Show specific fields (comma-separated, see [Available Fields](#available-fields)) |

### Examples

Fetch a single case subject:
```bash
./rh_case_subject.py 01234567
```

Fetch multiple cases:
```bash
./rh_case_subject.py 01234567 02345678 03456789
```

Show specific fields alongside the subject:
```bash
./rh_case_subject.py --fields status,severity,product,isClosed 01234567
```

Show full case details as JSON:
```bash
./rh_case_subject.py --full 01234567
```

Provide token directly:
```bash
./rh_case_subject.py --token 'your_token' 01234567
```

## How It Works

1. Exchanges the offline token for a short-lived access token via Red Hat SSO (`sso.redhat.com`)
2. Queries the Red Hat Support API v3 (`api.access.redhat.com/support/v3/cases`) for each case number
3. Displays the case subject (and optional fields) to stdout

## Output Format

Default output:
```
01234567: Case subject text here
```

With `--fields`:
```
01234567: Case subject text here  (status=Waiting on Red Hat, severity=2 (High), product=Red Hat Enterprise Linux, isClosed=False)
```

With `--full`: full JSON response from the API.

## Available Fields

Common fields returned by the v3 API that can be used with `--fields`:

| Field | Example Value |
|-------|---------------|
| `status` | `Waiting on Customer Action Required` |
| `isClosed` | `False` |
| `severity` | `4 (Low)` |
| `product` | `OpenShift Container Platform 4.20` |
| `version` | `4.20` |
| `caseType` | `Defect / Bug` |
| `createdDate` | `2026-09-17T04:57:45.000+0000` |
| `lastModifiedDate` | `2026-10-05T01:11:09.000+0000` |
| `contactName` | *(contact name)* |
| `ownerId` | *(case owner name)* |

**Note:** The v3 API does not provide an `internalStatus` field. Only `status` and `isClosed` are available for case status tracking.

Use `--full` to see all available fields for a given case.

## Notes

- The script uses the v3 API endpoint, which returns accurate case status. The v1 endpoint is known to return stale status values.
- The v3 API does **not** have an `internalStatus` field — use `status` and `isClosed` instead.
- The offline token is long-lived but can be revoked and regenerated at https://access.redhat.com/management/api.
- You must have access to the case in your Red Hat account to retrieve its details.
