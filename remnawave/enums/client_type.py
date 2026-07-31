from enum import StrEnum


class ClientType(StrEnum):
    """REQUEST_TEMPLATE_TYPE — значение `{clientType}` в `/api/sub/{shortUuid}/{clientType}`."""
    STASH = "stash"
    SINGBOX = "singbox"
    MIHOMO = "mihomo"
    JSON = "json"
    V2RAY_JSON = "v2ray-json"
    CLASH = "clash"
