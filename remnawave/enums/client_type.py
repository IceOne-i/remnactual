from enum import StrEnum


class ClientType(StrEnum):
    """REQUEST_TEMPLATE_TYPE — значение `{clientType}` в `/api/sub/{shortUuid}/{clientType}`."""
    STASH = "stash"
    SINGBOX = "singbox"
    MIHOMO = "mihomo"
    XRAY_JSON = "json"
    V2RAY_JSON = "v2ray-json"
    CLASH = "clash"

    #: Историческое имя члена XRAY_JSON
    JSON = "json"
