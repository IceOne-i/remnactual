# Remnawave Python SDK — fork

[![PyPI](https://img.shields.io/pypi/v/remnactual?logo=pypi&logoColor=white&label=pypi)](https://pypi.org/project/remnactual/)
[![Python](https://img.shields.io/pypi/pyversions/remnactual?logo=python&logoColor=white)](https://pypi.org/project/remnactual/)
[![License](https://img.shields.io/github/license/IceOne-i/remnactual?color=44cc11)](https://github.com/IceOne-i/remnactual/blob/production/LICENSE)
[![Publish](https://img.shields.io/github/actions/workflow/status/IceOne-i/remnactual/upload.yml?logo=githubactions&logoColor=white&label=publish)](https://github.com/IceOne-i/remnactual/actions/workflows/upload.yml)
[![Fork of remnawave/python-sdk](https://img.shields.io/badge/fork%20of-remnawave%2Fpython--sdk-24292f?logo=github)](https://github.com/remnawave/python-sdk)

[![Remnawave panel](https://img.shields.io/badge/Remnawave%20panel-%E2%89%A5%203.0.0-1f6feb)](https://remna.st)
[![Backend contract](https://img.shields.io/badge/backend--contract-3.2.0-1f6feb)](https://github.com/remnawave/backend/tree/3.2.0/libs/contract)
[![Endpoints](https://img.shields.io/badge/endpoints-192-1f6feb)](https://github.com/IceOne-i/remnactual#controllers)
[![Models](https://img.shields.io/badge/models-645-1f6feb)](https://github.com/IceOne-i/remnactual#controllers)
[![API docs](https://img.shields.io/badge/API%20docs-docs.rw-1f6feb)](https://docs.rw/api)

[![Pydantic v2](https://img.shields.io/badge/pydantic-v2-e92063?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![httpx](https://img.shields.io/badge/httpx-async-0e7c86)](https://www.python-httpx.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

Asynchronous Python client for the **[Remnawave](https://remna.st)** panel API, built on
`httpx` + `pydantic` v2, with `orjson` for fast serialization.

> [!IMPORTANT]
> **This is a fork of [`remnawave/python-sdk`](https://github.com/remnawave/python-sdk).**
> It is published to PyPI as **`remnactual`** (the upstream `remnawave` project belongs to the
> Remnawave community). The import name is unchanged — `import remnawave`.
> The fork exists to track the Remnawave 3.x API closely and to fix the divergences that
> the migration from 2.7.x left behind — see [What this fork changes](#what-this-fork-changes).
> Attribution for the original work is at the [bottom of this file](#credits).

---

## Compatibility

| SDK version | Remnawave panel | Backend contract |
| ----------- | --------------- | ---------------- |
| 3.2.0       | >= 3.0.0        | `@remnawave/backend-contract` 3.2.0 |
| 3.0.0       | >= 3.0.0        | `@remnawave/backend-contract` 3.0.0 |
| 2.8.1       | >= 2.8.0, < 3.0 | `@remnawave/backend-contract` 2.8.35 |

Every endpoint, request body and response model in this fork is verified against
`libs/contract` of [`remnawave/backend`](https://github.com/remnawave/backend) at tag `3.2.0`.

> 3.1 and 3.2 are purely additive, so the panel floor stays at 3.0.0: the fields they added
> are optional here and simply stay `None` against an older panel. `GET /system/configuration`
> of course needs a panel on 3.2.0.

> Remnawave 3.0 is **not** backwards compatible with 2.8 — users are identified by a numeric
> `id` instead of a `uuid`, `/api/ip-control` became `/api/connections`, and many endpoints
> answer with an empty body. Pin `2.8.1` if your panel is still on the 2.8 line.

**Requirements:** Python >= 3.11, < 3.15.

## Installation

```bash
pip install remnactual
```

The import name stays `remnawave`:

```python
from remnawave import RemnawaveSDK
```

Straight from git:

```bash
pip install "git+https://github.com/IceOne-i/remnactual.git@production"
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
        # 3.0: users are identified by a numeric id; there is no `uuid` field any more
        print(user.id, user.username, user.status, user.expire_at)


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
| `sdk.users` | CRUD, lookups by id / short-uuid / username, actions (incl. `extend`), tags, `stream` (cursor pagination + filters), accessible nodes |
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
| `sdk.connections` | Per-user / per-node connection jobs, drop connections (was `sdk.ip_control`) |
| `sdk.node_plugins` | Node plugins, executor, torrent-blocker reports |
| `sdk.infra_billing` | Providers, billing nodes, billing history |
| `sdk.bandwidthstats` | Per-node and per-user bandwidth stats (incl. legacy endpoints) |
| `sdk.system` | Stats, digest, HTTP counters, health, metrics, recap, configuration, x25519, SRR matcher |
| `sdk.auth` / `sdk.passkeys` / `sdk.api_tokens_management` | Login, OAuth2, passkeys, scoped API tokens |
| `sdk.remnawave_settings` / `sdk.snippets` / `sdk.keygen` / `sdk.metadata` | Panel settings, snippets, node secret key, user/node metadata |
| `sdk.webhook_utility` | Webhook signature validation and payload parsing |

## Request bodies and `null`

Request models are serialized with `model_dump(exclude_unset=True)`, i.e. **exactly the fields
you set are sent**. Several fields can only be cleared by sending an explicit `null`:

```python
from remnawave.models import UpdateUserBodyDto

# `telegram_id` is cleared, `email` is left untouched
await sdk.users.update_user(
    UpdateUserBodyDto(id=user_id, telegram_id=None)
)
```

Fields you do not pass are omitted from the payload, so the server's own defaults apply.

## Endpoints without a response body

In 3.0, 43 endpoints answer `204 No Content` or `202 Accepted` with an empty body: every
`DELETE`, the asynchronous bulk operations, node restarts, squad membership changes and the
plugin executor. Their SDK methods return `None` — success is "no exception raised", and
affected-row counts are no longer reported by the API.

```python
await sdk.users.delete_user(user_id)          # -> None (204)
await sdk.users_bulk_actions.bulk_delete_users(
    BulkDeleteUsersBodyDto(user_ids=[1, 2, 3])
)                                             # -> None (204)
await sdk.nodes.restart_node(node_uuid, RestartNodeBodyDto(force_restart=True))  # -> None (202)
```

## Error handling

Every non-2xx response raises a subclass of `ApiError`. The exception class is derived from
the `httpCode` declared for that error code in the backend contract.

```python
from remnawave.exceptions import ApiError, NotFoundError, ConflictError

try:
    user = await sdk.users.get_user_by_id(user_id)
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
        # single event replacing user.expires_in_*; hours are in meta
        print(payload.meta.expiration)
```

## What this fork changes

This fork tracks the Remnawave API closely and fixes the divergences each upstream migration
left behind.

### Migration to 3.1 / 3.2

Both releases are additive — no endpoint, path or field was renamed or removed.

- **Nodes carry a numeric `id`** next to the `uuid`, on `NodeResponseDto` and on the webhook
  node model (`data.id` of node events, `data.node.id` of torrent-blocker events). Node routes
  still take `{uuid}`.
- **Subscription request history reports the matched SRR rule** — `srrResponseType` and
  `srrRuleName` on both `GET /subscription-request-history` and
  `GET /users/{userId}/subscription-request-history`.
- **Added** — `GET /system/configuration` (`sdk.system.get_configuration()`), with the
  `system:configuration` token scope.
- **Renamed** — the contract's constant for error `A084` became
  `BULK_DELETE_USERS_BY_USER_IDS_ERROR` (the code and its HTTP status are unchanged); the old
  `BULK_DELETE_USERS_BY_UUID_ERROR` name stays as an alias of the same member.
- The `preStart` node plugin needs no SDK change — the contract types `pluginConfig` as
  `unknown`, so it stays an untyped mapping here.

### Migration to 3.0

- **Users are identified by a numeric `id`.** The `uuid` field is gone from the user model, all
  `{uuid}` path params became `{userId}` (integers), and bulk bodies take `userIds`.
- **`/api/ip-control` became `/api/connections`** — `sdk.ip_control` is now `sdk.connections`,
  with `by-user` / `by-node` jobs and `drop`.
- **43 endpoints answer with an empty body** (204/202) and their methods return `None`;
  the `Delete*ResponseDto` / `Bulk*ResponseDto` models were removed.
- **Removed upstream, removed here** — `GET /users/by-email`, `/by-tag`, `/by-telegram-id`,
  `/by-id`, both legacy bandwidth-stats endpoints, the `docs` object of `GET /tokens`, and the
  `profileTitle` / `profileUpdateInterval` / `supportLink` / `isProfileWebpageUrlEnabled` /
  `happAnnounce` / `happRouting` subscription settings (they moved to response headers).
- **Added** — `POST /users/{userId}/actions/extend`, `POST /tokens/ott`,
  `GET /system/stats/digest`, `GET /system/stats/http`, `POST /bandwidth-stats/nodes/usage`,
  internal-squad usage stats and targeted squad membership bulk actions,
  `GET /subscriptions/by-id/{userId}`.
- **Renamed** — `keygen` returns `secretKey` instead of `pubKey`; external squads split
  `responseHeaders` into `responseHeadersAdd` / `responseHeadersRemove`; request models follow
  the contract's `*BodyDto` naming, with the old `*RequestDto` names kept as aliases.

### Earlier: 2.8 compliance

- Removed the endpoints 2.8 dropped (`/xray`, `/inbounds/bulk/*`, `/sub/outline/...`,
  `POST /nodes/actions/reset-traffic`, `POST /auth/oauth2/tg/callback`,
  `GET /bandwidth-stats/nodes/realtime`).
- `userUuid` → `userId` in HWID devices and subscription request history; `hwidCheckup`
  replaced `isHwidLimited`; `resolvedProxyConfigs` replaced `rawHosts`.
- Error codes regenerated from the contract, exceptions mapped from the declared `httpCode`.
- Name collisions in `remnawave.models` resolved (webhook models are prefixed `Webhook*`).
- Serialization switched from `exclude_none` to `exclude_unset`, so an explicit `null` reaches
  the API; keys the contract requires unconditionally are always emitted.

## Development

The project is managed with [uv](https://docs.astral.sh/uv/) — there is no lock file, because
a library should resolve against whatever its consumers already have.

```bash
uv sync --group dev

# offline tests (3.0 contract regressions, models, enums, controller surface)
uv run pytest tests/test_3_0_compliance.py tests/test_models_validation.py \
              tests/test_enums.py tests/test_controllers_completeness.py

# full suite — requires a live panel
#   REMNAWAVE_BASE_URL, REMNAWAVE_TOKEN and the REMNAWAVE_* fixtures in tests/conftest.py
uv run pytest

# build locally — the version comes from the git tag
uv build
```

## Releasing

The version lives in exactly one place: **the git tag**. `pyproject.toml` carries no version
number — `hatch-vcs` derives it from `git describe` at build time, so a release
is a single action:

```bash
git tag v3.0.1
git push origin v3.0.1
```

Pushing to a branch never publishes anything. The `Publish Python Package` workflow then builds
the wheel and sdist (their version comes straight from the tag), runs the offline test suite,
asserts that the built version equals the tag, publishes to PyPI via Trusted Publishing
(OIDC — no tokens), and finally creates the GitHub Release with the artifacts attached.

Between tags the version is a PEP 440 development version derived from the last tag, e.g.
`3.0.1.post7.dev0+g1a2b3c4`, and `remnawave.__version__` reports whatever was installed:

```python
import remnawave
print(remnawave.__version__)
```

To rehearse without touching PyPI: Actions → *Publish Python Package* → *Run workflow* →
target `testpypi`.

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
