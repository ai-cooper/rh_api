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
| `--fields FIELD1,FIELD2,...` | Show specific fields (comma-separated) |

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
./rh_case_subject.py --fields status,severity,product 01234567
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
01234567: Case subject text here  (status=Waiting on Red Hat, severity=2 (High), product=Red Hat Enterprise Linux)
```

With `--full`: full JSON response from the API.

## Notes

- The script uses the v3 API endpoint, which returns accurate case status. The v1 endpoint is known to return stale status values.
- The offline token is long-lived but can be revoked and regenerated at https://access.redhat.com/management/api.
- You must have access to the case in your Red Hat account to retrieve its details.
