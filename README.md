# Remnawave Python SDK — fork

Asynchronous Python client for the **[Remnawave](https://remna.st)** panel API, built on
`httpx` + `pydantic` v2, with `orjson` for fast serialization.

> [!IMPORTANT]
> **This is a fork of [`remnawave/python-sdk`](https://github.com/remnawave/python-sdk).**
> It is maintained independently and is **not** published to PyPI under the `remnawave` name.
> The fork exists to track the Remnawave 2.8.x API closely and to fix the divergences that
> the migration from 2.7.x left behind — see [What this fork changes](#what-this-fork-changes).
> Attribution for the original work is at the [bottom of this file](#credits).

---

## Compatibility

| SDK version | Remnawave panel | Backend contract |
| ----------- | --------------- | ---------------- |
| 2.8.1       | >= 2.8.0        | `@remnawave/backend-contract` 2.8.35 |

Every endpoint, request body and response model in this fork is verified against
`libs/contract` of [`remnawave/backend`](https://github.com/remnawave/backend) at tag `2.8.1`.

**Requirements:** Python >= 3.11, < 3.15.

## Installation

```bash
pip install git+https://github.com/IceOne-i/remnactual.git@production
```

A specific branch or tag:

```bash
pip install "git+https://github.com/IceOne-i/remnactual.git@fix/api-2.8-compliance"
```

## Quick start

```python
import asyncio
import os

from remnawave import RemnawaveSDK
from remnawave.models import GetAllUsersResponseDto


async def main() -> None:
    sdk = RemnawaveSDK(
        # https://panel.example.com  or  http://127.0.0.1:3000
        base_url=os.environ["REMNAWAVE_BASE_URL"],
        # Bearer token from the panel: Settings -> API Tokens
        token=os.environ["REMNAWAVE_TOKEN"],
    )

    page: GetAllUsersResponseDto = await sdk.users.get_all_users(start=0, size=50)
    print(f"total: {page.total}")
    for user in page.users:
        print(user.username, user.status, user.expire_at)


asyncio.run(main())
```

The transport unwraps the API's `{"response": ...}` envelope for you, so responses are the
payload itself.

### Client options

```python
sdk = RemnawaveSDK(
    base_url="https://panel.example.com",
    token="...",
    caddy_token="...",                      # X-Api-Key when the panel sits behind Caddy
    ssl_ignore=False,                       # skip TLS verification (self-signed certs)
    custom_headers={"X-Real-IP": "1.2.3.4"},
    cookies={"session": "..."},             # reverse-proxy auth
)
```

You can also pass a pre-configured client and manage its lifetime yourself:

```python
import httpx

async with httpx.AsyncClient(
    base_url="https://panel.example.com/api",
    headers={"Authorization": "Bearer ..."},
) as client:
    sdk = RemnawaveSDK(client=client)
```

`base_url` is normalised automatically: a trailing slash is stripped and `/api` is appended
when missing.

## Controllers

| Attribute | Covers |
| --- | --- |
| `sdk.users` | CRUD, lookups by uuid/id/short-uuid/username/telegram/email/tag, actions, tags, `stream` (cursor pagination), accessible nodes |
| `sdk.users_bulk_actions` | `bulk/*` and `bulk/all/*` operations |
| `sdk.nodes` | CRUD, enable/disable/restart, reorder, reset traffic, bulk actions, tags |
| `sdk.hosts` / `sdk.hosts_bulk_actions` | CRUD, reorder, tags, bulk enable/disable/delete/update |
| `sdk.config_profiles` | Config profiles, inbounds, computed config, reorder |
| `sdk.inbounds` | Inbounds under `/config-profiles/inbounds` |
| `sdk.internal_squads` / `sdk.external_squads` | Squads, membership bulk actions, accessible nodes, reorder |
| `sdk.subscription` | Public `/sub/{shortUuid}` endpoints |
| `sdk.subscriptions` | Admin subscription lookups, raw subscription, connection keys |
| `sdk.subscriptions_settings` / `sdk.subscriptions_template` / `sdk.subscription_page_config` | Subscription settings, templates, subscription page configs |
| `sdk.subscription_request_history` | Request history and its stats |
| `sdk.hwid` | HWID devices, stats, top users |
| `sdk.ip_control` | Fetch IPs jobs, drop connections |
| `sdk.node_plugins` | Node plugins, executor, torrent-blocker reports |
| `sdk.infra_billing` | Providers, billing nodes, billing history |
| `sdk.bandwidthstats` | Per-node and per-user bandwidth stats (incl. legacy endpoints) |
| `sdk.system` | Stats, health, metrics, recap, x25519, SRR matcher |
| `sdk.auth` / `sdk.passkeys` / `sdk.api_tokens_management` | Login, OAuth2, passkeys, scoped API tokens |
| `sdk.remnawave_settings` / `sdk.snippets` / `sdk.keygen` / `sdk.metadata` | Panel settings, snippets, pubkey, user/node metadata |
| `sdk.webhook_utility` | Webhook signature validation and payload parsing |

## Request bodies and `null`

Request models are serialized with `model_dump(exclude_unset=True)`, i.e. **exactly the fields
you set are sent**. This matters in 2.8, where several fields can only be cleared by sending an
explicit `null`:

```python
from remnawave.models import UpdateUserRequestDto

# `telegram_id` is cleared, `email` is left untouched
await sdk.users.update_user(
    UpdateUserRequestDto(uuid=user_uuid, telegram_id=None)
)
```

Fields you do not pass are omitted from the payload, so the server's own defaults apply.

## Error handling

Every non-2xx response raises a subclass of `ApiError`. The exception class is derived from
the `httpCode` declared for that error code in the backend contract.

```python
from remnawave.exceptions import ApiError, NotFoundError, ConflictError

try:
    user = await sdk.users.get_user_by_uuid(uuid)
except NotFoundError as e:
    print(e.code, e.message)      # A025 User not found
except ConflictError:
    ...
except ApiError as e:
    print(e.status_code, e.error)
```

`remnawave.enums.ErrorCode` contains every error code of the contract; `ERROR_HTTP_CODES` and
`ERROR_MESSAGES` in `remnawave.enums.error_code` expose the declared status and default message.

## Webhooks

```python
from remnawave import RemnawaveSDK

sdk = RemnawaveSDK(base_url=..., token=...)

# `raw_body` must be the RAW request body (bytes or str) — re-serializing a parsed dict
# can change the byte string and break the signature check.
payload = sdk.webhook_utility.parse_webhook(raw_body, request_headers, webhook_secret)
if payload is None:
    ...  # invalid signature

if sdk.webhook_utility.is_user_event(payload.event):
    user = payload.data
    if payload.event == "user.expiration":
        # 2.8: single event replacing user.expires_in_*; hours are in meta
        print(payload.meta.expiration)
```

## What this fork changes

Relative to upstream at the time of forking, this branch aligns the SDK with the 2.8 contract:

- **Removed endpoints that no longer exist in 2.8** — `GET/PUT /xray`, `POST /inbounds/bulk/*`,
  `GET /sub/outline/...`, `POST /nodes/actions/reset-traffic`, `POST /auth/oauth2/tg/callback`,
  `GET /bandwidth-stats/nodes/realtime`.
- **`userUuid` → `userId` (number)** in HWID devices and subscription request history,
  plus the new `requestIp` field.
- **Hosts / nodes** — `tags[]`, `pinnedPeerCertSha256`, `verifyPeerCertByName`,
  `mihomoIpVersion`, `note`, `proxyUrl`, `nodeConsumptionMultiplier`; node `system`/`versions`
  objects replace the flat `xrayVersion`/`cpuCount`/… fields (kept as read-only properties).
- **Subscriptions** — `hwidCheckup` replaces `isHwidLimited`; `resolvedProxyConfigs` replaces
  `rawHosts`.
- **Response rules** — `encryption` (age1 / age1pq1), `disableHwidCheck`, `excludeHostsByTags`,
  `additionalExtendedClientsRegex`.
- **Nodes restart** — `forceRestart` is always sent in the request body.
- **Infra billing** — custom billing nodes (nullable `nodeUuid`/`node`), `billedAt`,
  list-shaped responses for history create/delete.
- **Error codes** regenerated from the contract (229 codes), and exceptions mapped from the
  declared `httpCode`.
- **Name collisions resolved** in `remnawave.models` — webhook models are prefixed `Webhook*`
  (old names remain available inside `remnawave.models.webhook`), and the duplicate
  `GetMetadataResponseDto` that silently broke `GET /api/system/metadata` is gone.
- **Serialization** switched from `exclude_none` to `exclude_unset`, so explicit `null` reaches
  the API.

Some of these are breaking changes for code written against the pre-2.8 SDK; they are
intentional, because the previous behaviour could not work against a 2.8 panel.

## Development

```bash
pip install -e .
pip install pytest pytest-asyncio pytest-mock python-dotenv pytz

# offline tests (2.8 contract regressions, models, enums, controller surface)
pytest tests/test_2_8_compliance.py tests/test_models_validation.py \
       tests/test_enums.py tests/test_controllers_completeness.py

# full suite — requires a live panel
#   REMNAWAVE_BASE_URL, REMNAWAVE_TOKEN and the REMNAWAVE_* fixtures in tests/conftest.py
pytest
```

## Credits

This SDK is a fork of the official
**[`remnawave/python-sdk`](https://github.com/remnawave/python-sdk)**, maintained by the
Remnawave community.

Upstream history:

- originally written by [@kesevone](https://github.com/kesevone);
- previously maintained by [@sm1ky](https://github.com/sm1ky) at
  [`sm1ky/remnawave-api`](https://github.com/sm1ky/remnawave-api);
- now maintained by the Remnawave community at
  [`remnawave/python-sdk`](https://github.com/remnawave/python-sdk).

The Remnawave panel itself lives at [`remnawave/backend`](https://github.com/remnawave/backend);
API documentation is at [docs.rw](https://docs.rw).

## License

MIT — see [LICENSE](LICENSE). The original license and copyright of the upstream project are
preserved.
